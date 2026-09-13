---
type: is
id: is-01m2chvkkmv158bkmqg9444jn8
title: Complete the strict Python and TypeScript/JavaScript floor for retained workbench code
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
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T04:54:22.572Z
updated_at: 2026-09-13T05:43:46.744Z
---
Owner explicitly requires tbd best-practice floor across all new code and retained live spike code. Integrate parent Python coverage first. Python: pinned3.14, Ruff formatting/lint and BasedPyright with zero warnings/errors, precise public types and no blanket exclusions. TS/JS: zero-warning Biome, separate tsc noEmit with full tsconfig.base flags, checkedJS allowJs/checkJs as needed; new/package sources may not inherit the4 legacy relaxations. Retire relaxed flags on promoted workbench sources and keep untouched legacy exceptions explicit and shrinking. Existing think-4cwy is CLOSED and its xxxx followups are not a completion plan. Add type-aware promise checking for JS per tbd overlay (or actual TS coverage), config negative controls, and import/source-extension coverage. Flowmark remains sole Markdown formatter and existing nonblocking Markdown CI policy remains. No global suppressions or broad any to reach green.

## Notes

Owner selected top-level packages/workbench/. All package Python tools, TypeScript/JavaScript modules, tests and probes must be explicitly discovered by existing lint/type/CI selection. Existing think-4cwy remains historical; no new module enters its four-flag relaxation. Extract embedded TRIAL_JS/GUARD_JS into checked files and close runtime/declaration setSeed/seed mismatch. Preserve an independent numerical verification path where needed.
