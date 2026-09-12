---
type: is
id: is-01m2ad9avdatjwfznq7zwqjget
title: Validate and publish the reconciled PR149 head
kind: task
status: in_progress
priority: 1
version: 7
delegate: root integration lane
labels: []
dependencies: []
parent_id: is-01m26rygs7f0s76v147x0px4cd
child_order_hints:
  - is-01m2ar91msd279bq940mkybctf
created_at: 2026-09-12T08:56:00.620Z
updated_at: 2026-09-12T12:15:01.893Z
---
Run focused unit, lint, type, live-browser geometry, queue-watchdog, exact-head pre-push, hosted CI, and the full research checkpoint on the combined PR149 revision. Push without overwriting concurrent author work, update the PR title and body with exact costs and evidence limits, verify the PR remains stacked on PR148 and mergeable, then close and sync every completed bead.

## Notes

Published exact head 237c4023 as a fast-forward of remote b6a81495 after confirming no concurrent author movement. Focused tests, lint/type, records, Chromium held-font and PDF checks passed; unrestricted pre-push passed 46/74 named steps with 5,057 tests, Ruff over 1,782 files, BasedPyright zero findings, 939.23s wall; required hosted CI is green. The subsequent exact-head full checkpoint ran 7,467.30s and failed only its slow-marker floor because test_a_third_of_the_corpus_certifies_a_weaker_bound_than_it_reports measured 0.97s below the 1s threshold. Child think-5rh4 tracks returning that intact test to the fast lane and then rerunning pre-push, CI, and the full checkpoint. A first new pre-push attempt lacked DYLD_FALLBACK_LIBRARY_PATH and was rejected at Cairo import; the correctly configured retry is running. PR149 remains stacked on PR148; origin/main is still d507f5c7.
