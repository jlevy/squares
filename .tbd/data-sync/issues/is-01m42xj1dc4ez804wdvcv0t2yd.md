---
type: is
id: is-01m42xj1dc4ez804wdvcv0t2yd
title: "Site: synopsis and frontier main-thread long tasks"
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m42xfwp06kzm2b390dx1cw17
created_at: 2026-10-04T07:37:51.276Z
updated_at: 2026-10-04T08:27:09.877Z
---
Local cold load, no throttling (2026-10-04, measure_site_pages load): synopsis.html blocks the main thread ~1.09 s, frontier.html ~0.64 s, all-results ~0.26 s. Profile and cut; separate from the asset work.

## Notes

2026-10-04: preview_site.screenshots at 390 px leaves 186-196 math spans on synopsis.html untypeset in this sandbox, on main (site-base) and on the shared-assets branch alike; likely the same main-thread cost. Not a regression of think-31yw.
