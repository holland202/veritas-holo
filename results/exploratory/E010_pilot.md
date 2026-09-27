# E010 pilot (exploratory, seeds 101-110, disjoint from the registered 601-640)

E007's runner moved from S5 to A5: generators the 3-cycles (0 1 2), (1 2 3), (2 3 4); 60 states;
held-out ordered pairs (g0, g1) and (g1, g2); training words of length 1-6 that avoid them (349 words).
Otherwise as E007: 8 × 8 unitary operators, nearest-centroid readout fitted on CLEAN long words.
Output: `E010_pilot.txt`; per-seed rows: `E010_pilot_seeds101-110.jsonl`.

- HELDOUT: 10 of 10 learned CLEAN words (1.0000 at L = 160), and all 10 scored 1.0000 on HELD words.
- PAIR (the memorising null): 10 of 10 learned CLEAN words; HELD accuracy at L = 160 between
  0.0135 and 0.0210, which is chance (1/60 = 0.0167).
- Relator scores of the HELDOUT runs: 5, 6, 8, 6, 4, 4, 5, 3, 5, 5.

Thresholds set from this pilot for the registration: 30 of 40 successes for each arm (the pilot saw
10 of 10; 30 leaves room for a lower true rate without making the prediction empty).
Unlike E007 on S5 (4 of 16 pilot successes), training almost always succeeds here. Why is not
tested; a smaller group with fewer training words is one candidate.
