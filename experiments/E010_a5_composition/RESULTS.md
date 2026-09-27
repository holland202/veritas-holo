# E010 results: 3 of 3 registered predictions held (x86_64, Python 3.11.15, NumPy 2.4.4, 2026-09-27)

`python experiments/E010_a5_composition/run.py`, seeds 601-640, both arms. Full output:
`results/verified/E010_x86_64.json`; per-seed rows: `results/verified/E010_per_seed.jsonl`.

```
HELD   H1  40 HELDOUT runs learned CLEAN words (need >= 30); HELD accuracy at L=160 on them: 1.0000 (all 40)
HELD   H2  PAIR HELD accuracy at L=160, max over 40 seeds: 0.0240 (< 0.05)
HELD   H3  40 PAIR runs learned CLEAN words (need >= 30), so the null is not just a weak learner
VERDICT  3 of 3 registered predictions held
```

(The H1 line is shortened: the runner prints 1.0000 forty times.)

- **H1 held.** All 40 per-letter runs learned the words they saw, and all 40 scored 1.0000 on words full
  of the two transitions they never saw.
- **H2 held.** The memorising null stayed at chance on those words (1/60 = 0.0167). Its maximum over 40
  seeds at L = 160 was 0.0240.
- **H3 held.** The null learned the seen words 40 of 40 times, so the contrast is between two models
  that both fit their training data.

**What this adds to E007.** Held-out composition was not a property of one group or presentation: it held
on A5 with 3-cycle generators as on S5 with transpositions. Training succeeded 40 of 40 times here,
against 12 of 40 for E007's S5 setup; why is not tested.

**Limits.** Composition is built into the per-letter architecture (as in E007). Two groups, one width,
one choice of held-out pairs each.
