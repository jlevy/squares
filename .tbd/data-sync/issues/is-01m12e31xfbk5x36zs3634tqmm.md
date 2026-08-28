---
type: is
id: is-01m12e31xfbk5x36zs3634tqmm
title: Enforce one live bounded commitment per bead
kind: bug
status: closed
priority: 2
version: 2
labels:
  - packing
dependencies: []
parent_id: is-01m127tej32njy532m2q642418
created_at: 2026-08-27T20:20:26.158Z
updated_at: 2026-08-28T01:36:56.103Z
closed_at: 2026-08-28T01:36:56.102Z
close_reason: "Invariant added: at most one READY commitment per bead. Refined from at-most-one-live during scoping, because at-most-one-live would flag think-sfzh's BC-018/BC-021 legitimate blocked dependency chain. Resolved the one violation (think-kdil backed BC-028 and BC-038, both ready; BC-028 stopped as superseded). Verified to fire and pinned by a negative control."
resolution: null
duplicate_of: null
---
A bead may back several bounded commitments, which is the intended way to carry a lane across agendas: think-1s0h backs BC-010 (agenda-001), BC-029 (agenda-003) and BC-037 (agenda-004). Many COMPLETE commitments per bead is the useful part, a record of successive bounded attempts.

Several LIVE ones is ambiguity, and it is producing contradictory state today:

  think-1s0h  bead in_progress  BC-010 ready, BC-029 blocked, BC-037 blocked
  think-kdil  bead open         BC-028 ready, BC-038 blocked
  think-sfzh  bead —            BC-018 blocked, BC-021 blocked

Ask whether think-1s0h can be worked and four sources give different answers. Bead status and commitment state are also separate vocabularies (open/in_progress/closed versus ready/blocked/complete/tentative/stopped) with nothing reconciling them.

Fix: add an invariant to packing-ledger check that at most one non-terminal commitment may reference a given bead. It sits naturally beside the existing dependency check, which already caught a ready commitment depending on an incomplete one.

Three beads violate it today. It would also have rejected BC-037 and BC-038 at the moment they were added in session 029.
