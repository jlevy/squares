# BC-255 Theorem 3 Source-Control Review

**GO for the exact-angle source control.** No blocking mathematical or implementation
finding was identified.
This is independent review under `think-2f79`, W7 pipeline-improvement phase 5,
2026-09-06, within the authorized `20:09:14–20:34:14 UTC` slice.
It does not accept a new theorem, H-036’s target, or an interval-angle instrument.

The author explicitly stopped all three assigned files at `20:11:40 UTC` before this
review’s executions.
I reviewed the
[implementation](../../../../../cases/stromquist/restricted_orientation.py),
[author tests](../../../../../tests/test_stromquist_restricted_orientation.py), and
[source-control report](bc-255-theorem3-source-control-slice-01.md).
Those files and the archived source were not changed.
The coordinator owns Git publication and acceptance.

## Mathematical Checks

I visually checked pages 9–11 of the
[archived primary PDF](../../../../../resources/papers/stromquist-2003-packing-10-or-11-unit-squares.pdf),
including Figure 13 and the full Theorem 3 coordinate list.
The four P10 seeds and all twelve P12 coordinates match the source at $s=2+(4/3)\sqrt2$.
In particular, $G=(4/5,s-2)$ and the three A-points are the Theorem 3 values, not the
earlier Theorem 2 repair.
The source defines boxes as interiors of squares with side strictly greater than one.

The seven output conclusions are the required ones: axis P10 coverage, 45° localization,
three separate A-point forcings, and P12 coverage separately at 0° and 45°. The replay
does not replace individual triple containments by a weaker simultaneous-failure test.

The exactness and completeness argument checks out:

- The field is the positive root of $x^2-2$ isolated in $(1,2)$. Equality uses reduced
  rational coefficients; nonzero signs use rational interval refinement.
  No float determines a geometric branch.
  The reviewer tests also compare signs with an independent rational squared-comparison
  oracle.
- At either permitted angle, containment gives the full closed center square
  $[h,s-h]^2$. Its projected polygon is intersected with every product of singleton
  events and intervening open intervals.
  Projected point coordinates plus or minus $1/2$ are all possible membership changes,
  so membership is constant on each product stratum.
  Domain-bound events close the enumeration.
- Closed convex clipping retains extreme points when intersections collapse to segments
  or points. For any strict defining linear inequality, the average of all retained
  vertices is strict exactly when some vertex is strict.
  Thus the same average satisfies all non-identically-tight strict inequalities
  simultaneously. This justifies both open-stratum reachability and the additional strict
  localization-failure constraints; checking only the original cell witness would not
  suffice.
- The reported dimensions are product-event dimensions.
  A center-domain vertex can lie inside an open event segment; the implementation
  retains that case and the author report explicitly distinguishes it from affine
  intersection dimension.
- P10 is invariant under horizontal and vertical reflections, the group $K_4$, not all
  of $D_4$. Within the center domain, the exception region is exactly $1\le x\le s-1$
  with $y\le1$ or $y\ge s-1$. Its complement is the union of the three strict regions
  actually checked. Normalization reflects the entire configuration, not one square
  independently.
- Every larger open source box contains its concentric closed unit square strictly
  inside. A P10-avoiding box therefore supplies a P10-avoiding closed unit square;
  localization and triple forcing give three interior P12 hits in the normalized box.
  Each of the other ten boxes requires a distinct interior P12 hit, but only nine points
  remain. Closed-unit boundary hits are consequently valid here.
  This argument yields the source’s strict-sublevel lower-bound implication, not
  exclusion of unit squares at equality.

## Adversarial Controls

The
[nine reviewer tests](../../../../../tests/test_stromquist_restricted_orientation_review.py)
are retained separately from the author’s seven tests.
They add:

- Rational sign comparisons, including a Pell pair with $p^2-2q^2=1$ after 25 exact
  recurrences. The tiny nonzero $p-q\sqrt2$ stays positive, while subtracting $1/p$ makes
  it negative; exact zero remains distinct.
- An independent power-basis spelling of the original coordinates and an explicit check
  that quarter-turning $(s/2,1)$ produces a point not in P10.
- A rotated empty-support control whose four domain vertices occur inside open event
  segments, a rotated singleton domain, and strict half-plane tests that distinguish
  feasible interiors from closure-only contacts.
- The explicit canonical center $(1+\sqrt2/3,3/4)$. Its closed unit square avoids P10
  and contains all three A-points.
  The open square of side $101/100$ at the same center also fits, avoids P10, and
  contains the triple.
  This is a nonvacuous source box, not an eleven-square packing.
- Three separate mutations, moving one A-point at a time to the far corner region.
  Each produces its named forced-A obstruction, passes the independent
  corner/determinant witness check, and leaves the other two forced-A conclusions true.
  The receipt correctly does not call these failed auxiliary statements counterexamples
  to the source’s strict-box theorem.

The unchanged source replay reports event-dimension counts `(280,526,247)` at 0° and
`(406,841,444)` at 45°. There are no axis P10 avoiders; at 45° six strata avoid P10 and
one meets the canonical rectangle.
All seven conclusions are true, the obstruction list is empty, and `theorem_acceptance`
remains false.

## Executions and Remaining Scope

These commands ran from `packing/` on the stable files with frozen Python 3.14 and no
network or dependency change:

```bash
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache UV_OFFLINE=1 /usr/bin/time -p uv run --frozen --all-extras --group dev python -m pytest -q tests/test_stromquist_restricted_orientation_review.py tests/test_stromquist_restricted_orientation.py --durations=5
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache UV_OFFLINE=1 /usr/bin/time -p uv run --frozen --all-extras --group dev python -m cases.stromquist.restricted_orientation
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache UV_OFFLINE=1 /usr/bin/time -p uv run --frozen --all-extras --group dev ruff check tests/test_stromquist_restricted_orientation_review.py
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache UV_OFFLINE=1 /usr/bin/time -p uv run --frozen --all-extras --group dev basedpyright tests/test_stromquist_restricted_orientation_review.py
```

| Check | Result | Process wall seconds | CPU seconds |
| --- | --- | ---: | ---: |
| Author and reviewer tests | 16 passed, no skips; pytest 8.34 seconds | 8.65 | 8.22 |
| Fixed source CLI | All seven conclusions true; complete receipt | 1.69 | 1.66 |
| Reviewer-test Ruff | Zero findings | 0.03 | 0.02 |
| Reviewer-test BasedPyright | Zero errors, warnings, or notes | 0.80 | 1.22 |

The slowest individual test took 1.92 seconds.
CPU is user plus system time from `/usr/bin/time -p`; these are shared-host single-run
development costs, not isolated performance comparisons or total review cost.

This review trusts the project’s exact field implementation after inspecting its
preconditions and sign path; it is not formal verification or a new independent
standalone checker. Finite adversarial tests support, but do not replace, the partition
and convexity argument above.
No unresolved source-control assumption requires a code change from this review.

The remaining boundary is substantive: exact checks at 0° and 45° say nothing uniform
over the ±0.25° neighborhoods, and the source side is not 3.878. An interval extension
still needs complete event-order changes, certified coefficient bounds, and all boundary
leaves. No target attempt, registry change, or theorem acceptance occurred.
The coordinator may integrate this source control and choose the next phase separately.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
