---
type: is
id: is-01m0r89x325gj6qqtskwawxh48
title: Separate portable mathematical checks from stochastic golden characterization
kind: bug
status: open
priority: 0
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels: []
dependencies: []
parent_id: is-01m0rkz14t04yjme92gnfncfv7
created_at: 2026-08-23T21:26:54.818Z
updated_at: 2026-08-24T01:00:50.408Z
---
D-059 and D-075. PR #16 retained a useful like-for-like cross-environment discrepancy: after source builds, the rendered golden differed at fixed n=10 seeds across two environments. A fresh PR #15 integration run of tools/golden_basins.py --deep passed locally in about 91 seconds, while PR #16 records a generic rebuilt-map mismatch elsewhere.

The evidence does not identify which mathematical predicate failed in the other environment: golden_basins.py labels any rendered-byte drift under the aggregate ORACLE FAILURES heading. It also does not establish the proposed floating-point/toolchain cause because the other run did not retain a complete fingerprint or raw per-predicate result. The earlier comparison of seed 14 against seed 7 was invalid and remains retracted.

The defect is broader than annealer_gap. The byte-compared rendering includes stochastic endpoint identities, discovery counts, frequencies, found_optimum, and trajectory data. Dropping one scalar would not make that surface portable.

Acceptance: define a cross-environment mathematical surface with individually reported convergence, retained-pose validity, and proved-value predicates; define a separate versioned characterization surface; retain raw output, endpoint poses, engine binary digest, Rust version, target, CPU/host, proposer, quench, equivalence policy, seeds, and budgets; run the same artifact on at least two environments; and update D-059/golden policy from the observed predicate-level comparison. Do not claim the post-quench oracle or the cause is portable before this experiment.

## Notes

2026-08-23 PR #16 integration correction. The original bead correctly discovered that source-build hermeticity did not guarantee byte-identical output, but overclaimed that every post-quench oracle survived and that only annealer_gap moved. The generic failure output cannot support that conclusion, and the full stochastic map remains compared. PR #16's five-commit correction history and like-for-like discrepancy are preserved in PR #15; D-075 records the overclaim. Work remains open under the acceptance criteria above.
