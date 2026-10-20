---
type: is
id: is-01m53h0rqh401n0wc2kyky8m5b
title: Standing logic reads a reported print as exact, so an entry held below its review reads 'superseded' by nothing
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m50j15k23rw2vdmvyvs07rqt
created_at: 2026-10-16T23:33:38.673Z
updated_at: 2026-10-16T23:33:38.673Z
---
Found during #622's intake (lane N, 58de4dedc; #661 reviews A2 and B). render_recent_results.py:296-302 reads a bound with no exact form as exactly its printed value, and check_standing.improvements compares an unreplayed (C0) entry with the reported lane only. At n=29 the Kingbird print 5.93383346267692 (a truncation; T-009's 1e-44 Krawczyk box contains S) therefore reads as exact and below T-195, so holding T-195 at C0 before its review makes it derive 'superseded' with no superseding result. Fix: treat a print without an exact form as an interval (the print within one unit of its last place) in standing and status, so an undecided order stays undecided, and allow the T-193-style hold before a review exit. Related: think-6gti (sigma at 29).
