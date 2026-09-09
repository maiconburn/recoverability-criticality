# P8-F4', the log channel as a confluent limit (mini-freeze, 2026-09-09)

Frozen BEFORE any fit. Re-analysis of the existing deterministic F3 gate
data (`results/p8f3_gate.json`: CosmoFlow squeezed shapes S(k_L) at
nu = 1 and nu = 0.85), motivated by the control-neutrality theorem
(`THEOREM_EP_NEUTRALITY.md`): the "Jordan log channel" x^{3/2} ln x at
nu = 1 is the confluent limit of two coalescing powers
{x^{1/2+nu}, x^{5/2-nu}} (the subleading branch of the leading tower
and the leading term of the subleading tower), exactly as
t e^{-i mu t} is the confluent limit of two damped exponentials. The
physical shape is analytic in nu through 1; the "log" is a basis
choice, not a separate dynamical channel. Two consequences are
testable on the F3 data without new compute:

P8-F4'.1 (the F3 gate failed on a basis artifact). With the nu-CORRECT
basis {x^{1/2-nu}, x^{1/2+nu}, x^{1/2+nu} ln x} at nu = 0.85 (the F3
gate used x^{3/2} at both nu, which forces the log term to mimic the
true x^{1.65} at nu = 0.85), the improvement factor R(0.85) is below 3,
while R(1) with {x^{-1/2}, x^{3/2}, x^{3/2} ln x} stays above 20, so
the localization ratio R(1)/R(0.85) exceeds 7.
KILL: R(0.85) > 10 with the correct basis (the log improvement is
generic slack unrelated to the basis; the F3 verdict stands as is).

P8-F4'.2 (mimicry by the confluent basis). At nu = 1, a log-free
three-power basis {x^{1/2-nu'}, x^{1/2+nu'}, x^{5/2-nu'}} with nu'
scanned in [0.95, 1.05] reaches a residual within a factor 2 of the
log basis for some nu' in the window (the log is reproduced by two
nearby powers, the Prony-mimicry of P16.1 in the scale variable).
KILL: no nu' in the window within a factor 2 (the log would be a
genuinely separate channel, contradicting the confluence picture and
the theorem's reading of P8).

Disposition if both hold: the F4 "survival of the log channel in the
interacting swept limit" question (the day-of-compute cloud run listed
in HANDOFF.md) is basis-dependent and is NOT run; what is physical and
already established is the analyticity of the shape in nu and the
finite mass-estimation error at nu = 1 (P8.1's CRB law is the labeled
two-component task, consistent with the Jacobian ladder). Recorded as
a theorem-driven closure, not as a measurement of the survival.
Fits: weighted least squares on relative residuals, same grid and
weights as the F3 gate (results/p8f3_gate.json).
