---
type: is
id: is-01m4fx2qznxbkzt7z9wcagk3fb
title: Mirror Papers and About documentation sections on the homepage
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-09T08:39:37.715Z
updated_at: 2026-10-09T08:51:34.273Z
started_at: 2026-10-09T08:39:48.408Z
closed_at: 2026-10-09T08:51:34.269Z
close_reason: null
resolution: null
duplicate_of: null
---
Replace homepage Learn More with Papers including all registered readings; retain a separate PDFs section; add Squares Project Documentation mirroring About content/cards via shared rendering. Style every About H1 like The Squares Project title. Preserve video, resource cards and existing destinations; refresh draft.

## Notes

Homepage now uses shared paper_cards() for all four actual readings under Papers, retains separate PDFs and Video, and includes documentation_block() identical to About lead/five document cards. Removed obsolete homepage paper helper. About three H1s all use site-title, matching The Squares Project. Preserved learn-more alias and updated forward.js to honor real homepage documentation anchor. PlanL25/shared design updated and Flowmark applied. Nine narrow source assertions passed including exact shared-document comparison; two retained desktop/mobile heading-spacing/native-video checks passed1280/390. Node19 passed; Ruff/format, Biome, overview tsc, targeted BasedPyright clean. Direct index/About/Papers +47asset refresh, no pruning/corpusbuild; three live URLs HTTP200/current. Astra independent source/published inspection clean: equal reading targets, equal five document IDs/destinations, no duplicateIDs/matherrors, no homepageH3 and three AboutH1site-title.
