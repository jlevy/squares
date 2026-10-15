---
type: is
id: is-01m4zhwv1epw2mebdd065xrt37
title: Fix News bookmark regression oracle for a newest S3 article
kind: bug
status: closed
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zaazfxmv8px64xvdvdqnc7
hold: null
hold_until: null
created_at: 2026-10-15T10:32:00.813Z
updated_at: 2026-10-15T11:15:51.138Z
started_at: 2026-10-15T10:32:16.664Z
closed_at: 2026-10-15T11:15:51.138Z
close_reason: Delivered and reviewed in PR617, merge f97bc0b199e2493b0d84ba51f512e2b406b73021. Pages run38722914631 and full main Packing38722914629 succeeded; hosted verify-deployment succeeded10:59:54UTC. Live index/news/papers HTTP200 v0.7.5 smoke retained in news-live-v075-smoke.json. Includes shared article headers/original dates, compact filters/topics/meters, site fonts, concurrent adoption news and bookmark oracle.
resolution: null
duplicate_of: null
---
PR617/e063 frontend CI 38719526145 passed 423 cases but two viewport variants timed out in the legacy About bookmark assertion. New first article is S3; production correctly forwards to news.html?news-s=3%2C4%2C5#anchor so it is visible despite the S4/S5 default. Test expected an exact query-free URL, inherited from when first article was S4. Select expected bookmark behavior without assuming newest significance; retain exact path/fragment, required score/filter and visible/expanded target assertions. No production behavior, timeout or assertion weakening. Run both native viewport regressions and relevant filtering/forwarding tests.
