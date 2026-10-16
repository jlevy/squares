---
type: is
id: is-01m50s7ppqb37qxtm4ty6bxw0a
title: Simplify news topics and align tag filters with card labels
kind: bug
status: in_progress
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
child_order_hints:
  - is-01m514v8x4k6258tc7fve3sa4b
hold: null
hold_until: null
created_at: 2026-10-15T21:59:31.275Z
updated_at: 2026-10-16T01:22:26.839Z
started_at: 2026-10-15T21:59:45.784Z
---
Remove Correction and Audit from News tags and filter choices while retaining Results classifications and article claims. Use matching sentence-case topic labels and shared light/dark chip colors in joined compact wrapping filter choices. Add per-topic tallies at selected significance levels, independent of selected topics; All counts unique score-matching news items. Remove duplicate topic tags from homepage news cards while retaining status, verification/confirmation, credits, caveats and full-result links. Extend the existing design rules and focused browser/news contracts, then PR, review and publish as the next site patch.

## Notes

Implemented News-only topic subset, shared sentence-case fills, score-aware topic tallies and homepage tag deduplication. PR #633 final head 3fb5508ce116e8f42f15731de1bae55a600996ec prepares site v0.7.11; lower final documentation delta removes a stale browser file count. Formal remote stack #635 consists of #633 then CI repair #634 head 7f5c351e51abe2d244373438ced606a38fa955fe. Source and browser contracts passed; final-head reviews and hosted CI are in flight. All 43 S3+ results registered October 8–15 on main22a67 have News-visible coverage. Pending #627 results are not announced as merged. Close after exact merge and deployment verification.

2026-10-16 continuation: Final consolidated PR633 head3d0d61e61675295af2b777cf8d66fe7f33addafa pushed in formal stack635 below634. One prepared site v0.7.11;61 News contracts,111 cut controls,19 edition/impact controls passed. Five native floors passed (Ruff corrected literal wraps,1.10s recheck). Current hosted Packing38833352952/Pages38833352987 in progress; final independent senior review and live verification pending.
