---
type: is
id: is-01m5jn6b695wqc6sn8t3n0ts57
title: Site identity = git commit + its ISO committer time in footer and similar places; remove DATA_REVISION and release_pin (spec PR 3)
kind: task
status: open
priority: 1
version: 1
labels:
  - release
dependencies: []
parent_id: is-01m5jbt0g3a824950bggsqqjtc
created_at: 2026-10-22T20:35:12.201Z
updated_at: 2026-10-22T20:35:12.201Z
---
Owner: footer shows the git commit and that commit's ISO timestamp; same pair wherever the exact site version is captured. Spec §6 PR 3 (pages.yml scope outputs, --source-commit/--source-time).
