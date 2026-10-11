---
type: is
id: is-01m3rp1yjrw96h7yy6azcahx2w
title: Profile exact sequential geometry cost for T060 nonfield exclusions
kind: task
status: closed
priority: 0
version: 11
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rb05kzxrn6zcj60cs1c91f
child_order_hints:
  - is-01m3s1n0yn7v1x1rqvn3raqhem
  - is-01m3s2enf7qb4c4kv1s4ndv5tp
  - is-01m3s36jew3nmbz2yhdf33yf8w
  - is-01m3s5g5mzpjt0rcz12n5cxy3h
created_at: 2026-09-30T08:14:19.735Z
updated_at: 2026-10-06T08:36:11.084Z
closed_at: 2026-10-06T08:36:11.084Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): Row-cost inventory and profile retained (receipts/nonfield-manifest/row-cost-inventory.json, generic2095-row-profile.json under n11-optimality-2026-09-29) and the indexed cover adopted; T-060 confirmed at S5/V4/C5. Open child think-iks0 moved to think-3i74 before closing
resolution: null
duplicate_of: null
---
Build reusable row-cost inventory and bounded profile from pinned nonfield manifest and accepted generic mask 2095 receipt. Identify exact union cover hotspot and assess safe optimization without changing frozen verifier; report calibrated scenarios and differential acceptance conditions.

## Notes

Measured exact kernel4.6-4.9x rowCPU; full1687 aggregate1.75xCPU. Frozen root continuation now completes891.927s one-worker. Independent worktrees keep generic/capture implementation concurrent with replay. At this checkpoint fullroot/1723 output completion was noticed after coding intervals; require process-status checks at coding milestones and immediate parent result notification to avoid idle downstream dependencies. No mathematical credit from file existence alone; reviewed source/receipt bindings required.
