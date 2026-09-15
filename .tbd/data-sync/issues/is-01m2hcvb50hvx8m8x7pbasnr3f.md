---
type: is
id: is-01m2hcvb50hvx8m8x7pbasnr3f
title: Admit the Route A same-corner availability-root experiment at q=96/25
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - admission
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
created_at: 2026-09-15T02:03:03.199Z
updated_at: 2026-09-15T02:37:41.848Z
---
After BC-353 selects Route A, freeze one complete same-corner availability-blocker root at q=96/25: the physical root definition and 16-root denominator, shared continuous parent variables, all label/pose/incidence strata, strict-core transfer, matched point baseline, candidate conditional capacities, exact full-domain checker, positive and adversarial controls, acceptance rule, and representation-level kill rule. Run no scientific target in this admission block. Merge its separate PR before the discriminator run.

## Notes

Selected by BC-353 after three independent Astra Max route audits. Run as the next 75-minute no-target admission PR from the merged planning branch; freeze the 16-root denominator, one complete same-corner root at 96/25, all strata, shared geometry, matched baseline, exact controls, independent checker, and accept/kill rules. Route S is the fallback if admission fails.
