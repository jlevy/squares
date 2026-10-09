---
type: is
id: is-01m4fhtg9da0y5514xbzg58cr6
title: "Resolve Couzo raw-byte retention conflict between #460 and the known-best-packings policy"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T05:22:53.357Z
updated_at: 2026-10-09T05:30:32.181Z
started_at: 2026-10-09T05:30:32.181Z
---
#460 retains raw Couzo certificate and decimal-pose bytes (source/*.gz, facts .xz) on a factual-data rationale; known-best-packings/README.md says Couzo packets retain no upstream byte; #466 and #469 are derived-only. Owner decision needed before merging the stack.

## Notes

Owner decision 2026-10-09 (in session): keep #460's retained factual Couzo certificate/decimal-pose files and amend the known-best-packings policy to permit retaining factual numeric data from unlicensed sources while prose stays hash-pinned. #466/#469 remain derived-only (permitted, not required).
