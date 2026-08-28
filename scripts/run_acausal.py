"""(A) Halving law inside the acausal band: lambda = 0.095, 0.105."""
import sys, json
sys.path.insert(0, 'scripts')
import run_sweep as rs
rs.LADDER = [0.095, 0.105]
rs.OUT = rs.RESULTS / "sweep_acausal.json"
rs.main()
