---
type: is
id: is-01m22knv1pys6mdfahpg6j0tq8
title: "X-024 slice A4: the exact plateau reader for threshold duals"
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-09T08:13:46.418Z
updated_at: 2026-09-09T10:18:48.129Z
closed_at: 2026-09-09T10:18:48.128Z
close_reason: "The plateau reader is promoted as packing/devtools/plateau_reader.py with eighteen tests, and its controls on the 88-core ceiling family at 191/50 reproduce: two-of-three 5/4 at memberships (4, 8, 8), the eleven-entry corner clique at 11/8 with tau* = 5/3, the wall lines tight at exactly 3, and floor atoms at 5/8 and 1/2. The run is retained as results/agenda-033/plateau-reader-191-50.json and reported in lane-t2-plateau-reader.md."
resolution: null
duplicate_of: null
---
Lane T2's first instrument in both outcomes: on a symmetrised plateau dual, verify_ceiling depth, the exact maximum two-of-three charge over all point triples (vertex membership sets), maximal cliques above weight one with exact piercing LPs (tau* < 2), wall and diagonal line chords, and the Chvatal-Gomory separation program through HiGHS with exact re-verification; output a ranked list of exact violated atoms or a certificate that none exists. Prototype scripts: scratch theory-2/twothree_exact.py and marks_and_lines.py.
