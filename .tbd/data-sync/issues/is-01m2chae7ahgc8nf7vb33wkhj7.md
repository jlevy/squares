---
type: is
id: is-01m2chae7ahgc8nf7vb33wkhj7
title: Validate imported animations before assigning numerical evidence
kind: bug
status: in_progress
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels:
  - workbench-roadmap
  - workbench-phase-1
dependencies:
  - type: blocks
    target: is-01m2chahf57z4w9tj5gehbs0td
  - type: blocks
    target: is-01m2b7na7psnnn1j62g1yjdtta
  - type: blocks
    target: is-01m2ckzvnsawqg79z9ybspc3yt
  - type: blocks
    target: is-01m2chr65cx0jhfd1gsmx3r31y
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T04:44:59.989Z
updated_at: 2026-09-13T06:17:27.747Z
---
Review R1 at 6e191a35: animation_from_trace.py:148-167 defaults missing feasible to true and creates CheckSummary(passed=True) without checking poses. Two coincident unit squares in side 1 export with numerically-checked metadata. Validate shape, finite geometry, counts, walls and pairs at import; missing evidence stays candidate; carry actual check provenance. Add negative import/export regression and valid-record control.
