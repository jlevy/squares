---
type: is
id: is-01m1w02sjh48x0b0d16f1yz9ak
title: Recover or recompute the missing BC206 n12 cutting-floor witness
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1vyfpzegaxyp52t4bfx85md
created_at: 2026-09-06T18:35:52.782Z
updated_at: 2026-10-06T08:40:47.540Z
closed_at: 2026-10-06T08:40:47.540Z
close_reason: "Obsolete: D-478 already qualifies the BC206 floor (about 10.85 at side 397/100) as an unreplayed historical report, and nothing on main depends on it. n = 12's verified lower bound is now 7943/2000 = 3.9715 (T-095), above 397/100 by another route, so recovering that witness would settle nothing."
resolution: canceled
duplicate_of: null
---
The retained BC206 log reports a floor around10.845594 at L397/100 but the generating family/state is absent. The log names f-397-100.state.json as a warm start, but no retained family supports replay of the best floor. After D476/D477, qualify it as an unreplayed historical report. Completion requires recovering the exact family/state and replaying it with the repaired verifier, or rerunning the bounded experiment and retaining a reproducible exact witness. Do not promote the rounded log to a certified bracket; no invalidity of the number has been demonstrated.
