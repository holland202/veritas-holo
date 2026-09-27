# E004: results

Registered in `PREREG.md` (commit ce92251). The code was committed before the run.
**4 of 6 held on x86_64. G1 and G5 FAILED as registered; both failures are kept below.**

## What failed, first

- **G1 FAILED.** REP's minimum accuracy was 0.9985, on seed 2 at L = 10, where 1.0000 was
  registered. Cause, checked after the run: on that seed 0.0015 of the test words (3 of 2000) belong
  to a class that never appears among the training words. A nearest-centroid readout cannot name a
  class it has no centroid for. The representation itself is exact (`tests/test_e004.py` checks that
  every REP holonomy is its label's permutation matrix), so the flaw is in the readout I registered,
  not in the arm. At L = 40 and 160, REP scored 1.0000 on every seed.
- **G5 FAILED.** SHAM's accuracy at L = 40 was 0.0747 (seeds 0.069, 0.098, 0.057), against a
  registered < 0.05. Its relation checks came out as predicted: t² = 1 and c⁵ = 1 held to 1e-14, and
  (tc)⁴ = 1 was broken by at least 2.8356. At L = 160 it fell to chance (0.0070).
  **Exploratory diagnosis, not registered:** because the sham keeps t² = 1 and c⁵ = 1, every word
  collapses to a shorter "reduced word", and words with the same reduced word get the same
  holonomy. On a separate draw, 23% of test words at L = 40 had a reduced word already seen in
  training; at L = 160 the figure was 0%. So the sham recovers labels by recognising repeats, and
  that stops once reduced words stop repeating. The registered threshold did not allow for the
  relations the sham keeps.

## Output (pasted verbatim, x86_64)

```
VERITAS-HOLO E004 | seeds 1-3 | x86_64 | Python 3.11.15 | NumPy 2.4.4
S5 by t=(0 1), c=(0 1 2 3 4); order of tc = 4; 6000 train + 2000 test words per length; chance 1/120 = 0.0083
arm                 L=10      L=40     L=160   (mean test accuracy over seeds)
REP               0.9995    1.0000    1.0000
DIAG              0.0618    0.0188    0.0152
COUNT-CEILING     0.1930    0.0217    0.0175
RANDOM-U          0.4363    0.0072    0.0097
SHAM              0.9122    0.0747    0.0070
TABLE             1.0000    1.0000    1.0000
SHAM relations: max ||t^2-I|| 2.72e-15, max ||c^5-I|| 9.22e-15, min ||(tc)^4-I|| 2.8356
FAILED G1  REP min accuracy L=10 0.9985, L=40 1.0000, L=160 1.0000
HELD   G2  DIAG equal-count deviation 3.54e-15; L=40 0.0188 <= ceiling 0.0217 + 0.02, L=160 0.0152 <= ceiling 0.0175 + 0.02
HELD   G3  COUNT-CEILING L=40 0.0217, L=160 0.0175 < 0.05
HELD   G4  RANDOM-U L=40 0.0072, L=160 0.0097 < 0.05
FAILED G5  SHAM t^2 2.72e-15, c^5 9.22e-15 < 1e-12; (tc)^4 2.8356 > 1e-3; L=40 0.0747, L=160 0.0070 < 0.05
HELD   G6  TABLE min accuracy 1.0000 at every L (no advantage over classical)
VERDICT  4 of 6 registered predictions held
```

Record: `results/verified/E004_x86_64.json`.

## What this shows

- **Commuting state is capped by letter counts, as the prior work says.** DIAG's holonomy is a
  function of the counts, to 3.54e-15. At L = 160 it scored 0.0152, under the count ceiling of 0.0175,
  even with 32 dimensions against REP's 5.
- **Noncommutativity alone carries nothing here.** RANDOM-U scored 0.0072 at L = 40 and 0.0097 at
  L = 160; chance is 0.0083. This is the difference from E002, where any noncommuting pair carried
  the signed area.
- **The relations are what matter.** Operators that satisfy S5's relations track the state exactly at
  16× the shortest length. The sham, which keeps some of the relations, carries a signal that fades
  with length (G5 above).
- **No advantage over classical computation.** The 120-state table is exact everywhere (G6). The
  finding concerns commuting recurrent state, the class used by diagonal state-space models, and
  not computers in general.

## Next

- **E004b** (to be registered before running): an exact-decode readout, or the class-coverage
  condition built in, so that G1 tests the arm and not the readout; and the sham's reduced-word
  overlap as a registered variable.
- **E004-U1** (the step toward real models): learn the operators from data and see whether training
  finds the relations.

## Replication on the S25 (2026-09-27, pasted by the operator)

```
VERITAS-HOLO E004 | seeds 1-3 | aarch64 | Python 3.14.6 | NumPy 2.4.4
arm                 L=10      L=40     L=160   (mean test accuracy over seeds)
REP               0.9995    1.0000    1.0000
DIAG              0.0610    0.0188    0.0152
COUNT-CEILING     0.1930    0.0217    0.0175
RANDOM-U          0.4363    0.0072    0.0097
SHAM              0.9122    0.0747    0.0070
TABLE             1.0000    1.0000    1.0000
SHAM relations: max ||t^2-I|| 2.76e-15, max ||c^5-I|| 9.97e-15, min ||(tc)^4-I|| 2.8356
VERDICT  4 of 6 registered predictions held
```

The same six verdicts, with every registered number equal to x86_64's. One value differs:
DIAG at L = 10 is 0.0610 on the S25 and 0.0618 on x86_64. L = 10 is not a registered length for
DIAG. The likely cause is a near-tie between class centroids, broken differently by rounding on the
two machines; this has not been checked.
