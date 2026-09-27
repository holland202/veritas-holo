# E012 results: 6 of 6 registered predictions held (x86_64, Python 3.11.15, 2026-09-27)

`python experiments/E012_relator_projection/relproj.py 741 771 OUT.jsonl`, 120 cases. Rows:
`results/verified/E012_per_case.jsonl`.

```
delta 0.1: certified DATA 22/30, SPECTRAL 27/30, ALT 30/30, WRONG 0/30, EXACT 30/30; ALT min margin 1.4809
delta 0.15: certified DATA 5/30, SPECTRAL 12/30, ALT 30/30, WRONG 0/30, EXACT 30/30; ALT min margin 1.2494
delta 0.2: certified DATA 0/30, SPECTRAL 7/30, ALT 30/30, WRONG 0/30, EXACT 30/30; ALT min margin 1.0547
delta 0.3: certified DATA 0/30, SPECTRAL 1/30, ALT 23/30, WRONG 0/30, EXACT 30/30; ALT min margin -2.3220
ALT certified 113: acc 1.0 in 113; uncertified 7: acc < 1 in 7
HELD   R1  HELD   R2  HELD   R3  HELD   R4  HELD   R5  HELD   R6
```

- **R1 held.** ALT was certified 30/30 at δ = 0.1, 0.15 and 0.2. Its smallest margin there was 1.0547
  or more, well above zero.
- **R2 held.** 23/30 at δ = 0.3.
- **R3 held.** The data codebook reached 5/30 at δ = 0.15 and 0/30 at δ = 0.2; ALT reached 30/30 at both.
- **R4 held.** Rounding t and c alone (SPECTRAL) gave 7/30 at δ = 0.2; adding the order of tc gave
  30/30. The product relation does most of the work.
- **R5 held.** With the wrong order for tc (3 instead of 4), 0 of 120 were certified.
- **R6 held.** The certificate agreed with the 10⁴-step runs in 120 of 120 cases.

**What this adds.** E011 left a gap: a codebook built from data stopped working at about δ = 0.1.
Three numbers read from labelled transitions close most of it: the orders of t, c and tc. Projecting
the noisy operators onto matrices with those orders recovers a codebook that is certified wherever
the true representation's codebook is, up to δ = 0.2, and in 23 of 30 cases at δ = 0.3. This is E006's
relator idea, the thing that predicted training success, now used as a repair step instead of a
diagnostic.

**Limits.** S5, one presentation, three hand-chosen relators, one noise model, dimension 5. The
orders come from labels. R7 (finding the orders from the operators alone) and repairing failed E005
training runs are open.
