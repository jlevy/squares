---
type: is
id: is-01m2e2zxfmfxgd5tb2zcbzn9rr
title: "R3: recheck coordinator.status success bytes at final retention boundary"
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m2dzxxp9raxnvx21zk6mawes
created_at: 2026-09-13T19:13:03.988Z
updated_at: 2026-09-13T19:32:08.548Z
closed_at: 2026-09-13T19:32:08.548Z
close_reason: "Integrated verifier repair 2ea77405 was independently accepted at exact verifier/test blobs: valid coordinator-shaped 22-file root passes, missing/extra files refuse, and status changes at check, digest, copy, and final boundaries refuse. Focused suite 15 passed. Actual positive-run bytes and evidence-commit OID remain separate operational gates; no profile/BC329 target ran."
resolution: null
duplicate_of: null
---
Independent exact-head review at verifier repair 0874e912 found an F5 status race: retention first reads coordinator.status as 0, then a mutation to 2 occurs before the digest snapshot; the copy and final digest accept 2 and return accepted. Add a target-free mutation control at the retain boundary and require the final copied/current status to remain the fixed success value 0. Keep the root otherwise byte/type exact. No positive profile or BC329 target.

## Notes

September 13 independent verifier rereview at 0874e912 REFUSED R3. Status 0→2 between first read and digest snapshot was copied and accepted. Sol max repair delegated in an isolated worktree; no positive profile/target. Durable rereview added to PR156.
