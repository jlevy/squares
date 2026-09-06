---
type: is
id: is-01m1ttyjn42mfcq1rtc9phc76h
title: "PR 94: live-site checker rejects the new build-commit edition stamp"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-09-06T07:46:57.315Z
updated_at: 2026-09-06T08:05:14.839Z
closed_at: 2026-09-06T08:05:14.839Z
close_reason: Fixed in PR 94 commit 9c82dc2a. All required CI checks passed in run 34020582886; page build passed in 34020582877. Focused regression tests, final 31-step records gate, both revised negative controls, and n11/n17 package controls passed.
resolution: null
duplicate_of: null
---
check_published_site.py:125 still searches PUBLICATION_EDITION (pinned 9307172a), while render_explainer.page_edition stamps the build commit. Mocked healthy responses reproduce a false failure. Build the expected stamp from check() commit argument and cover it with a mocked end-to-end check test.
