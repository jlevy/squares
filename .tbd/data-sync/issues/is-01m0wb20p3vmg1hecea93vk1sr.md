---
type: is
id: is-01m0wb20p3vmg1hecea93vk1sr
title: Use directory-relative paths with uv directory commands
kind: bug
status: closed
priority: 3
version: 2
spec_path: explorations/packing/campaign/agent-sessions/session-011-eight-hour-continuation.md
labels:
  - packing
  - focus-process
dependencies: []
parent_id: is-01m0w9a47h5zrn7jf16pp2kpxs
created_at: 2026-08-25T11:31:59.798Z
updated_at: 2026-08-25T11:33:51.246Z
closed_at: 2026-08-25T11:33:51.246Z
close_reason: The focused Ruff and BasedPyright commands were rerun with paths relative to uv directory; formatting, lint, and static analysis all pass. D-288 retains the first command error.
resolution: null
duplicate_of: null
---
The first focused Ruff command combined uv run --directory explorations/packing with a path still prefixed by explorations/packing, so Ruff looked for a doubled nonexistent path and stopped before formatting. Rerun with cases/trump11/incidence_cores.py relative to the selected directory, record D-288, and keep the corrected command in the phase receipt.
