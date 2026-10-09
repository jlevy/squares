---
title: n17 Session186 Performance and Validation Review
date: 2026-10-07
status: reviewed
---
# n17 Session186 Performance and Validation Review

Prioritize exact coverage-event work for one measured optimization, and repair checkout
import provenance before another expensive validation checkpoint.
The accepted replay profile attributes 52.93% of replay wall time to coverage and 9.44%
to collisions. Neither a larger facet cache nor a collision-first rewrite has a measured
justification. This review selects prospective work; it changes no checker, runs no
scientific target, and establishes no speedup.

Session186 runs October 8, 00:10:09Z–06:10:09Z, with research ending at 05:40:09Z. The
repository date is October 7 Pacific.
Root owns preregistration, execution and integration; Astra reviews mathematical
equivalence. The regional proof instrument and this engineering lane can proceed
independently.

## What the Measurements Establish

The
[exp290 diagnostic](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-290-matched-exact-replay/README.md)
preserves an initial 12.202-second process-sampling failure, followed by an unchanged
guard/resource retry.
The retry completed in 221.938 supervised seconds: NONE and PHASES independently
returned full `PASS_STALL` with equal mathematical payloads and seed/node/cells byte
identities. Their replay times were 109.465 and 111.545 seconds.
Overlapping host activity and observer overhead prevent treating their difference as an
optimization effect.

The
[exp294 mechanical audit](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-294-stages-exact-replay/mechanical-summary.json)
checks the same mathematical result and input identities, all sixteen step observations
and counter parity against PHASES. Replay took 108.237 wall seconds and 104.257 CPU
seconds. These are measured exclusive stages:

| Stage | Calls | Wall seconds | CPU seconds | Replay wall share |
| --- | ---: | ---: | ---: | ---: |
| Required-domain coverage | 1,024 | 57.293 | 54.916 | 52.93% |
| Remaining step verification | 16 | 23.233 | 22.461 | 21.46% |
| Final-state agreement | 1 | 10.255 | 10.138 | 9.47% |
| Collision-region validation | 1,024 | 10.218 | 9.986 | 9.44% |
| Partner-cover admission | 16 | 4.841 | 4.378 | 4.47% |
| Compression | 16 | 0.768 | 0.763 | 0.71% |

Inclusive stage times overlap; they must not be added.
The unattributed residual is 0.225 wall seconds.
Header and step/EOF observations include canonical digest work and terminal header
processing, so they are not pure JSON-decoding measurements.
Coverage-event generation, section construction and interval merging were not timed
separately.
The 25,134,984 logical collision-facet checks count retained obligations, not
all replay arithmetic or a demonstrated bottleneck.

Facet memo evictions were zero; forbidden-region memo evictions were 192. Cache lookup
hits were unobserved.
The supervisor sampled at most 472,891,392 bytes of current RSS for a live process.
Its 4 GiB limit is sampled **per process**, with owned-group cleanup; it is neither
aggregate group memory nor an allocation-time hard limit.
The recorded process lifetime peak is a different measurement.
This is one accepted control on a loaded host, not a representative population sample.

Exp284’s completed producer and timed-out fresh conditional replay remain unaccepted
geometry. Its 619.365-second combined run and 300-second fresh ceiling identify an
operational failure, but exp294 does not explain that failure.
Profile the accepted control rather than reuse exp284’s unverified child.

## One Optimization: Exact Coverage-Event Pruning

The standing
[coverage implementation](../../../packing/devtools/verify_n17_kernel_certificate.py)
already sweeps edge pairs with overlapping closed x-ranges.
A narrowly reviewable candidate adds exact closed y-range rejection before computing
line determinants and crossing coordinates.
Reject a pair only when its y-ranges are strictly disjoint; equality and touching remain
candidates. Precompute each edge’s bounds from its exact endpoints.
This changes prospective work, not the coverage domain, events, probes or acceptance
rule.

