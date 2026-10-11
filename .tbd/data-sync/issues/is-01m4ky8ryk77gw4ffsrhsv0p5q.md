---
type: is
id: is-01m4ky8ryk77gw4ffsrhsv0p5q
title: Propose upstream tbd ownership and lifecycle instruction contract
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-10-10T22:17:21.618Z
updated_at: 2026-10-10T22:50:05.450Z
closed_at: 2026-10-10T22:50:05.447Z
close_reason: Upstream instruction work is executing under think-nx5z and tbd-9fvc; user clarified that collaboration guidance must be opt-in and lightweight defaults preserved. Consolidated tracking avoids parallel implementation of the same proposal.
resolution: duplicate
duplicate_of: is-01m4kymmpjrq8shca52m1xv1vs
---
Audit think-qpm4 found route-specific claiming, no required ownership acceptance in delegation/handoff, missing start-of-session refresh and immediate post-commit sync, and unconditional closure wording. Proposed upstream change: one shared lifecycle contract in prime/skill/closing plus delegation, handoff, planning and commit shortcuts; unique per-agent identities; inspect claimed/skipped rather than exit status; explicit transfer coordination; sync at start, claim publication, each commit, handoff and end. Preserve project queue and coordinator rules. This is proposed follow-up, not implemented.
