---
type: is
id: is-01m4fhtg9da0y5514xbzg58cr6
title: "Resolve Couzo raw-byte retention conflict between #460 and the known-best-packings policy"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T05:22:53.357Z
updated_at: 2026-10-09T05:43:35.077Z
started_at: 2026-10-09T05:30:32.181Z
---
#460 retains raw Couzo certificate and decimal-pose bytes (source/*.gz, facts .xz) on a factual-data rationale; known-best-packings/README.md says Couzo packets retain no upstream byte; #466 and #469 are derived-only. Owner decision needed before merging the stack.

## Notes

Amended at #442 4c5085de3 (head 49d33c0c2): known-best-packings/README.md new 'Retained Factual Data' section (owner decision 2026-10-09; factual data of packing sources may be retained bound to upstream identities; prose/programs never copied; retention grants no licence; derived-only still allowed); wording aligned in upper_bound_packets.py docstring, resources/README.md:528, Couzo 09-27 and de Winter packet READMEs. No bytes, flags, data or pins changed. Inventory: #442 Ry-Xu, #448 Gupta, #460 Couzo retain factual upstream files; main Couzo/de Winter/SQUISH, #466, #469 derived-only. Follow-ups sent: Ry-Xu sources.json raw_asset_retained rows; #469 packet README wording.
