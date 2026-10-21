---
type: is
id: is-01m5g2wfw0xf50d000t9mn6wbv
title: Compare closing credits and rollup identities semantically after HTML compaction
kind: bug
status: in_progress
priority: 1
version: 3
delegate: profiles_data_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T20:36:46.063Z
updated_at: 2026-10-21T20:43:03.862Z
started_at: 2026-10-21T20:36:52.170Z
---
Hosted CI retains correct footer and Couzo/Fitzharding profile links but quote-sensitive assertions reject unquoted href attributes after compaction. Own only the closing-credit assertion section in packing/tests/test_overview.py and quote-sensitive finder-credit assertions in packing/tests/test_results_rollup.py. Compare parsed HTML while preserving exact text, link targets, native-navigation attributes, order and multiplicity. Verify the three hosted failures and meaningful mutation checks; run focused lint and type checks. Renderer/CLS changes belong to the frontend worker; no commit by this worker.

## Notes

Implementation frozen for coordinator integration. Changed only the closing-credit assertion section of packing/tests/test_overview.py and quotation-sensitive credit/headline assertions in packing/tests/test_results_rollup.py. HTMLParser event comparisons retain exact decoded text, destinations, attributes, element order and multiplicity while accepting quoted or unquoted attributes. Top-level and nested footer checks preserve one full footer and exactly three closing-credit lines. Mutation controls reject changed names, URLs, duplicated or reordered people and new-tab profile navigation.

Validation: uv run --frozen --all-extras --group dev pytest -q tests/test_results_rollup.py plus the results.html and profiles/evan-daniel.html closing-credit cases and the unquoted-footer regression: 30 passed in 45.61 seconds. This includes both hosted suite C finder failures and the suite A results.html footer failure. The first focused run exposed the same quotation-only mismatch in a linked headline, which is now covered by the final full-module pass. Ruff check and format check pass for both files; git diff --check passes. Focused BasedPyright with the external Python 3.14 interpreter and two threads reports 0 errors, 0 warnings, 0 notes. No renderer changes, staging, commit or push by this worker. Frontend title/CLS changes in other sections of test_overview.py were preserved. Hosted CI confirmation remains with the coordinator.
