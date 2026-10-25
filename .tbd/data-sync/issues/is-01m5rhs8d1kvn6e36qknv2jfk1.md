---
type: is
id: is-01m5rhs8d1kvn6e36qknv2jfk1
title: "PR #805 (merge): senior review A of the Fang Theorem A review mapping"
kind: task
status: closed
priority: 2
version: 4
delegate: c-rev-805-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5qsa0zpbykjt72q42fhz1fw
hold: null
hold_until: null
created_at: 2026-10-25T03:31:04.225Z
updated_at: 2026-10-25T03:47:06.518Z
started_at: 2026-10-25T03:31:08.705Z
closed_at: 2026-10-25T03:47:06.518Z
close_reason: "Review A of #805 posted (issuecomment-6393100033): approve with nits (A1, A2 Low; A3 suggestion)."
resolution: null
duplicate_of: null
---

## Notes

2026-10-25 c-rev-805-1024: Review A (senior, round 1) of #805 posted as a PR comment, https://github.com/jlevy/squares/pull/805#issuecomment-6393100033, at head b39a06378, base 4089f9587. Verdict: approve with nits. A1 Low: result-requests.yaml:23717-23718 says 'The issue calls the lemmas 1 and 2' but neither #797's body nor the author's comments name a lemma (the numbering was the record's own). A2 Low: #797's first withdrawn question has changes: file (23766) while its note says the answer could falsify no credit, lineage or file; check_requests --report prints that it could falsify the record's file. A3 suggestion: decide the k^{2/5} crossover exactly in fang_theorem_a.py (the sampled daniel_k25_crossover is no longer cited). Verified: 5/5 program digests; review doc flowmark-idempotent; V3/C1 matches T-163 and Ryu's RUNGS row; renames complete; construction/compare/check reproduce receipts; crossover 735,988/736,595 exact in integers over [3e5, 1e6); deficiency_family HOLDS; check_results ok; check_requests #797 3/3 closeable; read_through 00:49:19Z matches; 215 + 157 tests pass. Worktree removed.
