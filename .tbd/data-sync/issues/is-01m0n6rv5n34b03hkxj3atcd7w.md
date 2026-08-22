---
type: is
id: is-01m0n6rv5n34b03hkxj3atcd7w
title: Extract exact coordinates and contact graph of Trump's packing
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
assignee: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
created_at: 2026-08-22T17:02:23.925Z
updated_at: 2026-08-22T17:07:42.711Z
closed_at: 2026-08-22T17:07:22.721Z
close_reason: "Extracted the full construction from the catalogue SVG: 6 axis-aligned + 5 tilted squares, tilt angle a with sec(a) a degree-8 root, both contact equations, the closed form s = 2 + (2+sin a)/(cos a + sin a), and all five derived constants. Re-verified at 40-digit precision; residuals below 1e-32."
---
Pull per-square coordinates and rotation angles from the Kingbird SVG source. Reconstruct the contact graph, verify rigidity by counting degrees of freedom against contact constraints, and confirm the contact equations eliminate to the known degree-8 polynomial.
