# E009 pilot (exploratory; seeds 401-420, disjoint from every registered seed)

This follows from the review of the Constitutional Geometry document and from E008. There were three
questions, and two of the answers changed the plan.

1. **Do E005's learned operators drift at long horizons, and does snapping help?** (seeds 401-410)
   Every run that succeeded at L = 160 still scored 1.000 at L = 1000 and at L = 5000 **without**
   snapping. Snapping to the readout's own class centroids every 8 steps changed nothing. The learned
   operators do not drift on this scale, so **snapping is not needed for them. It is dropped from the
   registration.** (E008's snapping result stands for operators with real error.)
2. **Does a blind closure check work?** (seeds 401-410) The orbit of the learned 8 × 8 operators hit the
   600-element cap on every seed, including the successful ones. Successful runs build the group in
   part of the space and leave the rest unconstrained (E005 L6). A closure check on the whole space
   cannot tell success from failure. **Dropped.**
3. **Two replacements** (seeds 411-420):
   - **Training-consistency residual** (blind: training words and their labels only, no known
     relations, no test words): the mean distance of each training word's holonomy from its label's
     mean. Successful runs: 2.16e-13, 0.274, 0.256, 2.10e-13, 2.12e-13, 0.234, 0.275. Failed runs:
     0.485, 0.513, 0.366. **A threshold anywhere between 0.275 and 0.366 separates them.**
   - **float16 execution:** the state is rounded to float16 after every step (as on a phone NPU or GPU
     that works in half precision). Every successful run still scored 1.000 at L = 1000 and L = 10000.
