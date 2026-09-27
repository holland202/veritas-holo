# E008 pilot (exploratory; seeds 1-3, disjoint from the registered seeds 21-23)

S5's exact 5 × 5 permutation representation, conjugated by a random unitary V, so the operators are
generic complex matrices and every product accumulates floating-point rounding (float64). Words of
random t / c letters; decode by the nearest of the 120 exact class matrices (also conjugated by V).

| arm | L = 1e3 | L = 1e4 | L = 1e5 | L = 1e6 |
|---|---|---|---|---|
| exact operators, no snapping: max deviation from the true class matrix | 2.53e-13 | 2.48e-12 | 2.47e-11 | 3.95e-10 |
| same, decoding accuracy | 1.0 | 1.0 | 1.0 | 1.0 |
| operators perturbed by δ = 1e-2, no snapping: accuracy | 0.0625 | 0.0 | 0.03125 | |
| same δ, snap to the nearest class matrix every step | 1.0 | 1.0 | 1.0 | |
| same δ, snap every 10 steps | 1.0 | 1.0 | 1.0 | |

At L = 1e4, snapping every step held accuracy 1.0 for δ = 0.05, 0.1, 0.2 and 0.4. Snapping every 10
steps held for δ = 0.05 and failed (0.0) for δ ≥ 0.1. Snapping every 100 steps failed for every δ
tried. Rounding drift grows roughly linearly: about 2.5e-16 per step.
