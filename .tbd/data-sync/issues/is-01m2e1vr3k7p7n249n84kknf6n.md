---
type: is
id: is-01m2e1vr3k7p7n249n84kknf6n
title: "R2/R3: bind retained reader proof copies to checked admission bytes"
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m2b884n0ms50xp93q6aaps1g
created_at: 2026-09-13T18:53:18.834Z
updated_at: 2026-09-13T18:53:18.834Z
---
Exact-head verifier review at 878e18d0 showed a copy-boundary mutation after admission can replace retained profile-1 proof with {} while retain reports accepted. Recheck copied command, stream, status, proof, and admission bytes against the checked originals and add deterministic failure injection.
