---
type: is
id: is-01m1vzcaw7nt6mevfa15cbm51x
title: Preview explainer typography, PDF layout, and reading guide
kind: task
status: open
priority: 2
version: 12
labels: []
dependencies: []
created_at: 2026-09-06T18:23:36.838Z
updated_at: 2026-09-06T20:39:40.385Z
---

## Notes

Local explainer preview now has a documented paper typography profile beside its CSS: packing/devtools/templates/paper-design.md. Shared figure text, captions, and footnotes use Source Sans 3 at 0.95 of the 18.5px sans base (17.575px web), regular410, with medium550/bold680 emphasis. Supporting text and links are gray on the web and black in print; persistent underlining removed. Math keeps KaTeX fonts with inherited support color; semantic status/data colors remain. SVG labels compensate for viewBox scaling, get wider row spacing, scroll horizontally on narrow screens, and use a stable print viewport. Long Fig7 note now wraps as HTML. Atlas internal labels remain an explicit dense-artifact exception. HTML/PDF rebuilt, 14 pages. Desktop light and mobile dark supporting typography audits pass in screen/print, including overlap and underline checks; print layout clean; 43 explainer tests, Ruff, and BasedPyright pass. Final PDF pages 4,11,14 and enlarged contradiction equation visually reviewed. Earlier prose/credits/Further Reading/print changes remain. Existing oversized LP equation triggers global print scaling; tracked separately in think-215l and documented as a limit on absolute PDF font sizes. Preview changes remain local and uncommitted.
