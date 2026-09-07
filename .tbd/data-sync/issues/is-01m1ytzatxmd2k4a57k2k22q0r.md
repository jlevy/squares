---
type: is
id: is-01m1ytzatxmd2k4a57k2k22q0r
title: Reconcile incoming PR110 Session096 identity collision after it lands
kind: chore
status: open
priority: 2
version: 1
spec_path: packing/campaign/agendas/agenda-027-compatibility-and-restricted-families.md
labels: []
dependencies: []
parent_id: is-01m1ythhcq8vqfdk9zhaz8h2k8
created_at: 2026-09-07T21:04:19.805Z
updated_at: 2026-09-07T21:04:19.805Z
---
Read-only check found open PR110 ecd4a035 session-096-residual-skeleton.md and codex-task-tree-session-096.yaml collide with landed PR112 Session096 Stromquist review and receipt path at4620e483. PR111 also has a known separate Session093 collision tracked by think-rzek. Preserve source identities and complete references/receipt attribution; never overwrite a landed session to integrate another one. Monitor owner corrections before merge; if still present when landed, make a scoped integration repair and validate the full record set. Session097 is newly owned by this separate kernel-pricing branch.
