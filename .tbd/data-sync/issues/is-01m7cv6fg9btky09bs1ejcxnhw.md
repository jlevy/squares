---
type: is
id: is-01m7cv6fg9btky09bs1ejcxnhw
title: "Import #977 (s(297) <= 17.739455558289) and #979 (s(332), s(409), beyond the horizon, built from it): Joost de Winter's double-step staircase variant of T-174"
kind: task
status: in_progress
priority: 1
version: 5
delegate: bold-ritchie-l154
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-14T10:56:05.125Z
updated_at: 2026-11-14T14:09:45.062Z
started_at: 2026-11-14T10:56:06.869Z
---

## Notes

2026-11-14 11:06Z bold-ritchie-l154: packets de-winter-s297-upper-bound-2026-11-14 (7b4701f) and de-winter-issue979-2026-11-14 (c70defa) written; custody checks pass. Controls plan stated before any certify or sharp-controls run: scratch l154/notes/controls-plan.md, SHA-256 18ad29d05373dd46ba5415b52e9e6cccfd32e42491e4dbb7d02120dba15e6054, 2026-11-14T11:06:15Z. 297 exact side 17.7394555582889518 (ceiling 16 places), 9.617e-4 below T-174; 332 and 409 exactly S297 + 1 and S297 + 3.
2026-11-14 13:37Z bold-ritchie-l154: replay on both routes (9 jobs) and 33 sharp controls as stated; T-174 margin 0; own 1.824e-59; identity 55 beyond a tenth. Registered T-299 (V3/C3, S3) and rows at 332 and 409 (verified). Merged L153 review (f78457039) and mapped it (V-de-winter-977-979-review-check, two review evidence entries); no disagreement. Adopted T-299 at 297 in the pass of 14 November; grid-slack 0.5-degree view drawn; Evan Daniel's KKT solve 1.824e-59 below the side, view held at row 4 (RV-3). Draft PR jlevy/squares#980 at b506ef72e (labels S3, intake); records 55/55, edit 71/71. Owed after merge: replies on #977 and #979 with the review's six questions. blocked_on: jlevy/squares#980
2026-11-14 14:12Z bold-ritchie-l154: first hosted run on b506ef72e failed on a stale composite-figure.json (sweeps atlas sample, shard C test_rigidity_status); fixed in 501a06235, re-pinned f955dcee8; hosted CI green on f955dcee8 (Packing validation 43601883906, Certificate page 43601883950, mergeability 43601878134); PR mergeable, clean, draft. Handed back to the coordinator. blocked_on: jlevy/squares#980
