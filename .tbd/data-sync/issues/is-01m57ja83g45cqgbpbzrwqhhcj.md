---
type: is
id: is-01m57ja83g45cqgbpbzrwqhhcj
title: "PR #665 A2: refresh geometry-dependent derived records"
kind: bug
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m57j9xsga57szgfah5ex2bcd
hold: null
hold_until: null
created_at: 2026-10-18T13:13:15.631Z
updated_at: 2026-10-18T13:38:35.802Z
started_at: 2026-10-18T13:13:25.536Z
---
High; review A https://github.com/jlevy/squares/pull/665#pullrequestreview-5562201404. packing/frontier/n-068.md:64 and 27 other rigidity blocks, plus chunk-components census, are stale after adoption. Refresh owning tools and downstream views; verify check modes.

## Notes

Implemented in 391fdc594046d6090379de55ff552243f42ca6d5: owning writers refresh 28 rigidity blocks, component/partition census and dependent profile/taxonomy/overlays. Cheap check modes pass. Fresh census --check remains queued behind the coordinator-controlled local gate slot; no push.
