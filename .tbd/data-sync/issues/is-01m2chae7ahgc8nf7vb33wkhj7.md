---
type: is
id: is-01m2chae7ahgc8nf7vb33wkhj7
title: Validate imported animations before assigning numerical evidence
kind: bug
status: closed
priority: 1
version: 9
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
updated_at: 2026-09-13T08:32:22.337Z
closed_at: 2026-09-13T08:32:22.336Z
close_reason: Implemented at 15d97a59 after foundation f9099096. All Python animation/render/SVG consumers independently re-admit supplied geometry, preserve prefix guidance and validate record references. Shared Python/TypeScript fixture rejects false feasible claims; 124 package Python tests and actual browser import/edit/export/capture checks pass.
resolution: null
duplicate_of: null
---
Review R1 at 6e191a35: animation_from_trace.py:148-167 defaults missing feasible to true and creates CheckSummary(passed=True) without checking poses. Two coincident unit squares in side 1 export with numerically-checked metadata. Validate shape, finite geometry, counts, walls and pairs at import; missing evidence stays candidate; carry actual check provenance. Add negative import/export regression and valid-record control.

## Notes

Package consumer migration implemented; 105 Python contract tests pass. Shared Python/TypeScript fixture checks IDs, geometry and prefix guidance. SVG consumers re-admit dataclasses. Awaiting next committed checkpoint before closure.
