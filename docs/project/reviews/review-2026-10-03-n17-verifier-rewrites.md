---
title: n17 Verifier Rewrites Review
date: 2026-10-03
status: planning-review
---
# n17 Verifier Rewrites Review

**Session:** 168, lane R6 (independent soundness reviewer).
**Reviewed:** the standing kernel verifier
`packing/devtools/verify_n17_kernel_certificate.py` at commit `e0b66f07b` (SHA-256
`5c550f7c…`, lane F2’s rewrite) against the reviewed version at `55656158`
(`26bd5b41…`), and the standing branch-and-bound verifier
`packing/devtools/verify_n17_bb_certificate.py` at `ff5471e89` (`9ca8df6f…`, lane P2’s
Taylor path and enclosure retry) against `55656158` (`4a93c74c…`). **Question:** may
either new digest be listed under `verifiers:` in
`packing/campaign/explorations/X048-session-168-pilots/certified-sub-patterns.yaml`,
where `devtools/census_n17_certified.py` counts an admitted entry only with a passing
full verification by a listed digest?
**Method:** the diffs read in full against the two prior reviews
(`review-2026-10-02-n17-w7-closure.md`,
`review-2026-10-02-n17-branch-and-bound-certifier.md`) and F2’s rationale
(`review-2026-10-02-n17-cost-reduction-performance.md`, section 4); then scripts of my
own under
`packing/campaign/explorations/X048-session-168-pilots/audit-verifier-rewrites/`:
`audit_kernel_rewrite.py.txt` (a differential harness of the new integer forms against
the reviewed `Fraction` forms and against a third method), `mutate_cert.py.txt` and
`make_fixture.py.txt` (34 doctored kernel certificates), `run_verifier_mutants.py.txt`
with `mutant_plugin.py.txt` (21 mutants of the verifier’s new code, each run against the
harness, the committed tests and the doctored certificates), `bb_trig_retry.py.txt` (the
2,400-bit retry on crafted enclosure tables), and the agreement runs whose receipts and
logs sit beside them (`w7-*.json`, `n1-*.json`, `a-*.json`). Nothing in the repository
was edited except this document, that directory and, at the coordinator’s request, the
test file `packing/tests/test_verify_n17_certificates.py` (section 2.8); the verifiers
and the ledger are untouched.

## Verdicts

- **Kernel verifier `5c550f7c…`: ADMIT WITH CONDITIONS.** Every obligation the reviewed
  version checked is still checked, exactly, and nothing is weakened: the edge-merge
  facets are the exact halfplane description of partner − core for every pair the
  certificate can present, the sweep decides closed coverage exactly, and the four memos
  are pure functions of exact inputs, invalidated when their inputs change.
  The new verifier re-proves W7 in full with the admitted receipt’s counts, agrees with
  the reviewed verifier on the same sampled rows of W7 and of N1, refuses all 33 unsound
  doctored certificates, and every weakening mutant of its new code is caught by at
  least one check in this review.
  The conditions (section 2.8) were three test additions, not verifier changes: the
  committed tests missed three weakening mutants that only this review’s own cases
  caught, and the digest should not be listed until the suite that guards the next
  rewrite sees them. They are met: the tests are in the committed file, each of the five
  mutants named in section 2.8 now fails at least one committed test, the unmutated
  verifier passes all 27, and the verifier’s bytes, and so the digest, are unchanged.
- **Branch-and-bound verifier `9ca8df6f…`: ADMIT.** The interval-mode (schema v1) path
  is unchanged in effect, and now stricter in three places; the 2,400-bit retry of a
  failed enclosure cannot accept an enclosure that excludes the true value; the Taylor
  checks X1 to X5 are sound as far as reading and the committed Taylor tests establish.
  No Taylor certificate is planned for admission, and admitting one would be a review of
  that certificate, not of this digest.
- **Kernel verifier with the cover fix (section 6, added later): can be listed.** Every
  listed kernel revision checked a zero-area row only at sample points, and those from
  `e0b66f07b` on let a one-point section through with no containing span.
  Neither branch was taken on W7, SW9 or N1, and the fixed verifier passes all three in
  full.

## Summary

- **The kernel rewrite keeps the proof and changes the arithmetic.** The diff
  (`git diff 55656158 e0b66f07b`) touches three computations and nothing else: collision
  facets, the row cover, and memoisation.
  The seed, frame, hull chain, compression, closure derivation, final-state comparison,
  partner-cover equality and strictness, the region’s containment in the required
  domain, the degenerate-row branch and the `--sample` protocol are byte-identical.
- **Facets.** `difference_facets` is the support-function form of a Minkowski sum: every
  facet of partner − core has the direction of an edge of the partner or of the negated
  core, and its support is the partner’s maximum minus the core’s minimum.
  Both inputs reach it as `hull` output with at least three vertices and positive area
  (lines 771–772 and 929–930), so no degenerate direction, repeated vertex or non-convex
  input can enter; parallel directions merge on a lowest-terms key.
  On 206 pairs, including slivers, 2^-50 edges, odd denominators and point-symmetric
  pairs, the facet set equals the reviewed hull form’s, every facet is tight, and random
  points near the boundary classify identically.
- **Sweep.** `covered_by_sweep` probes every vertex abscissa and edge crossing in the
  domain’s x-range and one interior point of every open slab between them; on an open
  slab no edge begins, ends or crosses, so every comparison the closed-interval merge
  makes has a constant outcome there, and one probe decides the slab.
  An uncovered point of the closed domain has an uncovered open neighbourhood meeting
  the domain’s interior, so some slab sees it.
  On 229 cases, among them a gap of width 2^-60 hidden strictly between two events, the
  sweep agrees with the reviewed area cover and with point sampling.
  Two observations, neither a defect: `section_covered` deems a one-point target with no
  span covered, which the sweep can meet only at the domain’s extreme abscissae and
  which the neighbouring slab probe then exposes (section 2.2); and the sweep’s section
  of a polygon is the min and max of its live edges’ ordinates, which is right only for
  convex input, and every call site passes `hull` output.
- **Memos.** The facet memo keys on both cores’ exact homogeneous vertex tuples, the
  forbidden-region memo on the exact owned hull and core, the row-minimum memo on the
  normal direction over an immutable domain, and a partner row’s admitted cover is
  reused only on the same accepted `Row` object with byte-equal published lists; a
  partner’s own step builds new `Row` objects, so its covers are proved afresh.
  Doctored certificates that republish a cover with a wider core, a grown domain, or
  stale lists after the partner stepped (relabelled so that only the domain check can
  refuse) are all refused.
- **Agreement.** W7 in full: PASS, 184 s, every count equal to the admitted receipt’s
  (30,952,184 facet inequalities, 7,752 regions, 3,324 cover checks, 19,282 partner
  rows). W7 sampled at four rows per step: old and new PASS on the same 270 rows with
  identical counts, 342 s against 76 s. N1, the pending 17-cell state node (32 bins, 82
  steps), sampled at one row per step with every row of the closure step: the new
  verifier passes it in 117 s with the checker’s closure (owner 18, step 81), 113 rows
  in full, 400 regions, 669,668 facet inequalities, 41,162 partner rows; the reviewed
  verifier passes the same rows with the same closure and identical counts in 923 s.
- **Mutation testing.** 33 unsound doctored certificates refused, each at the check its
  construction targets, and one control passed its cover check (section 2.6). Of 21
  verifier mutants, 19 are caught by at least one check, one is equivalent (vertical
  edges are redundant with the non-vertical edges that end on them), and one, a memo
  keyed on the normal’s x-component alone, is caught by nothing here and is established
  by reading (section 2.7). The committed tests miss three weakening mutants: two sweep
  mutants that probe only at events, caught by the hidden-lens cases, and a collision
  loop over the first partner row only, caught by a region vertex pushed past a later
  row’s facet.
- **Branch and bound.** The v1 path’s values are computed by the same code (the plane
  tuples carry two extra fields the v1 path ignores; `cos_sin` is the same series at the
  same 160 bits), and three checks are new and stricter: the manifest’s schema must
  match the Taylor setting, a cut record must have four or eight fields, and a wall-row
  reference in an interval certificate is refused.
  On A sampled (50 closures of each kind, the 20 deepest, every ancestor, 100
  enclosures, seed 7) the two verifiers PASS the same 1,225 nodes with identical counts.
  The retry accepts an enclosure only when this module’s own 2,400-bit enclosure fits
  inside it: on a crafted table, a recorded enclosure narrower than the 160-bit one but
  containing the true value is refused by the reviewed verifier and accepted by the new
  one, and two that exclude the true value are refused by both.
  X1 to X5 are read in section 3.4; the 35 committed tests of both verifiers pass.

## 1. What the Kernel Rewrite Changed

The reviewed verifier proved each full row’s collision regions against
`planes_of(minkowski_diff(partner_core, core))` in `Fraction`, with the minimum over the
partner row’s domain recomputed per facet, and decided each row’s cover by
`covered_by_area`: closed clipping subtraction whose leftover pieces must have total
area zero. The rewrite:

- computes the facets of partner − core by `difference_facets` in homogeneous integers
  (`(X, Y, Z)` with `Z > 0`, `homogeneous` at line 307) and checks each region vertex by
  cross-multiplication (`check_collisions`, lines 837–848);
