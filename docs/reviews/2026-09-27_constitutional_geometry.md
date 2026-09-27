# Review: "Constitutional Geometry: A Triad-Closed Operator Framework for Invariant Preservation in Multi-Body Systems"

**Document reviewed:** J. Harlow (HadronQ), dated 2026-09-27, 67 pages, marked "Patents under file and
Pending, All Rights Reserved". The operator shared it for this review. This file summarises and
assesses it; it does not reproduce it. Section and equation numbers refer to the PDF.

**Reviewer:** Claude (Anthropic), for veritas-holo. Every claim below points to a place in the
document, to a standard mathematical fact, or to a run in this repository.

## 1. What the document claims

Four invariants are required of multi-body evolution (§5.1):

- holonomy closure (every admissible loop returns every state to itself, eq. 5.1.1);
- curvature admissibility (curvature stays in a finite set of "sectors");
- energy-partition stability (total energy preserved; redistribution only through "admissible
  channels");
- phase-space coherence.

The central **Necessity Theorem** (Thm 15.1, restated as Meta-Theorem 16.1 and Unification Theorem 32.2)
says that any geometry that preserves these invariants is "constitutionally equivalent" to one with:

- a **finite** state space (H1);
- sector-restricted curvature and holonomy (H2);
- a closed operator algebra (H3);

plus three closure conditions: structural, analytic and arithmetic (H4-H6). The key step from a
continuum to a finite state space is the **Drift Lemma** (Lemma 17.3, F.1, G.1): continuum evolution
drifts in holonomy and curvature unless curvature is restricted to a discrete set.

## 2. Verdict

**The necessity result is not established.**

- Most "lemmas" are restatements of definitions.
- Several definitions are inconsistent with each other.
- The one substantive step, the Drift Lemma, is given only as a proof sketch.
- As stated, the Drift Lemma is false for exact continuum flows. It is contradicted in practice by
  geometric integrators, and by a run in this repository (§4).

The document contains no computation, data, or falsifiable prediction. Sections 21-24 and 28-31
(gauge theory, field equations, quantisation, shadow map, foam, bundle) are definitions, and the
"theorems" there are asserted without proof.

What survives is a vocabulary for well-known structures: finite group and monoid actions, word
metrics on Cayley graphs, and holonomy as a product of transition operators. Part of that vocabulary
maps usefully onto things veritas-holo already measures (§5).

## 3. Specific defects

1. **Admissibility is vacuous.**
   - Def 7.2 and 9.1 call an operator O : S → S admissible when O(s) ∈ S for all s ∈ S. Every function
     from S to S satisfies this by its type.
   - So H3/H4 closure under composition (eq. 7.7, 9.4, 13.2) is automatic: a composite of maps S → S
     is a map S → S.
   - Lemma 11.1, 11.2 and 13.6 therefore prove nothing. Lemma 13.6's proof supposes
     (O_i ∘ O_j)(s) ∉ S, which the types already rule out.
2. **Holonomy closure is stated two incompatible ways.**
   - Eq. 5.1.1 requires U(γ)x = x for **all** x and all loops. That makes every holonomy operator the
     identity, a flat geometry.
   - The document then builds a non-trivial holonomy group, gauge group and curvature on it
     (§21, §27).
   - Eq. 27.4 quietly weakens the requirement to U(γ)(s₀) = s₀ at the base point only.
   - Under 5.1.1 the holonomy group is trivial and §21 is empty. Under 27.4 the invariant is a
     different, much weaker one.
3. **Adjoints and inverses are used where they need not exist.**
   - Closure under adjoint (H4, eq. 29.5) and conjugation O R O⁻¹ (Prop 19.4, 27.4, B.5) need a
     linear structure and invertibility.
   - Admissible operators are arbitrary maps S → S, including non-invertible ones.
   - The "formal left-inverse" mentioned under Prop 19.4 does not exist for a non-injective map.
4. **Subtraction of operators is undefined.**
   - D_const O = ∇(s,O) − O∘∇(s,1) (eq. 23.1) and F_const (eq. 23.2) subtract maps on a bare finite
     set, which has no addition.
   - The field equations D F = 0 (Thm 23.3) are therefore not well-formed. They are also stated with
     no proof.
5. **The metric is defined circularly.** Eq. 25.2 defines d as an infimum of L(γ), and L (eq. 25.3)
   is defined as a sum of d.
6. **Analytic closure (H5) perturbs discrete objects.**
   - "R′ = R + εD stays in its sector" (eq. 8.3, 13.3) needs sectors to be open sets in an operator
     space. The document declares them a finite enumerated set.
   - For generic operators, a small perturbation moves the eigenvalues. Staying in a sector is
     therefore an assumption (an axiom) presented as a derived property (Lemma 13.7).
7. **Arithmetic closure (H6) is impossible as written.**
   - "f(σᵢ, σⱼ) ∈ K_adm for any admissible index operation f (addition, composition, enumeration)"
     (eq. 8.5).
   - A finite set is closed under addition only if the addition is modular (a finite monoid such as
     ℤ_n), and closure cannot hold for "any" operation.
8. **The Drift Lemma confuses numerical error with geometry.** Its proof (F.1, G.1) argues from
   truncation error in *numerical* discretisations. Four problems:
   - The exact continuum flow of a smooth system preserves its invariants exactly. Rotation on a
     sphere, unitary evolution and Hamiltonian flow (energy, symplectic form) are standard examples.
   - Structure-preserving integrators keep invariants to rounding for very long times:
     - symplectic integrators bound the energy error;
     - Lie-group integrators keep the state on the group.
     See Hairer, Lubich & Wanner, *Geometric Numerical Integration*; Iserles et al., "Lie-group
     methods", *Acta Numerica* 2000.
   - Rounding error in a product of unitary matrices grows slowly, not "unboundedly" in any practical
     sense (§4).
   - "Unless curvature is restricted to a discrete set" is asserted, not derived.
9. **Continuum-to-finite "collapse" is ill-defined.**
   - Thm 32.2(1) maps a continuum shadow manifold onto a finite S via Φ⁻¹. A continuum has no
     bijection with a finite set, and Φ is only injective on S (eq. 28.2).
   - "Constitutional equivalence up to relabelling" (§16, Lemma 32.4) is left loose enough that the
     theorem cannot be tested.
10. **Minimality and uniqueness are asserted.** Lemma 32.3 (the invariant set is the unique minimal
    one), 32.5-32.10 and Cor. 32.11-32.16 carry no proofs.
11. **The physical example has no content.** "Tokamak quantum mechanics" (§23.1) lists the four
    invariants in plasma words. There is no model, calculation or measurement.
12. **The worked examples are trivial.**
    - Ex. 1-3 (§10.1) are a 3-cycle permutation, a diagonal sign matrix, and O₁³ = I.
    - They are correct, but they are what is already known about cyclic groups.

## 4. Direct counterexamples (measured here)

- **E001 P5:** unitary evolution on the continuum state space ℂ³² kept every state's norm within
  2.11e-15 of 1 over the registered trajectory (x86_64), and 2.66e-15 on the S25. A continuum
  representation preserved the invariant to rounding, with no finite state space.
- **E008 (registered before its run; 4 of 4 held):** an exact continuum representation of S5, run for
  10⁶ steps in float64, stayed within 6.48e-10 of the true state and decoded perfectly, on 3 seeds.
  Drift grows linearly, about 6e-16 per step, so it would take about 10¹⁵ steps to matter. **Operator
  error** is what breaks a representation: at 1e-2 per step, decoding reached chance by 10⁴ steps.
  Snapping to the finite set of valid states every step kept decoding exact to 10⁵ steps. Snapping only
  every 10 steps failed at an error of 0.1. So a finite codebook is a useful *tool* against accumulated
  model error, not a *necessity* for preserving invariants.

## 5. What is usable, with its real name and prior art

| Document's term | Standard object | Use here |
|---|---|---|
| admissible states and operators, closed algebra | a finite set with a monoid or group action; a representation | E004-E007 are exactly this: S5 acting on 120 states, with learned operators |
| holonomy closure U(γ) = I on loops | relators of a group presentation (words equal to the identity) | **E006's relator score is a measured "holonomy closure"**, and it predicted training success (17/17 each way) |
| sector restriction | quantisation to a finite codebook, i.e. error correction by projection | **E008:** snapping learned or noisy operators' running state to the nearest valid state stops accumulated error |
| constitutional metric and geodesics | word metric and shortest paths on the Cayley graph | a minimal admissible action sequence (BFS); possible use in sovereign-veritas planning checks |
| gauge transformation O ↦ gOg⁻¹ | change of basis / conjugation | the E008 codebook is conjugated by V; readouts must be basis-invariant |
| "drift" | error accumulation in long products | the measured quantity in E008; E005-E007 face it with learned operators |

Two ideas worth carrying into the builds:

1. **Loop residual as a health monitor (veritas-holo, veritas-companion).**
   - Any system whose transitions should compose consistently can be checked on loops.
   - A loop is a sequence that should return to where it started. Its residual measures
     inconsistency, and it needs no test data (E006 is the S5 case).
   - For the companion, two routes to the same fact that give different values are a loop that does
     not close, which is the UNCERTAIN status it already has. C003 can measure it that way.
2. **Snap-to-codebook for long horizons (veritas-holo).**
   - A learned representation that is almost right fails at long lengths because error accumulates.
   - Projecting the running state onto the finite set of valid states, often enough, removes the
     accumulation. E008-U1 would build the codebook from data for E005's learned operators.

**Not usable as claimed:** the necessity theorem, the unification theorem, the field equations, and
any statement that finite-state structure is *required* for invariant preservation.

## 6. If the author wants the claims tested

Ask for one quantitative prediction that the framework makes and a standard method does not. For
example: a multi-body system, an integrator, a horizon, and a measured invariant error that exceeds a
stated bound without sector restriction and stays under it with sector restriction. That can be
registered and run here.
