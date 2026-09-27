# E001 — results

Registration: [PREREG.md](PREREG.md), committed before the runner existed.

## Container x86_64, Python 3.11.15, NumPy 2.4.4, seed 1

```
VERITAS-HOLO E001 | seed 1 | x86_64 | Python 3.11.15 | NumPy 2.4.4
state dimension 32, operators 8, trajectory length 12
HELD   P1  max ||U'U-I|| 7.22e-14, max |det U-1| 7.83e-14
HELD   P2  max d(A'Ax, x) 3.26e-15
HELD   P3  min ||[Ai,Aj]|| over 28 pairs 0.2352
HELD   N3  max ||[Di,Dj]|| over 28 diagonal pairs 0.00e+00
HELD   P4  slope 2.0000, h(0.001)/0.001^2 / ||[X,Y]|| = 1.000000
HELD   N4  max h(eps) for diagonal X, Y 7.20e-16
HELD   P5  checker PASS, worst | ||x_k|| - 1 | 2.11e-15
HELD   N5  checker FAIL, worst | ||x_k|| - 1 | 0.0818
HELD   P6  |d(Ux,Ux') - d(x,x')| 4.15e-17 (d(x,x') = 9.903e-07)
HELD   P7  seed 1 twice: b9e9b84f9688c364 b9e9b84f9688c364; seed 2: 68243756c48f906d
state holonomy d(A1 A2 A1' A2' x, x) = 0.0378  (reported, not predicted)
replay digest b9e9b84f9688c364ba037fa0279ea1794d7e2b0a4ff062b769a9c6ab94f803b5
VERDICT  10 of 10 registered predictions and nulls held
```

Seeds 2 to 5, same machine: `VERDICT  10 of 10 registered predictions and nulls held` each.
Full record: `results/verified/E001_seed1_x86_64.json`.

## What held, and what it means

- **P1-P7 held, and the three nulls behaved.** The diagonal operators commuted (N3, exactly 0),
  their loop had no holonomy (N4, 7.20e-16), and the non-unitary sham was caught (N5, norm error
  0.0818). So the checks can say no.
- **P4 is the one non-trivial numerical prediction:** holonomy around a small loop scales as ε²
  (slope 2.0000) with the coefficient ||[X, Y]|| to six places. That is the Baker-Campbell-Hausdorff
  formula, confirmed in this implementation.
- **What it does not mean.** Every property here is a known property of unitary matrices. E001
  shows the instrument is built correctly. It shows nothing about reasoning, and the state holonomy
  0.0378 is a number, not yet a signal: whether holonomy carries useful information is P8, E002's
  question, not run.

## Found while testing

- The sabotage test (every operator forced diagonal) made P3 fail as it should, but the first
  version of the test compared NumPy's `np.False_` to Python's `False` with `is`, which never
  matches; it now converts with `bool()`. The runner's verdicts were right throughout.
- Under that sabotage P4's ratio divides by ||[X, Y]|| = 0 and NumPy warns; P4 then fails, which is
  the correct verdict.

## Still open

- **P8** (E002): does holonomy along task-solving paths carry information a matched sham cannot?
- **P9**: the seed-1 digest on the S25 (aarch64). Command:
  `python experiments/E001_operator_algebra/run.py --json results/registered/E001_seed1_aarch64.json`

## P9 on the S25 (Termux, aarch64, Python 3.14.6, NumPy 2.4.4), 2026-09-27

```
VERITAS-HOLO E001 | seed 1 | aarch64 | Python 3.14.6 | NumPy 2.4.4
state dimension 32, operators 8, trajectory length 12
HELD   P1  max ||U'U-I|| 6.87e-14, max |det U-1| 7.16e-14
HELD   P2  max d(A'Ax, x) 3.07e-15
HELD   P3  min ||[Ai,Aj]|| over 28 pairs 0.2352
HELD   N3  max ||[Di,Dj]|| over 28 diagonal pairs 1.94e-16
HELD   P4  slope 2.0000, h(0.001)/0.001^2 / ||[X,Y]|| = 1.000000
HELD   N4  max h(eps) for diagonal X, Y 7.20e-16
HELD   P5  checker PASS, worst | ||x_k|| - 1 | 2.66e-15
HELD   N5  checker FAIL, worst | ||x_k|| - 1 | 0.0818
HELD   P6  |d(Ux,Ux') - d(x,x')| 1.70e-17 (d(x,x') = 9.903e-07)
HELD   P7  seed 1 twice: 8f42fa22d14b5d6e 8f42fa22d14b5d6e; seed 2: f252ca0984c04411
state holonomy d(A1 A2 A1' A2' x, x) = 0.0378  (reported, not predicted)
replay digest 8f42fa22d14b5d6eb74ce79613a66cea545ff29ffa938db802c3c12d6a98c2d9
VERDICT  10 of 10 registered predictions and nulls held
```

