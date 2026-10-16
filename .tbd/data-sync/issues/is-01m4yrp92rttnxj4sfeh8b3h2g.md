---
type: is
id: is-01m4yrp92rttnxj4sfeh8b3h2g
title: "Register cases 76 and 95 in the mixed-cover tools, then record the zmx2 + zm_mixed reproductions of T-184 and #610 as evidence"
kind: task
status: in_progress
priority: 2
version: 4
delegate: user-eb-records-76-95
labels: []
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-15T03:11:31.416Z
updated_at: 2026-10-16T06:11:36.705Z
started_at: 2026-10-16T05:25:32.902Z
---
The C3 route for T-184 (#594, s(76)=9) and #610 (s(95)=10) needs the full reproductions (zmx2 D4 sweep over 10,000 roots plus all zm_mixed.py sub-roots, already run and retained in packets bengreff-s76-certificate-* and bengreff-s95-certificate-2026-10-15 on intake-610 @ 7c65c191b) recorded as evidence entries. That first needs cases 76 and 95 registered in the two mixed-cover tools (zmx2, zm_mixed). Then a stage 4 review with no blocking defect raises the rungs. Optional: zmx2 --full (think-eucc, ~6 CPU-h), as T-066's s(59) replay ran. Found by the #610 lane on 2026-10-15.

## Notes

2026-10-16T05:40Z user-eb-records-76-95 (lane E): started on branch claude/intake-2026-10-16-records-76-95 from origin/main e2e018f32. Plan: (1) register 76/95 in replay_evand_zmx2 and audit_evand_mixed_covers with a zmx2+zm_mixed split-composite judge and tests; (2) targeted zm_mixed.py controls on mutated covers (packets lack them); (3) evidence entries, verifiers rows, coverage entries, uncited until lane F's review; (4) draft PR. No rung change before lane F's verdict.

2026-10-16T06:12Z lane E checkpoint: tool slice committed and pushed at 5575ad2bf (claude/intake-2026-10-16-records-76-95): replay_evand_zmx2 cases 76/95 (+ source --uncert-cap for run) and their retained controls; audit_evand_mixed_covers split cases, composite judge, compare-sub-roots, check covers both packets (clean: 8096+64 sub-roots for 76, 9981+304 for 95; replay equals source root for root). Tests in test_audit_evand_mixed_covers, test_replay_controls (+ zm_mixed.py pose receipts held), test_replay_tools. Priced zm_mixed.py cert refusals of the two retained mutations: not affordable (depth 24 > 5 CPU-min and depth 12 > 10 CPU-min on one cell, both stopped); ~15 CPU-min spent. Next: evidence entries, verifiers rows, coverage entries (uncited until lane F).
