---
type: is
id: is-01m21brwj6et9vbnf7fvnpva2x
title: Keep queued math hidden through bootstrap recovery
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: kpress_font_pipeline
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T20:36:23.236Z
updated_at: 2026-09-08T20:37:10.522Z
---
Pages34274946315 exposed a real slow-startup gap: the3s root recovery timer can reveal prepared formulas whose queued hydration has not begun. Give collected static targets independent pending visibility until completion or readable fallback, preserve the runtime deadline and no-JS behavior, and retain a delayed-queue/held-font regression. Delegate kpress_font_pipeline; independent review caption_rendering.
