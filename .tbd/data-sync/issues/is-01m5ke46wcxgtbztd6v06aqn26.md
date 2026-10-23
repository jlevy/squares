---
type: is
id: is-01m5ke46wcxgtbztd6v06aqn26
title: Apply common document guidelines and modern paper presentation to both tutorials
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: site-followups-ui
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T03:50:56.651Z
updated_at: 2026-10-23T04:17:29.919Z
started_at: 2026-10-23T03:51:03.045Z
closed_at: 2026-10-23T04:17:29.918Z
close_reason: "Implemented in ab238b2f73e60dbe331b2c22e94165e8083de41b, https://github.com/jlevy/squares/pull/743. Applied common-doc, prose cleanup and Flowmark to TUTORIAL.md and TUTORIAL-ADVANCED.md: consistent subsection Title Case, five semantic figure/caption associations, shared paper caption typography/spacing and 24rem packing stage. The two wide atlas canvases reuse the existing paper crop_to_container renderer; source SVGs remain intact. Preserved exactly 114 anchors and 642 source math spans. Entire focused tutorial module passed 2 tests; actual container/viewBox centers, all five loaded diagrams and sans captions checked at 1280/390px. Coordinator visually confirmed the cropped first figure and captions. Official module cost admission refreshed by CI worker: 8.890s. Implementation complete; hosted CI, final review and deployment are not claimed."
resolution: null
duplicate_of: null
---
Rigorously review both tutorials against common-doc-guidelines and modern explanatory paper design: consistent heading roles and Title Case, centered diagrams, sans-serif captions, reading measure, spacing, accessible figure associations, desktop/mobile and print where applicable. Fix source templates/shared rules, preserve mathematical meaning and existing anchors. Compare actual modern paper styles rather than inventing tutorial exceptions; user explicitly requests subagent implementation.
