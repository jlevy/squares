---
type: is
id: is-01m3v5tpd99dwt1tx2h7eerhcg
title: "Land the stack in order: #255 (website), then #262 (ladder), then #254 (math)"
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T07:28:28.071Z
updated_at: 2026-10-01T16:04:17.568Z
closed_at: 2026-10-01T16:04:17.565Z
close_reason: "All three landed on main on 2026-10-01: #255 website and #262 rating ladders (f9a3409f0), #254 math (5ec014a25). The later stack (#261, #265, #264, #269) landed the same day (main fe6399451)."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: land this as soon as possible, in an organized order, without time spent on conflicts. (1) jlevy/squares#255 is ready at 158820d9d: hosted CI 27 pass, mergeable, current with main 306ae9fab. The session permission check refused the merge (merge without review); the owner merges it (PR page, or gh api -X PUT repos/jlevy/squares/pulls/255/merge -f merge_method=merge; it is the base of a stack, so the ordinary merge call is refused). (2) After it merges: watch the Pages deploy, run check_published_site against the live site, record the overview and overview-unchanged job budgets from that run. (3) Point #262 at main once it carries the final website base and its gates pass; the owner merges. (4) #254 then takes one merge of main, one tool re-run and one gate run. (5) Follow-up PRs after that: claude/site-polish-2 (results table, intro), claude/prose-without-ceremony, the result-kind classification.

## Notes

2026-10-01 07:58 UTC: the owner merged the stack; jlevy/squares#255 and #262 landed together on main as f9a3409f0. Pages run 36833533118 and post-merge validation 36833532960 are running. Remaining: verify the live site; jlevy/squares#254 (math, now based on main) takes one merge of main; follow-up PRs claude/site-polish-2 and claude/prose-without-ceremony.
