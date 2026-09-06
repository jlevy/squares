---
type: is
id: is-01m1trx8pzvj8529kjnmtn9rzg
title: "thirdparty/verify.py: refuse duplicate sites and outside atoms like the other two verifiers"
kind: task
status: in_progress
priority: 3
version: 2
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T07:11:17.214Z
updated_at: 2026-09-06T07:49:12.586Z
---
Follow-up to B3 (think-tp23). verify_claim.py now refuses an atom outside [0, L]^2 and two atoms at one site before any condition, as minimal_verify.py does; thirdparty/verify.py still merges duplicate sites (line ~262) and reports containment only as info (line ~722), so the three standard-library verifiers do not yet agree on what a well-formed certificate is. The claim template says minimal_verify.py refuses them too and does not mention the package. Align thirdparty/verify.py, checking that falsify.py's perturbation rows and check.py's control (Massaccesi's n = 17) still pass, and say so in thirdparty/README.md.
