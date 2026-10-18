---
type: is
id: is-01m57syyvkw6dmkteecqk9nn5n
title: "PR #665: isolate short-budget browser and segment CLI controls"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m57j9xsga57szgfah5ex2bcd
hold: null
hold_until: null
created_at: 2026-10-18T15:26:54.311Z
updated_at: 2026-10-18T15:27:03.065Z
started_at: 2026-10-18T15:27:03.064Z
---
Own only packing/tests/test_browser_diagnostic.py and packing/tests/test_segment_cover_replay.py. Clean 2890 broad gate killed nested browser pytest during collection under its 2s deadline and the one-node segment CLI before JSON under its outer 10s deadline. Quiet focused receipt timeout-focused-2890be7fa.log records both pass in 3.46s and 0.49s call time. Mark these real subprocess controls pool_heavy, preserve browser 2s, set only incomplete segment outer bound to 25s above two inner 10s Git queries plus startup, and cover forced provenance timeout failing closed. Use frozen external Python and installed Flowmark hook overrides, never common .venv; commit only owned paths. No broad gate or GitHub mutation.