`covered_by_sweep` consumes convex polygons in hull order, inserts every in-range vertex
abscissa, and checks every event and intervening slab midpoint.
Its separate degenerate coverage branch must remain unchanged.
Skipping same-polygon pairs has stronger ordered-convex-boundary prerequisites; defer
that shortcut from the first candidate.
Do not convexify disconnected domains, sample angles, omit partner rows, or infer an
event cap from the caller’s wall guard.

Before selecting a benchmark, add low-frequency event/section attribution and counts of
candidate pairs, strict-y rejects, executed determinants, events and probes.
Keep logical verification counters separate.
Synthetic controls must compare complete event/probe sequences and first uncovered
abscissas to the original implementation: touching boundaries, collinear overlaps,
vertical edges, narrow gaps, rational scale changes and positive-area domains with
degenerate regions are material cases.

Then preregister matched full replays on identical accepted objects, rational container,
cells, interpreter, memo capacities and resource limits.
Use quiet alternating orders, at least two ABBA blocks, and retain every result,
CPU/wall time and sampled RSS. Each replay can retain the prior 180-second cooperative
ceiling and an explicit outer supervisor; root must allocate the combined lease before
execution. Acceptance requires exact mathematical payload, full counts and boundary
parity, plus a repeatable wall and CPU improvement without a material memory increase.
If attribution shows little event work or the y-range comparisons cost more than they
save, reject this candidate.

Implement the candidate in a disjoint worktree or coordinate an explicit source hold.
Standing geometry is a transitive dependency of the regional finite instruments;
changing it between frozen construction and fresh checking would invalidate their
common-source custody even when the wrapper is unchanged.

For scale only, halving the **entire** measured coverage stage would predict roughly
1.36× whole-replay speed at the observed shares.
The selected filter addresses only an unknown portion of that stage; no such gain is
forecast. A regional finite construction can spend time outside standing replay, so its
gain requires separate attribution.

## One Validation Repair: Bind Imports to the Selected Checkout

The
[frozen full checkpoint](../../../packing/campaign/agent-sessions/session-185-frozen-full-checkpoint.json)
ran 3,402.14 seconds under a 3,600-second ceiling and completed with **95 pass, five
failure, one skip** among 101 steps.
Nineteen page/workbench failures compared imported primary-checkout paths against the
managed worktree.
A shared editable environment is a concrete scope defect that should be
detected before another hour-long checkpoint.

Select a launcher preflight that sets checkout-specific `PYTHONPATH` and verifies the
resolved `sqpack`, validator, developer-tool and workbench module paths belong to that
checkout. An intentionally contaminated environment must refuse; an explicit override
must load the selected sources.
Clear a stale `PACKING_PROJECT_ROOT`; do not export a parent-checkout override into
negative-control clones.
Their mutated private checkout must supply its own import paths and retain the existing
mutation controls. Preserve the external Python environment and worktree-specific Cargo
target. The earlier engine-path plumbing already binds build and runtime paths; do not
copy a binary or silently skip its obligations.

Other debts remain scoped: historical Taylor byte pins failed although the new toy
certificates passed their own full exact verifier; their origin difference is unproved.
Mac contact-shade drift, Rust toy/progress timeouts and the old soundness-engine skip
remain distinguishable from geometric rejection.
Later focused source repairs do not turn that frozen checkpoint into a full
current-source pass.

The terminal local push hit its selected 240-second INT ceiling with **zero completed
step verdicts observed**. Its future-wait traceback does not identify a failed check.
The peer Mac run wrote eight successful assertions/JUnit in 4.585 seconds, then hung
after tests; TERM produced exit 143. That command was incomplete, and its cause remains
unproved. Keep durable per-step artifacts and explicit launcher/source context on the
next selected gate; do not rerun a broad tier simply to erase these records.

