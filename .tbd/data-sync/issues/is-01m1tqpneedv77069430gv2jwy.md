---
type: is
id: is-01m1tqpneedv77069430gv2jwy
title: "B2: verify_claim.py surfaces its own self-check failure as a traceback, not a verdict"
kind: bug
status: in_progress
priority: 2
version: 2
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:12.301Z
updated_at: 2026-09-06T06:50:20.572Z
---
verify_claim.py least_mass raises AssertionError when the direct sum at the witness disagrees with the swept minimum; main catches only OSError, KeyError, TypeError, ValueError around loading. A verifier bug then prints a traceback with status 1, which a caller reads as a refusal of the certificate. Fix: catch AssertionError around decide, print an internal-error line, exit 2, distinct from both verdicts; document the third status in the claim template's 'How to Check It'. Add a test that forces the path. Regenerate.
