---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 17
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-09T03:35:56.636Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Current approved integration and maintained pin are committed at 327aed41, with published main d43ea686d included and data pin 9c34421f. The complete current records gate passed all 48 selected steps in 62.25 seconds with zero skips or failures. Current source contracts pass 27 PDF tests and all 46 result-overview tests across two honest receipts; earlier 191 CLI and 19 budget/snapshot contracts also passed. Senior review covers 83 of 95 changed paths, with only 12 generated/deleted asset paths excluded, and found one P2 producer bug: update_selected writes the full figure before refusing a scoped refresh. Fix is tracked by think-59ta and must pass no-write-on-refusal regressions and independent confirmation. Current PDF assets passed actual full-page and cropped visual/text/ink checks but will be regenerated for the latest equal-font unlinked black footer and recent-first credits. The current website preview refresh is still in progress; old page HTML must not be called fresh. Finder has again revealed the dated 324 PDF. Automated browser navigation remains blocked; the original human-approved localhost:8799 server stays available for manual review. Full push gate, branch push, PR, exact-head hosted CI and full checkpoint remain pending. Original local-merge approval blocker is resolved. Keep the epic open for further requests; no GitHub merge authorized.
