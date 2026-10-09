---
type: is
id: is-01m4fr5rgtmrjm5mvqbe6j90cn
title: Refine case popover math, status order, and navigation arrows
kind: task
status: in_progress
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-09T07:13:53.665Z
updated_at: 2026-10-09T07:46:05.737Z
started_at: 2026-10-09T07:14:10.664Z
---
Center the small Case Record label above a larger properly typeset n=count formula. Place case icons first, followed by the star and notes, then textual status tags such as proved. Give all bottom destination actions the same right-arrow design. Remove All cases from case navigation; make Atlas the case directory and forward old directory URLs while retaining individual canonical case records. Verify local desktop/mobile rendering, keyboard stepping, and compatibility destinations.

## Notes

Completed case presentation and Atlas directory changes in the local draft. All324 canonical case records have a centered prepared serif n=count heading, centered Case Record eyebrow, icons followed by star/notes then status tags, no All cases action, and three matching right-arrow destination buttons. Fixed the floated-close formatting context and generic sibling padding so article/math align with the panel; sticky close retains its hitbox and scroll/focus behavior. Six viewport/theme header checks and two sticky-close checks passed, with fresh desktop/mobile screenshots independently reviewed by root and Astra. Routing checks passed19Node,3result links,29browser and6static; unknown-selector rerun finishing after restoring preview files. All324 case records, current forwarders and116 regenerated result fragments are restored (two previously supplied result files preserved). Root HTTP checks for homepage, Atlas, case15, unknown-selector forwarder and T115 all returned200. T115 actual fetch smoke passed. Shared CSS refs verified. Astra approved bounded source changes; broad publication/history gates stay on think-xio5.
