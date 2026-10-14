---
type: is
id: is-01m4w46xw173rgshbzzkr2zzhy
title: "PR #592 A5: the new tests pin register contents and duplicate the enum test"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: addresser-592-review-a
labels: []
dependencies: []
parent_id: is-01m4w0w8x81jgrxwd2dshv8f0v
hold: null
hold_until: null
created_at: 2026-10-14T02:35:08.033Z
updated_at: 2026-10-14T02:35:14.157Z
started_at: 2026-10-14T02:35:14.157Z
---
Low. tests/test_results_register.py:1059-1093; tests/test_site_result_filters.py:306. Fix: membership assertions; drop the duplicate enum assertion and _find_kind_enum; keep ordering. Review A (senior, round 1, head 7a1aadceb), PR #592: https://github.com/jlevy/squares/pull/592#issuecomment-6159185393
