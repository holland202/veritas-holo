# E005: can gradient descent learn a group's state from short examples and track it 20× longer? Registration

Status: **Registered** (2026-09-27), after an exploratory pilot on seeds 11-16
(`results/exploratory/E005_pilot.md`) and before any run on the registered seeds 1-5. The
thresholds below were set from the pilot. That is the point of piloting: E004 lost two predictions
to thresholds nobody had checked.

## Question

E004 showed that operators satisfying S5's relations track its state at any length, and commuting
operators cannot. Here nobody supplies the relations. Given only words of length ≤ 8 labelled
with the permutation they compose to, does gradient descent on unitary operators find operators
that track the state on words of length 160? And does the same training restricted to commuting
(diagonal) operators fail, as the theory says it must?

This bears on current models, where whether training finds state-tracking solutions is an open,
practical question. E005 is one small, controlled instance of it.

## Setup (fixed)

- **Training data:** all 510 words of length 1-8 over {t, c}, each labelled by its S5 element (E004's
  t, c). No relation of the group is given.
- **Model:** two 8 × 8 unitary operators, initialised at random (Haar) from the seed.
- **Loss:** equal-label pairs pull their holonomies together (squared Frobenius distance).
  Different-label pairs are pushed at least 4.0 apart. 64 + 64 sampled pairs per step, 3000 steps,
  Riemannian momentum steps on U(8) (lr 0.05, decayed linearly; momentum 0.9). Implementation:
  `veritas_holo/learn.py`.
- **Commuting arm:** identical training with the operators restricted to diagonal unitaries.
- **Test:** 6000 + 2000 fresh random words at L = 40 and at L = 160 (5× and 20× the longest training
  word), with the nearest-centroid readout of E004 fitted on the 6000. The operators never see a
  word longer than 8; only the readout sees long words.
- **Seeds 1-5.**

## Registered predictions

- **L1** On at least 3 of the 5 seeds, the learned operators reach test accuracy ≥ 0.99 at L = 160.
- **L2** Every seed that meets L1 also reaches ≥ 0.99 at L = 40.
- **L3 (null, commuting)** The learned diagonal operators score ≤ the letter-count ceiling + 0.02 at
  L = 40 and at L = 160, on every seed.
- **L4 (null, untrained)** The same seed's operators before training score < 0.05 at L = 40 and
  L = 160, on every seed. Training, not the architecture, does the work.
- **L5 (instrument)** Every trained operator is unitary to < 1e-10.
- **L6 (mechanism)** Five words that equal the identity in S5 are fixed in advance: t², c⁵, (tc)⁴,
  (t c⁻¹ t c)³ and (t c⁻² t c²)². The run checks that each is the identity under E004's exact
  representation. On every seed that meets L1, each of these relator matrices has at least 4 of its 8
  eigenvalues within 1e-2 of 1. Training has built the relations into part of the space.

## Limits (stated before running)

- A 120-state lookup table does this exactly (E004 G6). The claim concerns what training finds, not an
  advantage over classical computation.
- The readout is fitted on labelled long words. Only the operators are trained on short words alone.
- One group (S5), one width (8), one training length (≤ 8). The pilot failed on 1 of 6 seeds at
  width 8, and at width 5 it failed on every seed.

## Unrun

- **E005-U1** Pick among a few restarts using the training loss alone, with no test data, and see
  whether the pick is reliable.
- **E005-U2** A group or task nobody labels by hand: automata learned from traces of a real system's
  actions (for example sovereign-veritas gate decisions).
