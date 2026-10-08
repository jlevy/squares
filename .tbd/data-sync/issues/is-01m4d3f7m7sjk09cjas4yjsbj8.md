---
type: is
id: is-01m4d3f7m7sjk09cjas4yjsbj8
title: "PR #433 A1: mutation-worker source exceeds 192 MiB cap"
kind: bug
status: closed
priority: 1
version: 6
delegate: codex-fibonacci-merge-ready
labels: []
dependencies: []
parent_id: is-01m4d3eryja3jhzk668anzbtwd
hold: null
hold_until: null
created_at: 2026-10-08T06:33:35.110Z
updated_at: 2026-10-08T07:22:02.131Z
started_at: 2026-10-08T06:34:06.036Z
closed_at: 2026-10-08T07:22:02.130Z
close_reason: A1 fixed at 97b3c3a; complete hosted suite A and fast validation pass, and correctness B plus performance C independently verify the repair with no findings. Final PR readiness remains tracked by think-9swm.
resolution: null
duplicate_of: null
---
High finding A1 in review A https://github.com/jlevy/squares/pull/433#pullrequestreview-5452512279. At head 52adbb0e6d37e1fcdf8ed76c78e1a8775f95ccb0 suite-a run 37737159148/job 113179212924 reports 201417439 bytes against 201326592. Locations packing/devtools/run_negative_controls.py:1063 and packing/tests/test_negative_controls.py:434. Audit unconsumed snapshot inputs, retain research/Git evidence and dependency rescue, preserve cap/assertions, verify omission/rescue and hosted gate.

## Notes

A1 fixed and pushed in 97b3c3a995bac5d7d8279da9d0eef42def3ca9cb; worktree clean. Disposition: https://github.com/jlevy/squares/pull/433#issuecomment-6054206251. The historical Session 177 profile packet (358,041 bytes) and exp-063 census (440,375 bytes) remain in Git but leave disposable worker snapshots unless a checked document link or registered result dependency requires restoration. Audit found only historical prose, output references and README command examples; no current registered consumer. Exclusions remove 798,416 bytes; code/tests add 5,103. Applying that delta to the former hosted reading predicts 200,624,126 bytes, leaving 702,466 below the unchanged 192 MiB cap; this exact new count was not printed or measured on a complete local checkout.

Red test: 1 failed / 1 passed in 12.77 seconds. Repair selection: 9 passed in 15.19 seconds; Ruff check/format and BasedPyright clean under Python 3.14.7, no hook bypass. Production copier/index fixture verifies source preservation, actual omission, counter equality and byte-for-byte private indexed restoration through both rescue routes. Cap refusal remains covered.

Hosted confirmation completed: suite A at https://github.com/jlevy/squares/actions/runs/37739532201/job/113186775564 reports 2,870 passed and 23 skipped in 123.00 seconds, including all three formerly failing full-copy tests. The whole fast run passes. Current merge tree is d69fb76d72b38d60f0e260acb70221fba2d67bb5, from repaired head and main 7a8d9c16daa267c3a778554036374884194c2c36. All eleven worker/resolver jobs in deferred run 37739532146 also pass; its final aggregate is queued at 07:21 UTC. Parent think-9swm retains that final merge-readiness obligation.

Dedicated correctness review B https://github.com/jlevy/squares/pull/433#pullrequestreview-5452827342 and resource review C https://github.com/jlevy/squares/pull/433#pullrequestreview-5452965842 verify the repaired head with no findings or suggestions. C independently confirms the byte delta and five copies per policy: 854,512 to 56,096 bytes in its fixture, with private indexed copies and exact counter agreement. A1 has no remaining repair or verification obligation.
