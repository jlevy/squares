---
type: is
id: is-01m20wc9s2gcb2acab0n391wft
title: Fix stretched list markers introduced by kpress font merge
kind: bug
status: in_progress
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-08T16:07:22.136Z
updated_at: 2026-09-08T16:08:47.812Z
---
Review of merge 33cd4760 / PR 128: upgraded kpress draws filled CSS square markers, but explainer-shell overrides their height to 1lh. This makes every unordered-list bullet a vertical bar on screen and in print. Correct shared CSS and extend existing layout validation to detect stretched/missing marker dimensions, including a negative control.
