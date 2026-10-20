---
type: is
id: is-01m4mdbqsgkdz008e42ffjx4ej
title: "Atlas: adopt the register's regularizations definition for the project's own regularized layer, as a softschema contract"
kind: task
status: in_progress
priority: 1
version: 7
delegate: claude-code@vm
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m4mdbq6bhkv71fxeeckawsbt
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
child_order_hints:
  - is-01m4t5y8cd4b8kfymqjt7g3bwa
hold: null
hold_until: null
created_at: 2026-10-11T02:41:07.376Z
updated_at: 2026-10-13T09:07:15.382Z
started_at: 2026-10-12T11:32:11.446Z
---
Epic think-cdud. The project's own regularization layer (packing/atlas/known-best/regularized/index.json, contract packing.squares:RegularizedAtlasIndex/v1 with no softschema block; devtools/regularize_axis_components.py, algorithm regularize_axis_components/2; the view witnesses' open certificate.regularization and derived_from blocks) records provenance that no schema validates and no person or credit. Give index.json (and the view witnesses' regularization block) a softschema contract whose per-view provenance uses the same terms as the register's regularizations field (of/derived_from, by = project, method, side, changes, identity), and hold it in validate_schemas. Fold into the stacked regularization PR if that PR replaces the layer.

## Notes

2026-10-11, owner (session_017JNnKDwL74rnktr9s8BdjP): "as we're making all these changes, we'll want to track that these are regularizations that we have done. We track the provenance of the best packings within our schema." Raised to P1 and made a blocker of the full run (think-ux1v). Done on #511: devtools.regularize_evand now writes, per count, report.regularization in the register's regularizations-item terms (by: project, method naming Evan Daniel's search/regularize with the pin, variant and placement, side, changes {straightened, re_angled, merged_rotation_groups_deg}, identity {basis: measured, measured_in, one_to_one, moved, max_move, max_turn_deg}) plus of_witness and provenance (the case record's source_key, found_by, improved_by, which a regularization never changes); a test validates it against results.schema.yaml's item once `of` is resolved; reclassify backfills it. Remaining here: the softschema contract for index.json and the view witnesses' certificate.regularization block in the same terms, and admission writing the record into each index entry (and into a register result's regularizations where the side is below U).

2026-10-12 (overnight): implemented on jlevy/squares#548 — RegularizedAtlasIndex/v2 with its softschema schema, every entry naming its generator (axis tool, evand-regularize with pin/patches/variant, regularize_grid_slack /0 and /1) and carrying its regularization in the register's terms with identity measured; --check-atlas and --verify-atlas cover every generator; the register's generated regularized_drawings block (82 items at #549) checked by check_results. Closes when #548 merges.
