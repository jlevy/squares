---
type: is
id: is-01m23a765at8xvgz842wkh5wcx
title: Keep title-math PDF at the canonical 17 pages across platforms
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-09T14:47:43.528Z
updated_at: 2026-09-10T02:29:44.559Z
closed_at: 2026-09-10T02:29:44.557Z
close_reason: "Merged Squares PR #146 as 93af1e4d. Exact deployed artifact passed 34/34 checks and the PDF is 17 pages; CI now rejects future page-count drift."
resolution: null
duplicate_of: null
---
After Squares PR #143 merged, the exact GitHub Pages artifact at d47882cf passed its content/link contract but rendered as 18 pages on hosted Linux while the reviewed macOS PDF is 17. Compare page boundaries and typography metrics, identify the title-math trigger, and restore the canonical 17-page pagination without undoing mathematical italic s(11) or adding brittle platform-specific spacing. Extend CI so the hosted PDF page count cannot drift silently.

## Notes

Exact PR143 deployment reproduced at 18 pages on macOS and hosted Linux. Prepared title math enlarged the h1 line box by 4.34375px, pushing break-inside:avoid Figure 1 to page 2 and cascading to 18 pages. The title-only 1.05em reservation with derived -0.138em alignment restores the old geometry exactly while preserving the italic KaTeX s. Local two-render PDF check passes at 17 pages; CI and deployed-site checks now require exactly 17.
