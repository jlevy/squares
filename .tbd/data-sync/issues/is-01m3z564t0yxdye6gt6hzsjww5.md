---
type: is
id: is-01m3z564t0yxdye6gt6hzsjww5
title: "W2: sampled full-recompute audit in release builds, with a fault-injection control (spec 4.2)"
kind: task
status: closed
priority: 2
version: 2
labels:
  - verifiers
dependencies: []
parent_id: is-01m3yrezbcgcr728c37fq49bvf
created_at: 2026-10-02T20:34:12.416Z
updated_at: 2026-10-02T23:07:05.872Z
closed_at: 2026-10-02T23:07:05.872Z
close_reason: Release audit and fault-injection control at the commit after 67d7179fe; exp-014 prices it at 3.4%.
resolution: null
duplicate_of: null
---
The spec's controls include a box-level fault injection that flips one inside classification. sqverify-fast's debug build re-derives every incremental centre bound from the full rectangle list; release builds have no such redundancy. Add a deterministic sampled audit (e.g. every K-th box and every box at depth <= 3 recomputed from the full list, refusing on disagreement), a test hook that flips one classification, and a control showing the audit refuses it; price the audit in the campaign.
