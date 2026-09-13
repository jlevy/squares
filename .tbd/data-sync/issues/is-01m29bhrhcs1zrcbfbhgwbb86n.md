---
type: is
id: is-01m29bhrhcs1zrcbfbhgwbb86n
title: Make the public workbench API and its types agree
kind: chore
status: closed
priority: 3
version: 6
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-2
dependencies:
  - type: blocks
    target: is-01m2chvkkmv158bkmqg9444jn8
  - type: blocks
    target: is-01m2chr65cx0jhfd1gsmx3r31y
parent_id: is-01m299tcsrh44b8n8m1c6jpgcb
created_at: 2026-09-11T23:06:25.195Z
updated_at: 2026-09-13T07:32:54.598Z
closed_at: 2026-09-13T07:32:54.598Z
close_reason: "Implemented at f9099096: canonical finite geometry/config/source admission, exact uint32 seeds, post-step returned-snapshot validation, authoritative typed API with negative shape/key controls. 78 package Python contract/admission tests and 31 Node tests passed; whole Python/type/browser floors passed. Further consumer migration and strict legacy graduation remain open under the package roadmap."
resolution: null
duplicate_of: null
---
Phase 2, review R8: setSeed/seed are present at runtime but missing in the probe declaration. Use one authoritative type definition, remove duplicated API knowledge, and test runtime versus declared keys plus semantic parameter/result shapes. New source and assertions belong under packages/workbench. Acceptance: a deliberate missing/extra API key or incompatible parameter/result fails a normal gate; setSeed reports the effective seed under think-dq1l. Phase 3 exports typed browser/headless entry points from this contract.
