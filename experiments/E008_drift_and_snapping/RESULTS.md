# E008: results

Registered in `PREREG.md` (commit fee6556) after the pilot on seeds 1-3. **4 of 4 held on x86_64
(Intel Xeon).**

## Output (pasted verbatim)

```
seed 21: F1_acc_1e6 1, F1_dev_1e6 6.481e-10, F1_dev_1e3 6.506e-13, F1_dev_1e5 6.482e-11, F2_acc 0.0625, F3_acc 1, F3_dev 0, F4_sparse_acc 0, F4_every_acc 1
seed 22: F1_acc_1e6 1, F1_dev_1e6 3.087e-10, F1_dev_1e3 3.114e-13, F1_dev_1e5 3.088e-11, F2_acc 0, F3_acc 1, F3_dev 0, F4_sparse_acc 0, F4_every_acc 1
seed 23: F1_acc_1e6 1, F1_dev_1e6 6.111e-10, F1_dev_1e3 6.127e-13, F1_dev_1e5 6.115e-11, F2_acc 0, F3_acc 1, F3_dev 0, F4_sparse_acc 0, F4_every_acc 1
VERITAS-HOLO E008 | seeds (21, 22, 23) | x86_64 | Python 3.11.15 | NumPy 2.4.4
HELD   F1  max dev at 1e6 6.48e-10, 3.09e-10, 6.11e-10; growth 1e3->1e5 99.6x, 99.2x, 99.8x
HELD   F2  no snapping, delta 1e-2, L 1e4: 0.0625, 0.0000, 0.0000
HELD   F3  snap every step, delta 1e-2, L 1e5: 1.0000 (dev 0), 1.0000 (dev 0), 1.0000 (dev 0)
HELD   F4  delta 0.1: snap every 10 0.0000, 0.0000, 0.0000; snap every step 1.0000, 1.0000, 1.0000
VERDICT  4 of 4 registered predictions held
```

## What this shows

- **Rounding drift in a continuum representation is real and negligible.** Exact S5 operators in a
  rotated complex basis, multiplied 10⁶ times in float64, stayed within 6.48e-10 of the true class
  matrix and decoded perfectly. The drift grows linearly: about 100× from 10³ to 10⁵ steps, which
  is about 6e-16 per step. At that rate it would reach the decoding margin after about 10¹⁵ steps.
  "Drift is unavoidable unless the state space is finite" does not hold at any practical horizon.
- **Operator error is what breaks a representation.** Operators off by δ = 1e-2 fell to chance within
  10⁴ steps (0.0625, 0, 0).
- **Snapping to a finite codebook removes that failure.** Projecting the running state onto the nearest
  of the 120 valid states after every step kept accuracy at 1.0 with zero deviation to 10⁵ steps,
  with the same wrong operators.
- **Snapping has to beat the error.** With δ = 0.1, snapping every 10 steps failed on every seed (0.0),
  while snapping every step succeeded (1.0). The codebook helps only if the state is corrected before
  it leaves the correct cell.

For veritas-holo, this means a learned representation that is almost right can track state over long
horizons, provided its running state is snapped to a codebook of valid states often enough. That is
E008-U1: build the codebook from data for E005's learned operators.