- decides the cover by `covered_by_sweep` (line 521) and keeps `covered_by_area` as the
  reference the tests hold it against;
- memoises `difference_facets` per pair of cores (`State.difference`), `minkowski_diff`
  per (owned hull, core) (`State.forbidden_region`), the least value of `n · y` over a
  partner row’s domain per direction (`CoverRow.minimum`), and the admitted cover of a
  partner row (`Row.cover`, reused at `check_partners` lines 798–806 only when the same
  `Row` object sees byte-equal `domain` and `core` lists).

`check_partners` also replaces `if not vertices` by `if not any(r.residual)`, which is
the same test, and `check_collisions` computes `planes_of(required)` once per row
instead of once per vertex, which is the same check.
Everything else in the module is unchanged.

## 2. Soundness of the New Code

### 2.1 The Edge-Merge Facets Are Exact

**Claim.** For strictly convex counterclockwise polygons $P$ and $C$ with at least three
vertices,
$\{p : n \cdot p \le h_P(n) - \min_{w \in C} n \cdot w \text{ for every } n \in
N\}$, with $N$ the outward edge normals of $P$ and the negated outward edge normals of
$C$, equals $\mathrm{hull}(P - C)$.

**Why.** The support function of a Minkowski sum is the sum of the summands’ support
functions, and in the plane the edge directions of $P + (-C)$ are exactly the edge
directions of $P$ and of $-C$ (the face of the sum in direction $n$ is the sum of the
faces, and a face that is an edge of either summand gives an edge of the sum).
So the halfplanes over $N$ are exactly the facets of the sum, each with its exact
support, and a convex polygon is the intersection of its facet halfplanes.
Extra directions would only add supporting halfplanes, which do not cut the set; the
risk is a missing direction or a wrong support, and the evidence below checks both.

**Where the implementation meets the claim.** `directions` (line 358) takes the normal
$(q_y - p_y,\; p_x - q_x)$ of each edge $p \to q$ scaled by the positive product of the
two denominators, outward for counterclockwise order, and divides by the gcd so that
parallel directions share a key; `hull` (Andrew’s chain, line 102) returns
counterclockwise order with collinear points removed.
`support` (line 371) compares $v/z$ values by cross-multiplication with positive
denominators. `difference_facets` (line 387) takes the partner’s maximum and the core’s
minimum and forms
$(h_n, h_d) = (\text{top}_n \text{low}_d - \text{low}_n \text{top}_d,\;
\text{top}_d \text{low}_d)$ with $h_d > 0$. In `check_collisions` the bound is
$h + \min_{y \in D} n \cdot y$ as $(h_n m_d + m_n h_d)/(h_d m_d)$ and the test
$(n \cdot v) h_d m_d \le \text{bound}_n z$ is the reviewed inequality cleared of
denominators. The inputs are `cover.core` (the hull of the published partner core, at
least three vertices and positive area, line 772) and `core_h` (the hull of the row’s
core, line 929–930), so a repeated or collinear vertex, a segment or a point never reach
`directions`, where a zero normal would divide by zero rather than pass.
The reviewed `require(len(facets) >= 3)` is kept.

**Evidence.** `audit_kernel_rewrite.py.txt --only facets`: 206 pairs (six fixed pairs,
including core = −partner where every direction merges and a core with an edge exactly
parallel to a partner edge, and 200 random pairs drawn from coarse-grid, 2^-30-grid,
odd-denominator, sliver, 2^-50-edge and regular kinds); 2,014 facets.
For every pair the set of (lowest-terms normal, exact support) equals the reviewed
`planes_of(minkowski_diff)` set with the same cardinality, every facet is attained by a
vertex difference and violated by none, and 20 random points per pair within 2^-45 of a
hull edge classify identically under both forms.
The committed `test_difference_facets_are_the_hull_facets` makes the first of these
checks on 41 pairs.

### 2.2 The Sweep Decides Closed Coverage Exactly

**Claim.** `covered_by_sweep(D, R)` returns `True` if and only if the closed convex
polygon $D$ (positive area) is contained in the union of the closed convex polygons in
$R$ (those with at least three hull vertices; points and segments cover no area and are
dropped, as the area form drops them).

**Why.** Let $E$ be the set of vertex abscissae of $D$ and of every region in $D$'s
x-range together with every abscissa where two non-vertical edges cross there.
On an open slab between consecutive points of $E$ no edge begins or ends and no two
edges cross, so for any two live edges the order of their ordinates is the same at every
abscissa of the slab, or they are the same line and equal everywhere.
Every comparison `section_covered` makes is between ordinates of live edges at the probe
(the sort by lower end, the gap test, the cursor update and the end test), so its
outcome at one interior probe is its outcome at every abscissa of the slab; ties among
equal lower ends do not change the merge’s result.
A convex polygon with a live edge on a slab has exactly two live edges there, so its
section is the closed interval between their ordinates, and at an event abscissa its
section is the min and max over its live edges and vertical edges, which `_widen` takes.
If some point of $D$ is uncovered, it has an open neighbourhood disjoint from the closed
union, that neighbourhood meets the interior of $D$ in an open set, and that open set
contains abscissae of an open slab; at those abscissae the section of $D$ has an
uncovered open sub-interval, so the merge fails there and hence at the slab’s probe.
Conversely a `True` at every probe gives coverage on every slab and at every event.

**Where the implementation meets the claim.** `compile_edges` (line 428) writes each
non-vertical edge as $a x + b y + c = 0$ with $b > 0$ so that its ordinate at $X/W$ is
$-(aX + cW)/(bW)$ with a positive denominator (line 562), and files vertical edges by
their normalised abscissa; I checked that the line through $p$ and $q$ vanishes at both.
`sweep_events` (line 451) adds every vertex abscissa in $[\text{left}, \text{right}]$
and, for every pair of edges with overlapping closed x-ranges (edges taken by increasing
`lo`, against those whose `hi` still reaches it), the crossing $x = (b_1 c_2 - c_1
b_2)/(a_1 b_2 - b_1 a_2)$ when it lies in the overlap; parallel edges are skipped, and
coincident ones are equal everywhere.
`covered_by_sweep` requires the domain’s own extremes to be the first and last events
(line 540), probes `positions[0]`, then for each consecutive pair the `between` ratio
and the right event (line 545), keeps an edge live while `lo <= probe <= hi` (lines
552–557), and requires the domain to have a section at every probe (line 567). `between`
(line 327) returns a lowest-terms ratio strictly inside $(a, b)$ by continued fractions;
on 223 pairs, including Farey neighbours with 30-digit terms where nothing below the
mediant’s denominator fits, it is strictly inside, in lowest terms, and at the mediant
when forced. `section_covered` (line 487) sorts by a float key and confirms the order
exactly on every adjacent pair, which is enough because the order relation on the lower
ends is transitive; a mis-sort would be redone exactly, never accepted.

**Two observations, neither a defect.**

- `section_covered(((y, 1), (y, 1)), [])` is `True`: a target that is a single point
  with no span never enters the merge, and the final test `cursor >= high` holds.
  The sweep meets a one-point domain section only at `left` and `right` when the
  domain’s extreme vertex is not on a vertical edge.
  An uncovered extreme vertex has an uncovered neighbourhood in the domain’s interior,
  which the first or last slab probe reports: the harness cases `vertex-only-gap-2^-40`,
  `-2^-70` and `-right` (a wedge whose only region is the wedge cut 2^-40, 2^-70 and
  2^-50 short of one vertex) all return `False`. A one-line guard
  (`if low == high and not spans: return False`) would remove the quirk; it is not
  needed for soundness.
- The section of a polygon at a probe is the min and max of its live edges’ ordinates,
  which is the polygon’s section only when the polygon is convex; a non-convex or
  self-intersecting region would have its section overstated.
  Every region reaching the sweep is `hull` output (`forbidden_region` returns
  `minkowski_diff`, a hull; collision regions and residuals are hulled at lines 828 and
  916; the domain is `hull(required)` at line 872), so the contract holds, and it should
  be kept if the call sites change.

**Evidence.** `audit_kernel_rewrite.py.txt --only sweep`: 229 cases, 93 covered and 136
not, with the sweep agreeing with `covered_by_area` on every one, the first uncovered
abscissa reported exactly when the verdict is `False`, and a third method agreeing: 30
random points of a covered domain each inside some region, and a centroid of a leftover
piece of the area subtraction inside none (2,926 points).
The cases: 200 random tilings of random convex domains cut by random lines (rectangle,
coarse-grid, 2^-30-grid, odd-denominator and regular kinds), with a piece removed, a
piece shifted by 2^-40, a piece shrunk toward an interior point by 1 − 2^-35, or
unrelated regions and a segment added; and 29 constructed ones: a **lens hidden strictly
between two events** at widths 1/8, 2^-40 and 2^-60 (a left block whose vertical edge
covers the whole section at $x = a$, a right block likewise at $x = b$, and between them
a region whose peaked roof rises from $y = 2$ at $x = a$ under a region whose V-shaped
floor sits $2\varepsilon$ above it at $x = a$ and crosses it at $x = a + 4\varepsilon$,
so the gap is invisible at every event and visible on one open slab), each with its
closed control; 4 × 4 axis-aligned tilings with one tile narrowed by 2^-50 horizontally,
vertically, or at one corner; a fan of four triangles around an interior point with one
apex pulled back by 2^-50; a bow-tie of four triangles meeting at a point, with and
without one; the domain itself, twice, shaved by 2^-60 at one vertex, and shifted by
2^-60; a domain and tiling with denominators $2^{40} 3^7 5^3$; segments and points mixed
in; a triangle fan with one piece shrunk by 1 − 2^-40; an engulfing region, and two
engulfing half-planes 2^-50 apart.
The committed `test_the_sweep_agrees_with_the_area_cover` has 48 random cases of the
first kind and no hidden lens, which is why the two sweep mutants of section 2.7 pass
it.

