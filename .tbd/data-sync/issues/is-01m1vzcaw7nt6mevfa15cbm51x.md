---
type: is
id: is-01m1vzcaw7nt6mevfa15cbm51x
title: Preview explainer typography, PDF layout, and reading guide
kind: task
status: in_progress
priority: 2
version: 14
labels: []
dependencies: []
created_at: 2026-09-06T18:23:36.838Z
updated_at: 2026-09-06T22:37:24.389Z
---

## Notes

The user approved the final preview and explicitly requested merge and deployment end to end, including checking all links. Changes are committed and pushed through 184f15475cb243fe2853efd5d28d1d1ca38d0f9d on codex/explainer-editorial-fixes, with origin/main 8743cb0dce21314625f9a75f9934a600f21e6de9 integrated. PR #99 has its final title/description. Standard PR validation (run 34064274054) and Pages build (34064274043) passed; complete checkpoint 34064334605 is running before merge. No deployment yet.

Latest local preview changes raise the sans base to 19px (19/18 of prose), with shared figure text, captions, and footnotes at 18.05px on the web, regular 410, medium 550, and bold 680. Main title and subtitle scales are 1.5 and 1.25 (28.5px and 23.75px web), centralized beside the sans settings. The opening heading is New Result. The typography table in packing/devtools/templates/paper-design.md is updated. Print source-note spacing is compacted to avoid stranding the colophon. Shared gray web/black print colors and no persistent underlining remain. Generated HTML/PDF are in packing/site.

The 19px light desktop and dark 390px typography audits pass in screen and print with no size/color/overlap/underline findings. Print layout audit passes. CSS/document arithmetic reviewed; PDF pages 1 through 14 visually reviewed. The atlas intentionally occupies its own page, with existing spare space on page 2. Existing oversized LP equation still triggers global print scaling; tracked separately as think-215l and documented as a limit on absolute PDF font sizes.

Pre-push validation on the committed integrated tree passed 2474 behavioral tests, skipped 1, and deselected 55. Its only failed steps could not find ruff/basedpyright on PATH. Re-running the lint and type floors with the existing development environment on PATH passed Ruff, BasedPyright (0 errors/warnings), Clippy, and rustfmt. Final changes passed packing-validate --push --since c8f68b82: 45 selected steps and 512 reachable tests. All 32 HTTPS targets returned 200; 18 internal anchors, 2 repository heading fragments, 4 local linked assets and the social-preview PNG resolve. All 17 repository permalinks name current head184f1547. No unresolved placeholders or stale repository pins. Retained content is current: 22 results, 15 apparently new, 7 atlas lower bounds, accurate T-022 refinement note. Hosted PDF is14pages with successful reproducibility, typography, and layout checks. Complete checkpoint remains before merge; then use devtools.check_published_site with the exact merged SHA to verify live HTML/Markdown/PDF/assets and repository links.
