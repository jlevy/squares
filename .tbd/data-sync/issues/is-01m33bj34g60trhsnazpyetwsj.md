---
type: is
id: is-01m33bj34g60trhsnazpyetwsj
title: Set the n in the legend's 'holding n unit squares' as math, like s(n)
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T01:26:51.279Z
updated_at: 2026-09-22T01:57:09.272Z
closed_at: 2026-09-22T01:57:09.271Z
close_reason: "80f597f9e: the sentence's n is KaTeX math from the same build as s(n) (bound_html.n), inline in the words, and held to the sentence's line by the same two rules."
resolution: null
duplicate_of: null
---
The owner (2026-09-21): in the stage legend's first row, 's(n) is the side of the smallest square holding n unit squares', the second n is plain text while the first is KaTeX math. Both are the same variable and should read the same: render the n in the sentence as math too (buildStageNote in packages/workbench/src/application.js, from the same KaTeX build that makes bound_html.side_of). Do it with think-clnq, since both change that row, and hold both n's to the sentence's baseline in the same check.
