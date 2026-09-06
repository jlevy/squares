---
type: is
id: is-01m1w6y3e81b1nyygpwm2yfbsr
title: Keep oversized display math from scaling the whole printed explainer
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-06T20:35:39.079Z
updated_at: 2026-09-06T20:35:39.079Z
---
The long covering-linear-program display in explainer-article.md reaches roughly 616 CSS px in the nominal 576px Letter print column. Chromium expands and scales the print layout, so CSS point sizes do not equal physical PDF sizes. Reflow the display within the column, verify absolute PDF text sizes using a retained diagnostic, and review pagination. Preserve shared figure/caption/footnote size and stable SVG print viewport. The current shared-role preview preserves prior 14-page flow and matches SVG/caption physical text size; this task owns removing the older global print-scaling behavior.
