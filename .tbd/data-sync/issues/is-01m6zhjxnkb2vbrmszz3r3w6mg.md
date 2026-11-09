---
type: is
id: is-01m6zhjxnkb2vbrmszz3r3w6mg
title: "Stage 4 blind review of #927-#931 (Özden's five upper bounds)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: bold-ritchie-l64-review
labels:
  - intake
  - review
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-09T06:57:59.474Z
updated_at: 2026-11-09T07:09:44.954Z
started_at: 2026-11-09T06:58:03.800Z
---
Blind stage-4 mathematical review with a clean-room exact checker, frozen findings and SHA-256 before reading the import lane's work; precedent review-2026-11-04-ozden-893-894-299-204.md and review-2026-11-05-evand-914-seven.md.

## Notes

L64 (bold-ritchie-l64-review), stage 4 blind review of #927-#931.

- 07:05Z: read both precedents (11-04 ozden, 11-05 evand-914), issues #927-#931, the
  Witness/v2 schema, epistemics (significance, review records) and result-import stage 4.
  Record on main 19b354a5c: T-256 (232, 307), T-270 (268), T-263 (299), T-272 (303).
- Cloned the five repositories into scratch (one commit each, pins match the issues).
  Same sqcheck.py blob aa4b27ca and LICENSE.md blob 9803370f in all five.
  Not read: sqcheck.py, verifier/README.md, any sqpack witness or verifier code.
- Certificates are Witness/v2 `representation: corners`, rational p/q strings with
  ~10^215 denominators, promoted by this repository's `packing-witness promote
  --strategy robust-rational`. Writing the clean-room checker now.