Required hosted CI at `69509014eb15ef9721a7b4e1a387cb2de482b194` was green by 22:16:03Z:
26 successes and 30 conditional skips, including
[packing-required](https://github.com/jlevy/squares/actions/runs/37694549369/job/113044552559).
That certifies its required hosted surface, not full current-source certification or a
new merge. Follow the [validation tiers](../../../development.md#validation-tiers) and
retain `think-7hy3` as the full-certification obligation.

## Session186: Observed Validation Causes and a Sealed Checkpoint Recipe

The early Session186 failures identify source selection and consumer-contract defects,
not a measured Python execution regression.
The local push floor stopped at its 120.106-second outer ceiling.
Its exact-verification step completed in 80.089 seconds; lint also saw two overlong
lines in a concurrently authored, untracked one-round draft.
Those draft lines were outside the committed `a01f` source.
The timeout and earlier Mac post-test hang do not establish where Python spent time.

The hosted `a01f9adf5ac108f755ce164e410220da42fe9c8d` run completed with 22 successes,
30 conditional skips and four failures, including the required rollup.
Its concrete causes were different:

- A narrative mutation still named 225 rounds while the rendered synopsis contained 228,
  so its literal anchor no longer resolved.
- An earlier worker prune omitted the exact 38,637-byte n13 family file consumed by the
  retained n32 inventory control.
  The full source kept that evidence, but the private worker lacked it.
- Newly tracked regional source contained genuine accepted-artifact byte boundaries that
  needed entries in the generated-artifact registry.
  The detector itself and its prohibition on source pins stayed unchanged.

The repairs preserve the original consumer assertion, the 192 MiB worker cap and the
integrity detector. An isolated copy-back control preserves the family’s exact bytes
while omitting sibling operational bulk.
Later source-only review found three more modules with legitimate accepted-input or
receipt boundaries; their registry entries remain pending a sealed checkpoint check.
These are readiness repairs, not evidence that the latest hosted surface is green.
A numeric synopsis anchor must be refreshed with its corresponding rendered count,
including any subsequent registration.

The existing [validator](../../../packing/src/sqpack/cli/validate.py) can support a
bounded checkpoint without a new policy or omitted checks:

1. Root selects an isolated checkout at the reviewed source and preserves its unique
   untracked assets. Confirm that the lint target directories contain no unrelated draft
   Python files: a clean tracked diff alone does not seal ignored files.
   Bind the external interpreter, that checkout’s Python roots and its own Cargo target.
2. Run [checkout import preflight](../../../packing/devtools/check_checkout_imports.py)
   with `--checkout PATH --bind-paths --output FILE`. Apply the same checkout-specific
   environment to the subsequent gate; the preflight changes only its child.
   Keep `PACKING_PROJECT_ROOT` absent, and let mutation workers bind their own source
   roots.
3. Inspect `packing-validate --push --since BASE --list` and the declared budgets, then
   run that required selection with retained command and step artifacts.
   Push keeps the edit floor and selects reachable tests conservatively; unsafe
   narrowing falls back to the whole suite.
   `--since` includes dirty, staged and untracked changes, so it does not create a
   snapshot. Artifact metadata records those inputs but does not lock them against
   concurrent writers.
4. Retain an explicit enclosing wall ceiling and owned-process cleanup.
   The existing `--timeout-seconds` bounds individual subprocesses, not the whole run.
   A completed focused `--only` check proves its named scope; it does not replace
   required push coverage.
   Keep the normal and pooled-heavy lanes and all selected consumer checks.

The current performance experiment remains the one selected optimization.
No further cache, clipping or gate optimization is justified by these failures.
A future launcher repair should first demonstrate selected-import parity, successful
private-worker mutation detection and unchanged required step/test selection on the same
sealed tree. Only after attributing repeated gate cost should root select a timing
experiment with matched source, work, resource limits and complete verdicts.
Incomplete runs have no speedup verdict.
The quiet eight-replay exact-Y campaign’s already frozen wall, CPU, memory and
mathematical-parity criteria remain its acceptance rule.

## First Matched Campaign: Six Valid Replays, No Gain Verdict

[Exp298](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-298-coverage-y-prefilter/README.md)
ended incomplete after 738.166 supervised seconds.
Six full fresh replays completed; each returned the same accepted `PASS_STALL`
mathematical payload, input identities, all sixteen step boundaries, proof counters and
memo-eviction observations.
The seventh phase was interrupted and the eighth never started.
No performance threshold was evaluated, and no gain is accepted from that prefix.

The terminal supervisor records `guard_unavailable`: its `/bin/ps` RSS sample exceeded
the unchanged one-second timeout.
It terminated the owned group, recorded return code −15 and completed cleanup.
The largest sampled current RSS was 440,221,696 bytes per live process.
This does not explain the host delay or replace the sampled guard with a hard allocation
limit.
The phase journal still said `running` after termination; its status is stale, not
evidence that work continued.
A derived terminal report must join the supervisor and preserve the original journal and
unknown child outcome.

After the campaign ended, the independent full one-round synthetic suite passed all 36
controls in 102.10 seconds under its 120-second outer ceiling.
Three focused CI controls passed in 10.60 seconds, and scoped Ruff, format and
BasedPyright checks had zero findings.
These checks cover the exact family-file copy-back, current literal anchor and live
artifact registry; they do not establish a full push or checkpoint pass.
The anchor was 228 at that check and must follow a later rendered-count freeze.

## Remaining Full-Certification Debt

The old five failed steps do not all remain unexplained.
The malformed campaign command and guard CLI fixture have later focused repairs.
Checkout import binding and explicit engine paths also have focused evidence; neither
has yet replaced the old full run with a correctly bound current-source checkpoint.
The engine-path tests used synthetic engines, so they do not certify the actual
soundness perimeter’s engine cells.

Two Taylor historical byte pins remain unchanged.
Their retained new three-owner certificates passed complete independent verification
with zero failures, which settles those artifacts’ geometric validity but leaves their
difference from historical bytes unexplained.
The Rust partial-line control and two-worker progress control still need a bounded quiet
reproduction with their original internal ceilings.
The Mac contact-shade census drift is also unrepaired; a descriptive golden mismatch is
not an n17 exclusion failure.
Repeated producer runs, golden replacement or longer test timeouts would not resolve
these distinctions by themselves.

A new full checkpoint is feasible within this session’s remaining clock, but its old
3,402.14-second runtime is not a completion promise.
After the quiet campaign, select a sealed source, pass import/artifact readiness and
retain per-command artifacts.
The existing default full tier has a 3,600-second ceiling; adding `--deep` or `--strict`
would introduce a different rebuild/skip contract.
Prefer launching by 04:34:50Z, leaving cleanup and five minutes before the 05:40:09Z
research boundary. Root must budget setup separately and report actual contention,
failures, skips and cleanup.
Keep `think-7hy3` open until its required current-source evidence is obtained; neither
hosted fast green nor accumulated focused repairs is a full-checkpoint pass.

## Where the Four-Hour Budget Went

The
[native partial cost receipt](../../../packing/campaign/resource-usage/codex-task-tree-session185-final-checkpoint.yaml)
ends at 22:04:39Z while three sessions were live.
It records lower bounds of 14.341 agent-hours and 3.778 wall-hours, including 5.916
aggregate model-stream hours, 1.095 compaction hours, 2.039 command-category hours and
1.008 agent-wait hours.
These overlap across agents and are not CPU accounting; do not add them into a wall-time
total or a complete four-hour cost.

Coverage optimization can reduce a repeated accepted replay, while correct checkout
preflight can avoid spending a checkpoint on the wrong imported sources.
Neither explains model reasoning, compaction or all coordination cost.
Keep one bounded engineering candidate beside the regional mathematical lane, publish
scoped receipts at source freezes, and choose any further work from measured results.

## Late-Block Validation and Storage Incident

The local push tier selected roughly 150 reachable test files and nine pytest workers.
It ended with five failed steps after 955.75 seconds.
The owned broad test group was terminated to release resources; this is an incomplete
behavioral run, not a passing suite.
Three project Ruff findings and an ESLint scan into another chat’s `.worktrees` were
corrected. Direct follow-up identified the remaining source-floor diagnostics: integrity
passed, while the session-close report needed its standing renderer.
The latter was rendered and checked without repeating the broad tier.

This run did not qualify a frozen source commit: source changed while it ran.
The full checkpoint’s preferred 04:34:50Z and latest 04:39:59Z launch times were missed
while sealing source and handling critically low storage.
The full checkpoint remains unlaunched.
Its 3,600-second scope and ceiling were not shortened, and no subset result replaces its
verdict. The protected 05:40:09Z research cutoff remains fixed.

At 04:45Z the internal volume had about 146,000 KiB available and the external volume
about 1,050,000 KiB. Two completed, reproducible test-fixture directories were staged
with `trash` after no-open-handle checks: `pytest-19` (499,056 KiB allocated) and
`main-merge-focused/control-snapshot0` (300,088 KiB allocated).
Their actual destinations are under `/Volumes/spud-ext1/.Trashes/502/`. Trash was not
emptied. Later free-space measurements include concurrent activity and cannot be
attributed to same-volume staging.
Unique research evidence, source, logs and the active environments were kept.

Mathematical targets continued beside this incident.
Hardened original-cell headers completed in 4.170 seconds.
The saved-pose incircle construction and fresh verification completed in 2.058 seconds,
rejecting all 95 fixed saved poses with all 12,920 pairs accounted for per phase.
This retires their orientation stage without a cell exclusion.
Published C2 acquisition completed in 78.944 seconds and its single unsampled replay
started at 04:50Z from immutable recovery source `e72c7f3c6`, under the prospectively
selected 2,400-second ceiling.
The primary checkout continues separate whole-cell mathematical work.
The
[C2 compact summary](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-311-c2-full-replay/mechanical-summary.json)
records its incomplete stop after 480.468 seconds: the one-second RSS process query
timed out, the owned group was terminated, and cleanup completed.
The last 18,000 checked nodes are progress, not a FULL receipt.
No ordinary exclusion was admitted, and the unchanged run was not retried.

The resulting iteration rule is concrete: use focused source controls and complete
bounded mathematical discriminators during development, run hosted CI alongside them,
and diagnose each failed job before another broad local selection.
This incident supports fixing selection and process isolation; it supplies no measured
gain for the incomplete coverage-optimization campaign.

The [hosted e72 run](https://github.com/jlevy/squares/actions/runs/37729215869) failed
all four behavioral shards.
Five fresh CLI fixtures lacked the selected checkout on their child Python path; an
in-process output-ceiling control inherited forbidden imports; a SciPy-absence assertion
inspected the whole pytest process; and the envelope reader bypassed the project YAML
loader. These were repaired with explicit child environments, fresh-process checks, and
the equivalent project loader.
Eight focused controls passed in 94.34 seconds; the complete envelope module passed 36
controls in 2.08 seconds.
Its measured 1.893 test-seconds were admitted through the existing whole-module cost
route. The relevance module passed all 16 controls in 0.47 seconds and supplied a second
measured cost, 0.347 test-seconds, when another test file landed.
Scheduling-only ownership changes then brought all four unknown-file shares below the
unchanged 10% guard; the final two shard controls passed in 0.43 seconds.
Project Ruff, formatting, types and the focused diff check passed.
These checks qualify the narrow repair, not a full current-source checkpoint.
The validate job stopped before validation when its pinned setup-uv action aborted a
manifest fetch after five seconds; no tool version or mathematical limit was changed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
