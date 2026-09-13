---
type: is
id: is-01m2bmgw7cc1mqnmeb0h9wk3hk
title: "admit_threshold_atom_orbits: the negative-weight branch is unreachable"
kind: bug
status: in_progress
priority: 3
version: 3
delegate: verifier_review
labels:
  - research-tooling
dependencies: []
parent_id: is-01m2csyyq4nzfqppqj639avs51
created_at: 2026-09-12T20:21:42.251Z
updated_at: 2026-09-13T07:38:31.564Z
---
devtools/admit_threshold_atom_orbits.py checks each family placement for a negative weight and raises 'family placement {index} has negative weight', but Placement.__post_init__ raises 'placement weights must be non-negative' first, inside CeilingCertificate.from_record on the line above. The branch can never run, and the existing test matches the Placement wording rather than the devtool's, which is how it went unnoticed. Dead defensive code that reads as a check is false assurance: a reviewer counting the reader's refusals counts one that does not exist. Found during the session-127 audit of this instrument and deliberately not fixed there, to keep that change to the token-count work. Either delete the branch or give it a reachable case.
