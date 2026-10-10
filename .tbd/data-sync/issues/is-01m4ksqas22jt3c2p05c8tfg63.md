---
type: is
id: is-01m4ksqas22jt3c2p05c8tfg63
title: Center visible Atlas rows and animate expansion on both pages
kind: bug
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T20:57:55.731Z
updated_at: 2026-10-10T21:36:10.713Z
started_at: 2026-10-10T20:58:07.605Z
---
Center homepage and dedicated Atlas canvases based on visible rows. Use the same shared controls, legend, overview and initial100-square preview on both pages, expanding to324 with complete Grid/Triangle row cutoffs. Prepare hidden diagrams before reveal so artwork does not arrive incrementally; preserve first-paint responsiveness, shared FLIP animation, mobile panning, case links/popovers and reduced motion. Supersedes earlier36-square homepage staging. Verify representative desktop/mobile transitions, then update PR462 and local preview.

## Notes

Shared controller implements 100→324→100 with identical tabs/legend, centered visible canvas and shared FLIP. Hidden SVG rows prepare after fonts one per frame; requested images retain high priority and decode failures preserve links. Four focused desktop/mobile nodes passed in 68.30s, two source tests passed in 9.68s, and 25 shared-engine Node tests passed. Scoped static floors and Astra review passed. Published commit 5b04d007 exposed stale test contracts, a repeated 848-element startup restyle, and a separate native 302ms task against the unchanged 300ms guard. Blink source confirmed the FontFaceSet.ready getter forced layout after placement writes; capturing its promise before mount fixes that ordering. The unchanged restyle guard and native HTTP/noJS 1280/light scenario both passed locally (2 tests, 101.69s including fixture preparation). The native CI overrun predates Atlas JavaScript and remains a retained failed receipt; no performance bound was weakened. Follow-up commit and exact-head CI pending.
