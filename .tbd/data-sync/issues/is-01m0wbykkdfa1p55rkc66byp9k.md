---
type: is
id: is-01m0wbykkdfa1p55rkc66byp9k
title: Preserve interruption semantics for unbounded validation calls
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0vpakbh6fy8p18cxsmtydgd
created_at: 2026-08-25T11:47:36.678Z
updated_at: 2026-08-25T11:57:20.887Z
closed_at: 2026-08-25T11:57:20.886Z
close_reason: "Completed before commit: unbounded validation calls keep the original subprocess.run path and process-group interruption behavior; isolation occurs only for an explicit finite timeout."
resolution: null
duplicate_of: null
---
The first uncommitted timeout primitive started a new session for every validation subprocess even when no deadline was supplied. Existing worker-thread checks would stop receiving the main process group interrupt while the executor still waited for them. Preserve the original unbounded subprocess path; isolate only calls that actually request a bounded tree timeout.
