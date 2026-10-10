---
type: is
id: is-01m4f5h2c1vbdzh5k0amxnn5c0
title: Make the embedded SVG Atlas honor live light and dark themes
kind: bug
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels:
  - website
dependencies:
  - type: blocks
    target: is-01m4ex3gpzxxh9eqemc2r78p4e
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-09T01:48:01.280Z
updated_at: 2026-10-10T18:55:57.138Z
started_at: 2026-10-09T01:48:13.448Z
closed_at: 2026-10-10T18:55:57.138Z
close_reason: |-
  Completed the reviewed implementation and CI repair published in PR462 (https://github.com/jlevy/squares/pull/462) at exact head d3c99face8fa81fd6ad265111265e4f6a6067106. The coordinator's sole final CI watch exited 0: 31 PASS, 26 intentional SKIP, 0 failures, 0 pending; frontend PASS and all final-head checks green.

  Final behavior supersedes stale descriptions: single centered n=53 hero; homepage Triangle preview 36→100→324→36; About H1; inline homepage video; complete Atlas and Frontier Survey, shared navigation/design and case/result previews retained. The canceled scientific PDF change is excluded. No assertion, 300ms startup bound or scientific content is changed by this closeout.

  Earlier local 901-second incomplete validation and the 195c80948 startup failure remain preserved in prior notes and durable receipts; final hosted success does not relabel those runs. This closes implementation and CI-repair beads only. Full checkpoint think-xio5, epic think-2u4x, process owner think-ht59 and scoping follow-up think-9k61 remain open.
resolution: null
duplicate_of: null
---
The native homepage SVG Atlas retains a white poster background and fixed ink in dark mode. Use shared theme tokens for its background, labels and outlines while preserving packing geometry and hue semantics. Cover live light/dark/automatic theme changes in the initial two-row preview and full expanded graphic, cached collapse/re-expansion, and desktop/mobile. Keep exported poster SVG/PDF source artifacts unchanged.

## Notes

Implemented with scoped shared theme tokens for nativeSVG backgrounds, containerfills, outlines/grid, labels, evidencebadges andstars; originalpacking polygonfills unchanged. Both initialpreview andfetched/cachedgraphicuse sameCSS andbackgroundmarker. Final16homepagebrowsercasespassed inclliveSystem/light/dark atdesktop/mobile for36→324→36, contrast>=4.5 andunchangednativepalette. Local8766draftrefreshed; sourceverified, awaitingcombinedrepositoryverification/commitpublication.
