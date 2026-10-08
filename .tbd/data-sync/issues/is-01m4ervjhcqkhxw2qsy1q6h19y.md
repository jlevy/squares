---
type: is
id: is-01m4ervjhcqkhxw2qsy1q6h19y
title: "PR454 D1: distinguish relaxation from restricting separation branches"
kind: task
status: in_progress
priority: 3
version: 2
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@spud10.local
labels:
  - n-17
dependencies: []
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
hold: null
hold_until: null
created_at: 2026-10-08T22:06:34.027Z
updated_at: 2026-10-08T22:09:22.631Z
started_at: 2026-10-08T22:09:22.631Z
---
Astra correctness Low: strategy line140 incorrectly calls dropping disjunctive alternatives a relaxation. Omitting pair-separation constraints relaxes; retaining only some separating-axis branches restricts and cannot prove exclusion of every packing. Use Astra exact replacement; documentation-only; preserve original result/pilotcriteria. Await formalD marker then address on owning454layer and propagate upstack.
