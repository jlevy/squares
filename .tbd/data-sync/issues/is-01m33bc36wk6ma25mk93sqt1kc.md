---
type: is
id: is-01m33bc36wk6ma25mk93sqt1kc
title: Stage text shows a grey selection highlight during the animation
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T01:23:34.747Z
updated_at: 2026-09-22T01:57:09.977Z
closed_at: 2026-09-22T01:57:09.976Z
close_reason: "80f597f9e: the stage refuses text selection (user-select: none on #stage). Reproduced first: on a control page without the rule, a double-click and drag selected the badges, the headline's 11 and the gap bar's 3.826447. check_animate_view's stage_takes_no_selection makes those gestures on every run and passes with the rule."
resolution: null
duplicate_of: null
---
The owner (2026-09-21) sees text on the stage drawn with a slight grey background while the animation plays, as if it were selected. Suspected cause: the stage's text (the headline, the facts, the legend) is ordinary selectable HTML, so a click, drag or double-click on the stage, or a select-all, leaves a browser selection that is repainted on every frame. Reproduce it on the built page, find what makes the selection, and fix it at the cause (for example the stage not being a text-selection surface), then add a check that the stage carries no selection after the gestures that caused it. A captured video must never show it.
