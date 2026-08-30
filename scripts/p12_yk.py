"""P12'': full probabilistic Yoshida-Kitaev decoder + Petz bridge.
Frozen in FROZEN_P12_P13.md. Gates unit-tested (house rule)."""
import json
import pathlib

import numpy as np
from scipy.linalg import expm, sqrtm

I2 = np.eye(2); X = np.array([[0,1],[1,0]]); Z = np.array([[1,0],[0,-1]])
def kron(*ops):
    out = np.array([[1.0+0j]])
    for o in ops: out = np.kron(out, o)
    return out

N = 8   # [REF, M, L1, L2, R1, R2, M2, Mt]
REF, M, L1, L2, R1, R2, M2, Mt = range(8)

def apply(Us, idxs, v):
    k = len(idxs)
    t = v.reshape([2]*N)
    rest = [j for j in range(N) if j not in idxs]
    t = np.transpose(t, idxs + rest).reshape(2**k, -1)
    t = (Us @ t).reshape([2]*N)
    inv = np.argsort(idxs + rest)
    return np.transpose(t, inv).reshape(-1)

# unit tests
v = np.zeros(2**N, dtype=complex); v[0] = 1.0
w = apply(X, [3], v); assert int(np.argmax(np.abs(w))) == 2**(N-1-3)
w = apply(kron(X, X), [1, 6], v)
assert int(np.argmax(np.abs(w))) == 2**(N-1-1) + 2**(N-1-6)
print("apply() unit tests: PASS", flush=True)

def scrambler(steps, J=1.0, hx=1.05, hz=0.5):
    def opn(o, i):
        return kron(*[o if j==i else I2 for j in range(3)])
    HZZ = sum(opn(Z,i)@opn(Z,i+1) for i in range(2))
    HX = sum(opn(X,i) for i in range(3)); HZ = sum(opn(Z,i) for i in range(3))
    Uz = expm(-1j*(J*HZZ + hz*HZ)); Ux = expm(-1j*hx*HX)
    U = np.eye(8, dtype=complex)
    for _ in range(steps): U = Ux@Uz@U
    return U

bell = np.zeros(4, dtype=complex); bell[0]=bell[3]=1/np.sqrt(2)
base = np.kron(np.kron(np.kron(bell, bell), bell), bell)
cur = [REF, M, L1, R1, L2, R2, M2, Mt]
perm = [cur.index(q) for q in range(8)]
psi0 = np.transpose(base.reshape([2]*8), perm).reshape(-1)

phip = bell.copy()
P_bell = np.outer(phip, phip.conj())   # 4x4 projector onto |phi+>

def project_bell(v, i, j):
    """Project qubits (i, j) onto |phi+>; return unnormalized state."""
    t = v.reshape([2]*N)
    rest = [q for q in range(N) if q not in (i, j)]
    t2 = np.transpose(t, [i, j] + rest).reshape(4, -1)
    t2 = P_bell @ t2
    t2 = t2.reshape([2]*N)
    inv = np.argsort([i, j] + rest)
    return np.transpose(t2, inv).reshape(-1)

def reduced(psi, keep):
    t = psi.reshape([2]*N)
    rest = [j for j in range(N) if j not in keep]
    Mx = np.transpose(t, keep+rest).reshape(2**len(keep), -1)
    return Mx @ Mx.conj().T

def fidelity_bell(rho4):
    return float(np.real(phip.conj() @ rho4 @ phip))

def yk(steps):
    U = scrambler(steps)
    v = apply(U, [M, L1, L2], psi0)
    v = apply(U.conj(), [M2, R1, R2], v)
    v = project_bell(v, L1, R1)
    v = project_bell(v, L2, R2)
    p = float(np.real(np.vdot(v, v)))
    if p < 1e-12:
        return 0.0, p
    r = reduced(v/np.sqrt(p), [REF, Mt])
    return fidelity_bell(r), p

