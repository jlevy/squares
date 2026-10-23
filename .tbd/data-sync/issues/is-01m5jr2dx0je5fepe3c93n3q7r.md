---
type: is
id: is-01m5jr2dx0je5fepe3c93n3q7r
title: Prerender same-site pages on hover with speculation rules
kind: feature
status: closed
priority: 1
version: 4
delegate: claude-kind-mccarthy
labels: []
dependencies: []
parent_id: is-01m5jr2cr74kbbn71j05pqsgkd
hold: null
hold_until: null
created_at: 2026-10-22T21:25:29.631Z
updated_at: 2026-10-23T01:43:38.697Z
started_at: 2026-10-22T21:25:36.932Z
closed_at: 2026-10-23T01:43:38.692Z
close_reason: "Merged in https://github.com/jlevy/squares/pull/740 as 7ce902c6a (merge commit). Pages-only speculation rules (/, /*/, /*.html; not [download]) at moderate eagerness on every site page; papers/forwarders/workbench unchanged. Senior+performance review fixes in 912a97a03. Follow-ups: think-81h7 (workbench), think-0dws (Chromium acceptance check), think-15b4 (benchmark tool, mobile narrowing)."
resolution: null
duplicate_of: null
---
Add a <script type=speculationrules> with prerender, eagerness moderate (hover ~200 ms or pointerdown) to every site page head. Chromium (Chrome, Edge) builds the page in the background so the click swaps it in; other browsers ignore the tag. Measured with no DevTools attached (DevTools disables prerendering): index->results ~110 ms, results->atlas ~117 ms, atlas->index ~25 ms click-to-settled with the headroom fix. Static site, no analytics, no unload handlers, so prerendering has no side effects.

## Notes

2026-10-23 00:45Z: draft PR https://github.com/jlevy/squares/pull/740 at bb5014af2 (feat 5d9e4e198 + merge of main e929137a8). Rules from render_overview.speculation_rules_tag(), added by _site_head and static_content_page; head_tags unchanged so the four papers and the forwarders are byte-identical (release.py no-public-change record). check_site_scripts skips type=speculationrules. Test: test_site_head.py::test_every_page_prerenders_a_hovered_site_link. Local: 149 affected tests pass; --edit 67/68 (type floor OOM in container, 0 errors on changed files). Labels S2 + project. Workbench follow-up: think-81h7. Close on merge.
