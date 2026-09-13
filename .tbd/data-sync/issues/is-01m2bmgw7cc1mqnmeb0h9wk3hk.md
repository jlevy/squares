---
type: is
id: is-01m2bmgw7cc1mqnmeb0h9wk3hk
title: "admit_threshold_atom_orbits: the negative-weight branch is unreachable"
kind: bug
status: closed
priority: 3
version: 5
delegate: verifier_review
labels:
  - research-tooling
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-12T20:21:42.251Z
updated_at: 2026-09-13T08:19:32.957Z
closed_at: 2026-09-13T08:19:32.956Z
close_reason: "Fixed: the unreachable branch was the per-placement weight check in _family (admit_threshold_atom_orbits.py:96). Placement.__post_init__ (ceiling.py:115) already raises 'placement weights must be non-negative', and CeilingCertificate.from_record builds Placements, so certificate.placements can never carry a negative weight. Verified: from_record refuses first and the admitter's message is 'invalid ceiling family: placement weights must be non-negative' -- which is exactly what the retained test already matched ('non-negative', not the dead branch's 'has negative weight'), so the branch was never the thing under test. Loop removed; the constructor check and the control stay, and the test now documents that the refusal is the constructor's."
resolution: null
duplicate_of: null
---
devtools/admit_threshold_atom_orbits.py checks each family placement for a negative weight and raises 'family placement {index} has negative weight', but Placement.__post_init__ raises 'placement weights must be non-negative' first, inside CeilingCertificate.from_record on the line above. The branch can never run, and the existing test matches the Placement wording rather than the devtool's, which is how it went unnoticed. Dead defensive code that reads as a check is false assurance: a reviewer counting the reader's refusals counts one that does not exist. Found during the session-127 audit of this instrument and deliberately not fixed there, to keep that change to the token-count work. Either delete the branch or give it a reachable case.
