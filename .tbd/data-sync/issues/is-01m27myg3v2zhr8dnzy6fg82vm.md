---
type: is
id: is-01m27myg3v2zhr8dnzy6fg82vm
title: Reconcile the v0.4.0 explainer pagination after final claim additions
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m26sv4284ry42pyavjhmmzqs
created_at: 2026-09-11T07:12:10.874Z
updated_at: 2026-09-11T07:18:26.785Z
closed_at: 2026-09-11T07:18:26.784Z
close_reason: "Reproduced 22 pages on the exact PR #148 base and on the stacked #149 head, showing #149 did not add the page. Updated the reviewed count after the final claim links and C5 paragraph, passed 204 focused page/render tests, produced two byte-identical normalized PDFs with 22 pages and 24 embedded fonts, and visually inspected contact sheets for all 22 pages without clipping or blank-page regressions."
resolution: null
duplicate_of: null
---
The expected page count was set to 21 before the final standalone-claim links and V4/C5 assurance paragraph landed. Two independent renders of the exact current PR #148 head on the same host produce 22 pages. Confirm the content delta rather than attributing it to PR #149, update the reviewed count and its regression expectations, rebuild, visually inspect all pages, and record the new measured artifact in PR #148.
