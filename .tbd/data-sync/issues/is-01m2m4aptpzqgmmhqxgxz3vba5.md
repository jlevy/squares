---
type: is
id: is-01m2m4aptpzqgmmhqxgxz3vba5
title: "Address review: PR #175 — the guard, the ratchet and the probe loader"
kind: task
status: in_progress
priority: 1
version: 19
labels: []
dependencies: []
child_order_hints:
  - is-01m2m4b6x0t593cq2zvvwnv09m
  - is-01m2m4b864y4skq152a8dnxev4
  - is-01m2m4b91n3s3cfc5cjh4k8w9b
  - is-01m2m4b9y1e21rkx6bqqpnr9x2
  - is-01m2m4bap0n4e7khbmfb67b61k
  - is-01m2m4bbbrpqrpbs3vbv8pnazc
  - is-01m2m4bbznncaty72xbahjpngs
  - is-01m2m4bcyqx0vgks5nx75q3kfn
  - is-01m2m4jes05shkg78frj7n6v9s
  - is-01m2m4jhkv3mw83marbk3cwzqv
  - is-01m2m4jkpetf189mh8trf866gw
  - is-01m2m4jn8rggcnd09kz4y5qfkx
  - is-01m2m4jq6zqjsb031svc45t74f
  - is-01m2m4jsgp20vf60gqr245265w
  - is-01m2m66z2th383fhep5zh67yfe
  - is-01m2m66zx2kaa04dgecjgzvj8b
created_at: 2026-09-16T03:31:52.789Z
updated_at: 2026-09-16T05:02:58.200Z
---

## Notes

2026-09-16 recovery audit: recovered comprehensive R1-R8 commit 0ab75b7c was a sibling of remote PR head 582d384a; e4d96b6f was correctly one commit on top of 582d384a, not a sibling. Reconciliation head 0dfcd70b now preserves both lineages: 7eb20ffd applies the e4d delta onto 0ab, and merge commit 0dfcd70b records e4d/582 ancestry. Focused evidence is green (109 guard tests, 23 browser-floor contract tests, Ruff, live guard over 912 files / 469 allowlisted sites, and 177 probe declarations). Required pre-push validation is running before the integrated head is pushed and propagated through #178/#179/#181/#180.
