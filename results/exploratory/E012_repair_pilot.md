# Can relator projection repair a failed training run? Exploratory, not registered: no

E012's open door: apply E012's projection (orders 2, 5, 4 for t, c and tc; 20 rounds) to operators
learned as in E005/E006, and score them again at L = 160. Seeds 21-40 (E006's pilot seeds).
Script: `E012_repair_pilot.py`; rows: `E012_repair_pilot_seeds21-40.jsonl`.

- **Failed runs: 0 of 6 repaired.** Seeds 21, 23, 24, 30, 34 and 35 scored 0.007-0.128 at L = 160 after
  projection, against 0.0085-0.128 before.
- **Successful runs: 14 of 14 still exact** (1.0 before and after).
- E006's relator score did not move in any of the 20 runs.

**Reading.** A failed run is not a noisy copy of a representation: projection moved it (Frobenius
distance 0.20-0.44) without reaching a working one. E012's method repairs operator *error*. It does
not repair a wrong *structure*, so failed training still needs a restart (E006's policy). This is
recorded so that nobody tries it again expecting a different result on these seeds. It was never
registered, and it is not a claim.
