---
type: is
id: is-01m2e1vr3k7p7n249n84kknf6n
title: "R2/R3: bind retained reader proof copies to checked admission bytes"
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m2b884n0ms50xp93q6aaps1g
created_at: 2026-09-13T18:53:18.834Z
updated_at: 2026-09-13T19:32:21.447Z
closed_at: 2026-09-13T19:32:21.447Z
close_reason: Verifier repairs at 0874e912 and 2ea77405 were independently rereviewed on exact source/test blobs. The original six adversarial mutations now refuse, including shared-invalid identity, extra run record, nonzero retained status, stale staged tree, oversized JSON integer, and changed proof copy. The later R3 valid-root/status-race findings have separate accepted repairs. Operational postcommit OID and positive-run evidence remain open under parent gates.
resolution: null
duplicate_of: null
---
Exact-head verifier review at 878e18d0 showed a copy-boundary mutation after admission can replace retained profile-1 proof with {} while retain reports accepted. Recheck copied command, stream, status, proof, and admission bytes against the checked originals and add deterministic failure injection.
