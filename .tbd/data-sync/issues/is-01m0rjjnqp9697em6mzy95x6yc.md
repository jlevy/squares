---
type: is
id: is-01m0rjjnqp9697em6mzy95x6yc
title: "PR #16 R16-1: portable-oracle conclusion and repair are unsupported"
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels: []
dependencies: []
parent_id: is-01m0rj3jzb99380az12g72g6n8
created_at: 2026-08-24T00:26:27.951Z
updated_at: 2026-08-24T00:38:51.999Z
closed_at: 2026-08-24T00:38:51.998Z
close_reason: "Fixed in the PR 16 absorption: the response no longer infers a portable post-quench oracle from aggregate byte drift or prescribes dropping only annealer_gap. D-075 records the error; D-059 and think-osyp retain the predicate-level portability experiment."
resolution: null
duplicate_of: null
---
PR 16 response lines 223 and 263-265 conflict: one retained report says seed 7 does not reach the proved optimum, while the conclusion says every environment did. The generic ORACLE FAILURES label does not identify the failed predicate, and dropping only annealer_gap leaves the rest of the stochastic rendered map under byte comparison. Preserve the measurement, narrow the conclusion, separate portable mathematical checks from environment-scoped stochastic characterization, and retain provenance. Layer: docs/tooling. Defect log entry required.
