---
type: is
id: is-01m2chag118qjnczfj2zbrtx3b
title: Enforce executable strategy and animation contract semantics
kind: bug
status: closed
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels:
  - workbench-roadmap
  - workbench-phase-1
dependencies:
  - type: blocks
    target: is-01m2chahf57z4w9tj5gehbs0td
  - type: blocks
    target: is-01m2ckzvnsawqg79z9ybspc3yt
  - type: blocks
    target: is-01m2b7na7psnnn1j62g1yjdtta
  - type: blocks
    target: is-01m2chr65cx0jhfd1gsmx3r31y
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T04:45:01.855Z
updated_at: 2026-09-13T08:32:22.580Z
closed_at: 2026-09-13T08:32:22.579Z
close_reason: Implemented at 15d97a59. Typed strategy and animation contracts enforce counts, finite poses, IDs, ordered time, per-frame sides, seed domain/default receipts and guidance ancestry; unsupported execution/renderer modes reject explicitly. 124 package Python tests and shared browser import/edit/export controls pass.
resolution: null
duplicate_of: null
---
Review R2: source random/given is schema-admitted but _structure unconditionally loads record; grid phase may return fewer than n poses when round(side)^2<n; traces must retain each frame side rather than final phase side. Reject unsupported fields and enforce counts/finite poses, identity, time and provenance. Audit guide ancestry, contract conformance and seed receipt with bounded controls.

## Notes

Typed strategy/count/time/seed contracts and package migration implemented; 105 Python contract tests pass. Unsupported SVG palette modes reject explicitly. Browser importer/editor verification and committed checkpoint remain before closure.
