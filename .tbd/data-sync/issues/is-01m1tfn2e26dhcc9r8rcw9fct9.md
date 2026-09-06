---
type: is
id: is-01m1tfn2e26dhcc9r8rcw9fct9
title: Remove legacy condition uses of C0–C5 from durable reviews
kind: bug
status: closed
priority: 1
version: 5
labels:
  - documentation
dependencies: []
parent_id: is-01m1sn5t0dm6rjj200pw5p1b7a
created_at: 2026-09-06T04:29:31.456Z
updated_at: 2026-09-06T07:05:06.543Z
closed_at: 2026-09-06T07:05:06.542Z
close_reason: Legacy certificate-condition collisions were removed from maintained prose and the audit passes repository validation.
resolution: null
duplicate_of: null
---
Audit every durable C0 through C5 occurrence. These tokens are reserved exclusively for epistemic confirmation levels. Rewrite the old certificate-condition labels in docs/project/reviews/review-2026-09-04-pr80-stacked-hardening.md without C-tokens while preserving the historical mapping, and decide the same literal-policy issue for quoted old labels in the PR78 adversarial review. Run Flowmark, documentation checks, and exact rg evidence before closing.

## Notes

Completed the durable terminology audit. Six offender files now use descriptive Program/Step or Control labels; PR78/PR80 prior repairs remain intact. Remaining matches were classified as genuine epistemic/convention references, generated views, source-faithful archive/external notation, one preserved historical quotation, or mathematical symbols. Flowmark, diff-check, documentation checks, edit validation, and pre-push validation pass.
