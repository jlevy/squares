---
type: is
id: is-01m4er1s8rgjp1kb0bvf7stpb5
title: "PR461 D1: correct held-input recheck timing in exp316 metadata"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels:
  - n-17
dependencies: []
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
created_at: 2026-10-08T21:52:28.951Z
updated_at: 2026-10-08T21:52:28.951Z
---
Correctness review D Low: checked_by line57 overstates timing. Witness/transitive accepted inputs are checked after proof inside endpoint_packet; descriptor and construction packet are additionally checked after provenance. Factual metadata correction only, preserve primary criteria, manifests, receipts, source identity and mathematical outcome. Review https://github.com/jlevy/squares/pull/461#pullrequestreview-5463237872.
