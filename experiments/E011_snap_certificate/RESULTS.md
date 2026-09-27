# E011 results: 5 of 5 registered predictions held (x86_64, Python 3.11.15, 2026-09-27)

`python experiments/E011_snap_certificate/cert.py 711 741 10000 OUT.jsonl`, 300 runs. Every DATA
codebook covered all 120 states. Rows: `results/verified/E011_per_run.jsonl`.

```
certified 210: accuracy 1.0 in 210
uncertified 90: accuracy < 1.0 in 90; accuracy range 0.0-0.5625
delta 0.05: DATA certified 30/30, min margin 0.7071, max 1.4404; EXACT certified 30/30, min margin 1.6495, max 1.8069
delta 0.1: DATA certified 26/30, min margin -0.4270, max 0.8578; EXACT certified 30/30, min margin 1.3335, max 1.6216
delta 0.15: DATA certified 4/30, min margin -1.1887, max 0.3614; EXACT certified 30/30, min margin 1.0523, max 1.4447
delta 0.2: DATA certified 0/30, min margin -1.5506, max -0.0053; EXACT certified 30/30, min margin 0.7999, max 1.2765
delta 0.3: DATA certified 0/30, min margin -1.6373, max -0.5050; EXACT certified 30/30, min margin 0.3627, max 0.9669
HELD   P1
HELD   P2
HELD   P3
HELD   P4
HELD   P5
```

- **P1 held (soundness).** All 210 certified runs decoded 32 of 32 words at L = 10⁴. This is a
  theorem, so P1 confirms the implementation, not the mathematics.
- **P2 held (the certificate is not loose).** All 90 uncertified runs decoded fewer than 32. The
  closest case: seed 720, DATA, δ = 0.2, margin −0.0053. It decoded 0.15625. A margin barely below
  zero was already enough to fail.
- **P3 held.** 90 of 300 uncertified: the certificate says no often.
- **P4 held.** DATA was certified 30/30 at δ = 0.05 and 0/30 at δ = 0.2.
- **P5 held.** EXACT was certified 150/150. Its smallest margin shrinks with δ: 0.3627 at δ = 0.3.

**What this adds.** Before E011, knowing whether snapping works at length L meant running to length L.
Now 242 matrix products decide it for every length, and in 300 of 300 runs the long run agreed with
the decision. The data-built codebook, which needs no knowledge of the representation, works to
about δ = 0.1: 26/30 certified there, 4/30 at 0.15.

**Limits.** The certificate needs the transition labels (the multiplication table). One group, one
dimension, one noise model. The data codebook's range (δ ≈ 0.1) is for 4000 words of length 1-20; a
larger or better-chosen sample was not tried. P6 (a codebook chosen to maximise the margin) is still
open.
