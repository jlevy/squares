---
type: is
id: is-01m28p7hk413y0vtx12w7jba2v
title: "Phase 6A: the workbench's palette comes from sqpack, not a copy"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T16:53:50.307Z
updated_at: 2026-09-11T16:53:50.307Z
---
The page has its own PALETTE and SHADES tables, copied from sqpack/render/style.py and sqpack/render/color.py and kept in step by hand. compare_palette.py measures that they still agree, which is a check standing in for a guarantee -- and it only agrees today because someone noticed it did not.

build_candidate.py should emit them into the page from the modules themselves at generation time: the twenty hues, the five-shade ramp, the angle-class tolerance and the hue-order contract. Then a palette change reaches the workbench the way it reaches every other drawing in this repository, and compare_palette.py goes back to being what it should be -- a check that the PAGE draws what the modules say, rather than the only thing keeping two copies in step.

Done when: no colour constant in template.html is written by hand, and changing SQUARE_HUE_PALETTE changes the built page.
