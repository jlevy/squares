---
type: is
id: is-01m1v4dbpphp7w9ytdf7v6v7cz
title: Reconcile duplicate BC-220 and BC-221 gate beads
kind: bug
status: closed
priority: 0
version: 3
labels:
  - release-blocker
  - orchestration
dependencies:
  - type: blocks
    target: is-01m1v2yhy02qmka8ez4d2f5bde
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T10:32:18.901Z
updated_at: 2026-09-06T10:43:40.245Z
closed_at: 2026-09-06T10:43:40.244Z
close_reason: Integrated commit 7e5604cb defines think-vniz + think-u7i4 as one T+4 coordinator transaction and think-u8h0 + think-gt06 as one T+8 transaction, each with one immutable decision packet. Live tbd edges show the scientific gates block their continuation wrappers and all downstream lanes pass through the paired transaction.
resolution: null
duplicate_of: null
---
Agenda 024 names BC-220 as think-u7i4 and BC-221 as think-gt06, while the continuation wrappers use think-vniz and think-u8h0; BC-231 and BC-243 depend on the former gate and T+4-to-T+8 wrapper beads depend on the latter. Before release, define each pair as one coordinator gate transaction, add explicit dependency edges or a single authority mapping, and ensure no lane can bypass its scientific gate.
