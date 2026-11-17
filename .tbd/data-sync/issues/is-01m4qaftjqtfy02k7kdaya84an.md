---
type: is
id: is-01m4qaftjqtfy02k7kdaya84an
title: "check_scroll_restoration: wait for the reload's own navigation, as #520 did for result filters"
kind: bug
status: closed
priority: 3
version: 4
delegate: w-records-1026
labels:
  - site
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T05:48:38.865Z
updated_at: 2026-10-26T10:25:23.656Z
started_at: 2026-10-26T10:18:09.589Z
closed_at: 2026-10-26T10:25:23.656Z
close_reason: "Done in #827 (4454e938a, merged at 909ddc76e): check_scroll_restoration waits on the main frame's load event, which a same-document navigation never fires. #539 closed with its final reply (issuecomment-6413623970)."
resolution: null
duplicate_of: null
---
From #520 review A1: packing/devtools/check_scroll_restoration.py:130 uses expect_navigation without a URL around a page reload, so KPress's scroll-stamp replaceState (vendor/kpress/src/kpress/format/static/js/history.js:292-294) can satisfy it early, the race #520 fixed in tests/test_site_result_filters.py. Not reproduced yet.

## Notes

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): https://github.com/jlevy/squares/issues/539 (label bug). Tracker https://github.com/jlevy/squares/issues/544.
