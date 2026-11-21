# Bounded mathematical review of the equal-absolute-tilt claim

The local reduction and certificate arithmetic checked here are consistent.
The restricted minimum-5 theorem remains pending because exhaustive graph coverage, the
common-orientation theorem, and the large-angle exclusion were not replayed or fully
reviewed. The two unrestricted lower bounds also remain pending.

The source is `geometry/equal_magnitude.md` in the
[pinned archive](acquisition/manifest.json).
All source members have digest entries in
[the inventory](acquisition/archive-members.json.gz).
The earlier 4.95 mark-ownership review was read before this review, as were the author’s
proof and implementation.
The first-party checker reconstructs the inequalities but is informed by that source;
its agreement is corroboration, not blind independence.

## What the small-angle argument needs

Write `t = tan(theta/2)`, `c = cos(theta)`, `s = sin(theta)`, `u = c+s` and
`d = u(u-1)`. For `0 < t <= 1/24`, `theta < 1/12`. A unit square’s transverse chord has
length at least one within radius `r = (1-d)/2` of its center.
This follows by solving the chord formula `min(1/c, (u/2 - abs(v))/(cs)) >= 1`; for zero
tilt the radius is 1/2. Thus five centers in a coordinate span at most `1-d` would
produce five interior-disjoint unit chords on one line, impossible when the board side
is strictly below 5.

Sorting the centers gives rank-group bounds `j+1/2-jd <= coordinate <= j+1/2+(4-j)d`,
for `j = 0,...,4`, four centers per group.
The first-party checker uses `e=1/12`, `d<=e(1+e)=13/144`, and checks `32d²<1`. Two
centers in one pair of rank groups would then have Euclidean distance less than one,
contradicting their disjoint inscribed radius-1/2 disks.
The twenty occupied cells have exactly one vacancy in every row and column.

For a step between adjacent horizontal ranks, `1-5d <= dx <= 1+3d`. An axial step has
`abs(dy)<=4d`; a diagonal step has `abs(dy)<=1+3d`. The exact rational checks
`(1+3d)e+4d<1` and `(1-5d)(1-e²/2)-(1+3d)e>0` respectively exclude a transverse
separating normal on an axial step and make a selected forward normal point forward.
The two incident edge-normal directions exhaust the separating-axis alternatives for
squares. Boundary contact is allowed, so all necessary separation inequalities are weak.

For equal signs the projected separation is `c dx + lambda s dy >= 1`. For opposite
signs it is `c dx + lambda s dy >= c(c+s)`: the projected half-width sum is
`(1+cos(2theta)+sin(2theta))/2 = c(c+s)`. On a diagonal, `dy` has the rank-step sign, so
maximizing the two projections chooses that sign.
On an opposite-sign axial edge, eliminating `dy` with `abs(dy)<=4d` gives the weaker
necessary inequality `c dx >= cu-4sd`.

Adding the two wall clearances and the four chain inequalities yields
`S >= u + A/c + B*u - tan(theta)*(H+d*K)`, with `A+B=4` and `H,K` computed from rank
differences and the endpoint coefficients of the transverse coordinates.
[The retained checker](programs/check_small_angle.py) reconstructs this polynomial bound
for all 992 incorrectly signed one-diagonal chains.
It separately enumerates the bridge geometry for all 120 vacancy permutations.
The histograms agree with the source.
This does not enumerate the global sign assignments.

## Certificate arithmetic

The retained coefficient bank has 117 records, SHA-256
`009441b65a3364e5f2abc5736a07dc46632dfba32b03d880780fb7c6849e238f` for its original gzip
member. Set `C=1-t²`, `D=1+t²`, `U=1+2t-t²` and change center variables to `X=2D²x`. The
checker reconstructs the wall, rank, same-sign, mixed-diagonal and mixed-axial rows in
these variables. It checks that each supplied polynomial multiplier is nonnegative and
that the weighted center coefficients cancel exactly.
The negated scalar right side must equal the supplied margin and be strictly positive
for `0<t<=1/24`.

