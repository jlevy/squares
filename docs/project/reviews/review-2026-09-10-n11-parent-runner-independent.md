# Independent Admission Review: BC326 Parent-Domain Runner

**September 10, 2026. Verdict: PASS for target-free instrument admission.** No blocking
defect remains in the final reviewed surface.
The reproduced runtime admission defects have been corrected, all 56 focused tests pass,
and Ruff and BasedPyright report no findings.
This review evaluates the instrument and its scientific scope; it does not report an
exp151 target result or admit a new packing claim.

The reviewed checkout is `/Users/levy/.codex/worktrees/88e2/squares`, on
`codex/n11-daytime-strategy`, with base HEAD `3a18a05a6af75e3800612549d5a3c5fe419b96f2`.
The initial review used the coordinator’s **2026-09-10T19:03:26Z** freeze.
The review was reopened for the narrow timeout-receipt correction and completed against
the current content identities at **2026-09-10T19:37:03Z**. The runner, schema, and
tests are working changes under review; the Git blob identities below bind this verdict
to their final content.
A clean execution commit and prospective target registration remain separate
requirements before BC326 can run.

## Scope and Evidence

The primary reviewed files are:

- `packing/devtools/wall_owner_parent_compatibility.py`;
- `packing/devtools/wall_owner_parent_inputs.py`;
- `packing/devtools/wall_owner_parent_experiment.py`;
- `packing/cases/n11_five_dot_cover/parent-domain-experiment.schema.json`;
- the three corresponding test modules under `packing/tests/`;
- `docs/project/reviews/review-2026-09-10-n11-parent-adapter-admission.md`;
- `packing/cases/n11_five_dot_cover/unit-parent-centre-contract.md`.

The review also followed the exact source-binding, frame-construction, physical-map,
B-only extremum, strict-escape replay, and transitive import implementations.
It read the retained fixed-cover transfer argument and the BC326 plan and agenda.
The repository instructions, tbd review guidance, and documentation guidelines were
applied.

The initial 45 focused tests passed in 27.34 seconds under the project Python.
Those tests did not catch the runner boundary defects below.
Independent synthetic probes reproduced them, and the coordinator repaired the shared
files during the review.
The final source review includes those repairs, rather than treating the initial passing
suite as admission evidence for the original runner.

All geometry executed by this reviewer used synthetic inputs or a direction-only formula
control. The four retained receipts were inspected for Git and producer identities, but
the saved exp151 residual was never evaluated against a parent box or owner class.
The reviewer made no shared-source edits, commits, pushes, or publications.

The final reviewed contents have these Git blob identities, obtained with read-only
`git hash-object` before and after the reopened checks.
Only the experiment runner and input-wrapper test module changed from the initial
admission:

| Repository-relative path | Git blob |
| --- | --- |
| `packing/devtools/wall_owner_parent_compatibility.py` | `6360f3af422a40fea40c1722da9fcb779fa5b1be` |
| `packing/devtools/wall_owner_parent_inputs.py` | `2cdb3dc0b313cda5f9324ae5d03341ce0ce61cae` |
| `packing/devtools/wall_owner_parent_experiment.py` | `b316e4c439720a0ffdf306568c6430b49278ff62` |
| `packing/cases/n11_five_dot_cover/parent-domain-experiment.schema.json` | `24108b43eeca43bdb920cba1c14d1e93eb1bff9e` |
| `packing/tests/test_wall_owner_parent_compatibility.py` | `a7b3acdaee6c65c9bb2f6c3cbb9a347080dee65c` |
| `packing/tests/test_wall_owner_parent_inputs.py` | `d5bbe285009d6fe3d44eb308d9cd47883d6ab7ff` |
| `packing/tests/test_wall_owner_parent_experiment.py` | `8b24385437f4d661a215c43f0bf023e858293439` |
| `docs/project/reviews/review-2026-09-10-n11-parent-adapter-admission.md` | `7bbf2f57a1daea418b9c03ba5b28044f59d59e82` |
| `packing/cases/n11_five_dot_cover/unit-parent-centre-contract.md` | `714229c1250e1403b44ea60fa873b2bd2e5bf4dc` |

## Findings and Dispositions

### NR-1: Completion could cross a declared deadline — Blocker, corrected

The initial `run_parent_target` could return `complete/residual-self-excluded` when its
injected clock was already 2 and its deadline was 1. The outer publisher checked only
the external deadline.
A synthetic source load at time 1 followed by completion at time 93 therefore produced a
complete result with `scientific_seconds=92`, despite the frozen 90-second allowance.
The result validator also accepted a complete artifact whose recorded scientific and
process times were 121 and 122 seconds.

