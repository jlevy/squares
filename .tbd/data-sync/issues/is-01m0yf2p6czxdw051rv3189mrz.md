---
type: is
id: is-01m0yf2p6czxdw051rv3189mrz
title: "W3: chunk taxonomy census over the imported n <= 100 record corpus"
kind: task
status: in_progress
priority: 2
version: 6
labels: []
dependencies: []
created_at: 2026-08-26T07:20:45.004Z
updated_at: 2026-08-30T10:37:10.163Z
---
Descriptive census, not a pass/fail round: for every imported record pose, report the minimal chunk decomposition (angle classes, per-class lattice skeleton, chunk sizes, wall/corner seating, tilted-chunk count j) and tabulate which chunk shapes and arrangements actually recur across n. Output is a taxonomy table plus the non-expressible residue, feeding H-044's criterion and pricing which grammar moves the enumerator needs. Freeform exploratory work belongs in W3 and may not emit a W6 verdict.

## Notes

2026-08-30 session-045: BC-024 closed. Source-stratified taxonomy over the exact-adjacency band, plus wall seating computed from witness corners (the census's lattice coordinates are relative to a component and cannot tell a corner bar from a middle one). Three populations, not one sample: exact-grid 64 records / 64 components / 0 tilted; kingbird-derived-facts 34 / 387 / 237; unitsquare-rendering (n=68,69) 2 / 137 all singletons / 58 tilted. The finding inverts the expected shape of the residue: every other-polyomino in the corpus has angle exactly 0 -- one distinct value across all 109 -- so all 295 tilted components are singletons, bars, Ls or rectangles and already expressible. Extending the grammar to reach the residue is a question about axis-aligned polyominoes. Wall seating splits the residue into two populations with nothing between: 44 whole-record grid subsets on four walls, 65 corner-seated blocks on two; none touches one, three or none. The largest part of the residue is trivial geometry -- n=7 is an integer grid with two squares missing. Seating cross-checked against n=5's exactly known contacts from X-007: [0,2,2,2,2]. No H-044 verdict emitted; the census's known_gap says an unexpressed component is not a refutation until the minimal-partition solver exists, and a test asserts the record says so. Evidence: campaign/explorations/X-008-the-residue-is-axis-aligned.md, devtools/census_chunk_taxonomy.py, campaign/series/series-000-smoke-and-calibration/results/bc-024-chunk-taxonomy.json, tests/test_chunk_taxonomy.py. Next action: none for this commitment; the residue characterization feeds the partition-instrument design.
