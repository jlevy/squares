---
type: is
id: is-01m4h6a4q9ae0cpbehsytpg2p2
title: Make local validation failures prompt and bounded
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h0qnqn4f6w8p5q5sr1n9ba
hold: null
hold_until: null
created_at: 2026-10-09T20:40:11.747Z
updated_at: 2026-10-09T20:49:06.359Z
started_at: 2026-10-09T20:41:20.804Z
closed_at: 2026-10-09T20:49:06.354Z
close_reason: "Published in PR475 commit 1ace022ddf5fa25b9c307e864bc228300b6e88ea; summary https://github.com/jlevy/squares/pull/475#issuecomment-6088884586. Guard rejects incompatible PYTEST_ADDOPTS cache_dir before selection, reports bounded live stderr progress and failures, skips exclusive pytest after failed edit prerequisites, and isolates nested probe temp directories. Focused validation CLI regressions: 26 passed, 183 deselected in 17.32s under a 120-second outer ceiling. Targeted BasedPyright: 0 errors, warnings or notes; Ruff check/format and git diff --check passed."
resolution: null
duplicate_of: null
---
PR475 prevention: reject global PYTEST_ADDOPTS cache_dir overrides before running gates; skip the exclusive reachable push phase after failed edit prerequisites; show periodic stderr progress and prompt failures while preserving final stdout and process cleanup.
