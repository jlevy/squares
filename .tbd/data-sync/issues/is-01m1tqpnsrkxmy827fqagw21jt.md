---
type: is
id: is-01m1tqpnsrkxmy827fqagw21jt
title: "B3: the two standard-library verifiers accept different inputs"
kind: bug
status: in_progress
priority: 2
version: 2
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:12.663Z
updated_at: 2026-09-06T06:50:20.877Z
---
verify_claim.py merges the weights of atoms at a repeated site and never checks an atom lies in [0, L]^2; minimal_verify.py and thirdparty/verify.py refuse both. Add the duplicate-site and containment checks to verify_claim.py as preconditions, refused by name before any condition (or, if merging is kept, say so in the claim document; prefer the checks so the three verifiers agree on a well-formed certificate). Tests for both refusals. Regenerate.
