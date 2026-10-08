---
type: is
id: is-01m4ex3427hyrmyny5yan8sryb
title: Repair case n=291 math on its page and popover
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
labels:
  - website
dependencies:
  - type: blocks
    target: is-01m4ex3gpzxxh9eqemc2r78p4e
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
created_at: 2026-10-08T23:20:35.650Z
updated_at: 2026-10-08T23:20:48.607Z
---
Reproduce the reported ugly or broken mathematics on cases/291.html and its atlas/Frontier popover at mobile and desktop sizes before diagnosing the cause. Inspect the long inline verified interval, plain-ASCII general-bound prose, prepared math/font inheritance, and local containment. Correct the actual failure without changing mathematical meaning, and retain a regression checking math errors, missing glyphs, raw markup and clipping. See L1 and Case pages and popovers in the spec.
