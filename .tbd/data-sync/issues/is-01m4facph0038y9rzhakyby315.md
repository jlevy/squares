---
type: is
id: is-01m4facph0038y9rzhakyby315
title: Open the hero case popover and navigate to expanded Atlas cases
kind: feature
status: in_progress
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels:
  - website
dependencies:
  - type: blocks
    target: is-01m4ex3gpzxxh9eqemc2r78p4e
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-09T03:13:00.958Z
updated_at: 2026-10-09T04:19:58.532Z
started_at: 2026-10-09T03:14:19.707Z
---
Homepage hero contains three native packing SVG examples in order11,26,53 (latest counts supersede17). Side by side and centered, capped width on wide screens; narrow screens fill text width with a small margin. One caption names best packings known for11,26,and53 squares. Each opens its own existing case popover and retains a canonical ordinary case-record link for noJS. Keep social preview case53 unchanged. Shared popover actions for Case Record, Frontier row and Atlas tile follow current case; Atlas target fully expands before reveal. Preserve relative URLs, noJS and history. Verify hero11/26/53 plus existing291/324 navigation; shared expansion tracked by think-hyd6.

## Notes

Hero53 opens the one shared case popover, ordinary cases/53.html noJS fallback. Popover offers record, survey-row atlas.html#n-N and diagram atlas.html#atlas-n-N actions updated on case stepping. Diagram links fully expand the Atlas before focus/scroll, use native hash navigation for correct target highlight and history, and have noJS all-tiles fallback. Eighteen focused browser/markup/link cases passed including53/291/324, both arrow steps, same/different hashes and triangle/large Back/Forward. Node fetch/fallback26pass; typed/browser/Python floors clean. Astra source review clean. Full core +paperHTML+Workbench preview rebuilt; no PDFs regenerated, no commit/push.
