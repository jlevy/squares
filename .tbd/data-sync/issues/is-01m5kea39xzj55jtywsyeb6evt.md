---
type: is
id: is-01m5kea39xzj55jtywsyeb6evt
title: "check_published_site still expects the pre-#737 markup: verify-deployment red on main since 31584003e (atlas index rows, Papers nav entry)"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: c-lane-verifier-737
labels:
  - site
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-23T03:54:09.597Z
updated_at: 2026-10-23T03:55:10.018Z
started_at: 2026-10-23T03:55:10.018Z
---
Main's Certificate page run 39896243132 on 31584003e (#737, site navigation) deployed, but verify-deployment failed: 'atlas.html indexes 0 registered case records in order' and 'Papers is not the bar's current entry' on the four paper pages. The live site is fine: atlas.html links all 324 cases/N.html, and paper pages carry #737's nav (<a data-page="papers" href="../papers.html" aria-current="true">) plus breadcrumbs. check_published_site.py still matches CASE_INDEX_LINK = <tr id="n-(\d+)" ... data-case-href=... and PAPERS_CURRENT = <a data-page="explanations" aria-current="page" href="../papers.html">. Update both to #737's markup, preferably derived from site_navigation.py / the atlas renderer rather than hard-coded, with tests against rendered pages so the next nav change cannot silently break verification.
