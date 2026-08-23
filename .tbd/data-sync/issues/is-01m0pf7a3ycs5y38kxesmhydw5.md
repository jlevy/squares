---
type: is
id: is-01m0pf7a3ycs5y38kxesmhydw5
title: Bring packing Python and Rust to the project lint floor
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels:
  - defect-class:validity
dependencies: []
parent_id: is-01m0pdh5bj67ca8vk7ct53g5qt
created_at: 2026-08-23T04:49:21.021Z
updated_at: 2026-08-23T05:09:16.843Z
closed_at: 2026-08-23T05:09:16.492Z
close_reason: "pyproject.toml with ruff (broad select, reasoned exceptions) + basedpyright: ruff clean, 0 type errors. Rust: clippy pedantic + unsafe_code forbid + rustfmt, clean. Both enforced in test.sh. The floor found 5 real issues including non-strict zip in field arithmetic and a TAU literal."
---
Per python-rules, python-modern-guidelines, python-cli-patterns: uv for everything, ruff + basedpyright with a high floor, from __future__ import annotations, pathlib, modern unions, full annotations, atomic output files via strif, docstring style, inline tests under ## Tests. Rust: clippy with a high floor (pedantic), rustfmt, deny warnings. Wire both into test.sh so the floor is enforced, not aspirational.
