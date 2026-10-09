---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 24
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
child_order_hints:
  - is-01m4fgak1gswjj6et81wfndgrm
  - is-01m4fgam2ghc99ka4m1nbjwt4c
  - is-01m4fgamsz4gh4nf00hbmt339k
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-09T06:22:12.345Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Latest complete right-aligned revision is committed at source 87b546, pin d832ce8, and assets 002a891162690beb0724a371cf8b87a084bfb22d. Actual PDF QA passed for 18 complete uniform rows, left-aligned information, unchanged packing geometry and grid gap, and consistent body typography; both PDFs contain no URI annotations. Maintained integrated preview passed and latest PDF is selected in Finder. Full pre-push at 002 was interrupted when spud-ext1 disconnected; its partial receipts are retained and are not a passing gate. It also caught a test probe-loader call and an invalid Ruff environment setting. The test-only fix passes focused scanner, negative control, lint, and types and is awaiting senior review/root commit; RUFF_NO_CACHE will be true on the complete normal-retention rerun. User remounted the drive; write/fsync/unlink verified. No PR or push yet. Required full pre-push, hosted fast/deferred checkpoint, formal review publication, and final merge-ready sweep remain. The epic remains open; no GitHub merge is authorized.
