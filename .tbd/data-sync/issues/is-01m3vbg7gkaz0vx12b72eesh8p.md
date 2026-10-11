---
type: is
id: is-01m3vbg7gkaz0vx12b72eesh8p
title: "Site nav: the site name sits on the same baseline as the tabs"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T09:07:36.580Z
updated_at: 2026-10-01T10:13:09.275Z
closed_at: 2026-10-01T10:13:09.259Z
close_reason: "24ff0a10a, merged into the follow-up branch claude/site-polish-3 (73f454837): the site name stands on the links' baseline through baseline alignment and a shared line height; measure_site_pages gains a baselines mode and preview_site a baseline check."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: the text of the site name on the nav bar should have the same baseline as the tabs. It doesn't look aligned. Measure the text baselines of the site name and of each tab label in Chromium at 1280, 768 and 390 (a baseline probe, not box edges); align them with baseline alignment in the bar's layout (align-items: baseline or equivalent), not with a pixel nudge, so it holds when the sizes change (think-lk8b); the logo mark, if any, is centred on the name's text without moving the baseline; pin with a browser test that the baselines agree within half a pixel.
