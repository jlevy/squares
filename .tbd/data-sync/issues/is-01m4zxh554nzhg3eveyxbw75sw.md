---
type: is
id: is-01m4zxh554nzhg3eveyxbw75sw
title: Measure restored main integration work and assess native fast-job fan-out
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-15T13:55:20.867Z
updated_at: 2026-10-15T13:55:48.325Z
started_at: 2026-10-15T13:55:48.324Z
---
F1 correctly removes unauthenticated fast-check reuse. In final full run38744311408 the complete integration job is the remaining critical path after the dedicated workers pass, so retain its actual cost and assess a small native same-workflow alternative: can existing fast PR jobs execute on non-PR events with an exact complementary integration selection and aggregate? No cross-run proof/API/attestation framework, duplicated checks, cap increases, source waivers or speculative speed claim. First inventory the nonfast steps still owned by validate and prove exact partition before proposing implementation. Keep this investigation separate from frozen PR620 unless a real failure requires a fix.
