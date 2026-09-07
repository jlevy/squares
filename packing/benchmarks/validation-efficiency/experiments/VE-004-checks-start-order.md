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

Registered before the corrected comparison; no samples or accepted result yet.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
