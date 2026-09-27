# E011 pilot (exploratory, seeds 701-710, disjoint from the registered 711-740)

**Starting question (E008-U1):** can the snapping codebook be built from labelled data instead of from
the exact group representation, for operators with real error?

**First attempt failed, and why matters.** The per-label mean holonomy of 4000 random labelled words of
length 1-12 covered only 117-119 of the 120 states. Snapped decoding then scored 0.00-0.13 at L = 1000
even at δ = 0.01, where snapping to the exact codebook scored 1.0. A walk that reaches a state missing
from the codebook is snapped to a wrong one and never recovers. With words of length 1-20 every state
was covered, and the same method scored 1.0 at δ = 0.1 on 3 of 3 seeds (0.0 at δ = 0.2).

Two other constructions did worse at δ = 0.1: the mean over only the shortest words per state (1.0, 0.0,
0.5 on the 3 seeds) and a fixed-point refinement c_{gs} ← mean of O_g c_s (0.56, 0.09, 0.66).

**What came out of it: a finite certificate.** Snapping is deterministic, so correctness reduces to 242
checks. For each state s and letter g (and for the start, O_g I), O_g c_s must be nearer to c_{gs} than to
any other entry. Call the smallest gap the margin.
- If the margin is positive, induction gives exact decoding for every word of every length.
- If it is negative at some (s, g), every word that visits s and then reads g is decoded wrong from there on.
`cert.py` computes the margin and, separately, runs 32 random words of length 10⁴.

Pilot, 10 seeds × 5 noise levels × 2 codebooks (data mean, length 1-20, 4000 words; exact):

| δ | data: certified | exact: certified |
|---|---|---|
| 0.05 | 10/10 | 10/10 |
| 0.1 | 8/10 | 10/10 |
| 0.15 | 2/10 | 10/10 |
| 0.2 | 0/10 | 10/10 |
| 0.3 | 0/10 | 10/10 |

The margin agreed with the long run in all 100 cases. 70 were certified, and all 70 decoded 32 of 32
words at L = 10⁴. 30 were not, and all 30 decoded fewer (0.0 to 0.5). Rows are in
`E011_pilot_seeds701-710.jsonl`.
