# E006 pilot (exploratory; seeds 21-40, disjoint from every registered seed)

E005's training, unitary arm only, 20 seeds. For each run: the relator score (the minimum, over
E005's five relator words, of the number of eigenvalues of the learned relator matrix within 1e-2 of 1,
out of 8), computed from the trained operators alone; then the test accuracy at L = 160. Raw lines are
in the two `.jsonl` files next to this one.

| score | runs | reached ≥ 0.99 at L = 160 |
|---|---|---|
| 1 | 2 | 0 |
| 2 | 2 | 0 |
| 3 | 1 | 0 |
| 4 | 3 | 2 (seeds 27, 38); seed 24 failed at 0.128 |
| 6 | 8 | 8 |
| 7 | 2 | 2 |
| 8 | 2 | 2 |

Overall 14 of 20 succeeded (0.70). With the threshold at 5, 12 runs are accepted and all 12 succeed.
Two successful runs are rejected (score 4). With the threshold at 4, 15 are accepted, 14 succeed, and
seed 24 is a false accept.

A correction to what was said in conversation before this file was written: after the first 10 seeds
it was reported that "all 6 runs with a score of 4 or more were perfect". That was wrong. There were
7 such runs, and seed 24 (score 4) failed. Score 4 is the ambiguous band.
