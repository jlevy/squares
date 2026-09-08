---
type: is
id: is-01m21dyxvmcggme4gkh8j849hx
title: Preserve reading position when the explainer reloads
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: font_pr_history
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T21:14:38.322Z
updated_at: 2026-09-08T21:20:25.393Z
---
User reports that Cmd-R while scrolled lower on the local d122d19c preview returns the page to the top. Preserve normal browser reload scroll restoration; inspect hash/history/picker initialization and startup layout before adding manual scroll storage. Delegate font_pr_history.
