---
type: is
id: is-01m0wtzvzf88stpgg69rt5mmqa
title: Document the minimum uv version needed for the pinned Python 3.14.7
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m0wtz4vb81vyh3665rt33xh2
created_at: 2026-08-25T16:10:26.671Z
updated_at: 2026-08-25T19:11:22.392Z
closed_at: 2026-08-25T19:11:22.391Z
close_reason: "Fixed in b450072: development.md names uv 0.12 as the tested bootstrap floor and records the uv 0.8.17 CPython 3.14.7 failure signature."
resolution: null
duplicate_of: null
---
development.md pins Python 3.14.7 via .python-version, but an agent container with uv 0.8.17 cannot install it ('No download found for cpython-3.14.7-linux-x86_64-gnu'); uv 0.12.x succeeds. CI pins setup-uv v9 so only local/remote agent sessions hit this. Add one line to development.md stating the minimum uv version (and the failure signature) so bootstrap failures are self-diagnosing; relates to the agent-session-bootstrap guideline.
