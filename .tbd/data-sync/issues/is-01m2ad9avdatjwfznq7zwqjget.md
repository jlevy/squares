---
type: is
id: is-01m2ad9avdatjwfznq7zwqjget
title: Validate and publish the reconciled PR149 head
kind: task
status: in_progress
priority: 1
version: 3
delegate: root integration lane
labels: []
dependencies: []
parent_id: is-01m26rygs7f0s76v147x0px4cd
created_at: 2026-09-12T08:56:00.620Z
updated_at: 2026-09-12T09:43:02.385Z
---
Run focused unit, lint, type, live-browser geometry, queue-watchdog, exact-head pre-push, hosted CI, and the full research checkpoint on the combined PR149 revision. Push without overwriting concurrent author work, update the PR title and body with exact costs and evidence limits, verify the PR remains stacked on PR148 and mergeable, then close and sync every completed bead.

## Notes

Final candidate head is 237c4023, 9 files and 832 insertions/50 deletions above PR148. Thirty-six focused tests pass, Ruff and BasedPyright are clean, D-490/D-491 generated views and synopsis agree, the exact records tier passes 32/74 in 88.80 seconds, and the exact rebuilt Chromium receipt reports 13 held fonts, 450 targets, 369 bases, every base hidden before and visible after, root_watchdog_paused true, and zero findings. A sandboxed pre-push attempt ran 936.97 seconds and failed its reachable-test step because macOS denied multiprocessing forkserver Unix-socket binding; that attempt is environmental evidence only. The unchanged exact head is now running the required unsandboxed pre-push gate as session 70515. Push, PR metadata, fresh hosted CI, full checkpoint, and final bead sync remain.