There was a second boundary after the first fix: advancing the clock to 200 inside the
final publisher still returned `complete` with saved scientific time zero and process
time one. The clock sample preceded authority serialization, schema validation, and the
atomic write. Direct owner-gain completion could also cross its deadline inside the
checkpoint callback.

**Fix implemented:** The runner computes one scientific deadline as the minimum of the
90-second allowance and the absolute process deadline.
Publication checks that deadline before and after writing and replaces an overrun with a
partial document. A slow initial publication prevents target entry.
Complete recorded results must be strictly inside both frozen budgets.
The direct target checks residual, B-only, parent, checkpoint, and final owner
dispositions before claiming completion.

Independent controls now reject completion in these cases.
The two owner controls used real exact synthetic evaluator results: B-only
incompatibility with maximum `-14931/20000`, and a matched owner-domain gain with B-only
maximum `23/40000` and parent maximum `-23/40000`. Advancing the outer clock past the
deadline leaves both outcomes partial.
The checkpoint-overrun variant also remains partial.

Final repair sites: `packing/devtools/wall_owner_parent_experiment.py:723`, `:776`,
`:827`, `:860`, `:940`, `:992`, and `:1589`.

### NR-2: Failed admission could leave a complete artifact — Blocker, corrected

The initial result loader had no final deadline check on its residual-only path.
A synthetic complete result could be read back with deadline 1 and clock 2. The worker
published a complete candidate before readback, and an ensuing readback error left that
candidate marked complete.
The supervisor likewise preserved any schema-valid existing complete JSON after killing
the worker. A probe returned process status 1 while the saved document still said
`complete`.

**Fix implemented:** Independent readback checks its absolute deadline before returning.
Worker readback failure atomically downgrades a complete candidate to partial.
The supervisor handles timeout and ordinary nonzero exits, preserving the sources,
residual check, exact rows, and scientific-start state of a valid candidate while
removing its complete status.
Missing or malformed output uses the invalid-result fallback.
The timeout path terminates the process, waits two seconds, and kills it if necessary.

The final synthetic timeout control preserves bound source and residual evidence in a
partial artifact. The existing partial schema and exact readback also accept a completed
owner-domain-gain comparison inside a top-level partial document.
Keeping that row is sound: top-level incompleteness prevents promotion, while exact
readback still verifies the row.
The coordinator removed a transient `comparisons.pop()` that would have discarded an
already-checkpointed comparison.

Final repair sites: `packing/devtools/wall_owner_parent_experiment.py:1364`, `:1636`,
`:1685`, `:1699`, and `:1734`; the retained checkpoint comparison is at `:859`.

### NR-3: The claimed implementation pin omitted executing code — Blocker, corrected

The initial dependency list omitted transitive project modules including the fractional
direction generator and model, fixed-pattern strict predicates, and their dependencies.
The readback cleanliness check covered only that incomplete list.
The revision validator also accepted a caller-selected repository without proving that
the running modules came from it.
A stale editable installation or `PYTHONPATH` could therefore separate the attested
checkout from executing project code.

**Fix implemented:** The runner reconstructs the recursive local Python import closure,
including package initializers, and requires its declared list to equal that closure.
The reviewed closure contains 26 paths including the result schema.
Both revision guards bind the entry point to the requested checkout and check the
origins of loaded project modules.
A foreign `sqpack.field` origin is a tested rejection.
The clean execution guard checks the entire checkout; readback permits a new result
while requiring the complete implementation closure to remain clean and tracked at the
same revision.

An independent closure reconstruction matches the declared 26 paths.
The ordinary review environment resolves the executing project modules into this
checkout.

Final repair sites: `packing/devtools/wall_owner_parent_experiment.py:235`, `:264`,
`:347`, and `:391`.

### NR-4: Final test fixtures violated the callback protocol — Medium, corrected

The final type-check attempt reported two test-only argument-type errors.
Two injected target callbacks used the first parameter name `target_inputs`, while
`ParentTarget` required `inputs`, making keyword-call compatibility fail.
The findings were sent to the coordinator, who corrected the fixtures.
The final independent BasedPyright run reports 0 errors, 0 warnings, and 0 notes.
The corrected callbacks are in `packing/tests/test_wall_owner_parent_inputs.py:629` and
`:694`.

