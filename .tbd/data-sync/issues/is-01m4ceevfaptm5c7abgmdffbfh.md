---
type: is
id: is-01m4ceevfaptm5c7abgmdffbfh
title: Collect all available exact Kingbird side facts for the continuation
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex-polynomial-01a118e4
labels: []
dependencies: []
parent_id: is-01m4cee7q2jdj5scgd5wa72y24
hold: null
hold_until: null
created_at: 2026-10-08T00:26:22.569Z
updated_at: 2026-10-08T02:21:27.748Z
started_at: 2026-10-08T00:26:33.808Z
closed_at: 2026-10-08T02:21:27.747Z
close_reason: "Completed in source-data commit6862568c6 and PR435: pinned n55/n71/n83/n126 facts, complete degree672 n83 coefficients, 201 located historical occurrences with zero unparsed rows; 43 source/extractor tests and independent Astra source checks pass. Raw SVGs remain outside retained source per acquisition policy."
resolution: null
duplicate_of: null
---
W1 bounded collection: fetch n55/n71/n83 using devtools.extract_kingbird_svg_exact, retain derived facts and acquisition evidence only, determine every available current and superseded polynomial. Own extractor fixes and its tests plus a new facts packet. Do not mutate shared frontier records. Feeds think-nymu, think-xy91 and think-krbs; coordinator integrates. Use external scratch. Verify source pins and exact checks, report failures honestly.
