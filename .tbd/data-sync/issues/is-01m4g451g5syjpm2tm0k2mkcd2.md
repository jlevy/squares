---
type: is
id: is-01m4g451g5syjpm2tm0k2mkcd2
title: "OR-18: move the n17 stack's ~314 MB retained certificate/replay JSON out of Git"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels:
  - n-17
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-09T10:43:13.029Z
updated_at: 2026-10-09T10:43:13.029Z
---
Stack 455 (#404) landed 21 retained JSON results >5,000 lines totalling ~314 MB (exp-260/289/291/292/293/296/297/300/301/302/305 certificate/replay pairs; exp-291/292 ~34.7 MB each). Tracked tree grew 1,029.5 MB (main 3213d651b) -> 1,364.5 MB (bead35d93). OR-18 says keep bulk data out of Git; the repo has hosted-data manifests (packing/hosted/*.yaml) and #435 moved PDFs to hosted storage. Owner decision needed: host these with manifests + reproducible acquisition (history still carries the blobs unless rewritten), or record why they must stay. Related: X-051 custody findings (200 objects 2.14 GB unhosted), open #406 (refuse added bulk blobs).