### NR-5: External timeout preserved a stale partial reason and clock — Medium, corrected

The earlier timeout path preserved an already-valid partial receipt unchanged.
That prevented false completion, but left its earlier checkpoint reason and elapsed
clocks in place after the external 120-second stop.
The coordinator’s correction deliberately updates an existing partial receipt only for
the timeout disposition.
An ordinary nonzero exit continues to preserve its more specific existing partial
reason.

The independent control constructs a synthetic partial receipt with one exact completed
owner comparison, a four-second source replay, and scientific/process clocks of 37 and
41 seconds. Reproducing the former dispatch by omitting the new `rewrite_partial`
argument leaves that earlier receipt unchanged after the simulated timeout.
This is a reproduction of the previous dispatch semantics, not an execution of a saved
old checkout.

With the current dispatcher, both termination during the grace period and forced kill
produce `partial/incomplete` with error `worker exceeded the 120-second external bound`.
The injected process elapsed time is 125.25 seconds.
The rewritten receipt records that value and scientific time 121.25, preserves the
four-second source replay and scientific-start flag, and preserves the sources,
authority, residual, summary, and exact comparison without modification.
Exact independent readback still accepts the retained row as partial evidence.
Promotion to complete is refused.
The ordinary nonzero-exit control leaves the original partial receipt byte-for-byte
unchanged.

The updater retains the larger of the new process duration and the existing recorded
duration, preventing a clock rollback.
It continues to validate and atomically publish the replacement.
It also now records a readback refusal for an already-partial worker candidate when that
readback fails; this keeps the new admission failure visible.
No scientific evaluation or input-binding behavior changes in this correction.

Final repair sites: `packing/devtools/wall_owner_parent_experiment.py:1643`, `:1704`,
`:1713`, `:1748`, and `:1762`. The added regression control starts at
`packing/tests/test_wall_owner_parent_inputs.py:1226`. The independent reproduction is
preserved at `/private/tmp/n11-parent-partial-timeout-review-probe.py`.

## Source Pins and Authoritative Inventories

The production pins agree with the tracked receipt blobs and the producer fields read
from the receipts:

| Receipt | Git blob | Producer revision |
| --- | --- | --- |
| exp143, `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json` | `cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19` | Not exposed as a separate producer field |
| exp146, `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-146-wall-owner-footprints.json` | `e54fa98133db5f2135cae8875188f51b7db26e12` | `915758898a97c92793f51e62b7a6b17f846895ca` |
| exp149, `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-149-selected-wall-tuple-cover.json` | `83ec897738d6d1b228623c3ac4c10cd9170d5940` | `5600c0fb4eccf9e9dcdf82b02506d3d4340651cb` |
| exp151, `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-151-selected-six-dot-cover.json` | `46d34b1e295d9f5178379b02780a8c598c1a73e5` | `c8cd38dad502c78840144bcae42df4294ba7f3d0` |

All four paths are rooted under
`packing/campaign/series/series-000-smoke-and-calibration/results/`. The pins store full
repository-relative paths.
Path validation refuses absolute paths, noncanonical path forms, traversal, and a
resolved symlink escape.
The admitted receipt loaders bind working bytes to clean tracked blobs.
The wrapper requires all four loaded receipts to report the same checkout revision and
requires that revision to match the frozen pin.
The production executor further requires the receipt checkout and implementation
revision to agree.

`load_parent_adapter_inputs` calls all four retained loaders, replays the selected
strict escape, augments the sixth-site input, and replays the saved six-dot strict
escape before binding inputs.
It independently rebuilds the full 361-orientation residual manifest and sixteen local
owner classes. The four selected owners retain the tuple `(0,0,0,7)` in BL, BR, TL, TR
order, with 181 expected signed frames per selected class.
Each frame binds its exact ray, orientation index, quarter-turn selector, and complete
folded-index/reflection source tuple.
Missing provenance is not accepted merely because cardinality is unchanged.

The source wrapper binds the fixed residual to its own orientation and source tuple.
The residual receives no owner mark or owner displacement box.
Result authority records the complete manifests independently of which rows the target
processes; readback rebuilds that authority rather than trusting the result’s own
expected-frame counts.

## Parent Geometry and Physical Transport

For a retained unit direction `r`, let `S=|r.x|+|r.y|` and `T=||r.x|-|r.y||`. The
admitted rule is exactly

```text
B = 9977/10000
q = 96/25
D = 207107/90000000
e(r,D) = max((B/2)*S, 1/2, (S-T*D)/(2+D^2))
```

