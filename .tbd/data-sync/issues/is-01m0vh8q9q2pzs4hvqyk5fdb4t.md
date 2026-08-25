---
type: is
id: is-01m0vh8q9q2pzs4hvqyk5fdb4t
title: Use fixed visual tokens and certified contact marks in packing SVGs
kind: feature
status: closed
priority: 1
version: 8
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels: []
dependencies: []
created_at: 2026-08-25T04:01:16.590Z
updated_at: 2026-08-25T06:40:26.519Z
closed_at: 2026-08-25T06:40:13.589Z
close_reason: Implemented and committed the fixed cool palette, pure-black boundary system, clipped certified contact marks, updated docs/spec, regenerated gallery, and 73-control/full-gate validation in daca22e.
resolution: null
duplicate_of: null
---
Centralize the approved document style as fixed constants: a deterministic 20-color cool square palette, opaque pure-black 1.25px container and square outlines, and tempered-yellow #e3c64a contact segments/dots at 60% opacity with 9px segment width and 5.5px point radius. Keep fills, contacts, and outlines in explicit order; clip every contact mark to the union of its exact participating square interiors; preserve optional contact display, exact semantic annotations, deterministic generation, CLI/docs/atlas integration, retained examples, and structural/visual regression controls.

## Notes

Implemented in commit daca22e and pushed on codex/packing-svg-rendering-toolkit. SVG rendering checker passes 73 controls; Ruff and BasedPyright pass; ./test.sh passes all 31 repository steps; make format-check passes; retained SVGs and manifest/metrics were regenerated and visually inspected at 900px and 2400px.
