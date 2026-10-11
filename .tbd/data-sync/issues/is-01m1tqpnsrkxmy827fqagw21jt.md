---
type: is
id: is-01m1tqpnsrkxmy827fqagw21jt
title: "B3: the two standard-library verifiers accept different inputs"
kind: bug
status: closed
priority: 2
version: 3
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:12.663Z
updated_at: 2026-10-06T08:25:14.034Z
closed_at: 2026-10-06T08:25:14.034Z
close_reason: "Done: PR 94 (merged 2026-09-06, 3e1fd715d) implements B3. All three verifiers refuse duplicate sites and atoms outside the closed container before evaluating."
resolution: null
duplicate_of: null
---
verify_claim.py merges the weights of atoms at a repeated site and never checks an atom lies in [0, L]^2; minimal_verify.py and thirdparty/verify.py refuse both. Add the duplicate-site and containment checks to verify_claim.py as preconditions, refused by name before any condition (or, if merging is kept, say so in the claim document; prefer the checks so the three verifiers agree on a well-formed certificate). Tests for both refusals. Regenerate.
