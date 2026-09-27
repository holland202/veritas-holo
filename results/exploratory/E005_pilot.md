# E005 pilot (exploratory, before registration)

Pilot seeds 11-16, which are disjoint from the registered seeds 1-5. Operators were trained on all
510 words of length 1-8 over {t, c}, labelled by their S5 element. Accuracy is the nearest-centroid
readout of E004, on words of length 40 and 160.

- dim 5: 0 of 2 seeds reached 0.99 at L = 160 (0.011, 0.006).
- dim 8: 5 of 6 seeds reached 1.0000 at L = 160 (seeds 11, 12, 13, 14, 15). Seed 16 fell to 0.0115.
- dim 16: 1 of 1 seed reached 1.0000.
- Learned diagonal (commuting), dim 8, seeds 13 and 16: 0.0185 and 0.015 at L = 160, level with the
  letter-count ceiling (0.0135, 0.018).
- For each of five S5 relator words, the number of eigenvalues of the learned relator matrix within
  1e-2 of 1, out of 8: 7, 5, 8 on successful seeds (minimum over the relators), 1 on the failed seed.
- A "strict" readout with centroids from the training words alone scored 0.74 at L = 160, because
  those words cover only 88 of the 120 classes (the G1 lesson from E004). It is not used in E005.

The raw pilot outputs (p3_*, p4_*) are kept next to this file.
