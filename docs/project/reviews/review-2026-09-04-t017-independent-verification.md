# Review 2026-09-04 — independent verification of T-017 (s(12) ≥ 77/20)

An independent reviewer, given the theorem statement and the two retained certificate
files only, with the project’s implementation withheld, wrote a verifier from scratch
and ran it on both certificates.
The verifier is retained verbatim as
[`independent_verify.py`](../../../packing/cases/n12_fractional_certificate/independent_verify.py).
What follows is the reviewer’s report and proof check, unedited.

## Report

**Verdict: ACCEPT.** Both retained certificates verify.
Written from the theorem statement only; no project code read or reused.
Exact rational arithmetic throughout.

## Proof (details in `proof-check.md`)

Every step holds. Two remarks, neither fatal:

- `D = (t_{k+1}-t_k)/(1+t_k t_{k+1})` is the tangent of the maximal **half**-gap, not
  the full gap as the statement’s parenthetical says.
  Since `theta = 2 arctan t`, the formula is exactly `tan((theta_{k+1}-theta_k)/2)` —
  precisely (and tightly) what Step 2 needs.
  Prose error, not a hypothesis error.
- `C4` quantifies over every placement in the *closed* container, a strict superset of
  the placements the proof meets.
  Superset = stronger hypothesis = sound.
  Likewise the closed-square/boundary-atom convention is safe because `Q ⊂ int(S)`
  **strictly** (from `C3`), so boundary atoms of `Q` still lie in one unit square’s
  interior and are never double-counted.
  Closed vs open container only makes `C4` harder; the conclusion is `s(n) > L`, of
  which the claimed `s(n) >= L` is a weakening.

## Method (`verify.py`)

Per direction I work in the rotated frame scaled by `m = q^2+p^2` (`t = p/q`), so
`cos`/`sin` are exact integers `(q^2-p^2, 2pq)`. Covered mass is piecewise constant on
the arrangement of the `2N` atom-square edges per axis.
I enumerate **all** arrangement pieces — open intervals, and the breakpoints themselves
— in both axes (453 pieces each for 113 atoms), and mass on each cell is summed
**directly over atoms** (an atom-indexed inner product; no prefix sums, no difference
arrays). The admissible-centre set is exactly `[delta, L-delta]^2` in `xy` with
`delta = (B/2)(cos+sin)`. I compute two bounds: a **lower** bound over every cell whose
*closure* meets that set (exact polygon clipping), and an **upper** bound over cell
representatives *provably inside* it.
They coincided at every direction of both certificates, so the continuum minimum is
pinned exactly.

Cross-checks: a separate naive implementation (full breakpoint+midpoint grid,
four-corner feasibility test, Fraction-by-Fraction atom sums) agrees exactly at k = 0,
1, 57, 180 on both certificates (149 s). 4,525 randomly sampled cells re-summed by brute
force matched. Negative control: same atoms with `L` enlarged to 4 gives C4 min = 1/10
(correctly fails).

## Results — all 181 directions (k = 0..180) checked for both

|  | 19/5 (68 atoms) | 77/20 (113 atoms) |
| --- | --- | --- |
| C0 D4-invariance | PASS | PASS |
| C1 `sum w < 12` | PASS, 58/5 = 11.6 | PASS, 191/16 = 11.9375 |
| C2 `t_K^2+2t_K-1 >= 0` | PASS, = 309449/2.5e11 | same |
| C3 `B(1+D) < 1` | PASS, D = 207107/90000000, B(1+D) = 899635478111/900000000000 = 0.999594975679 | same |
| C4 exact min mass | **1 exactly** at k=0, centre (12427/20000, 12427/20000) | **1 exactly** at k=0, centre (115047/220000, 115047/220000) |
| C4 runtime | 5.4 s | 11.7 s |

C4 is tight (min = 1, not more); C1 and C3 have slack.
All atoms lie in `[0,L]^2`.

## Break tests on the 77/20 certificate (atom #0 = (37/44, 423/440, 7/32))

| perturbation | refused? | failing condition(s) |
| --- | --- | --- |
| weight −1/10000 | yes | C0, and C4 (min drops to 9999/10000) |
| drop the atom | yes | C0, and C4 (min drops to 25/32) |
| shift x by +1/1000 | yes | **C0 only** — C4 still holds at 1 |
| (bonus) −1/10000 across the whole D4 orbit | yes | **C4 only** (min 4999/5000); C0–C3 pass |

No discrepancy with the claim.
`total_mass` and `least_cell_mass` in the JSON match what I computed independently.

## Proof check

Verdict up front: **every step holds**. One label in the statement I was given is wrong
(the parenthetical describing `D`), but the *formula* for `D` is the correct, tight one,
so the hypothesis `C3` is exactly what the proof needs.
Details in step 3.

Notation: container `K = [0,L]^2`, shrink `B`, net `0 = t_0 < ... < t_K`,
`theta_k = 2 arctan(t_k)`, atoms `(x_i, y_i, w_i)`, total mass `W = sum w_i`.
`mass(X) = sum of w_i over atoms with (x_i,y_i) in X`.

## Step 0. What is being contradicted

Assume `n` closed unit squares `S_1..S_n` with pairwise disjoint interiors, all
contained in `K`. We derive `n <= W`, contradicting `C1` (`W < n`).

## Step 1. Reduce the orientation to [0, pi/4]

A square is invariant under rotation by `pi/2`, so its orientation `phi` may be taken in
`[0, pi/2)`. If `phi > pi/4`, apply the reflection `R(x,y) = (y,x)`, which maps `K` onto
itself.
`R` sends direction angle `alpha` to `pi/2 - alpha`, so `R(S_j)` is a unit square
inside `K` with orientation `pi/2 - phi` in `[0, pi/4)`. **Checks out.** Note the proof
only needs invariance under this one reflection; `C0` demands the full dihedral group
`D4`, which is a strictly stronger hypothesis and therefore safe.

