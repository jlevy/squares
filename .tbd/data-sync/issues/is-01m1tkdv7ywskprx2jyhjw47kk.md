---
type: is
id: is-01m1tkdv7ywskprx2jyhjw47kk
title: "verify_claim.py: decide, not raise, when no B-square fits at a direction (F3)"
kind: bug
status: closed
priority: 2
version: 3
labels:
  - review-gpt6
dependencies: []
parent_id: is-01m1tkdspk8c3n71xsc2e2t4g7
created_at: 2026-09-06T05:35:29.021Z
updated_at: 2026-09-06T06:21:09.267Z
closed_at: 2026-09-06T06:21:09.267Z
close_reason: "Implemented in 41fb401a on claude/pdf-paper-small-fixes (PR #92); reviewed by the coordinator; CI green"
resolution: null
duplicate_of: null
---
Finding 3, confirmed at packing/cases/n11_fractional_certificate/verify_claim.py:149-151 -- least_mass raises ValueError when 2h >= L ('no B-square ... fits ... with room to spare'). Two valid theorem inputs are conflated: 2h > L makes Condition 5 vacuously true at that direction; 2h = L leaves exactly one feasible center whose mass can be checked directly. Reviewer's reproduction: n = 2, L = B = 1/2, net (0, 1/2), one unit-weight atom at (1/4, 1/4) satisfies every hypothesis and the verifier raises. The thirdparty package documents empty and singleton domains, so the two public paths disagree. Fix: either handle both cases or restrict the advertised domain and distinguish 'unsupported input' from 'failed hypothesis' in the output. The verifier is embedded byte-for-byte in both claim documents: regenerate with devtools.render_verifiable_claim and keep tests/test_verify_claim.py green. Also make the sweep explanation in the claim template state the nonempty-interior assumption if it is kept.