### 2.3 The Memos Return Only What Was Computed for Their Inputs

| Memo | Key | Value | Invalidation |
| --- | --- | --- | --- |
| `State.facets` | the two cores as tuples of homogeneous integer vertices in hull order (equal polygons give equal tuples, since `homogeneous` of a lowest-terms `Fraction` pair is canonical) | `difference_facets`, a pure function of the key | none needed |
| `State.forbidden` | `(tuple(owned hull), tuple(core))` as exact `Fraction` points | `minkowski_diff`, pure; the owned hull is replaced, never mutated, by `compress` (lines 1017–1019) | none needed |
| `CoverRow.minima` | the facet direction `(nx, ny)` in lowest terms | `support(domain, nx, ny, largest=False)` over the immutable `domain` tuple fixed at admission | none needed |
| `Row.cover` | the accepted `Row` object, with the published `domain` and `core` lists compared by value (lines 799–803) | the proof that the domain equals the hull of the row’s residual vertices and the core is strict over the row’s interval, a pure function of `(Row.residual, Row.interval, lists)`; `Row.residual` is never mutated after construction | a partner’s own step stores fresh `Row` objects with `cover=None` (`check_step` line 975, `verify_objects` line 1118), so every cover of a re-stepped partner is proved afresh; any change in either published list proves afresh |

A cache hit therefore skips no obligation: it returns the result of the same obligation
on the same inputs. The checks around the memo are still run on every step: the partner
must be in the mask and not the owner, the cover must have one item per accepted row,
each item’s reference and interval must equal the row’s, a dead row must publish empty
lists, and a cover with no live row is refused.

**Evidence.** The committed
`test_a_republished_partner_cover_is_reused_only_when_identical` and
`test_the_facet_cache_keys_on_the_exact_cores`; the doctored certificates
`cover-memo-same-domain-wider-core` (refused “core not strict” at the later step),
`cover-memo-same-core-grown-domain` (“domain”), `cover-stale-after-partner-stepped`
(“reference”) and `cover-stale-relabelled-after-partner-stepped` (the stale lists
carrying the new rows’ references and intervals, so that only the domain check can
refuse: refused “domain”); and the five cache mutants of section 2.7. On the W7 fixture
of 14 steps every step republishes all six partners, so the memo’s reuse path is
exercised on 672 partner rows and the verdict and counts are the reviewed verifier’s.

### 2.4 Independence

The module imports `argparse`, `gzip`, `hashlib`, `json`, `math`, `random`, `time`,
`collections.abc`, `dataclasses`, `fractions`, `itertools`, `pathlib` and `typing`, and,
lazily in `cover_cells`, `devtools.check_n17_capacity_one_cover`, which imports
`devtools.check_n17_endpoint_feasibility` and nothing from `sqpack.hull_kernel`,
`check_n17_subpattern`, the selector or the branch and bound.
The committed `test_a_verifier_imports_no_producer_checker_or_solver` imports the module
in a subprocess, builds the cells and asserts that none of those modules, nor anything
named like HiGHS, is in `sys.modules`; it passes.
The two Python verifiers still share CPython’s `int` and `fractions` with the checker,
as the performance review’s section 4 notes; the rewrite adds no dependency.

### 2.5 Agreement With the Reviewed Verifier

| Run | Verifier | Mode | Status | Rows in full | Collision regions | Facet inequalities | Partner rows | Seconds |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| W7, admitted receipt (`verification.json`) | `26bd5b41` | full | PASS | 3,324 | 7,752 | 30,952,184 | 19,282 | 4,258 |
| W7, F2’s receipt (`verification-5c550f7c.json`) | `5c550f7c` | full | PASS | 3,324 | 7,752 | 30,952,184 | 19,282 | 242 |
| W7, this review (`w7-new-full.json`) | `5c550f7c` | full | PASS | 3,324 | 7,752 | 30,952,184 | 19,282 | 184 |
| W7, `--sample 4 --sample-seed 12345` (`w7-old-sample4.json`) | `26bd5b41` | sample | PASS | 270 | 596 | 2,076,688 | 19,282 | 342 |
| W7, same sample (`w7-new-sample4.json`) | `5c550f7c` | sample | PASS | 270 | 596 | 2,076,688 | 19,282 | 76 |
| N1, `--sample 1 --sample-seed 12345` (`n1-old-sample1.json`) | `26bd5b41` | sample | PASS | 113 | 400 | 669,668 | 41,162 | 923 |
| N1, same sample (`n1-new-sample1.json`) | `5c550f7c` | sample | PASS | 113 | 400 | 669,668 | 41,162 | 117 |

The sampling code is unchanged, so the same seed selects the same rows in both
verifiers, and the counts compare row for row.
Every count the two verifiers report on the same input is equal; the closure derived is
`all_parent_poses_forbidden` for owner 5 at step 57 on W7 and for owner 18 (interior-W)
at step 81 on N1, the closure lane K2’s checker recorded.
N1 is the 17-cell state node from lane K2’s `--check-saved` run (32 bins, 82 steps,
8,470 collision regions), which the checker passed; it is pending, not admitted, and is
used here only as a second, larger input on which the two verifiers can be compared.

### 2.6 Doctored Certificates

`make_fixture.py.txt` produces W7 at 8 bins with lane K2’s producer (14 steps, 112 rows,
257 collision regions, two steps with kernels, four compressions, a stall; the same
shape as lane R3’s mutation fixture), saved with the checker tool’s saver so that only
the mathematics is wrong.
`mutate_cert.py.txt` edits a deep copy per mutation, re-saves it, and runs the new
verifier’s `verify_objects`; the unmutated fixture is accepted (84,300 facet
inequalities, 672 partner rows).
Where a mutation would first trip a structural check rather than the one under test (a
residual change alters the published common-core planes and outer bounds; a seed change
alters the digest the node binds), the harness recomputes those so the refusal names the
intended check.

| Mutation | Expected refusal | Verdict |
| --- | --- | --- |
| collision-region vertex pushed 2^-40, and 2^-80, past its tightest facet over every live partner row | region escapes the collision set | refused |
| a vertex added past a facet of a partner row other than the first live one, every first-row facet still satisfied | region escapes the collision set | refused |
| region vertex outside the required domain | escapes the required domain | refused |
| region naming the owner; region naming a partner whose cover was removed | collision partner | refused, refused |
| partner cover domain with a vertex dropped; with a far vertex added | domain | refused, refused |
| a live partner row declared empty; every row declared empty | domain | refused, refused |
| partner core scaled by 1.02; by 1 + 2^-20 | core not strict | refused, refused |
| the same domain republished at a later step with a wider core (memo) | core not strict | refused |
| the same core republished with a grown domain (memo) | domain | refused |
| a cover copied from before the partner stepped; the same relabelled with the new rows’ references and intervals | reference; domain | refused, refused |
| a residual polygon dropped, planes recomputed; planes kept | required domain NOT covered; common-core planes | refused, refused |
| a residual shrunk toward its centroid by 1 − 2^-40; by 1 − 2^-70 | NOT covered | refused, refused |
| a corner triangle of side 2^-40 cut from a residual; a vertical residual edge moved inward by 2^-50 | NOT covered | refused, refused |
| a collision region shrunk by 1 − 2^-40 | NOT covered | refused |
| the row’s residuals replaced by four pieces of its required domain with a lens of width 2^-40 hidden between two events, collision regions removed | NOT covered | refused (uncovered at $x = 253059607/146052101$) |
| the same with the lens closed (control) | passes the cover check | passed it; refused later at “final residual”, as the altered residual no longer matches the final state |
| a kernel point pushed 2^-40 past its tightest common-core plane | kernel point fails a plane | refused |
| a retained hull vertex moved one grid unit; an extra retained point with a copied witness | witness point | refused, refused |
| a prior owned hull with a point added | prior hull | refused |
| a row removed | any | refused (“final rows”) |
| a closure declared on a stall | no closure derived | refused |
| a seed row with a vertex dropped; an unowned seed point, both with the node rebound to the new seed digest | seed row domain; not owned | refused, refused |
| the owner’s core scaled by 1 + 2^-20 | core not strict | refused |

Lane R3’s 26 mutations against the kernel’s checker are matched here against the
verifier where the verifier checks the same thing; the unowned seed point, which ends as
`INCOMPLETE` in the checker, is refused outright by the verifier’s bounded bisection.

### 2.7 Mutants of the Verifier’s New Code

`run_verifier_mutants.py.txt` applies each textual patch once to a scratch copy of the
verifier and runs three checks against it: the harness (`--trials 120`), the twelve
kernel tests of `tests/test_verify_n17_certificates.py` (with `mutant_plugin.py.txt`
binding the mutant under the committed module’s name, so the repository is untouched),
and the 34 doctored certificates (caught when the mutant accepts an unsound one or
refuses the sound fixture).

