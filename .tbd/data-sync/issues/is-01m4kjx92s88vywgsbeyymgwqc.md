---
type: is
id: is-01m4kjx92s88vywgsbeyymgwqc
title: Audit upstream rendering precedence in website integration
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T18:58:50.583Z
updated_at: 2026-10-10T19:01:45.125Z
started_at: 2026-10-10T18:59:32.325Z
---
Before integration, verify website branch is fully committed/pushed. Map origin/main PDF, square and Atlas rendering improvements against website changes; preserve upstream rendering semantics and this branch website organization. Current fetched origin/main af17208c0 is already ancestor of clean d3c99face; audit semantic overrides and await identification of any pending upstream commit before merge. Track concrete resolutions and exact-head validation.

## Notes

Read-only integration map completed by three agents, including Astra. Website HEAD d3c99face8fa81fd6ad265111265e4f6a6067106 equals its pushed origin branch and is clean. Fetched origin/main af17208c02b08f343199ac102401d40278cf0dfc is already ancestor, explicitly merged as second parent of eb9d1271c. Atlas cleanup worktree is clean at af17208c0. No local or formal remote stack membership. No new upstream commits to merge; user clarification about pending branch/commit remains outstanding.

Precedence map: retain upstream scientific Atlas/PDF assets, build_known_best_atlas.py, atlas_print_font.py, sqpack.render and dedicated placement/scale mathematics (all unchanged versus main). Preserve website section organization, single53 hero, S4 recent preview, Papers/PDF/video/documentation placement, About/navigation/legacy URLs, themed popovers and deep-link destinations. Resolve shared files by function/selector, never whole-file ours/theirs.

Meaningful remaining rendering divergence: homepage wrappedPlace in atlas-view.js and scoped site.css wrapping geometry, plus cropped-poster preview in overview_sections.py. If current main is the intended authority, smallest semantic reconciliation is reuse atlas_grid/_atlas_cell upstream split row/segment markup for homepage, preserve staged36→100→324→36 controls and shared FLIP, keep324 persistent case links, scope only URL/root state, use upstream place for both surfaces, remove homepage wrap/crop payload and CSS. Preserve no-JS homepage36 rows; do not inherit dedicated no-JS reveal-all. Narrow screens would use upstream horizontal pan. One worker owns coupled overview_sections.py, atlas-view.js, homepage-atlas.js, site-atlas.d.ts, site.css, homepage.css; separate review verifies website organization and renderer semantics. No scientific data/PDF generator or dedicated atlas-grid change needed.

No source edits, merges or tests performed during audit. Wait for target clarification/finalized upstream content before further integration; current branch and green exact-head PR462 remain intact.
