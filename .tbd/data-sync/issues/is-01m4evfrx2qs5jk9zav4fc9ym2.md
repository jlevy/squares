---
type: is
id: is-01m4evfrx2qs5jk9zav4fc9ym2
title: "n17 PR404 D1: annotate historical guarded-clause sign notation"
kind: chore
status: closed
priority: 3
version: 4
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: root
labels:
  - n-17
dependencies: []
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
hold: null
hold_until: null
created_at: 2026-10-08T22:52:33.057Z
updated_at: 2026-10-08T23:43:06.796Z
started_at: 2026-10-08T22:53:01.554Z
closed_at: 2026-10-08T23:43:06.796Z
close_reason: Bounded B3/D1 repairs published in PR404 0a8b46e13/18e3a6f4f and propagated unchanged to both children; targeted verification and exact-readback dispositions recorded. Current required CI/full qualification remains open under think-0m0x; no merge readiness or new mathematical result claimed.
resolution: null
duplicate_of: null
---
PR404 full review D1, pinned head 1d1691bf5e6e1115ad1597b5f72bbd12ad9b0b88.

H315 repeats historical 'quadratic minima<=0' shorthand without a local annotation.
Exp307 and its research report already explain the notation error. Astra confirmed
the frozen implementation contract is MIN(clearance slack)>=0, equivalently
MAX(negative slack)<=0.

Append a concise factual Annotation linking the existing exp307 clarification.
Preserve the frozen criterion, regime, body, threshold, outcome and source identity;
do not retrospectively retune or promote the result.

## Notes

October 8 published current-main consolidation:
D1 annotation is committed in 0a8b46e13 and published at integrated PR404 head 18e3a6f4f20f534e80074131d4947c633cca5ef3; exact source parity retains it through both children. H315 appends the correction of historical sign shorthand; frozen acceptance criterion, original body, result, quantities and source identity are unchanged. Astra reviewed semantics and documentation/campaign checks pass. Published exact-readback verified disposition: https://github.com/jlevy/squares/pull/404#issuecomment-6071220456. Close bounded documentation finding only; no new proof or current full checkpoint claim.
Review: https://github.com/jlevy/squares/blob/18e3a6f4f20f534e80074131d4947c633cca5ef3/docs/project/reviews/review-2026-10-08-n17-merge-readiness.md
Progress: https://github.com/jlevy/squares/issues/405#issuecomment-6071221013