| Mutant | What it weakens | Harness | Committed tests | Doctored certificates |
| --- | --- | --- | --- | --- |
| facets: core directions dropped | a facet subset | caught | caught | missed |
| facets: core support as a max | every facet bound too large | caught | caught | caught (refuses the sound fixture) |
| facets: partner support skips a vertex | a bound too small or too large | caught | caught | caught (refuses the fixture) |
| collision: row minimum subtracted | bound wrong | missed (not audited) | caught | caught (refuses the fixture) |
| collision: first partner row only | a dropped quantifier | missed (not audited) | **missed** | caught (the later-row vertex is accepted) |
| sweep: no mid-slab probes | gaps between events unseen | caught (hidden lens) | **missed** | missed |
| sweep: crossings not events | slab order not constant | caught (hidden lens) | **missed** | missed |
| sweep: ended edges stay live | sections overstated | caught | caught | caught |
| sweep: edges live early | sections overstated | caught | caught | caught |
| sweep: vertical edges ignored | — equivalent: the non-vertical edges ending on a vertical edge are live at its abscissa and give the same section | missed | missed | missed |
| section: gap ignored | an uncovered interval accepted | caught | caught | caught |
| section: end ignored | a short merge accepted | caught | caught | missed |
| section: open merge | touching spans treated as a gap less | caught | caught | caught |
| `between` returns an endpoint | the slab probe is an event | caught | caught | missed |
| cache: facets keyed on the partner alone | facets of another core reused | missed (not audited) | caught | caught (refuses the fixture) |
| cache: forbidden region keyed on the hull alone | a region of another core reused | missed (not audited) | missed | caught (refuses the fixture) |
| cache: cover reused when the domain matches | a wider core reused | missed (not audited) | caught | caught |
| cache: cover reused when the core matches | a grown domain reused | missed (not audited) | caught | caught |
| cache: covers survive the partner’s step | stale proofs reused | missed (not audited) | missed | weakened: the relabelled stale cover is reused and the certificate is refused later at a collision check instead of at “domain” |
| cache: row minimum keyed on $n_x$ alone | a minimum of another direction reused | missed (not audited) | missed | missed |
| `homogeneous` scales $x$ by the wrong factor | every integer form wrong | caught | caught | caught (refuses the fixture) |

Reading the misses: the harness audits only the four pure functions, so collision-loop
and cache mutants are outside it by design; the doctored certificates can only show a
mutant that accepts something, and a mutant that refuses more is caught by the sound
fixture. The row-minimum key mutant is seen by nothing here: on the fixture no partner
row meets two facet normals with equal $n_x$ and different $n_y$ in a way that changes a
verdict, and the committed code’s key `(nx, ny)` is the full input of `support` over a
fixed domain, which is what establishes it.

### 2.8 Conditions: Three Test Additions, Made

Three weakening mutants passed the committed tests as they stood and were caught only by
cases written for this review.
A verifier whose tests do not see a dropped quantifier in its collision loop, or a sweep
that probes only at events, is guarded by this review alone, and the next rewrite would
start from the same blind spots.
I judged the test additions a condition of listing the digest rather than a follow-up,
and at the coordinator’s request made them myself, so that the author of the verifier
and the author of its guard stay separate:
`packing/tests/test_verify_n17_certificates.py` now holds 27 tests (from 23), passes
`ruff format`, `ruff check` and `basedpyright`, and the verifier’s bytes are unchanged
(`sha256sum` gives `5c550f7c…` after the edit).
`verifier-mutants-tests.log` runs the whole extended file against the five mutants named
below (`run_verifier_mutants.py.txt --whole-file --skip-harness --skip-certs`) and
against the unmutated verifier:

| Verifier | Result of the extended test file |
| --- | --- |
| unmutated `5c550f7c` | 27 passed |
| `sweep-no-mid-slab-probes` | `test_the_sweep_sees_a_gap_hidden_between_events` fails, 26 pass |
| `sweep-no-crossing-events` | `test_the_sweep_sees_a_gap_hidden_between_events` fails, 26 pass |
| `collision-first-partner-row-only` | `test_the_kernel_verifier_checks_every_live_partner_row` fails, 26 pass |
| `cache-forbidden-key-hull-only` | `test_the_forbidden_region_cache_keys_on_the_exact_core` and the partner-row test fail, 25 pass |
| `cache-minimum-key-nx-only` | `test_the_row_minimum_memo_keys_on_the_whole_direction` fails, 26 pass |

1. **The sweep mutants** (`probes.extend((between(a, b), b))` → `probes.extend((b,))`,
   and every edge pair treated as parallel), caught by the harness cases `lens-2^-40`,
   `lens-2^-60` and `lens-1/8`. `lens_regions(eps)` builds the construction of section
   2.2 on the square $[0, 4]^2$: a left block to $x = 1$, a right block from $x = 3$, a
   region whose roof rises from $(1, 2)$ to $(2, 9/4)$ and a region whose V-shaped floor
   starts $2\varepsilon$ above it at $x = 1$ and crosses it at $x = 1 + 4\varepsilon$.
   `test_the_sweep_sees_a_gap_hidden_between_events` asserts that the area cover and the
   sweep both refuse it at $\varepsilon = 2^{-40}, 2^{-60}$ and $1/8$, that the sweep’s
   reported abscissa lies in $(1, 1 + 4\varepsilon)$, and that both accept the closed
   version ($\varepsilon = 0$). Both mutants return `True` on the open one.
2. **The collision-loop mutant** (`for cover in partners[pj]` → `partners[pj][:1]`),
   caught by the doctored certificate `region-vertex-pushed-later-row-only-2^-40`. A
   fifth doctored blind-pair closure cannot see it: on the blind pair the first live
   partner row’s collision set, cut to the required domain, lies inside every later
   row’s set in all 16 regions (`blind_pair_first_row_equivalence.py.txt`), so a
   verifier that stopped at the first row is equivalent to the full one there.
   `test_the_kernel_verifier_checks_every_live_partner_row` therefore produces W7 at 8
   bins once per module (the fixture of section 2.6, 14 steps, about 4 s), replays the
   verifier’s state to the step with the verifier’s own functions, cuts a row’s required
   domain by the first live partner row’s facets in the reviewed hull form, takes a
   vertex of the cut that violates a facet of a later row, appends it to the collision
   region (so the region still contains the old one and the row’s cover is untouched),
   and expects “escapes the collision set”; the undoctored objects must pass
   `verify_objects` as a stall.
   The test produces the objects with lane K2’s producer, as the blind pair’s test does;
   the verifier under test imports neither.
3. **The two cache tests** I had recommended as cheaper additions, made in the same
   change: `test_the_forbidden_region_cache_keys_on_the_exact_core` (the same owned hull
   with two cores $2^{-40}$ apart gives two cached regions, the second equal to a fresh
   `minkowski_diff`) and `test_the_row_minimum_memo_keys_on_the_whole_direction` (five
   directions, among them $(0, 1)$ and $(0, -1)$ and $(1, 0)$ and $(1, 2)$, each
   returning `support` over the domain, with five entries cached).
   The second catches the one mutant nothing in this review had seen (section 2.7).

For `cache-cover-survives-restep`, which the doctored certificates only weaken, a
doctored closure with a stale relabelled cover expecting “domain” would catch it in the
committed style (the mutant then fails elsewhere, and the message assertion fails); I
leave it as a follow-up.

### What I Looked For and Did Not Find

An inward rounding anywhere in the integer forms (there is no rounding: every comparison
is a cross-multiplication with positive denominators); a float that decides anything
(the one float, the sort key, is confirmed exactly); an open comparison where the
reviewed version had a closed one (the facet test, the live-edge range, the section
merge and the slab endpoints are all closed); a probe set that could miss a slab (events
are sorted exactly and `between` is strictly inside); a memo keyed on object identity
alone or on a mutable value (the cover memo is keyed on identity *and* the published
lists, and `Row.residual` has no writer after construction); a cache that outlives its
inputs (the partner’s step replaces its rows); a change to the `--sample` protocol or to
what a sampled run claims (none; the receipt still says `sample`); any weakening of the
degenerate-row branch (unchanged).

## 3. The Branch-and-Bound Verifier

### 3.1 What Changed

`git diff 55656158 ff5471e89`: `cos_sin` becomes a call to `cos_sin_bits(t, KBITS)`, the
same series at the same 160 bits with the scale parameterised; `check_trig` retries a
failed enclosure at `PRECISE_BITS = 2400`; `planes_of_piece` returns five-tuples
`(nx, ny, r, c, o)` whose last two fields (the chord factor and the offset of X3) the v1
path never reads (`row_of` passes `plane[:3]` to `plane_box_min`; the closed-pair and
pair-split checks test only whether the plane list is empty); `row_of` dispatches a
`["w", t]` reference to `wall_row` and an eight-field cut to `taylor_cut_row`, both of
which refuse unless `header.settings.taylor` is true; `combination_min` and
`check_bounds` gain the $k$ angle-offset columns only when `self.taylor` is set; the
header check requires the manifest’s schema to be v1 without the Taylor setting and v2
with it, and $K \ge \sqrt2/4$ by $16K^2 \ge 2$; `parsed_cut` refuses a cut with any
field count but four or eight; `prepared` derives `centres_q` and `offsets_q` from a
node’s `taylor` record when present.

