# Claim ledger

One file per claim. Status moves only on evidence: PROPOSED -> IMPLEMENTED -> TESTED -> REPLICATED,
or REFUTED (kept, never deleted), or UNKNOWN. A claim cites the registered predictions that test it
and the result file that shows the verdict.

| id | status | claim |
|---|---|---|
| C001 | TESTED | the reference implementation obeys the SU(n) algebra it is built on (E001) |
| C002 | REFUTED | holonomy carries task information a spectrum-matched sham cannot: the sham carried it too (E002, E3) |
| C003 | REFUTED | E001 replays byte for byte on the S25 and x86_64 (P9): digests differ; verdicts and values agree |
| C005 | REPLICATED | E001 replays on the S25 and x86_64 to 10 decimal places (P10, seeds 1-5) |
| C006 | REPLICATED | small-loop holonomy carries signed area for any noncommuting pair; commuting pairs carry none (E002; x86_64 and S25) |
| C007 | REPLICATED | a per-resource holonomy fingerprints concurrent histories and merges from fingerprints alone (E003) |
| C008 | TESTED | relation-respecting holonomy tracks S5 exactly at L=40, 160; commuting holonomy is capped by letter counts; relation-free noncommuting holonomy is at chance (E004) |
| C009 | REFUTED | a spectrum-matched sham carries no S5 signal at L=40: it carried 0.0747 (E004, G5) |
| C010 | TESTED | gradient descent learns S5 state tracking from words <= 8 and extrapolates to 160 (3 of 5 seeds), building in the relations; commuting training cannot (E005) |
| C011 | TESTED | a relator score read from the trained operators before any test separates working from failed training runs: 17/17 accepted succeeded, 17/17 low scores failed (E006) |
| C012 | TESTED | operators trained without two transitions handle them exactly (12/12 successful runs at 1.0); a transition-memorising null stays at chance on them (E007) |
| C013 | TESTED | rounding drift in a continuum representation is negligible to 1e6 steps; operator error is what breaks decoding, and snapping to a finite codebook every step removes it (E008) |
| C014 | REFUTED | a blind training residual gates training success (B1, B2 failed: 16/18 and 6/22; AUC 0.904) (E009) |
| C015 | TESTED | successful learned operators stay exact at L=10000 in float16 (22/22) (E009) |
| C016 | TESTED | held-out composition holds on A5 with 3-cycle generators: 40/40 at 1.0; the memorising null at chance (E010) |
| C017 | TESTED | a 242-product margin decides snapped decoding for every length: 300/300 agreement with 10⁴-step runs; a data-built codebook is certified to δ ≈ 0.1 (E011) |
| C004 | PROPOSED | the geometric layer improves a local LLM's reasoning beyond a sham |
