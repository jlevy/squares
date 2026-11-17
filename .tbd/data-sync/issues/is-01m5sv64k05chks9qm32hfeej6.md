---
type: is
id: is-01m5sv64k05chks9qm32hfeej6
title: "Exact-side register slice 3: every count 1..324 (degree-1 houses by reference, numeric gaps)"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-10-25-exact-side-register.md
labels:
  - project
dependencies: []
parent_id: is-01m5sv3xcxr02a4019fz9bbmn9
created_at: 2026-10-25T15:34:37.920Z
updated_at: 2026-10-25T15:34:37.920Z
---
Slice 3 of the exact-side register (spec docs/project/specs/active/plan-2026-10-25-exact-side-register.md; epic think-gbr2; tracker #811). Make the register cover every count 1..324: each remaining house as a degree-1 fact by reference to its record (a rational exact form is not copied, since some run to thousands of digits, as n = 29's does), and the numeric gaps at 55 and 71 as explicit absences naming their beads (think-phh8, think-1blg), so a reader finds any count's exact side in one place.

Waits on the owner's answer to the spec's first open question (also "Decisions for the Owner" on the slice-1 pull request): list every count, rational houses included, or keep the register to algebraic facts. Price: about 2 agent-hours; the check stays a few seconds.
