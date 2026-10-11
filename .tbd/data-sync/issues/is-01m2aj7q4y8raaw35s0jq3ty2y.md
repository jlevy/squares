---
type: is
id: is-01m2aj7q4y8raaw35s0jq3ty2y
title: Document the admitted BC329 runner on the final publication stack
kind: task
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - docs
dependencies:
  - type: blocks
    target: is-01m2axbxf0xz00ezc32q4mesn2
  - type: blocks
    target: is-01m260z2959dmcmn61pn2z7jsk
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
hold: null
hold_until: null
created_at: 2026-09-12T10:22:30.557Z
updated_at: 2026-10-06T08:40:16.470Z
closed_at: 2026-10-06T08:40:16.469Z
close_reason: "Superseded: it waited on an admitted calibration that the owner deferred (think-zwlf) and that is now moot; the landing descriptions (think-gidf, closed) carry the runner's unexecuted status. BC329's prospective endpoint 3.8267215 is below T-033's proved 3.8269975, so the packet could not move any bound even before T-060; its runner and calibration machinery is retained unexecuted on main via PR #156. Its 'paused' hold (the owner's 2026-09-14 BC329/heavy-computation hold, think-zwlf) was cleared to close it: the hold's premise, a small n11 gain, no longer exists."
resolution: canceled
duplicate_of: null
---
After the implementation and calibration are admitted, update the final-stack BC329 preflight and V3 daytime plan without restoring the superseded 'weak lower bound' wording. Replace the instruction to retain through the old decide_threshold_certificate CLI with the fixed runner; document its command, exact exit codes, artifact schema, recovery/readback rules, claim limit, actual route concurrency, clock boundaries, measured allowances, and target-free admission receipt. Keep coverage explicitly unrun until a separately registered scientific target completes. Apply Practical Prose and Flowmark and verify all links and generated records.

## Notes

Final documentation must state explicitly that BC329 is an unconditional eleven-core fixed-B packet using budget M<11. It is distinct from BC330's four-owner/seven-residual conditional idea, which would require a separate physical selection and domain-completeness theorem.

Paused: 2026-09-14 owner hold (think-zwlf): depends on admitted calibration, which is deferred. The landing descriptions (think-gidf) carry the runner's unexecuted status and limits instead.
