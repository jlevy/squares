---
type: is
id: is-01m25zs0w1ctenbb2c5wt9q06v
title: Decide the T-026 explainer architecture from a source-bound complexity audit
kind: task
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - explainer
dependencies:
  - type: blocks
    target: is-01m25zs0ygtqsqfx233fhjrxqf
parent_id: is-01m25zrj5np9ywft00t8j8neaz
created_at: 2026-09-10T15:42:56.895Z
updated_at: 2026-09-10T16:52:13.708Z
closed_at: 2026-09-10T15:56:54.082Z
close_reason: "Accepted incremental explainer architecture: preserve the point-only T-018 teaching spine and interactive figures; add a source-derived advanced T-025/T-026 section and current weak-bound headline. Decision recorded in docs/project/reviews/review-2026-09-10-n11-explainer-architecture.md."
resolution: null
duplicate_of: null
---
Audit the current explainer source, renderer, figures, tests, T-025 proof, T-026
dilation proof, and canonical interpretation documents. Produce a short decision
record choosing incremental extension or full tighter-case rewrite before prose or
figures are changed.

Choose the incremental architecture when the simple point certificate remains a
correct and substantially clearer teaching spine and the tighter result can be
explained by a bounded extension that defines threshold atoms, their packing budget,
the exact T-025 endpoint, and T-026 dilation. Choose the full rewrite only if keeping
the simple case would make the headline materially misleading or require parallel
explanations whose combined complexity exceeds one coherent tighter-case treatment.

Record every stale headline, number, verifier claim, certificate toggle, figure,
caption, link, and test affected by either choice. Keep the result's evidential status
and endpoint qualification explicit. This is a documentation determination, not a
scientific result.

## Notes

The accepted decision is retained in this bead and the standalone draft PR: preserve T-018's point-only teaching spine and interactive figures, then add a source-derived advanced T-025/T-026 section. The temporary source-bound audit remains at /private/tmp/n11-explainer-architecture-plan.md; no new mapped durable review file was added.