### 3.2 The Interval Path Is Unchanged in Effect

For a v1 certificate the values the verifier computes are the reviewed ones: the
enclosures (same series, same scale; the retry runs only after a failure and only makes
the check more permissive, see 3.3), the planes’ first three fields (`base = g_lo * c`
with $c = 1$ or $1 - x^2/2$ is the reviewed `g_lo` and chord; the wide-piece $r$ is the
reviewed $g_{lo} - 2\tau(S + \tau D) - \varepsilon E$ computed as `g_lo - offset`), the
cut minimum, the Farkas and bound combinations over $2k$ columns, and the box
inheritance. Three refusals are new: a v1 manifest whose `schema` is not
`n17-subpattern-bb-certificate/v1` (the reviewed verifier never read the schema), a cut
with a field count other than four or eight (the reviewed verifier read four fields and
ignored the rest), and a `["w", t]` reference in an interval certificate (the reviewed
verifier would have read it as a cut index).
None can turn a refusal into a pass.

**Agreement on A.** Both verifiers on the admitted A certificate with
`--sample 50 --deepest 20 --trig-sample 100 --seed 7` (`a-old-sample.json`,
`a-new-sample.json`; the node choice is seeded and the choosing code is unchanged, so
the same 1,225 nodes are checked): both PASS with no node failure; 41,598 nodes, 21,215
closed leaves (10,032 disc, 4,504 lp, 6,679 pair), depth 31; identical counts: 51,793
cuts, 21,581 bound tightenings, 54 Farkas, 34 disc and 32 pair closures, 844 angle and
261 pair splits, 100 enclosures; 103 s against 114 s. The verifier was not rewritten for
speed and is not faster.

### 3.3 The 2,400-Bit Retry Cannot Accept an Enclosure That Excludes the Truth

`check_trig` accepts a recorded enclosure $[c_{lo}, c_{hi}] \times [s_{lo}, s_{hi}]$
when this module’s own enclosure fits inside it; the retry recomputes the module’s
enclosure at 2,400 bits and asks the same question.
`cos_sin_bits` sums the Taylor terms $t^n/n!$ as integer intervals scaled by
$2^{\text{bits}}$, stops when the next term’s magnitude is below two units, and widens
both results by that magnitude plus one unit; since every derivative of cosine and sine
is bounded by one, the Lagrange remainder of the degree-$(n-1)$ polynomial is at most
$|t|^n/n!$, so the result is a valid enclosure at any precision.
A valid enclosure inside the recorded one puts the true value inside the recorded one,
which is what every later check needs; a tighter valid enclosure only makes the
containment test more permissive among recorded enclosures that *do* contain the truth.
A recorded enclosure that excludes the true value contains no valid enclosure at any
precision and is refused after the retry as before.
The recorded normal must still lie inside the recorded enclosure.

**Evidence.** `bb_trig_retry.py.txt` (log `bb-trig-retry.log`) makes the committed
tests’ crowded-row certificate (203 nodes, 116 enclosures, interval mode) and rewrites
the middle entry of its enclosure table four ways, re-hashing the table and the
manifest:

| Enclosure recorded at $t = 2.1671…$ | Reviewed `4a93c74c` | New `9ca8df6f` |
| --- | --- | --- |
| as written by the pilot | PASS | PASS |
| this module’s own 400-bit enclosure: narrower than 160 bits, contains the true value | FAIL (its 160-bit enclosure does not fit) | PASS, through the retry |
| the 400-bit enclosure shifted by $2^{-300}$: excludes the true value | FAIL | FAIL |
| the written enclosure shifted by twice its width: excludes the true value | FAIL | FAIL |

The one new acceptance is of an enclosure that contains the true value, which is the
only property the later checks use.

### 3.4 The Taylor Checks X1 to X5

The LP of a v2 node has columns $x_s, y_s$ and the offsets $t_s = \theta_s - c_s$ over
$T_s = [lo_s - c_s, hi_s - c_s]$, with the centres $c_s$ read from the node and the
ranges derived by the verifier (`prepared`); the expansion is valid about any point with
$\rho = \max |t|$, so a centre outside its interval costs accuracy, not soundness.

- **X2, gap lines.** For a pair $(i, j)$ and signs $s_1, s_2 \in \{\pm1\}$, let
  $f(\alpha) = (s_1 \cos\alpha + s_2 \sin\alpha)/2$; then $h(\alpha) = (|\cos\alpha| +
  |\sin\alpha|)/2 \ge f(\alpha)$ and
  $g = \tfrac12 + h(\theta_j - \theta_i) \ge \tfrac12 +
  f(\alpha_0 + \tau)$ with $\alpha_0 = c_j - c_i$ and $\tau = t_j - t_i \in A$,
  $|\tau| \le
  \rho$. Taylor’s theorem with $f'' = -f$, $|f''| \le \sqrt2/2$, gives
  $f(\alpha_0 + \tau)
  \ge f(\alpha_0) + f'(\alpha_0)\tau - (\sqrt2/4)\tau^2$, and
  $f'(\alpha_0)\tau \ge b\tau -
  |f'(\alpha_0) - b|\rho$ for any slope $b$. `line_constant` (line 648) bounds
  $f(\alpha_0)$ below from the enclosure of $\cos\alpha_0, \sin\alpha_0$ with the signs
  applied, bounds $|f' - b|$ above by `spread = max(d_hi - b, b - d_lo)` with
  $f' = (s_2\cos -
  s_1\sin)/2$ enclosed, and subtracts $K\rho^2$ with $K \ge \sqrt2/4$ (checked at the
  header). So $g \ge a + b\tau$ with $a$ recomputed here, never read from the record.
- **X3, planes at the pose’s own gap.** The reviewed lemma gives $n(\phi) \cdot d \ge g$
  at an end angle or $n(m) \cdot d \ge g\cos x \ge g(1 - x^2/2)$ at the chord, and the
  float normal is within $\varepsilon$ of the true one componentwise, so $\bar n \cdot d
  \ge c\,g - o$ with $(c, o) = (1, \varepsilon E)$ or $(1 - x^2/2, \varepsilon E)$; for
  a wide piece the reviewed bound $n(m) \cdot d \ge g - 2\tau(S + \tau D)$ gives $(1,
  2\tau(S + \tau D) + \varepsilon E)$. These are the fields `planes_of_piece` records.
  Since $c > 0$, $r = c\,g_{lo} - o$ remains a valid lower bound and the possibility
  filter is unchanged.
- **X4, Taylor cuts.** A cut $u \cdot d - w\tau \ge v$ is valid when
  $v \le \min\{u \cdot
  d - w\tau : d \in \text{d-box},\ \tau \in A,\ \bar n \cdot d \ge c(a + b\tau) - o\}$
  over every possible plane, because the pose’s own plane satisfies
  $\bar n \cdot d \ge c\,g -
  o \ge c(a + b\tau) - o$ by X2 and X3. `taylor_plane_min` (line 945) bounds each such
  minimum below by the Lagrangian $\max_{\lambda \ge 0}\big[\min_{\text{boxes}} (u -
  \lambda\bar n) \cdot d + (\lambda c b - w)\tau + \lambda(ca - o)\big]$ over
  $\lambda = 0$ and the three multipliers that cancel a coefficient; weak duality makes
  every candidate a valid lower bound whether or not the region is nonempty, and the
  committed `test_the_exact_taylor_bound_is_the_lp_value` shows the maximum reaching the
  LP value on a hand-solved instance.
  The row returned, $(u, -u, -w, w)$ on the four centre columns and the two offset
  columns with right side $-v$, is the cut.
- **X5, wall rows.** $x_s \ge h(\theta_s) \ge f(c_s + t_s) \ge a + b t_s$ with $a$
  bounded by `line_constant` at $c_s$ and $\rho_s$; `wall_row` refuses a recorded $a$
  above that bound and returns $-x_s + b t_s \le -a$ for side $+1$ and
  $x_s + b t_s \le U - a$ for side $-1$ (the field order `[s, axis, side, s1, s2, b, a]`
  matches the pilot’s `taylor_ref`).
- **X1, the combinations.** `combination_min` minimises each offset column over
  `offsets_q`; bounds (C4) tighten centre columns only, and a bound on an offset column
  would index past the boxes and be reported as malformed.

**Evidence.** The committed `tests/test_verify_n17_bb_taylor.py` passes two Taylor
certificates (a crowded row in the open and one against the west wall, with wall rows
referenced) and refuses nine doctored kinds: a cut’s $v$ raised by $10^{-6}$, its slope
$b$ changed, a sign flipped, a centre moved by $1/10$, the centres removed, a wall’s $a$
raised by $10^{-6}$, $K = 1/4$, an interval claim on a Taylor certificate, and a v1
schema on a v2 certificate.
Those 12 tests and the 23 of `tests/test_verify_n17_certificates.py` pass at `HEAD`
(`bb-tests.log`, 35 passed in 24 s), the kernel verifier’s twelve among them.

## 4. Bottom Line