- **All ten held on the phone too.** Every value printed at four or more digits is the same as on
  x86_64 (0.2352, slope 2.0000, ratio 1.000000, 0.0818, 0.0378); only the rounding-level residues
  differ (e.g. N3: 1.94e-16 here, 0.00e+00 there).
- **P9 refuted.** The replay digest differs: `8f42fa22…` on the S25, `b9e9b84f…` on x86_64. Replay
  is exact per platform (P7 held on both) but not across them: the states agree to rounding and
  differ in their last bits, which a sha256 over raw bytes sees. The registration expected this was
  possible ("different BLAS and LAPACK builds"); it is now measured. Same lesson as
  sovereign-veritas's model replies: a byte-level fingerprint is a claim about the exact kernels
  that ran.
- **P10 (registered, not run):** a digest over the states rounded to 10 decimal places matches on
  both platforms for seeds 1 to 5. The worst differences seen here are around 1e-14, so rounding at
  1e-10 should absorb them, unless a value sits on a rounding boundary; that is the way it could
  fail.

## P10, x86_64 side (container, 2026-09-27)

`Trajectory.digest(decimals=10)` rounds real and imaginary parts to 10 places and adds 0.0 so that
-0.0 and 0.0 hash alike. A new test pins the instrument: 1e-14 noise changes the raw digest but not
the rounded one, a 1e-6 change still shows, and -0.0 equals 0.0 (13 passed). E001 verdicts unchanged
(10 of 10, seeds 1-5). Rounded digests on x86_64, to be compared with the S25:

```
seed 1  a20f68e73d04bbf7d6b322884859725e940c4f3505ba02377f100bb9efbb068b
seed 2  c6a52390c8b442d7d4ddee1afe33c85b85b1fe5916db4a4b12691d3961720055
seed 3  958217cbd993dc68de4bec7928eac9f61579a24b17f13e9d4c15d8cbbed54022
seed 4  0ce75d98dbe5a24d25d26097e69d6a71f6a06d5c5b3c39dc68b5b8a711f80ca0
seed 5  833b7caa8e650ea90eaf3ef4bedb7ff3fe54d6f6f0597ac0c8c6b83a3ef9897d
```

## P10 on the S25 (Termux, aarch64), same day

```
rounded digest (10 dp, P10) a20f68e73d04bbf7d6b322884859725e940c4f3505ba02377f100bb9efbb068b VERDICT  10 of 10 registered predictions and nulls held
rounded digest (10 dp, P10) c6a52390c8b442d7d4ddee1afe33c85b85b1fe5916db4a4b12691d3961720055 VERDICT  10 of 10 registered predictions and nulls held
rounded digest (10 dp, P10) 958217cbd993dc68de4bec7928eac9f61579a24b17f13e9d4c15d8cbbed54022 VERDICT  10 of 10 registered predictions and nulls held
rounded digest (10 dp, P10) 0ce75d98dbe5a24d25d26097e69d6a71f6a06d5c5b3c39dc68b5b8a711f80ca0 VERDICT  10 of 10 registered predictions and nulls held
rounded digest (10 dp, P10) 833b7caa8e650ea90eaf3ef4bedb7ff3fe54d6f6f0597ac0c8c6b83a3ef9897d VERDICT  10 of 10 registered predictions and nulls held
```

**P10 confirmed.** Seeds 1-5: all five rounded digests identical to the x86_64 ones recorded before
this run, and 10 of 10 held on every seed on both platforms. So E001's trajectories replay across
Arm (Qualcomm Oryon) and x86 (Intel Xeon) to 10 decimal places; the raw-byte digest (P9) does not.
The stated way it could still fail, a value landing on a rounding boundary, did not happen in
these 5 x 13 states; it remains possible for other seeds and is why the claim is "5 seeds", not
"always".
