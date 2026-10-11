---
type: is
id: is-01m3qfvpn0dgprt6f2pb61bjza
title: Fan out hosted deferred validation across immutable-tree jobs
kind: task
status: closed
priority: 1
version: 8
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T21:06:49.119Z
updated_at: 2026-10-06T08:34:34.431Z
closed_at: 2026-10-06T08:34:34.430Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): Deep-gate fanout on origin/main: .github/workflows/deep-gate.yml resolve-tree, four deferred whole-Step jobs, exhaustive-1..3, deep-gate-required; first hosted measurement recorded in gate-budgets.yaml; PR #246 MERGED 2026-09-30. Repeat-sample spread is think-be1s's
resolution: null
duplicate_of: null
---
Split the deep gate's eight existing complete deferred Step verdicts into four balanced explicit hosted jobs and the exhaustive_exact lane into three stable whole-file shards through packing-validate. Resolve one immutable checkout SHA for every job; preserve nonempty, pairwise-disjoint complete coverage, unique timing artifacts, required aggregation, and honest inherited/derived job budgets until hosted cells provide direct baselines.

## Notes

Implemented deep-gate immutable resolver, four whole-Step deferred jobs, three whole-file exhaustive shards, exact aggregate and receipt contracts, tracked pending hosted measurements, and suite-file provenance. Added exhaustive-file-costs.json from retained run 35579234418. Focused evidence: 93 workflow/shard/budget tests pass; root's full validation CLI/selector run 191 pass; Ruff format/check clean; BasedPyright 0 findings; collect-only exhaustive union 60 nodes = shards 2+30+28, disjoint. First hosted candidate must replace pending_measurement entries and report critical-path wall plus runner-minutes. Upload-artifact remains warn/non-gating; in-job HEAD equality is fail-closed. Post-merge parity tracked as think-08ht.

Independent budget review of 5060cb6f8: GitHub API for successful workflow_dispatch run 36636552951 confirms head 9174140a, all ten declared workers completed successfully, wall 1133s, and worker durations 17/778/475/621/623/957/953/858/1015/1111s totaling 7408s. The register records the eight new-topology observations plus wall with spread null for the single sample; existing multi-run slow-lane and screen baselines and spreads are preserved. Only wall, resolve-tree, and deferred-atlas-grid ceilings tighten (3430->1900, 36->30, 980->900), each under 2x headroom. Focused budget/post-merge contracts pass 61/61. No enforcement change or speedup claim; keep open for repeat hosted evidence and publication.

Publication delta push at 0ce06bfd9 found a budget declaration mismatch after 1778 other tests passed: test_every_deep_gate_job_is_clocked_against_a_declared_wall requires a non-null sample spread for measured entries. The retained sampler computes max/min and emits 1.00 for a single observation; the previous note's spread null is superseded. Isolated parity commits 4f2ab1ed1 and 8856bb81a set the nine newly measured deep-gate fields to 1.00 and clarify that this one-sample arithmetic ratio does not estimate runner-to-runner variance. Post-merge pending entries and historical multi-run baselines are unchanged. Focused deep-gate/budget/post-merge tests pass 74/74; budget declaration, Ruff/format, and BasedPyright pass. Publication CI and repeat hosted measurements remain outstanding.
