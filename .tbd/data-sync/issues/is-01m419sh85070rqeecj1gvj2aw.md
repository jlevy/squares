---
type: is
id: is-01m419sh85070rqeecj1gvj2aw
title: "CI: test_overview's site-render fixture cost lands in a test call on some runs and trips the 12 s backstop"
kind: bug
status: open
priority: 2
version: 2
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels:
  - ci
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-03T16:33:10.917Z
updated_at: 2026-10-07T06:23:10.673Z
---
On f4642c051 and 155abe8a2, suite-a failed the per-test backstop: test_overview.py::test_every_link_to_a_result_goes_to_its_row at 21.5 s and 21.2 s of CALL wall. In the green 056de341f run the same ~21.9 s was booked as SETUP (the module-scoped rendered fixture renders every site page, about 22 s). The junit totals are equal, so the work is the same and only the phase changes. The validator enforces call time only. It does not reproduce locally in either order (setup 13-20 s, call 0.03 s). It went away on 53fe57147 after the shard record was rebuilt (4aeab380d), which moved files between shards, so the cause is unexplained and may recur. Evidence: CI command logs in the run artifacts (validation-timings-suite-a-1). A lasting fix should make the render's phase deterministic, or make the cases page render cheaper (30 of 48 s in the profile is kpress Markdown parsing of the 9 MB cases page).
