---
type: is
id: is-01m1tfn2e26dhcc9r8rcw9fct9
title: Remove legacy condition uses of C0–C5 from durable reviews
kind: bug
status: in_progress
priority: 1
version: 3
labels:
  - documentation
dependencies: []
parent_id: is-01m1sn5t0dm6rjj200pw5p1b7a
created_at: 2026-09-06T04:29:31.456Z
updated_at: 2026-09-06T05:43:59.418Z
---
Audit every durable C0 through C5 occurrence. These tokens are reserved exclusively for epistemic confirmation levels. Rewrite the old certificate-condition labels in docs/project/reviews/review-2026-09-04-pr80-stacked-hardening.md without C-tokens while preserving the historical mapping, and decide the same literal-policy issue for quoted old labels in the PR78 adversarial review. Run Flowmark, documentation checks, and exact rg evidence before closing.

## Notes

Post-T+2 xhigh editorial audit complete. Six confirmed offender files now use descriptive Program/Step or Control labels: strategy review; BC152 readiness review; BC158 factual review; X-012; exp-058; session-067. PR78/PR80 prior fixes remain. All six have zero bare C0-C5/C1-C8 collisions, exactly one footer, Flowmark --no-cache pass, and diff-check pass. Remaining 458 repository matches were classified as 212 genuine epistemic/convention references, 41 generated views, 203 source-faithful/archive or external notation, one preserved PR80 historical quotation, and one mathematical symbol; no additional offender found. Close after repository documentation validation confirms.
