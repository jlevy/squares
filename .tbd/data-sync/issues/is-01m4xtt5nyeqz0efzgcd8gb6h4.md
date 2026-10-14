---
type: is
id: is-01m4xtt5nyeqz0efzgcd8gb6h4
title: "News604 hosted browser assertions: article headings and settled width-cap control"
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4xm9zrn7p4nygg25gwy9cxw
hold: null
hold_until: null
created_at: 2026-10-14T18:29:21.714Z
updated_at: 2026-10-14T18:29:36.775Z
started_at: 2026-10-14T18:29:36.774Z
---
Current-head Packing38614518600 frontend116026059173 has3failures: global homepage H3/H4/H5/H6 count expects2 though3Newsarticle headings nowexpected; atlas.html scripted negativecontrol reads same-frame computed maxWidth3120 after140rem injected, affected by KPress0.01ms reduced-motion allproperty transition. Preserve all actual width/gutter/panning assertions and >500px negativegap. Update outside-News heading contract and separately assert3Newsarticles, make injected cap deterministic, retain targeted realChromium proof. 419othercasespassed6skipped. Batch with independent review findings before nextpush.
