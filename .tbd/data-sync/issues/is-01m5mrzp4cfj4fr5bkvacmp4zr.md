---
type: is
id: is-01m5mrzp4cfj4fr5bkvacmp4zr
title: "Site URLs: disposition for the nine atlas/regularized SVGs the algebraic adoption removes (70, 102, 123, 153, 207, 258, 259, 295, 302)"
kind: task
status: in_progress
priority: 1
version: 2
delegate: c-fix-756-1023
labels:
  - decision
  - site
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T16:19:57.196Z
updated_at: 2026-10-23T22:18:45.109Z
started_at: 2026-10-23T22:18:45.109Z
---
The adoption of the nine algebraic houses on 23 October 2026 (think-ot5c, branch claude/intake-2026-10-23-algebraic-houses) leaves the regularized layer's index with no view at 70, 102, 123, 153, 207, 258, 259, 295 and 302. The axis tool refuses a number-field witness (`unsupported-scalar-kind`), the lapsed strong views are not kept (the owner's answer to question 13, think-r8cn), and no regularizer yet draws an exact view of a number-field witness (think-mbdw). So `render_overview.support_file_paths` no longer declares `atlas/regularized/n-{70,102,123,153,207,258,259,295,302}.svg`. These nine are live rows in packing/site-urls.yaml, first published 2026-10-07.

`site_urls --check --history-ref origin/main` (the records tier's "published URL registry and historical compatibility" step, and the PR gate) fails with "removed live URL atlas/regularized/n-102.svg: retain a forwarder or a withdrawn tombstone". It stops at the first of the nine.

Each disposition the registry offers touches site infrastructure that belongs to the site lane:
- (a) A `render_overview.MOVED_FILES` copy of `atlas/house/n-NNN.svg` at each old address, with the matching `moved` lines in .github/workflows/pages.yml (publish job) and the fixture in tests/test_pages_workflow.py. The address keeps serving the drawing now drawn. When think-mbdw later draws a view there, the same PR has to drop the entry, or the step's "already published" guard fails.
- (b) `status: withdrawn`, which `validate_registry` admits only for `.html` paths, so `site_urls` needs an asset-file withdrawal: code in site_urls.py.
- (c) Hand-editing the rows to `status: forwarded`. The validator would pass, but nothing serves a forward for an asset and the deployed check fetches no assets, so the registry would claim a redirect that does not happen. Not recommended.

Recommended: (a), or (b) if the site lane prefers a withdrawn asset to a stand-in drawing. The intake lane was scoped away from site code (LANE-RULES "Scope"), so it made none of these changes. Done when the nine addresses have a disposition the registry accepts and the algebraic houses PR's records tier passes.