## Step 2. The concentric shrunken square

Let `S` be a unit square, centre `c`, orientation `phi` in `[0, pi/4]`. Pick a net angle
`theta_k` with `d = |phi - theta_k|`. Let `Q` be the **closed** square of side `B`,
centred at `c`, at orientation `theta_k`.

`Q` is contained in the open interior of `S` iff for each of the four edge normals `u`
of `S`, the support function of `Q - c` in direction `u` is `< 1/2`. That support value
is `(B/2)(|cos a| + |sin a|)` where `a` is the angle between `u` and `Q`’s axes; for all
four normals `a` differs by multiples of `pi/2`, so all four give `(B/2)(cos d + sin d)`
for `d` in `[0, pi/4]`. Hence

```
Q strictly inside int(S)  <==  B (cos d + sin d) < 1.
```

Since `cos d + sin d = cos d (1 + tan d) <= 1 + tan d`, it suffices that
`B (1 + tan d) < 1`. **Checks out.**

## Step 3. The angular net, and what D really is

`theta_0 = 0`, and `C2` (`t_K >= tan(pi/8)`, equivalently `t_K^2 + 2 t_K - 1 >= 0`)
gives `theta_K = 2 arctan(t_K) >= pi/4`. So every `phi` in `[0, pi/4]` lies in some
`[theta_k, theta_{k+1}]`, and choosing the nearer endpoint gives
`d <= (theta_{k+1} - theta_k)/2`.

Now `(theta_{k+1} - theta_k)/2 = arctan(t_{k+1}) - arctan(t_k)`, whose tangent is
exactly `(t_{k+1} - t_k)/(1 + t_k t_{k+1})` — the quantity defining `D`. So **`D` is the
tangent of the maximal HALF-gap, not of the full gap**; the parenthetical in the
statement I was handed ("this is tan of the full angular gap") mislabels it.
That does not damage anything: `tan` is increasing on `[0, pi/2)`, so `tan d <= D`, and
with `C3` (`B(1+D) < 1`) Step 2 applies.
`D` is in fact the tight constant; had `D` been the tan of the *full* gap it would
merely have been a more conservative (still valid) choice.
The error is in the prose, not in the hypothesis.
**Checks out.**

## Step 4. Applying C4

For the (possibly reflected) square `S' = R^e(S)`, we have `Q ⊂ int(S') ⊂ S' ⊂ K`. So
`Q` is a closed `B`-square at a net direction lying inside the **closed** container.
That is precisely an instance of `C4`, so `mass(Q) >= 1`.

`C4` quantifies over *every* such placement inside `K`, which is a strict **superset**
of the placements the proof actually meets (those inside some unit square of the
hypothetical packing).
Quantifying over a superset makes the hypothesis stronger, so the implication is sound;
the verifier can only be too demanding, never too permissive.
**Checks out.**

## Step 5. The closed-square / boundary-atom convention

`C4` counts an atom on the boundary of the closed `B`-square as covered.
This is legitimate because Step 2 gives `Q ⊂ int(S')` *strictly*: every atom of `Q`,
boundary included, lies in the open interior of `S'`. So the closed convention never
double-counts across squares.
It also makes the covered-mass function upper semicontinuous — the boundary value is
`>=` the value on either adjacent cell — which is why a verifier must sample the
arrangement’s edges and vertices as well as its open cells (they can only carry *larger*
values, so omitting them is safe for the minimum, but including them is needed to report
the function correctly).
**Checks out.**

## Step 6. Pulling back and summing

Let `Q_j` be the shrunken square for `S_j` and `P_j = R^{e_j}(Q_j)` its pullback (`e_j`
in {0,1}). `C0` says the weighted atom multiset is `D4`-invariant, so
`mass(P_j) = mass(Q_j) >= 1`. And `P_j ⊂ int(S_j)`.

The interiors `int(S_j)` are pairwise disjoint, hence so are the `P_j`, hence each atom
contributes its weight to at most one `P_j`. Therefore

```
n <= sum_j mass(P_j) <= W < n     (last inequality is C1),
```

a contradiction. **Checks out.** (Note the mass sums are over finitely many atoms with
nonnegative weights, so no convergence issue.)

## Step 7. Closed vs open container, and the final inequality

The contradiction rules out a packing in the **closed** square `K = [0,L]^2`. If
`s(n) <= L`, then `n` unit squares fit in a square of side `s(n) <= L` — actually it
suffices that for any `L' > s(n)` a packing exists in side `L'`, but we can avoid the
attainment question entirely: if `s(n) < L`, take any `L'` with `s(n) <= L' < L`
admitting a packing; a closed square of side `L'` embeds in `K`, contradiction.
If `s(n) = L`, a packing in side exactly `L` exists by the standard compactness
argument, again a contradiction.
Either way `s(n) > L`, and in particular the claimed `s(n) >= L`.

So the stated conclusion `s(n) >= L` is **weaker** than what the argument gives
(`s(n) > L`) and is therefore safe.
Working with the closed container rather than the open one is the conservative choice:
`C4` is required at more placements.
**Checks out.**

## Summary of the only two soft spots

1. `D` is mislabelled in the statement (half-gap, not full gap).
   The formula is right and `C3` is the correct sufficient condition.
   No consequence.
2. `C4` is stated over all placements in the closed container — a superset of what is
   needed. This is a strengthening, so it is sound; it is also what makes the condition
   checkable without reference to any particular packing.
