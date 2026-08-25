---
type: is
id: is-01m0wyakt0rfex9sm4dcgvay40
title: Closed round exp-012 was re-adjudicated in place on the tutorial branch
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0wy9s97fwegw5kqrge2p8sy
created_at: 2026-08-25T17:08:44.480Z
updated_at: 2026-08-25T17:49:28.873Z
closed_at: 2026-08-25T17:49:28.873Z
close_reason: Fixed on the PR 33 branch; see review-2026-08-25-tutorial-soundness-iteration-2.md and defects D-320..D-328. Full gate green.
resolution: null
duplicate_of: null
---
The tutorial branch rewrote exp-012's stored verdict (rejected -> unresolved), its titles, and H-024's registered claim/criterion in place, applying the newer assurance vocabulary retroactively to a round that was sound under its preregistered terms. Resolution in the PR 33 merge: restore the registered claim and the preregistered rejected verdict; keep H-042/exp-037 as the serialization-scoped successor (the correct mechanism for the vocabulary shift). Conventions' corrections discipline covers this; the in-place rewrite bypassed it.
