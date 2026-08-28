---
type: is
id: is-01m13ew8pthcyc4ayvn3kjcwcb
title: Consolidate the duplicated Motion Lab snap reducer before Phase 2
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-08-28T05:53:26.745Z
updated_at: 2026-08-28T05:53:26.745Z
---
explorations/packing/src/sqpack/motion_lab/snap.py (501 lines) and assets/free-quench-model.js (385 lines) implement the same snap/translate/rotate/release logic twice, ~886 lines total. A parity test (test_browser_reducer_matches_its_python_reference_on_generated_states) now pins them together, but Phase 2 adds contact-lock and rigid-group semantics to BOTH copies, which is when the duplication starts costing real work. Options: generate the JS from the Python, move snapping server-side behind the existing loopback service, or accept the duplication and extend the parity test to cover the new constraint operations. Decide before Phase 2 (think-mn9j) starts.
