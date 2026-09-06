---
type: is
id: is-01m1v1w5a9nmhrthcpb0ffpan7
title: Reconcile the n=11 Lean formalization spike before continuation release
kind: task
status: open
priority: 0
version: 1
labels:
  - formalization
  - launch-blocker
dependencies: []
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T09:47:58.152Z
updated_at: 2026-09-06T09:47:58.152Z
---
The cold-entry strategy audit found that landed main lacks packing/cases/n11_fractional_certificate/lean-spike/ and retains a pre-discovery Lean note. Audit the unlanded prior branch only as untrusted source material, port the requested formalization assets onto the current continuation branch under coordinator ownership, update every statement to the current T-018/567130649-cell/minimal_verify.py 316-line record, add executable controls where practical, validate, and resolve the omission before releasing active research. Do not merge or cherry-pick an open branch wholesale.
