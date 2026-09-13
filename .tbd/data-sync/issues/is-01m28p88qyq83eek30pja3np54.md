---
type: is
id: is-01m28p88qyq83eek30pja3np54
title: Migrate workbench app composition, builders and tools into the package
kind: task
status: open
priority: 2
version: 9
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-3
dependencies:
  - type: blocks
    target: is-01m2ckzxqf9s88871t1zkmayse
  - type: blocks
    target: is-01m29f4zbw0vv3xj1xbe95narx
  - type: blocks
    target: is-01m2chakgrn8keadss1jcs401b
parent_id: is-01m2chahf57z4w9tj5gehbs0td
created_at: 2026-09-11T16:54:14.013Z
updated_at: 2026-09-13T05:43:48.016Z
---
Phase 3 under think-zisr: assemble the extracted kernel, data, timeline and mode controls into packages/workbench; move all workbench-specific Python/JS builders, capture and benchmark adapters, fixtures and browser probes there. Replace the old script-by-path build with package commands and update root Pages integration and all path-sensitive gates. General sqpack libraries remain dependencies. Acceptance: package build/test/typecheck/lint and capture use package sources only; self-contained artifact and deterministic receipts agree; no app code newly placed in flat devtools. Temporary compatibility wrappers require named consumers and retirement through think-cqfc. Banner removal follows accurate evidence labels, not an old Phase 6 checklist.

## Notes

Owner-selected destination is top-level packages/workbench/ (2026-09-12). Migrate all live workbench-specific sources and tools, including Python build/capture/benchmark adapters, into that package. Shared sqpack library code remains a dependency. Do not add permanent flat devtools wrappers; only consumer-backed temporary compatibility entry points, retired through think-cqfc.
