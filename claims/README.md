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
| C004 | PROPOSED | the geometric layer improves a local LLM's reasoning beyond a sham |
