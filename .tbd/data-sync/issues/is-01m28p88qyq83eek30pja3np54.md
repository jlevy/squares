---
type: is
id: is-01m28p88qyq83eek30pja3np54
title: Extract live workbench sources and retire the spike entry points
kind: task
status: open
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m2chahf57z4w9tj5gehbs0td
created_at: 2026-09-11T16:54:14.013Z
updated_at: 2026-09-13T05:00:51.787Z
---
The generator is a script run by path and the instruments (compare_palette.py, grade_motion.py, measure_law.py, measure_greens.py, capture_stills.py, smoke_capture.py) sit beside it in the spike tree. They become devtools modules run with python -m, alongside build_workbench_site.py and capture_video.py which already are.

The banner that says the page is a prototype comes off as the LAST step of Phase 6, after A through D. It is what makes the current state honest, and removing it before the rest would make the page claim something that is not yet true.

Also here: the retained spike tree keeps its NOTES.md and its revision history, because that record is worth keeping; what moves is the code that is still running.

## Notes

Owner-selected destination is top-level packages/workbench/ (2026-09-12). Migrate all live workbench-specific sources and tools, including Python build/capture/benchmark adapters, into that package. Shared sqpack library code remains a dependency. Do not add permanent flat devtools wrappers; only consumer-backed temporary compatibility entry points, retired through think-cqfc.
