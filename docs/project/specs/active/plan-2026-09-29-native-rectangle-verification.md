# Native Rectangle Verification and wand125 Tools Intake

**Status:** Active. The verifier golden tests and Rust gate review (think-v4dn,
think-k8hl) and PR integration (think-sewp) are done; the native rectangle verifier
(think-bmf3) and the ceiling/admission findings (think-xgjo) remain open under
think-8cps. The pose-tree replay (think-190a) was retired on 2026-10-13: it was evidence
toward s(11), which T-060 settles.

The rectangle-density intake independently checks exact inputs and theorem premises, but
delegates complete coverage to Tokoharu’s `verify.cpp`. This work adds a native
implementation with a different geometric decision procedure and records the new wand125
tools without promoting unverified claims.

Parent bead: **think-8cps**. The
[mathematical intake review](../../reviews/review-2026-09-29-wand125-tools-mathematics.md)
owns source findings; the [tooling overview](../../guides/verification-tooling.md) owns
the inventory of available checks and gaps.

## Blocks and Ownership

| Block | Workflow | Bead | Deliverable and completion criterion |
| --- | --- | --- | --- |
| Source intake and claim review | W2 factual-review | think-8cps, think-xgjo | Pin the MIT source, cite its maintained repository, register T-058 and T-059 without frontier promotion, retain the ceiling and admission findings |
| Native rectangle verifier | W7 pipeline-improvement | think-bmf3 | Exact rational coverage engine, standalone candidate CLI, refusal controls, independently reviewed mathematical contract, and retained complete or explicitly inconclusive receipts |
| Verifier golden tests and Rust gate review | W7 pipeline-improvement | think-v4dn, think-k8hl | Complete CLI decision goldens with separate semantic checks; live Rust lint probes, executed Rust tests and rustdoc; scoped review and validation evidence |
| PR integration and certification | W7 pipeline-improvement | think-8cps, think-sewp | Reconcile the expired inherited session record, reduce frontend runtime without dropping checks, and obtain passing CI and full-checkpoint evidence |
| General pose-tree replay | W2 factual-review | think-190a | Audit branch/enclosure/measure premises and replay all 12,028 n11 minima; reuse the reconciled T-037 global proof for the identical certificate |
| Reader documentation | W8 documentation-pass | think-8cps | Maintained repository index, synopsis summary, and tooling inventory naming actual independence and remaining gaps |

The W7 block has parallel lanes with disjoint writes: mathematical contract and review
(GPT-6 Astra), implementation and tests (GPT-5.6 Sol, high), and verification overview
(GPT-6 Astra). The coordinator owns registries, claim identifiers, integration, receipts
and validation.
A bounded checkpoint follows the first usable engine and its controls; an
expensive certificate replay is a separate selected run, not a prerequisite for every
code edit.

## W7 Acceptance Contract

The native engine must decide the same geometric obligation without importing,
translating, calling or trusting `verify.cpp`. It may consume the same exact candidate.
Nonnegative rectangle densities permit a lower bound from a polygon contained in every
checking core over a rational center box.
Exact polygon clipping and integration then bound the captured mass throughout the box.
Exhaustive subdivision covers the entire admissible center domain at every required net
angle.

The implementation must check exact target count and side, nonnegative weights,
rectangle dimensions and orbit multiplicities, strict mass budget, net coverage and the
core-to-parent containment bridge.
A finite sample, successful source log, missing angle, timeout or unclosed box cannot be
accepted as a complete proof.
Point and threshold-charge certificates remain separate formats and proof contracts.

Controls must include a complete analytic positive certificate, an underweight cover, an
over-budget input, malformed or unsupported geometry/net metadata, and an exhausted
search budget. Check clipping at tangencies and box boundaries.
Bind every receipt to the exact input and implementation revision, record the required
and decided angle census, and distinguish coverage from the full packing-bound decision.

### Implementation and Review Standards

Load `tbd guidelines general-eng-agent-principles code-review-rules` before a verifier
review and `tbd guidelines general-testing-rules golden-testing-guidelines` before
changing its tests. For Rust code, also load `rust-rules`, `rust-lint-format-rules`,
`rust-testing-rules` and `rust-code-review-rules`. Record the applicable rules, findings
and actual gate results in the review and PR comments.
A passing lint gate does not establish the geometric theorem.

