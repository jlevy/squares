---
type: is
id: is-01m50wb1kss9b0h32m4fg0kv1f
title: Use surnames by default throughout News titles and details
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
child_order_hints:
  - is-01m50xpb6z1n1wcs43g1nm3f43
hold: null
hold_until: null
created_at: 2026-10-15T22:53:46.477Z
updated_at: 2026-10-16T01:08:25.338Z
started_at: 2026-10-15T22:54:30.080Z
---
User requests surnames only, unless ambiguous, in every News title and detail. Audit existing headline, summary and details and any generated News-only credit presentation. Preserve full canonical attribution, sources, result status, math, dates, corporate names and necessary disambiguation. Document the same editorial rule for future intake. Implement as a compatible reviewed site patch without restarting unrelated in-flight CI; verify generated homepage and archive output.

## Notes

2026-10-16 continuation: Surname changes consolidated into PR633 head3d0d61e61675295af2b777cf8d66fe7f33addafa. All41 articles/133 labels audited;26entries/64 substitutions; URLs, code and math preserve original tokens. Boundary A1 fixed through ordinary-text callback and61 passing contracts. Current final senior review and deployment pending.
