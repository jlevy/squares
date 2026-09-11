---
type: is
id: is-01m28p88qyq83eek30pja3np54
title: "Phase 6E: the workbench moves into devtools, and the banner comes off"
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
created_at: 2026-09-11T16:54:14.013Z
updated_at: 2026-09-11T20:33:23.513Z
---
The generator is a script run by path and the instruments (compare_palette.py, grade_motion.py, measure_law.py, measure_greens.py, capture_stills.py, smoke_capture.py) sit beside it in the spike tree. They become devtools modules run with python -m, alongside build_workbench_site.py and capture_video.py which already are.

The banner that says the page is a prototype comes off as the LAST step of Phase 6, after A through D. It is what makes the current state honest, and removing it before the rest would make the page claim something that is not yet true.

Also here: the retained spike tree keeps its NOTES.md and its revision history, because that record is worth keeping; what moves is the code that is still running.
