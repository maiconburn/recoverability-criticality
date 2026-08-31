"""Symbolic derivation check: the task-exponent ladder {p-1, 2p-2, 2p-1}
equals the leading s-orders of inverse-Vandermonde row norms.

Model tangents in the monomial basis t^k e^{-i mu t}:
  amplitude direction of node j: column (delta_j^k / k!)_k
  frequency direction of node j: A_j * column shifted by one order
Task A uses the plain p x p Vandermonde (frequencies known); tasks B and
C use the confluent 2p x 2p system (everything free). With a generic
positive-definite Gram on monomials, CRB(param) ~ ||row of V^-1||, so
the exponent is the most negative s-order in that row.

Predicted: task A rows -> -(p-1); frequency rows -> -(2p-2);
amplitude rows (confluent) -> -(2p-1).
"""
import sympy as sp

s = sp.symbols("s", positive=True)


def leading_order(expr):
    e = sp.simplify(expr)
    if e == 0:
        return None
    pow_ = sp.degree(sp.fraction(sp.together(e))[1], s) * -1 + \
        sp.degree(sp.fraction(sp.together(e))[0], s)
    # robust: use series at s->0 via sp.limit of log-ratio is heavy;
    # instead find n with finite nonzero limit of e/s^n
    for n in range(-12, 13):
        lim = sp.limit(e / s**n, s, 0)
        if lim.is_finite and lim != 0:
            return n
    return None


def row_orders(V):
    Vi = V.inv()
    orders = []
    for i in range(Vi.rows):
        best = None
        for j in range(Vi.cols):
            n = leading_order(Vi[i, j])
            if n is not None:
                best = n if best is None else min(best, n)
        orders.append(best)
    return orders


for p, us, As in [(2, [1, -1], [1, 2]),
                  (3, [1, -1, 2], [1, 2, 3])]:
    deltas = [s * u for u in us]

    # Task A: plain Vandermonde, monomials 0..p-1
    V = sp.Matrix(p, p, lambda k, j: deltas[j] ** k / sp.factorial(k))
    ordA = row_orders(V)
    print(f"p={p} task A (plain V) row orders: {ordA}  "
          f"predicted -(p-1) = {-(p - 1)}", flush=True)

    # Confluent system: 2p columns (amp_j, freq_j), monomials 0..2p-1
    n = 2 * p
    cols = []
    for j in range(p):
        cols.append([deltas[j] ** k / sp.factorial(k) for k in range(n)])
    for j in range(p):
        cols.append([sp.Integer(0)] + [
            As[j] * deltas[j] ** (k - 1) / sp.factorial(k - 1)
            for k in range(1, n)])
    Vc = sp.Matrix(cols).T
    orders = row_orders(Vc)
    amp_rows, freq_rows = orders[:p], orders[p:]
    print(f"p={p} confluent: amplitude rows {amp_rows}  "
          f"predicted -(2p-1) = {-(2 * p - 1)}", flush=True)
    print(f"p={p} confluent: frequency rows {freq_rows}  "
          f"predicted -(2p-2) = {-(2 * p - 2)}", flush=True)

print("done", flush=True)
