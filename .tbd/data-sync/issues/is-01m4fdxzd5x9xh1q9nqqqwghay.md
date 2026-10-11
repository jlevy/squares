---
type: is
id: is-01m4fdxzd5x9xh1q9nqqqwghay
title: "Qualify #466 integrity baseline sites and records-tier wall"
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T04:14:52.836Z
updated_at: 2026-10-09T04:44:43.745Z
started_at: 2026-10-09T04:20:35.289Z
closed_at: 2026-10-09T04:44:43.744Z
close_reason: Integrity baseline admitted via allowlist with trust-boundary justification (a111b1264); records wall overrun shown environmental by same-host A/B; hosted Packing green
resolution: null
duplicate_of: null
---
#466 validate/suite C refuse four new source-custody comparison sites (Couzo checker lines 224,226,287,552) missing from the integrity baseline; records tier 456s > 300s. Resolve through the maintained baseline workflow with real trust-boundary justification; do not suppress tests or relax limits.

## Notes

Fixed a111b1264 on #466: couzo_extended_reports.py admitted to integrity-ceremony.yaml allowlist as kind download (sites 224/226 pinned upstream commit/tree, 287 unretained source blob bytes vs pinned blob id, 552 rebuilt TXT vs pinned blob id); docstring names the boundary; no baseline raised, no control removed. Records-tier: hosted CI never runs --records; its 49 steps run inside --checks (150s) and full (3600s). Same-host A/B --records jobs2 inner1: #463 814491bd3 56.76s vs #466 a111b1264 56.29s, both 49 PASS; 456s was host load. Hosted Packing 37883997391 on a111b1264 SUCCESS all jobs (merge ref included #463 T-129 fix). Follow-up: records tier never clocked at its reference shape (jobs2/inner1/cpus2), so its drift rule is unarmed.
