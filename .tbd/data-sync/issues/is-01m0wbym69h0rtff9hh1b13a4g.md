---
type: is
id: is-01m0wbym69h0rtff9hh1b13a4g
title: Fail closed where Windows process-tree cleanup is unproved
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0vpakbh6fy8p18cxsmtydgd
created_at: 2026-08-25T11:47:37.289Z
updated_at: 2026-08-25T11:57:21.362Z
closed_at: 2026-08-25T11:57:21.361Z
close_reason: "Completed before commit: removed the unproved taskkill fallback. Explicit bounded-tree mode fails closed on Windows pending a tested backend."
resolution: null
duplicate_of: null
---
The first uncommitted timeout primitive treated taskkill as a Windows process-tree guarantee, ignored a nonzero taskkill exit, and could fall back to killing only the direct parent before an unbounded communicate. Windows has no CI coverage here. Keep ordinary unbounded behavior portable, but fail closed for bounded tree mode until a tested Job Object or equivalent backend exists.
