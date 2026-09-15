---
type: is
id: is-01m2cj9hf5v77se0yyzbr5jqd6
title: Give the workbench stage keyboard and reduced-motion support
kind: task
status: open
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-2
dependencies:
  - type: blocks
    target: is-01m2chahf57z4w9tj5gehbs0td
  - type: blocks
    target: is-01m2ckzvnsawqg79z9ybspc3yt
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T05:01:59.126Z
updated_at: 2026-09-15T03:33:25.281Z
---
Review found template labels a generic container while hiding the role=img SVG, and no reduced-motion path in workbench. Expose a current accessible title/description, keyboard manipulation and transport controls, focus behavior, and reduced-motion playback policy. Reuse Motion Lab contract patterns and verify the served stage with behavioral accessibility checks. Consolidate implementation and tests in packages/workbench; no separate UI system.

## Notes

2026-09-14, lane D-page (PR #160 review D62, D65): the Pack panel's keys go through one tested map that ignores Ctrl, Meta and Alt, and its live regions announce state changes only (dd0858a3, think-65qo, think-wheg).
