---
type: is
id: is-01m5asgacqywyn87qt4bs1tt0m
title: "Site agent: lighten results.html before it reaches the 2,000,000-byte hard ceiling (1,645,613 bytes at 309 results on 17 November; about 77 rows of room, roughly three weeks)"
kind: task
status: open
priority: 2
version: 9
delegate: profiles-pr-coordinator
labels:
  - site
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-19T19:16:37.910Z
updated_at: 2026-11-20T07:44:56.339Z
started_at: 2026-10-22T09:05:15.934Z
---
Measured on claude/integrate-514 (bf1beaab1, PR #514 + main f3d5da7b): results.html is 1,203,626 bytes at 217 results against the 1,250,000 ceiling in devtools/site_urls.py; at the p90 row cost (4,607 + 291 B) the room is about 8 results, so RESULTS_ROOM_THROUGH was set to 225. Registering #675/#678's upper bounds (up to ~85+79 rows) or several intakes will exceed it. Options: paginate/lazy-render the results table, compress row markup, or re-measure the page-load budgets at a larger size and re-select the ceiling under OR-17. Test name and spec still say 'through 200'.

## Notes

2026-10-20 (PR #514 review D): with #514's sections, results.html is 1,203,554 B at 217 results (main 1,157,668); headroom 46,446 B ~9 results at p90 row 4,603+291 B. Ceiling 1,250,000 kept (owner default). Its CLS/LCP timing was measured on the table-only 1,141,207 B page; no timing with sections. Second limit: overview sections 37,858 of ROLLUP_BYTES 48,000 (79%); ~32 more arrivals in one window fail test_the_overview_stays_brief. Test name/spec fixed in 1881cfff9. #675/#678 registration exceeds both; do this before registering them.

2026-10-22 PR578 final build at a020a6a11328a28f3f756b7c0a76a13179a76a38: results.html measured 1,248,251 bytes at 228 registered results against the existing 1,250,000-byte cap, leaving only 1,749 bytes. Independent performance review O confirmed the size and passing guard. This is a byte measurement, not renewed browser-latency qualification. Re-measure timing and choose a durable presentation/size solution before further result growth. Prior limits and historical measurements above remain evidence.

2026-11-12 (#970, L132): results.html is 1,600,513 source bytes at 297 results (hosted run 43182861315, and locally), past 1,600,000. The ceiling moved to 1,700,000, room through 318 at a P90 row of 4,587. This is the third byte-only raise since the last timing (22 October, 1,324,108 bytes; +21%). At about 25–30 registrations a week the room lasts about a week, and the 2,000,000-byte hard limit (about 87 rows) about three weeks. Timing re-measurement and a durable lightening are owed before the next raise; the hard limit is the owner's.

2026-11-17 coord-intake-1117: OWNER DECIDED (think-k8vt): "Hand both to the site agent (Recommended)": the results-page lightening and the News card layout fix (fold before first paint, reserve the filter bar, batch the reads) are the site agent's work; intake keeps raising results.html's exception in measured 100,000-byte steps up to HARD_HTML_LIMIT.

2026-11-17T22:30Z w4-records-1117r (think-8gvd, applying think-k8vt): handed to the site agent by the owner's decision of 17 November 2026 (think-k8vt, "Hand both to the site agent (Recommended)"). The results.html lightening is the site agent's work; left open for that agent, unclaimed by intake. Intake's part stays as before: where an intake change pushes results.html past its exception, it raises the exception in measured 100,000-byte steps up to HARD_HTML_LIMIT, per the 5 and 12 November precedent, and says so here.

2026-11-20T07:50Z c5-fixes (PR #1035, think-a88h): #1035 registers no result, but its credit lines (T-057's sources carried down the 211 chain) add 3,441 bytes to the 327-result page: 1,716,490 source bytes against main 7b6bc29e8's 1,713,049. At a P90 row of 4,512 bytes the room through 346 projected to 1,802,218, past the 1,800,000 exception (hosted run 44271657178, suite-b). Per think-k8vt, results.html's exception moves one 100,000-byte step to 1,900,000 (devtools/site_urls.py, PAGE_CEILINGS in tests/test_overview.py, docs/project/site-urls.md): 183,510 bytes left, 40 rows at 4,512 with 3,030 to spare, RESULTS_ROOM_THROUGH 346 -> 367, enough for the imports of the next days (about 7 results in flight on 20 Nov). Timing not re-measured. After this step HARD_HTML_LIMIT (2,000,000) is one more step, about 62 rows from the current page, so the lightening here is now due within roughly two weeks of registrations.
