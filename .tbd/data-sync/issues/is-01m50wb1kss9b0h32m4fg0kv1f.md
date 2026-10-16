---
type: is
id: is-01m50wb1kss9b0h32m4fg0kv1f
title: Use surnames by default throughout News titles and details
kind: task
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
child_order_hints:
  - is-01m50xpb6z1n1wcs43g1nm3f43
hold: null
hold_until: null
created_at: 2026-10-15T22:53:46.477Z
updated_at: 2026-10-16T02:00:42.565Z
started_at: 2026-10-15T22:54:30.080Z
---
User requests surnames only, unless ambiguous, in every News title and detail. Audit existing headline, summary and details and any generated News-only credit presentation. Preserve full canonical attribution, sources, result status, math, dates, corporate names and necessary disambiguation. Document the same editorial rule for future intake. Implement as a compatible reviewed site patch without restarting unrelated in-flight CI; verify generated homepage and archive output.

## Notes

2026-10-16 continuation: Surname changes consolidated into PR633 head3d0d61e61675295af2b777cf8d66fe7f33addafa. All41 articles/133 labels audited;26entries/64 substitutions; URLs, code and math preserve original tokens. Boundary A1 fixed through ordinary-text callback and61 passing contracts. Current final senior review and deployment pending.

2026-10-16 final integration: formal stack635 now targets main ee9cec6e after intake632 and S1 replies626/625. News633 head e31ca7787b1e0838c07a195f71802b6ee7cf6788; CI634 head098009354b4191d774f56f659e0fa90706c1f2a4. Sitev0.7.12, inherited scientific pin e35725f0 and claim source6ba43f14. Separate T191/T192 S3 V0/C0 stories retain unchanged standing bounds; shared delivery keeps full audit/frozen provenance.63 focused tests passed17.60s after2 expected-red controls; sitecut111passed/15deselected90.99s; native70passed155.56s and Python types0errors170.71s before the two metadata-only rebases. Requests, claim generation and final publication/URL contracts rechecked (48.14s). Final current-head reviews and ordinaryCI are pending; do not close until merge/live verification. Prior8d/78df all4workflows passed with actual51forwarders/0skips and original900s shareddeadline. New metadata-churn followup think-m2fn; original causal stall and broader3min goal remain open.
