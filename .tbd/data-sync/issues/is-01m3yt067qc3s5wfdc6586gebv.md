---
type: is
id: is-01m3yt067qc3s5wfdc6586gebv
title: "W2-B: sqverify_fast point and segment atoms (mixed and linear certificates)"
kind: task
status: closed
priority: 2
version: 2
labels:
  - verifiers
dependencies: []
parent_id: is-01m3yrezbcgcr728c37fq49bvf
created_at: 2026-10-02T17:18:42.934Z
updated_at: 2026-10-03T01:37:46.326Z
closed_at: 2026-10-03T01:37:46.325Z
close_reason: |
  Milestone B done on claude/lane-w2-fast-verifier-wip. sqverify-fast admits formats M and L, bounds points and segments (SOUNDNESS lemmas B1-B3), runs direction zero by branch and bound when atoms are present (Z1, Z2), uses the per-bin domain for format M (lemma D), and its release audit reclassifies every item afresh (A3). All six replayed mixed and linear certificates verify at all 201 directions (benchmarks/measure-verifier/census-mixed/README.md); the retained n37 and n101 controls, near-threshold controls and fault injection are refused (devtools/check_sqverify_fast.py --only mixed).
resolution: null
duplicate_of: null
---
Milestone B: add point masses and uniform-linear segments with the core-containment rule, same tests, controls and benchmarks.
