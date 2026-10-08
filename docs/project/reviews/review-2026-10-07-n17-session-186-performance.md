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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
