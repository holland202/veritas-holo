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
