---
type: is
id: is-01m57ja83g45cqgbpbzrwqhhcj
title: "PR #665 A2: refresh geometry-dependent derived records"
kind: bug
status: in_progress
priority: 1
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m57j9xsga57szgfah5ex2bcd
hold: null
hold_until: null
created_at: 2026-10-18T13:13:15.631Z
updated_at: 2026-10-18T14:48:15.245Z
started_at: 2026-10-18T13:13:25.536Z
---
High; review A https://github.com/jlevy/squares/pull/665#pullrequestreview-5562201404. packing/frontier/n-068.md:64 and 27 other rigidity blocks, plus chunk-components census, are stale after adoption. Refresh owning tools and downstream views; verify check modes.

## Notes

Fixed by owning writers in391fdc594, plus bf93722b1 downstream composite refresh. Rigidity, components/partitions, profiles/taxonomy/overlays are current. Fresh census --check passes100 records. Composite diff is exactly28 rigidity assessment scope strings, with no total changes, and owner --check passes. Four concrete gate regressions pass on clean2890be7fa. Broader rerun/CI/disposition still pending.
