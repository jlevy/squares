---
type: is
id: is-01m28p88bksqacpaddf7gkw4mz
title: "Phase 6C: the workbench's gates run where gates run"
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
created_at: 2026-09-11T16:54:13.617Z
updated_at: 2026-09-13T05:42:45.600Z
closed_at: 2026-09-13T05:42:45.599Z
close_reason: "Superseded by think-kpvc: current bounded semantic PR coverage, measured tier budgets and negative controls own this gate work. No implementation completion claimed."
resolution: null
duplicate_of: null
---
check_workbench.py, check_revision6.py, check_revision7.py and test_candidate.py are run by hand, which means they are run when someone remembers. Between them they are the only thing holding the page's behaviour: the colour map, the force law, the relationship graph, the hand-drawn contact graph, the panel's fit, and now the trajectory-cost ceiling.

They belong on the pull-request surface under packing-validate, as a step with a declared budget like every other. check_workbench alone is about 90 seconds in the pinned headless shell, so it is a --fast step rather than an --edit one; test_candidate's full type-and-fit sweep over 324 pairs is slower and may belong in the deep gate.

Depends on 6B for the lint floor, though not strictly -- a gate can run code the floor does not cover.

Done when: a change to template.html that breaks the colouring fails a pull request.
