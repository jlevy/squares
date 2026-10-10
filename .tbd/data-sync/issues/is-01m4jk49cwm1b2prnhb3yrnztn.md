---
type: is
id: is-01m4jk49cwm1b2prnhb3yrnztn
title: "Import Guzhou0806: s(40) > 335427/50000 from wand125's rect_n40_L67 density with a clipped-corner estimate (#485)"
kind: task
status: in_progress
priority: 1
version: 2
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T09:43:25.852Z
updated_at: 2026-10-10T09:49:28.113Z
started_at: 2026-10-10T09:49:28.112Z
---
Issue https://github.com/jlevy/squares/issues/485 (opened 2026-10-10). Claim: s(40) > 335427/50000 = 6.70854, unrestricted rotations, above the case's reported and verified 67/10 from wand125's rect_n40_L67 (#281). Also a weaker full-core bound s(40) > 67000 sqrt(6400006889)/798988091 > 6.70848908. Source Guzhou0806/n40-square-packing at e5abeb4d078a5c5b35df6204dd9b93378e5a7880, release n40-670854-20261010, n40-670854.zip SHA-256 dbefee8658dc8f7d2e4a6ed21b0c3cd29f36ae393405a218f6bbfdce54465bc5. Rust nodal verifier, 401 directions, 32,970,910 nodes; wand125 commented a review on 2026-10-10 reporting a clean replay. Stages 1-3 on this pass; mathematical review of the clipped-corner estimate and strictness argument by Fable at max.
