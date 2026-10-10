---
type: is
id: is-01m4m1xqxqrhwvhbrxayp143cf
title: Refine the print atlas recent-result legend and regenerate its exports
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T23:21:14.422Z
updated_at: 2026-10-10T23:28:20.270Z
started_at: 2026-10-10T23:21:51.925Z
---
User-authorized print-only shared 100/324 atlas legend edit: move the recent-result entry after deg; exact visible text recent result (since August, 2026), with only recent result red and the date suffix black. Preserve web wording, all counts in records, research witnesses, triangular geometry and separate Row comparison/default behavior. Regenerate both canonical SVG/PDF/PNG families using maintained --update-composites from retained witnesses; inspect actual PDF/PNG legend crops and keep receipts/dated aliases coherent. Coordinate homepage hashed asset publication after canonical output freeze; no commit or push.

## Notes

Implemented and export-frozen, 2026-10-10. Only _append_summary_legend in packing/devtools/build_known_best_atlas.py changes print rendering: right column now angles, contacts, degree, recent; recent row reads exactly recent result (since August, 2026), omits its count, and splits the red recent result prefix from the black date suffix. Shared atlas_legend web order/wording/counts, research records/witnesses, canonical triangle geometry and separate Row comparison/PDF defaults are unchanged. Existing print legend/position/ink tests were migrated; no new broad matrix.

PDF skill read in full. Its mark_artifact_operation_started.mjs succeeded exactly once with operation-kind edit, expected-output-count 2 and output-format pdf before authoring. External volume mounted/writable; project Python3.14 and external task environment used. Maintained command from packing: PYTHONPATH=src:.:../packages/workbench/tools .venv/bin/python3 -m devtools.build_known_best_atlas --update-composites. It passed retained-record preflight and export postflight, drawing from retained witnesses without rebuilding them: 2 SVG, 4 PNG, 2 PDF. Identity v0.5.0-c8abd5; data2026-10-10. Dated PDF names stay square-packings-100-20261008.pdf and square-packings-324-20261008.pdf; internal dates20261010120000Z match SVG data. Existing100 high-resolution/cropped exports were refreshed coherently. Full324 PNG7497x5361, one1x raster only; no massive2x324 export.

Actual rendered PDF and canonical PNG legend crops inspected for both100/324: correct final row after deg, exact red prefix/black suffix, no overlap or clipping. Durable evidence /Users/levy/.codex/visualizations/2026/10/08/01a11dc7-6f9d-7060-be5c-4cff21839702/print-legend-rxkc contains four inspected crops, both JUnit receipts and export-receipts.json. Every PNG/PDF receipt matches its current SVG. SVG digest100=6549dd4ce5fe080ee476320f3901192591e08556ca047af682ec7d90b2b39786;324=ca1a0b238497cdb27bc22c0c1d1c7d958b8a576d92d877a759db34b5a2aa4dcc. PDF bytes100=89605,324=533965.

Focused source/shared-web/print-spacing run initially9passed/2failed in4.77s; failures were old degree-row and recent-key expectations and were migrated. Corrected two cases plus existing regenerated-export receipts/counts/triangle cases then8passed in10.52s. Scoped BasedPyright0errors/warnings/notes; scoped Ruff format/check and diff check pass. No broad gate, PDF layout/default-scale change, commit or push. Canonical output freeze released to homepage worker for hashed full-PNG publication and dated PDF aliases; header received implemented/verified status. Parent owns remaining bounded review, publication and merged-tree full checkpoint.

Process finding from coordinator: root broad session22526 was stopped with exit130 at50% after old loaded oracles failed while source/exports moved; traceback line/source versions disagreed. This is an interrupted moving-tree run, not final verification, and no failure is reclassified as a pass. Complete broad validation must run only after author freeze on the pinned merged tree; keep think-ht59/think-xio5 obligations intact.
