---
type: is
id: is-01m0vtngjde38hddb52a2y3tb1
title: Integrate SVG toolkit with current main and add a large gallery example
kind: task
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels: []
dependencies: []
created_at: 2026-08-25T06:45:32.860Z
updated_at: 2026-08-25T07:27:53.552Z
closed_at: 2026-08-25T07:27:53.551Z
close_reason: Merged current origin/main, ported the renderer to the mature layout, added and embedded verified n=29, regenerated all gallery SVGs with renderer v4, added systematic embed/palette controls, and passed the full 32-step gate plus focused post-merge gates.
resolution: null
duplicate_of: null
---
Resolve the origin/main engineering-maturity refactor into the deterministic SVG toolkit without preserving obsolete tools, top-level sqpack, or test.sh paths. Move reusable renderer code under src/sqpack, case adapters under cases, and generators/checkers under devtools; register validation with packing-validate. Systematically regenerate and verify every Markdown-embedded packing SVG with the approved palette, add a provenance-safe larger example (prefer exact n=29) to the retained gallery, README, and tutorial, then run full validation, push, and confirm PR CI.
