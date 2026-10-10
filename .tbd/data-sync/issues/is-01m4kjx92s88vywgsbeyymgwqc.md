---
type: is
id: is-01m4kjx92s88vywgsbeyymgwqc
title: Audit upstream rendering precedence in website integration
kind: task
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T18:58:50.583Z
updated_at: 2026-10-10T19:21:42.215Z
started_at: 2026-10-10T18:59:32.325Z
---
Before integration, verify website branch is fully committed/pushed. Map origin/main PDF, square and Atlas rendering improvements against website changes; preserve upstream rendering semantics and this branch website organization. Current fetched origin/main af17208c0 is already ancestor of clean d3c99face; audit semantic overrides and await identification of any pending upstream commit before merge. Track concrete resolutions and exact-head validation.

## Notes

Read-only integration map completed by three agents, including Astra. Website HEAD d3c99face8fa81fd6ad265111265e4f6a6067106 equals its pushed origin branch and is clean. Fetched origin/main af17208c02b08f343199ac102401d40278cf0dfc is already ancestor, explicitly merged as second parent of eb9d1271c. Atlas cleanup worktree is clean at af17208c0. No local or formal remote stack membership. No new upstream commits to merge; user clarification about pending branch/commit remains outstanding.

Precedence map: retain upstream scientific Atlas/PDF assets, build_known_best_atlas.py, atlas_print_font.py, sqpack.render and dedicated placement/scale mathematics (all unchanged versus main). Preserve website section organization, single53 hero, S4 recent preview, Papers/PDF/video/documentation placement, About/navigation/legacy URLs, themed popovers and deep-link destinations. Resolve shared files by function/selector, never whole-file ours/theirs.

Meaningful remaining rendering divergence: homepage wrappedPlace in atlas-view.js and scoped site.css wrapping geometry, plus cropped-poster preview in overview_sections.py. If current main is the intended authority, smallest semantic reconciliation is reuse atlas_grid/_atlas_cell upstream split row/segment markup for homepage, preserve staged36→100→324→36 controls and shared FLIP, keep324 persistent case links, scope only URL/root state, use upstream place for both surfaces, remove homepage wrap/crop payload and CSS. Preserve no-JS homepage36 rows; do not inherit dedicated no-JS reveal-all. Narrow screens would use upstream horizontal pan. One worker owns coupled overview_sections.py, atlas-view.js, homepage-atlas.js, site-atlas.d.ts, site.css, homepage.css; separate review verifies website organization and renderer semantics. No scientific data/PDF generator or dedicated atlas-grid change needed.

No source edits, merges or tests performed during audit. Wait for target clarification/finalized upstream content before further integration; current branch and green exact-head PR462 remain intact.

Implementation completed and pushed atop PR 462 as e8243e9ca2bf6e4740c31ac67ad331a6d503d2d0. Upstream af17208c02b08f343199ac102401d40278cf0dfc was already an ancestor; this change reconciles the remaining homepage rendering override rather than repeating the merge. Scientific data, PDF generators and scientific/PDF assets remain unchanged.

Homepage now reuses the dedicated Atlas's canonical _atlas_rows/_atlas_cell split-row/segment markup, compact standalone SVG images, place geometry and shared SiteAtlasView.change/FLIP. Removed wrappedPlace, the cropped-poster/gzip preparation path and scoped wrapping/palette CSS. Keep all 324 persistent canonical case links, stages 36->100->324->36, Small/Fixed rendering, case popovers, single 53 hero and website organization. Narrow screens use the upstream horizontal pan. Homepage no-JS shows 36 and Explore; dedicated no-JS still reveals all 324. Clicks require no markup preparation or layout fetch; lazy immutable SVG image requests may occur.

Focused evidence: four source contracts passed in 12.96s ; 25 shared-engine Node tests passed. First browser selection passed 10 contracts with four instrumentation failures in 90.53s (packing-pixel sample and incorrect engine-abort asset path). Those four oracles were corrected and the four affected checks passed in 68.07s. Stage counts/identity/immediate shared animation, pointer/popover links, reduced motion, live themes, no-JS and missing-engine fallback are green across 1280/390. Scoped Biome/ESLint, overview and homepage-probe TypeScript, Ruff/check-format and BasedPyright (0 errors, 0 warnings, 0 notes) passed; diffcheck passed. Astra's bounded review approved the frozen reconciliation; parent reports normal commit hooks passed.

Small source/browser/rerun/Python-type logs and the probe type configuration are preserved byte-for-byte in /Users/levy/.codex/visualizations/2026/10/08/01a11dc7-6f9d-7060-be5c-4cff21839702/process-review/p7c4-reconciliation/. session-floor-receipts.json records the retained Node/lint/type command outputs from the tool session; no checks were rerun for archival.

Exact-head CI for e8243e9ca2bf6e4740c31ac67ad331a6d503d2d0 is pending. Keep this bead open until all exact-head checks are green; full checkpoint, epic and process follow-ups remain open.
