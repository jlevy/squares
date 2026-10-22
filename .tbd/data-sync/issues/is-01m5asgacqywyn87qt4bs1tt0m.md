---
type: is
id: is-01m5asgacqywyn87qt4bs1tt0m
title: "Results page size and timing: 1,749 bytes remaining at 228 results"
kind: task
status: open
priority: 2
version: 4
delegate: profiles-pr-coordinator
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-19T19:16:37.910Z
updated_at: 2026-10-22T09:05:37.172Z
started_at: 2026-10-22T09:05:15.934Z
---
Measured on claude/integrate-514 (bf1beaab1, PR #514 + main f3d5da7b): results.html is 1,203,626 bytes at 217 results against the 1,250,000 ceiling in devtools/site_urls.py; at the p90 row cost (4,607 + 291 B) the room is about 8 results, so RESULTS_ROOM_THROUGH was set to 225. Registering #675/#678's upper bounds (up to ~85+79 rows) or several intakes will exceed it. Options: paginate/lazy-render the results table, compress row markup, or re-measure the page-load budgets at a larger size and re-select the ceiling under OR-17. Test name and spec still say 'through 200'.

## Notes

2026-10-20 (PR #514 review D): with #514's sections, results.html is 1,203,554 B at 217 results (main 1,157,668); headroom 46,446 B ~9 results at p90 row 4,603+291 B. Ceiling 1,250,000 kept (owner default). Its CLS/LCP timing was measured on the table-only 1,141,207 B page; no timing with sections. Second limit: overview sections 37,858 of ROLLUP_BYTES 48,000 (79%); ~32 more arrivals in one window fail test_the_overview_stays_brief. Test name/spec fixed in 1881cfff9. #675/#678 registration exceeds both; do this before registering them.

2026-10-22 PR578 final build at a020a6a11328a28f3f756b7c0a76a13179a76a38: results.html measured 1,248,251 bytes at 228 registered results against the existing 1,250,000-byte cap, leaving only 1,749 bytes. Independent performance review O confirmed the size and passing guard. This is a byte measurement, not renewed browser-latency qualification. Re-measure timing and choose a durable presentation/size solution before further result growth. Prior limits and historical measurements above remain evidence.
