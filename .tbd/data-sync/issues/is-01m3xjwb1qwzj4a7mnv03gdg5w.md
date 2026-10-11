---
type: is
id: is-01m3xjwb1qwzj4a7mnv03gdg5w
title: "Overview atlas: drop the two notes under the grid (the triangle's row key and 'Every case … is also in the frontier survey')"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T05:55:02.325Z
updated_at: 2026-10-02T07:09:30.751Z
closed_at: 2026-10-02T07:09:30.751Z
close_reason: "Merged in jlevy/squares#304 (b27bb27f5, merge 81cb5716): the triangle key and the line under the atlas expander are gone."
resolution: null
duplicate_of: null
---
Owner, 2026-10-02: 'and drop these notes, tehy are obvious, from the overview below the survey: Each row ends at a perfect square, where the best packing is the plain grid, and holds the cases that need a square of that side: 2 to 4 need side 2, 5 to 9 side 3, and so on. / Every case from n = 1 to 324 is also in the frontier survey, and each has a case record.' Both sit under the atlas grid on the Overview: the first is the Triangle view's key (.site-atlas-key), the second the line under Show More. Remove both, keep the Show More / Show Less button's spacing right without them, and keep the links they carried reachable (the Frontier Survey section directly below links the Frontier page; each tile opens its case record). Update the tests and paper-design.md that pin them.

## Notes

2026-10-02 10:10 UTC, branch claude/ladders-to-results, draft PR #304: done, committed after c05e0202e. The Triangle view's key (ATLAS_TRIANGLE_KEY) and the line under the expander are gone from atlas_grid(), with their CSS and the probe's key_shown; the expander's row ends the block. Each tile opens its case record; the Frontier page is a page card (think-ec5k). test_site_atlas_views and the Overview's atlas tests pass (49). Shots of the atlas foot in Grid/Triangle, collapsed/expanded, at 1280/390 on the final head.
