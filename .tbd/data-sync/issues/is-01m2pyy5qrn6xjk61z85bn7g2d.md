---
type: is
id: is-01m2pyy5qrn6xjk61z85bn7g2d
title: Apply one rigorous design system and consistent layout across every workbench tab
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-17T05:55:22.487Z
updated_at: 2026-09-17T20:57:26.105Z
closed_at: 2026-09-17T20:57:26.104Z
close_reason: "Landed on main: PR #191 (merge fa4c8d84) and PR #192 (merge fc988f86), 2026-09-17. Hosted CI green on both heads; owner questions in the PR descriptions remain open as follow-ups."
resolution: null
duplicate_of: null
---
Owner request 2026-09-17: the workbench still shows many visual variations, and page layout is uneven on some tabs. Apply a highly consistent design system (tokens for colour roles, spacing scale, type scale, radii, borders, control sizes, layout grid) and enforce it everywhere in packages/workbench (assets/workbench.css, assets/template.html, inline styles in src/), so every tab shares one rigorous, clean page layout. At main 035d84c6 the stylesheet is 1,374 lines with 17 custom properties, 24 distinct hex colours and 78 distinct px values, and 19 inline-style sites in TypeScript. Done when: a checked-in contract refuses raw design values outside the token layer (allowlist only shrinks); a checked-in browser check measures layout consistency across every tab at the declared viewport sizes; before/after screenshots of every tab at each viewport are reviewed; all existing workbench, accessibility and page contracts still pass. Serves O6 (clear, accessible UI).

## Notes

2026-09-17: PR #192 (b5ac510b), stacked on #191; fixture suppression fix 3db43561 rebased; combined-code checks pass (package 201/201, workbench pytest 311, floor contract 55, deterministic build, frontend tier). Description lists visible changes for owner review. Merge after #191.
