# E005: results

Registered in `PREREG.md` (commit ba16d68) after a pilot on the disjoint seeds 11-16. The code was
committed before the registered run. **6 of 6 held on x86_64.**

## Output (pasted verbatim, x86_64)

```
VERITAS-HOLO E005 | seeds 1 2 3 4 5 | x86_64 | Python 3.11.15 | NumPy 2.4.4
training: all 510 words of length 1-8; operators 8x8 unitary; test at L = 40 and 160
relators are the identity under the exact S5 representation: t^2 yes, c^5 yes, (tc)^4 yes, (t c^-1 t c)^3 yes, (t c^-2 t c^2)^2 yes
seed  learned 40  learned 160  diag 40  diag 160  ceil 40  ceil 160  init 40  init 160  min eig~1  train s
   1      1.0000       1.0000   0.0155    0.0145   0.0230    0.0135   0.0100    0.0060       6/8      116
   2      0.3960       0.0220   0.0205    0.0145   0.0230    0.0160   0.0070    0.0060       3/8      117
   3      1.0000       1.0000   0.0175    0.0195   0.0135    0.0165   0.0065    0.0040       7/8      117
   4      0.9065       0.0845   0.0190    0.0185   0.0180    0.0135   0.0110    0.0110       1/8      117
   5      1.0000       1.0000   0.0240    0.0185   0.0180    0.0180   0.0075    0.0045       4/8      119
HELD   L1  3 of 5 seeds reach >= 0.99 at L=160 (need >= 3)
HELD   L2  those seeds at L=40: 1.0000, 1.0000, 1.0000 (all >= 0.99)
HELD   L3  learned diagonal max excess over count ceiling +0.0060 (<= +0.02)
HELD   L4  untrained max 0.0110 (< 0.05)
HELD   L5  max ||U'U - I|| 2.62e-13 (< 1e-10)
HELD   L6  successful seeds' min relator eigenvalues near 1: 6, 7, 4 (each >= 4 of 8)
VERDICT  6 of 6 registered predictions held
```

Record: `results/verified/E005_x86_64.json`. Run with `--jobs 5`. Training takes about 117 s per seed
for the unitary arm, plus the same again for the diagonal arm.

## What this shows

- **Gradient descent learned to track S5 from short examples and extrapolated 20×.** It saw only the
  510 words of length ≤ 8, labelled by their permutation, and was never given the group's relations.
  On 3 of 5 seeds the learned 8 × 8 operators score 1.0000 on fresh words of length 40 and 160.
- **The learned operators satisfy the registered S5 relations on part of the space, although no
  relation was supplied during training.** On the successful seeds, each of the five registered
  relator words has at least 4 of its 8 eigenvalues within 1e-2 of 1 (6, 7 and 4). The failed seeds
  reached only 3 and 1. That points to a representation of the group in part of the space rather than
  a memorised lookup of the training words. The eigenvalue count is the evidence; "represents the
  group" is the interpretation.
- **Commuting operators trained the same way cannot do it.** The diagonal arm sits at the
  letter-count ceiling on every seed (at most +0.0060 above it), as the theory says it must.
- **Training did the work.** The same operators before training score at most 0.0110 (chance is
  0.0083).

## Limits

- **2 of 5 seeds failed** (0.0220 and 0.0845 at L = 160). Both also had few relator eigenvalues near 1
  (3 and 1), so failure shows up in the operators themselves, before any test. That is what E005-U1
  will use: choose among restarts without test data.
- A 120-state lookup table does this exactly. The result concerns what training finds, not an
  advantage over classical computation.
- The readout is fitted on labelled long words; only the operators are trained on short words.
- One group, one width.

## S25, seed 1 only (2026-09-27, pasted by the operator)

```
VERITAS-HOLO E005 | seeds 1 | aarch64 | Python 3.14.6 | NumPy 2.4.4
seed  learned 40  learned 160  diag 40  diag 160  ceil 40  ceil 160  init 40  init 160  min eig~1  train s
   1      1.0000       1.0000   0.0155    0.0145   0.0230    0.0135   0.0100    0.0060       6/8       37
FAILED L1  1 of 1 seeds reach >= 0.99 at L=160 (need >= 3)
...
VERDICT  5 of 6 registered predictions held
```

Every value for seed 1 equals x86_64's, including the relator count (6/8). The "FAILED L1" is not a
result. L1 is registered over the five seeds together, and one seed cannot reach 3 of 5. The runner
said so badly: it now prints `PARTIAL L1 ... not evaluated` on a partial run, and leaves L1 out of the
count. The seed-1 training took 37 s on the S25 against 116 s on x86_64 with 5 jobs in parallel.
