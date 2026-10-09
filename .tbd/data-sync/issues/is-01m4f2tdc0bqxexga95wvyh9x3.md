---
type: is
id: is-01m4f2tdc0bqxexga95wvyh9x3
title: Align the theme gear with the navigation baseline
kind: bug
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels:
  - website
dependencies:
  - type: blocks
    target: is-01m4ex3gpzxxh9eqemc2r78p4e
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-09T01:00:41.727Z
updated_at: 2026-10-09T04:42:24.865Z
started_at: 2026-10-09T01:02:00.516Z
---
Correct shared theme gear alignment: owner confirms current gear is too high relative to navigation tab text. Align its visible glyph optically with the tab text baseline using rendered desktop/mobile evidence, not only box alignment. Preserve target size, menu anchoring, wrapped navigation, Headroom and all page shells. Verify bounded widths1280/390/320 and representative ordinary, direct-paper and Workbench headers; keep local draft refreshed.

## Notes

Corrected gear optical alignment with vertical-align:calc((1cap - 1.05rem)/2), retaining shared baseline wrapper, button geometry, menu anchor and Headroom. Prior icon measured2.32px high; final ordinary icon shifts2.625px downward with0.346px ink-center error. Five retained focused tests passed6.72s across1280/390/320 and6shells; Biome/strictTS/Ruff/BasedPyright/Flowmark clean. Live ordinary/direct-paper/Workbench allthreewidths optical/hitbox/menu andHeadroom passed. Workbench error0.348px; menu gap4px; button31.17pxwidth and34.59pxdesktop/32.31pxmobileheight retained. Root reviewed desktop/mobile ordinary screenshots, correctlycentered. Astra source/oracle review nofindings. Designsystem updated. Preview newimmutablef122f4d9f8022b95navCSS published acrossallHTMLrefs andWorkbench ownassets; oldassets preserved. Heroindexlatest11/53/203 retained. Evidence gear-optical-alignment.json andgear-after screenshots in durablevisualizationfolder. Localdraftonly; no commit/publication/merge.
