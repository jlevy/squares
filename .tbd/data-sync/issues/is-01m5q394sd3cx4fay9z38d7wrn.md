---
type: is
id: is-01m5q394sd3cx4fay9z38d7wrn
title: "PR B of #763: map T-240's stage 4 review (V3/C3), adopt and regularize at 268 and 303"
kind: task
status: in_progress
priority: 1
version: 4
delegate: c-prb-763-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T13:58:21.741Z
updated_at: 2026-10-24T16:34:48.226Z
started_at: 2026-10-24T13:58:27.438Z
---

## Notes

2026-10-24 c-prb-763-1024 (PR B of #763, W2 records; coordinator coord-intake-1024). Branch claude/intake-2026-10-24-issue763-pr-b (worktree /home/user/wt-prb) from main 2ec489d1e. PR: https://github.com/jlevy/squares/pull/794 (draft; labels intake, S3).

DONE
- Review retained byte for byte (8ecf28f2b): docs/project/reviews/review-2026-10-24-couzo-n268-n303.md and the packet's review/review-2026-10-24/ (programs match out/program-digests.sha256), mapped in the document map.
- Mapping (0709fd3f5, fixes dce05249f): V-couzo-763-review-check (decides, clean-room); E-couzo-763-exact-feasibility (maintained replay, shared-components: sqpack/verify.py is the manifest's first checker, evand-cert reader; RF-4) and E-couzo-763-review-exact-feasibility (independent-implementation, coverage full 2/2); external_review on the report atom and the replay; T-240 reviews. check_results: T-240 V3/C3; S3 confirmed by the review. No unfinished_confirmations (none existed; rung 4 is in next_rung). check_requests --backlog no longer lists T-240.
- Record findings: RF-1 (co-author trailers and efef7d1's "Codex's reviewed intake" in the packet README, the report atom, T-240's claim), RF-2 (previous_source), RF-3 (one arrangement, three placements; packet question 8 and notes), RF-5 (268 decimal rounded at 14 places, no ellipsis), RF-6 (Daniel's 268 is Lavrentev's placement; credit follows the placement adopted). RF-7..RF-12 and the six author questions go in the reply.
- Adoption (1c4d4a25c): pass dated 2026-10-25 (the 24 October pass already moved 303); 268 from T-174 (4.45e-3), 303 from T-239 (2.78e-3); credit 268 Tymchishin -> Couzo, 303 Lavrentev -> Couzo (manifest's credit); in-corpus coverage entry couzo-issue763-2026-10-23-in-corpus; reader in upper_bound_reports.HOUSES.
- Regularization (cases/regularized_drawings/think-bk9r-2026-10-24/): grid-slack 0.5 deg admitted and drawn at both (row 10); evand regularizer: row-3 register candidates at both (268: exactly Daniel's 8a8879a side; 303: 8953489116897633490914356559681/(5*10^29), 3.63e-12 below T-240, first-pass rung, all three exact routes accept), row-7 review view at 268; SETTLED[268] removed. ~31 CPU-min (evand 1708 s, grid 73 s, selection and layer ~1.5 min).
- default_drawings --compare vs main: 268 decided-no-better T-174 house drawing (0 uneven, 838 sides) -> regularized grid view of T-240 (19 uneven, 751 sides); 303 grid view of T-239 (37 uneven, 760) -> grid view of T-240 (0 uneven, 848). No strong view gives way; 0 pending.
- Feeds (8977b819f, 95dca0137): custody (70 houses, 200 inputs, 44 mutations), screen (SCREEN_FINDINGS 124/1247/302/5243; 268 joins tolerance-unstable), bound citations, X049 censuses, research tables, case verifiers, rigidity blocks, census spans (Tymchishin, Lavrentev unresolved finders), tests; CI sweeps slice carries the 763 packet (5b663df70).
- Release: papers' no-change record measured at 8977b819 and dce05249 (69 files, byte-identical x3); stamp_landed --apply --date 2026-10-25 (houses 268, 303); DATA_REVISION re-pinned to 95dca0137 (6b6216108).
- Validation: records tier 53/53 at 6b6216108; edit tier 66/69 at 3913ad451 (rigidity fixed after; type floor timeout on the contended host, basedpyright on changed files 0 errors; ESLint env); 26 affected test modules 1752 passed, 4 failed and fixed.
- Reply to #763 drafted in think-ptkk's notes (not posted).

REMAINS / FOR THE COORDINATOR
- Merge on 25 October 2026 UTC or later (pass date). Re-stamp if later.
- Register candidates: the regularizer's solved view at 303 (3.63e-12 below T-240) needs a registration bead like think-8r5w; at 268 its side equals Daniel's (T-242 in #792). think-8r5w's own 303 candidate is now 2.78e-3 above the house.
- Row-7 review: Daniel's same-side view at 268, for the owner.
- think-l49q (#792): if it merges first, rename Daniel's 268 to T-242 in T-240's notes and next_rung on the merge of main; re-housing at 268 is think-hx0e's.
- Profiles for Tymchishin and Lavrentev (census spans unresolved).
- News: S3 story drafted in the PR body; lands after merge (import_changelog).
- The backlog bead's T-240 row can go (T-240 is V3/C3).
- The #763 acknowledgement's requests-record entry (posted 13:37:28Z) is not recorded here.

STATUS 2026-10-24 16:40Z (c-prb-763-1024): head 7b6410d83 (DATA_REVISION ff9e896e1). Hosted: Packing validation 40110977552 and Certificate page 40110977525 succeeded; packing-required and pages-required pass, 31 checks pass, none fail. Later fixes after the first notes: 95dca0137 (rigidity blocks), 5b663df70 (CI sweeps slice), 1c6be595f (tests), ff9e896e1 (composite figure record); papers re-measured at ff9e896e (69 files x3 identical). Not merged; main unchanged at 2ec489d1e. Not synced (the coordinator syncs).
