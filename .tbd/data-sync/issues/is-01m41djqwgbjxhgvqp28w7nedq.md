---
type: is
id: is-01m41djqwgbjxhgvqp28w7nedq
title: "Papers: OpenGraph image and details for the optimality paper and the explainer"
kind: task
status: closed
priority: 2
version: 9
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T17:39:22.640Z
updated_at: 2026-10-06T08:31:08.820Z
closed_at: 2026-10-06T08:31:08.807Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): Notes say it closes when #334 merges: #319 MERGED 2026-10-04T02:51Z and #334 MERGED 2026-10-04T06:25Z; check_published_site.py on origin/main requires og:image/type/size/alt on every served page, including papers/n11-optimality-review.html and the explainer
resolution: null
duplicate_of: null
---
The n = 11 optimality paper (papers/n11-optimality-review.html) and the lower-bounds explainer publish no og:image or description. Give each a link preview with an image drawn for it or the site's card, from the same head builder the site pages use.

## Notes

Merged in jlevy/squares#319 (ebe5415a7) without its review's fixes; those are in jlevy/squares#334 (forwarders from their page's record; publish checks the assembled site). Closes when #334 merges.
