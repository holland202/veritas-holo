# E006 (E005-U1): results

Registered in `PREREG.md` (commit 3b0effb) after the 20-seed pilot. The runner was committed before
the run (33b3550) and made resumable (the commit after it) when this machine restarted during the
first attempt; that attempt had printed nothing. The run then continued across two more restarts
from its per-seed file (`results/verified/E006_per_seed.jsonl`). Each seed's ACCEPT/REJECT decision is
stored with the time it was made, before that seed's test words were built, and the runner asserts
this for all 40 seeds. **4 of 4 held on x86_64 (Intel Xeon).**

## Output (pasted verbatim)

```
VERITAS-HOLO E006 | seeds 41-80 | x86_64 | Python 3.11.15 | NumPy 2.4.4
acceptance rule: relator score >= 5 (of 8); decisions sealed before each test (checked: all 40 decided before tested)
seed score decision   acc 40  acc 160
  41     5   ACCEPT   1.0000   1.0000
  42     6   ACCEPT   1.0000   1.0000
  43     8   ACCEPT   1.0000   1.0000
  44     7   ACCEPT   1.0000   1.0000
  45     1   REJECT   0.3010   0.0145
  46     6   ACCEPT   1.0000   1.0000
  47     2   REJECT   0.3840   0.0155
  48     7   ACCEPT   1.0000   1.0000
  49     1   REJECT   0.3600   0.0875
  50     2   REJECT   0.3725   0.0180
  51     4   REJECT   1.0000   1.0000
  52     7   ACCEPT   1.0000   1.0000
  53     4   REJECT   1.0000   1.0000
  54     7   ACCEPT   1.0000   1.0000
  55     0   REJECT   0.4155   0.0155
  56     6   ACCEPT   1.0000   1.0000
  57     1   REJECT   0.8870   0.0625
  58     7   ACCEPT   1.0000   1.0000
  59     6   ACCEPT   1.0000   1.0000
  60     1   REJECT   0.7430   0.0175
  61     2   REJECT   0.7410   0.0245
  62     4   REJECT   1.0000   1.0000
  63     5   ACCEPT   1.0000   1.0000
  64     6   ACCEPT   1.0000   1.0000
  65     1   REJECT   0.4125   0.0045
  66     2   REJECT   0.5550   0.0190
  67     4   REJECT   0.1935   0.0145
  68     6   ACCEPT   1.0000   1.0000
  69     1   REJECT   0.6515   0.0090
  70     7   ACCEPT   1.0000   1.0000
  71     2   REJECT   0.7120   0.0110
  72     2   REJECT   0.2620   0.0155
  73     1   REJECT   0.4965   0.0970
  74     1   REJECT   0.7405   0.0210
  75     7   ACCEPT   1.0000   1.0000
  76     7   ACCEPT   1.0000   1.0000
  77     1   REJECT   0.5095   0.0170
  78     0   REJECT   0.3565   0.0100
  79     4   REJECT   1.0000   1.0000
  80     4   REJECT   0.0650   0.0170
accepted 17: 17 succeeded; score <= 3: 17, 0 succeeded; score 4 (no prediction): 6, 4 succeeded
base success rate 0.5250; policy jobs succeeded 9/10, blind first-seed 2/10; mean trainings per job 2.70
HELD   D1  precision of ACCEPT 1.0000 >= 0.95
HELD   D2  success among score <= 3: 0.0000 <= 0.10 (17 runs)
HELD   D3  base success rate 0.5250 in [0.5, 0.9]
HELD   D4  policy delivered a successful run in 9 of 10 jobs (>= 9)
VERDICT  4 of 4 registered predictions held (D5 reported, not scored)
```

## What this shows

- **The check sorted training runs almost perfectly, before any test was opened.** All 17 ACCEPTED runs
  (score ≥ 5) succeeded at length 160. All 17 runs with a score of 3 or less failed. The 6 runs with
  a score of exactly 4 went both ways (4 succeeded, 2 failed). As in the pilot, 4 is the ambiguous
  band.
- **It turns an unreliable procedure into a reliable one.** Training alone succeeded 52.5% of the
  time here (lower than the pilot's 70%, and only just inside D3's registered range). Taking the first
  ACCEPTED run in each group of 4 delivered a working model in 9 of 10 groups, at a mean of 2.70
  trainings. Taking each group's first seed without looking delivered 2 of 10.
- **What it rests on:** the check knows S5's relations in advance. It is a mechanistic diagnostic,
  not a model judging itself. The blind version (E006-U1) is open.

The four predictions are not independent confirmations. D1, D2 and D4 all measure the same
separation. The finding is one thing: the score separates success from failure prospectively.

![E006](../../figures/E006_restart_diagnostic.png)
