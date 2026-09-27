# E008: is drift unavoidable in a continuum representation, and does snapping to a finite codebook stop it? Registration

Status: **Registered** (2026-09-27), after the pilot on seeds 1-3 (`results/exploratory/E008_pilot.md`)
and before any run on the registered seeds 21-23.

## Why

A document received today ("Constitutional Geometry", reviewed in
`docs/reviews/2026-09-27_constitutional_geometry.md`) claims, as its Drift Lemma, that evolution in a
continuum representation must drift in holonomy and curvature **unless** states are restricted to a
finite set. It uses that lemma to argue that a finite-state structure is **necessary**. The claim can be
tested directly on this instrument. It splits into two separate claims:

1. **Rounding drift.** An exact continuum representation, run in floating point, drifts until it fails.
2. **Model-error drift.** Slightly wrong operators accumulate error. Restricting the state to a finite set
   ("sector restriction"), here by snapping to the nearest of a finite codebook, stops the
   accumulation.

We expect claim 1 to fail at any practical horizon and claim 2 to hold. The second is useful for
veritas-holo: learned operators are never exact.

## Frozen setup

S5 by t and c. Operators are V P_g V† (P_g is the 5 × 5 permutation matrix, V a Haar unitary), in
float64. Random words; decode by the nearest of the 120 class matrices V P V†. The code is `core.py`
(the pilot code, unchanged). "δ-perturbed" means each operator is multiplied by exp(iδH), with H a
random Hermitian matrix drawn from the seed. Seeds 21, 22 and 23. The runner is `run.py`.

## Registered predictions

- **F1 (rounding drift is real but negligible)** Exact operators, no snapping, 8 words at L = 1e6: max
  deviation from the true class matrix < 1e-8 and decoding accuracy 1.0, on every seed. The deviation
  at L = 1e5 divided by the deviation at L = 1e3 lies between 10 and 1000 on every seed: drift grows,
  and stays far below the decoding margin.
- **F2 (model-error drift is real)** δ = 1e-2, no snapping, 32 words at L = 1e4: accuracy ≤ 0.2 on
  every seed.
- **F3 (snapping stops it)** The same δ, snapping to the nearest class matrix every step, 32 words at
  L = 1e5: accuracy 1.0 and final deviation 0, on every seed.
- **F4 (snapping is not magic; the null)** δ = 0.1, snapping every 10 steps, 32 words at L = 1e4:
  accuracy ≤ 0.2 on every seed. Snapping works only if it happens before the error crosses the
  decoding margin. With δ = 0.1 and snapping every step: accuracy 1.0 on every seed.

## Limits

- One group, a synthetic noise model, one precision (float64). The codebook here is exact. Learned
  operators (E005) need a codebook built from data; that is E008-U1.
- F1 speaks to rounding drift in this setting. It says nothing about chaotic continuum dynamics, where
  errors grow exponentially.
