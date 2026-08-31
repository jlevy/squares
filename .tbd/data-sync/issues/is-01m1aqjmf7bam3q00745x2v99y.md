---
type: is
id: is-01m1aqjmf7bam3q00745x2v99y
title: "W7: square-subsystem selector to make the interval route generic"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-08-31T01:40:09.318Z
updated_at: 2026-08-31T01:40:09.318Z
---
The generic promotion chain stops at refine/krawczyk raising not-square: assembly yields 122 equations against 88 unknowns at n=29 and nothing selects an independent square subsystem (close() only adds rows; grep of src/sqpack/promote finds no selector). The rank computation already does the SVD and exact_lp.independent_rows does the analogous LP job. A selector plus driver would turn packing-witness promote --strategy interval-existence from checker-not-built into a working generic certifier. From session-049's machinery inventory (X-009); only matters for poses precise enough for extraction to decide.
