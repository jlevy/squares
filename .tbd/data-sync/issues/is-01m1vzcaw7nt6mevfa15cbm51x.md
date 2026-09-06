---
type: is
id: is-01m1vzcaw7nt6mevfa15cbm51x
title: Preview explainer typography, PDF layout, and reading guide
kind: task
status: in_progress
priority: 2
version: 15
labels: []
dependencies: []
created_at: 2026-09-06T18:23:36.838Z
updated_at: 2026-09-06T23:18:09.739Z
---

## Notes

User approved merge and deployment end to end, with every link current.

PR #99 merged at 62f53438565f75c420eabd096a26014bc1fc3339 after standard PR validation 34064274054 and full deferred checkpoint 34064334605 passed on head 184f15475cb243fe2853efd5d28d1d1ca38d0f9d, base 8743cb0dce21314625f9a75f9934a600f21e6de9. The merge tree is identical to the checked head. Pages deployment 34065708315 passed. Live publication checker passed 26/26 checks against 62f53438, and the full link audit passed all 32 external URLs, 18 internal anchors, 2 repository fragments, and assets. All 17 repository permalinks name the deployed commit. Current content records 22 results, 15 apparently new, and 7 atlas lower bounds, with an accurate T-022 refinement note.

The actual deployed 14-page PDF was reviewed page by page. It exposed one Linux-only line wrap on page 4: the period and footnote after Trump’s upper bound began the next line. Follow-up PR #104 at 0ab655e5bf5304baaaff6ad642671b2621a9f3fa keeps the formula, punctuation, and source reference together with a nowrap span. No research content changed. All 43 explainer tests and all 45 selected push-tier steps passed, and the local regenerated PDF remains 14 pages. Independent review confirmed Markdown output remains unchanged after Flowmark. Hosted Pages build 34066362183 passed; required PR validation 34066362179 is running.

Remaining: merge #104 when required checks pass, verify its deployed revision and actual page 4 PDF, watch post-merge CI, then close and sync this task. The unchanged scientific surface retains the full checkpoint evidence above; affected rendering checks are rerun on the follow-up. The existing oversized display-math print scaling limitation remains in think-215l.

Accepted design: sans base 19px, shared figure/caption/footnote text 18.05px on web, weights 410/550/680, main title/subtitle scales 1.5/1.25, H2 1.2. Gray supporting text on web and black in print, no persistent underline. Opening section New Result. Colocated paper-design.md documents the settings and upstream candidates. Generated outputs are under packing/site; production is https://jlevy.github.io/squares/.
