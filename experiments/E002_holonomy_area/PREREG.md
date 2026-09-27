# E002 — what does holonomy carry, and is it anything a cheap computation cannot get? Registration

Status: **Registered** (2026-09-27), before any E002 code was written. Results go in `RESULTS.md`.

## Why E002 changed shape before it was built

E001's P8 proposed: holonomy along task-solving paths carries information that a sham with **the
same eigenvalue spectra and randomised eigenvectors** cannot. Working the design out showed that
premise is wrong before running anything. By Baker–Campbell–Hausdorff (confirmed in this code by
E001's P4), a small closed loop of steps ±εX, ±εY has holonomy ≈ exp(−ε² · A · [X, Y]), where A is the
signed area the loop encloses. That holds for **any** pair of operators that do not commute. Two
random-eigenvector operators almost never commute, so P8's sham should carry the signal just as well
as the "real" operators. The structure that matters to leading order is noncommutativity itself,
not any particular geometry. A sham that destroys the signal has to commute.

And the signal, signed area, is computable directly from the path by the shoelace formula with a
few additions per step. So E002 asks two honest questions instead of P8's one:

1. Does the holonomy readout carry the path's signed area, for which operators, and at what step
   size? (the instrument question)
2. Does any geometric arm beat the cheap exact computation? (the "advantage" question, which is
   expected to come out **no** for this task)

**Design constraint carried over from token-veritas:** states and paths are defined formally (words
over four step symbols), with no text and no embeddings. token-veritas found that a sentence
embedding measured wording rather than information; a text encoder in front of this substrate would
pass that flaw on. Text comes later, with its own control for it.

## Setup (fixed before running)

- A **path** is a random balanced word of length 40 over {x+, x−, y+, y−}, 10 of each, uniformly
  shuffled. Read as unit steps on the square lattice it is a closed path; its **target** is the
  signed area it encloses (shoelace formula).
- **Holonomy** for an arm with generators (X, Y) and step ε: H = U_{w40} ··· U_{w1}, U(x±) = exp(±iεX),
  U(y±) = exp(±iεY). **Readout** f = Re tr(C† (H − I)) / ||C||_F², C = [X, Y] (the arm's own
  commutator; f = 0 when C = 0). One feature, so there is nothing to overfit.
- **Score:** per seed, 200 training paths and 200 held-out paths; fit target ≈ a·f + b by least
  squares on training, report R² on held-out. 20 seeds (1-20). Headline number: the mean held-out R²,
  with the minimum over seeds.
- **Arms:**
  - **SU2** X = σx/2, Y = σy/2 (rotations about orthogonal axes: the "right" geometry), ε = 0.05.
  - **SU32-RANDOM** X, Y random traceless Hermitian 32 × 32, ||·||_F = 1, ε = 0.05: this is P8's
    sham in effect (no designed structure, noncommuting).
  - **SPECTRUM-SHAM** P8's sham exactly: X unchanged from SU32-RANDOM; Y replaced by V·diag(spec Y)·V†
    with V a random unitary: same eigenvalues, randomised eigenvectors, ε = 0.05.
  - **ABELIAN** X, Y random traceless diagonal 32 × 32, ||·||_F = 1 (commuting), ε = 0.05.
  - **SU2-LARGE** as SU2 with ε = 1.0 (a large step, higher-order terms dominate).
  - **SHOELACE** the exact signed area computed from the word by additions; no operators.

## Registered predictions

- **E1** SU2: mean held-out R² > 0.99.
- **E2** SU32-RANDOM: mean held-out R² > 0.99. No designed geometry needed.
- **E3** SPECTRUM-SHAM: mean held-out R² > 0.99. **This is P8's sham carrying the signal, which
  would refute P8's premise as registered in E001.**
- **E4 (null)** ABELIAN: mean held-out R² < 0.05; the holonomy of every balanced word is the
  identity to rounding (max ||H − I||_F < 1e-12).
- **E5** SU2-LARGE: mean held-out R² < 0.5. The linear area signal is a small-loop property.
- **E6** SHOELACE: R² = 1 exactly on every seed, at a cost of about 2 additions and 2
  multiplications per step, against at least 8 complex multiplications per step for SU2 and about
  32³ for SU32. On this task no geometric arm can beat it; the registered expectation is that
  **geometry gives no advantage here.**

Unrun, the question E002 hands on:

- **E7 (E003's question).** A task where the information in a path's holonomy is **not** computable
  by an equal-cost classical recurrence. Signed area is not such a task. Until one is found and
  registered, veritas-holo has no candidate for a reasoning advantage, and the README says so.

Stated limits: one task family, one word length, one readout. R² thresholds chosen from the
second-order BCH estimate before running, not tuned.
