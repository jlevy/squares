---
type: is
id: is-01m1tqpn2wcz47dqd846yf8e8g
title: "A10: 'the four lines bounding the admissible centers' is not what the verifier adds"
kind: bug
status: in_progress
priority: 2
version: 2
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:11.931Z
updated_at: 2026-09-06T06:50:20.268Z
---
verifiable_claim.md 'Why the Sweep Is Exact' and verify_claim.py's comment block say the arrangement adds the four lines bounding the admissible square; at any direction but 0 those are oblique and the code adds the domain's extreme U and V values (its bounding box) and then clips. The decision is correct either way, but a reader implementing from the prose would build a different arrangement. Fix: '...with the extreme U- and V-coordinates of the admissible square, cut the plane into finitely many open cells. A cell may straddle the admissible square's oblique edge; the clipping test decides exactly which cells meet it.' minimal_verify.py already says it right. Regenerate the claim documents.
