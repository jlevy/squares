---
type: is
id: is-01m68g3hqcfvxxbpxaxmxpemac
title: "CI: frontend worker gw1 crashed in test_site_case_records.py, 757 s against 105 s (run 41175767887, #850 review A3)"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-10-31T08:09:35.212Z
updated_at: 2026-10-31T08:09:35.212Z
---
Review A3 of #850 (31 October 2026): in Packing validation run 41175767887 (PR #850 at 40df512a1), the frontend job's step "site table layout in Chromium" ran 756.77 s against a recorded 104.74 s (7.23x; the tier's ceiling is 165 s) and failed because pytest-xdist worker gw1 crashed while running tests/test_site_case_records.py::test_a_frontier_row_opens_its_record_and_steps_to_the_next. Every other job of the run passed, and the next runs of the same tree (41178188203 at fea8351b2, 41180240126 at e4cac5eb1) passed. The branch changed no frontend or site code (packets, evidence and coverage records only), so it reads as host load or a browser crash, not a code fault; the empty commit 8f8eabb5b was pushed to re-run CI because the re-run API was not open to that session.

A sevenfold overrun on a pull-request tier is what OR-17's wall ceiling exists to catch. To do: read run 41175767887's frontend artifact (validation-timings-frontend-1, artifact 13033306637) for the crashed worker's last output and the step's timings; decide whether the test or its browser start needs a guard (a per-test timeout, a crash-retry, or a quarantine), or record it as runner variance under think-ht59 with the measurement.
