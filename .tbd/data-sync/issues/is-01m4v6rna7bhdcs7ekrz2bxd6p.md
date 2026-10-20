---
type: is
id: is-01m4v6rna7bhdcs7ekrz2bxd6p
title: generate_frontier_case --refresh drops a record's generated regularization note
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-13T18:00:31.814Z
updated_at: 2026-10-13T18:00:31.814Z
---
Follow-up from Review A (round 1) on jlevy/squares#585, finding A8. Related to think-inss (the stale promotion/intake path of the same command), which does not name this.

packing/devtools/generate_frontier_case.py: `refresh_records` redrafts an existing case record and carries over only its `packing.rigidity` block (`with_rigidity_of`). The `packing.regularization` field that `devtools.regularized_drawings` writes (133 of 324 records on #585: who regularized the drawing, this project's modifications to Evan Daniel's regularizer, and the result that registers a project regularization) is not in the draft, so a refresh drops it. `--check` ignores the block (`without_rigidity` strips both `LATER_BLOCKS`), so nothing in the generator notices; `regularized_drawings --check` (records tier, via check_results) reports the record as drifted afterwards.

Fix: either carry the existing `regularization` block over on refresh as `with_rigidity_of` does for `rigidity`, or have the refresh path re-run `regularized_drawings`' writer for the counts it rewrote. Add a test in packing/tests/test_generate_frontier_case.py that a refreshed record keeps its note.

Done when a refresh of a record with the field leaves `python -m devtools.regularized_drawings --check` green.
