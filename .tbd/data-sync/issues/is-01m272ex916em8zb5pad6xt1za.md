---
type: is
id: is-01m272ex916em8zb5pad6xt1za
title: Add a container mechanism so the side is a phase
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T01:49:05.696Z
updated_at: 2026-09-11T01:49:05.696Z
---
Map row 9. devtools/packing_strategy.py gains a container mechanism in MECHANISMS with _run_container, so a strategy can resize its box as a declared phase rather than as a side effect of project or ratchet. The ascent's Open and Close beats are this mechanism run twice with different targets, which is why it comes before the ascent generator.

sqpack.render.motion already animates a changing container side as of 72ed5e4f, so the rendering half is done; this is the strategy half.
