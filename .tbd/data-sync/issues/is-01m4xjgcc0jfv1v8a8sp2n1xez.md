---
type: is
id: is-01m4xjgcc0jfv1v8a8sp2n1xez
title: "#514 review B1: the headroom test measured 40 more results from the current page, so its room slid with every registration"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-10-14T16:04:12.288Z
updated_at: 2026-10-14T16:05:21.507Z
closed_at: 2026-10-14T16:05:21.507Z
close_reason: "fixed in 07fb14f66: test_overview holds results.html through RESULTS_ROOM_THROUGH = 200 results at the measured p90 row and average entry cost, and asserts site_urls' 1,150,000 exception equals PAGE_CEILINGS; site_urls.py's reason and docs/project/site-urls.md say 'through 200'"
resolution: null
duplicate_of: null
---
Review B of #514 (review 5520287797), finding B1: the headroom test measured 40 more results from the current page, so its room slid with every registration
