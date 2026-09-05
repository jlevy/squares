# Self-Contained Package for Third-Party Checking of s(11) ≥ 19/5

Everything a reader needs to check, with their own tools and without trusting this
repository, that eleven unit squares do not fit in a square of side 3.8. The directory
can be copied out of the checkout and run without importing code from the rest of the
project or installing its dependencies: a certificate as plain data, the theorem it
instantiates written out with its proof, a single-file verifier that uses only Python’s
standard library, a control reconstructed from another author’s published result, and
the perturbations the verifier refuses.

It is not itself a third-party check, and the name says so.
This project wrote every file here, on the day of the result; a package assembled by the
party making the claim cannot be the independent check of it.
What the package supplies is the material such a check needs, so that making it is
someone else’s to do.

## The Claim

Let `s(n)` be the side of the smallest square that contains `n` unit squares with
pairwise disjoint interiors, the unit squares being free to rotate.
(Formally `s(n)` is the infimum of the sides that admit such a packing; a compactness
argument shows the infimum is attained, but nothing below needs that.)

**Claim.** `s(11) ≥ 19/5 = 3.8`.

This package checks that claim, and everything below is about it.
The repository has since certified a larger value for the same case,
`s(11) ≥ 381/100 = 3.81`, retained at `../certificate.json` and decided by two verifiers
that fail differently.
The package deliberately still carries `19/5`: it is the artifact an adversarial review
read line by line, and its pasted numbers are that review’s observations.
Nothing here is stale — `19/5` is a retained rung and the argument for it is the
argument for the larger value — but a reader who wants the repository’s current best
bound should read the case record rather than this file.

The shortest complete check of that larger value is one directory up rather than in this
package: `../minimal_verify.py` decides the retained `381/100` bytes the way `verify.py`
decides these, from one file that uses Python’s standard library and nothing else, and
`python3 minimal_verify.py certificate.json` reaches `VERIFIED s(11) >= 381/100` in
about 47 seconds. `../PROOF-CARD.md` states that claim on one page with the constants it
turns on.

What it displaces: the lower bound `2 + 4/√5 = 3.788854…` stated by Walter Stromquist,
*Packing 10 or 11 unit squares in a square*, Electronic Journal of Combinatorics 10
(2003), R8
([link](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r8)). That
the new value is larger is decided in integers: both sides being positive,

```
19/5 > 2 + 4/√5   iff   19/5 − 2 > 4/√5   iff   (19/5 − 2)² · 5 > 16   iff   81/5 > 16,
```

and `81/5 = 16.2`. The movement is `19/5 − (2 + 4/√5) = 0.011145…`.

