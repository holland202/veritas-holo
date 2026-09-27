# E003: results

Registered in `PREREG.md` (commit ee623a5). The code was committed before the run.
**8 of 8 held on x86_64 and on the S25.**

## Output (pasted verbatim, x86_64: the run that wrote the JSON)

```
VERITAS-HOLO E003 | seeds 1-5 | x86_64 | Python 3.11.15 | NumPy 2.4.4
alphabet: 12 actions over 5 resources: 0:24 1:0 2:0 3:4 4:23 5:23 6:13 7:01 8:03 9:04 10:2 11:1
logs: 1000 of length 200; legal shuffle = 50 independent swaps; SL(2, F_p) check 5 of 5 seeds
BASE (per-resource SHA-256) equality agrees with ground truth on 3000 of 3000 pairs
merge time HF: 3.5 us (|v|=100), 3.7 us (|v|=100000)
extend time BASE: 15.9 us (|v|=100), 14042.4 us (|v|=100000)
build time per event: HF 1.54 us, BASE 0.26 us
HELD   T1  legal shuffles same history 1000/1000, HF unchanged 1000/1000
HELD   T2  illegal swaps different history 1000/1000, HF changed 1000/1000
HELD   T3  HF equality = ground truth on 3000/3000 pairs
HELD   T4  merge(F(u),F(v)) = F(uv) 1000/1000; 16-segment tree 1000/1000
HELD   T5  N1 commuting accepts illegal swaps 1000/1000 = 1.0000 >= 0.99
HELD   T6  N2 one-block rejects legal shuffles 1000/1000 = 1.0000 >= 0.99
HELD   T7  merge-time ratio 100000/100: HF 1.06 < 3, BASE 883.6 > 100
HELD   T8  per-event build: HF 5.9x BASE (HF slower, as registered)
VERDICT  8 of 8 registered predictions held
```

Timing lines vary run to run (an immediate rerun gave HF 3.6 / 4.3 us, BASE 19.6 / 16207.7 us, T7 ratios 1.20 and 828.3, T8 5.6x; still 8 of 8). Everything else is exact integer arithmetic and replays identically.
That run's record is in `results/verified/E003_x86_64.json`.

## What this shows

- **A holonomy can serve as a fingerprint of a concurrent history.** Legal reorderings leave it
  unchanged (1000 of 1000), and a single swap of dependent actions changes it (1000 of 1000). It
  agrees with the normal-form ground truth on all 3000 pairs.
- **E002's null became the design lever.** Where resources are disjoint the matrices commute, and
  the fingerprint forgives reordering. Where resources are shared they do not commute, and it
  notices. Make everything commute (N1) and it accepts every illegal swap. Make nothing commute
  (N2) and it rejects every legal shuffle. The two nulls fail in opposite directions, as registered.
- **The advantage is composition, and only composition.** Merging two fingerprints took 3.5 us for a
  100-event segment and 3.7 us for a 100,000-event segment. The SHA-256 baseline has to re-read the
  raw segment: 15.9 us vs 14042.4 us. On equality alone the baseline is just as correct (3000 of 3000)
  and 5.9x faster per event.

## A property found in analysis, not registered

A Merkle tree can also concatenate two digests in constant time. Its root, though, depends on
where the log was cut into segments and on how independent actions interleaved. This fingerprint
depends on neither: every cut and every legal interleaving gives the same value (T1, T4). That
comparison was not a registered arm, so it is recorded here as analysis only.

## Limits

- Not secure against an adversary. SL(2) Cayley hashes have published collision attacks (E003-U1
  is open).
- One alphabet (12 actions, 5 resources), one log length (200), one prime (2^61 − 1).

## Replication on the S25 (2026-09-27, pasted by the operator)

```
VERITAS-HOLO E003 | seeds 1-5 | aarch64 | Python 3.14.6 | NumPy 2.4.4
alphabet: 12 actions over 5 resources: 0:24 1:0 2:0 3:4 4:23 5:23 6:13 7:01 8:03 9:04 10:2 11:1
logs: 1000 of length 200; legal shuffle = 50 independent swaps; SL(2, F_p) check 5 of 5 seeds
BASE (per-resource SHA-256) equality agrees with ground truth on 3000 of 3000 pairs
merge time HF: 6.3 us (|v|=100), 6.7 us (|v|=100000)
extend time BASE: 22.0 us (|v|=100), 18118.4 us (|v|=100000)
build time per event: HF 1.87 us, BASE 0.31 us
HELD   T1  legal shuffles same history 1000/1000, HF unchanged 1000/1000
HELD   T2  illegal swaps different history 1000/1000, HF changed 1000/1000
HELD   T3  HF equality = ground truth on 3000/3000 pairs
HELD   T4  merge(F(u),F(v)) = F(uv) 1000/1000; 16-segment tree 1000/1000
HELD   T5  N1 commuting accepts illegal swaps 1000/1000 = 1.0000 >= 0.99
HELD   T6  N2 one-block rejects legal shuffles 1000/1000 = 1.0000 >= 0.99
HELD   T7  merge-time ratio 100000/100: HF 1.06 < 3, BASE 824.4 > 100
HELD   T8  per-event build: HF 6.0x BASE (HF slower, as registered)
VERDICT  8 of 8 registered predictions held
```

The alphabet and every exact count match x86_64; only the timings differ, as timings do. The
merge-time ratio is flat on both machines (1.06 and 1.06). C007 moves from TESTED to REPLICATED.
