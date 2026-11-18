---
type: is
id: is-01m5pdb4p3a5q65jka3hb9y04v
title: "Record #763's deletion bound at 683 (684's certificate less one square) once think-kzme decides whether an issue-claimed deletion bound gets a row"
kind: task
status: closed
priority: 3
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T07:34:58.499Z
updated_at: 2026-11-18T01:52:07.022Z
closed_at: 2026-11-18T01:52:07.022Z
close_reason: "Settled by the owner's answer of 17 November 2026 (think-gmoj): 683 gets no row, so there is no row to record; #763's n683 is settled in #1016 (merged 2980557a2). check_bead_tree --before-close: ok (w4r-records-1118)."
resolution: null
duplicate_of: null
---
Couzo's #763 claims 683 as a deletion from its own 684 certificate (certified_bounds.json at 964ee2b: kind certificate, deleted_squares 1, certificates/best/n684.cert). The #763 walk records it (below every report at 683) and holds it back from a row (beyond_horizon_replay.WALKS[ISSUE_763].held, CONSEQUENCE, think-kzme): D6 makes a deletion bound an earlier report, and whether an issue that claims one gives it a row is think-kzme's question. When think-kzme answers: write the row (decided from the retained 684 certificate's first 683 poses), or record why none. Created by c-import-763-1024 (PR A, think-ptkk).

## Notes

2026-11-17T23:40Z w4-records-1117r (think-8gvd, applying think-gmoj): the answer is 'record why none': #763's 683 has no row by the owner's answer of 17 November 2026 (no certificate file of its own); recorded in w4's records PR (walks, sources, result-requests n683). Close after that PR merges.
