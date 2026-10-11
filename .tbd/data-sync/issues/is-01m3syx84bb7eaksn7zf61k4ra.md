---
type: is
id: is-01m3syx84bb7eaksn7zf61k4ra
title: "n = 11 shows as Reported, awaiting replay: rounded reported lower bound compared numerically with the verified one"
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T20:08:17.290Z
updated_at: 2026-09-30T21:56:59.325Z
closed_at: 2026-09-30T21:56:59.324Z
close_reason: "Fixed in febdbe249 on claude/overview-page-impl: Row.shows_reported treats a reported lane carrying the same results, or the same value at printed precision (bounds_agree_at_declared_precision), as not separately reported; regression test test_a_rounded_report_of_the_verified_result_is_not_awaiting_replay fails on the old code. Awaiting-replay block: 49 cases from n = 11 became 48 from n = 18."
resolution: null
duplicate_of: null
---
packing/frontier/n-011.md stores the reported lower bound rounded (3.87708359002281) and the verified one at 32 digits; render_recent_results.Row.shows_reported compares them as numbers, returns True, so README (main, README.md:348) and the site's awaiting-replay disclosure list n = 11 as awaiting a replay that already happened, with a reported value below the verified one. Fix in the display logic (two lanes carrying the same result are one lane, or equality within the reported value's stated precision), with a regression test; do not rewrite the source's reported value.
