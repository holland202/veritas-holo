# E001 — operator algebra on SU(32): registration

Status: **Registered** (2026-09-27), before any code below was written. Results are appended in
`RESULTS.md` and never edited into this file.

## What E001 is for, and what it is not

E001 checks that the reference implementation does what the mathematics says it must: closure,
inverses, commutators, holonomy, invariant preservation and deterministic replay, on explicitly
constructed SU(n) operators acting on unit state vectors. Every one of these is a known property of
unitary matrices. **E001 is an implementation test, not a discovery and not a reasoning result.**
Passing it shows the instrument works; it says nothing yet about whether geometric structure helps
any computation. That question is E002's, and it is registered below as unrun (P8).

Each prediction that can pass trivially has a **null control** beside it that must come out the
other way, so a checker that always says PASS would be caught.

## Setup (fixed before running)

- State space: unit vectors in C^32 (n = 32). Distance between states: phase-aligned Euclidean,
  d(x, y) = || x − y · (⟨y,x⟩ / |⟨y,x⟩|) ||₂, which ignores the global phase (states are rays) and,
  unlike arccos(|⟨x,y⟩|), stays accurate near zero.
- Operators: T = exp(iH), H a random traceless Hermitian 32 × 32 matrix (complex Gaussian entries,
  Hermitised, trace removed, scaled to ||H||_F = 1). exp is computed from the eigendecomposition of
  H. So T ∈ SU(32) up to rounding.
- 8 such operators A1..A8; a trajectory of 12 steps applies A1..A8 then A1..A4. numpy
  `default_rng(1)` for everything; the seed is the only input.

## Registered predictions

- **P1 closure.** Every prefix product U_k of the trajectory (k = 1..12) satisfies
  ||U_k† U_k − I||_F < 1e-10 and |det U_k − 1| < 1e-10.
- **P2 inverse.** For each A_i and the initial state x, d(A_i† A_i x, x) < 1e-12.
- **P3 noncommutativity.** All 28 pairs of A1..A8 have ||[A_i, A_j]||_F > 1e-3.
  **N3 null:** 28 pairs of diagonal SU(32) elements (exp of random traceless diagonal H) have
  ||[A, B]||_F < 1e-12.
- **P4 holonomy scaling.** X, Y random traceless Hermitian with ||X||_F = ||Y||_F = 1;
  H(ε) = e^{iεX} e^{iεY} e^{−iεX} e^{−iεY}, h(ε) = ||H(ε) − I||_F, for ε in
  {0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001}. By the Baker–Campbell–Hausdorff formula
  H(ε) = exp(−ε² [X, Y] + O(ε³)), so: the least-squares slope of log h against log ε lies in
  [1.95, 2.05], and h(0.001) / 0.001² is within 1 % of ||[X, Y]||_F.
  **N4 null:** X, Y diagonal: h(ε) < 1e-12 for every ε.
  Also reported, not predicted in size: the state holonomy ε_H = d(A1 A2 A1† A2† x, x).
- **P5 invariant preservation.** Along the 12-step trajectory, | ||x_k|| − 1 | < 1e-12 at every
  step, and the invariant checker reports PASS.
  **N5 sham:** the same trajectory with A3 replaced by a non-unitary matrix of the same Frobenius
  norm (√32): the checker reports FAIL, with a norm error above 1e-3.
- **P6 isometry.** x′ = normalise(x + 1e-6 δ), δ a random unit vector: after the trajectory,
  |d(U x, U x′) − d(x, x′)| < 1e-12. This is what "perturbation resistance" means for a unitary map;
  it is a property of the maps, stated so it cannot be sold as robustness.
- **P7 replay.** Two runs with seed 1 give the same sha256 over the bytes of all 13 states; a run
  with seed 2 gives a different one.

Unrun, left open on purpose:

- **P8 (E002's question).** Holonomy along operator paths chosen to solve a task carries
  information a sham cannot: with a sham whose operators have the same eigenvalue spectra but
  randomised eigenvectors (same cost, same dimension, structure destroyed), a registered task score
  differs by more than its seed-to-seed spread. Not run; E002 must define the task first.
- **P9 cross-platform replay.** The seed-1 digest is the same on the S25 (aarch64, Termux) as on
  x86_64. It may well fail (different BLAS and LAPACK builds); if so, the replay claim is per
  platform.

Stated limits: one seed for the headline run; tolerances chosen from double-precision rounding at
n = 32, not tuned after running.
