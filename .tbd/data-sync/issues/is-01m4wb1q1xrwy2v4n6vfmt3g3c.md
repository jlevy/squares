---
type: is
id: is-01m4wb1q1xrwy2v4n6vfmt3g3c
title: "PR592 C2: exclude sampled evidence from every rung derivation path"
kind: bug
status: open
priority: 1
version: 1
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wajcx0q76t3ppdzfbjxq4d
created_at: 2026-10-14T04:34:37.244Z
updated_at: 2026-10-14T04:34:37.244Z
---
Published correctness C2: older samples and numerical, proof, and external-review branches can raise V/C rungs. Backfill coverage, filter samples before every rung-bearing branch, and ratchet legacy omissions.
