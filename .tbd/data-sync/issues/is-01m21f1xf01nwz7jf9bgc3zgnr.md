---
type: is
id: is-01m21f1xf01nwz7jf9bgc3zgnr
title: Review math loading complexity before release
kind: task
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: kpress_font_pipeline
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T21:33:44.799Z
updated_at: 2026-09-09T03:00:31.114Z
closed_at: 2026-09-09T03:00:31.114Z
close_reason: "Implemented, reviewed, merged in Squares PR #135 (merge 171bba339321b8d63d85a59ab5f2db946270be0e) with reusable work in KPress PR #68 (merge a6203389c0a6d1f6e542b1f50fa177121eae7f4a). All PR and post-merge CI passed; Pages serves edition 171bba33; live publication 34/34 and delayed-font smoke pass. HTML/PDF opened locally. Native reload retains 3000px exactly in Chromium, Firefox, and WebKit with JS on/off. Bullet raster-shape follow-up think-x65m remains open because measured geometry is already square."
resolution: null
duplicate_of: null
---
Owner is concerned that the working page relies on an overengineered or brittle font pipeline. Perform a bounded independent architecture review of build-time KaTeX rendering, geometry reservations, saved font variants, cached font readiness and platform rendering assumptions. Identify removable machinery and concrete release blockers; preserve the working page and do not start a replacement rendering framework.

## Notes

Latest owner request asks for a systematic upstream-ownership pass. The earlier simplicity/runtime review is complete. Reopened for a bounded review of the final font-size, macOS weight, native scroller and measured-strut baseline changes against KPress 4a868bb, confirming every generic defect is fixed or documented upstream and host-only preparation remains in Squares. Delegated to kpress_font_pipeline while final PR CI runs.
