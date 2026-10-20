---
type: is
id: is-01m4v4ehd59t1r89qwksx77bmh
title: "Merge the n = 17 stack (#560, #571, #577) and later landings of main into PR #578"
kind: task
status: open
priority: 2
version: 35
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: null
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
  - is-01m5a4zc4pv94653zmjwbj73wc
  - is-01m5a5x0yke5qr3pas87kt8wvd
  - is-01m5aacgfa93je9b78k14cm4gg
hold: null
hold_until: null
created_at: 2026-10-13T17:20:02.981Z
updated_at: 2026-10-19T14:52:24.425Z
started_at: 2026-10-13T17:20:09.838Z
---
Watch origin/main and merge it into the profiles branch, keeping both the Overbeck and Hosono renames, reconciling the census and regenerating views. Stack merged in 37b1c8bf7.

## Notes

2026-10-19 requested integration and reviews complete. Source work isolated in /Volumes/spud-ext1/worktrees/squares-profiles-review-20261018 on codex/profiles-upstream-review-20261018; original checkout remains unchanged at e1f921bf09d6387fc27302b367cb4b1114b89082 and main checkout was not modified.

Draft PR #578 is pushed at b76a24fd29bdab28b5c946adeff88313fd28eb47, integrating 391 upstream commits through e952755bcad005738785ab8bab0d0b7176f34fed. Fourteen initial conflicts and three later conflicts resolved. Both release histories preserved; proposed site v0.8.0 follows v0.7.28. DATA_REVISION remains 0adba2aa6 because latest incoming changes do not touch DATA_PATHS.

Independent Astra senior and design reviews and subsequent fixes complete. Review B: https://github.com/jlevy/squares/pull/578#pullrequestreview-5568711596 . Final integration Review C: https://github.com/jlevy/squares/pull/578#pullrequestreview-5568927630 . Review A dispositions: https://github.com/jlevy/squares/pull/578#issuecomment-6263281637 . PR description and review receipts updated with final acceptance. Six verified fix beads closed: think-um9i, think-uivz, think-iyao, think-jhst, think-isve, think-97m2.

All standard packing CI (39222982076), publication CI (39222982024), mergeability check and full checkpoint (39223503977) passed at this exact head. Full checkpoint: https://github.com/jlevy/squares/actions/runs/39223503977 ; 14 successful jobs, 10 intentional skips, zero failures or pending jobs, 31m32s. Superseded canceled attempts are not counted as passes. Local focused and design evidence is retained, including 50 screenshot contexts and 25 navigation checks. Local broad validation did not complete and unexplained timing failures remain think-j13b, open and unclaimed.

Latest preview rebuilt from b76a24fd2 and opened in default browser: http://127.0.0.1:8792/profiles/index.html . Data-edition stamp v0.8.0-0adba2. Server session 19441 serves external scratch/site. Durable review, design, timing, build and CI evidence: /Volumes/spud-ext1/agent-evidence/squares-profiles-review-20261019/ .

Selected next entry: historical population remains think-m7il (354 unresolved spans and 146 PDFs awaiting full-credit inspection). Local timing diagnosis remains think-j13b. This recurring upstream-refresh bead returns open and unclaimed for future refreshes on request. Current requested integration is complete. Keep PR draft; do not merge or deploy.
