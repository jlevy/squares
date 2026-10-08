---
type: is
id: is-01m4cb69m9baw467t6ee5ewc92
title: "PR #427 A2 — High: the selected atlas refresh leaves chunk derivatives for the previous geometry."
kind: bug
status: in_progress
priority: 1
version: 2
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4cb68shtz5h0braprdqj1qb
hold: null
hold_until: null
created_at: 2026-10-07T23:29:16.424Z
updated_at: 2026-10-08T00:20:30.609Z
started_at: 2026-10-08T00:20:30.609Z
---
Review https://github.com/jlevy/squares/pull/427#pullrequestreview-5449633758 head83748.

**A2 — High: the selected atlas refresh leaves chunk derivatives for the previous
geometry.** `packing/devtools/build_known_best_atlas.py:2534` updates selected witnesses
and the manifest, but the import’s retained output closure omits
`packing/atlas/known-best/chunk-components.json` and `chunk-partitions.json`. At this
head, `profile_known_best_chunks.py:604` observes n=88’s partition source kind
disagreeing with the manifest.
The same CI job records `census_known_best_chunks --check` refusing stale
`chunk-components.json` after 82.81 seconds.
The manifest advertises these chunk annotations while their inputs have changed.

**Fix:** run the owning chunk census and profile producers, refresh their downstream
taxonomy/contact/score outputs as required by the dependency graph, and retain those
generated results. Run their checks and the full affected gate.
Recheck the private-worker byte cap after adding the missing output changes.