The kernel verifier `5c550f7c…` is sound: the rewrite changes how three quantities are
computed and not what is required of a certificate, the new computations are exact by
argument and by measurement against the reviewed ones, and the memos cannot return a
result for an input they were not computed for.
It re-proves the admitted W7 certificate with the admitted counts in 184 seconds, and
the two verifiers agree row for row on the W7 and N1 samples.
The three test additions of section 2.8 are in, they change no byte of the verifier, and
each mutant they were written for now fails a committed test; I judged them a condition
of listing the digest rather than a follow-up, because the committed suite is what
stands between this review and the next rewrite, and as it stood it did not see a
dropped quantifier in the collision loop or a sweep that probes only at events.
With them in, admit it.

The branch-and-bound verifier `9ca8df6f…` is sound for interval-mode certificates, with
three new refusals and no new acceptance on that path, and its Taylor path is sound as
far as reading and the committed tests establish.
Admit it; a Taylor certificate, if one is ever put forward, needs its own full
verification and review as A’s did.

Three non-blocking follow-ups for the kernel verifier: the one-line guard on a one-point
target in `section_covered`; a comment at `covered_by_sweep` stating that regions must
be convex and in hull order; and a doctored closure with a stale relabelled cover for
`cache-cover-survives-restep`.

## 5. Addendum (2026-10-03): Adaptive Rows, Digest `64474e45`

**Reviewed:** `packing/devtools/verify_n17_kernel_certificate.py` at lane P2’s worktree
`9d3cb521b` (SHA-256 `64474e45…`), which is the admitted `5c550f7c…` plus the verifier
hunk of `p2-adaptive-final.patch` (+47 −10; applying that hunk to `5c550f7c` gives
`64474e45` byte for byte).
**Materials:** P2’s patch, worktree, receipts, mutants and lane K2’s two refined
closures under the session scratchpad `lanes/p2-refine/`; my scripts, receipts and logs
under `audit-verifier-rewrites/refinement/` (`mutate_refined.py.txt`,
`run_refinement_mutants_r6.py.txt`, the `64474e45` module retained as `.py.txt`, `w7-*`,
`n1-*`, `doctored-*`, `refinement-mutants-r6*`, `worktree-tests.log`). The verifier
still imports nothing beyond the standard library and the cover tool, and nothing from
`gmpy2`, onto which the producer and checker moved at `c401c81d6`; the arithmetic
diversity of section 2.4 is kept.

**Verdict: ADMIT WITH CONDITIONS.** Refined rows cannot be accepted unsoundly: the rows
of a step must partition $[0, 1]$ exactly, each must cite by reference an accepted row
of the owner that contains it, and every obligation of a row (its legal box, its strict
core, its required domain, its cover) is taken over the row’s own interval, as every
obligation of a partner row is.
Uniform certificates are verified exactly as before, with identical counts and an
identical sample draw.
The conditions are, as in section 2.8, test additions: the committed suite (42 tests in
P2’s worktree, all passing) misses five weakening mutants that only this review’s
doctored refinements catch, and the minimal test for each is given below.

### 5.1 What Changed

`predecessors(accepted, rows, si)` replaces the positional check
`(lo, hi) == prior.interval == (ri/bins, (ri+1)/bins)` and the dict comparison of
`prior_reference`. It requires the step’s rows to be a nonempty list whose intervals
start at 0, each at the previous one’s end, each with $lo < hi \le 1$, the last ending
at 1; builds a map from the canonical JSON of each accepted row’s reference to that row,
refusing duplicates; and for each row takes the accepted row its `prior_reference`
names, refusing a missing one and a row whose interval leaves its predecessor’s.
`check_step` then uses that predecessor where it used the positional one, and
`verify_objects` draws the full set and the sample from the step’s own row count.
Nothing else moved: the required domain is still `prior.outer` cut by
`wall_box(lo, hi)`, the core is still proved strict over `(lo, hi)`, the row’s reference
must still be `{phase3, node, step, row index}`, partner covers are still admitted per
accepted row with `len(items) == len(rows)`, matching references and intervals and a
strict core over the partner row’s own interval, the kernel is still held to every row’s
planes, the closure is still derived over every accepted row, and the seed is still
required uniform.

### 5.2 Why a Refined Row Cannot Be Accepted Unsoundly

- **Partition.** The cursor starts at 0 and each row must start exactly where the last
  ended, with positive length, and the last must end at 1: closed rows with no gap and
  no overlap (a shared endpoint lies in both rows, and both are proved).
  A gap would leave angles no row speaks for; the mutants `partition-gap-accepted`,
  `-overlap-accepted`, `-end-unchecked`, `empty-row-allowed` and my
  `partition-start-unchecked` each remove one of these and each is caught (5.4).
- **Predecessor by reference.** Accepted references are unique by construction (each was
  required equal to the verifier’s own expected dict, with the row index, or to the
  seed’s), so the duplicate check is redundant, as P2 says of the one equivalent mutant;
  canonical-JSON equality is at least as strict as dict equality (it tells `1` from
  `True`). A citation of another owner’s row, of a replaced row (the grandparent), of
  the row itself or of nothing is refused.
- **Containment and uniqueness.** The accepted rows partition $[0, 1]$ by induction (the
  seed is uniform and every step’s rows are proved a partition), so a row of positive
  length lies inside exactly one accepted row; the citation must name that one, a row
  can never span two accepted rows (no coarsening), and the natural order of citations
  is forced.
- **The row’s own interval.** The required domain is the predecessor’s outer domain,
  which contains every centre the owner can have at the predecessor’s angles and so at
  the row’s, cut by the legal box of $[lo, hi]$, valid on the whole row by the concavity
  argument of `wall_box`; the core is proved strict over $[lo, hi]$; the cover is
  decided on that required domain.
  P2’s mutants `box-of-the-predecessor`, `box-not-cut` and `box-of-the-upper-half` and
  my four half-interval core mutants probe this, and
  `test_a_refined_row_is_held_to_its_own_legal_box` shows the wall closure has rows
  whose cover reaches only their own box, so the box of the row’s own interval is what
  the pass depends on.
- **Partner covers of variable length.** `check_partners` is unchanged: one item per
  accepted row of the partner, in order, with the row’s reference and interval, dead
  rows empty, a cover with no live row refused, and the admitted cover memoised on the
  accepted `Row` object, which the partner’s own step replaces.
  My doctored covers with a missing last item, two items swapped, or an item’s interval
  widened to the parent’s are refused (“cover length”, “reference”, “interval”).
- **The sample draw.** The sample is drawn from `range(count)` per step and the closure
  step is always checked in full; for a uniform certificate `count == bins` and the
  generator consumes the same numbers, so the draw is the one `5c550f7c` made: the
  sampled W7 and N1 receipts below carry its counts exactly.
- **No refined certificate was ever admissible before.** The reviewed `5c550f7c` refuses
  both of K2’s refined closures at “step 4 row 0: interval” (`blind-5c550f7c.json`,
  `wall-5c550f7c.json`).

### 5.3 Evidence

| Run | `5c550f7c` | `64474e45` |
| --- | --- | --- |
| W7 full (`w7-full-64474e45.json`) | PASS, 184 s | PASS, 291 s; counts and closure identical (30,952,184 inequalities, 7,752 regions, 3,324 rows, 19,282 partner rows) |
| W7 `--sample 4 --sample-seed 12345` | PASS, 76 s | PASS, 109 s; the same 270 rows, 596 regions, 2,076,688 inequalities |
| N1 `--sample 1 --sample-seed 12345` | PASS, 117 s | PASS, 171 s; the same 113 rows, 400 regions, 669,668 inequalities |
| K2’s refined blind closure (2 bins; rows per step 2, 2, 2, 2, 4, 4, 8) | FAIL at “step 4 row 0: interval” | PASS: 24 rows in full, 24 regions, 2,416 inequalities, 18 partner rows, closure owner 0 step 6 |
| K2’s refined wall closure (2 bins; 2, 2, 2, 2, 4, 4, 4, 4, 5) | FAIL likewise | PASS: 21 rows in full, 21 regions, 1,500 inequalities, 16 partner rows, closure owner 0 step 8 |

P2’s own full receipts (`w7-full-64474e45.json`, `n1-full-64474e45.json` in the
materials) agree with the admitted counts on both uniform certificates, N1 in full
(2,611 rows, 16,709,184 inequalities).

**Doctored refinements** (`doctored-{blind,wall}-64474e45.log`), beyond P2’s nine
committed ones: a closing step whose first row starts at $2^{-20}$ (“interval gap”) or
whose last row ends at $1 - 2^{-20}$ (“do not reach the end”); a reversed interval; a
row citing itself (“not an accepted row”); a split’s second child ending $2^{-30}$ past
its parent with the next row moved to meet it, so only containment can refuse (“escapes
its predecessor”); both children claiming the parent’s whole interval (“overlap”); the
three partner-cover edits above; a refined row’s core, and a refined partner row’s core,
scaled until strict over one half of the row only (“core not strict”); and the same two
cores grown by a single point found by search that is strict over one half of the row
and not the other, which leaves every other obligation of the row intact.
All 15 applicable mutations are refused at the intended check on both closures; the two
scaled lower-half forms are not applicable because strictness binds at the low end on
these closures, which is why the grown-point form was added.

### 5.4 Mutants

`run_refinement_mutants_r6.py.txt` reproduces P2’s thirteen mutants and adds seven, each
against P2’s selection of the worktree’s committed tests and against the doctored
refinements on both closures (`refinement-mutants-r6.log`, `-core-strict.log`).