What it does not say: the best known packing of eleven unit squares, found by Walter
Trump in 1979, has side `3.877083…` (the root of
`s⁸ − 20s⁷ + 178s⁶ − 842s⁵ + 1923s⁴ − 496s³ − 6754s² + 12420s − 6865` near that value;
see Erich Friedman’s survey *Packing Unit Squares in Squares*,
[link](https://erich-friedman.github.io/papers/squares/squares.html)). So
`3.8 ≤ s(11) ≤ 3.877083…`, the case stays open, and nothing here bears on whether
Trump’s packing is optimal.
The argument shows that a container of side exactly `19/5` is too small; the strict
inequality `s(11) > 19/5` also follows (by compactness), but the claim is the weak one.

## Run It

| File | What it is |
| --- | --- |
| `certificate.json` | The `n = 11` certificate at `19/5`, plain data, byte-identical to `../certificate-19-5.json` (SHA-256 `60ac0c33e2e5a55874a10b0d09c6aaf3f891db921b063cc860114c2d4588c055`). Not regenerated for this package. `../certificate.json` is the case’s *top* rung and now carries `381/100`, a different file with a different hash; see the note under the claim. |
| `verify.py` | The verifier: one file, standard library only, exact rational arithmetic, no imports from this repository. |
| `control-n17-massaccesi.json` | Gustavo Massaccesi’s published `n = 17` certificate, rebuilt as data in the same schema. |
| `build_n17_control.py` | Rebuilds the control file from the constants of its published source; `--check` confirms the shipped file matches. |
| `falsify.py` | Applies the perturbations in the falsification table, checks each against the result it must produce, and prints what the verifier refuses. `--quick` runs the bounded negative-weight control alone. |
| `check.py` | The whole check in one command. |

One command, with whatever `python3` is on your `PATH` (CPython 3.8 or later, tested
with 3.10 through 3.14, nothing installed):

```shell
python3 check.py
```

It rebuilds the control data and compares it to the shipped file, then runs `verify.py`
on the certificate and on the control.
Each run prints every condition with its numbers and ends in `VERIFIED` or `REFUSED`;
the script exits non-zero on any refusal.
Expect about half a minute.
Condition 5 took 22 to 27 s on the certificate and 7 to 8 s on the control with CPython
3.10 through 3.14 on an idle core, and 39 s and 14 s in the pasted run below, on a
contended one. The outputs are pasted verbatim below.

## The Theorem

The argument is a weighted, fractional form of the classical *unavoidable set* argument
for square packing. Sam Burns published it in August 2026 for `n = 17`
([post](https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/)),
and Gustavo Massaccesi improved the `n = 17` bound the same month with a certificate
found by linear programming, in the shape used here
([post](https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html),
[method](https://gus-massa.blogspot.com/2026/08/linear-programing-for-square-packing.html)).
Neither the theorem nor the certificate shape is this project’s; the `n = 11` instance
is.

**Data.** An integer `n ≥ 1`; rationals `L > 0` (the container side) and `B > 0` (the
shrunken side); a *direction net* of rationals `0 = t₀ < t₁ < … < t_K`, standing for the
angles `θ_k = 2 arctan(t_k)`; and finitely many *atoms* `(x_i, y_i, w_i)` with rational
coordinates and rational weights `w_i ≥ 0`. For a set `Q` in the plane write
`mass(Q) = Σ { w_i : (x_i, y_i) ∈ Q }`. The container is the closed square
`K = [0, L]²`.

**Hypotheses.**

- **Condition 1.** The weighted atom set is invariant under the eight symmetries of `K`:
  for every atom, each of the eight images of its site under
  `(x, y) ↦ (x, y), (L−x, y), (x, L−y), (L−x, L−y), (y, x), (L−y, x), (y, L−x), (L−y, L−x)`
  is a site of the same total weight.
  (The proof uses only the reflection `(x, y) ↦ (y, x)`; the certificate declares the
  full group, and checking it is a stronger hypothesis, hence safe.)
- **Condition 2.** `Σ w_i < n`.
- **Condition 3.** `θ_K ≥ π/4`. Since `tan(π/8) = √2 − 1` is the positive root of
  `t² + 2t − 1` and that polynomial increases for `t ≥ 0`, this is exactly
  `t_K² + 2t_K − 1 ≥ 0`, a rational inequality.
- **Condition 4.** `B(1 + D) < 1`, where
  `D = max_k (t_{k+1} − t_k) / (1 + t_k t_{k+1})`. Since `θ = 2 arctan t`, half the gap
  between adjacent net angles is `arctan(t_{k+1}) − arctan(t_k)`, whose tangent is
  exactly that quotient; so `D` is the tangent of the largest *half*-gap.
- **Condition 5.** For every `k` and every closed square `Q` of side `B` whose edges
  make angle `θ_k` with the axes and which lies inside `K`: `mass(Q) ≥ 1`.

**Conclusion.** `n` unit squares with pairwise disjoint interiors do not fit in `K`;
hence `s(n) ≥ L`.

## The Proof

Suppose closed unit squares `S₁, …, S_n ⊂ K` have pairwise disjoint interiors.
We derive `n ≤ Σ w_i`, contradicting Condition 2.

1. **Orientation reduction.** A square is unchanged by a quarter turn, so its
   orientation `φ` (the angle its edges make with the axes) may be taken in `[0, π/2)`.
   If `φ > π/4`, apply the reflection `R(x, y) = (y, x)`. It maps `K` onto itself and
   sends a direction at angle `α` to angle `π/2 − α`, so `R(S_j)` is a unit square in
   `K` with orientation `π/2 − φ ∈ (0, π/4)`. Write `S'_j` for `S_j` or `R(S_j)`,
   whichever has orientation `φ' ∈ [0, π/4]`.
2. **A net angle nearby.** By Condition 3 and `t₀ = 0`, the net angles run from `0` to
   at least `π/4`, so `φ'` lies in some `[θ_k, θ_{k+1}]`, and the nearer endpoint `θ`
   satisfies `d := |φ' − θ| ≤ (θ_{k+1} − θ_k)/2`. Since `tan` increases on `[0, π/2)`,
   `tan d ≤ D`.
3. **A concentric shrunken square.** Let `Q` be the closed square of side `B`, centred
   at the centre of `S'_j`, with orientation `θ`. Its support function in the direction
   of any edge normal of `S'_j` is `(B/2)(cos d + sin d)`, while `S'_j` extends `1/2`
   from its centre in that direction; so `Q` lies in the open interior of `S'_j` as soon
   as `B(cos d + sin d) < 1`. Now
   `cos d + sin d = cos d · (1 + tan d) ≤ 1 + tan d ≤ 1 + D`, and Condition 4 gives
   `B(1 + D) < 1`. Hence `Q ⊂ int(S'_j) ⊂ K`, strictly inside.
4. **Condition 5 applies.** `Q` is a closed `B`-square at the net angle `θ` lying inside
   `K`, so `mass(Q) ≥ 1`.
5. **Pull back.** Let `P_j = Q` if `S'_j = S_j`, and `P_j = R(Q)` otherwise.
   Then `P_j ⊂ int(S_j)`, and `mass(P_j) = mass(Q) ≥ 1` because by Condition 1 the
   weighted atom set is invariant under `R` (the atoms inside `R(Q)` are the images of
   the atoms inside `Q`, with the same weights).
6. **Count.** The interiors of the `S_j` are pairwise disjoint, so the `P_j` are
   pairwise disjoint and each atom lies in at most one of them.
   With `w_i ≥ 0`, `n ≤ Σ_j mass(P_j) ≤ Σ_i w_i < n`. Contradiction.

So no such packing exists in `[0, L]²`. If `s(n) < L`, the definition of the infimum
gives a packing in some square of side `L' < L`, which sits inside `[0, L]²`; therefore
`s(n) ≥ L`.

Two remarks a careful reader will want settled.
First, `Q` is closed and Condition 5 counts atoms on its boundary; this never
double-counts, because step 3 puts `Q` strictly inside the interior of one unit square.
Second, Condition 5 quantifies over every `B`-square inside `K` at a net angle, a
superset of the squares the proof meets; a stronger hypothesis can only make the theorem
harder to apply, never unsound.

## The Certificate

`certificate.json` carries:

| Quantity | Value |
| --- | --- |
| `n` | 11 |
| `L` (`outer_side`) | `19/5 = 3.8` |
| `B` (`square_side`) | `9977/10000` |
| Net | `t_k = (207107/500000) · k / 180`, `k = 0, …, 180` (181 directions) |
| `t_K` | `207107/500000 = 0.414214`, against `tan(π/8) = 0.4142135…`; slack `t_K² + 2t_K − 1 = 309449/250000000000` |
| `D` | `207107/90000000`; `B(1 + D) = 899996306539/900000000000 = 0.9999958…` |
| Atoms | 425, on 425 distinct sites, all inside `[0, L]²`, invariant under all eight symmetries |
| Total weight | `43391/4000 = 10.84775 < 11` |
| Least covered weight | `50003/50000 = 1.00006`, attained at direction 0 by the square centred at `(53/100, 53/100)`; over all 181 directions, 90,546,593 cells decided |

The margin in Condition 5 is `6/100000`, and the margin in Condition 4 is `4.1 × 10⁻⁶`.
Both are decided exactly; a floating-point check would have no business here.

**Schema.** A JSON object with the fields below.
Every rational is a string matching `-?[0-9]+(/[1-9][0-9]*)?`; the verifier refuses any
other form, so a decimal or a float cannot enter and be rounded.
It also refuses a duplicate object key, a non-integer or Boolean `n` or
`direction_steps`, a JSON number where a rational string belongs, a malformed atom row,
and a missing required field — each by name, before any condition is decided, rather
than coercing the value or failing partway through the sweep.

| Field | Type | Meaning |
| --- | --- | --- |
| `n` | integer | the number of unit squares |
| `outer_side` | rational | `L` |
| `square_side` | rational | `B` |
| `angle_limit` | rational | `T`; the net is `t_k = T · k / K` |
| `direction_steps` | integer | `K` |
| `atoms` | array of `[x, y, w]` | rational site coordinates and weight |
| `claim` | string | must read `s(n) >= L` for the file’s own `n` and `L`; the verifier checks this so the label cannot mislead |
| `total_mass`, `least_cell_mass` | rational | the record’s own bookkeeping; optional, but recomputed and compared if present, and a disagreement is a refusal |
| `id`, `symmetry` | string | labels; Condition 1 checks the symmetry regardless of what is declared |

## The Verifier

`verify.py` reads the file, checks the shape the theorem assumes (`n ≥ 1`, positive
sides, non-negative weights, a net that starts at 0 and increases, the declared claim
equal to the theorem’s conclusion), then decides Condition 1 to Condition 5 in that
order and prints each with its numbers.
None of Condition 1 to Condition 5 short-circuits: a file failing Condition 2 still has
its Condition 5 minimum computed, so a refusal names every failing condition among them.
The preconditions are different — a file that fails one of those is refused there and
the conditions are not reached, because a malformed file has no conditions to decide.
Every quantity is a `fractions.Fraction`; floats appear only in printed approximations
beside the exact value.

Condition 1 to Condition 4 are closed-form rational tests and can be read off the code
in a minute. Condition 5 is the substance, and it is decided over the continuum of
placements, not sampled:

- Fix a net direction with exact cosine `c = (1 − t²)/(1 + t²)` and sine
  `s = 2t/(1 + t²)`, so `c² + s² = 1` exactly.
  Rotate coordinates so the placed square is axis-parallel: `u = cx + sy`,
  `v = −sx + cy`. A closed `B`-square centred at `(U, V)` covers the atom at
  `(u_i, v_i)` iff `|u_i − U| ≤ B/2` and `|v_i − V| ≤ B/2`; the covered weight is a sum
  of indicator functions of closed boxes, one per atom.
- The square lies inside `K` iff its centre `(X, Y)` satisfies `h ≤ X, Y ≤ L − h` with
  `h = B(|c| + |s|)/2`. That closed square of admissible centres, `F`, is a rotated
  square in the `(U, V)` plane with four exactly known corners.
- The values `u_i ± B/2` and `v_i ± B/2` cut the plane into a grid of open cells.
  On an open cell the covered weight is constant (every box has its edges on grid
  lines). A point on the boundary of a cell covers at least what the cell covers (a
  closed box containing a point of the cell contains the cell’s closure).
  And every point of `F` is on the closure of some open cell that meets `F`, because `F`
  has interior points arbitrarily close to each of its points.
  Therefore the minimum of the covered weight over `F` is the minimum over the open
  cells that meet `F`, and cell boundaries never need to be visited: they can only carry
  more.
- Whether an open cell `(a, b) × (c′, d)` meets `F` is decided exactly by clipping the
  polygon `F` to the strip `a ≤ U ≤ b` (exact rational Sutherland-Hodgman clipping),
  reading off the `V`-range `[lo, hi]` of the clipped polygon, and testing `c′ < hi` and
  `lo < d`; the Condition 5 comment block in `verify.py` proves this test is exact for
  the open cell, not just its closure.
- The weight on every cell is computed by a two-dimensional prefix sum over integer
  weights (the rational weights times their common denominator).
  The minimising cell’s weight is then recomputed by direct summation over the atoms, at
  an explicit centre inside that cell and inside `K`, in the original coordinates; a
  disagreement aborts the run.
  `--audit N` re-sums `N` further random admissible cells per direction the same way.

Two things the verifier does at the edges of that argument are worth writing down,
because in both the reader is owed the reason and not just the behaviour.

**A declared number that disagrees with the replay is a refusal, not a note.** The
theorem does not use `total_mass` or `least_cell_mass`; the conditions are decided from
the atoms. But a file that states its own least covered weight and states it wrongly is
wrong about itself, and a checker that prints that as an aside and then says `VERIFIED`
has certified bytes it disagrees with.
The recomputed values are compared against the declared ones, a mismatch is counted with
the failing conditions, and no such file ends in `VERIFIED`.

**A direction where no `B`-square fits is accepted, and accepted on vacuity.** The set
of admissible centres at a direction is `[h, L − h]²`, where `2h` is the width of the
`B`-square’s bounding box there.
Where `2h > L` that set is empty, and Condition 5 quantifies over nothing, so it holds.
The earlier verifier raised instead, and the change of policy is deliberate: the
acceptance is sound.
Condition 5 is a *hypothesis*, and the proof applies it only to a `B`-square it has
already placed strictly inside a unit square inside the container; if no `B`-square at
that direction fits in the container, then no unit square containing one fits either,
and the proof never reaches that direction.
A stronger hypothesis can only make a theorem harder to apply, and an empty one cannot
make it unsound. What the change costs is worth stating in the same breath.
This checker’s value is that it refuses what it cannot handle, and a direction accepted
on vacuity is a direction where it decided nothing.
So it says so: the run prints how many directions admitted no placement, and a
certificate whose every direction is vacuous is reported as having decided nothing
rather than as having passed.
Neither shipped artifact has a vacuous direction.
Where `2h = L` there is exactly one admissible centre; the open-cell argument has no
open cell to reason about there, so that one closed placement is evaluated directly.

The verifier reports the exact least covered weight, the direction and the centre of a
square that attains it, and the number of cells decided.
The count is worth reading: a verifier that quietly decides fewer placements makes every
certificate easier to accept.
The falsification row below that enlarges the container to side 4 is what shows this one
scores the cells beyond the atoms’ reach — its least covered weight is `0`, found in a
corner no atom can reach.
That is not the control; the control is Massaccesi’s `n = 17` certificate, whose least
covered weight is exactly `1`.

## The Control: Massaccesi’s Published n = 17 Certificate

A verifier that has only ever confirmed its own project’s results has confirmed nothing.
`control-n17-massaccesi.json` is the certificate Gustavo Massaccesi published in August
2026 for `s(17) ≥ 4.5058`, rebuilt as plain data by `build_n17_control.py` from the
constants of his published verifier: `L = 45058/10000`, empty border `M = 15513/10000`,
`B = 9973/10000`, `T = 207107/500000`, `K = 180`, weight scale `576`, a `29 × 29` grid
with `coord[i] = M/2 + i(L − M)/28`, and 23 orbit representatives `(i, j, w)` each
giving weight `w/576` to every distinct image of grid point `(i, j)` under the
container’s symmetries.
None of his verification logic is reused.
The rebuild reproduces the three checksums his source states: 168 atoms, total weight
`9744/576 = 203/12`, and `L = 22529/5000 = 4.5058`.

The same `verify.py`, unchanged, accepts it and reports the bound `22529/5000`, the
published value, with least covered weight exactly `1` (the published certificate is
tight) and `B(1 + D) = 899635478111/900000000000`. The value matters: an earlier reading
of the theorem in this project divided by `B` and would have reported `4.51799`,
overstating a published result; the control is what catches that kind of error.

## Falsification

`falsify.py` perturbs the certificate and runs the full decision on each variant.
The perturbed atom is chosen from the verifier’s own witness: the first atom covered by
the least-covered placement, so a change to it must show in Condition 5.

Each row is also an assertion.
Every perturbation carries the result it must produce — the verdict, the five condition
outcomes and the exact least covered weight — and the script exits non-zero if a run
disagrees, so the table is checked rather than merely printed.
Those expected numbers are this file’s and no other’s, which is why `falsify.py`
declines a path that is not this directory’s `certificate.json` instead of measuring a
different certificate against them.
`python3 falsify.py --quick` runs the one mutation whose expectation does not depend on
which certificate it is applied to — atom 0 given weight `-1` — which the preconditions
refuse before any Condition 5 sweep, in well under a second.

Real output of `python3 falsify.py` (about four minutes):

```
baseline: deciding the unperturbed certificate to locate its tight placement
least covered weight 50003/50000 at direction 0, centre (53/100, 53/100)
perturbed site: atom 0 at (1/2, 29/30), weight 407/25000
```

| Perturbation | Condition 1 | Condition 2 total | Condition 3 slack | Condition 4 B(1+D) | Condition 5 least covered weight | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| weight of that atom lowered by 1/10000 | FAIL (425 atoms) | PASS (216953/20000) | PASS (309449/250000000000) | PASS (0.999995896) | FAIL (24999/25000 = 0.999960) | REFUSED |
| weights of its whole orbit (8 atoms) lowered by 1/10000 | PASS (425 atoms) | PASS (216939/20000) | PASS (309449/250000000000) | PASS (0.999995896) | FAIL (49993/50000 = 0.999860) | REFUSED |
| that atom dropped | FAIL (424 atoms) | PASS (1083147/100000) | PASS (309449/250000000000) | PASS (0.999995896) | FAIL (49189/50000 = 0.983780) | REFUSED |
| its whole orbit dropped | PASS (417 atoms) | PASS (1071751/100000) | PASS (309449/250000000000) | PASS (0.999995896) | FAIL (387/400 = 0.967500) | REFUSED |
| that atom shifted by +1/1000 in x | FAIL (425 atoms) | PASS (43391/4000) | PASS (309449/250000000000) | PASS (0.999995896) | PASS (50003/50000 = 1.000060) | REFUSED |
| container side 4 instead of 19/5, atoms unchanged | FAIL (425 atoms) | PASS (43391/4000) | PASS (309449/250000000000) | PASS (0.999995896) | FAIL (0 = 0.000000) | REFUSED |
| container side 4, atoms translated by +1/10 to keep the symmetry | PASS (425 atoms) | PASS (43391/4000) | PASS (309449/250000000000) | PASS (0.999995896) | FAIL (0 = 0.000000) | REFUSED |
| weights scaled so the total is exactly n | PASS (425 atoms) | FAIL (11) | PASS (309449/250000000000) | PASS (0.999995896) | PASS (1100066/1084775 = 1.014096) | REFUSED |
| angle limit 41/100, short of tan(pi/8) | PASS (425 atoms) | PASS (43391/4000) | FAIL (-119/10000) | PASS (0.999972539) | FAIL (195849/200000 = 0.979245) | REFUSED |
| B raised to 1/(1 + D), so B(1 + D) = 1 | PASS (425 atoms) | PASS (43391/4000) | PASS (309449/250000000000) | FAIL (1.000000000) | PASS (50003/50000 = 1.000060) | REFUSED |

The run ends with `falsify.py: every mutation run matched its refusal oracle`, which is
the line that makes the table above a check and not a report.

Read the rows as demonstrations of the verifier, not of the certificate.
Every condition is seen refusing something.
Condition 5 moves by exactly what was taken from the tight placement: one atom lowered
by `1/10000` lowers the least covered weight from `50003/50000` to `24999/25000`, a drop
of `1/10000`; lowering its whole orbit lowers it by `2/10000`, because the corner
placement covers two members of the orbit, the atom and its mirror image across the
diagonal; dropping the atom removes its `407/25000`. The shifted atom leaves Condition 5
at its old value and is caught by the symmetry condition alone, which is why Condition 1
is a condition and not a label.
The container of side 4 with the atoms recentred is refused by Condition 5 alone, with
every other condition passing and a least covered weight of `0`: a square in the widened
margin covers nothing, and the verifier scores those placements.

## Output of the Stranger Run

Run from a copy of this directory outside the repository, with an empty environment
(`env -i PATH=/usr/bin:/bin bash -c 'time python3 check.py'`, so `python3` is the system
interpreter and nothing from this project is importable).
Verbatim:

```
$ which python3; python3 --version
/usr/bin/python3
Python 3.11.15
$ time python3 check.py
control data rebuilt from the published constants: identical to control-n17-massaccesi.json
python 3.11.15
certificate C-n011-fractional-19-5
  n = 11, L = 19/5 = 3.800000, B = 9977/10000, net t_k = 207107/500000 * k / 180 for k = 0..180, 425 atoms
  PASS  P1 n >= 1, L > 0, B > 0 | n = 11, L = 19/5, B = 9977/10000
  PASS  P2 every weight is non-negative | 425 atoms, 0 negative
  PASS  P3 net starts at 0 and is strictly increasing | t_0 = 0, K = 180, t_K = 207107/500000
  PASS  P4 every atom is an (x, y, weight) triple | 425 atoms
  PASS  P5 the declared claim is the theorem's conclusion | declared 's(11) >= 19/5', theorem gives 's(11) >= 19/5'
  PASS  Condition 1 atoms invariant under the container's symmetries | 425 atoms on 425 distinct sites, all eight maps preserve the weights
  PASS  Condition 2 total weight below n | total 43391/4000 = 10.847750 against n = 11
  PASS  Condition 3 net reaches pi/4 | t_K = 207107/500000, t_K^2 + 2 t_K - 1 = 309449/250000000000
  PASS  Condition 4 containment B(1 + D) < 1 | D = 207107/90000000, B(1 + D) = 899996306539/900000000000 = 0.999995896154
  Condition 5: sweeping every net direction
    direction   0/180  t = 0                  cells   34969  least weight 50003/50000 = 1.000060  running least 50003/50000
    direction  30/180  t = 207107/3000000     cells  503177  least weight 50003/50000 = 1.000060  running least 50003/50000
    direction  60/180  t = 207107/1500000     cells  512197  least weight 50003/50000 = 1.000060  running least 50003/50000
    direction  90/180  t = 207107/1000000     cells  512765  least weight 50003/50000 = 1.000060  running least 50003/50000
    direction 120/180  t = 207107/750000      cells  505529  least weight 50003/50000 = 1.000060  running least 50003/50000
    direction 150/180  t = 207107/600000      cells  501069  least weight 50003/50000 = 1.000060  running least 50003/50000
    direction 180/180  t = 207107/500000      cells  499545  least weight 50003/50000 = 1.000060  running least 50003/50000
  PASS  Condition 5 every admissible placement covers weight >= 1 | least covered weight 50003/50000 = 1.000060 at direction 0 (t = 0), centre (53/100, 53/100) ~ (0.530000, 0.530000); 90546593 cells over 181 directions in 38.7 s
  info  declared total_mass 43391/4000 == recomputed 43391/4000
  info  declared least_cell_mass 50003/50000 == recomputed 50003/50000
  info  all atoms lie in [0, L]^2: yes (not a condition; an outside atom only wastes weight)
VERIFIED: s(11) >= 19/5 = 3.800000
python 3.11.15
certificate control-n17-massaccesi-4.5058
  n = 17, L = 22529/5000 = 4.505800, B = 9973/10000, net t_k = 207107/500000 * k / 180 for k = 0..180, 168 atoms
  PASS  P1 n >= 1, L > 0, B > 0 | n = 17, L = 22529/5000, B = 9973/10000
  PASS  P2 every weight is non-negative | 168 atoms, 0 negative
  PASS  P3 net starts at 0 and is strictly increasing | t_0 = 0, K = 180, t_K = 207107/500000
  PASS  P4 every atom is an (x, y, weight) triple | 168 atoms
  PASS  P5 the declared claim is the theorem's conclusion | declared 's(17) >= 22529/5000', theorem gives 's(17) >= 22529/5000'
  PASS  Condition 1 atoms invariant under the container's symmetries | 168 atoms on 168 distinct sites, all eight maps preserve the weights
  PASS  Condition 2 total weight below n | total 203/12 = 16.916667 against n = 17
  PASS  Condition 3 net reaches pi/4 | t_K = 207107/500000, t_K^2 + 2 t_K - 1 = 309449/250000000000
  PASS  Condition 4 containment B(1 + D) < 1 | D = 207107/90000000, B(1 + D) = 899635478111/900000000000 = 0.999594975679
  Condition 5: sweeping every net direction
    direction   0/180  t = 0                  cells    2025  least weight 1 = 1.000000  running least 1
    direction  30/180  t = 207107/3000000     cells   92781  least weight 1 = 1.000000  running least 1
    direction  60/180  t = 207107/1500000     cells   94145  least weight 1 = 1.000000  running least 1
    direction  90/180  t = 207107/1000000     cells   92873  least weight 1 = 1.000000  running least 1
    direction 120/180  t = 207107/750000      cells   91589  least weight 1 = 1.000000  running least 1
    direction 150/180  t = 207107/600000      cells   90869  least weight 1 = 1.000000  running least 1
    direction 180/180  t = 207107/500000      cells   90221  least weight 1 = 1.000000  running least 1
  PASS  Condition 5 every admissible placement covers weight >= 1 | least covered weight 1 = 1.000000 at direction 0 (t = 0), centre (364907/560000, 364907/560000) ~ (0.651620, 0.651620); 16562293 cells over 181 directions in 13.5 s
  info  declared total_mass 203/12 == recomputed 203/12
  info  all atoms lie in [0, L]^2: yes (not a condition; an outside atom only wastes weight)
VERIFIED: s(17) >= 22529/5000 = 4.505800
check.py: all three steps passed

real	0m52.422s
user	0m34.333s
sys	0m1.510s
exit status 0
```

## Provenance, and What Is Not Claimed

- **The method is not this project’s.** The theorem and the certificate architecture are
  Burns’s and Massaccesi’s (August 2026, blog posts, not peer reviewed).
  Their work aimed at `n = 17`. What is new here is the `n = 11` instance: the 425 atoms
  and their weights, found on 2026-09-04 by a linear program with column generation on a
  symmetric site grid, rationalised to exact weights.
  How the certificate was found has no bearing on whether it is valid; the search code
  is deliberately not part of this package.
- **The novelty claim rests on a bounded search.** The project’s record marks the result
  *apparently novel* relative to the corpus it holds: Friedman’s survey, the Kingbird
  catalogue of records, Stromquist 2003, Bentz 2010 and 2016, Nagamochi 2005, and the
  two 2026 posts. No systematic arXiv or preprint sweep and no MathOverflow search is on
  record. “First movement since 2003” is a statement about that corpus.
- **Who checked it.** The project’s own verifier accepted the certificate; a reviewer
  inside the project wrote a second verifier from the theorem statement with the
  implementation withheld, reproduced the `n = 17` value as a control, and accepted the
  `n = 12` certificates from the same generator; this package is a third implementation,
  written from the theorem for a reader outside the project, with the same control.
  A fourth decision has since been made by a different method rather than a different
  implementation — see the first objection below.
  No one outside the project has reviewed the result yet.
- **A calibration rung exists.** Before this certificate, the same generator was run at
  side `189/50 = 3.78`, below Stromquist’s bound, where a certificate proves nothing
  new; it was found and verified, and is retained as `../certificate-189-50.json`. The
  comparison `(189/50 − 2)² · 5 = 7921/500 < 16` confirms it sits below.
- **What is claimed is exactly `s(11) ≥ 19/5`.** Not a value of `s(11)`, not optimality
  of Trump’s packing, not a bound for any other `n` (every `n > 11` already carries a
  larger bound in the literature or in the project’s record).

## What a Sceptic Could Still Object To

- **Same method family, three times — but no longer only that.** This verifier and the
  project’s two exact ones are independent implementations of the same reduction: an
  exact event-cell sweep over a rational direction net.
  Three agreeing implementations of one reduction test the code and not the reduction,
  which is why this objection was worth stating.
  It has since been answered, though not by anything in this directory.
  The repository now also decides Condition 5 by interval arithmetic with directed
  rounding — branch and bound over boxes of centres, where an atom counts for a box only
  if its coverage rectangle contains the whole box, so the count is a lower bound by
  construction. There is no event grid, no difference array and no polygon clipping: the
  two routes share the certificate and the closed-form conditions, and share no part of
  how Condition 5 is decided.
  It decides Condition 5 on the doubled net (`θ_k` and `π/2 − θ_k`, 361 directions),
  which means it never invokes the reflection argument of step 1 and does not need
  Condition 1 at all. Run on *this file’s bytes* — SHA-256
  `60ac0c33e2e5a55874a10b0d09c6aaf3f891db921b063cc860114c2d4588c055`, the hash in the
  table above — it certifies all 361 directions in 1,195,755 boxes with none stalled, in
  about ten seconds, and its enclosure of the least covered weight has width zero at
  `50003/50000`: the value printed in the run above, to the digit, from arithmetic that
  rounds outward at every step.
  It returns Massaccesi’s `22529/5000` on the same control.
  Two things a reader should hold onto.
  That check is not shipped here: this package is standard-library-only and
  self-contained, so a stranger running `check.py` still gets one method, and the
  interval route has to be taken on this project’s word or read in the repository at
  `packing/src/sqpack/fractional/interval.py`. And neither route protects against a
  wrong statement of the theorem, which both share; a proof-assistant formalisation of
  the theorem and of one of the two reductions is still the check nobody has done.
- **The reduction is proved on paper.** The argument that finitely many open cells
  decide the continuum lives in the Condition 5 comment block of `verify.py` and in the
  section above. It is elementary, but it is the place where a wrong verifier would be
  wrong; the falsification row that enlarges the container shows cells beyond the atoms’
  reach are scored, and the cell counts are printed, but neither is a proof.
- **Trust in the interpreter.** The decision rests on CPython’s arbitrary-precision
  integers and the `fractions` module.
  They are widely used and not formally verified.
- **Authorship.** The package was written by the project that claims the result, on the
  day the result was found.
  The published `n = 17` value is its only anchor outside the project.
- **The theorem itself.** Steps 1 to 6 above are short and can be checked by hand; the
  support-function inequality in step 3 and the invariance argument in step 5 are the
  two places to read slowly.
  No formal proof exists.
- **Tightness.** The Condition 5 margin is `6/100000`. Exact arithmetic makes the size
  of the margin irrelevant to validity, but a reader should know the certificate is
  delicate: any rounding, in either direction, would change the verdict.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
