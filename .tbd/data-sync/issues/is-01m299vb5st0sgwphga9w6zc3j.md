---
type: is
id: is-01m299vb5st0sgwphga9w6zc3j
title: "J1: pin Biome and write the floor config"
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m299tcsrh44b8n8m1c6jpgcb
created_at: 2026-09-11T22:36:42.040Z
updated_at: 2026-09-11T22:53:31.451Z
closed_at: 2026-09-11T22:53:31.434Z
close_reason: Biome 2.5.11 pinned exact in the root package.json (15 days old, the newest clearing the 14-day rule), biome.json carrying Profile B's floor, scoped to the JavaScript and CSS this repo owns. Landed as c8e852ca.
resolution: null
duplicate_of: null
---
`@biomejs/biome` at an exact version in the root package.json, beside the pinned lefthook, with package-lock.json committed. Never npx/bunx: supply-chain-hardening forbids a runner that can fetch latest when the dependency is absent.

`biome.json` at the repository root, carrying Profile B's floor: formatter on (2-space, the repo's own line width), `style.useBlockStatements`, `correctness.noUnusedVariables` and `noUnusedImports`, `assist.actions.source.organizeImports`.

Scope it to the JavaScript and CSS this repository owns and nothing else: the workbench's assets, the probes, and any other first-party script. Excluded, each for a reason: `vendor/` (submodules we do not own), the built `site/` (generated), anything minified.

Worked example in a sibling repository: /Users/levy/wrk/aisw/trading/biome.json.
