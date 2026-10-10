---
type: is
id: is-01m4kwcp3tcpddyxpxsn1wfbvb
title: Animate shared Atlas expansion height smoothly
kind: bug
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T21:44:32.629Z
updated_at: 2026-10-10T21:48:31.074Z
started_at: 2026-10-10T21:44:45.675Z
---
Animate the overall Atlas expansion and collapse using shared transition tokens on homepage and Atlas, preserving preloaded persistent tiles and immediate reduced-motion behavior.

## Notes

Implemented shared viewport height reveal using existing 360 ms Atlas duration/easing. Existing tile FLIP retained; follower transforms skipped during height animation to avoid double movement. WAAPI cleanup leaves no inline height. Six live geometry reads passed: homepage and Atlas at1280/390 have intermediate height frames; rapid mobile expand-collapse returns to727.5px with no animations; reduced-motion commits immediately. Biome, overview/probes tsc, Ruff, and25Node tests passed. Preview updated source=published=HTTP200; PDFs untouched. Review and publication pending.
