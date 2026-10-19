---
type: is
id: is-01m4v4ehd59t1r89qwksx77bmh
title: "Merge the n = 17 stack (#560, #571, #577) and later landings of main into PR #578"
kind: task
status: in_progress
priority: 2
version: 31
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: profiles-final-merge
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
child_order_hints:
  - is-01m57g2khg6prcesy0fyxf32gc
  - is-01m59ev56c1da5q51t9h5jxpg7
  - is-01m59eyytph14724m9yrwe5x3e
  - is-01m59gqa1rq6jbsah86qha7xtt
  - is-01m59gsv3bsj068eq0mbhnga56
  - is-01m59jfeg786bcnxfbrm0mmjq3
  - is-01m59kfzac51p79k9q2myr0t18
hold: null
hold_until: null
created_at: 2026-10-13T17:20:02.981Z
updated_at: 2026-10-19T08:36:13.585Z
started_at: 2026-10-13T17:20:09.838Z
---
Watch origin/main and merge it into the profiles branch, keeping both the Overbeck and Hosono renames, reconciling the census and regenerating views. Stack merged in 37b1c8bf7.

## Notes

2026-10-19 continuation: all source work is isolated in /Volumes/spud-ext1/worktrees/squares-profiles-review-20261018 on codex/profiles-upstream-review-20261018. The original checkout remains unchanged at e1f921bf0; another agent owns the main checkout.

Pushed b76a24fd29bdab28b5c946adeff88313fd28eb47 to draft PR #578. Integrated 391 upstream commits through e952755bc, resolving 14 initial conflicted files and three later conflicts. Both parents' release histories survive; proposed site v0.8.0 follows v0.7.28. Data pin remains 0adba2aa6 because the latest incoming changes do not touch DATA_PATHS.

Independent Astra architecture and design reviews identified and reviewed fixes for source-specific identity authorization, overlapping spans, a native-panel request race, snapshot capacity, T-174 HTML size/link auditing, a parser callback signature, historical adoption replay, and complete release-decision scopes. Review B is published at https://github.com/jlevy/squares/pull/578#pullrequestreview-5568711596. Prepared Review C covers the latest upstream integration at the current head; publish it with final receipts.

Validation retained: 89 result/preview tests; six writer tests covering all 53 adoption contracts; 95 release/URL tests; 42 verifier-integration tests; browser floor including 341 Node tests; 50 screenshot contexts and 25 navigation checks. The exact post-commit release gate against e952755bc passes. The current standard validation job passes. Remaining standard CI is run 39222982076, Pages is 39222982024, and the full checkpoint is 39223503977. Superseded checkpoint attempts were canceled and are not complete passes.

Next entry: wait for these exact-head checks, fix any failures, publish Review C and Review A dispositions, close the fixed child beads, update this handoff and sync. Do not merge or deploy the draft PR. Local broad validation did not complete; retain the unexplained timing failures under think-j13b. Historical population remains think-m7il: 354 unresolved spans and 146 PDFs awaiting full-credit inspection.

Latest local preview was rebuilt from b76a24fd2 and opened in the default browser at http://127.0.0.1:8792/profiles/index.html. Its data-edition stamp is v0.8.0-0adba2. Durable review, design, timing and build evidence is in /Volumes/spud-ext1/agent-evidence/squares-profiles-review-20261019/. Prepared PR body and Review C are in the external task scratch tmp directory.
