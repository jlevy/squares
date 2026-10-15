---
type: is
id: is-01m4zdsxez5kg9ffagfvqja44y
title: Preserve percent-encoded News archive bookmark forwarding (B2)
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zaazfxmv8px64xvdvdqnc7
hold: null
hold_until: null
created_at: 2026-10-15T09:20:30.686Z
updated_at: 2026-10-15T09:20:53.220Z
started_at: 2026-10-15T09:20:53.219Z
---
Correctness review B at895637: excluded News entries use legacy forward anchors, but news-forward.js looks up raw location.hash without percent decoding. Previously supported encoded changelog-entry fragments now fail to reach the retained CHANGELOG archive. Reuse guarded decodeURIComponent from existing card/filter scripts; malformed hashes stay harmless. Add real raw/encoded excluded-entry forwarding regression without removing current eligible-bookmark coverage. Patch delegated to existing browser-contract worker.
