---
type: is
id: is-01m0nbcspqfcf3tta2r5ppx3ww
title: "Filed flowmark issue #70: inline $...$ math split and escaped on rewrap"
kind: bug
status: closed
priority: 2
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0na001wtn9wb0fkwndgwwrq
created_at: 2026-08-22T18:23:12.087Z
updated_at: 2026-08-22T18:23:12.516Z
closed_at: 2026-08-22T18:23:12.516Z
close_reason: "Built a minimal reproduction, confirmed it on both implementations, verified it is idempotent, checked all 20 existing issues, read #62 in full and confirmed this is not covered but rather contradicts its 'already robustly safe' claim for inline math. Filed as jlevy/flowmark#70 with repro, scope, real-world impact measurements and a suggested fix."
---
flowmark breaks lines inside inline math spans and escapes the leading character of the continuation, corrupting LaTeX. Affects both the Python 0.7.0 and Rust 0.3.2 implementations identically. Contradicts issue #62's claim that the interior of inline math is already safe.
