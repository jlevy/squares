---
softschema:
  contract: squares.validation_efficiency:Experiment/v1
  schema: ../experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: VE-001
  title: Reuse float midpoint-to-cell lookup
  registered: "2026-09-06"
  tier: exploratory
  control_label: float-control
  candidate_label: float-candidate
  minimum_samples: 3
  minimum_improvement: 0.15
  maximum_allocation_ratio: 1.25
  target: tests/test_fractional_generate.py::test_the_float_oracle_scores_every_cell_the_exact_sweep_scores
---
# Reuse Float Midpoint-to-Cell Lookup

The original helper repeats float conversion and binary search for every cell of a
Cartesian grid. Precompute each axis’s mapping once and gather the same values.
The independent `reduce_to_cells` oracle, exact minima, full reference-cell coverage,
three configurations, directions, and tolerances remain unchanged.

Correctness guards cover rounded/coincident events against the scalar mapping and an
empty grid that must report every missing cell.
The independent review is retained with the block’s review artifacts.
See the [protocol](../README.md).

## Disposition

Adopt the lookup reuse.
All three pairs passed and cleared the preregistered arithmetic screen in the
[generated report](../report.md).
The coordinator reviewed the original scalar loop against the vectorized lookup:
midpoint rounding, left-search convention, all reference-cell visits, independent exact
minima, and tolerances are preserved.
The added tie and empty-grid regressions protect the two sensitive boundaries.
One per-axis precomputation adds little complexity and removes repeated work.

The
[affected-source audit](../../../../docs/project/reviews/review-2026-09-06-validation-efficiency-implementation.md)
verifies reconstruction from the retained patch and stable test source hashes.
Unrelated edits changed whole-tree diff digests between samples; this is an exploratory
component result with that explicit provenance limitation, not a full-checkpoint claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