Positivity uses rational Bernstein coefficients on `[0,1/24]`. Nonnegative coefficients
prove nonnegativity; a positive last coefficient makes the polynomial strictly positive
at every positive point, including the upper endpoint.
All arithmetic uses Python integers and exact fractions.
All 117 records pass.
Altering a margin constant or replacing a multiplier by -1 is rejected.

This verifies each conditional contradiction.
It does not establish that the conditions of some certificate occur in every admissible
global graph. The source reports 3,636 sign assignments after paired-chain filters, 240
uniform assignments, 256 mixed symmetry representatives, 26,611 separation graphs, and
zero uncovered graphs.
Those counts have not been independently reproduced here.
Nor have the separate 120 sign-cover and 430 graph-cover Boolean UNSAT results.

## Whole-theorem and unrestricted dependencies

For `t>=1/24`, positive orientations have normalized half-angle at least `1/24`.
Negative orientations can be represented by `pi/2-theta`, whose half-angle is
`(1-t)/(1+t)<=23/25`. Thus the claimed large-angle exclusion on `[1/24,23/25]` would
apply. That exclusion depends on the side-five unrestricted screen’s 1,142 labelled
assignments, rebuilt geometric profiles and nine remaining angular ownership
alternatives. It is not part of the small polynomial bank.

Uniform signs are delegated to the common-orientation proof: 41 near-zero certificates,
7,360 middle-angle subset exclusions across 31 intervals and 27 weighted covers.
Its verifier is standard-library Python, but neither its coverage nor its geometric
certificates were checked here.
At zero angle a strict sub-5 center box can be partitioned into sixteen cells of
diameter less than one in the infinity norm; hence at most sixteen aligned tiles fit.
A 4-by-5 aligned array provides the upper bound 5.

For 4.95 the earlier review established the 22-mark cover and the reduction from 231
vacancy pairs to 67 reflection classes.
The next proof gate is still the complete tree and all 75 native terminal exclusions,
including orientation-interval coverage and contact/tie conventions.
Those use the pinned Mira-Cult geometry kernel also implicated in #1050; custody checks
do not verify that kernel.

For 4.99755 the new reduction uses two marked patterns and a side-five screen over
53,361 ordered mask pairs / 6,787 symmetry classes.
The recipe records 1,068 ownership exclusions, 47 root-frame exclusions, and 27 refined
matchings with 89 geometric terminals.
It carries 1,141 exclusions forward from larger boards and replaces one root at the
target side. The transfer argument preserves nearest-mark ties by scaling centers and
marks; it needs independent review together with the reopening of all four
unselected-mark ownership choices.
A saved-output ledger cross-check does not regenerate any native exclusion or prove the
original screen complete.
The author’s one-root rerun also does not replay the other 1,141 entries.

## Next bounded review gates

1. Review and independently enumerate the small-angle sign and graph encodings,
   including reflection parity, vertical chains, endpoint conventions and assignment of
   each certificate’s rules.
   Delete a required bridge clause or certificate and confirm that the appropriate
   coverage check fails.
   The standalone lane needs only Python’s standard library; the second formulation
   needs a system Z3 shared library through `advanced/z3_lra.py`.
2. Audit the common-orientation proof separately.
   Review all interval endpoints, half-open weighted windows and outward polygon
   rounding before accepting saved counts or selecting a replay budget.
3. Review the shared geometry kernel and side-five label-screen reduction before using
   the large-angle theorem or 4.99755 recipe.
   The native path needs a C++17 compiler and rebuilds pinned upstream programs; it is a
   separate authorized execution task.
4. Keep 4.95 and 4.99755 as separate cases.
   For either, preserve a feasible grid control and test a removed root/branch, an
   angular gap, an altered endpoint and weak-versus-strict contact semantics.
   The stronger endpoint must prove every inherited exclusion reaches the target, not
   only the changed matching.

Concrete source entry points and prerequisite files are listed in
[dependencies.json](dependencies.json).
They are proposed future commands, not executed checks.
No theorem defect was found in the bounded inequalities examined; no conclusion is
offered on the unreviewed exhaustive stages.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
