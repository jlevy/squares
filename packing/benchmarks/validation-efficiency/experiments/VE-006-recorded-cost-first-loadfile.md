---
softschema:
  contract: squares.validation_efficiency:Experiment/v1
  schema: ../experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: VE-006
  title: Start loadfile work units in recorded cost order
  registered: "2026-10-14"
  tier: exploratory
  control_label: loadfile-case-count-control
  candidate_label: loadfile-recorded-cost-candidate
  minimum_samples: 3
  minimum_improvement: 0.15
  maximum_allocation_ratio: 1.25
  target: packing-validate --suite-a/--suite-b/--suite-c/--suite-d
---
# Start Loadfile Work Units in Recorded Cost Order

Pytest-xdist 3.8’s `LoadFileScheduling` inherits a default queue reorder by case count.
The suite already partitions modules using recorded whole-module costs, but case count
can give a cheap, highly parametrized module priority over an expensive small module.

The hypothesis is that starting known modules by descending recorded cost reduces the
final shard tail while retaining the same collection, file locality and worker
allocation. The candidate uses the public `pytest_collection_modifyitems` hook and
xdist’s existing `--no-loadscope-reorder` option.
It groups by canonical physical module path, preserves each module’s original case order
and breaks cost ties by path.
Unrecorded modules run first in path order; they receive no invented weight.
The hook acts only on a configured shard using loadfile with that option.
Unsharded, serial and frontend collection retain their existing order.
The controller transmits this exact decision and shard through supported xdist worker
metadata, because xdist rewrites worker distribution to `no` before collection.
Xdist retains its scheduler, crash recovery and low-watermark behavior: a worker with
more than two pending cases does not receive another work unit merely to prefill two
units.

## Frozen Admission Guards

Before the next hosted measurement, freeze these categorical requirements:

- Every existing selected node remains present exactly once, with unchanged identities
  and per-module case order.
  Every required current-head node executes without a skip.
- All four canonical shard selectors pass their functional checks, coverage guards and
  enforced 12-second CALL ceiling.
  Their wall ceilings remain 335/360/360/335 seconds.
- The four shard receipts belong to the same immutable source and run attempt.
  Worker allocation, inner allocation, browser requirement, markers, shard assignment
  and limits remain unchanged.
- The current-head affected mutation controls pass.
  The normal frontend remains a separate required surface; these four shards do not
  claim its excluded cases ran.
- No scheduler subclass, worker-count change or eager fixture relocation accompanies the
  ordering change.
- A real two-worker receipt establishes the intended module priority and identical
  collections after xdist worker setup; mock-shaped configuration checks alone do not
  establish that the hook runs.

A single successful cohort can establish admission against these guards.
It cannot establish a timing improvement.
The verdict remains pending until the actual receipts arrive; any failed guard rejects
that observation.

## Comparative Screen

The campaign’s exploratory screen remains three interleaved control/candidate pairs,
with the same cost record, selected nodes, four-CPU hosted regime, Python 3.14.7,
`--jobs 1 --inner-jobs 1`, pinned browser and unchanged optional-skip policy in both
arms. Each receipt must capture source, tree, command, allocation, JUnit and omissions.
Require every trial to pass, at least a 15% median wall reduction with nonoverlapping
ranges, and allocated worker-seconds no greater than 1.25 times control.
Report median and range, followed by a separate correctness and complexity judgment.

The unsuccessful run
[38597483408](https://github.com/jlevy/squares/actions/runs/38597483408) at source
`08d23c06b1819bd42fcdf3b1199455d57b416967` is an operational antecedent, not a paired
passing baseline. Repricing the cost record during integration requires holding that new
record fixed in both comparative arms; it cannot be attributed to ordering.
No candidate timing observations or speedup estimates are registered here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
