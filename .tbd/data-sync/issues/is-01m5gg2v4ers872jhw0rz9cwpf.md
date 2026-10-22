---
type: is
id: is-01m5gg2v4ers872jhw0rz9cwpf
title: Balance main action button labels against their visible capital-letter ink
kind: bug
status: in_progress
priority: 2
version: 2
delegate: about_profiles_implementation
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-22T00:27:25.698Z
updated_at: 2026-10-22T00:28:08.084Z
started_at: 2026-10-22T00:28:08.071Z
---
The main shared site-action links and buttons have equal physical padding, but their uppercase Source Sans labels appear high inside the filled rectangle. Measure line-box and cap-ink geometry using retained browser tests, repair the shared typography rule without guessed pixel offsets, retain icon alignment and hit areas, and refresh the immutable CSS preview. No unrelated source edits or push.
