---
type: is
id: is-01m4wtv34pphy5w434wk13b85x
title: Resolve four scheduled main test-time ceiling overruns without weakening assertions
kind: bug
status: in_progress
priority: 1
version: 18
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
child_order_hints:
  - is-01m4wzs72rh8db5f4mp5y8w4wr
  - is-01m4x4c32d5wdje51ep66pbzmm
  - is-01m4x4c3gx5fggqnt3ha5v8gpw
  - is-01m4x5q04a41ca6rsj99gpd11d
  - is-01m4x9zbx706gftwnvmxgsnd0g
  - is-01m4xatk8zfjpdxv9kq2gv4yn1
  - is-01m4xes8ehmmxzpjctygnawq8h
  - is-01m4xjdycq4m3d047sdrdcfba9
  - is-01m4xjdytsg7x53t8pg6zja54b
  - is-01m4xjdz83t1r1pk7kcw3cvsaj
  - is-01m4xk1h2skppdp58y4zr0kvph
hold: null
hold_until: null
created_at: 2026-10-14T09:10:37.460Z
updated_at: 2026-10-14T16:14:41.630Z
started_at: 2026-10-14T10:03:10.224Z
---
Optional scheduled full integration run38536321398 at f73 passes functional tests but violates12s per-test ceiling for four nodes: site_forwarders no-script redirect13.08s; results_register full-part citations T15312.17s; overview_sections no-script canonical atlas20.10s; regularized_drawings edited-block check13.44s. Main push full gate and Pages deployment passed sameSHA. Diagnose full integration contention/cold-path cost, optimize or explicitly classify measured expensive cases while preserving assertions and meaningful CI coverage; avoid broad ceiling increases.

## Notes

PR590 is merged/live. Current PR599 head 58b6a8688d87661a7ebeac6ef3e5c944f09efd01 contains main37; all33 changed paths independently reviewed through K (5520950386), no unresolved source findings. Genuine-push required-browser 38594336170 FAILED: A atlas pool-worker CALL14.45 seconds and whole339.7>335; B all functional/CALL assertions passed but whole384.2>360. C/D and ten schema controls passed, no current deadline; ordinary Packing38594344872/Pages38594345606/mergeability passed. Fixer owns atlas pool comparison (think-jxo0); root reprices complete current cohort under think-t01m without hand weights or ceiling changes. Previous failed full/enforced runs remain failed; mathematical/deferred reuse is limited to independently reviewed unchanged consumers and inputs. Intermittent900-second deadline remains unproved fixed (think-ma3y); ordinary required-browser omissions separately tracked think-zvp7. Merge still requires fresh strict proof and live25-entry About verification.
