---
type: is
id: is-01m4evfrx2qs5jk9zav4fc9ym2
title: "n17 PR404 D1: annotate historical guarded-clause sign notation"
kind: chore
status: open
priority: 3
version: 1
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels:
  - n-17
dependencies: []
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
created_at: 2026-10-08T22:52:33.057Z
updated_at: 2026-10-08T22:52:33.057Z
---
PR404 full review D1, pinned head 1d1691bf5e6e1115ad1597b5f72bbd12ad9b0b88.

H315 repeats historical 'quadratic minima<=0' shorthand without a local annotation.
Exp307 and its research report already explain the notation error. Astra confirmed
the frozen implementation contract is MIN(clearance slack)>=0, equivalently
MAX(negative slack)<=0.

Append a concise factual Annotation linking the existing exp307 clarification.
Preserve the frozen criterion, regime, body, threshold, outcome and source identity;
do not retrospectively retune or promote the result.
