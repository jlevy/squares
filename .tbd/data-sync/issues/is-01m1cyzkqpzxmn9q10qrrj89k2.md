---
type: is
id: is-01m1cyzkqpzxmn9q10qrrj89k2
title: "Codify the epistemics: epistemics.md, V/C/S/N ladders, T-results register, checker, README orientation"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-08-31T22:28:03.431Z
updated_at: 2026-09-01T01:46:26.511Z
started_at: 2026-08-31T22:58:47.788Z
---
Owner-approved build (2026-08-31, follows the verification review's rubric gaps). W7 pipeline-improvement. Deliverables: (1) epistemics.md at repo root — the single owner of the epistemic vocabulary: V0-V5 verification ladder (claim-in-the-world), C0-C5 confirmation ladder (our end-to-end establishment) with machine-checkable promotion checklists per rung, S1-S5 anchored significance (declared, dated, never gating), novelty adopted from the existing enum; granularity min-rule for compound claims; bridging table from the evidence atoms (assurance/method/origin/performed_by/relationship_to_generator/external_review/replay_status); permanent resolutions of the four review rubric gaps. (2) packing/frontier/results.yaml — T-NNN results register with schema, initial ~9 records. (3) devtools checker deriving V/C from cited evidence atoms and failing on disagreement with declared rungs; negative control in controls.yaml; tests. (4) Generated frontier/RESULTS.md sorted by significance then confirmation. (5) conventions.md section 4 shrunk to field formats with semantics pointer; identity table T-NNN row pointed at the register. (6) README orientation section: whether this is only a survey or carries novel results, and which ones at which levels, pointing at RESULTS.md and epistemics.md; SYNOPSIS represents the same accurately. New PR from the restarted branch.

## Notes

Final review 2026-08-31: README is now the detailed reader front door (survey, results, inventory, terminology and ids, linked toolchain/technical stack, reports, autonomous research layers, conventions, layout) while definitive contracts remain in their owning documents. epistemics.md is a concise present-state V/C/S/N contract. Results validation now reaches C5, checks exact V/C predicates and repository-file boundaries, refuses hidden stronger evidence and reversed scopes, runs for open-ended dependencies, and has worker-snapshot coverage. The review also reconciled the synopsis/document map, current n=29 status, conventions, T-007 scope, generated views, CI uv pin, and D-411 through D-417. Pre-push passed with 1100 tests; the full gate passed every surface except sub-floor n=5 float equality, which D-417 fixes and whose formerly failing step plus regression now pass. PR #67 remains open; keep this bead in progress until merge.
