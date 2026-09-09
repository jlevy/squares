---
type: is
id: is-01m21dyxvmcggme4gkh8j849hx
title: Preserve reading position when the explainer reloads
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: font_pr_history
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T21:14:38.322Z
updated_at: 2026-09-09T03:00:31.095Z
closed_at: 2026-09-09T03:00:31.095Z
close_reason: "Implemented, reviewed, merged in Squares PR #135 (merge 171bba339321b8d63d85a59ab5f2db946270be0e) with reusable work in KPress PR #68 (merge a6203389c0a6d1f6e542b1f50fa177121eae7f4a). All PR and post-merge CI passed; Pages serves edition 171bba33; live publication 34/34 and delayed-font smoke pass. HTML/PDF opened locally. Native reload retains 3000px exactly in Chromium, Firefox, and WebKit with JS on/off. Bullet raster-shape follow-up think-x65m remains open because measured geometry is already square."
resolution: null
duplicate_of: null
---
User reports that Cmd-R while scrolled lower on the local d122d19c preview returns the page to the top. Preserve normal browser reload scroll restoration; inspect hash/history/picker initialization and startup layout before adding manual scroll storage. Delegate font_pr_history.
