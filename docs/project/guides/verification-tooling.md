# Verification Tooling and Its Boundaries

This repository verifies several different mathematical objects: feasible packings,
weighted point covers, threshold charges, rectangle densities, and finite geometric
subproblems. A checker establishes only the theorem and input format it implements.
The existence of a checker is separate from a completed run on a particular claim.

## The n = 11 Argument from First Principles

To prove the optimal side length, two inequalities must meet at the same exact value.
A feasible packing of eleven unit squares in a square of side $T$ establishes
$s(11) \le T$. Global optimality additionally requires excluding every packing with side
less than $T$, including independently rotated squares and boundary contact.
Here $T = 3.8770835900228141773078970601\ldots$ denotes the exact algebraic endpoint,
not the printed decimal used as a tolerance.

The lower-bound proof turns that continuous question into a finite, exhaustive cover.
The 2,184 canonical patterns cover all configurations under the reviewed reduction.
Exact geometric checks exclude 2,180 patterns; symmetry relates the four survivors.
The capture argument confines the remaining configurations to a local region, and the
local endpoint argument rules out every smaller container.
The exact feasible witness supplies the matching upper bound.
Every required exclusion and capture component has a completed execution, and the review
checks that their hypotheses and conclusions join without a missing case.

There are three different forms of checking in this process:

- **Geometric execution** computes the exact inequalities that eliminate cases or
  constrain configurations.
  This is where most proof runtime is spent.
- **Composition and mathematical review** establish exhaustiveness, symmetry, boundary
  handling, state joins and the final implication.
  The fast final composer reconciles retained evidence; it does not repeat the geometric
  calculations.
- **Software validation** checks implementation contracts, malformed inputs, regression
  controls and repository integration.
  Passing general CI does not prove the theorem.

The accepted result is T-060 at **S5/V4/C5**: significance on a central open case, exact
machine verification, and a mapped review-ready confirmation record.
`C5` does not imply a distinct mathematical method, and `V4` does not mean a
proof-assistant kernel checked the argument.
Our checkers share disclosed exact arithmetic and construction primitives with the
source. There is no claimed uniqueness theorem or formal V5 certification.
See [the classification definitions](../../../epistemics.md).

## Separate Pipelines and Remaining Work

| Pipeline | Current result | Remaining work |
| --- | --- | --- |
| Global n = 11 optimality, T-060 | All required mathematical obligations executed and reviewed; final composition has no pending obligations | Simplify the argument before writing the dedicated explainer; add convenient fresh chained replay automation |
| Rectangle-density certificates, wand125/tokoharu tools | Optional independent Rust exact area backend and differential controls pass | Complete an external certificate replay and meet the C++ effectiveness and speed target; current bounded runs remain inconclusive and Rust is slower |
| Wang–Li intake, PR #249 | Separate historical improvement to the previous n = 11 lower bound, with its own verification record | Integrate the still-draft PR #249 onto main after PR #246; reconcile claim IDs and shared generated records while preserving historical source credit |

These pipelines do not substitute for one another.
The rectangle-density checker is not the checker for the global optimality argument.
Porting an exact polygon-area operation to Rust does not strengthen the geometric bound
or reduce its required search boxes by itself.
The completed rectangle experiment tested a stronger, independently reviewed derivative
bound before committing to a native port.
Its
[preregistered diagnostic](../reviews/review-2026-09-30-rectangle-derivative-bound.md)
evaluated all 13 frozen pending boxes in 1.163 seconds including setup, improved no
bound and closed no new box.
That negative result rules out adoption on this evidence; it grants no proof credit or
speed claim.

Fresh whole-proof automation (`think-e2ot`) is an engineering gap: all constituent
geometric runs already completed, but their existing receipt chains include
execution-specific bytes.
A fresh chain needs reviewed state-equivalence joins.
The publisher’s stale audit bindings (`think-gzju`) are another reproducibility defect;
neither is an unexecuted mathematical premise in the accepted composition.
Native performance (`think-3cwg`), proof simplification (`think-uz2x`), the later
explainer (`think-08pw`), and cross-PR reconciliation (`think-d15x`) stay separately
tracked.

The reusable exact kernels have distinct homes: rectangle geometry in
[`sqpack.rectangle_density`](../../../packing/src/sqpack/rectangle_density.py) and
[`sqverify_exact`](../../../packing/sqverify_exact/), and reviewed n11 union and
collision kernels in
[`n11_fast_exact_cover`](../../../packing/devtools/n11_fast_exact_cover.py) and
[`n11_integer_collision`](../../../packing/devtools/n11_integer_collision.py).
The [pending-inventory helper](../../../packing/devtools/rectangle_pending_inventory.py)
validates canonical rational coordinates, permitted domains and the complete declared
pending-box inventory for rectangle diagnostics.
Each caller still binds its candidate, checker, threshold, search settings and any
replay receipt; the helper grants no coverage or proof credit.
D4, field, capture and endpoint implications remain in source-specific checkers.
A thin fresh-replay entry point (`think-e2ot`) still needs reviewed state-equivalence
joins between their newly executed receipts.
It need not change the accepted historical evidence.

## Completed Global Proof Evidence

