# E009: a blind check that training worked, and half-precision execution. Registration

Status: **Registered** (2026-09-27), after the pilot on seeds 401-420
(`results/exploratory/E009_pilot.md`) and before any run on the registered seeds 501-540.

## Question

E006's check predicted success, but it used S5's known relations. The pilot suggests a check that
uses only the training data: the **training-consistency residual**. It is the mean, over training
labels, of the average distance between each training word's holonomy and the mean holonomy of the
words with that label. Operators that represent the group map all words of a label to one matrix,
giving a residual near 0 (or small, if part of the space is unused). Operators that do not, do not.

Second question, for running on the phone: do the learned operators survive **half-precision
execution** over long sequences?

## Frozen setup

- Training exactly as E005 (8 × 8 unitary, 510 words of length ≤ 8, 3000 steps). `core.py` and
  `pilot_common.py` are as used in the pilot.
- **Residual threshold 0.32** (the middle of the pilot's gap, 0.275-0.366). ACCEPT if the residual is
  below 0.32. The residual is computed from training words only, before any test word is generated.
- Success = test accuracy ≥ 0.99 at L = 160 (float64, the nearest-centroid readout as in E005).
- **float16 execution:** the operators and the running state are rounded to float16 (real and
  imaginary parts) after every step; 400 test words at L = 10000; same readout.
- Seeds 501-540.

## Registered predictions

- **B1 (precision)** At least 95% of ACCEPTED runs succeed.
- **B2 (rejects)** At most 10% of REJECTED runs succeed.
- **B3 (not trivial)** At least 5 runs are accepted and at least 5 rejected.
- **B4 (half precision)** Every successful run scores ≥ 0.99 at L = 10000 under float16 execution.

## Limits

- The residual uses training labels. It is blind to the group's relations, not blind to supervision.
- One group, one width. float16 is simulated by rounding in NumPy; it is not measured on phone
  hardware.
