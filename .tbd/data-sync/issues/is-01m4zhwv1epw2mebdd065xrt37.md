---
type: is
id: is-01m4zhwv1epw2mebdd065xrt37
title: Fix News bookmark regression oracle for a newest S3 article
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zaazfxmv8px64xvdvdqnc7
hold: null
hold_until: null
created_at: 2026-10-15T10:32:00.813Z
updated_at: 2026-10-15T10:32:16.665Z
started_at: 2026-10-15T10:32:16.664Z
---
PR617/e063 frontend CI 38719526145 passed 423 cases but two viewport variants timed out in the legacy About bookmark assertion. New first article is S3; production correctly forwards to news.html?news-s=3%2C4%2C5#anchor so it is visible despite the S4/S5 default. Test expected an exact query-free URL, inherited from when first article was S4. Select expected bookmark behavior without assuming newest significance; retain exact path/fragment, required score/filter and visible/expanded target assertions. No production behavior, timeout or assertion weakening. Run both native viewport regressions and relevant filtering/forwarding tests.
