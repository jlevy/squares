---
type: is
id: is-01m49ph1mprzwjqxe2r959cvbz
title: "A2: closed-world and append-only registry checks; tombstones for withdrawn rows"
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-06-site-urls-seo-performance.md
delegate: codex-pr395@spud10.local
labels:
  - pages
dependencies: []
parent_id: is-01m49ph0abvy6j16zcq4jse39y
hold: null
hold_until: null
created_at: 2026-10-06T22:49:39.734Z
updated_at: 2026-10-08T00:33:20.798Z
started_at: 2026-10-06T22:54:03.206Z
---
Lane A. Closed world in publish job and preview_site; append-only vs origin/main registry in push tier; tombstone pages for withdrawn results/cases instead of write_site pruning to 404.

## Notes

PR #395 review A2: required PR validation must enforce registry drift/history and selected-producer closed world, independent of skipped full-site publish. Add a negative missing-path regression. Review: https://github.com/jlevy/squares/pull/395#pullrequestreview-5450014385.
