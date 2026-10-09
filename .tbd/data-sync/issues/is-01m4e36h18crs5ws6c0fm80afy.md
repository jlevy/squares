---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 26
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
child_order_hints:
  - is-01m4fgak1gswjj6et81wfndgrm
  - is-01m4fgam2ghc99ka4m1nbjwt4c
  - is-01m4fgamsz4gh4nf00hbmt339k
  - is-01m4fqjt02p8hxaxbgq056z2mq
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-09T07:03:32.609Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Current reviewed branch head is 9c64e0b614970cff9634f1814829867b4acd4fc1, with data/layout 87b546, export source/pin d832ce8 and unchanged asset blobs 002a8911. Actual PDF QA and integrated preview passed; final PDF selected in Finder. Both JavaScript guards and mandatory pan/frame checks pass after the named probe import. All 64 full prechecks passed. The normal suite then ended without a final receipt; worker progress records one stale centered-control CSS test assertion. A subsequent run was intentionally stopped so the web subagent can fix that test against the requested left alignment, preserving all other checks. The unexplained termination is not attributed to a timeout or OOM. Full recorded rerun, hosted checkpoint, formal reviews, and PR publication remain pending. All work stays under the open epic; no GitHub merge is authorized.
