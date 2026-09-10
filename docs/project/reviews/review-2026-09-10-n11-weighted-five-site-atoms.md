# Readiness of the Weighted Five-Site Atom Direction

**September 10, 2026. Status: two concrete candidates with an exact resource proof; the
scientific comparison is not ready to run.** The resource argument is valid, and an
abstract five-site comparison shows a strict advantage over ordinary threshold atoms
supported on those same sites.
Whether that advantage survives the retained square geometry and the larger covering
program remains open.
Admission should first add a binary threshold on integer site multiplicities, then
validate the exact matrices for a new finite comparison.
A general floor-atom implementation is unnecessary for these candidates: their total
multiplicity is seven and their threshold is four, so floor charge and binary charge
coincide on every possible core.

This audit inspected source and retained records.
It ran no placement search, LP, weighted-atom replay, or coverage target.
The source charges below remain reported historical readings until the proposed
independent replay succeeds.

## Retained Objects and Their Admission Level

The two candidate objects are at JSON pointer `/k5_cliques/atom` in the retained readers
below. Artifact filenames in this section resolve under
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/`.

| Reader File | Site Multiplicities, in Stored Order | Reported Family | Reported Charge |
| --- | --- | --- | --- |
| [lane-a6-reader-saturated-symmetric.json](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a6-reader-saturated-symmetric.json) | `(1,2,2,1,1)` | 64 placements, total weight 11; 10 charged placements | `3/2` |
| [lane-a6-loop-reader-2.json](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a6-loop-reader-2.json) | `(2,2,1,1,1)` | 56 placements, total weight 11; 8 charged placements | `3/2` |

Both store threshold `4`, size `7`, budget `1`, and equal threshold and floor charges.
The corresponding retained families are
[the symmetric family](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a6-saturated-symmetric-153-40.json)
and
[loop family 2](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a6-loop-family-2.json).
Their historical reader `source` fields name scratch paths.
A new replay must bind the current retained family and candidate bytes directly; the
scratch path is historical metadata, not a live input or a source identity.

The independent six-cut admissions concern ordinary atoms.
They do not admit these two weighted objects.
The source storage label `k5_cliques` identifies the discovery route.
The clique search and its fractional piercing program explain how the objects were
discovered, but neither is needed to prove their resource inequality once the exact
sites and multiplicities are fixed.

The completed A6 comparison added six ordinary distinct-site atom orbits.
Their zero reported weight in that larger covering LP does not evaluate the two weighted
candidates here. Repeating those same six additions on the same program would repeat a
completed comparison; admitting the weighted rule changes the proposed atom family.

The retained
[floor-atom scaffold](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a4-flooratoms.py.txt)
has explicit multiplicities, weighted D4 keys, serialization, and LP columns.
The retained
[A6 program](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a6-lp-struct.py.txt)
imports that shape as a third column block.
These are archived scratch sources, not maintained admission tools.
The former coerces integers with `int(...)`, uses float membership with `COVER_SLACK`,
and does not check every serialized declaration.
Port its representation ideas; do not inherit its results as exact production admission.

## Resource Proof and Its Geometric Hypothesis

A **site** is a point in the container.
A **core** is a closed square of the declared smaller side, placed at a direction from
the finite angle net.
A weighted site carries positive integer multiplicity `a_s`, interpreted as that many
labelled tokens occupying the same point.
A **binary threshold atom** charges a core once its contained token count reaches
threshold `t`. Put

```text
A = sum_s a_s
h(P) = sum_{s in P} a_s
f(P) = 1 if h(P) >= t, otherwise 0.
```

For pairwise disjoint closed cores `P_i`, each token belongs to at most one core.
If `m` cores are charged, then

```text
t m <= sum_i h(P_i) <= A,
```

so `m <= floor(A/t)`. With nonnegative atom weight `w`, the certified upper bound on
total charge is `w floor(A/t)`. This is a safe resource budget; it need not be the
sharpest budget attainable for a particular geometry.

For both candidates, `A=7` and `t=4`, so the budget is `w`. Also `0 <= h(P) <= 7`, and
therefore `floor(h(P)/4) = [h(P)>=4]` for every core.
That equality licenses using the archived floor-column formula for these candidates
after exact admission.
It does not identify floor and binary atoms when `A>=2t`.

The closed-disjointness condition matters.
Interior-disjoint unit squares may share a boundary site and hence share every token at
it. The existing
[physical transfer](../../../packing/src/sqpack/fractional/certificate.py) places each
closed net core strictly inside its unit square under the strict containment condition.
Those cores are disjoint as closed sets, which is sufficient.
Merely testing nonoverlap of core interiors would not establish this resource argument.
Different atoms may reuse the same site; their budgets are separate, and summing their
individual inequalities remains valid.

## An Exact, Abstract Expressiveness Test

Both multiplicity patterns become `(2,2,1,1,1)` after relabelling.
Call the two heavy sites `H1,H2` and the three light sites `L1,L2,L3`. A **trace** is
the subset of sites contained in a core.
The minimal traces charged by the weighted atom are:

- `{H1,H2}`;
- each of the six triples containing one heavy site and two light sites.

On the abstract universe of all subsets of these five sites, the minimum budget of a
nonnegative combination of ordinary distinct-site threshold atoms that charges every
weighted-positive trace by at least one is exactly `4/3`. The weighted atom itself uses
budget `1`.

For the upper bound, take the three ordinary two-of-three atoms on `{H1,H2,Lj}`, each
with weight `1/3`, and a three-of-five atom with weight `1/3`. The heavy pair receives
charge one from the first three atoms.
Every minimal triple receives `2/3` from those atoms and `1/3` from the last.
Monotonicity covers all larger positive traces.
All four atoms have unit unweighted budget, so the combined budget is `4/3`.

For the lower bound, assign abstract fractional mass `1/3` to the heavy-pair trace and
`1/6` to each of the six minimal triples.
The total is `4/3`. This mass satisfies every ordinary threshold resource inequality on
subsets of the five sites:

| Ordinary Atom’s Budget | Threshold | Largest Charge Against These Seven Weighted Traces |
| --- | --- | --- |
| 1 | 1 | `5/6` |
| 1 | 2 | `1` |
| 1 | 3 | `1` |
| 1 | 4 or 5 | `0` |
| At least 2 | Any | At most total mass `4/3`, hence at most its budget |

For an explicit check of the table, let an ordinary support contain `h` heavy sites and
`l` light sites.
Let `Q_l(r)` count pairs of light sites meeting that support in at least
`r` sites:

```text
Q_l(r) = sum over j=0,1,2 of [j >= r] C(l,j) C(3-l,2-j).
```

A binomial coefficient outside its usual range is zero.
The ordinary atom’s charge at threshold `k` is then

```text
[h >= k]/3 + (h Q_l(k-1) + (2-h) Q_l(k))/6.
```

Taking `0 <= h <= 2`, `0 <= l <= 3` and `k <= h+l < 2k` gives the first four rows.
These are all budget-one ordinary atoms; larger budgets are covered by the final row.
Any nonnegative combination that charges all seven traces at least one must therefore
have budget at least their total fractional mass `4/3`.

This is an analytic statement about Boolean incidence and atoms supported on the same
five sites. It is not a statement that the seven traces are simultaneously realized by
admissible square cores at the retained coordinates, nor that other point sites or atoms
cannot remove the difference.
It provides a precise reason to test multiplicities and a small exact control for the
new representation. It establishes no packing bound.

## Smallest Maintained Representation

Extend the ordinary threshold representation with an explicit integer multiplicity per
distinct coordinate.
Missing multiplicities in legacy records mean all ones.
Keep site count and token count separate:

```text
site_count  = len(points)
token_count = sum(multiplicities)
budget      = weight * (token_count // threshold)
trace_count = sum(a for (point,a) if point is in the closed core)
key         = (sorted((x,y,a) triples), threshold)
```

The smallest compatible change retains `.points` as distinct coordinates and avoids
silently changing what existing `.size` cursor code means.
Add an explicit token-count property and audit every budget and expansion call site.
A single property rename without that audit can make a sweep consume seven rectangles
when it created five.

Require genuine positive JSON integers, excluding booleans, floats, strings, zero and
negative values. Require equal array lengths and `1 <= t <= token_count`. Treat
`total_multiplicity`, `size`, `budget`, and `orbit_size` as optional checked
declarations, never authoritative inputs.
The independent reader must recompute the budget from the raw multiplicities rather than
trusting the model’s budget property.

For certificate input, reject repeated coordinates.
The declared multiplicity field is the only representation of coincident tokens.
A separate explicit import operation may merge repeated exact coordinates by adding
multiplicities, but must retain the mapping and refuse contradictory declarations.
Sorting coordinates without carrying their multiplicities, converting to a set, or
placing near-duplicate points around a boundary changes the atom.
Rational strings must remain exact; no decimal simplification is licensed by the
historical charge.

Give weighted certificate records a version or variant that the current unweighted gate
refuses. The current strict loader ignores unknown atom fields: adding only a
`multiplicities` field under `variant: threshold` lets an old verifier silently read a
different object. Update format dispatch and its refusal tests as part of admission.

### D4 Symmetry

Transform coordinates and carry each multiplicity with its site.
Deduplicate images using the weighted key, including threshold.
Geometric support symmetry alone is insufficient: a reflection that exchanges a heavy
and a light site is not a symmetry of the weighted atom.

An orbit column’s coefficient on a placement is the sum of charges over its distinct
images. Its cost is the number of distinct images times the per-image resource budget.
Do not assume eight images or deduplicate with the ordinary point-only key.
Check symmetry after coordinate normalization and after the declared translation.
Deduplicate the two new candidate orbits against each other using these same keys; do
not guess how many orbits or images survive.

## Changes Required in the Two Coverage Methods

The event-cell proof survives multiplicity: membership remains constant on open cells,
and a boundary of a closed core can only add sites and their positive token counts.
The charge is still monotone.
This does not justify treating a site on a boundary as only partly present; all of its
tokens have the same membership.

For the event sweep in `packing/src/sqpack/fractional/threshold.py`, retain one
geometric membership rectangle per distinct site, but expand it into labelled token
rectangles when forming the existing inclusion-exclusion terms.
Subsets are subsets of token indices, so equal rectangles must retain their
combinatorial multiplicity.
The usual seven-token, threshold-four identity has 64 subset terms and total absolute
coefficient mass 209 before geometric cancellations.
The existing int64 headroom check must use token count in this expansion bound.
The direct reference grid should instead paint each distinct site’s rectangle with its
integer multiplicity and then threshold the count.
It must not reuse the sweep’s token expansion.

For `packing/src/sqpack/fractional/threshold_interval.py`, the smallest change repeats
the distinct site’s index `a_s` times in the atom’s member row.
The existing boolean gather then counts tokens, while geometric interval enclosures are
still computed once per distinct coordinate.
Build this row directly from explicit multiplicities, rather than sharing the sweep’s
expansion helper. Update exact witness reevaluation to sum multiplicities directly.
Retain memory caps, and validate token-count and threshold headroom before allocation or
narrowing to int16. A small supported token cap is enough for this admission; arbitrary
multiplicities need not be admitted in the same block.

The interval method may stall at exact membership seams, especially with the retained
long rational coordinates.
A stall is unresolved, not a false atom or a failed budget proof.
Require agreement and complete coverage only when claiming certificate admission; the
exact finite matrix experiment can be evaluated independently of whether a future
candidate certificate has passed continuous coverage.

## Producer, Capacity Reader, and Record Changes

| Component | Required Change |
| --- | --- |
| `threshold.py` model, record conversion, symmetry and budgets | Explicit multiplicities, weighted keys, strict validation, separate token count, versioned serialization |
| `decide_threshold_certificate.py` | Parse and preserve multiplicities; refuse malformed or unsupported versions; verify all declarations |
| `admit_threshold_atom_orbits.py` | Reconstruct weighted D4 images and exact membership; independently recompute token budgets and every image’s charge |
| `admit_fixed_support_dual.py` when used | Parse weighted priced rows and recompute orbit costs; its current constructors assume ordinary atoms |
| Maintained paired-program producer | Exact common matrix and column cost manifests; append weighted columns only in treatment; retain rational primal and dual witnesses |
| Event sweep and interval route | The distinct implementations described above, plus exact witness agreement |
| Geometric transformations and freezes | Preserve multiplicities when moving points, including `dilation_corollary.py`; no constructor may default a weighted atom back to all ones |

The archived `floor_atom_columns` applies a float slack to membership.
A candidate covering primal feasible for that loosened matrix may fail the exact matrix.
A float LP can propose weights; independently evaluate every common row and column in
rational arithmetic for the two witness inequalities.
A tolerance flag or successful HiGHS status cannot replace that check.

## A Valid Common Finite Comparison

The proposed finite comparison uses container side `383/100`, core side `9977/10000`,
and the retained 181-direction net.

The historical 15,021-row program is unavailable.
The retained `lane-a6-dual-round1-structural-rows.json` contains only 16 positive-dual
rows, and the small ceiling families are also supports rather than full program
reconstructions. `lane-a6-structural-sites-153-40.json` retains 1,400 site orbits, not
the complete historical point-column inventory.
The 2,566 ordinary atom orbits and six later ordinary orbits are available.
These facts permit a new finite program but do not recover the old one.

Before solving either arm, materialize and retain exact manifests for:

1. The row union, with each exact placement geometry, source path and source entry,
   deduplication key, core side and direction.
   Include both candidates’ matched source families so the representation has observable
   positive controls. Declare any other retained supports or prospectively generated rows
   explicitly.
2. The common point sites and ordinary threshold orbits.
   Choose a reproducible set from retained sources; do not label it the historical
   complete support. If the new weighted sites also become point columns, add those point
   columns to **both** arms before comparing.
   Otherwise declare that they occur only inside the new atoms.
3. The complete exact direction list, D4 folding rule, geometry convention, column
   order, costs, initial state, solver settings, target cap, and both arms’ result
   locations.

Source families include reflected net directions and declare `symmetric_only: true`.
Preserve their exact geometry or prove their folding into the declared D4 row regime.
Do not interpret a source direction index without its net or round an angle to a nearby
direction.

The proposed translation from `153/40` to `383/100` is exactly `(1/400,1/400)` for both
coordinates. With core side unchanged, translating every site and row by that vector
preserves every incidence and commutes with D4 about the respective container centres.
Consequently a finite program built entirely by this translation has exactly the same
matrix and optimum as its smaller-container counterpart.
This is useful for a controlled atom comparison, but it provides no evidence about newly
available boundary placements at `3.83`. Those placements enter through separately
declared row generation or the full coverage gate.

The control has the declared common point columns and 2,572 ordinary orbit columns
before any exact deduplication.
The treatment appends only the deduplicated weighted orbits.
Use the same rows, common columns and solver conditions, with one solve per arm under
the frozen shared cap.
If a control cannot cover a declared row, report the finite program’s infeasibility; do
not add columns or drop rows after seeing the result.

Let `M w >= 1` be the covering constraints, `c` the exact resource costs, and
`M^T y <= c` the dual constraints.
Verify `w,y >= 0` and all inequalities independently in rationals.
Then `c.w` is a finite primal upper bound and `sum(y)` a finite dual lower bound.
A strict effect is proved when treatment upper bound is below control lower bound.
Equality requires matched exact bounds or an equivalent exact shared optimality witness.
Zero treatment weights or equal printed decimals alone do not prove a tie.

## Staged Admission and Falsifiable Accept Rules

| Stage | Deliverable | Accept Rule | Outcome if Incomplete |
| --- | --- | --- | --- |
| Representation and theorem | Maintained weighted binary atom, exact record round-trip, weighted D4 key, resource proof | All 32 site masks for each motif agree with explicit token counting; identity, symmetry, invalid-integer, duplicate-coordinate and understated-budget mutations behave as declared | Weighted target remains unrun |
| Independent source replay | Exact receipts for both retained candidate-family pairs | Exact total tokens `7`, threshold `4`, budget `1`; source charge `3/2` and exact charged-placement list reproduced; candidate and family identities bound | Identify the exact discrepancy; do not replace coordinates or candidates within this protocol |
| Coverage mechanics | Small positive, negative and boundary controls for direct, sweep and interval paths | Closed-boundary token membership agrees; dense and slab results agree; interval enclosures contain direct rational values; positive controls finish and agree exactly; a known undercharged core is rejected | Representation may be sound, but certificate coverage admission remains blocked |
| Paired instrument | Reproducible exact common manifests and maintained runner | Same matrix on common columns, treatment-only additions, exact orbit costs; all-one multiplicities reproduce legacy rows; cap/deadline/partial-result and forged-witness refusals pass | No finite scientific comparison |
| New finite comparison | One newly registered hypothesis and experiment record | `U_treatment < L_control` using independently checked rational witnesses | Exact tie rejects this frozen improvement claim; overlap or unfinished solve is unresolved |
| Continuous certificate, conditional on a candidate | Full candidate certificate and physical transfer record | Budget below eleven, every required direction and centre covered by both complete routes, exact agreement and physical transfer conditions checked | No new global bound; an escape rejects only the declared weight vector on its declared domain |

The first four stages form the bounded W7 admission block.
They are fixture and source validation, not an early look at the new LP target.
Register a new hypothesis after the source entry point and common input manifests are
fixed. H-156 is already confirmed by T-026, so this finite comparison needs a separate
hypothesis and result record.
If admission takes longer than the block, carry its explicit unfinished dependencies
forward and keep the target unrun.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
