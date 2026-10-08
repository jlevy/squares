---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 11
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-08T23:37:43.854Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

47records-tier steps, full static floors,67mandatoryChromium checks and the n211/324actualPDF reviews pass. Data committed d32a825de4cea6967f1c8e754e91eebbd20293d2 and pin committed92f82467d; final324exports use v0.5.0-d32a82. All three source/preview/review lanes are coordinated; 100legacy contribution fix is source-clear under think-4yfk, boundedgreen verification active after own-cache cleanup restored a tiny allocation. Externalvolume was down to32MiB and refused mkdir with ENOSPC; deleting only inactive task caches/Chromiumfixture restored51MiB, still insufficient for broad pre-push validation. Unique evidence is retained under agent-evidence/squares-atlas-cleanups-01a11c30/final. PRbody is prepared but unpublished. Next: finish100focusedchecks/exports/aliasreceipt and visualQA, run fresh complete change-reachable --push gate after ≥1GiB free, commit source/exports, pushcodex/atlas-triangle-default, create/attach full-context PR, wait requiredCI+complete hostedcheckpoint at exacthead. No merge requested or performed.
