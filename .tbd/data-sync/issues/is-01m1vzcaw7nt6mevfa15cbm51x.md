---
type: is
id: is-01m1vzcaw7nt6mevfa15cbm51x
title: Preview explainer typography, PDF layout, and reading guide
kind: task
status: open
priority: 2
version: 13
labels: []
dependencies: []
created_at: 2026-09-06T18:23:36.838Z
updated_at: 2026-09-06T22:14:27.147Z
---

## Notes

The reviewed explainer changes are committed through c8f68b82 on codex/explainer-editorial-fixes, with origin/main integrated. PR #99 has not been updated, merged, or deployed. The user explicitly requested a preview before merge, so merge remains on hold.

Latest local preview changes raise the sans base to 19px (19/18 of prose), with shared figure text, captions, and footnotes at 18.05px on the web, regular 410, medium 550, and bold 680. Main title and subtitle scales are 1.5 and 1.25 (28.5px and 23.75px web), centralized beside the sans settings. The opening heading is New Result. The typography table in packing/devtools/templates/paper-design.md is updated. Print source-note spacing is compacted to avoid stranding the colophon. Shared gray web/black print colors and no persistent underlining remain. Generated HTML/PDF are in packing/site.

The 19px light desktop and dark 390px typography audits pass in screen and print with no size/color/overlap/underline findings. Print layout audit passes. CSS/document arithmetic reviewed; PDF pages 1 through 14 visually reviewed. The atlas intentionally occupies its own page, with existing spare space on page 2. Existing oversized LP equation still triggers global print scaling; tracked separately as think-215l and documented as a limit on absolute PDF font sizes.

Pre-push validation on the committed integrated tree passed 2474 behavioral tests, skipped 1, and deselected 55. Its only failed steps could not find ruff/basedpyright on PATH. Re-running the lint and type floors with the existing development environment on PATH passed Ruff, BasedPyright (0 errors/warnings), Clippy, and rustfmt. The larger final-review checkpoint and new-head PR CI remain for release after preview approval.
