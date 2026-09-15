---
type: is
id: is-01m2he302p2h2sb20kbt4wsw4q
title: Build the compaction pass as a retained instrument, with its scatter control
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-15T02:24:42.581Z
updated_at: 2026-09-15T02:24:42.581Z
---
Build the compaction pass that exp-209 describes as a retained instrument, with its control and outputs, before anything relies on its observation.

exp-209 records an inline pass: after repair, each square walks toward the centre of the bounding box as far as it will go without overlapping, at a shrinking step; the control runs the same pass after scattering the arrangement outward by 0.15 of a side. The program, inputs and outputs were not kept, so the round supports no conclusion (#155 review R7, D31).

`think-3hb7` owned this, and was closed on 2026-09-13 as a disposition (the record marked unreproducible) without building anything, so nothing open owned the work.

Done when:
- the pass and its scatter control are committed code that reads regenerated benchmark rows or trial receipts (on #160 and above, the package benchmark's receipts), with a test that fails if the control does not shrink a scattered arrangement;
- a separately registered round, not a repair of exp-209, runs it with its outputs retained;
- the annealing plan and exp-209 name this bead instead of think-3hb7.
