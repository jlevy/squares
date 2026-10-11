---
type: is
id: is-01m1tqpn2wcz47dqd846yf8e8g
title: "A10: 'the four lines bounding the admissible centers' is not what the verifier adds"
kind: bug
status: closed
priority: 2
version: 3
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:11.931Z
updated_at: 2026-10-06T08:24:51.954Z
closed_at: 2026-10-06T08:24:51.954Z
close_reason: "Done: PR 94 (merged 2026-09-06, 3e1fd715d) implements A10. The page now names the extreme U and V coordinates (the bounding box) and the clipping test, matching the code."
resolution: null
duplicate_of: null
---
verifiable_claim.md 'Why the Sweep Is Exact' and verify_claim.py's comment block say the arrangement adds the four lines bounding the admissible square; at any direction but 0 those are oblique and the code adds the domain's extreme U and V values (its bounding box) and then clips. The decision is correct either way, but a reader implementing from the prose would build a different arrangement. Fix: '...with the extreme U- and V-coordinates of the admissible square, cut the plane into finitely many open cells. A cell may straddle the admissible square's oblique edge; the clipping test decides exactly which cells meet it.' minimal_verify.py already says it right. Regenerate the claim documents.
