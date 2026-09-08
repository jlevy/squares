---
type: is
id: is-01m1yx7vnjtzna6de63m6h02vf
title: Reconcile H125 synopsis views and rerun the checkpoint outside process-inspection sandbox
kind: bug
status: closed
priority: 1
version: 4
spec_path: packing/campaign/agendas/agenda-027-compatibility-and-restricted-families.md
labels: []
dependencies: []
parent_id: is-01m1ytzagmmx58w96ksbf5j3dj
created_at: 2026-09-07T21:43:56.337Z
updated_at: 2026-09-07T21:55:41.793Z
closed_at: 2026-09-07T21:55:41.792Z
close_reason: Corrected immutable c3a4e8ec:45of66 applicable push steps passed200.88s gate/203.99s external. Synopsis reconciliation complete; process-inspection permission and immutable .venv dependency link fixed environment only. Failed earlier receipts retained, no tests weakened.
resolution: null
duplicate_of: null
---
Immutable4649e23a first push check failed75.13s: H125 missing from synopsis hypothesis table and blocked count stale; two unchanged validation process-cleanup tests could not execute ps under sandbox. 679passed3failed4deselected62.15s. Fix native rendered/manual synopsis surfaces and record actual failed receipt. Rerun same bounded immutable push with required process-inspection permission; do not weaken tests or claim this is a mathematical/source defect.

## Notes

Second immutable push atc3a4e8ec:74.34s,681passed1failed4deselected61.08s; process-inspection failures resolved. The remaining unchanged negative-control test is an environment defect: private snapshot uv uses UV_NO_SYNC=1 and links the validation checkout .venv, but that frozen checkout had no .venv, causing ModuleNotFoundError yaml. A fresh isolated diagnostic confirms it; no scientific source or test changed. Add only the missing symlink to the locked original environment, rerun the isolated test then the bounded push tier. Explicit PACKING_PROJECT_ROOT removed so cloned snapshots select themselves.
