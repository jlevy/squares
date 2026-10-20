---
type: is
id: is-01m57syyvkw6dmkteecqk9nn5n
title: "PR #665: isolate short-budget browser and segment CLI controls"
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m57j9xsga57szgfah5ex2bcd
hold: null
hold_until: null
created_at: 2026-10-18T15:26:54.311Z
updated_at: 2026-10-18T15:43:44.344Z
started_at: 2026-10-18T15:27:03.064Z
closed_at: 2026-10-18T15:43:44.342Z
close_reason: Committed cd5cc5cff7c0365e185eba9e6226d59a10e011a7; only browser/segment test files (+27/-1), worktree clean. Root reviewed no blocker. Preserved browser whole-command 2s deadline; marked the two real subprocess controls pool_heavy; scoped incomplete CLI bound25s above two inner10s Git calls; invalid-input cap remains10s. New forced second-provenance-query timeout asserts exit2/error JSON/not proved and matching output file. Both complete modules:11 passed6.82s; exact collection all11=normal9+pool2, disjoint. Ruff/format pass; BasedPyright0 errors/warnings/notes. Isolated normal hooks2.65s using installed Flowmark and external frozen Python, no uv/shared-venv mutation. Durable module/collection/commit receipts under /Volumes/spud-ext1/agent-source/squares-665-review-20261018/ with timeout-hardening prefixes. No broad gate, push or GitHub mutation. Slot released to coordinator/676.
resolution: null
duplicate_of: null
---
Own only packing/tests/test_browser_diagnostic.py and packing/tests/test_segment_cover_replay.py. Clean 2890 broad gate killed nested browser pytest during collection under its 2s deadline and the one-node segment CLI before JSON under its outer 10s deadline. Quiet focused receipt timeout-focused-2890be7fa.log records both pass in 3.46s and 0.49s call time. Mark these real subprocess controls pool_heavy, preserve browser 2s, set only incomplete segment outer bound to 25s above two inner 10s Git queries plus startup, and cover forced provenance timeout failing closed. Use frozen external Python and installed Flowmark hook overrides, never common .venv; commit only owned paths. No broad gate or GitHub mutation.