The mismatch assumption is the nearest retained direction selected before owner routing.
It is not inferred from concentricity alone.
The retained transfer proof gives `B*(1+D)=899996306539/900000000000 < 1`, so the
selected closed core lies strictly inside its unit parent.
For `0<=d<1`, `S>=1` and `T<=1` make `S-T*d` positive.
The signed L1 lower bound and `sqrt(1+d*d)<=1+d*d/2` therefore justify the rational
angular term without reversing an inequality.
The old strict-core wall extent remains in the maximum.

An independent exact control checked 361 retained rays at each of three rational parent
rotations: half-tangents `-1/900`, `0`, and `1/900`. All 1,083 cases satisfy the
declared mismatch bound, and the derived extent never exceeds the literal unit-parent
coordinate half-extent.
This is a formula control, not an all-angle proof or a retained-pose measurement; the
analytic argument supplies the universal statement.

The adapter reconstructs the original anchored centre domain
`Z_B=K_B intersect (mark+[0,B/2]r+[0,B/2]Jr)` before restricting it.
It rejects stale polygons, dimensions, supports, and common rectangles.
It intersects the reconstructed domain with the closed box `[e,q-e]^2` and recomputes
the consumed support fields and common rectangle.
Empty, point, segment, and area results remain distinct.
The original exp146 frame identity and derived geometry are recorded separately.

The physical maps are exact:

| Physical owner | Map | Determinant | Corner permutation |
| --- | --- | --- | --- |
| BL | `(x,y)` | `+1` | `(0,1,2,3)` |
| BR | `(q-x,y)` | `-1` | `(1,0,3,2)` |
| TL | `(x,q-y)` | `-1` | `(2,3,0,1)` |
| TR | `(q-x,q-y)` | `+1` | `(3,2,1,0)` |

The wrapper checks coefficients, translations, target-family field, and permutations
against these four maps.
The symmetric parent box is invariant.
For determinant `+1`, the transported owner axes are `(Lr,LJr)`; for determinant `-1`,
they are `(LJr,Lr)`. The latter exchanges the two nonnegative displacement coordinates
and restores a right-handed frame.
Local class labels remain unchanged under physical placement.
The separate diagonal class involution is not used as a corner map.

## Extrema, Quantifiers, and Attribution

For each nonempty derived frame, the evaluator maximizes

```text
n dot residual_centre
  - min(n dot owner_centre over the derived domain)
  - owner_support_radius(n)
  - residual_support_radius(n)
```

over all eight signed owner and residual SAT axes.
The owner-centre minimum is the correct direction: it maximizes the available separating
gap. Linear projection attains its extremum at a vertex of the closed convex centre
domain, including point and segment domains.
Deterministic world-coordinate tie breaking preserves a reproducible witness.
The literal replay constructs square vertices and checks the signed gaps separately from
the support-radius formula.

The completion meanings are:

| Result | Required evidence | Permitted conclusion |
| --- | --- | --- |
| Residual self-exclusion | The fixed residual centre lies outside its own necessary parent box | This fixed core pose cannot be a selected unit-parent core under the rule |
| B-only incompatibility | The matched B-only class is exhausted and independently replayed nonpositive | The old model already excludes coexistence with this individual owner class |
| Owner-domain gain | The same owner’s B-only positive witness replays, and the parent class is exhaustively nonpositive or exactly all-empty | The added restriction excludes coexistence through this individual owner class |
| No owner-domain exclusion | All four selected classes have individually positive parent-restricted witnesses | This rule has not individually eliminated the fixed pose through these classes |
| Partial or unresolved | A prefix, a deadline, or a refused replay | No completion or universal-negative claim |

An incompatible parent result requires every expected derived frame, exactly one
extremum for each nonempty frame, no duplicate or extraneous indices, and a global
maximum equal to exact recomputation and literal replay.
All-empty classes use `impossible` with null maxima; they do not invent a margin.
A positive result proves only one separated strict-core witness and may stop the
extremum scan early, but the source manifest and derived frame inventory are complete.

Zero is sufficient for a fixed-pose strict-core exclusion because actual selected cores
are compact and strictly inside disjoint parents.
Zero supplies no positive-area neighbourhood radius.
Positive individual witnesses do not establish simultaneous four-owner feasibility, a
permitted unit-parent angle, an eleven-square packing, or a global owner-routing
theorem.

