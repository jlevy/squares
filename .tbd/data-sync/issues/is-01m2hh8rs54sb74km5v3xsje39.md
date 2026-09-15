---
type: is
id: is-01m2hh8rs54sb74km5v3xsje39
title: Decide whether the step chips belong in Animate
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m2gyhqfmr0xpcjsr34na3acq
created_at: 2026-09-15T03:20:17.444Z
updated_at: 2026-09-15T03:20:17.444Z
---
Found 2026-09-14 by lane D-page's port of the legacy checkers; an owner question, not a review finding.

`updateStepChooser` in `packages/workbench/src/application.js` sets `#step-chips` hidden whenever the mode is not Pack ("the quick picks are Pack's"), but `.chips { display: inline-flex }` in `packages/workbench/assets/workbench.css` is declared after the `[hidden]` rule with equal specificity, so Animate draws the chips anyway. Since the independent Pack panel replaced the legacy Pack view, the attribute hides the chips nowhere a viewer can see.

Decide which is intended: chips in Animate (drop the stale `hidden` toggle) or no chips (a `.chips[hidden]` rule, a visible change). The ported `single_view` check in `animate_view_contract.py` deliberately asserts neither.
