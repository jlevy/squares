---
type: is
id: is-01m1sj27q6t7hfz6dx74wvy5nn
title: Publish the explainer's generated Markdown as a hotlinked, LLM-readable artifact
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T19:52:25.574Z
updated_at: 2026-09-05T20:06:02.626Z
closed_at: 2026-09-05T20:06:02.626Z
close_reason: "Figures lost their border and the caption rule, keeping the padding. The explainer now publishes site/explainer.md: the substituted article, figures reduced to captions, one copy per figure rather than one per certificate, no HTML, unkerned maths, flowmarked in process via the pinned Python build. 49,131 bytes to 14,248. The MD chip points at it, served directly by Pages."
resolution: null
duplicate_of: null
---
The MD chip links to the template, which carries {{PLACEHOLDERS}} and is not what the page says. Publish the substituted Markdown to site/ so Pages serves it directly (no GitHub blob wrapper), and point the chip there. Requirements: flowmarked; clean math with no KaTeX kerning artifacts; HTML used correctly so it reads well as text; context-efficient for pasting into an agent, accepting that graphics do not carry. Needs a decision on the interactive apparatus (canvas stages, control panels, the chip row) and on the per-certificate figure duplication the picker creates.
