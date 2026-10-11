---
type: is
id: is-01m44rnqpqb3fxdr4p5npk31b2
title: "Ladders: S5's significance mark overlaps the description beside it"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m42xfwp06kzm2b390dx1cw17
hold: null
hold_until: null
created_at: 2026-10-05T00:50:58.391Z
updated_at: 2026-10-05T01:45:25.857Z
started_at: 2026-10-05T01:07:56.310Z
closed_at: 2026-10-05T01:45:25.857Z
close_reason: Merged in jlevy/squares#348
resolution: null
duplicate_of: null
---
Owner report 2026-10-05: on all-results.html#verification-ladders the words beside S5 overlap its mark. The mark is 58.8px in the page's face against a 3.6rem (57.6px) rail, 65px in the fallback face. Fix: rail 3.75rem and a minmax(rail, max-content) track so a wider face pushes the description along.
