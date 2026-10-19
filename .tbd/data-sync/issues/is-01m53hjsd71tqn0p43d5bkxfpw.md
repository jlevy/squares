---
type: is
id: is-01m53hjsd71tqn0p43d5bkxfpw
title: "Standing and supersession read a reported print with no exact form as exact (T-195 hold, #661 A2)"
kind: bug
status: in_progress
priority: 3
version: 3
delegate: user-eb-intake-622
labels: []
dependencies: []
parent_id: is-01m50j15k23rw2vdmvyvs07rqt
hold: null
hold_until: null
created_at: 2026-10-16T23:43:29.191Z
updated_at: 2026-10-17T01:07:13.593Z
started_at: 2026-10-16T23:43:38.879Z
---
Found by review A (A2) and review B of jlevy/squares#661 (T-195, PR #622's N29 certificate), 16 October 2026.

`devtools.render_recent_results.span` (packing/devtools/render_recent_results.py:296-302) spans a case bound that has no `exact_form` as its print, a single exact number. `check_standing.improvements` reads an unreplayed entry against the reported lane only. So at n = 29 the Kingbird catalogue print 5.93383346267692 is read as an exact side below T-195's certificate side. T-195 held at V0/C0 then derives `superseded` with no superseding result. tests/test_result_status.py refuses that, and the result page would print it.

That contradicts epistemics.md:370-372: a bound is superseded only where its cases hold a bound at least as good. The per-count ledger (devtools.intake_ledger) reads the same print as a span within one unit of its last place and rules the comparison undecided.

The hold was tried at f6929451a and reverted at 58de4dedc on #661's branch. That is why T-195 could not be held at its reported rungs before its stage 4 exit, as T-193 was (PR #651, review A2).

Fix: read a print with no exact form as the span its rounding allows (as intake_ledger.printed_side does) in standing and supersession, so that an entry held at C0 against a catalogue print reads pending (undecided), not superseded. Add a test with T-195's shape: a reported lane holding a print within one unit of an unreplayed entry's side.

Done when the next unreplayed entry against a catalogue print can be held at V0/C0 without a false `superseded`.

## Notes

2026-10-17 user-eb-intake-622: the same print-read-as-exact flaw was in devtools/check_source_coverage.py (a selected override had to be strictly below the Kingbird print). Fixed for #661, on the coordinator's direction: a print orders an override only beyond one unit of its last place (_not_above_print), the reading the n = 29 ledger uses, with tests below, inside and beyond the unit (tests/test_source_coverage.py). Prepared as local commit 8f990ae3f on prep-661-after-660; it lands on #661 in its post-#660 pass. The standing logic (render_recent_results.span / check_standing reading a print with no exact form as exact) stays open here; think-nhsd is the same flaw.
