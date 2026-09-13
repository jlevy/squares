---
type: is
id: is-01m2chr65cx0jhfd1gsmx3r31y
title: Put workbench behavioral checks on the PR validation surface
kind: task
status: open
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-2
dependencies:
  - type: blocks
    target: is-01m2chahf57z4w9tj5gehbs0td
  - type: blocks
    target: is-01m2ckzvnsawqg79z9ybspc3yt
  - type: blocks
    target: is-01m2chakgrn8keadss1jcs401b
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T04:52:30.506Z
updated_at: 2026-09-13T05:43:46.832Z
---
Review: build_workbench_site claims workbench checkers run in packing-validate, but reviewed leaf only wires Biome/tsc; workbench Python Playwright programs are outside default tests and validation. Choose a small semantic suite for startup, run/reset/mode transitions, finite validity, shared seed replay, raw/repaired results and frame/export provenance. Wire into the existing tier partition with measured budgets and config-contract tests. Preserve unique spike assertions during package migration; do not gate source-string/revision checks by default.
