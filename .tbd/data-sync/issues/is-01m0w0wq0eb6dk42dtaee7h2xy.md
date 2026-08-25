---
type: is
id: is-01m0w0wq0eb6dk42dtaee7h2xy
title: Correct exp-038 ray normalization and dimension criterion
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-038-h-023-n5-fixed-angle-polytope.md
labels: []
dependencies: []
parent_id: is-01m0vyhtzd0j8gnfwm5k040ff1
created_at: 2026-08-25T08:34:20.302Z
updated_at: 2026-08-25T08:36:25.828Z
closed_at: 2026-08-25T08:36:25.827Z
close_reason: "Completed before target implementation: exp-038 now defines canonical rays and their exp-037 normalization map, requires nonempty bounded domain and six affinely independent feasible points, separates LP level optimality from pathwise stress, mutates proof inputs, and sharply refuses global, terminal, and component claims. Softschema, ledger, synopsis, and defect reconciliation pass."
resolution: null
duplicate_of: null
---
The first exp-038 preregistration draft used R_i without mapping exp-037's stratum-dependent scalings, inferred dimension five from rank six alone, and phrased an LP level certificate as differential no-descent. Define canonical vectors and source normalization, require six affinely independent feasible points, separate level optimality from pathwise stress, and add executable mutations before commit or target execution.
