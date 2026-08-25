---
type: is
id: is-01m0wtzvzf88stpgg69rt5mmqa
title: Document the minimum uv version needed for the pinned Python 3.14.7
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m0wtz4vb81vyh3665rt33xh2
created_at: 2026-08-25T16:10:26.671Z
updated_at: 2026-08-25T16:10:26.671Z
---
development.md pins Python 3.14.7 via .python-version, but an agent container with uv 0.8.17 cannot install it ('No download found for cpython-3.14.7-linux-x86_64-gnu'); uv 0.12.x succeeds. CI pins setup-uv v9 so only local/remote agent sessions hit this. Add one line to development.md stating the minimum uv version (and the failure signature) so bootstrap failures are self-diagnosing; relates to the agent-session-bootstrap guideline.