The target evaluates owners in TR, BL, BR, TL order.
An owner-domain gain is matched to that owner’s positive B-only control.
It may stop before B-only controls at later corners are run.
That is consistent with the registered individual-class question; it does not establish
that all four B-only classes are compatible.
No B-only failure found in the matched control can be relabeled as parent gain: both
structural validation and exact readback enforce that attribution.

## Saved-File Admission and Atomic Output

The JSON schema closes object shapes and requires exact rational strings.
It is a structural contract, not sufficient scientific authority by itself.
The loader rejects duplicate JSON keys and non-finite JSON constants, checks finite
nonnegative clocks and their partition, and refuses completion outside either frozen
allowance.

`load_parent_result` rebinds the implementation and all receipts, compares frozen
settings, regenerates authority, reconstructs the residual check, and re-evaluates every
saved comparison. Completed B-only and parent records must equal deterministic exact
recomputation. Unresolved parent records can contain only an ordered derived-frame
prefix; saved extrema require the complete derived inventory and must be the correct
ordered nonempty-frame prefix.
Partial maxima remain observed values with null global maxima and retained errors.
Changed geometry, missing frames, false slack, wrong map or class, altered attribution,
and forged summaries cannot pass this readback merely by changing a status field.

Output preparation requires a fresh `.json` path and excludes input receipts and project
code/test directories.
Schema validation precedes replacement.
The installed Strif writer uses a temporary sibling and `Path.replace`, providing atomic
visibility on this host.
It does not promise power-loss durability: no file or directory `fsync` is requested.
A failed write may leave a temporary sibling, while an existing final checkpoint remains
visible.

The scientific clock starts only after the full input-loading and replay wrapper
returns. It is shared by the residual check, matched controls, restrictions, exact
replay, and checkpoints.
The production worker is externally supervised for 120 seconds, including its work and
independent readback, with a two-second termination grace.
Internal checks are cooperative; a blocking operation is stopped by the supervisor.
Complete candidates are interpreted only after successful independent readback.
If publication, readback, or worker termination prevents admission, the surviving
artifact is partial or invalid.

## Validation and Remaining Scope

| Check | Result |
| --- | --- |
| Initial focused suite | 45 passed in 27.34 seconds |
| Focused suite at the initial admission | 56 passed in 108.92 seconds |
| Final focused suite after the timeout-receipt correction | 56 passed in 41.30 seconds |
| Ruff over the three modules and three test files | Passed |
| Final BasedPyright over the same six files | 0 errors, 0 warnings, 0 notes |
| Independent rational parent-rotation control | 1,083 exact cases passed |
| Independent final clock, readback, timeout, publication, JSON, and closure controls | Passed |
| Exact late owner-disposition and preserved partial-row readback controls | Passed |
| Reopened partial timeout, terminate, kill, retained-row exact readback, promotion refusal, and nonzero-exit controls | Passed |

The final focused command is run from `packing/` with the project Python 3.14.7:

```bash
.venv/bin/python3 -m pytest -q \
  tests/test_wall_owner_parent_compatibility.py \
  tests/test_wall_owner_parent_inputs.py \
  tests/test_wall_owner_parent_experiment.py
```

The first attempted `uv run --frozen` invocation failed because the sandbox could not
write the global uv cache.
The documented direct project-interpreter alternative ran the tests; the older
interpreter on `PATH` was not used.

The external termination controls use a synthetic process that exercises timeout,
terminate, grace-period timeout, kill, and nonzero-exit handling.
This review did not run a real 120-second worker or test host failure and power loss.
Recorded clocks are validated execution metadata, not an authenticated external timing
record. The normal trusted Python runtime and installed libraries remain outside the Git
source attestation.

The design fits the task: a pure exact adapter, a source-only admission wrapper, and a
thin fixed-target runner keep geometry, source authority, and experiment disposition
separate. Reusing the admitted B-only evaluator and literal square replay avoids a new
mathematical model.
The recursive import-closure guard protects the specific omitted-code
failure found here. No alternate architecture is required for this bounded instrument.

The earlier adapter-admission document remains accurate as a dated review of two library
modules. It must not be treated as the review of this runner or as evidence that the
target ran. The final BC326 record should cite this runner review and retain the
individual-class claim limit.

Before scientific execution, the coordinator must freeze a clean implementation commit
containing the complete dependency closure and prospectively register the exact output
path, retained source identities, fixed tuple and residual, rule, owner order, clocks,
and acceptance meanings.
This review does not substitute for those gates, the wider repository validation
checkpoint, or independent readback of the eventual actual result.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
