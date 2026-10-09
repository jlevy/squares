---
type: is
id: is-01m4h1cx9na53vx9yjzmddwyqm
title: "OR-1: commit a Rust/Python kernel receipt parity comparator"
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@spud10.local
labels:
  - n-17
dependencies: []
parent_id: is-01m4gve5z0rn7s43dyr04hgj28
hold: null
hold_until: null
created_at: 2026-10-09T19:14:19.573Z
updated_at: 2026-10-09T23:27:42.031Z
started_at: 2026-10-09T23:27:42.029Z
---
No committed tool compares Rust n17_kernel_verify receipts with the Python standing verifier's (validate.py's native gate only runs fmt/clippy/cargo tests). The #472 admission used an ad hoc compare.py (scratchpad rust-tools) applying H-335's rule: all fields equal except provenance, directory, seconds. Commit it as a devtools tool with tests and cite it from exp-317 / H-335.
