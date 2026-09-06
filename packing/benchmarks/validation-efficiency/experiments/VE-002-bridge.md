---
softschema:
  contract: squares.validation_efficiency:Experiment/v1
  schema: ../experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: VE-002
  title: Reuse bridge row inventory
  registered: "2026-09-06"
  tier: exploratory
  control_label: bridge-control
  candidate_label: bridge-candidate
  minimum_samples: 3
  minimum_improvement: 0.15
  maximum_allocation_ratio: 1.25
  target: tests/test_minus_w_bridge.py
---
# Reuse Bridge Row Inventory

Build `RowJetInventory` once per field within the bridge invocation, then share it
across checks that consume the same immutable rows.
Preserve all fifteen scale checks, three owner checks, exact arithmetic, and refusal
behavior.

The full bridge module supplies equality, sensitivity, refusal, and builder-count
guards. This experiment measures the whole module.
See the [protocol](../README.md).

## Disposition

Adopt invocation-local inventory reuse.
All three pairs passed and cleared the preregistered arithmetic screen in the
[generated report](../report.md).
The coordinator reviewed the shared inventory’s lifetime and call sites: each invocation
rebuilds it, owner checks receive fresh active rows, and all scale, owner, sensitivity,
and refusal checks remain.
Reusing existing immutable setup earns its small implementation cost.

The
[affected-source audit](../../../../docs/project/reviews/review-2026-09-06-validation-efficiency-implementation.md)
reconstructs the bridge source and test exactly from the retained patch.
The receipts directly hash the test, but not the imported bridge module.
Unrelated edits changed whole-tree diff digests.
The source audit is therefore part of this exploratory acceptance; the timings alone do
not establish full-source or full-checkpoint equivalence.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
