# BC-255 Theorem 3 Source Control: First Slice

Status: complete exact-angle source-control replay; independent review pending,
2026-09-06. All seven reported checks pass, with no obstruction.
This is a bounded source-control commission under the coordinator’s W7
pipeline-improvement phase 4 (correctness), for BC-255 / H-036 / H-102, child
`think-2kld`. The authorized author interval is `19:49:58–20:19:58 UTC`, followed by a
separately commissioned independent review.
The obligations below were recorded before the first test ran and are unchanged.
This result does not establish H-036’s perturbed-angle claim or accept a new theorem.

## Frozen Source-Control Obligations

Use only Stromquist’s original Theorem 3 coordinates at $s=2+(4/3)\sqrt2$ and
orientations exactly 0° and 45°, from the archived
[paper](../../../../../resources/papers/stromquist-2003-packing-10-or-11-unit-squares.md#45-degree-packings).
The earlier
[assessment](bc-255-restricted-angle-assessment.md#fixed-domain-and-complete-cases)
states the conditional mechanism; its proposed substitution of 3.878 and perturbed
angles is not part of this control.
The existing Theorem 2 repair and archived source remain unchanged.

For a closed unit square at angle $\theta$, test the complete center domain $[h,s-h]^2$,
where $h=(\cos\theta+\sin\theta)/2$. The ten source points are the distinct horizontal
and vertical reflections of the four Figure 13 seeds.
The twelve source points are exactly Theorem 3’s three A-points and B through J.

The required checks are:

1. Every axis-oriented closed unit square contains a ten-set point.
2. Every 45° closed unit square avoiding the ten-set has center in the four reflection
   images of $R=[1,s/2]\times[0,1]$.
3. Every such avoiding square with center in $R$ contains each of the three A-points.
   A failure for one A-point is sufficient; simultaneous failure is not required.
4. Every closed unit square in either orientation contains a twelve-set point.

The paper defines a box as the interior of a square of side strictly greater than one.
Its concentric closed unit square lies strictly inside it.
Therefore closed-unit coverage and forcing are sufficient source-control obligations;
their boundary hits count and become interior hits of the box.
A failed closed-unit strengthening is not automatically a counterexample to the paper’s
strict-box statement.
Any escape must be checked independently by square corners and oriented determinants,
with its exact side and boundary semantics stated.

## Pre-Execution Controls and Complete Partition

First test a side-one container, its only axis-oriented unit square, and marked point
$(1,1)$: the singleton center domain is covered by a boundary hit.
Then test side four with sole marked point $(2,2)$: a contained square centered at
$(1/2,1/2)$ is an independently verifiable escape.
Include an open-line stratum and endpoint control so a polygon routine cannot discard
lower-dimensional cases unnoticed.

At each exact angle, transform center coordinates to the square’s orthonormal frame.
The projected coordinates of all marked points, plus or minus $1/2$, are the complete
point-entry and exit events.
Include the center-domain bounding coordinates.
Partition each axis into singleton events and intervening open intervals, then take
their Cartesian products.
These products retain every open rectangle, open segment, and vertex, including
coincident events and containment contacts.
Point membership is constant on each product stratum.
Intersect relevant strata with the exact closed center-domain polygon; a vertex average
and strict stratum checks decide whether its relative interior is reached.
Apply the same exact clipping to the localization failure regions and the closed
canonical rectangle when needed.

The source control must finish all four obligations or retain its exact first
obstruction and the unchecked remainder.
The default entry point is `python -m cases.stromquist.restricted_orientation`, with no
target-side or angle option.
Tests and the source-control command run under frozen Python 3.14 through `uv`, with
`/usr/bin/time -p` for process wall and CPU costs.
No H-036 target, interval extension, packing search, new theorem acceptance, or shared
record mutation is authorized.

## Execution Record

The reusable [source replay](../../../../../cases/stromquist/restricted_orientation.py)
uses `sqpack.field.NumberField` with minimal polynomial $x^2-2$ and root interval
$(1,2)$. Its printed side is `poly[2,4/3]` in the basis $(1,\sqrt2)$. Geometry, sorting,
clipping, and signs are exact; no floating approximation determines membership,
feasibility, or a reported outcome.
The program constructs the ten-set from the four original seeds and their $K_4$
reflections, and copies all twelve Theorem 3 coordinates without modification.
It checks the distinct-point inventory counts ten and twelve.

The complete run reports:

| Exact orientation | Reachable event vertices | Reachable open event segments | Reachable open event rectangles | Ten-set-avoiding strata | Such strata meeting $R$ |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0° | 280 | 526 | 247 | 0 | 0 |
| 45° | 406 | 841 | 444 | 6 | 1 |

The dimension columns describe the product event stratum, not necessarily the affine
dimension of its intersection with the center domain.
Containment-only contacts inside a higher-dimensional event stratum are also retained.
The six avoiding strata and the one canonical stratum show that the 45° localization and
forced-triple checks are not vacuous.
These are counts from the replay, not a proposed estimate or a claim about perturbed
angles.

All seven checks returned true: axis ten-set cover, 45° localization, forced $A_1$,
forced $A_2$, forced $A_3$, and twelve-set cover separately at 0° and 45°. The
obstruction list is empty, `complete` is true, and `theorem_acceptance` is false.

### Completeness and Strict Boundaries

For each of the two orientations, the program projects all 22 labelled marked points.
It deduplicates every entry/exit coordinate within the center-domain bounds, keeps each
coordinate as a singleton, and keeps each intervening interval open.
Every center therefore belongs to exactly one product stratum, and every point’s closed
membership is constant on that stratum.
Coincident source points in the combined lists retain their separate labels while
coincident event lines are deduplicated.

Closed half-plane clipping intersects each product stratum’s closure with the exact
projected center-domain polygon.
It preserves degenerate segments and points.
The average of the retained vertices lies in the convex intersection.
For any strict defining linear inequality, the average is strict if at least one
retained vertex is strict; if all vertices are on its boundary, no feasible point can be
strict. Applying this to every open stratum edge decides whether the stratum itself is
reached, including lower-dimensional intersections.
No area threshold or numerical tolerance removes a cell.

The union of the four exception rectangles, within the container, is

$$
1\leq x\leq s-1,\qquad y\leq1\ \text{or}\ y\geq s-1.
$$

Its complement is exactly the union of $x<1$, $x>s-1$, and $1<y<s-1$. For each
ten-set-avoiding 45° stratum, the checker clips against each of those three regions and
enforces its strict inequalities after taking the vertex average.
All three intersections are empty.
It separately intersects with the closed canonical $R$, retaining its boundary, and
checks each A-point’s membership bit independently.
The canonical restriction uses the horizontal and vertical reflection group $K_4$;
quarter-turn symmetry of the ten-set is not assumed.

An open source box of any side greater than one contains its concentric closed unit
square strictly inside it, even when a marked point is on that unit square’s boundary.
If eleven disjoint boxes existed, at least one would avoid the ten-set.
The checked axis cover and localization put it in a reflected copy of $R$. Reflecting
the entire configuration into $R$ preserves the container, the ten-set, disjointness,
and the two allowed square orientations modulo quarter turns.
The forced triple then puts three distinct twelve-set points in that box’s interior.
The checked twelve-set cover gives every other box an interior point from the same set,
but only nine points remain for ten boxes.
This explains how the checked one-square obligations supply the source’s conditional
argument. Source-distinct review and the coordinator’s acceptance remain separate.

### Controls, Refusals, and Development Failures

The
[seven retained tests](../../../../../tests/test_stromquist_restricted_orientation.py)
pass with no skips. They retain the singleton boundary hit, the side-four escape at
$(1/2,1/2)$, and all 49 strata of that small escape control: 16 vertices, 24 segments,
and nine rectangles.
Closed clipping is checked on a segment and its endpoint, including rejection of the
endpoint when the stratum requires an open segment.
At a rotated control with an exact event crossing, projection masks agree with an
independent corner/determinant calculation on every reachable stratum.
The witness checker does not call the clipping or mask producer.
Every escape the reusable cover routine returns receives that direct check.

The open-square control distinguishes three facts at center $(1,1)$ in side two:
$(3/2,3/2)$ is in the closed unit square, is not in its interior, and is in the open
square of side $6/5$. Only the last open square is a source box.
Expected refusals cover four unsupported angle values, an empty rotated center domain, a
mixed-field point, failed corner containment, and a target-side command option.
The command refuses unknown arguments before constructing the source replay.

TDD began with an expected missing-module import failure, followed by a passing
singleton test. An initial rotated fixture had no reachable event vertex, so its
assertion that it tested all three dimensions failed; the fixture was corrected to place
an exact event crossing at the container center.
A later missing-entry-point import failed before the source replay was implemented.
The open-boundary and CLI-refusal tests also failed before those interfaces existed.
The CLI had initially ignored extra arguments and still run only the fixed source case;
it now rejects them.
No command used a different containing side or angle for the Theorem 3 replay.
Focused lint found line lengths and excess positional arguments; type checking found a
missing optional-value narrowing in the escape test.
All were corrected before the final checks.

### Commands and Measured Cost

Commands ran from `packing/` in the frozen Python 3.14 environment, offline, using an
existing cache and a non-login shell.
The initial traceback identified Python `3.14.7`. Times are `/usr/bin/time -p` process
results including `uv` startup; CPU is user plus system time.
They are single-run development costs on the shared host, not isolated performance
comparisons or estimates for H-036.

```bash
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache UV_OFFLINE=1 /usr/bin/time -p uv run --frozen --all-extras --group dev python -m pytest -q tests/test_stromquist_restricted_orientation.py
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache UV_OFFLINE=1 /usr/bin/time -p uv run --frozen --all-extras --group dev python -m cases.stromquist.restricted_orientation
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache UV_OFFLINE=1 /usr/bin/time -p uv run --frozen --all-extras --group dev ruff check cases/stromquist/restricted_orientation.py tests/test_stromquist_restricted_orientation.py
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache UV_OFFLINE=1 /usr/bin/time -p uv run --frozen --all-extras --group dev basedpyright cases/stromquist/restricted_orientation.py tests/test_stromquist_restricted_orientation.py
```

| Command/checkpoint | Result | Wall seconds | CPU seconds |
| --- | --- | ---: | ---: |
| Initial TDD run | Expected missing-module import failure | 0.87 | 0.38 |
| First singleton control | One test passed | 0.36 | 0.27 |
| First complete source-test run | Five tests passed, no skips | 1.88 | 1.84 |
| First source CLI replay | All seven source obligations passed | 2.01 | 1.77 |
| Final focused test suite | Seven tests passed, no skips; pytest reported 1.82 seconds | 2.03 | 1.95 |
| Final source CLI replay | Same complete receipt, no obstruction | 1.70 | 1.65 |
| Final Ruff check | All checks passed | 0.03 | 0.02 |
| Final BasedPyright check | Zero errors, warnings, and notes | 0.76 | 1.37 |

Intermediate runs, including the named TDD failures, are not included in the table’s
final-check rows. No sum of these rows is presented as total worker cost.
Peak memory, formatter cost, and reasoning CPU were not measured.
The coordinator owns active-time accounting and publication provenance.

## Remaining Obligations

The source-control replay is ready for independent review of its arithmetic, partition
completeness, boundary semantics, source transcription, and conditional counting step.
This author does not accept their own result.
Integration validation and publication belong to the coordinator.

No interval-angle instrument, order-change isolation, or uniform proof over H-036’s
unchanged angle neighborhoods has been built or priced.
Passing the two exact source angles does not certify any intervening or nearby angle,
and the source side is not the H-036 target side.
The earlier uniform-core transfer obstruction is unchanged.
No source lemma, theorem statement, archived coordinate, existing repaired-cover result,
or H-036 criterion was changed.
The only authored files are this report and the two linked implementation/test files;
there were no dependency, shared-record, bead, or Git mutations.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
