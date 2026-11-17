---
type: is
id: is-01m5ve2qf4ty6vdvwjqr8s3nnq
title: "test_site_homepage news facets: Page.goto(index.html) hit its 30 s cap at load 27"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-26T06:24:03.555Z
updated_at: 2026-10-26T06:24:03.555Z
---
Observed by w-eng-issues-1026 while running `packing/tests/test_site_homepage.py` five times
under `-n 2` for #550 (PR #827, head `519d879cb`), on a shared four-cpu host.

`test_news_facets_history_bookmarks_and_shared_meters[1280]` and `[390]` failed in two of
the five runs. Both were the first run of each of two concurrent streams, at load 27 with
the edit tier also running. Each failed with
`Page.goto: Timeout 30000ms exceeded` while navigating to `http://homepage.test/index.html`
(`wait_until="load"`), in `shared_chooser_contract` (test_site_homepage.py line 1559, called
at line 1688). The other three runs passed all 32 tests (load 12 to 21). The `atlas_seen`
fixture and its ten tests passed in all five runs.

The page's assets are fulfilled by a Python route handler in the test process, so under
load a full `load` waits on every asset round trip. Not investigated further. What remains:
decide whether the test should wait on the page's own state, as #520, #547 and #550 did,
or whether `load` on a routed page is the right wait. Lengthening the timeout is not the
fix.
