---
type: is
id: is-01m272ex916em8zb5pad6xt1za
title: Add a container mechanism so the side is a phase
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T01:49:05.696Z
updated_at: 2026-09-11T05:13:29.321Z
closed_at: 2026-09-11T05:13:29.307Z
close_reason: "Built: devtools/packing_strategy.py MECHANISMS carries 'container' with _run_container, which resizes the box as a declared phase and scales centres about the container's middle so a square against a wall stays against it. The ascent's Open and Close beats run it twice with different targets."
resolution: null
duplicate_of: null
---
Map row 9. devtools/packing_strategy.py gains a container mechanism in MECHANISMS with _run_container, so a strategy can resize its box as a declared phase rather than as a side effect of project or ratchet. The ascent's Open and Close beats are this mechanism run twice with different targets, which is why it comes before the ascent generator.

sqpack.render.motion already animates a changing container side as of 72ed5e4f, so the rendering half is done; this is the strategy half.
