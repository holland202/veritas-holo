# E009: results

Registered in `PREREG.md` (commit 1527596) after a 20-seed pilot. **2 of 4 held on x86_64. B1 and B2
FAILED; both are kept.**

## What failed, first

- **The blind residual did not separate success from failure the way the pilot suggested.**
  - Accepted (residual < 0.32): 18 runs, of which 16 succeeded (0.8889, registered ≥ 0.95).
  - Rejected: 22 runs, of which 6 succeeded (0.2727, registered ≤ 0.10).
  - The pilot's clean gap (0.275-0.366) came from 10 seeds. On 40 seeds, successes and failures
    overlap from 0.26 to 0.44.
- **Exploratory, after the run.** The residual still carries signal: the area under the ROC curve over
  the 40 seeds is 0.904, and every run with a residual of exactly 0 (5 runs) succeeded. As a gate, it
  is clearly weaker than E006's relator score, which separated 17 of 17 each way but needs the
  group's relations. The honest reading: knowing the relations buys a much better check.

## What held

- **B3:** 18 accepted and 22 rejected, so the test was not trivial.
- **B4, half precision:** all 22 successful runs scored 1.0000 at L = 10000 with the operators and
  the running state rounded to float16 after every step. The learned operators do not need double
  precision over long sequences. That matters for running them on the phone's half-precision GPU or
  NPU. This was simulated in NumPy; it has not been measured on the hardware.

## Output (pasted verbatim)

```
VERITAS-HOLO E009 | seeds 501-540 | x86_64 | Python 3.11.15
seed   residual decision  f64 L160  f16 L1e4
 501      0.465   REJECT    0.0125    0.0175
 502      0.259   ACCEPT    1.0000    1.0000
 503   2.28e-13   ACCEPT    1.0000    1.0000
 504       0.45   REJECT    0.1025    0.0800
 505      0.261   ACCEPT    0.3225    0.3100
 506       0.26   ACCEPT    1.0000    1.0000
 507      0.521   REJECT    0.0650    0.0825
 508      0.236   ACCEPT    1.0000    1.0000
 509      0.375   REJECT    0.1200    0.1250
 510      0.258   ACCEPT    1.0000    1.0000
 511      0.396   REJECT    0.2925    0.0100
 512   1.99e-13   ACCEPT    1.0000    1.0000
 513      0.506   REJECT    0.0150    0.0100
 514      0.259   ACCEPT    1.0000    1.0000
 515       0.53   REJECT    0.0825    0.0800
 516   2.02e-13   ACCEPT    1.0000    1.0000
 517   2.03e-13   ACCEPT    1.0000    1.0000
 518       0.37   REJECT    0.0075    0.0125
 519      0.261   ACCEPT    1.0000    1.0000
 520      0.439   REJECT    1.0000    1.0000
 521      0.327   REJECT    1.0000    1.0000
 522      0.262   ACCEPT    0.3025    0.3100
 523   2.35e-13   ACCEPT    1.0000    1.0000
 524      0.322   REJECT    1.0000    1.0000
 525      0.454   REJECT    0.0150    0.0150
 526      0.277   ACCEPT    1.0000    1.0000
 527      0.276   ACCEPT    1.0000    1.0000
 528      0.318   ACCEPT    1.0000    1.0000
 529      0.421   REJECT    1.0000    1.0000
 530      0.455   REJECT    0.0250    0.0150
 531      0.533   REJECT    0.0125    0.0225
 532      0.398   REJECT    0.0125    0.0100
 533      0.363   REJECT    0.0100    0.0175
 534      0.399   REJECT    0.3500    0.0175
 535      0.535   REJECT    0.0225    0.0100
 536      0.455   REJECT    0.0150    0.0100
 537      0.278   ACCEPT    1.0000    1.0000
 538      0.263   ACCEPT    1.0000    1.0000
 539      0.321   REJECT    1.0000    1.0000
 540      0.376   REJECT    1.0000    1.0000
FAILED B1  accepted 18, succeeded 16 (0.8889 >= 0.95)
FAILED B2  rejected 22, succeeded 6 (0.2727 <= 0.10)
HELD   B3  18 accepted, 22 rejected (each >= 5)
HELD   B4  float16 at L=10000 on the 22 successful runs: min 1.0000 (>= 0.99)
VERDICT  2 of 4 registered predictions held
```