def petz_channel_fid(steps):
    """Petz recoverability of the channel M -> R side (R1,R2,M2), no decode.
    Channel via Choi from the protocol state before any projection."""
    U = scrambler(steps)
    v = apply(U, [M, L1, L2], psi0)
    v = apply(U.conj(), [M2, R1, R2], v)
    # Choi of channel REF->(R side): the (REF, R1, R2, M2) reduced state IS
    # (1/2 x channel)(|phi+><phi+|) since REF-M was Bell.
    rho = reduced(v, [REF, R1, R2, M2])   # 16x16, order [REF, R...]
    # entanglement fidelity of the Petz-recovered channel:
    # F_petz = F(id ⊗ (P∘E) |phi+>) with P the Petz map of E w.r.t. max mixed.
    # Compute E from Choi: rho = sum_{ij} |i><j|_REF/2 ⊗ E(|i><j|)
    rho_t = rho.reshape(2, 8, 2, 8)
    E = np.zeros((2,2,8,8), dtype=complex)
    for i in range(2):
        for j in range(2):
            E[i,j] = 2*rho_t[i,:,j,:]
    # E(rho_in) = sum_ij rho_in[i,j] * E[i,j]... wait indices: E(|i><j|) = E[i,j]
    sigma = 0.5*(E[0,0] + E[1,1])   # E(I/2)
    s_inv_h = np.linalg.pinv(sqrtm(sigma))
    # Petz: P(y) = (1/2)^{1/2}... reference = I/2: P(y) = sqrt(rho_ref) A† ... 
    # P(y) = (I/2)^{1/2} E†(sigma^{-1/2} y sigma^{-1/2}) (I/2)^{1/2}
    # E†(y)[i,j] = Tr(E[j,i]... adjoint: <E†(y)|i><j|> = Tr(y† E(|i><j|))?
    # E†(y) matrix elements: (E†(y))[j,i] = Tr(E[i,j]^† y)? use def:
    # Tr(E(x)† y) = Tr(x† E†(y)). With x=|i><j|: E(x)=E[i,j] =>
    # Tr(E[i,j]† y) = (E†(y))[i,j]... careful: Tr(x† E†(y)) with x=|i><j| is
    # (E†(y))[j,i]?? Tr(|j><i| A) = A[i,j]. x† = |j><i| -> Tr = E†(y)[i,j].
    def E_dag(y):
        out = np.zeros((2,2), dtype=complex)
        for i in range(2):
            for j in range(2):
                out[i,j] = np.trace(E[i,j].conj().T @ y)
        return out
    def petz(y):
        mid = s_inv_h @ y @ s_inv_h
        return 0.5*E_dag(mid)   # sqrt(I/2)*...*sqrt(I/2) = (1/2)*E†(mid)
    # entanglement fidelity of P∘E: F = <phi+| (id ⊗ P∘E)(|phi+><phi+|) |phi+>
    # (id⊗PE)(phi+) = (1/2) sum_ij |i><j| ⊗ P(E(|i><j|))
    out = np.zeros((4,4), dtype=complex)
    for i in range(2):
        for j in range(2):
            pe = petz(E[i,j])
            out += 0.5*np.kron(np.outer(np.eye(2)[i], np.eye(2)[j]), pe)
    return fidelity_bell(out)

rows = []
for steps in (1, 2, 4, 8):
    Fyk, p = yk(steps)
    Fp = petz_channel_fid(steps)
    rows.append([steps, Fyk, p, Fp])
    print(f"steps={steps}: F_YK={Fyk:.4f} (p_succ={p:.4f})  F_Petz={Fp:.4f}", flush=True)
rows = np.array(rows)
F8, p8 = rows[-1,1], rows[-1,2]
print(f"P12''.1: F={F8:.4f}, p_succ={p8:.4f} ->",
      "CONFIRMED" if (F8 > 0.8 and 1/32 <= p8 <= 1/4) else ("KILLED" if F8 <= 0.5 else "inconclusive"), flush=True)
c = np.corrcoef(rows[:,1], rows[:,3])[0,1]
ratio_ok = bool(np.all(rows[:,1] >= 0.5*rows[:,3]))
near = bool(np.all(rows[:,1] >= 0.9*rows[:,3] - 1e-9)) 
print(f"P12''.2: corr(F_YK, F_Petz) = {c:.4f}; min F_YK/F_Petz = {np.min(rows[:,1]/np.maximum(rows[:,3],1e-12)):.3f}", flush=True)
print("P12''.2:", "CONFIRMED" if (c > 0.9 and ratio_ok) else ("KILLED" if (c < 0.5 or not ratio_ok) else "inconclusive"), flush=True)
json.dump(rows.tolist(), open("results/p12_yk.json","w"), indent=1)
print("done", flush=True)
