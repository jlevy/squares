---
type: is
id: is-01m2pz4tzrwqmxx3gze7axphq9
title: "New square: adjustable delay after the shrink, then a smooth fade-in at full size"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-17T05:59:00.856Z
updated_at: 2026-09-17T20:57:25.240Z
closed_at: 2026-09-17T20:57:25.237Z
close_reason: "Landed on main: PR #191 (merge fa4c8d84) and PR #192 (merge fc988f86), 2026-09-17. Hosted CI green on both heads; owner questions in the PR descriptions remain open as follow-ups."
resolution: null
duplicate_of: null
---
Owner request 2026-09-17, workbench Animate transitions: (1) a slightly longer delay after the shrink phase before the new (red) square appears, adjustable from the page like the other motion settings; (2) always fade the new square in a little more smoothly; (3) never add it small and grow it: it fades in at its final size, opacity only. Applies to every path that draws the arrival (staged and continuous timing, simple transitions and fastSimple, seeking, captured SVG frames), and reduced motion keeps its existing policy. Done when timeline and scene tests pin the order (shrink, delay, fade), the full-size opacity-only arrival and the new default, and the control round-trips like existing motion settings.

## Notes

2026-09-17: PR #191 (4c2f2da2), hosted CI green, description with measurements and four owner questions (step length, grid-fill wait, minimum fade, default delay). Merge fourth in the sequence.
