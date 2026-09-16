---
type: is
id: is-01m2gyhqfmr0xpcjsr34na3acq
title: "[epic] Workbench page feedback, 2026-09-14"
kind: epic
status: open
priority: 1
version: 11
labels: []
dependencies: []
child_order_hints:
  - is-01m2gyhsq5nec3wqw4c13c1x8j
  - is-01m2gyhvzcw159a5ew5hqbp7bv
  - is-01m2gyhy8jxc1p27shs4gfdkj0
  - is-01m2gyhzmdg3h1ptq6b2h74z4q
  - is-01m2gyj13czgw7vy7p6xsj0sxy
  - is-01m2gyj2x0wjbbqzmcvfbkr0zn
  - is-01m2h0qefn5vq2a94cz26em504
  - is-01m2hh8rs54sb74km5v3xsje39
  - is-01m2m2zmky0p8gw5m4zctfnfex
created_at: 2026-09-14T21:53:08.083Z
updated_at: 2026-09-16T03:08:21.501Z
---
Owner feedback on the workbench page, 2026-09-14, given while reviewing the page built from claude/annealing-search-benchmark (PR #155). PR #160's consolidated page (`packages/workbench`) still has every one of these (checked 2026-09-14: kind-tag in its template, no modifier guard in its keydown handlers, the whole numeral rolls, the step row sits in its own white block), so each fix must reach both: made here and carried through the merge into #160, or made once on #160 if the stack is re-based there.

Children: the static `n =`, even space around the headline, the ambiguous closed-form lines, the top-left kind tag, shortcuts firing under modifier keys, and the step row joining the regular controls.

## Notes

2026-09-14, lane D-page: the page-removal leftovers (D87) are cleaned up in bf0b8ed7 (think-c1bm). A new owner question from the legacy-checker port is think-8amg: the step chips are marked hidden outside Pack, but the stylesheet draws them in Animate.
