---
softschema:
  contract: squares.validation_efficiency:Experiment/v1
  schema: ../experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: VE-003
  title: Start exact verification before the checks queue
  registered: "2026-09-07"
  tier: exploratory
  control_label: checks-order-control
  candidate_label: checks-order-candidate
  minimum_samples: 3
  minimum_improvement: 0.15
  maximum_allocation_ratio: 1.25
  target: benchmarks/test_checks_timing.py
---
# Start Exact Verification Earlier

PR110 run 34154326299 passed correctness but exceeded the checks-tier runtime band
twice, at 150.31 and 150.24 seconds.
Native receipts place exact verification about 42 seconds behind engine setup and leave
a 41-second final interval with no other subprocess work running.
The preceding successful run took 91.06 seconds; unchanged exact commands were also
faster when running alone.
The available runner metadata does not identify the cause of that broader variation.

The candidate gives exact verification an early-start hint among unbudgeted steps.
Budgeted-step precedence, declared report order, every command, selected tier, timeout,
worker count and acceptance criterion remain fixed.
The proposed benefit is less idle capacity at the end, not cheaper mathematical
verification.

## Frozen Comparison

Use the [maintained instrument](../../validation_timing.py) and the explicit
[checks workload](../../test_checks_timing.py) on two clean checkouts beneath the attic.
The control contains this workload and protocol on merged baseline `22873a68`. The
candidate differs by the scheduling hint and its regression coverage.
Receipts bind their actual commits and source state.
The [48-name fixture](../VE-003-checks.json), frozen from that baseline, prevents a
passing observation with reduced or substituted coverage.

Alternate control and candidate three times on this macOS host, with the same Python
3.14 environment, warm filesystem caches, no cache flushing, three gate workers, one
inner worker, and one native thread per library.
No other heavy local runs may overlap.
Use a fresh native timing-artifact directory for each arm; run UUIDs distinguish trials.
Retain all stdout, stderr, JUnit, command and step receipts, including failures.

The scored metric is outer pytest wall time: the complete gate invocation plus its small
driver cost. Retain the CLI’s own tier wall separately.
All six observations must pass all 48 named checks.
Acceptance requires at least a 15% median reduction, nonoverlapping ranges, the existing
allocated-work ratio at most 1.25, and an independent correctness and complexity review.
A smaller or noisy result is not accepted by this screen.
No percentage claim transfers from this local regime to hosted CI.

The instrument records one allocated pytest driver; the gate itself has three workers.
Its absolute worker-seconds are a driver-allocation proxy, not actual gate worker time
or CPU. The constant gate allocation of three makes the before/after allocation ratio
the same. Native thread limits are controlled locally; the hosted receipts did not set
those limits. These regimes remain distinct.

An interrupted or timed-out wrapper is incomplete: stop the comparison and verify that
no detached gate children remain before another sample.
The wrapper retains raw output before coverage assertions, and ordinary tests never
collect this opt-in workload.

## Disposition

The first control observation, `a742211d2fb644eb835a6255a8e9268b`, failed at
`47970489`: 47 of 48 checks passed, but the documentation checker refused this unmapped
experiment document. The invocation completed normally in 99.48 seconds including the
pytest driver. There was no timeout or interrupted child.

Stop this comparison without a candidate observation or acceptance claim. Retain the
failed observation in the [generated report](../report.md) and its
[native checkpoint](../checkpoints/VE-003-control-setup.tar.gz).
[VE-004](VE-004-checks-start-order.md) repairs the shared document map before a fresh,
prospectively registered comparison with the same workload and acceptance rule.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
