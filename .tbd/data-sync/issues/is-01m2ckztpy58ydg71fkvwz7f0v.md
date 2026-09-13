---
type: is
id: is-01m2ckztpy58ydg71fkvwz7f0v
title: Establish the workbench package shell and immediate source-gate coverage
kind: task
status: in_progress
priority: 1
version: 12
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-phase-0
  - workbench-roadmap
dependencies:
  - type: blocks
    target: is-01m2chae7ahgc8nf7vb33wkhj7
  - type: blocks
    target: is-01m2chag118qjnczfj2zbrtx3b
  - type: blocks
    target: is-01m2chknz8861931tannzahgvh
  - type: blocks
    target: is-01m2chkpvbrqv1h9nttp8rrtqb
  - type: blocks
    target: is-01m292rgtadddppyrzfkjz1sn4
  - type: blocks
    target: is-01m2cj9hf5v77se0yyzbr5jqd6
  - type: blocks
    target: is-01m2ckzvnsawqg79z9ybspc3yt
  - type: blocks
    target: is-01m2chkrt876774phbaj1pa836
  - type: blocks
    target: is-01m2cmf6vy26q99h0pa25g518w
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T05:31:38.075Z
updated_at: 2026-09-13T06:00:01.138Z
---
Create top-level packages/workbench as the only destination for new workbench source during repair phases. Add locked package scripts and strict compiler/lint bases, package-local tests/probes/tools ownership, and extend repository layout docs, Python discovery, browser configuration, hooks and PR selection to the root package. Flowmark remains sole Markdown formatter. This is a small shell, not bulk extraction. Acceptance: real minimal TS/JS/Python fixtures are discovered by their applicable existing gates; deliberate excluded-source and relaxed-config controls fail; no broad suppressions or new spike/devtools application modules.
