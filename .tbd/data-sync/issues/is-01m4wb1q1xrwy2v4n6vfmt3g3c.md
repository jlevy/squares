---
type: is
id: is-01m4wb1q1xrwy2v4n6vfmt3g3c
title: "PR592 C2: exclude sampled evidence from every rung derivation path"
kind: bug
status: closed
priority: 1
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wajcx0q76t3ppdzfbjxq4d
hold: null
hold_until: null
created_at: 2026-10-14T04:34:37.244Z
updated_at: 2026-10-14T08:44:52.603Z
started_at: 2026-10-14T04:36:48.929Z
closed_at: 2026-10-14T08:44:52.603Z
close_reason: Fixed, independently confirmed in PR592 reviews D/E/F/G, green fast+Pages+full checkpoint38530454327 at final7a184720, and merged as f73e9de13d8ccc40b91d844b164f9c2ad9c032c1. Full mathematical proof replays remain tracked separately; no new verified n17 bound claimed.
resolution: null
duplicate_of: null
---
Published correctness C2: older samples and numerical, proof, and external-review branches can raise V/C rungs. Backfill coverage, filter samples before every rung-bearing branch, and ratchet legacy omissions.
