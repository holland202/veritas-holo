# E002 — results

Registration: [PREREG.md](PREREG.md), committed before the runner existed.

## Container x86_64, Python 3.11.15, NumPy 2.4.4, seeds 1-20 (20.2 s)

```
VERITAS-HOLO E002 | seeds 1-20 | x86_64 | Python 3.11.15 | NumPy 2.4.4
paths: balanced words of length 40, 200 train + 200 held-out per seed; signed-area sd 5.70
sham check: max |eig(Y_sham) - eig(Y)| 9.99e-16
arm                mean R2     min R2
SU2                 0.9999     0.9999
SU32-RANDOM         1.0000     1.0000
SPECTRUM-SHAM       1.0000     1.0000
ABELIAN            -0.0036    -0.0159
SU2-LARGE          -0.0018    -0.0701
SHOELACE            1.0000     1.0000
HELD   E1  SU2 mean R2 0.9999 > 0.99
HELD   E2  SU32-RANDOM mean R2 1.0000 > 0.99
HELD   E3  SPECTRUM-SHAM mean R2 1.0000 > 0.99
HELD   E4  ABELIAN mean R2 -0.0036 < 0.05, max ||H-I|| 7.19e-15 < 1e-12
HELD   E5  SU2-LARGE mean R2 -0.0018 < 0.5
HELD   E6  SHOELACE min R2 1.0000 == 1 at ~2 mult/step (SU2 >= 8 complex mult/step, SU32 ~ 32768)
VERDICT  6 of 6 registered predictions held
```

Full record: `results/verified/E002_x86_64.json`.

## What this shows

- **Small-loop holonomy carries a path's signed area, for any operators that do not commute.** The
  designed SU(2) rotations (0.9999), random SU(32) operators (1.0000) and P8's spectrum-matched sham
  (1.0000) all read it out on held-out paths. The operators that commute read out nothing
  (−0.0036); their holonomy is the identity to 7.19e-15.
- **P8's premise is refuted, as E3 predicted.** "Same spectra, randomised eigenvectors" does not
  destroy the structure; the sham scored as high as anything. The structure that carries the signal
  at small step size is noncommutativity itself. A sham for this kind of claim has to commute.
- **It is a small-loop property.** At step 1.0 the same SU(2) arm reads out nothing (−0.0018): higher
  order terms swamp the area.
- **No geometric advantage on this task, as registered.** The shoelace formula gets the area exactly
  on every seed with about 2 multiplications per step; the SU(32) arms spend about 32,768. The
  holonomy computes, expensively, something a two-line recurrence computes exactly.

## What it means for the project

This is the honest stopping point E002 was built to reach. The geometric substrate carries path-order
information, and that information here is fully available to a cheap classical computation. So
veritas-holo still has **no candidate for a reasoning advantage**. The open question is E7:
a task where a path's holonomy carries information that no equal-cost classical recurrence
computes. Signed area is not it. Until one is found and registered, C004 stays PROPOSED with nothing
behind it.
