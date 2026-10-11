---
type: is
id: is-01m21brwj6et9vbnf7fvnpva2x
title: Keep queued math hidden through bootstrap recovery
kind: bug
status: in_progress
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: kpress_font_pipeline
labels: []
dependencies: []
parent_id: null
created_at: 2026-09-08T20:36:23.236Z
updated_at: 2026-10-06T08:21:43.929Z
---
Pages34274946315 exposed a real slow-startup gap: the3s root recovery timer can reveal prepared formulas whose queued hydration has not begun. Give collected static targets independent pending visibility until completion or readable fallback, preserve the runtime deadline and no-JS behavior, and retain a delayed-queue/held-font regression. Delegate kpress_font_pipeline; independent review caption_rendering.

## Notes

This remains a broader product-behavior bead. PR149 diagnostic geometry failure mixed a test-harness artifact with the independent page watchdog: the artificial probe delayed KPress entry past three seconds, while the retained artifact did not timestamp the actual expiry, and production has no equivalent interceptor. The combined PR149 fix will pause the watchdog only inside that artificial geometry control and will retain the separate queue-watchdog control with the real timer active. Do not close this product bead from geometry-probe evidence alone; reassess its original acceptance criteria after the combined live and hosted runs.
