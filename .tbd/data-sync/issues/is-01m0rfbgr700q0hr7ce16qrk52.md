---
type: is
id: is-01m0rfbgr700q0hr7ce16qrk52
title: "D071: generated session reports overwrite history and are not durable"
kind: bug
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-process
  - documentation
dependencies: []
parent_id: is-01m0r7q3zk8x6cg4e30d149698
created_at: 2026-08-23T23:30:07.750Z
updated_at: 2026-08-23T23:47:53.242Z
---
runner.py writes every unattended-session handoff to campaign/session-report.md, overwriting the prior one, and the path is not a durable tracked history. Define a versioned session record for agent/delegation work and separately repair runner-report archival before unattended scale-up.

## Notes

2026-08-23 partial repair: versioned soft-schema agent-session artifacts now preserve the outer agent/delegation loop, and the generated ledger indexes them. The numeric campaign runner still overwrites campaign/session-report.md; keep D-071 open until its unattended reports use unique append-only paths and a regression proves history is retained.
