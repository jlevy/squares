---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 12
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: blocked
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-08T23:49:00.194Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

The n=211 record reflection and narrowed 6523×6090 poster data are committed at d32a825de4cea6967f1c8e754e91eebbd20293d2, with the isolated release pin 92f82467d and edition v0.5.0-d32a82. All 47 records-tier steps, full pre-late static floors and 67 mandatory Chromium tests pass. The late 100-PDF contribution fix has six passing focused tests plus clean scoped lint/format/types; canonical 100 exports still need regeneration. Strong source/record/original PDF reviews are clear; the subsequent four-node 324 footer edit now awaits user reconciliation under think-h0xi, so earlier final footer receipts are not claimed as current. Deployment sparse-checkout audit is clear with no change needed. Earlier preview pages and assets were verified, but final changed assets/aliases need recopy. External volume refused mkdir with ENOSPC; safe cleanup of only inactive own caches restored about 50 MiB, insufficient for the mandatory broad --push gate (needs at least 1 GiB). No final passing --push result, source/export final commit, push or PR exists. Full-context PR body is being corrected to state current evidence and pending work. Next: user footer choice; restore external headroom; reconcile docs/source/tests if needed; regenerate both families and visually verify current PDFs; refresh preview assets; complete change-reachable --push; commit/push codex/atlas-triangle-default; create and attach PR; confirm required PR CI and full hosted checkpoint at its exact head. No merge is requested or performed. Unique evidence is retained under /Volumes/spud-ext1/agent-evidence/squares-atlas-cleanups-01a11c30/final.
