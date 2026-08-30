"""P12: minimal Yoshida-Kitaev traversable wormhole vs Petz recoverability.
Frozen in results/FROZEN_P12_P13.md before this ran."""
import json
import pathlib
from itertools import product

import numpy as np

NQ = 3          # qubits per side
DIM = 2**NQ

I2 = np.eye(2); X = np.array([[0,1],[1,0]]); Y = np.array([[0,-1j],[1j,0]])
Z = np.array([[1,0],[0,-1]])

def kron(*ops):
    out = np.array([[1.0+0j]])
    for o in ops:
        out = np.kron(out, o)
    return out

def op_at(o, i, n=NQ):
    return kron(*[o if j == i else I2 for j in range(n)])

# deterministic kicked-Ising scrambler on NQ qubits
def scrambler(steps=6, J=1.0, hx=1.05, hz=0.5):
    HZZ = sum(op_at(Z, i) @ op_at(Z, i+1) for i in range(NQ-1))
    HX = sum(op_at(X, i) for i in range(NQ))
    HZ = sum(op_at(Z, i) for i in range(NQ))
    from scipy.linalg import expm
    Uz = expm(-1j*(J*HZZ + hz*HZ))
    Ux = expm(-1j*hx*HX)
    U = np.eye(DIM, dtype=complex)
    for _ in range(steps):
        U = Ux @ Uz @ U
    return U

U = scrambler()

# Bell pairs between L_i and R_i: |phi+>^{otimes NQ}, ordered L(0..2) R(0..2)
bell = np.zeros(4, dtype=complex); bell[0] = bell[3] = 1/np.sqrt(2)
state0 = np.array([1.0+0j])
for _ in range(NQ):
    state0 = np.kron(state0, bell)
# reorder from (L0R0 L1R1 L2R2) to (L0L1L2 R0R1R2)
def reorder(v):
    t = v.reshape([2]*(2*NQ))
    perm = [0, 2, 4, 1, 3, 5]
    return np.transpose(t, perm).reshape(-1)
psi_tfd = reorder(state0)

ZZ_LR = sum(kron(*[Z if j == i else I2 for j in range(NQ)],
                 *[Z if j == i else I2 for j in range(NQ)])
            for i in range(1, NQ))   # couple all EXCEPT the message/readout pair

from scipy.linalg import expm

def channel(g):
    """Effective channel: message qubit state -> readout qubit (R mirror of L0),
    via Choi/process tomography on the full protocol."""
    UL = kron(U, np.eye(DIM))
    URt = kron(np.eye(DIM), U.conj())
    C = expm(1j*g*ZZ_LR)
    total = URt @ C @ UL
    # build channel by inputting basis states rho_in on L0
    kets = {}
    for name, k in (("0", np.array([1,0])), ("1", np.array([0,1])),
                    ("+", np.array([1,1])/np.sqrt(2)),
                    ("i", np.array([1,1j])/np.sqrt(2))):
        # replace L0 half of its Bell pair with the message state:
        # project L0 of psi_tfd? Standard YK: swap message in. Build state:
        # psi = |m>_{L0} otimes rest, where rest = trace out L0 from TFD -> use
        # explicit: TFD = sum_s |s>_{L0}|s>_{R0}/sqrt2 otimes B_{12}; swapping
        # message in L0 leaves R0 maximally mixed purified by a reference we
        # drop -> effective input state:
        rest = np.zeros(2**(2*NQ - 1), dtype=complex)
        # rest lives on (L1 L2 R0 R1 R2): Bell(L1R1) Bell(L2R2) x mixed R0 ->
        # purify R0 with ancilla? Simplest faithful: keep reference qubit REF
        # entangled with R0: |phi+>_{REF,R0}. Total: REF + 6 qubits.
        pass
        kets[name] = k
    # -- do the REF construction once, outside loop
    return None

# The in-loop construction got complicated; do it cleanly here:
# System: REF (1) + L0 L1 L2 + R0 R1 R2  => 7 qubits, dim 128.
def run_protocol(g):
    from scipy.linalg import expm as e_
    # initial: |phi+>_{REF,R0} x Bell(L1,R1) x Bell(L2,R2); L0 = message slot
    # order qubits: [REF, L0, L1, L2, R0, R1, R2]
    def bell_pair(v, i, j, n=7):
        # v: state without qubits i,j? build full state directly instead
        pass
    # build by tensor construction: start with |0..0> amplitudes via kron of
    # pieces in a chosen order then permute.
    # pieces order: (REF,R0) bell, L0 placeholder |0>, (L1,R1) bell, (L2,R2) bell
    base = np.array([1.0+0j])
    base = np.kron(base, bell)          # REF,R0
    base = np.kron(base, np.array([1,0], dtype=complex))  # L0
    base = np.kron(base, bell)          # L1,R1
    base = np.kron(base, bell)          # L2,R2
    # current order: [REF, R0, L0, L1, R1, L2, R2] -> target [REF,L0,L1,L2,R0,R1,R2]
    t = base.reshape([2]*7)
    cur = ["REF","R0","L0","L1","R1","L2","R2"]
    tgt = ["REF","L0","L1","L2","R0","R1","R2"]
    perm = [cur.index(q) for q in tgt]
    psi0 = np.transpose(t, perm).reshape(-1)

    L_idx, R_idx = [1,2,3], [4,5,6]
    def op7(o, i):
        return kron(*[o if j == i else I2 for j in range(7)])
    UL = np.eye(128, dtype=complex)
    # embed U on qubits L0L1L2:
    def embed(Usmall, idxs):
        t = np.eye(128, dtype=complex).reshape([2]*14)
        # easier: build via kron in permuted basis
        # order [idxs..., rest...]:
        rest = [j for j in range(7) if j not in idxs]
        order = idxs + rest
        P = np.transpose(np.eye(128).reshape([2]*14),
                         axes=[*order, *[7+o for o in order]]).reshape(128,128)
        big = np.kron(Usmall, np.eye(2**(7-len(idxs))))
        return P.T @ big @ P
    ULs = embed(U, L_idx)
    URs = embed(U.conj(), R_idx)
    ZZ = sum(op7(Z, L_idx[i]) @ op7(Z, R_idx[i]) for i in range(1, NQ))
    C = e_(1j*g*ZZ)
    total = URs @ C @ ULs
    psi = total @ psi0
    # reduced state of (REF, R0): move kept axes to front, contract the rest
    t = psi.reshape([2]*7)
    keep = [0, 4]
    rest = [j for j in range(7) if j not in keep]
    M = np.transpose(t, keep + rest).reshape(4, 2**5)
    r2 = M @ M.conj().T
    phip = np.zeros(4, dtype=complex); phip[0] = phip[3] = 1/np.sqrt(2)
    F = float(np.real(phip.conj() @ r2 @ phip))
    return F, psi

gs = np.linspace(-1.5, 1.5, 41)
Fs = []
for g in gs:
    F, _ = run_protocol(g)
    Fs.append(F)
    print(f"g={g:+.3f}  F_tel={F:.4f}", flush=True)
Fs = np.array(Fs)
i0 = np.argmin(np.abs(gs))
istar = int(np.argmax(Fs))
print(f"F(0)={Fs[i0]:.4f}  max F={Fs[istar]:.4f} at g*={gs[istar]:+.3f}", flush=True)
print(f"P12.1: {'CONFIRMED' if (abs(gs[istar])>1e-9 and Fs[istar]-Fs[i0]>0.15) else 'KILLED'}", flush=True)
json.dump({"g": gs.tolist(), "F": Fs.tolist()},
          open("results/p12_teleport.json","w"), indent=1)
print("done", flush=True)
