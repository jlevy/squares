---
type: is
id: is-01m1ttyjn42mfcq1rtc9phc76h
title: "PR 94: live-site checker rejects the new build-commit edition stamp"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-06T07:46:57.315Z
updated_at: 2026-09-06T07:46:57.315Z
---
check_published_site.py:125 still searches PUBLICATION_EDITION (pinned 9307172a), while render_explainer.page_edition stamps the build commit. Mocked healthy responses reproduce a false failure. Build the expected stamp from check() commit argument and cover it with a mocked end-to-end check test.
