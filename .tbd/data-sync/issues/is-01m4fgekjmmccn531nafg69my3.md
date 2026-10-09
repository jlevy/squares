---
type: is
id: is-01m4fgekjmmccn531nafg69my3
title: Right align complete Triangle web rows with more vertical space
kind: feature
status: in_progress
priority: 1
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T04:58:54.929Z
updated_at: 2026-10-09T06:22:12.701Z
started_at: 2026-10-09T05:02:34.604Z
---
Latest user revision applies to website too: right align each complete logical Triangle row, remove intentional row splits, preserve readable same-sized drawings and halfdrawing grid gap with grid markers, leftalign information at upperleft where applicable, increase uniform vertical spacing. Keep MediumTriangle default and Grid option; complete narrow rows use existing scrolling rather than very small drawings. Web agent owns renderer CSS/probes/tests; coordinator verifies preview and publishes PR.

## Notes

Medium Triangle is the default with Grid retained. Eighteen complete right-aligned rows keep natural-sized drawings and the half-drawing grid gap inside the local horizontal scroll frame; controls and legend are left aligned and row spacing increased uniformly. Source is 87b546 and current assets are 002a8911. Node 22/22, frame 20/20, frontier 19/19, and integrated preview passed. The full gate caught two pan calls that the static embedded-JavaScript scanner could not recognize through atlas.LAYOUT. A test-only local probe loader fixes those calls without changing bytes, scanner rules, production, placement assertions, or exports; negative control 1 passed, scanner zero sites in 2,032 files, Ruff/format/BasedPyright green. Senior review and root commit precede the complete required pre-push rerun. Drive remounted and verified writable. Publication and hosted checks remain pending.
