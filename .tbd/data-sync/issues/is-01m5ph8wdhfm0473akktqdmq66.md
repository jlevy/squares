---
type: is
id: is-01m5ph8wdhfm0473akktqdmq66
title: "Address PR #781 review A (A1-A7): T-163's theorem part, the 18 pieces' replay as evidence, jExc wording, AI-assistance source, PR body"
kind: task
status: closed
priority: 1
version: 4
delegate: c-fix-781-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T08:43:38.801Z
updated_at: 2026-10-24T10:17:14.244Z
started_at: 2026-10-24T08:43:49.558Z
closed_at: 2026-10-24T10:17:14.244Z
close_reason: "Review A addressed at 8241aa881 (dispositions https://github.com/jlevy/squares/pull/781#issuecomment-6382994336): A1 via E-fang-excess-pieces-exact-replay (18/18 STRICT_VALID, receipt pieces-exact-check.log), A2-A7 fixed; hosted CI green (Packing validation 40084361052, Certificate page 40084361048, Branch mergeability 40084357404). Follow-up review B in think-j7d1."
resolution: null
duplicate_of: null
---

## Notes

## Review A of #781 addressed, 2026-10-24 (c-fix-781-1024, worktree /home/user/wt-781)

Head 8241aa881b44c3fee2149aea97e746ce0baab558 (ls-remote agrees); hosted CI green there (Packing validation 40084361052, Certificate page 40084361048, Branch mergeability 40084357404; 31 pass, 28 skipped, 0 fail; MERGEABLE). Dispositions reply: https://github.com/jlevy/squares/pull/781#issuecomment-6382994336. PR title and body refreshed.

Commits: aaf51a6fd (A1-A3, A5, A6 records, tests, packets), 7594246e2 (merge main 6808d293a, #787; conflicts in result-requests.yaml #603 summary and release.py, both sides kept), 98ce1995f (re-pin DATA_REVISION to aaf51a6f), 14452a74c (papers re-measured at 98ce1995: 69 files byte-identical x3, explainer math via SQPACK_CHROMIUM = host Chrome for Testing 153), b8e2c1fd9 (contract test: third conditional theorem), eba2bc491 (test_house_adoption LATER_CITATIONS projection for the n-241/n-273 citation; hosted shard C had failed on it at b8e2c1fd9, run 40083161890), fa9b8c073 (merge main b2ea7b09c, #788, no conflict, no data), 8241aa881 (release record notes #788 changes no paper input).

A1 path (a): E-fang-excess-pieces-exact-replay, receipt packing/resources/web/fang-excess-theorem-2026-10-13/receipts/pieces-exact-check.log (18 STRICT_VALID, least squeeze 0.000690144837 at 308, 4.9 CPU s); E-fang-excess-note-proof proof.conditional_on discharged by it; scope = the theorem's four counts (T-064 Valid7 precedent). V3 structural; note alone V0. A2: jExc short set {k = n-15 >= 37, k mod 21 in 16..20}, 1180/4986 to 5000 (test). A3: Fang comment 6255103888 quoted. A7: record half by #787; draft reconciled. think-494l's #603 draft revised locally (not synced).

Open: bead tree step fails on #534 naming closed think-wop1 (local bead store, outside the diff). Status of think-ist2 left to the coordinator.
