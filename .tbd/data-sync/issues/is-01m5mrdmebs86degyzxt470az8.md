---
type: is
id: is-01m5mrdmebs86degyzxt470az8
title: "Case pages: list the other certificates once per page, not in every house section (204's page grows with each adoption; review A7 of #753)"
kind: feature
status: open
priority: 2
version: 1
labels:
  - site
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T16:10:05.643Z
updated_at: 2026-10-23T16:10:05.643Z
---
From review A of #753 (A7, https://github.com/jlevy/squares/pull/753#issuecomment-6369144929). cases/204.html measures 320,783 bytes: 204 holds ten verified certificates and a section for each of the six that have been its house, and each house section lists every other certificate's side as inline math (about 900 bytes each), so each adoption adds a section and a line to every other section. #753 added measured exceptions at 350,000 (packing/tests/test_case_pages.py and packing/devtools/site_urls.py PAGE_BUDGET_EXCEPTIONS), which leave about 29 KB, roughly one more adoption. The fix is a generator/template change (adopt_houses' house sections or the case page renderer), outside the intake lanes' scope rule, so it is the site agent's. The next adoption at 204 should not only raise the ceiling again.
