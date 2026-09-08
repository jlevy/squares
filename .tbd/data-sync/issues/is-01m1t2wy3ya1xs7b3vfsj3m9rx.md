---
type: is
id: is-01m1t2wy3ya1xs7b3vfsj3m9rx
title: "Re-run the BC-219 preflight when PR 87 merges: it changes two frozen named inputs"
kind: task
status: open
priority: 1
version: 1
labels:
  - planning
dependencies: []
parent_id: is-01m1t2sgqmantgyx59knjxqheg
created_at: 2026-09-06T00:46:37.677Z
updated_at: 2026-09-06T00:46:37.677Z
---
PR 87 (claude/efficiency-block-gate-cost) moved from 5ab10a1a to d5bb2235 after agenda-024's last recorded head, and its delta against main modifies operating-rules.md (adds OR-12 through OR-14) and AGENTS.md, both in the BC-219 launch manifest, plus the ledger renderer (sqpack.campaign.ledger), the agenda map, SYNOPSIS.md, the agent-session schema and a new session-gate check. Agenda-024's own rule returns BC-219 to preflight on any upstream change to a named input. Record the head movement and disposition now; when PR 87 reaches main, re-hash the manifest, regenerate ledger.md and agenda-map.md, adopt the new session-record requirements for BC-225/239/249, and only then dispatch T+0.
