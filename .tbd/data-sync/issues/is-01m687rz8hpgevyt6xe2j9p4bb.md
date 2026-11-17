---
type: is
id: is-01m687rz8hpgevyt6xe2j9p4bb
title: "Owner decision: PR #744 (atlas expander removal + size rule) - close as superseded by #746, or apply the 23 Oct rule to #746's follow zoom"
kind: task
status: open
priority: 3
version: 1
labels:
  - owner-decision
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-10-31T05:44:00.016Z
updated_at: 2026-10-31T05:44:00.016Z
---
Merging main into #744 gives 23 conflicts with #746 (scroll-following Atlas, merged 2026-10-23 cc91ee1b8), which already removed Show More/Less and has automaticSize = wideScreen ? medium : small (atlas-view.js:817). Left in #744: the rule's derivation (rowWidth/automaticSize with Node tests), the measuring tool's row-share report, docs. Open: on main an untouched Triangle reached from the top opens at XL and zooms to Small at every width; the owner's words 'on a wide screen, we should never go all the way to small' may be about that zoom. Options: (a) static-only rule (no behaviour change; PR claim misleading), (b) stop the follow zoom at Medium on wide screens / Small on narrow by the half-row test (changes #746 behaviour; fresh branch), (c) close #744 as superseded. think-rk91 records the 23 Oct stop: atlas visuals are another agent's work. No commit or push made 2026-10-31.