| Mutant | Committed tests | Doctored refinements |
| --- | --- | --- |
| P2’s twelve weakening mutants (partition gap, overlap, end; containment skipped, lower end only; positional fallback, by containment; box of the predecessor, not cut, upper half; full mode and sample on the seed grid; empty row) | caught, 1 to 4 tests each, as P2 reports | five also caught here; the box mutants refuse the sound wall closure |
| `duplicate-accepted-unchecked` | missed: equivalent, see 5.2 | missed |
| `partition-start-unchecked` (the cursor starts at the first row’s own start) | **missed** | caught: `partition-starts-above-zero` accepted on the blind closure |
| `containment-upper-end-only` | caught (`cite_the_next_parent`) | missed |
| `core-strict-lower-half`, `core-strict-upper-half` (the owner’s core proved over half its row) | **missed** | caught: the grown-point and (upper) scaled cores accepted |
| `partner-core-strict-lower-half`, `-upper-half` | **missed** | caught likewise |
| `core-strict-predecessor-interval` (stricter) | nine tests fail: it refuses sound refined rows, never accepts more | refuses both sound closures |

**Conditions: five test additions,** for the mutants the committed suite misses.
All are edits in the style of `test_the_kernel_verifier_refuses_a_doctored_refinement`,
on the blind pair P2’s tests already produce, expecting the message named; the
procedures are in `mutate_refined.py.txt`.

1. `partition-start-unchecked`: set the closing step’s first row’s `interval[0]` to
   `"1/1048576"`; expect “interval gap” (`start_above_zero`).
2. `core-strict-lower-half` and `core-strict-upper-half`: take a refined row (one whose
   interval is narrower than its cited predecessor’s), find by the search in
   `point_strict_on_one_half` a point strict over the row’s lower (upper) half but not
   over the whole row, replace the core by the hull of the old core and that point, and
   recompute `common_core_halfplanes` from the new core and the row’s residual vertices;
   expect “core not strict”.
   Growing rather than replacing keeps every other obligation of the row satisfied, so a
   half-interval verifier accepts the certificate.
3. `partner-core-strict-lower-half` and `-upper-half`: the same point grown into a
   refined partner row’s published `core`; expect “core not strict”.

The four core mutants are on a line `5c550f7c` already had, so they are not a defect of
the patch; they matter now because “every obligation uses the row’s own interval” is one
of the facts the refinement rests on, and a row’s interval is now whatever the
certificate says it is.
The conditions change no byte of the verifier.

**Conditions made.** At the coordinator’s request the five tests are written, as five
more entries of `test_the_kernel_verifier_refuses_a_doctored_refinement` on the blind
pair (`start_above_zero`, and `grow_core_by_a_half_strict_point` and
`grow_partner_core_by_a_half_strict_point` for each half, with
`point_strict_on_one_half` as the search), in `refinement/r6-condition-tests.patch`
against `575795e02`; each runs in under a second here, and no test asserts a digest.
The whole file passes on the unmutated verifier (47 tests,
`worktree-tests-with-conditions.log`), and against the extended file every one of the
twenty mutants fails at least one committed test except the equivalent
`duplicate-accepted-unchecked` (`refinement-mutants-after-tests.log`): the five that
were missed now fail exactly the test written for each.

### 5.5 The Row Count

The verifier caps nothing: `predecessors` accepts any nonempty partition.
That has no bearing on soundness, since every row of every step is proved in full mode
and the closure step is proved in full in sample mode; it bears on cost, which grows
with the rows, and on sample mode, whose fixed `sample` rows per step cover a shrinking
share of a step as rows multiply, which is why a sampled run remains a planning check.
Two things worth doing: report the total and the largest per-step row count in the
receipt’s `counts`, so a refined certificate’s shape is visible in the ledger, and keep
the producer’s `max_rows` as the practical ceiling.
No change to the verifier is needed.

## 6. Addendum (2026-10-03): Closed Coverage of Points and Segments

**Reviewer:** Session 168, lane V1 (soundness).
**Reviewed:** the kernel verifier at `25c1cdef6`, the revision the ledger lists last,
and `packing/src/sqpack/hull_kernel/sweep.py`, against finding C2 of the n11 adversarial
review (`review-2026-10-03-n11-gpt6-pro-review-integration.md`): the n11 slice predicate
`covers_vertical` accepts a one-point target from a span that ends below it, 616 false
acceptances in a 12,180-case control.
The corrected reference is `packing/devtools/n11_closed_interval_cover.py`. The n17
kernel’s sweep is a copy of that routine, and the verifier’s merge was written after it,
so both were checked for the same class of defect.
**Materials:** `audit-verifier-rewrites/cover-soundness/`, with scripts retained as
`.py.txt`.

**Verdict.** Both n17 copies had the defect class, in three places.
None of the three can have changed an admitted result: on W7, SW9 and N1 the defective
branches were never taken, and the closure argument of 6.2 shows that two of them cannot
change any sweep verdict on a domain of positive area.
All three are fixed, 23 new tests hold the fixes, and the fixed verifier passes all
three certificates in full with their admitted counts (6.5).

### 6.1 The Three Defects

1. **The verifier’s merge (`section_covered`)** ended with `return not ratio_lt(cursor,
   high)`. A one-point target $[a, a]$ with no span at all, or with every span ending
   below $a$ (the merge skips those), fell through to `True`. Section 2.2 recorded this
   as a quirk that the sweep makes harmless.
   It is in every revision from F2’s `e0b66f07b` on; R3’s `556561586` decided coverage
   by area subtraction, which has no one-point case.
2. **The verifier’s zero-area branch (`check_cover`).** A required domain of zero area
   (a point or a segment) was checked only at its listed points and, for a two-point
   segment, its midpoint, each inside a polygon region or equal to a residual vertex.
   Covering the ends and the midpoint does not cover the segment.
   This branch is in every listed kernel revision, `556561586` included.
3. **The kernel’s `sweep.covers_vertical`** was the n11 routine verbatim, without the
   skip of spans below the cursor, so it accepted $[1, 1]$ from $[0, 0]$. The compiled
   form used by the fast and indexed covers (`covers.covers_vertical_compiled`) already
   skips them.

### 6.2 Whether Any Admitted Result Is Affected

**Argument, for defects 1 and 3.** Both are reached only through a sweep over a domain
of positive area: `covered_by_sweep` from the positive-area branch of `check_cover`, and
`exact_union_cover`, which refuses any other domain.
In a convex domain of positive area a vertical section is a single point only at the
leftmost or rightmost abscissa.
The open slab beside it is probed at an interior abscissa, where the section has
positive length and both forms of the merge decide exactly.
If that slab is covered, the extreme point is a limit of covered points, and a finite
union of closed regions contains its limits, so some region’s span contains the point
and the corrected merge accepts it too.
Accept and refuse therefore never differ between the two forms; only the abscissa a
refusal names can move, from the slab to the extreme itself.
Defect 2 has no such defense: a zero-area branch that passes says nothing about the
segment between its sample points.

**Measured.** The unfixed verifier (`25c1cdef6`, blob `ea1c7104…` in each record) was
run in full on each certificate with its `section_covered` and `check_cover` wrapped by
counters that delegate to the originals (`count_cover_paths.py.txt`,
`count-unfixed-*.json`). Each run passed.

| Certificate | Cover checks | Zero-area rows | Sections merged | One-point sections | Of those, no containing span | Seconds |
| --- | --- | --- | --- | --- | --- | --- |
| W7 | 3,324 | 0 | 626,236 | 1,240 | 0 | 235 |
| SW9 (`flag3-a9-pending`) | 3,359 | 0 | 554,193 | 1,368 | 0 | 215 |
| N1 (`N1-state-pending`) | 2,611 | 0 | 834,715 | 564 | 0 | 390 |

Neither defective branch was taken: no zero-area required domain occurs, and each of the
3,172 one-point sections had a span containing it.

**The kernel’s checker path.** `check_n17_subpattern --check-saved` sends a
positive-area row to `--cover indexed` by default, whose compiled merge skips spans
below the cursor, and a zero-area row to `closed_degenerate_cover`, which covers the
parameter interval $[0, 1]$ and so never has a one-point target.
The capture pilot calls the same row check with `cover="indexed"`. The defective
`sweep.covers_vertical` is on neither path; it serves the `reference` backend,
`node.check_row` and the n11 counting replay.
The rows’ published `input_domain` (`count_input_domains.py.txt`, `input-domains.log`)
gives the same split as the verifier: positive area on 3,324, 3,359 and 2,611 rows,
empty on 388, 3,920 and 13, zero area on none.
The kernel’s degenerate cover never ran on these certificates either.

**The counters are sensitive.** On the forged closures of 6.4
(`forged-instrument-check.log`) they report the zero-area row, which the kernel’s exact
cover refuses while the unfixed verifier passes the closure, and the one-point section
with no containing span, which the unfixed merge lets through before refusing at
$x = 22/21$.

### 6.3 The Fixes

**Verifier.**

- `section_covered` returns `False` after the loop, so `True` follows only a span that
  contains the cursor; a one-point target needs a span containing it.
  It also refuses, with `malformed coverage interval`, any target or span that is not
  two `int` `(numerator, denominator)` pairs with positive denominators and low end not
  above high end (`well_formed`). Every caller builds well-formed intervals, so this
  guard changes no verdict on a real certificate.
  A benchmark of 20 spans per call puts its cost near 5 s on a W7 run.
