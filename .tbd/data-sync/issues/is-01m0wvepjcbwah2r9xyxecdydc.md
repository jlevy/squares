---
type: is
id: is-01m0wvepjcbwah2r9xyxecdydc
title: Pin sqsearch Rust validation and preserve bounded geometry arithmetic
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels: []
dependencies: []
parent_id: is-01m0wqx97nb22qwx8v47hrpfqk
created_at: 2026-08-25T16:18:32.651Z
updated_at: 2026-08-25T16:18:32.651Z
---
Linux CI picked up Clippy 1.98 and began rejecting unchanged support-function half-sums under the new manual_midpoint lint while macOS and earlier runs passed. Pin the Rust toolchain used by sqsearch validation and document a narrow lint exception so CI is reproducible without changing floating-point rounding in validated geometry code.
