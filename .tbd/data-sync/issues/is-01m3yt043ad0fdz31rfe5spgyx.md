---
type: is
id: is-01m3yt043ad0fdz31rfe5spgyx
title: "W2-P: sqverify_fast performance loop against verify.cpp"
kind: task
status: closed
priority: 1
version: 4
labels:
  - verifiers
dependencies: []
parent_id: is-01m3yrezbcgcr728c37fq49bvf
created_at: 2026-10-02T17:18:40.746Z
updated_at: 2026-10-03T20:38:31.248Z
closed_at: 2026-10-03T20:38:31.248Z
close_reason: null
resolution: null
duplicate_of: null
---
Experiment-loop campaign: fixed benchmark (several directions of 3-4 certificates), verify.cpp timed as a black box on the same directions, pre-declared accept rule, hypotheses kept and rejected recorded in packing/benchmarks/measure-verifier/.

## Notes

Campaign packing/benchmarks/measure-verifier: H-001..H-011, exp-001..exp-013. Accepted H-002, H-006, H-007; rejected H-001, H-004, H-005, H-008, H-009, H-010, H-011. Standing build c2: 43x less CPU than verify.cpp on whole rect_n32_L595, 28.8x on six single directions (loaded host). Headline for an idle runner: bench_measure_verifier --headline. Open lead: lemma R7 cuts boxes 27-37% but costs as much in enclosures.
