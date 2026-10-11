---
type: is
id: is-01m41cpfe7rfkas78e4mvx12aa
title: "PR 315: the push gate's failures (results-table widths, release pin)"
kind: task
status: closed
priority: 2
version: 9
labels: []
dependencies: []
parent_id: is-01m41amwkn2j6r6jh6de7as7fb
created_at: 2026-10-03T17:23:56.487Z
updated_at: 2026-10-04T02:55:14.135Z
closed_at: 2026-10-04T02:55:14.135Z
close_reason: null
resolution: null
duplicate_of: null
---
packing-validate --push at 6f6113111: test_site_result_columns (long case list wraps; table scrolls no further than its floors at 1024 and 768) fails, since the status cell's successor list widens the column; test_release pin needs re-pinning after the last data commit.

## Notes

Merged to main in jlevy/squares#315 at 965a02cd5 on 2026-10-04 02:34 UTC; deployed by Pages run 37171500896 (publish, deploy and verify-deployment passed).