- The zero-area branch calls `degenerate_covered`. The domain is $P + t(R - P)$,
  $t \in [0, 1]$, between the ends of its hull.
  Each region, whether polygon, segment or point, is the closed hull of its vertices
  written as half-planes (`closed_planes`), and each half-plane bounds $t$ exactly.
  The resulting closed parameter intervals must cover $[0, 1]$, which `section_covered`
  decides. It is written from the verifier’s own `hull` and `planes_of` and imports
  nothing new; the import test still passes.
  A counter, `degenerate_cover_checks`, enters a receipt only when such a row is
  checked, so the three receipts keep their counts.

**Kernel.**

- `covers_vertical` skips a span wholly below its cursor, as the compiled form does.
- `vertical_interval` refuses an ordinate that is not an exact rational (`mpq`, its
  integer type, `Fraction` or `int`). A float coordinate turns `mpq` arithmetic into
  `mpfr`, and a NaN would slip through `min` and `max`. This is the n11 contract’s
  refusal of malformed endpoints, for a routine that takes polygons.
- **Every certificate is unchanged.** The closure argument of 6.2 makes the verdict of
  `exact_union_cover` the same for every input of exact rationals.
  The routine’s callers consume only that verdict and its event and probe counts, which
  the change does not touch, and the producer’s path uses the indexed cover.
  The blind-pair digest tests in `test_hull_kernel_octagon.py`, the mask-0 and case-2095
  full replays and the sequential tests all pass with the change: 137 tests over the
  `test_hull_kernel_*` files, `test_verify_n17_certificates.py` and
  `test_n11_closed_interval_cover.py`, in 129 s.

### 6.4 Tests

Seventeen tests in `test_verify_n17_certificates.py` and six in
`test_hull_kernel_primitives.py`:

- **The review’s 12,180 cases** (every target and every family of at most two of the 28
  closed intervals with integer ends in −3..3), for the verifier’s merge and for the
  sweep’s slice through polygons whose section at $x = 0$ is each interval: both agree
  with the corrected reference on every case.
- **The acceptance cases:** $[1,1]$ is refused from $[0,0]$ and from no span; a covered
  one-point target, a closed seam and a containing span are accepted; a gap of
  $10^{-50}$ at either end or at the seam is refused.
  Twelve malformed intervals are refused by the merge, and a float, a NaN and a `bool`
  coordinate by the sweep.
- **The review’s triangle**, whose section at $x = 0$ is the vertex $(0, 1)$, above its
  only region: the corrected sweep refuses at $x = 0$, the frozen n11 sweep at
  $x = 1/2$, and the fast and indexed covers at $x = 0$.
- **`degenerate_covered`** on a segment and a point against polygons, collinear
  segments, a crossing segment and points, with seams, gaps of $2^{-50}$, and boxes
  about the segment’s ends and midpoint that do not cover the rest of it.
- **Two forged one-row closures** (`forged_closure`): owner 0 claims every pose of its
  single row forbidden, with no residual and no collision region, so the cover alone
  decides. In the first, the cell meets the legal box in the segment from $(1/2, 3/4)$ to
  $(1/2, 5/4)$, and squares of half-side $1/16$ about its ends and midpoint leave
  $(13/16, 15/16)$ and $(17/16, 19/16)$ uncovered: refused as `degenerate row
  uncovered`, and passed with half-side $1/8$, where the squares meet at closed seams.
  In the second, a wedge’s leftmost vertex $(1, 1)$ has only the span $[1/4, 3/4]$ below
  it: refused at `x=1`, and passed when the covering square is moved so that its edge
  holds the vertex.
- **The kernel’s degenerate cover** refusing boxes about a segment’s ends and midpoint
  and accepting wider ones: a control on a routine that was already right.

**Against the unfixed code** (`run_cover_mutants.py.txt`, `v1_unfixed_plugin.py.txt`,
`cover-mutants.log`), each run installing one form in place of the fixed one:

| Form installed | New tests that fail |
| --- | --- |
| None (the fixed files) | none of 23 |
| The unfixed verifier (`25c1cdef6`) | all 17 verifier tests |
| Merge falls through on a one-point target | 3: the 12,180 cases, the acceptance cases, the wedge closure |
| Zero-area branch by points and midpoint | 1: the segment closure, which the unfixed branch passes |
| Merge without the interval check | the 12 malformed intervals |
| The unfixed sweep (`f864a576a`) | 5 of the 6 kernel tests, all but the degenerate-cover control |
| Slice without the skip | 2: the 12,180 cases, the triangle |
| Slice without the exact-ordinate check | the 3 inexact coordinates |

### 6.5 Re-Verification With the Fixed Verifier

The fixed verifier’s own command, in full mode, one certificate at a time on a shared
machine with a load average of 5 to 8 (`full-fixed-*.json`, `full-fixed-*.log`):

| Certificate | Status | Seconds | Against the admitted receipts |
| --- | --- | --- | --- |
| W7 | PASS | 260 | counts, closure (owner 5, step 57) and content ids equal to `verification.json` and `verification-5c550f7c.json` (242 s); 30,952,184 inequalities, 3,324 rows |
| SW9 (`flag3-a9-pending`) | PASS | 199 | equal to `verification.json` (351 s); closure owner 5, step 101; 28,321,424 inequalities, 3,359 rows |
| N1 (`N1-state-pending`) | PASS | 325 | equal to `verification.json` and `verification-5c550f7c.json` (315 s); closure owner 18, step 81; 16,709,184 inequalities, 2,611 rows |

No row of the three has a zero-area required domain, so no receipt gains the
`degenerate_cover_checks` counter.
The times are within the spread of the earlier runs under different load, and the
interval check’s estimated cost of about 5 s on W7 is below that spread.

### 6.6 The Ledger

**The fixed verifier can be listed.** Beyond what `25c1cdef6` re-derives, by the same
code, it has two exact checks that can only refuse: the merge’s containing-span rule
with its interval check, and the parameter cover of a zero-area row.
It passes W7, SW9 and N1 in full with their admitted counts (6.5). The 23 tests should
be committed with it, so that a later rewrite meets them, as section 2.8 asked of the
earlier conditions. The receipts in `cover-soundness/` were written in an uncommitted
worktree on `f864a576a`, so their provenance has `dirty: true` and names the module by
its blob, `859b6c56…`. A listing names the commit that carries this patch; these
receipts serve as its verification if the committed file has that blob, and otherwise a
full run at the commit does.

Every earlier listed kernel revision has defect 2, and those from `e0b66f07b` on also
have defect 1. Their receipts for W7, SW9 and N1 stand, by 6.2. For a new admission I
would accept only the fixed revision: an earlier revision’s pass on a certificate with a
zero-area row proves nothing about that row.
Whether to restrict the earlier listings to the entries they already verify is the
coordinator’s decision.

### 6.7 Elsewhere in the Class

The other interval merges in the n17 kernel and verifiers are exact:

- `covers.covers_vertical_compiled` skips spans below its cursor, and
  `covers.closed_degenerate_cover` covers the parameter interval $[0, 1]$, never a
  single point.
- The branch-and-bound verifier’s `check_pieces_cover` joins closed angle pieces that
  touch or overlap and asks one joined piece to contain each target, which is exact for
  a one-point target too.
- The capacity-one cover’s `_line_gap` merges toward the box side $[LO, HI]$, which has
  positive length, from cells that lie inside the box.
- The verifier’s `covered_by_sweep` and `covered_by_area` leave out regions with fewer
  than three hull vertices, which can only refuse more.

One gap is of completeness, not soundness: on a zero-area row the verifier refuses any
collision region, since `check_collisions` requires each region to have positive area.
A sound certificate whose producer put a collision region on such a row would be
refused. No such row occurs in W7, SW9 or N1.

## Evidence Status

| Kind | Items |
| --- | --- |
| Measured, this review | section 6: the counted runs of the unfixed verifier on W7, SW9 and N1, the published input domains, the forged closures, the 12,180-case enumerations, the mutants of 6.4, the 137 tests and the three full runs of the fixed verifier; section 5: the uniform runs under `64474e45`, the two refined closures under both verifiers, 17 doctored refinements, 21 mutants against the committed tests and the doctored refinements; sections 1 to 4: the facet, sweep, `between` and section audits; the W7 full run and the W7 and N1 sampled agreement runs; the 34 doctored certificates; the 21 verifier mutants against three checks; the extended test file against the five mutants it was written for; the blind-pair equivalence of the first-row-only mutant; the sampled agreement run on A; the four crafted enclosure tables; the 35 committed tests, now 39 |
| Read from code, this review | section 6: the closure argument of 6.2, the kernel checker’s cover dispatch and the other interval merges of 6.7; the diffs of both verifiers; the arguments of sections 2.1 to 2.3 and 3.2 to 3.4 |
| Taken from the record | the admitted W7 receipt and F2’s receipt; N1’s `check-saved.json`; A’s admitted receipt; the prior reviews’ line numbers and mutation lists |
| Not checked here | the kernel’s checker and producer (reviewed by R3); HiGHS and `mpmath` (nothing in either verifier depends on them); the Taylor producer’s floats (the verifier recomputes every Taylor quantity it uses) |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
