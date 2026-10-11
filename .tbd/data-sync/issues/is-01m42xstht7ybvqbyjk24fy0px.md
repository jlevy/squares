---
type: is
id: is-01m42xstht7ybvqbyjk24fy0px
title: "PR #305 A4: index page inlines 51 regularized tiles; ceiling raised to 4.7 MB"
kind: bug
status: closed
priority: 2
version: 5
labels:
  - deferred
dependencies: []
parent_id: null
created_at: 2026-10-04T07:42:06.394Z
updated_at: 2026-10-06T08:43:55.263Z
closed_at: 2026-10-06T08:43:55.263Z
close_reason: "Superseded by think-k8x9 (owner, 2026-10-04): the overview draws a regularized case once and no longer ships the house drawing, so the fetch planned here was not needed. origin/main tests/test_overview.py PAGE_CEILINGS puts index.html at 2,700,000 bytes, with the history in its comment."
resolution: canceled
duplicate_of: null
---
Review A finding A4 (Medium) on jlevy/squares#305: https://github.com/jlevy/squares/pull/305#pullrequestreview-5404831349

The index page inlines all 51 regularized atlas tiles in a <template data-atlas-regularized> (285,963 bytes; packing/devtools/overview_sections.py, the atlas block), which raised the index page's test ceiling from 4,300,000 to 4,700,000 bytes (packing/tests/test_overview.py). Without them the page is about 4.16 MB.

Fix: fetch the regularized tiles on the first selection of the Regularized layer, as result overviews are fetched via data-row-pop-src (packing/devtools/overview/row-popover.js), and restore the 4,300,000 ceiling.

Deferred from the review-A fixes (think-b13t) because it is a frontend change beyond the brief's 150-line bound: render_overview must emit a tile fragment beside index.html; overview/atlas-layer.js and atlas-grid.js must fetch it before swapping (and a ?layer=regularized deep link must not show house tiles first); check_published_site must require the fragment be served; and the site browser tests (tests/probes/site_atlas_views, test_site_atlas_views.py, measure_atlas_views and its probe, tests/node/overview_atlas_layer) read the template today.
