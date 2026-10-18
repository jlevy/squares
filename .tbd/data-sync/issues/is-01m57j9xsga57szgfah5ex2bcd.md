---
type: is
id: is-01m57j9xsga57szgfah5ex2bcd
title: "Address PR #665 review A: reconcile 37-count adoption"
kind: task
status: in_progress
priority: 1
version: 14
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m53ek3ff79x09e0bq00v9kcd
child_order_hints:
  - is-01m57ja7n509dvpscdq2yhrjyp
  - is-01m57ja83g45cqgbpbzrwqhhcj
  - is-01m57ja8hmnxefxj8ymx9537f2
  - is-01m57ja8zb6hss8cjvqfnp0ama
  - is-01m57ja9d68k25fjn6t8047jp5
  - is-01m57pjpenj2sq63cvqhtv2v8w
  - is-01m57syyvkw6dmkteecqk9nn5n
hold: null
hold_until: null
created_at: 2026-10-18T13:13:05.070Z
updated_at: 2026-10-18T15:46:07.993Z
started_at: 2026-10-18T13:13:25.509Z
---
Review A at https://github.com/jlevy/squares/pull/665#pullrequestreview-5562201404, pinned head bb85cbb590cbd009ebe5399dd379ee4a2faeeda5. Repair custody, derived records, adoption-dependent fixtures and result-page payload. Original owner remains claimed by user-eb-adopt-174; this linked lane owns the 18-Oct repair. Do not push until root coordinator validation and diff review.

## Notes

Current clean repair head: cd5cc5cff7c0365e185eba9e6226d59a10e011a7. Coordinator reviewed the substantive repair slices with no blocker. Commits: 391fdc594 adoption repair; b88568f9a probe lifetime/pool repair (closed child think-lrrt); bf93722b1 composite/fixture/consumer and paper review; aabaa006d data pin; 2890be7fa provisional site v0.7.26 patch and claim links; a8c9f46b8 README/site URL follow-through; cd5cc5cff browser/segment harness hardening (think-fzzu). T-195 is untouched; site version/date must reconcile in actual merge order. Original think-3mry remains separately claimed by user-eb-adopt-174.

Validation: fresh census check passed 100 records; initial focused batches passed 131 and 21 tests; harness passed 69; site cut passed 111 with 15 deselected; release contracts passed 41; record/pin quartet passed 4 in 5.86s at 2890. Pin and release impact are current. Eight generated paper HTML/Markdown files and linked assets equal original PR-head output before and after the site cut. Five claim documents change only 32 source-link revisions. No PDF rebuilt or compared.

Independent Astra bounded math review at 2890be7fa found no actionable findings. Fresh exact Fraction geometry accepted all 37 adopted T-174 houses plus retained n236 T-146 (863,887 pairs in 36.79s), and all 38 regularized views at their exact house sides (863,887 pairs in 34.22s). Complete house dictionaries match source certificate/native-job reconstruction; all 37 adopted sides strictly improve their archived predecessors. Maintained independent corner checker accepted n68 (2,278 pairs in 2.81s) and rejected duplicate/outside controls. Limits: no full three-route replay, optimizer replay, global/local optimality, rigidity or historical arrangement-identity proof. Report is transcribed from the review/tool transcript in independent-bounded-math-review.json; packings are unchanged through a8c9f46b8.

First completed push gate at 391fdc594: 67/69 steps passed, 1013.08s wall; normal tests 18,931 passed, 9 failed, 55 skipped, 1 xfailed; pool not reached. Four record/fixture failures have focused fixes. Five 60s nested-probe timeouts have concrete lifetime/pool repair without a timeout increase; exact earlier stall cause remains unproved. Initial setup-only interrupted failure is separately preserved.

Completed isolated full push gate at clean 2890be7fa: exit 1, 67/69 steps pass, 1366.35s wall within unchanged 1800s ceiling. Normal 18,928 passed, 5 failed, 55 skipped, 1 xfailed, 6 warnings; pool not reached. One real metadata failure was README's prior edition; the non-pytest URL registry drift also required owning regeneration. The other four failures were two empty-output 120s green-baseline timeouts, a 2s nested-pytest diagnostic not reaching its expected print, and a 10s segment-cover CLI timeout. Quiet unchanged-head diagnosis passed check_readme in 4.486s, ledger in 1.842s, and both shorter-deadline nodes (2 passed in 4.57s); exact broad-run stall causes remain unproved. think-fzzu supplies the reviewed cd5cc5cff hardening: two real controls move to pool; browser2s stays fixed, segment incomplete-command outer25s exceeds its two inner10s provenance calls, and a pure forced git-status-timeout test confirms exit2/error JSON/no proof. All 11 module tests pass in6.82s, Ruff/types and normal isolated hooks pass (2.65s). No speculative change to negative baselines.

Site-reference follow-through: owning URL writer/check accepts all 1,014 rows; only 482 lastmod dates change October 17 to 18, no URL identities or other fields. README changes only v0.7.25 to provisional v0.7.26. Four focused README/URL contracts pass in 1.06s; README owner, release impact (errors=[]), data pin bf93722b1, and diff checks pass. Normal direct isolated hooks pass in 72.70s. The full worktree is now clean after the separate two-file harness commit. No shared .venv mutation.

Full suite collection proves exactly identical 19,008 quick node identities at CPU_COUNT10 and CPU_COUNT4 before the latest harness changes. Current module collections prove 11 items = 9 normal + 2 pool, with exactly one new pure unit and no removed item. Combining those receipts derives a 19,009 full quick union, normal 18,988 / pool 21. CPU_COUNT4 maps to normal3; CPU_COUNT6 maps to normal5 through runner scheduling alone. Both retain pool1/jobs2/inner1 and all canonical ceilings, including1800s; final run shape awaits coordinator slot/resource selection. No new full collection on cd5cc5cff is claimed. Broad rerun is queued behind the coordinator's #676 records/push slot. Isolated frozen all-extra/dev external venv imports own sqpack/kpress/workbench_tools; Python3.14.7 and tools verified. Durable artifacts and exact command logs: /Volumes/spud-ext1/agent-source/squares-665-review-20261018/. Offline cost-first PR body revised and checker passes. No push, PR metadata mutation or disposition reply yet. A1-A5 remain open pending final full gate, repair-head hosted CI and marked dispositions. PR stays draft.
