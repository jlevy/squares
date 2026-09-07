---
softschema:
  contract: squares.validation_efficiency:Experiment/v1
  schema: ../experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: VE-004
  title: Start exact verification early with complete document mapping
  registered: "2026-09-07"
  tier: exploratory
  control_label: checks-order-control-v2
  candidate_label: checks-order-candidate-v2
  minimum_samples: 3
  minimum_improvement: 0.15
  maximum_allocation_ratio: 1.25
  target: benchmarks/test_checks_timing.py
---
# Start Exact Verification Earlier: Corrected Setup

This comparison repeats [VE-003](VE-003-checks-start-order.md) after its first control
failed the documentation map check. That failure remains in its original experiment.
Both new arms include the missing map entries, regenerated views, and the failed
observation. Freeze these common changes before timing. The candidate then adds only
the previously reviewed scheduler hint and its regression coverage from `292d40e7`.

Use the same complete workload and frozen 48-name fixture, the same host and Python
environment, three gate workers, one inner worker and one native thread per library.
Alternate three control/candidate pairs, with no heavy local work overlapping them.
Record immutable revisions and clean source state. Retain every observation and its
raw output, JUnit, command, step and run receipts; use a separate artifact directory for
each trial. Stop and verify child cleanup after an interrupted or timed-out observation.

The scored metric remains outer pytest wall time. All six invocations must pass all
48 checks. Acceptance requires at least a 15% median reduction, nonoverlapping ranges,
an allocated-work ratio no greater than 1.25, and independent correctness and complexity
review. No threshold, check selection, timeout or worker count changes. The driver
allocation proxy and limits on transfer to hosted CI remain as stated in VE-003.

## Disposition

Adopt the scheduling hint for the measured checks workload. The
[generated report](../report.md) records three passing samples per arm: control median
93.18 seconds (90.81–94.13), candidate median 71.84 seconds (64.96–73.09), a 22.9%
reduction with nonoverlapping ranges. The allocation ratio is below one and passes the
unchanged 1.25 guard. All six invocations passed the frozen 48 checks.

The control is `1dfdb8fb`; the candidate is `ed595fb6`. Their complete source difference
is the scheduler hint and its regression tests. Both source trees remained clean,
with no untracked inputs, throughout the alternating observations. Measurements ran
from 19:50:21 to 20:00:24 UTC on September 7. The earlier setup failure remains in
VE-003 and supports no performance inference.

The independent correctness review at 19:39:58–19:41:04 found no selection, timeout,
failure-propagation or report-order change. Twelve focused regression guards passed,
including a real early-started failure followed by successful checks. The complexity
review at 19:51:51–19:52:40 judged the optional boolean and stable secondary sort key
proportionate to this gain. Reordering the declarations would change report order;
hardcoding a step name in the sorter would hide the policy.

Independent evidence admission at 20:01:24–20:02:42 reproduced the existing report's
screen, checked all 48 names against stdout and native step receipts, verified the
JUnit evidence and byte-preserved imports, and confirmed chronological alternation and
matching host/worker regimes. It admits only this local exploratory checks-tier result.
The outer driver allocation remains a proxy, not measured CPU. A full checkpoint and
hosted CI are separate publication obligations; no speedup for either is asserted.

Native command, step and run receipts are retained for every pair:

| Pair | Control checkpoint | Candidate checkpoint |
| --- | --- | --- |
| 1 | [Control 1](../checkpoints/VE-004-control-1.tar.gz) | [Candidate 1](../checkpoints/VE-004-candidate-1.tar.gz) |
| 2 | [Control 2](../checkpoints/VE-004-control-2.tar.gz) | [Candidate 2](../checkpoints/VE-004-candidate-2.tar.gz) |
| 3 | [Control 3](../checkpoints/VE-004-control-3.tar.gz) | [Candidate 3](../checkpoints/VE-004-candidate-3.tar.gz) |

## Hosted Failure Evidence

The hosted observations motivated the candidate; they are not a matched performance
experiment. Their native command, step and run receipts are preserved below. The prior
successful run tested merge `8e2c0c31`; the two failures tested merge `1b2f3c56`.
Exact-verifier commands were unchanged across those sources.

| Hosted observation | Checks wall | Exact-verification step | Native receipts |
| --- | ---: | ---: | --- |
| [Prior success, run 34142796559](https://github.com/jlevy/squares/actions/runs/34142796559) | 91.06 s | 49.22 s | [Prior checkpoint](../checkpoints/VE-004-ci-prior.tar.gz) |
| [Run 34154326299, attempt 1](https://github.com/jlevy/squares/actions/runs/34154326299/attempts/1) | 150.31 s | 95.14 s | [First failure](../checkpoints/VE-004-ci-failure-1.tar.gz) |
| [Run 34154326299, attempt 2](https://github.com/jlevy/squares/actions/runs/34154326299/attempts/2) | 150.24 s | 94.35 s | [Second failure](../checkpoints/VE-004-ci-failure-2.tar.gz) |

Both failing attempts passed every correctness check and exceeded the unchanged
149.085-second drift boundary. The exact verifier started late and was the last step
running. Other unchanged commands also slowed, including commands that ran during that
final tail. Runner metadata does not identify a hardware or load cause. Starting the
verifier earlier addresses the measured queue delay; it does not explain or eliminate
hosted-runner variation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