**T-060: global n = 11 optimality is confirmed at S5/V4/C5.**
[11SquaresOptimal](https://github.com/Queuingtheorydotcom/11SquaresOptimal) claims the
exact Trump endpoint through a global cell cover, 2,180 exclusions, a symmetry bridge
and complete capture into a local isolation region.
Its 23-stage source driver is a new trust boundary.
Neither the existing native T-037 lower-bound checker nor the rectangle-density checker
validates this global argument.
The [intake packet](../../../packing/resources/web/n11-optimality-2026-09-29/README.md)
records the source pin, completed independent executions and publication limits;
**think-3i74** owns their integration.
Source replay, independent rule checks and complete global composition must be reported
separately.
General slow repository tests do not substitute for any of these obligations.
The [proof review and stage map](../reviews/review-2026-09-29-n11-optimality.md) records
the reviewed implications, completed replay and remaining engineering follow-ups.
The
[census and capture contract](../reviews/review-2026-09-29-n11-optimality-census-contract.md)
separates metadata completeness from geometric acceptance.

Focused first-party checks have now run:
[`check_n11_optimality_d4`](../../../packing/devtools/check_n11_optimality_d4.py)
confirms the conditional symmetry bridge in 1.00 seconds including startup;
[`check_n11_optimality_local_dual`](../../../packing/devtools/check_n11_optimality_local_dual.py)
recomputes all 8,448 local residuals in 15.41 seconds, using shared exact geometry
primitives. That residual receipt remains explicitly incomplete.
The subsequent
[`check_n11_optimality_local_isolation`](../../../packing/devtools/check_n11_optimality_local_isolation.py)
also checks curvature, all 88 feature margins and the complete nonlinear branch bridge;
it confirms fixed-T local isolation in 17.98 seconds including startup, with shared
geometry source disclosed.
Pose inclusion, all 2,180 exclusions and case-438 capture were checked separately.
Their completed executions and reviewed final composition now establish T-060 at
S5/V4/C5; an isolated component receipt would not establish the global theorem.

The
[pose-inclusion checker](../../../packing/devtools/check_n11_optimality_pose_inclusion.py)
now confirms all 136 live rows and 1,542 vertices lie in the accepted rectangle,
conditional on their geometric ancestry (3.38 seconds including startup).
The [case-census checker](../../../packing/devtools/check_n11_optimality_case_census.py)
also confirms the complete case lists (0.11 seconds including startup), explicitly
without accepting any exclusion geometry.
The
[mask-0 field checker](../../../packing/devtools/check_n11_optimality_field_mask0.py)
accepts all 55 ownership obligations, 136 closed angular rows and 459 canonical
exclusions in 16.58 seconds including startup.
The [mask-202 checker](../../../packing/devtools/check_n11_optimality_field_mask202.py)
adds 653 distinct cases in 17.61 seconds, for 1,112 accepted exclusions.
The weighted mask1155 extension adds 131 distinct exclusions after all 71 ownership
checks and 522 rows pass in 29.44 seconds wall.
Subsequent complete field batches establish the entire 1,904-case field union.
The independent generic checkers accept 276 further cases, including ten reviewed
singleton runs and 266 complete executions in parallel batches.
The exact union contains all 2,180 required exclusions.
All 14 capture-root rounds pass, including 154 owner updates, 16,551 closed rows and
1,060 owned additions.
Actual geometric executions plus the Astra-reviewed source and receipt chain establish
conditional root ownership.
The first complete capture owner update also passes all 217 rows and 3,173,632 exact
collision inequalities, including the common kernel, compressed additions and next-state
join. The subsequent full root-state replay accepts twelve more updates and exact final
state, with 2,185 complete rows and 92 additions in 891.93 seconds.
Its trailing partial step promotes no state.
All ten capture nodes are accepted, including all three far-leaf contradictions.
The near run completed all 121 updates and 119,372 query rows in 302.528 seconds with
three workers. Its exact final state discharges the pose-inclusion premise; the complete
endpoint composition passes with no pending obligations.
The
[exact exclusion inventory](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/exclusion-inventory.json)
and
[dated mathematical reviews](../reviews/review-2026-09-29-n11-optimality-census-contract.md)
are the acceptance record.
Only complete, observed and reviewed executions contribute to that union; earlier
incomplete attempts receive no credit.

The T-060 geometry path has three reviewed accelerators.
The [exact union sweep](../../../packing/devtools/n11_fast_exact_cover.py) measures
1.892 times the reference row CPU speed with complete-case parity.
The optional
[integer collision kernel](../../../packing/devtools/n11_integer_collision.py) removes
repeated rational normalization using exact homogeneous coordinates and
positive-denominator cross-multiplication.
Three pinned capture rows run
[4.607 to 4.920 times faster in kernel CPU](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-step0/collision-integer-benchmark.json),
with identical facet checks.
Its mathematical review, rational boundary controls and source-bound generic integration
pass. Complete case 1687 reproduces all 192 rows and 3,055,752 collision facets exactly;
measured process CPU falls from 235.45 to 134.63 seconds (1.75 times).
The runs had different host load, so their wall-time difference is observational.
The [indexed event sweep](../../../packing/devtools/n11_indexed_exact_cover.py) rejects
edge pairs only when their closed horizontal projections are disjoint.
On a difficult case-1383 source-proposal row, it returns the identical 613 events in
1.682 versus 8.085 CPU seconds (4.81 times faster).
That diagnostic grants no geometric credit; differential controls on accepted rows,
boundary cases and actual spawned-worker execution also pass.
These are kernel measurements, not whole-proof speedups.
This path is separate from the optional Rust rectangle verifier described below.
The [batch cost reporter](../../../packing/devtools/summarize_n11_nonfield_costs.py)
separates executor elapsed time from overlapping case-wall sums, checker CPU, and
invocation overhead.
Its
[17-batch measurement](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-reviewed-costs-2147.json.gz)
uses retained executions; absent historical metrics remain unknown.
For example, the latest 24-case batch used 4,453.66 CPU seconds over 1,771.40 seconds of
executor wall time. This measures compute utilization, not agent analysis time.
The separate center-1383 diagnostic used 118.05 CPU seconds in 120.01 wall seconds,
including 6.08 seconds of admission and 3.65 seconds of seed checking.
That incomplete run accepts no exclusion.
The reviewed indexed sweep completes the entire center partition with three workers in
886.961 seconds: eight nodes, both branches, 260 complete updates and 36,480 rows.
Current-step worker inputs reduce measured startup from 1.864 to 0.551 seconds.
A separate fresh, source-bound capture reader extracts all 121 near-state updates in one
parse (12.617 seconds), avoiding repeated parsing of the 186 MB source.
Neither optimization changes the geometry required for acceptance.
The final 32-case batch took 5,386.365 seconds wall and 20,359.523 seconds total CPU
with four workers. These timings measure actual validation, not agent analysis.
Fresh full-ensemble orchestration is tracked as `think-e2ot`: current child checkers pin
retained parent receipt bytes, including timings.
The
[reproduction guide](../../../packing/resources/web/n11-optimality-2026-09-29/README.md)
explains how to replay individual components and distinguishes that work from the fast
metadata composer. The completed ensemble proves the result with disclosed shared local
kernels; it is not a disjoint-method C4 or formal V5 proof.
The
[current verification checkpoint](../reviews/review-2026-09-29-n11-optimality.md#independent-verification-checkpoint)
separates these obligations and their evidence.
The
[capture refusal](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-ancestry/refusal-result.json)
records a confirmed stale final-state digest in the published near audit, blocking its
advertised fresh replay and capture binding.
This does not refute the packing theorem; the
[proof review](../reviews/review-2026-09-29-n11-optimality.md) gives the exact scope.

The [epistemic scale](../../../epistemics.md#confirmation) distinguishes a complete
replay (`C3`) from confirmation by a distinct complete method (`C4`) and a mapped review
(`C5`). A source checker run here is a replay.
An independent parser, an exact premise audit, or a comparison of output logs can
strengthen that replay without becoming a second coverage decision.
Each claim’s retained receipts determine which work is complete.

## Verification Families

| Object | Main tools | What they establish and where they stop |
| --- | --- | --- |
| Feasible packing geometry | [`sqpack.verify`](../../../packing/src/sqpack/verify.py), [`sqpack.assurance`](../../../packing/src/sqpack/assurance.py), [independent rational witness checker](../../../packing/devtools/check_rational_witness_independent.py) | Containment, unit-square geometry and pairwise interior disjointness. Exact rational or accepted algebraic-field data can prove an upper bound. The independent checker accepts rational corner witnesses only. Decimal checks remain numerical; feasibility alone does not prove optimality. |
| Interval enclosure of a packing | [`promote.interval_verify`](../../../packing/src/sqpack/promote/interval_verify.py) | Outward-rounded enclosures can certify strict separation and containment. Unresolved contact is `undecided`; this route cannot certify an equality from a positive-width enclosure. |
| Weighted point certificate | [`decide_certificate`](../../../packing/devtools/decide_certificate.py) | Exact event-cell sweep and directed-rounding interval branch and bound decide every required centre and direction. Full retention requires both methods to accept and agree on the minimum, with the input bytes unchanged. The shared certificate representation and theorem remain common premises. |
| Point and threshold certificate | [`decide_threshold_certificate`](../../../packing/devtools/decide_threshold_certificate.py) | Exact sweep and interval branch and bound decide point charges plus threshold atoms: charge when at least $k$ of a named set is covered, with its justified budget. The exact route also checks dense-grid and slab agreement. This is a separate schema from rectangle density. |
| Relational certificate | [`decide_relational_certificate`](../../../packing/devtools/decide_relational_certificate.py) | Two exact routes decide supported point, threshold and floor atoms. Its two-route admission verdict does not claim the floating-point interval confirmation still required for a T-id in this class. Ordinary supported threshold records are delegated to the threshold gate. |
| Adaptive parent-core certificate | [`parent_core`](../../../packing/src/sqpack/fractional/parent_core.py), [`parent_core_interval`](../../../packing/src/sqpack/fractional/parent_core_interval.py) | Exact checks prove the angle-row cover, strict core containment, symmetry and budget; interval subdivision decides every centre in each row’s parent domain. Source-specific readers support Kleddamag n11, Evan Daniel’s angle-net format and Guzhou R052. A pilot, input refusal or sizing run cannot establish complete coverage. |
| Tokoharu rectangle density | [`audit_tokoharu_density`](../../../packing/devtools/audit_tokoharu_density.py), [`audit_wand125_rectangles`](../../../packing/devtools/audit_wand125_rectangles.py), [native exact prototype](../../../packing/devtools/verify_rectangle_density.py) | Existing retained bound replays use the unchanged upstream C++ checker with independent exact prerequisites and input binding. The native prototype implements exact coverage without upstream code and passes a complete analytic control; a complete native run on a retained external certificate remains outstanding. |
| Mixed point and segment cover with zero margin | [`audit_evand_mixed_covers`](../../../packing/devtools/audit_evand_mixed_covers.py) | Independent exact measure, symmetry and root-census audits surround source `zmx2` and `zm_mixed.py` runs. These audits do not re-prove individual boxes. The native parent-core engine needs strict interior cores and has no segment atom, so it cannot replace these source checkers. |
| wand125 point-only and modified rectangle bundles | [`audit_wand125_point_and_mixed`](../../../packing/devtools/audit_wand125_point_and_mixed.py) | Independently checks exact arithmetic premises and input binding for the n21, n45 and n50 packets, then audits or reruns their source programs. Its `exact` command decides no coverage. The n50 research checker differs from the standard Tokoharu checker, including acceptance at coverage `>= 1`. |
| Finite family depth and closed polygon coverage | [exact face](../../../packing/devtools/density_face_verifier.py), [independent slab](../../../packing/devtools/density_slab_verifier.py), [graph certificate](../../../packing/devtools/check_geometric_graph_certificate.py), [closed polygon cover](../../../packing/devtools/check_closed_polygon_cover.py) readers | Scoped geometric lemmas about supplied square families or polygon inventories. The caller must bind the source geometry and prove the reduction to a packing claim. These tools do not supply global rectangle-density coverage over all square poses. |

The [native n11 review](../reviews/review-2026-09-22-native-n11-parent-core.md) records
a complete parent-core run and its reconciliation.
Other adapters have different limits: the
[Guzhou R052 native reader](../../../packing/devtools/verify_guzhou_r052_native.py)
records a refusal at the reviewed allocation ceilings; its optional sizing mode is
explicitly outside a coverage verdict.
The
[Evan Daniel angle-net reader](../../../packing/devtools/verify_evand_angle_net_native.py)
requires every row certified before reporting `PASS_COMPLETE`. Successful parsing or the
existence of either adapter is insufficient to upgrade a source claim.

## Rectangle Density: Native Coverage and Remaining Replay Work

A rectangle certificate spreads nonnegative mass uniformly over each rectangle.
For a checking square, the captured mass is the sum of rectangle-intersection areas
multiplied by their densities.
This varies continuously with the square’s centre; point-certificate event cells, whose
captured atom sets are constant, do not decide it.

The counting proof requires total mass strictly below $n$ and at least one unit of
captured mass for every required checking square.
A rational direction net and a strict shrink inequality place a checked inner square
inside every unit square, connecting the finite angle list to the continuum of
orientations. The retained standard Tokoharu format uses 201 directions and the stronger
coverage target $10001/10000$. All admissible centres at every direction must be
covered; scanning a finite set of centres only tests candidate placements.

The first-party exact preflight recomputes mass from the candidate decimals as rational
numbers, expands the eight symmetry images with multiplicity, and checks nonnegativity,
target side, the angle-net endpoint and containment and smoothing margins.
It also checks that every supplied binary64 interval encloses its exact datum and that
the axis-event list is complete.
The wand125 importer regenerates the interval input and checks its identity against the
published input. Source binding fixes which checker was reviewed and replayed.

The existing retained bound replays use Tokoharu’s unchanged `verify.cpp` for global
rotated coverage. Their independent rational clipping and slice probes test its
arithmetic at selected placements; they do not exhaust the centre domains.
That boundary is recorded in the
[Tokoharu mathematical review](../reviews/review-2026-09-22-tokoharu-density-mathematics.md)
and
[wand125 rectangle replay packet](../../../packing/resources/web/wand125-rectangle-certificates-2026-09-27/README.md#receipts).

The [native exact prototype](../../../packing/src/sqpack/rectangle_density.py)
implements a different independent coverage procedure that can produce complete proofs.
Equality at the acceptance threshold may remain unresolved under subdivision.
At axis alignment it enumerates all rectangle events and evaluates their grid exactly.
At each oblique net direction it subdivides the admissible centre domain into rational
boxes. A polygon contained in every checking square over one box supplies a lower bound
on captured mass, computed by exact clipping against the density rectangles.
The optional `corner-min` mode sums each rectangle’s least exact overlap at the four box
corners. The
[corner-bound review](../reviews/review-2026-09-29-rectangle-corner-bound.md) proves
this bound and explains why taking the minimum after summing the rectangles would be
invalid. The default remains `common-core`. The engine accepts an angle only after every
box has a sufficient lower bound.

The [CLI](../../../packing/devtools/verify_rectangle_density.py) rechecks exact
admission premises, rejects inconsistent net metadata, and binds its receipt to the
candidate bytes and checker source.
Its default threshold is $1$; the source’s `rhs` is recorded separately, and
`--threshold 10001/10000` requests the standard upstream target.
Only all 201 required angles can produce `VERIFIED`. A successful subset is `PARTIAL`;
an exhausted node, depth or cooperative search-time budget is `INCONCLUSIVE`; an exact
core placement below the requested threshold is `COUNTEREXAMPLE` to that certificate.
None of those other statuses establishes the packing bound.

`--retain-pending-boxes` retains exact unresolved boxes for oblique directions, with a
global 10,000-node request ceiling.
It refuses oversized requests rather than silently truncating diagnostics.
The [comparison command](../../../packing/devtools/compare_rectangle_density_bounds.py)
replays and matches a retained frontier before evaluating both bounds on identical
boxes. Its output is always `DIAGNOSTIC_ONLY`; it supplies no trusted-resume or
proof-aggregation mechanism.

The [native controls](../../../packing/tests/test_rectangle_density.py) include a
complete analytic positive density, an underweight cover, malformed inputs,
direct-construction admission bypasses, the retained over-budget negative control, and
refusal to promote a capped retained-certificate probe.
The executed receipts distinguish their outcomes:

| Input | Native result | Scope |
| --- | --- | --- |
| [Analytic density](../../../packing/resources/web/wand125-tools-2026-09-29/native-analytic-control.json), $n=3$, $L=\frac{3}{2}$, mass $\frac{1683003}{625000}$ | [`VERIFIED`](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-analytic.json) | All 201 angles at threshold $1$, with no unresolved leaves; a complete control for the new engine |
| Retained source negative control, $n=1$, mass $\frac{289}{10}$ | [`REFUSED`](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-admission-refusal.json) | Rejected by the strict mass budget before coverage |
| Tokoharu n11 certificate at $\frac{381}{100}$ | [`INCONCLUSIVE`](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-bounded.json) | Angle 1 only, capped at 100 nodes: 46 accepted leaves and 9 unresolved leaves; no complete coverage claim |
| Same n11 input and exact pending frontier | [`DIAGNOSTIC_ONLY`](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-bound-comparison.json) | All 9 pending boxes compared; corner bounds improved 3 but produced no new threshold crossing. The predeclared usefulness criterion was not met. |
| Same n11 input, angle 1 at 1,000 nodes and depth 20 | [`INCONCLUSIVE`](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-angle1-1000-nodes.json) | 428 accepted leaves; 67 depth-capped leaves and 11 queued boxes remain. No larger replay selected. |
| Same n11 input, two further levels on all 67 depth-capped parents | [`DIAGNOSTIC_ONLY`](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-depth22-refinement.json) | All 268 children evaluated; 15 parents close completely. The other 52 parents and 11 originally queued boxes prevent complete-angle coverage. |

A complete native coverage receipt for a retained external certificate remains
outstanding. The
[W7 implementation and replay plan](../specs/active/plan-2026-09-29-native-rectangle-verification.md),
tracked by **think-bmf3**, requires that run before assigning method-distinct
confirmation to the external certificate.

wand125’s MIT-licensed
[`square-packing-tools`](https://github.com/wand125/square-packing-tools) adds
transformations and search accelerations while retaining the unchanged Tokoharu checker
for acceptance. The
[tools review](../reviews/review-2026-09-29-wand125-tools-mathematics.md) tracks
transfer, budget recovery, the `B · UB(n)` ceiling, rescaling and the search changes as
separate claims.
A transformed certificate needs its resulting exact premises checked; if
coverage is inherited, the transformation theorem must justify that inheritance.
Otherwise it needs a new complete coverage run.
Cached search checks and batched counterexample screening supply neither obligation.

The
[executed admission negative control](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/admission-control.json)
shows why these obligations must stay separate: the source wrapper scaled a measure to
mass $289/10$ for $n=1$, passed all 201 coverage checks, and
[announced `s(1) >= 1.5`](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/admission-control.log).
Since $s(1)=1$, the announcement is false.
Coverage succeeded, but the required `mass < n` check was absent.
The native checker rejects that retained scaled input at admission, before attempting
coverage.

## wand125 Verification Process and Independent Equivalence

The updated
[source](https://github.com/wand125/square-packing-tools/tree/3eb08e6c675d8d5aa953cb93da049a3f3cdc6123)
is pinned separately from the original intake.
Its
[source archive and identities](../../../packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/source-provenance.json)
preserve that version.
Four subsequent commits change wrapper admission, ceiling guidance and tests/CI; the
canonical C++ coverage checker is unchanged.
Historical findings continue to describe their original source pin.

| Stage | Upstream responsibility | First-party equivalent obligation |
| --- | --- | --- |
| Candidate generation | LP, transfer, budget recovery and screening propose rectangles/weights; cached-axis and batched/parallel screens accelerate search | Keep outside acceptance; candidate quality may change verification cost but supplies no proof |
| Exact admission | `certify.prepare` parses exact fractions, checks nonnegative mass, support and shrink/smoothing/net safety, expands eight symmetry images and emits enclosing binary64 intervals | Independently recompute the exact source measure, all premises and interval-input identity; additionally require strict mass below target n for a packing claim |
| Axis case | `verify.cpp` evaluates the complete event grid | Independently enumerate all exact event endpoints and prove complete axis coverage |
| Oblique coverage | Certified inner polygon areas give center values; outward-rounded derivative bounds extend them over center boxes; subdivision covers all boxes | Independently prove a lower bound over every center box, using exact clipping/common-core or another reviewed bound; no point sampling substitution |
| Direction completeness | `run_verify.py` compiles with safe floating-point flags and runs all 201 unique directions | Bind the same complete direction set and threshold; reject missing/duplicate/partial output and exhausted budgets |
| Packing implication | Net containment covers arbitrary rotations; nonnegative total mass below n contradicts n disjoint unit squares each capturing at least one | Check the counting and containment premises explicitly; a coverage-only VERIFIED result is insufficient |
| Receipt publication | Source/input hashes and complete coverage summary | Retain complete outcome, scope, independent code identity, exact inputs, work and timings; no acceptance from a producer flag alone |

The source compilation is `g++ -O2 -std=c++17 -fno-fast-math -ffp-contract=off`. Record
the actual compiler and host; a command named g++ can select different toolchains.
The C++ checker uses binary64 outward intervals, not exact rational arithmetic.
Approximate polygon construction is accepted only after interval checks prove its
convexity/containment and area bound.
Search speedups do not change this final checker.
A C++ axis failure means its lower bound did not meet the threshold, and resource
exhaustion means unresolved; neither alone is an exact counterexample.
The raw certifier rereads the candidate when publishing its result, so independent
admission uses an immutable snapshot and verifies that final geometry/weights agree with
the proved input. This is a required binding contract, not a report of corruption in a
published certificate.

There are three distinct thresholds.
Native default $1$ suffices for its reviewed packing obstruction but is weaker than the
canonical coverage target $10001/10000$. Nominal compatibility requires that exact
target. For a strict performance comparison, use the exact rational value of C++'s
upward-rounded binary64 cutoff and record both values.
This matches the leaf cutoff, not the subdivision strategy or interval costs.
A rational checker can validly prove exact equality where interval rounding remains
inconclusive; that is not a disagreement about the theorem.

Effectiveness includes correct refusal, as well as successful positive runs.
The [native tests](../../../packing/tests/test_rectangle_density.py) cover exact
clipping, asymmetric symmetry orbits, negative weights and malformed data,
direct-construction admission bypasses, strict mass budgets, exact violating placements,
incomplete angle selection and exhausted subdivision budgets.
Analytic oracles test both bounds; retained external probes test that incomplete work
cannot be promoted. The
[benchmark controls](../../../packing/tests/test_rectangle_verifier_parity.py)
additionally check complete angle inventories and exact interval-input binding.
Remaining acceptance work is a complete representative external replay at the matched
threshold, adversarial threshold-boundary and stale-artifact controls across the full
publication path, and measured performance on that corpus.
Passing the analytic control does not close these items.
**think-bcle** tracks these adversarial acceptance and publication controls.

**Performance parity is not yet established.** The comparison must use identical
candidate bytes, n/L/B, complete center/direction domain, threshold and worker
allocation. Measure source preparation, compilation, kernel execution, total wall,
aggregate child CPU and memory separately.
Record algorithmic limits, which are not identical across engines.
Only complete results that hit no cap are eligible for timing comparisons; a timeout or
one-angle success is not a speed win.
Use an analytic complete control, then representative retained external certificates.
Predeclare the corpus and alternate paired runs before reporting aggregate performance;
report uncertainty and worst cases, not just the fastest sample.

The independent implementation imports no upstream coverage code.
Replay of unchanged `verify.cpp` tests reproducibility, while the independent procedure
checks the same mathematical obligations through different code.
The point/threshold row checker below is another family.
Neither rectangle coverage nor its speed comparison verifies the separate T-060
global-optimality capture proof.
**think-om8z** tracks this process audit and **think-0jps** its reusable benchmark.

The
[unchanged upstream production-path control](../../../packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/full-pipeline-control.json)
runs `certify.py`, its real compilation/runner and all 201 angles on the retained n=3
analytic candidate with one worker and a 60-second outer ceiling.
Its receipt records the observed wall time, exact mass, complete angle census and
source/input/final-artifact identities.
This is a reproduction of the full upstream acceptance path on that control; the paired
benchmark measures kernel cost separately.
LP search and ladder generation are outside this control because they propose candidates
rather than accept proofs.

The
[first matched analytic run](../../../packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/parity/analytic-control/result.json)
completed all 201 angles in both engines at the same effective threshold.
This one control exposes a cost gap rather than establishing performance parity:

| Measurement | Upstream C++ | Independent rational checker |
| --- | --- | --- |
| Subdivision/event nodes | 209 | 1,781 |
| Verification subprocess wall | 0.381 s | 0.432 s |
| Verification subprocess CPU | 0.00916 s | 0.426 s |

Compilation took 1.017 seconds; preparation and exact adapter binding together took
0.00152 seconds. These are single-run observations on the recorded host, not a stable
speed ratio. The C++ journal’s internal kernel sum is only 0.00352 seconds; startup
therefore matters greatly for this small control.
Different representations also matter: native coalesces eight coincident symmetry images
into one rectangle while preserving the exact measure.
**think-3cwg** tracks stronger bounds and arithmetic profiling before larger replay.
More workers alone would not eliminate either the extra subdivision work or the
arithmetic cost.

The
[bounded external n11 probe](../../../packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/parity/n11-angle1-feasibility/result.json)
uses the retained $L=381/100$ certificate and only angle 1 at the same threshold.
C++ completes that angle in 0.740 seconds of subprocess wall; native reaches its
13-second internal budget and returns `INCONCLUSIVE` in 13.104 seconds.
This is a concrete performance gap on a real certificate, not a measured full-proof
speed ratio. Neither this subset nor the analytic control confirms the external
certificate with our independent engine.
Full 201-direction acceptance remains open.

The
[bounded profile](../../../packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/parity/native-angle1-cprofile/result.json)
locates the cost in exact polygon geometry: 9.95 seconds cumulative in coverage, 9.26 in
intersection areas, and 8.06 in axis clipping during the 10-second instrumented run.
These times overlap and must not be added.
Fraction arithmetic and repeated GCD normalization dominate the inner work; the profiler
itself adds overhead, so its node rate is not a speed comparison.
It does identify a target for compiled exact arithmetic.

The
[fixed-work clipping comparison](../../../packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/parity/native-angle1-fixed1000-frontier-clip/result.json)
preserves the entire normalized result: 1,000 nodes, 494 accepted leaves and the same 13
pending boxes. Avoiding unnecessary rational subtraction on wholly inside or outside
polygons reduced verification CPU from 7.305245 to 5.506285 seconds (24.6%) in this
observation. Both implementations also completed the same 201-angle analytic control.
This supports the exact clipping optimization; it does not establish full external
certificate acceptance or C++ speed parity.

Here, **native means first-party independent implementation**. The rectangle verifier
defaults to Python exact arithmetic.
Its optional [Rust geometry kernel](../../../packing/sqverify_exact/) uses
arbitrary-precision rational clipping and area through a resident process.
Select it with `verify_rectangle_density --backend rust --rust-binary PATH` and the
common-core bound. Unsupported inputs or transport failures refuse acceptance.
Finite input and integer-bit limits restrict the Rust admission domain; equivalence is
claimed only on the admitted common-core inputs.
`sqsearch` remains a separate floating-point search engine.

The fast validation step `exact rectangle Rust geometry` checks 210 exact polygon
comparisons, ten malformed-input refusals, and complete analytic and bounded external
verifier comparisons.
Rust formatting, lint, tests, documentation and locked build also pass.
Astra-max reviewed the arithmetic and fail-closed integration, including timeout
frontiers, binary/source binding and child cleanup.

The
[matched receipt](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-rust-backend-matched-2026-09-30.json)
records identical exact reports: all 201 analytic angles took 0.504 seconds in Python
and 3.800 seconds in Rust; the external n11 1,000-node control took 13.252 and 24.085
seconds respectively, both inconclusive.
These wall observations include concurrent host load; Rust child CPU was 10.889 seconds
on the external control.
Exact rational geometry, rather than message transfer, dominated the measured Rust run.
Python remains the default; this backend establishes a reviewed implementation and
differential control, not a speed improvement or complete C++ equivalence.
Further performance work belongs to `think-3cwg` and must not delay the separate T-060
proof integration.

A
[three-pair transport diagnostic](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/rust-transport-fixed-2026-09-30.json)
compares 128 identical polygon queries sent singly or in batches.
Exact answers agree; the median batch/singleton wall ratio is 0.99243, failing the
predeclared 0.75 target.
Child computation consumed about 0.54 seconds versus 0.006–0.009 seconds in the
coordinator. Batching is not the measured bottleneck.
The Rust primitive already precomputes polygon bounds and skips disjoint rectangles, so
adding that optimization again would not improve it.
The retained benchmark makes both findings reproducible.

The
[exact-arithmetic performance study](../research/research-2026-09-30-exact-arithmetic-verifier-performance.md)
compares the pinned Python and Rust arithmetic algorithms and native-library options.
Its retained Rust sample places most query stacks in coverage computation, with GCD and
rational normalization prominent.
Source review identifies extra reductions in `num-rational` and different integer GCD
algorithms in `num-bigint` and CPython.
On 128 fixed queries, two otherwise identical experimental multiplication variants
isolate the final redundant reduction: omitting it reduced median Rust child CPU by
12.9%, with nonoverlapping ranges and identical exact answers in three interleaved
pairs. The candidate still used about 1.52 times the Python primitive’s CPU on that
workload. The default implementation is unchanged; this is neither a whole-verifier
speedup nor native/C++ parity, and the remaining library and allocation costs are not
yet isolated. `think-i5x7` tracks this investigation under the native-performance work.

The subsequent bounded verifier comparison (`think-ss4a`) matched all twelve exact
reports across three pairs on the complete analytic fixture and external angle 1 at
1,000 nodes. The coprime helper used 14.49% less median Rust child CPU and 17.85% less
median invocation wall time on the external workload; wall ranges overlapped.
That external result remains inconclusive, and production defaults remain unchanged.
`think-1ozu` tracks the narrowly reviewed adoption decision; the report retains the
paired measurements and source identities.

## T-059 Row Replay and Its Separate Global Argument

The wand125 entries are T-058 (ceiling) and T-059 (row replay).
Their September 29 intake and archived receipts used provisional labels T-056/T-057; the
merge retained those published IDs for Couzo and de Winter and assigned these new IDs to
wand125. Historical receipts keep their original labels and bytes.

T-059 concerns all 12,028 row minima of the Kleddamag n11 point and threshold-charge
certificate. It is a different input and theorem from the Tokoharu rectangle example.
The [row-census wrapper](../../../packing/devtools/check_general_pose_tree_census.py)
has three distinct operations: inspect legacy rows as unbound inventory, run the pinned
source checker with production-time input and source binding, and validate the resulting
row journal.
Complete row equality requires each index from 0 through 12027 exactly once.
Missing, repeated, stale or mixed rows cannot establish it.

The wrapper independently evaluates each returned witness with exact arithmetic.
This confirms the reported charge at that center; minimality over the entire row domain
still relies on the pinned source’s search.
A witness alone supplies an upper bound on the true minimum.
The wrapper uses isolated Python execution so an inherited optimization setting cannot
disable upstream assertions.

The
[fresh bound journal](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/n11-bound-sample-portable.jsonl)
and
[summary](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/n11-bound-sample-portable-summary.json)
cover rows 0, 6014 and 12027. All three source minima equal `1000047518`, and the
independent evaluator confirms all three attaining witnesses.
The result is `PARTIAL_ROW_EQUALITY`: 12,025 rows remain unreplayed by this wrapper, and
this sample does not include the recorded global minimum.
Its timing is a sample measurement, not a measured full-run cost.

The global packing argument is a separate obligation, already established for this
identical certificate by the
[complete native parent-core review](../reviews/review-2026-09-22-native-n11-parent-core.md)
and its retained 12,028-row coverage decision.
That evidence proves the angle cover, strict enclosures, D4 reduction, threshold-charge
budget and positive counting gap, supporting the existing `V4/C4` bound $s(11) > 31/8$.
It is reusable evidence, not a missing proof or a new promotion.
Native threshold coverage need not reproduce each exact row minimum, so it does not
settle T-059’s claimed minimum equalities.
The
[bead map](../specs/active/plan-2026-09-29-native-rectangle-verification.md#continuing-work-and-bead-dependencies)
tracks wrapper admission, complete replay and this prior-evidence reconciliation as
`think-pgrx`, `think-11z6` and `think-4t1e`.

## Mixed Covers and External Replay

“Mixed” names several formats here.
Threshold atoms, a point-and-segment measure, and the n50 rectangle bundle have
different geometric meanings and different acceptance conditions.
An importer must identify the measure and the theorem explicitly.

The
[September 28 Evan Daniel packet](../../../packing/resources/web/evand-square-packing-2026-09-28/README.md#limitations)
retains complete fresh `zmx2` runs, independently audited root inventories, and samples
of the separate `zm_mixed.py` checker.
Re-summarising the shipped complete records or replaying a restricted region does not
constitute a complete fresh run of that second checker.
The native point and parent-core routes do not implement its zero-margin segment
measures.
For the separate n32 point cover, [T-051](../../../packing/frontier/RESULTS.md)
now retains two complete source-checker replays and is `V4/C4`. Its
[record](../../../packing/frontier/n-032.md) distinguishes the arithmetic and
box-closing arguments while naming the shared point test, D4 fold, author and
subdivision architecture.
This n32 confirmation does not discharge the pending complete mixed-cover re-sweeps for
n21 and n45.

The
[September 28 wand125 packet](../../../packing/resources/web/wand125-point-and-mixed-2026-09-28/README.md#limitations)
distinguishes exact premise audits, source replay and pending work for each case.
In particular, its retained n50 sample covers four of 201 directions; that sample alone
does not establish the full rectangle claim.
The tool’s comparison modes can accept a matching partial run, so comparison success
must be read together with the covered scope.
A summary labelled `PASS` is meaningful only with the obligations it names.

Lean evidence needs the same separation.
Regenerating a data file or scanning for `sorry` does not run the kernel.
A theorem conditional on an unproved coverage premise also leaves that premise
outstanding after a successful build.
The external packets record which builds were attempted, which were blocked, and which
covering statements remain hypotheses; their status cannot be inferred from the presence
of `.lean` files.

## Admission and Regression Checks

Before promoting an imported lower bound, require:

1. **Identity and interpretation:** a pinned source, immutable certificate bytes,
   explicit count and side, measure format, and the exact checker or importer revision.
2. **The theorem’s premises:** nonnegative mass or charge, correct budget, symmetry
   where used, valid angle cover, containment and boundary conventions, and any
   transformation or rescaling argument.
3. **Complete decision scope:** every required angle, row or root, with no missing or
   duplicated work, no unresolved boxes, and no failed or capped branch treated as
   acceptance. Retain the full verdict and its input binding.
4. **Accurate confirmation:** distinguish source replay, first-party premise audit,
   first-party complete coverage and a second complete method.
   Record formal-kernel results and remaining hypotheses separately.

The fast regression tests cover several refusal boundaries:
[Tokoharu input and source mutations](../../../packing/tests/test_tokoharu_density_audit.py),
[wand125 rectangle identity and frontier binding](../../../packing/tests/test_wand125_rectangle_audit.py),
[native rectangle decisions and refusals](../../../packing/tests/test_rectangle_density.py),
[point gate failures](../../../packing/tests/test_decide_certificate.py),
[threshold decisions](../../../packing/tests/test_decide_threshold_certificate.py),
[parent-core premises](../../../packing/tests/test_fractional_parent_core.py),
[mixed-cover census and arithmetic](../../../packing/tests/test_evand_mixed_covers.py),
and
[wand125 point and mixed packet audits](../../../packing/tests/test_wand125_point_and_mixed.py).
These tests check the tools’ contracts; their passing does not replay every large
certificate.
The [validation tiers](../../../development.md#validation-tiers) distinguish
routine checks from deliberately scheduled full computations.

The
[native verifier plan](../specs/active/plan-2026-09-29-native-rectangle-verification.md#implementation-and-review-standards)
requires tbd’s language, testing and code-review guidelines, including the Rust rules
for Rust implementations and the golden-testing rules for CLI receipts.
Golden outputs preserve a reviewed decision trace; analytic controls and mathematical
review establish why the expected decision is justified.
The Rust `sqsearch` quality gate applies to the search crate.
It does not compile or test archived standalone `zmx2` sources, whose replay and
arithmetic obligations belong to their retained source packets.

For the new tools intake, transformation tests must include invalid target counts,
exhausted budgets, altered scales and nets, and stale metadata.
Search-acceleration tests need to exercise cached-axis invalidation, reused LP bases,
omitted working rows, and missing or duplicated parallel angle results.
Timing claims need matched inputs and measured runs; a speed-up is separate from a sound
certificate verdict.

The
[static accelerated-verifier review](../reviews/review-2026-09-29-wand125-tools-mathematics.md#accelerated-verifiers-static-review)
found that the lazy-zmx2 wrapper does not enforce pinned build identities or a mandatory
positive reference census, and its final assertions disappear under optimized Python.
Those admission controls need repair before integration.
The cached-axis arithmetic appears unchanged, but compiled differential tests remain
outstanding. Neither static review constitutes a complete accelerated replay.

## Running the Tools

Run commands from `packing/` with the project CPython 3.14 environment.
On this Mac, first verify the external scratch volume and set `TMPDIR`,
`CARGO_TARGET_DIR` and `UV_CACHE_DIR` to the task’s external scratch directories,
following [AGENTS.md](../../../AGENTS.md).
Keep unique receipts outside disposable scratch.
Use each packet’s replay instructions for its complete source invocation and resource
ceiling.

```bash
# Native retention decisions on certificates in the corresponding native format.
uv run --frozen python -m devtools.decide_certificate CERTIFICATE.json
uv run --frozen python -m devtools.decide_threshold_certificate CERTIFICATE.json

# Native exact rectangle prototype: full net, with an explicit cooperative search budget.
uv run --frozen python -m devtools.verify_rectangle_density CANDIDATE.json \
  --n COUNT --side SIDE --threshold 10001/10000 --angles all --max-seconds 300

# Exact premises and retained-record audits; these do not run global coverage.
uv run --frozen python -m devtools.audit_wand125_point_and_mixed exact --check
uv run --frozen python -m devtools.audit_evand_mixed_covers check

# Explicitly selected complete upstream replay of one retained rectangle certificate.
# RECEIPT_DIR must name a fresh durable output directory.
uv run --frozen python -m devtools.audit_tokoharu_density \
  --out "$RECEIPT_DIR" --n 11 --replay --workers 2 --timeout 900
```

The native gates’ `--quick` modes are useful for rejection but cannot retain a
certificate. The rectangle audit without `--replay` runs the exact prerequisites only.
Resume and comparison commands must retain the distinction between an incomplete
computation and a completed proof.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
