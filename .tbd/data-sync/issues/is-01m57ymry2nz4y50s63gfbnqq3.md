---
type: is
id: is-01m57ymry2nz4y50s63gfbnqq3
title: Use actual dependent PR base for release-impact validation
kind: bug
status: in_progress
priority: 2
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m578snhcmb9xf25bnb3atvy8
hold: null
hold_until: null
created_at: 2026-10-18T16:48:43.444Z
updated_at: 2026-10-18T17:06:57.940Z
started_at: 2026-10-18T16:48:51.049Z
---
On #676 rebased onto #661 a87de0cf7, clean2627322e1 records passes51/52 in110.18s but synopsis release impact compares main sitev0.7.25 to currentv0.7.27 and rejects correct adjacent25→26→27 history. Preserve adjacent edition validation and changelog main baseline. Select actual PR base from GITHUB_BASE_REF in hosted CI, explicit PACKING_RELEASE_BASE_REF locally, otherwise origin/main; preserve HEAD==main HEAD^1 path. Remove only redundant intake-layer n11 exemption because generated docs equal parent. Add focused own-layer pass and uncovered-input negative control plus ordinary-main selection controls before fresh records; no Stage3 registry writes before pass.

## Notes

2026-10-18 local #661 rebase complete at2627322e1 onto pinned a87de0cf7, with backup ref codex/intake-stage2-checkpoint-2a7a11ea6. All four packets and prior fixture repairs preserved. Re-rendered five n11 claim documents equal parent bytes; URL registry1015/0 and data pinbc6ed02e correct. Fresh records51/52 in110.18s exposed stack-baseline handling, not a result/schema failure. Scoped bug think-e05x repaired release-impact parent selection: GitHub PR base in CI, explicit local PACKING_RELEASE_BASE_REF, main default and HEAD^1 delivery path preserved; changelog stays main. Removed redundant old claim-document exemption and scoped its replacement to validation CLI code only, with source-reviewed no-paper-content-change rationale. Red selector3fail/2pass; full focused release module24pass112.80s; Ruff and BasedPyright0/0; focused synopsis1/1pass36.17s. Six-file commit5458a50d57b81846ce6d19a7b4af08b5680f34ac, normal isolated hooks6.10s. Fresh exact-head prereg records52/52PASS138.07s/300 (139.20s real), CPU6/jobs2/inner1, pinned-parent ancestor proof, isolated external TMPDIR; concurrent read-only fdu scanner disclosed. Logs records-5458a50d5-prereg-n5.* and release-base-*. Broad push remains held for storage audit. Parent authorized Stage3 on four grouped entries/six claim rows, V0/C0, after #661T195; source replay/math review stay separate descendants. No remote push/PR edit/issue comment/merge. Remote676 remains5fb743b3e; parent will formal-link to661 before qualified force-with-lease push.
