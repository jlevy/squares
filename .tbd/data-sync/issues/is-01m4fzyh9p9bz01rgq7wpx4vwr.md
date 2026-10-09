---
type: is
id: is-01m4fzyh9p9bz01rgq7wpx4vwr
title: "INLINE_LINK in run_negative_controls ignores #fragment links (latent worker-copy hole)"
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels:
  - n-17
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
created_at: 2026-10-09T09:29:45.526Z
updated_at: 2026-10-09T09:29:45.526Z
---
INLINE_LINK (\]\(([^)#\s]+)\)) never matches links that carry a #fragment, so link rescue misses files reached only through fragment links. ledger check stats docs/.../n11_research_review.md, reachable from campaign Markdown only via #fragment links; it is in workers only because one review links it without a fragment. If that link changes, ~35 ledger-check controls go red. Found during #464 prune tracing (scratchpad 464-prep). Fix: match fragment links (strip the fragment) and add a control.
