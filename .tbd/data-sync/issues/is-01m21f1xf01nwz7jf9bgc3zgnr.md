---
type: is
id: is-01m21f1xf01nwz7jf9bgc3zgnr
title: Review math loading complexity before release
kind: task
status: in_progress
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: kpress_font_pipeline
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T21:33:44.799Z
updated_at: 2026-09-08T23:18:41.008Z
closed_at: 2026-09-08T23:04:43.192Z
close_reason: Independent architecture review completed and unused shipped diagnostics removed. KPress retains one client renderer with optional host preparation; new formulas require no font rebuild. The exact Linux artifact passed all 29 Mac geometry cases, and the final baseline fix reuses existing measured dimensions and KaTeX struts. Canonical architecture is merged in KPress PR64.
resolution: null
duplicate_of: null
---
Owner is concerned that the working page relies on an overengineered or brittle font pipeline. Perform a bounded independent architecture review of build-time KaTeX rendering, geometry reservations, saved font variants, cached font readiness and platform rendering assumptions. Identify removable machinery and concrete release blockers; preserve the working page and do not start a replacement rendering framework.

## Notes

Latest owner request asks for a systematic upstream-ownership pass. The earlier simplicity/runtime review is complete. Reopened for a bounded review of the final font-size, macOS weight, native scroller and measured-strut baseline changes against KPress 4a868bb, confirming every generic defect is fixed or documented upstream and host-only preparation remains in Squares. Delegated to kpress_font_pipeline while final PR CI runs.
