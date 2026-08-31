---
type: is
id: is-01m1cyzkqpzxmn9q10qrrj89k2
title: "Codify the epistemics: epistemics.md, V/C/S/N ladders, T-results register, checker, README orientation"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-08-31T22:28:03.431Z
updated_at: 2026-08-31T22:58:47.789Z
started_at: 2026-08-31T22:58:47.788Z
---
Owner-approved build (2026-08-31, follows the verification review's rubric gaps). W7 pipeline-improvement. Deliverables: (1) epistemics.md at repo root — the single owner of the epistemic vocabulary: V0-V5 verification ladder (claim-in-the-world), C0-C5 confirmation ladder (our end-to-end establishment) with machine-checkable promotion checklists per rung, S1-S5 anchored significance (declared, dated, never gating), novelty adopted from the existing enum; granularity min-rule for compound claims; bridging table from the evidence atoms (assurance/method/origin/performed_by/relationship_to_generator/external_review/replay_status); permanent resolutions of the four review rubric gaps. (2) packing/frontier/results.yaml — T-NNN results register with schema, initial ~9 records. (3) devtools checker deriving V/C from cited evidence atoms and failing on disagreement with declared rungs; negative control in controls.yaml; tests. (4) Generated frontier/RESULTS.md sorted by significance then confirmation. (5) conventions.md section 4 shrunk to field formats with semantics pointer; identity table T-NNN row pointed at the register. (6) README orientation section: whether this is only a survey or carries novel results, and which ones at which levels, pointing at RESULTS.md and epistemics.md; SYNOPSIS represents the same accurately. New PR from the restarted branch.

## Notes

Delivered by session-061 (BC-107): epistemics.md; results.yaml T-001..T-013 with ResultsRegister/v1 schema; devtools/check_results.py deriving V/C from cited atoms in the records tier (inflation and unexplained understatement both refused; C3+ requires named adversarial controls); firing negative control; 5 pytest cases; generated frontier/RESULTS.md; conventions.md section-4 pointer + T-NNN identity row; README orientation split (first-established-here vs audited-from-the-literature by T-id); SYNOPSIS deferral + night handoff; document map entries; softschema 0.6.2->0.8.0. Deferred rather than force-fitted: (a) Trump local-isolation (E-n011-trump-local-rigidity) derives C3 but has no adversarial control test to name — build a mutation control for cases/trump11 tangent-cone enumeration, then register; (b) E-translation-escape-not-rigid is a numerically-checked survey observation across 89 cases with no single claim shape — owner decides whether it enters the register. PR open for the owner's whole-PR review; bead closes at merge.
