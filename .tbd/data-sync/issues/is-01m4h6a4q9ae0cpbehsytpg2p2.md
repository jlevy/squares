---
type: is
id: is-01m4h6a4q9ae0cpbehsytpg2p2
title: Make local validation failures prompt and bounded
kind: bug
status: closed
priority: 2
version: 6
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h0qnqn4f6w8p5q5sr1n9ba
hold: null
hold_until: null
created_at: 2026-10-09T20:40:11.747Z
updated_at: 2026-10-09T20:56:05.243Z
started_at: 2026-10-09T20:41:20.804Z
closed_at: 2026-10-09T20:56:05.241Z
close_reason: "PR475 final validation compatibility correction published as 27d5d24b92f6d493cfe49f46d2f979fca23c3fc9; summary https://github.com/jlevy/squares/pull/475#issuecomment-6088884586. Removed only the unconditional validation-started stderr message, preserving the 30-second heartbeat, prompt failure diagnostics, ordered final output and cleanup. Read-only review found the one-line fix sound. Frontier stderr contract, both live-progress scheduling modes and exclusive interrupt cleanup passed: 4 passed in 9.70s, Python 3.14, fresh external basetemp/cache, 120-second outer ceiling. Original guard published in 1ace022ddf5fa25b9c307e864bc228300b6e88ea with 26 focused tests and zero targeted type/lint findings."
resolution: null
duplicate_of: null
---
PR475 prevention: reject global PYTEST_ADDOPTS cache_dir overrides before running gates; skip the exclusive reachable push phase after failed edit prerequisites; show periodic stderr progress and prompt failures while preserving final stdout and process cleanup.

## Notes

Reopened: Final PR475 validation compatibility correction: preserve quiet stderr for short successful validation by removing the unconditional startup message; retain the 30-second heartbeat and prompt failures. Reopened pending bounded regression evidence and publication.
