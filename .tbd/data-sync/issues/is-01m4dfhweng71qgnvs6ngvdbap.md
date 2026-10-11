---
type: is
id: is-01m4dfhweng71qgnvs6ngvdbap
title: Investigate complete-checkpoint per-test wall crossings
kind: task
status: open
priority: 2
version: 10
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: null
labels: []
dependencies: []
parent_id: is-01m4cee7q2jdj5scgd5wa72y24
child_order_hints:
  - is-01m4dj5bn5abmfwtszq9a2vzae
  - is-01m4dj5c1eanf3jhea0vfk9m3j
hold: null
hold_until: null
created_at: 2026-10-08T10:04:44.884Z
updated_at: 2026-10-08T11:09:16.986Z
started_at: 2026-10-08T10:07:01.510Z
---
Full checkpoint 37756689659 at a0ca63461d33c7dc2e12f4d08c9af6008aa1ba20 has two preserved failed attempts. Attempt 1 crossed the 12-second per-test call ceiling in the overview-fragment control (12.43 seconds). Exactly one unchanged-head failed-job retry crossed different controls: census ledger 14.63 seconds and ten-shard residue 12.71 seconds. The overview failure was absent on attempt 2; no functional failure class was reported. Attempt 2 gate wall 1771.02 seconds remained within 3600 seconds; all eleven deep/portability jobs were reused passes. Automatic PR checks are separately green (31 passes, 26 intentional skips). Do not claim the complete checkpoint passed or infer a host cause from these wall readings.

Read-only triage identifies the overview cache/fixture opportunity and two concrete children: think-z8cv for invocation-local census manifest/count reuse and think-lyuh for real prepared residue-population reuse. No performance fix, profile or measured savings have been produced. Preserve object mutation, namespace, presence, size and digest controls; preserve all ten CLI/shard/partition/output assertions and the cold CLI path. A global path-only cache is unsafe. Diagnose using a preregistered bounded matched-shape comparison and existing progress/timing instrumentation when adequate external scratch capacity is available. Keep every existing assertion and timing ceiling. No further unchanged-head reruns are planned.

Unique receipts and failed-step logs for both attempts, the final automatic-check watch and read-only triage are retained outside scratch under agent-evidence/polynomial-catalogue-01a118e4/validation. This timing follow-up remains open; the selected mathematical continuation is think-s6np, followed by think-ohhz.

## Notes

Read-only source triage confirms no renderer/input-data work changed from a910a0e6 to a0ca6346. The changed case-popover script is outside this fragment path. test_site_head.py:508 calls render_overview.result_fragments()[0]; render_overview.py:1202 reloads the overview and eagerly renders every result despite the test inspecting only the first. It bypasses the documented shared render cache/module-fixture pattern in tests/site_renders.py:120. Reuse of the existing fixture is a plausible bounded improvement with original head assertions retained; not implemented in this slice and no source-level cause is established from one crossing. Earlier7.88s CPU lower bound and current12.43s call wall are not comparable measurements. Exactlyone failed-job rerun is attempt2 of37756689659 on identicala0ca6346; validator began2026-10-08T10:11:10Z. Preserve both attempts; this bead remains open for the source/cache improvement even if retry passes. No further local heavy tests because external free capacity was109MiB.

Delivery update, 2026-10-08:

Attempt 2 also failed on per-test wall limits: the census-ledger control took 14.63 seconds and the ten-shard residue control 12.71 seconds, each against 12 seconds. The earlier overview-fragment failure was absent; no functional failure class was reported. Gate wall was 1771.02 seconds within 3600 seconds and attempt running elapsed was 1903 seconds. Final run counts are eleven reused passes, two failures (main gate and dependent aggregate), and ten intentional skips. Both attempts are preserved; no further unchanged-head reruns were performed. Full-checkpoint timing remains unresolved under think-kyzi.. Exactly one failed-job retry ran on unchanged a0ca63461d33c7dc2e12f4d08c9af6008aa1ba20 and reused eleven passing deep/portability jobs. Attempt 1 and attempt 2 receipts remain separate, including the original 12.43-second call crossing a 12-second ceiling. This bead remains open for a bounded cache/fixture improvement; no fix was implemented and no precise timing cause is established. Preserve a check of the production result_fragments API and its no-head contract when reusing cached data; changing the control to a different rendering API would need explicit coverage justification. Future work should compare unchanged assertions and limits under the same source/runner shape, using the existing progress/timing instrumentation and adequate external storage. Selected mathematical continuation is still think-s6np.


Read-only performance triage after attempt 2 found two concrete repetition paths, unmeasured. certificate_data calls hosted_data.require for 200 object records; require reparses/revalidates the manifest after load_ledger already loaded it, for 201 parses per successful census. The 58 ledger entries are all admitted, and empty selector receipts trigger three identical admitted-mask count projections. Investigate invocation-local validated-manifest and count reuse under think-z8cv, preserving object presence/size/digest checks and mutation controls; a global path-only cache would be unsafe. The ten-shard test calls main ten times, rebuilding the same 346,104-state population before choosing each shard. Investigate a real shared prepared-population fixture under think-lyuh, retaining all ten CLI/shard/partition/output assertions and the separate cold CLI control. Both source paths and committed inputs are unchanged from a910a0e6 to a0ca6346. No patch, profile, benchmark or host-cause finding was produced. Adequate external capacity and a preregistered matched-shape comparison are required before heavy follow-up. The earlier overview-fragment cache opportunity remains under think-kyzi.
