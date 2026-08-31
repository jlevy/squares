---
type: is
id: is-01m0pnjqdee9v5tfkrg0pnpye8
title: "Fold PR #11's glossary into SYNOPSIS Terminology, or decide against it"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
created_at: 2026-08-23T06:40:26.542Z
updated_at: 2026-08-23T06:40:26.542Z
---
PR #11 (claude/glossary-and-reasoning-defect) added a standalone explorations/packing/glossary.md. PR #12 instead put a Terminology section inside SYNOPSIS.md. The PR #11 handoff raised the question of which home is right and left it open.

Current answer, taken in #12: inline in SYNOPSIS.md. The directory's ownership rule says each document owns one thing, the synopsis already owns "what this project knows", and a separate glossary is a second document that can drift from it -- the exact failure D-010, D-017, D-022 and D-028 are all instances of. A term defined next to the result that uses it is also harder to get wrong.

Before closing this, diff the two for anything #11 said that #12 does not:

- #11 separates cell from basin explicitly. ADOPTED in #12 as its own subsection next to T-2, with the exp-002 seed-2 numbers.
- #11 insists "quench" names all three stages. ADOPTED, in the Terminology entry and the T-2 subsection.
- #11 verifies its numbers against the artifact each came from (kink slopes vs exp-006/exp-010, bracketing vs exp-007..009, tilts vs frontier/n-011.md). #12's Terminology does NOT carry a per-number provenance note. Worth deciding whether check_synopsis.py should reconcile the Terminology numbers the way it already reconciles the round table.

Close as "declined, inline is the home" once that last point is settled either way.
