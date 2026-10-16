---
type: is
id: is-01m50s7ppqb37qxtm4ty6bxw0a
title: Simplify news topics and align tag filters with card labels
kind: bug
status: in_progress
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
child_order_hints:
  - is-01m514v8x4k6258tc7fve3sa4b
hold: null
hold_until: null
created_at: 2026-10-15T21:59:31.275Z
updated_at: 2026-10-16T02:00:41.548Z
started_at: 2026-10-15T21:59:45.784Z
---
Remove Correction and Audit from News tags and filter choices while retaining Results classifications and article claims. Use matching sentence-case topic labels and shared light/dark chip colors in joined compact wrapping filter choices. Add per-topic tallies at selected significance levels, independent of selected topics; All counts unique score-matching news items. Remove duplicate topic tags from homepage news cards while retaining status, verification/confirmation, credits, caveats and full-result links. Extend the existing design rules and focused browser/news contracts, then PR, review and publish as the next site patch.

## Notes

Implemented News-only topic subset, shared sentence-case fills, score-aware topic tallies and homepage tag deduplication. PR #633 final head 3fb5508ce116e8f42f15731de1bae55a600996ec prepares site v0.7.11; lower final documentation delta removes a stale browser file count. Formal remote stack #635 consists of #633 then CI repair #634 head 7f5c351e51abe2d244373438ced606a38fa955fe. Source and browser contracts passed; final-head reviews and hosted CI are in flight. All 43 S3+ results registered October 8–15 on main22a67 have News-visible coverage. Pending #627 results are not announced as merged. Close after exact merge and deployment verification.

2026-10-16 continuation: Final consolidated PR633 head3d0d61e61675295af2b777cf8d66fe7f33addafa pushed in formal stack635 below634. One prepared site v0.7.11;61 News contracts,111 cut controls,19 edition/impact controls passed. Five native floors passed (Ruff corrected literal wraps,1.10s recheck). Current hosted Packing38833352952/Pages38833352987 in progress; final independent senior review and live verification pending.

2026-10-16 final integration: formal stack635 now targets main ee9cec6e after intake632 and S1 replies626/625. News633 head e31ca7787b1e0838c07a195f71802b6ee7cf6788; CI634 head098009354b4191d774f56f659e0fa90706c1f2a4. Sitev0.7.12, inherited scientific pin e35725f0 and claim source6ba43f14. Separate T191/T192 S3 V0/C0 stories retain unchanged standing bounds; shared delivery keeps full audit/frozen provenance.63 focused tests passed17.60s after2 expected-red controls; sitecut111passed/15deselected90.99s; native70passed155.56s and Python types0errors170.71s before the two metadata-only rebases. Requests, claim generation and final publication/URL contracts rechecked (48.14s). Final current-head reviews and ordinaryCI are pending; do not close until merge/live verification. Prior8d/78df all4workflows passed with actual51forwarders/0skips and original900s shareddeadline. New metadata-churn followup think-m2fn; original causal stall and broader3min goal remain open.
