---
type: is
id: is-01m1tfn2e26dhcc9r8rcw9fct9
title: Remove legacy condition uses of C0–C5 from durable reviews
kind: bug
status: in_progress
priority: 1
version: 2
labels:
  - documentation
dependencies: []
parent_id: is-01m1sn5t0dm6rjj200pw5p1b7a
created_at: 2026-09-06T04:29:31.456Z
updated_at: 2026-09-06T04:37:29.122Z
---
Audit every durable C0 through C5 occurrence. These tokens are reserved exclusively for epistemic confirmation levels. Rewrite the old certificate-condition labels in docs/project/reviews/review-2026-09-04-pr80-stacked-hardening.md without C-tokens while preserving the historical mapping, and decide the same literal-policy issue for quoted old labels in the PR78 adversarial review. Run Flowmark, documentation checks, and exact rg evidence before closing.

## Notes

Concrete delegated fixes applied during the T+60-T+90 slice: PR80's historical mapping now uses descriptive former-condition names and Condition 1-5; PR78 paraphrases the typographic old labels without re-emitting them. Both files pass flowmark --no-cache --auto --check and git diff --check; no C-subscript token remains in either. Post-T+120 fresh editorial audit must classify all remaining Markdown matches: preserve confirmation-rung uses and source-faithful/literal external identifiers, rename local control or outline uses (notably the BC152 review, X-012, and the untrusted strategy-review C1-C5 headings), then record exact rg evidence.
