---
type: is
id: is-01m2dvhp7pymsbvgpfjkphq0jd
title: Search trials yield to cancellation and a completed trial is never reported timed out
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m2ckzy45b1b28pvt1nbh4gdm
created_at: 2026-09-13T17:02:57.780Z
updated_at: 2026-09-13T17:02:57.780Z
---
Review of the uncommitted Search layer (2026-09-13). The pack runner (src/search/pack-runner.ts runPack) is synchronous and never yields, so an AbortSignal cannot stop a running trial and concurrency above 1 only interleaves whole trials; only the clock deadline interrupts. The scheduler checks the deadline after the runner returns (scheduler.ts ~172-174), so a trial that completed its full fixed work but crossed the deadline is reported timed-out and never ranked. Acceptance: bounded work chunks that yield between chunks, cancellation observed within one chunk, a completed trial keeps its completed status regardless of wall clock, tests for both.
