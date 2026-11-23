# Focused Review: One-Axis Path Application and D4 Covariance

The source’s path enumeration, clause polarity and symmetry conventions are
mathematically consistent in this focused read.
No counterexample to the maintained local-path result was found.
This note closes the algebraic covariance derivation and identifies a bounded finite
audit; it does not claim that the new checker has run or that global graph coverage is
complete.

The shared P checkout was read at head `689a8ecf3546ea7f4b7003454f1cf7dcb8783044`. Its
maintained general-path gzip has SHA-256
`32182f37724fe649925fdbf1710d69f42fe64ac42ab892f7ea571f10e581d17c`, matching the
accepted portable input copied here.
No shared file, branch, task or GitHub object was changed.

## Evidence Read and Prior Exposure

This is not a blind review.
The reviewer previously read the contributor’s proofs and programs and prepared the
independent bank, bridge, census and general-path slices.
This pass reads the maintained local-path README and retention record, the frozen
first-party general-path checker, and these source archive members as text:

- `geometry/one_axis_equal.py`: sign decoding, D4 canonicalization and graph-to-rule
  convention.
- `geometry/one_axis_duals.py`: exact-path orchestration and its count assertions.
- `geometry/one_axis_paths.py`: exclusion-to-clause translation.
- `geometry/equal_path_polynomial.py`: full occupied-path generation.
- `geometry/signed_angle_graphs.py`: edge ordering and positive-literal interpretation.
- The already reviewed one-axis theorem and near-grid geometric argument.