The current native rectangle implementation uses Python exact rational arithmetic.
A Rust implementation must preserve that contract, with explicit handling of integer
overflow or arbitrary-precision arithmetic, input validation, complete angle and box
inventories, and distinct refusal, incomplete and verified outcomes.
Review unsafe and FFI invariants, panic paths and arithmetic bounds before performance
changes. Use the pinned Rust toolchain, all-target Clippy with denied warnings, tests,
format checks and documentation checks; any missing gate or justified departure needs a
tracked disposition.
The floating-point `sqsearch` engine remains a search tool.

Golden scenarios exercise the production CLI and retain complete output, exit status,
arguments and input identity.
Normalize only documented unstable fields, preserve exact mathematical values, and
require explicit regeneration followed by diff review.
Keep semantic assertions for strict mass, complete angle coverage and unresolved work
outside the approved output: an updated golden must not weaken those acceptance rules.
Analytic geometric controls and independent mathematical review remain necessary because
a golden can preserve a wrong answer.
Fast scenarios run in the ordinary CI test lane; large certificate replays retain their
own receipts and resource ceilings.
The
[guideline review](../../reviews/review-2026-09-29-native-rectangle-contract.md#rust-and-golden-testing-review)
records the implemented controls and measured checks.
Broader Rust support and search-CLI contracts remain in **think-cr8l**.

## Integration Order

1. Review the geometric contract and implement the smallest complete independent checker
   with refusal tests.
2. Run complete analytic controls and a bounded retained-certificate probe.
   Retain inconclusive output as a performance/coverage limit, never as proof.
3. Run a complete retained certificate if the bounded probe supports the cost.
   The existing source replay remains separate evidence; only a complete native success
   can support independent coverage for that same certificate.
4. Broaden to the standing wand125 certificates with per-input receipts.
   Keep unknown results and unreplayed cases explicit in the overview and beads.

T-058’s ceiling repair and admission controls are tracked in **think-xgjo**; the new
checker must enforce its own budget regardless of upstream driver behavior.
Speed claims need matched benchmarks if adopted and do not alter the proof acceptance
rule.

## First W7 Checkpoint

The native library, candidate CLI and twelve focused test cases are implemented.
Two review lanes checked geometry and admission separately; fixes include rechecking
directly constructed library inputs, exact scalar validation, bounded axis traversal and
binding the receipt to the input read for that run.
A subsequent GPT-6 Astra review at max thinking found two early-exit receipt-accounting
defects, both fixed with exact regression cases, and supplied asymmetric-orbit and
common-core controls with analytically known answers.

The
[retained checkpoint receipts](../../../../packing/resources/web/wand125-tools-2026-09-29/README.md#native-rectangle-checkpoint)
show a complete 201-angle analytic control and refusal of the upstream false n1 bound.
The retained n11 probe exhausted its 100-node budget at one angle with 9 boxes
unresolved. That is an inconclusive computation, not a failed geometric claim and not
independent confirmation of the published n11 certificate.

**Session 163 initial entry: W7, think-bmf3.** Improve or supplement the common-core
lower bound enough to close a retained certificate, with the same exact acceptance
contract. First compare the unresolved n11 boxes against tighter exact bounds and retain
both the control and bounded target receipts.
The selected candidate bound sums, for each rectangle separately, its density times the
minimum of its exact overlap areas at the four center-box corners.
Convexity and the planar
[Brunn–Minkowski inequality](https://faculty.gardner.wwu.edu/gorizia12.pdf) (Gardner,
Theorem 12.1, with zero overlap handled by nonnegativity) make this a valid lower bound;
taking the minimum of the total density at those corners would not be justified.
Retain the exact pending boxes first, then compare both bounds on identical boxes with a
30-second cap. A useful first result closes at least one previously unresolved box
without weakening any bound.
Larger wand125 replays depend on this cost assessment; T-059’s complete row replay
remains a separate W2 task, think-190a.

## Continuing Work and Bead Dependencies

The continuation uses Sol implementation lanes and GPT-6 Astra at max thinking for
mathematical and verifier review.
The coordinator owns records, integration and PR 246. Archived source remains immutable.
Completed engineering slices do not close their parent mathematical obligations.

The bounded diagnostic and admission slices `think-wjb2`, `think-rrwv`, `think-gfpf`,
`think-pgrx`, and snapshot repair `think-r5x7` are closed after publication and passing
required CI at `5d276119c`. Their negative or partial mathematical outcomes below are
unchanged. The concurrent
[validation efficiency block](../../reviews/review-2026-09-29-validation-parallelism.md)
is tracked by `think-xcij`, with hosted fanout `think-tddk`, selector precision
`think-6izq` (completed), post-merge workflow parity `think-08ht`, child-pytest receipts
`think-14lz`, exclusive pool-heavy allocation `think-ysvk`, and post-merge wall
reporting `think-0atx`. These change engineering validation and its observability, not
the mathematical completion conditions below.

| Obligation | Bead | Completion evidence or dependency |
| --- | --- | --- |
| Native frontier diagnostics and corner bound | think-wjb2 | Exact capped diagnostics, analytic controls, reviewed implementation and identical-frontier comparison; implemented and reviewed, with target results below |
| Two-level depth refinement | think-gfpf | Reviewed diagnostic and complete 67/268 comparison; 15 parent closures, no complete-angle claim |
| Complete native external certificate | think-aqne | Depends on think-wjb2 and its cost assessment; all 201 angles, no unresolved work, bound input/source receipt |
| T-059 strict provenance and census admission | think-pgrx | Production-time identity binding, exact unique row inventory, explicit partial/unbound states and adversarial controls; implemented and reviewed, with target results below |
| T-059 full row replay | think-11z6 | Depends on think-pgrx; all 12,028 minima and witnesses reconciled |
| T-059 global counting | think-4t1e | Reconcile the identical certificate with existing complete native parent-core evidence; the global argument is established, while wand125’s exact row equality remains separate |
| Guard transformed-certificate admission | think-pegr | Exact count, positive scale, mass, geometry and source binding; refuse the retained false announcement |
| Rigorous ceiling implementation | think-xl42 | Certified witness bounds, orientation allowance and outward rounding |
| Cached-axis compiled equivalence | think-q4eo | Pinned builds, tangency/threshold differential controls and complete canonical replay |
| Lazy zmx2 admission and build controls | think-lg4u | Bound identities, nonempty complete census, explicit optimized-Python refusals, fresh successful builds and checked indices |
| Reproduced performance claims | think-wk08 | Depends on think-q4eo and think-lg4u; complete accelerated replay and matched measurements |
| Broader first-party Rust contracts | think-cr8l | Support policy, dependency audit and CLI behavior; separate from mathematical coverage |

### Frozen First Comparison

The first comparison is an exact engineering determination, not a timing speed-up claim.
The subject is Tokoharu’s retained n11 rectangle input at side 381/100, angle 1,
threshold 1, with the common-core traversal capped at 100 nodes and depth 20. Capture
its full unresolved frontier under the existing 30-second cooperative search limit,
binding exact candidate bytes, checker source and settings.
Do not replace the historical bounded receipt.
A truncated frontier or failed identity/admission guard invalidates the comparison; it
is not a negative scientific result.

For each identical retained box, compute the common-core lower bound and the sum of
per-rectangle minimum corner overlaps.
Nonnegative density and the reviewed convexity argument must justify each term.
Never take the minimum of total corner coverage.
The acceptance criterion is fixed before target measurement: every completed comparison
must preserve or increase the lower bound, and at least one previously unresolved box
must reach threshold 1. The comparison has a 30-second ceiling; incomplete comparison
records remain explicitly partial, and absence of a threshold crossing is retained.
No change to the threshold, input, or selected frontier may rescue a failed criterion.

Analytic correctness controls and independent Astra-max review precede target
measurement. Timing fields describe that run only; a performance claim would require a
separate paired experiment with repeated samples.
Complete external verification remains think-aqne even if this narrower criterion
passes. The reusable comparison command and its bound receipts supply the execution
record; this plan and the owning bead supply the predeclared criterion.

### First Comparison Result

The
[retained frontier](../../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-frontier-2026-09-29.json)
contains all nine pending boxes after 100 common-core nodes at angle 1. The
[comparison](../../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-bound-comparison.json)
matched that frontier and evaluated all nine boxes in 1.420 seconds, including replay,
without reaching its 30-second cap.
Every corner bound was at least the common-core bound; three increased strictly, but
none crossed threshold 1 from below.
**The frozen usefulness criterion was not met.**

Four queued boxes already had a sufficient common-core bound when re-evaluated.
All three strict improvements occurred among those four.
The five boxes below threshold received no improvement.
Pending means unfinished traversal work; it does not mean every queued box has already
failed the old bound.
The implementation and analytic controls are retained, but the result supplies no
complete angle or external-certificate verification and no measured speed-up.

### Fixed Traversal-Cost Probe

**think-rrwv**, declared after the comparison and before execution, asks a different
question: can the existing common-core traversal finish angle 1 at 1,000 nodes, depth 20
and a 30-second cooperative ceiling?
The candidate, side 381/100 and threshold 1 are unchanged.
Retain all pending boxes and the stop cause.
Success requires the angle’s complete domain and zero unresolved leaves; an incomplete
result records the limit rather than prompting a larger rerun.
No result from one angle licenses an estimate or acceptance of all 201 directions.
The corner-bound usefulness criterion remains failed regardless of this probe’s result.

The
[probe receipt](../../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-angle1-1000-nodes.json)
is `INCONCLUSIVE`: 1,000 nodes, 428 accepted leaves and 78 unresolved leaves.
Of the pending boxes, 67 reached depth 20 and 11 remained queued at the node cap.
No exact elapsed-time field was retained, so this receipt supports the work census and
stop causes, not a measured runtime claim.
No larger replay follows from this result.

### Predeclared Two-Level Refinement Diagnostic

**think-gfpf**, under **think-bmf3**, executed the following contract after GPT-6 Astra
at max thinking reviewed it.
The predeclared criterion is preserved here; the result appears below.
Freeze the retained 1,000-node receipt, exact candidate, checker source and settings,
angle 1 and threshold 1. Reconstruct its complete pending census and select exactly the
67 depth-20 leaves. Recompute each parent bound, then split twice by the existing
longest-side rule and evaluate all four children with the unchanged common-core bound.
The run evaluates 268 child bounds under one 30-second cooperative ceiling.

Success requires all 67 parents processed, every child bound at least its parent’s, and
at least one previously unresolved parent whose four child bounds all reach 1. Retain
the complete parent/child census and exact partition checks.
Missing work or a timeout yields `PARTIAL_DIAGNOSTIC`; identity, partition or
monotonicity failures are refusals.
A complete run with no closed parent is a negative depth-plus-two result.
The diagnostic cannot accept a packing proof or trigger an automatic larger replay.

Before target measurement, implement a reusable command with an exact local control:
container side 4, core side 1/2, density 16 on the D4-invariant rectangle $[1,3]^{2}$,
weight 64 and count 65. At rotation $(4/5,3/5)$ on center box $[15/8,17/8]^{2}$, actual
coverage is exactly 4. The common-core parent bound is $9/25$; each of the four children
after two bisections has bound $169/100$. These are analytically derived expectations
for the local control, not full-net acceptance.
Exercise incomplete-child, timeout, stale-source and malformed-census refusals before
the target run.

The nine-box comparison does not predict this refinement’s result.
The 1,000-node frontier includes an unprocessed depth-1 box covering half the initial
domain, so even successful local refinement would not estimate complete-angle cost.

### Two-Level Refinement Result

The
[retained diagnostic](../../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-depth22-refinement.json)
matched the frozen frontier and evaluated all 67 parents and 268 children in 8.994
seconds, including the 1,000-node replay.
Every child bound preserved monotonicity and 15 parents closed with all four child
bounds at least 1. **The predeclared local usefulness criterion passed.** The other 52
parents did not close completely, and the 11 originally queued boxes were outside this
refinement. The result remains `DIAGNOSTIC_ONLY`; it supplies neither complete-angle
coverage nor a full-run cost estimate.
No larger run was automatically selected.

The
[reusable command](../../../../packing/devtools/refine_rectangle_density_frontier.py)
binds the candidate, original frontier, native checker, comparison helper and its own
source. Ten focused controls cover exact analytic aggregation, census, stale sources,
missing children, bounded reads and partial timeouts.
Astra-max reviewed readiness before the target run.
Full external coverage remains **think-aqne** under **think-bmf3**; the next slice must
design and cost a whole-angle traversal rather than aggregate this diagnostic into a
proof.

### W7 Timing Instrumentation

The current W7 cost instrument adds opt-in `--timing` to the rectangle CLI without
changing the exact checker.
It reports monotonic wall time and process CPU separately for input reading/hashing,
admission, verification and source recheck.
Verification includes the engine’s admission recheck; it is not a pure geometry-kernel
measurement. Startup, argument parsing, receipt construction, serialization and output
are excluded. Focused differential controls cover partial, inconclusive and mass-refused
outcomes; the existing untimed goldens remain unchanged.
Astra-max review found no acceptance regression in this instrumentation.

A single development smoke observation returned the existing 1,000-node, 428-accepted,
78-pending census, with about 6.585 seconds verification wall and 6.532 seconds process
CPU. Only summarized tool output was retained: the full receipt and execution-time CLI
identity were not captured.
This is a development observation, not a durable proof receipt, paired benchmark,
whole-angle estimate or speedup claim.
Outer process costs remain unknown.
The next retained measurement must capture full output and actual source/input
identities before launch; no larger replay follows automatically.

### Full T-059 Replay Readiness

The reviewed census wrapper can run rows `0-12027` without changing the source search.
It runs one serial subprocess and requires a finite whole-process time limit.
There is no wrapper-level resume or shard admission: a timed-out run retains a bound
partial journal, but separately requested row sets have different bindings and cannot be
combined into a complete verdict.

The source reports 9,446 CPU-seconds for a full replay.
That is reported cost, not a measurement on this host; the three sampled rows do not
estimate the full cost.
A complete local run has not been started.
Its admission must require exactly 12,028 unique rows, matching minima and exact witness
attainment, followed by `validate --require-complete`. Even `COMPLETE_ROW_EQUALITY`
would establish row replay rather than a new global packing proof.

**think-11z6** owns execution and evidence retention.
The wrapper limits journal reads to 64 MiB and publishes without overwriting an existing
path. Full-journal size remains unmeasured, but its required fields alone exceed the
roughly 480 KiB of remaining mutation-worker snapshot headroom after this integration.
Choose and test how to retain the full evidence before adding it to the repository;
serial execution itself needs no new verifier mathematics.
The broader distinction between link-existence checks and content inputs is tracked
under **think-t1lk**. Neither a compressed format nor parallel or resumable admission is
implemented by the current census wrapper.

## Focused Proof-Review Cost Baseline

**think-af9n** measures the time needed to obtain and review a proof-specific result.
General slow repository checks are batched at integration checkpoints, outside this
loop. Local checks cover the changed verifier, the selected proof obligation, and
affected integration contracts; a full repository gate is not a prerequisite for the
next mathematical diagnostic.

The baseline separates three surfaces:

| Surface | Measurements | Interpretation |
| --- | --- | --- |
| Analysis and coordination | Observed model-stream and first-token intervals, tool and agent waits, handoffs, repeated work, and overlap-safe elapsed time | These are observable execution intervals, not a direct measurement of useful reasoning; overlapping intervals cannot be added to explain wall time |
| Validation execution | Monotonic wall time, process CPU time, setup and input parsing, frontier replay, exact bound evaluation, and result serialization | Separate profiling runs from ordinary timing runs; record instrumentation overhead and do not treat parent CPU as total worker CPU |
| Proof progress | Visited and certified boxes, unresolved boxes by reason and depth, exact bound deficits, and the declared domain covered | Faster partial work does not establish complete coverage; selected difficult leaves cannot stand in for the whole remaining domain |

Reuse existing task-tree rollups and verifier receipts before adding instrumentation.
The next bounded diagnostic must bind its source, input, parameters and outcome, report
its timing boundary, and account for the queued boxes as well as depth-capped leaves.
Missing measurements remain explicitly unavailable.
No full-replay estimate follows from the three sampled minimum rows or the selected
refinement parents alone.

Choose an optimization only after identifying the dominant cost: reduce repeated
orchestration and unnecessary checks, improve mathematical bounds to reduce work,
compile measured exact-arithmetic kernels, or distribute independent work with bounded
worker counts. Preserve the simple exact reference and compare verdicts, exact values,
refusals and unresolved coverage before accepting an accelerated implementation.

Each comparison fixes source, inputs, workload and worker allocation; records host load
and cache state; and declares its wall ceiling and acceptance criterion before running.
Use repeated comparable samples with their spread for performance claims.
Retain negative results and timeout receipts, and stop a bounded diagnostic at its
declared limit rather than silently extending it.
The report states both elapsed time and total compute cost so reduced waiting is not
mistaken for reduced computation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
