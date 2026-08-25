---
type: is
id: is-01m0vtngjde38hddb52a2y3tb1
title: Integrate SVG toolkit with current main and add a large gallery example
kind: task
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels: []
dependencies: []
created_at: 2026-08-25T06:45:32.860Z
updated_at: 2026-08-25T06:45:32.860Z
---
Resolve the origin/main engineering-maturity refactor into the deterministic SVG toolkit without preserving obsolete tools, top-level sqpack, or test.sh paths. Move reusable renderer code under src/sqpack, case adapters under cases, and generators/checkers under devtools; register validation with packing-validate. Systematically regenerate and verify every Markdown-embedded packing SVG with the approved palette, add a provenance-safe larger example (prefer exact n=29) to the retained gallery, README, and tutorial, then run full validation, push, and confirm PR CI.