The source archive remains the stronger attachment linked from
[issue #1055](https://github.com/jlevy/squares/issues/1055#issuecomment-7058955337),
SHA-256 `475d7ef50e21ce4a83cfb4c8415c9e9852d619beeade5c4c8745c2c963d6c867`. No
contributor module was imported or executed.
The mathematical domain remains nineteen independently signed tilts of common magnitude
theta and one aligned tile, `0 < tan(theta/2) <= 1/24`, and strict board side `S < 5`.
The fully aligned endpoint is a separate elementary case.

## Path Completeness and Edge Binding

For a vacancy permutation p, the occupied cells are exactly
`{(x,y): x,y in {0,...,4}, y != p[x]}`. A horizontal full forward path has one cell in
each column; a vertical one has one in each row.
Choosing one cell from every layer exhausts these paths.
Filtering adjacent transverse differences to absolute value at most one is precisely the
local catalogue’s rank-step domain.
There is no other hidden path restriction in that construction.

Equivalently, each of the 259 universal five-rank walks determines at most one
horizontal path and one vertical path in a given occupancy pattern.
The horizontal coordinates are `(k,r[k])`; the vertical coordinates are `(4-r[k],k)`.
Keeping the walk exactly when all five cells are occupied gives the same path set.
This establishes a second, independently testable generation method.

Both producer modules order occupied cells lexicographically and list a diagonal edge
when its second endpoint has x coordinate one greater and y difference of magnitude one.
Consequently their edge masks have the same meaning by inspection, rather than merely
the same number of edges.
Along a forward path a diagonal edge cannot repeat: each advances to the next forward
rank. The producer’s addition of edge bits therefore equals bitwise union.
A zero-jump occupied full path cannot occur, since every row and column has only four
occupied cells; empty-clause handling remains a useful synthetic control.

These statements concern all occupied paths, not only a representative sample or the
one-jump bridges. What remains unexecuted is the finite roster comparison and the
application receipt binding each census case’s signs to its concrete paths.

## Clause Polarity

The producer’s graph bit one means horizontal separation.
Its clause pair `(positive,negative)` is satisfied when a chosen horizontal bit
intersects `positive`, or a chosen vertical bit intersects `negative`.

For an excluded horizontal path, all diagonal bits one would realize the four forward
separations; straight steps already have their forward separation by the near-grid
argument.
That conjunction is impossible, so the clause is the disjunction of the negated
diagonal bits. The source emits `(0,mask)` for horizontal paths.

For an excluded vertical path, all diagonal bits zero would realize the forward chain.
Its clause is the disjunction of the positive diagonal bits.
The source emits `(mask,0)` for vertical paths.
These agree with the graph-to-rule choice in `one_axis_equal.rows`.

A not-certified profile supplies no exclusion clause.
In particular, it must not be interpreted as a feasible path, and must not be excluded
by default. Duplicate clauses are harmless.
The source’s subsumption rule drops a clause only when a retained clause’s positive and
negative literal sets are both subsets; that implication is valid.
The next small audit does not need to reproduce subsumption.

## Universal Covariance of the Local Bound

Write the local transverse ranks as r, signs as a, and the four inclined coefficients as
lambda. For one normal choice the bound uses

`J = sum(lambda[i]*(r[i+1]-r[i]))`

and the maximum K of

`sum(lambda[i]*(eta[i+1]-eta[i]))`

over the box `eta[j] in [-r[j],4-r[j]]`.

Under reflection of the forward direction, reorder the chain and set

`r' = reverse(r), a' = -reverse(a), lambda' = -reverse(lambda)`.

The transverse step sequence becomes the negated reverse.
Pair categories and their complete sets of normal choices correspond bijectively.
For a mixed favorable diagonal, both factors in `(r[i+1]-r[i])*(a[i]+a[i+1]) > 0` change
sign, preserving the condition.
The two-option straight cases remain two-option cases.

J is unchanged. The map `eta' = reverse(eta)` is a bijection of the corresponding error
boxes and leaves the displayed linear form unchanged, so K is unchanged.
The two endpoint widths are exchanged; their sum is unchanged.

Under transverse reflection, set

`r' = 4-r, a' = -a, lambda' = -lambda, eta' = -eta`.

The error-box map is again bijective.
J and K, pair categories, step constants and endpoint widths are unchanged.
Thus the entire cleared polynomial is identical for each corresponding normal choice.
This proves invariance of the complete polynomial multiset, and hence of the Bernstein
exclusion predicate, under both generating reflections.
It is stronger than checking only the total number of exclusions.

For a board D4 transformation, let alpha be its sign on the forward direction and beta
its sign on the normalized transverse direction.
The tilt sign changes by the determinant `alpha*beta`. Reverse the path exactly when
alpha is negative and complement the transverse ranks exactly when beta is negative.
This is precisely the composition of the two local transformations above.

A quarter-turn preserves tilt sign but swaps horizontal and vertical graph choices.
A reflection negates tilt sign; it complements graph bits only if it also swaps the
coordinate axes. For the planned representation “quarter-turns followed by reflection in
x,” graph-bit complement occurs exactly for an odd number of quarter-turns.

The missing graph-edge/path covariance evidence is therefore finite representation
checking, not a new analytic inequality.

## A Concrete Wrong-Convention Detector

The accepted local check explicitly records the all-positive increasing walk
`r=(0,1,2,3,4)` as not certified and the all-negative increasing walk as excluded.
Forward reflection of the latter gives the all-positive decreasing walk, which must also
be excluded by the polynomial identity above.

Therefore replacing the vertical transverse ranks `4-x` with x while leaving tilt signs
unchanged changes a known verdict.
Likewise, reversing a path without the required reflection sign change can change its
classification. This is a counterexample to those erroneous conventions, not to the
source, which uses the correct vertical frame.
The prepared controls test this distinction against the retained receipt; they have not
run.

## Smallest Frozen Finite Audit

The checker in this directory reads only the accepted general-path receipt.
It does not parse the sign census, enumerate separation graphs or test polynomial
positivity again.

It checks:

- The full 29,008-profile domain, bound references, exclusion flags and failed-choice
  binding from the accepted receipt.
- Exactly 58,016 generator images, including equality of each normal-choice polynomial
  multiset and both exclusion statuses.
- Two independent diagonal-edge and occupied-path constructions for all 120 vacancy
  permutations.
- All 960 D4 geometry maps, with complete cell, edge and path permutations.
- Clause covariance after the appropriate edge permutation and graph-bit complement.
- Thirteen predeclared controls, including wrong polarity, missing literals, incorrect
  reflection signs, the wrong vertical frame, an omitted quarter-turn bit complement,
  missing or duplicate catalogue rows and an invalid bound reference.

The output retains the complete geometry and D4 permutation rosters.
Exact path totals are not prescribed; the conservative upper bounds are 62,160 paths and
497,280 D4 path images.
Matching a producer graph count is irrelevant to this audit.

The checker has not been run, imported, compiled or syntax-checked.
Its input is a 444,111-byte gzip whose expanded 14,993,939 bytes must match SHA-256
`a60f45a70cb57d4e1a1e58bcbe01b1f9cf1c527fc80c0e931d7e856af22b33bb`.

Proposed execution is one isolated project Python worker under the coordinator’s serial
memory-guard slot: target under 30 seconds and 0.15 GiB peak RSS; hard limits 60
seconds, 0.25 GiB owned process-tree cost and stop at host pressure 2. The internal
ceiling is 55 seconds, expanded input is capped at 32 MiB, and the streamed atomic
output is capped at 16 MiB. These limits are below the assignment’s 0.5 GiB owned-tree
maximum.

```bash
"$PYTHON" -I -B check_path_covariance.py \
  --input general-path-catalogue.json.gz \
  --output "$OUT/path-covariance.json"
```

Use a fresh external output path.
Verify the freeze before running; do not execute until the coordinator gives the guarded
slot. No completed verdict may be inferred from a partially written output, a cap, or a
nonzero worker/guard result.

## Remaining Mathematical Gaps

After this finite audit passes, the cheapest next slice is a complete sign-case
application roster: all 3,671 canonical census cases, every actual occupied path’s local
profile identifier, and the resulting clauses with their origins.
This is at most 1,901,578 lookups and does not require Boolean search.
Its exact roster and D4 binding must be retained.

Next come complete Boolean graph enumeration and the independent graph-to-bank
application: derive each surviving graph’s valid wall, rank and pair rules and show that
an accepted polynomial certificate uses only those rules.
Those are still required even if all current covariance checks pass.

One source detail reinforces the need for explicit graph evidence: `one_axis_duals.py`
asserts the 273,584 graph total only when `--exact-paths` is absent.
A successful producer exact-path exit therefore cannot, by itself, establish that
particular count. The new pipeline must record its independently obtained total and
investigate any difference.

Neither the one-axis theorem nor an unrestricted or angle-diversity result is promoted
by this review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
