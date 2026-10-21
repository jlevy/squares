---
type: is
id: is-01m5g2wfw0xf50d000t9mn6wbv
title: Compare closing credits and rollup identities semantically after HTML compaction
kind: bug
status: closed
priority: 1
version: 5
delegate: profiles_data_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T20:36:46.063Z
updated_at: 2026-10-21T21:26:03.313Z
started_at: 2026-10-21T20:36:52.170Z
closed_at: 2026-10-21T21:26:03.311Z
close_reason: Bounded fixes integrated; final-head Pages and Packing Validate pass, suites B/C pass and suite A assertions pass. Separate project-tally CALL runtime regression remains tracked by think-rolz.
resolution: null
duplicate_of: null
---
Hosted CI retains correct footer and Couzo/Fitzharding profile links but quote-sensitive assertions reject unquoted href attributes after compaction. Own only the closing-credit assertion section in packing/tests/test_overview.py and quote-sensitive finder-credit assertions in packing/tests/test_results_rollup.py. Compare parsed HTML while preserving exact text, link targets, native-navigation attributes, order and multiplicity. Verify the three hosted failures and meaningful mutation checks; run focused lint and type checks. Renderer/CLS changes belong to the frontend worker; no commit by this worker.

## Notes

Implementation frozen for coordinator integration. Changed only the closing-credit assertion section of packing/tests/test_overview.py and quotation-sensitive credit/headline assertions in packing/tests/test_results_rollup.py. HTMLParser event comparisons retain exact decoded text, destinations, attributes, element order and multiplicity while accepting quoted or unquoted attributes. Top-level and nested footer checks preserve one full footer and exactly three closing-credit lines. Mutation controls reject changed names, URLs, duplicated or reordered people and new-tab profile navigation.

Validation: uv run --frozen --all-extras --group dev pytest -q tests/test_results_rollup.py plus the results.html and profiles/evan-daniel.html closing-credit cases and the unquoted-footer regression: 30 passed in 45.61 seconds. This includes both hosted suite C finder failures and the suite A results.html footer failure. The first focused run exposed the same quotation-only mismatch in a linked headline, which is now covered by the final full-module pass. Ruff check and format check pass for both files; git diff --check passes. Focused BasedPyright with the external Python 3.14 interpreter and two threads reports 0 errors, 0 warnings, 0 notes. No renderer changes, staging, commit or push by this worker. Frontend title/CLS changes in other sections of test_overview.py were preserved. Hosted CI confirmation remains with the coordinator.

Coordinator-authorized closure receipt at exact head e162a870a899a61cc77cd47fa2f56c0ff388c8ea: Pages succeeded; Packing Validate succeeded; behavioral suites B and C passed. Suite A completed all 4,364 assertion tests successfully, then its unchanged CALL wall guard identified a separate project-tally performance issue, tracked in think-rolz. The bounded semantic-HTML comparison and T-196 adoption integration acceptance is met; the overall PR tracker and unrelated historical/coverage followups remain open. Hosted run: https://github.com/jlevy/squares/actions/runs/39676438793. This closure records the coordinator's final-head CI receipt; it does not claim the separate runtime guard is resolved in hosted CI.
