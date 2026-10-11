---
type: is
id: is-01m3wffzcesehcgxce8hewhhp7
title: Large generated assets are regenerated on demand, not on every data commit
kind: task
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T19:36:37.004Z
updated_at: 2026-10-01T22:34:34.500Z
closed_at: 2026-10-01T22:34:34.461Z
close_reason: "jlevy/squares#285 merged 2026-10-01 (main 69c79ed81): a poster states the data it was drawn from and is never re-stamped; a re-pin is one line (python -m devtools.release_pin --update, 0.3 s); posters are redrawn by --update-composites at a version bump; cut_release prepares a bump."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'let's be careful we are not taking large amounts of time to regenerate the pdf and large assets on every build, it may be slowing down dev cycle too much. that can be on demand.' Today every data-path commit must be followed by a re-pin that runs build_known_best_atlas --update and rewrites eight binary composites (PDF, SVG, four PNGs) for a stamp change; under load that took 10 to 18 minutes per branch on 1 October, and the eight binaries conflicted in every merge between open PRs. Measure where build time goes (the atlas re-stamp, the papers' PDFs, the films' posters, preview_site), then change the release contract so a data commit needs no binary regeneration: the stamp is carried outside the binaries or applied at deploy time, the composites are rebuilt on demand (a release, or when their own inputs change), and test_release still proves the published site names the data it shows. OR-14.

## Notes

Implemented on claude/release-assets-on-demand (41723049f), jlevy/squares#285 opened 2026-10-01: a poster states the data it was drawn from and is never re-stamped; re-pin is 'python -m devtools.release_pin --update', one line, 0.15 s CPU (was 967 s and eight binaries, 13.6 MB a commit; 48 such commits on main, 41 in three days); build_known_best_atlas --update-composites redraws posters in 44 s CPU at a version bump; devtools.cut_release prepares a bump. Records and edit tiers pass; 657 tests. Owner choices: posters may trail data between bumps (recommended yes); stamp keeps the data revision; dateline is the data's date; derive the pin in CI later; posters out of git only if needed.
