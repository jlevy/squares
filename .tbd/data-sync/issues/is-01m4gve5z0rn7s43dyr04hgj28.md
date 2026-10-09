---
type: is
id: is-01m4gve5z0rn7s43dyr04hgj28
title: "Admit #472's 12 native kernel certificates (wand125) after clean replay and custody"
kind: task
status: closed
priority: 1
version: 11
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: codex@spud10.local
labels:
  - n-17
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
child_order_hints:
  - is-01m4h1cx9na53vx9yjzmddwyqm
hold: null
hold_until: null
created_at: 2026-10-09T17:30:09.760Z
updated_at: 2026-10-09T23:28:28.129Z
started_at: 2026-10-09T18:52:23.854Z
closed_at: 2026-10-09T23:28:28.129Z
close_reason: "PR #475 merged as 0f16c033a87464cfab127ba54748ca5e2536babd after final independent review D and exact-head complete checkpoint. Both sessions consolidated at https://github.com/jlevy/squares/pull/475#issuecomment-6090970439; tracker #405 and roster #413 updated, #472 closed. Comparator think-n53s remains open under think-tmz6; other scoped follow-ups remain open."
resolution: null
duplicate_of: null
---
Issue #472: 12 sub-pattern certificates from this repo's own producer (check_n17_subpattern mode A), standing kernel verifier FULL PASS at blob 1ad706c21 (main f0ec5b6), receipts dirty:true from a wrapper checkout with one hand-edited directory field each; hosted in wand125/square-packing releases (HostedData/v1). Exact projection vs main's 60-entry ledger: -1,047 orbits / -8,240 states -> 3,636 / 28,528; distance-2 tail 95 -> 94 (row 23). Needs: clean-worktree FULL replay under a ledger-listed verifier (main's verifier is now be8135f6, unlisted), Rust parity, custody under a census-readable manifest, admission round. Est. ~2 CPU-h, ~4 agent-h. Owner decision to start.

## Notes

2026-10-09T18:52Z User go-ahead 2026-10-09 ~18:55 UTC: do it here in parallel. Container: 4 cores, 15 GB RAM, cargo present; wand125 release downloads work; uploads.github.com reachable directly (302). Plan: admission-grade replay under listed verifier blob 1ad706c21 (main 3213d651b), forward check under be8135f6e, Rust parity, mirror to jlevy/squares release data/n17-issue-472-kernel-certificates-v1 with HostedData manifest, admission round on branch based on #475. Estimate ~3-4 h wall, ~4-6 CPU-h.



2026-10-09T19:14Z Integrity: 24 objects (411,682,476 B) SHA-256 + manifests OK. Rust parity (toolchain 1.98.0, n17_kernel_verify at 6a0499ba4): 12/12 PASS, all closures all_parent_poses_forbidden, 26 fields agree with contributor Python receipts; total ~12 min loaded. Paperwork: exp-317 registered locally (3d132c3e0 on i472/admission based on 2beac080d); dry-run census 3,636/28,528. Decisions: use ledger release data/n17-x048-session-168-certificates-v1 for custody (census reads only that manifest); parity comparator recorded as declared deviation + OR-1 bead; disclose replay started 18:57 before exp-317 commit (criteria from H-341 at 17:51). Python listed-blob replay in progress.



2026-10-09T19:34Z Container restarted mid-run; pass 1 survived. Pass 1 (admission grade, 3213d651b, verifier 1ad706c21, full, clean receipts): 12/12 PASS, closures all_parent_poses_forbidden, all fields equal contributor's; sum 6,461 s verifier time. Rust parity vs fresh replays: 12/12 agree on 26 fields. Pass 2 (forward, be8135f6e) restarted in background. Finalization agent applying exp-317: custody upload of 24 objects to data/n17-x048-session-168-certificates-v1, ledger rows, census recount.



2026-10-09T20:59Z Admission complete on branch: exp-317 accepted, H-341 confirmed (d9217eccf, ecd1b3871). Custody: 24 assets (411,682,476 B) on data/n17-x048-session-168-certificates-v1, clean fetch SHA OK. Census 72 admitted -> 3,636 orbits / 28,528 states, endpoint survives, d2 94/736. Forward replay under be8135f6e 12/12 PASS. Merged owner's concurrent commits on #475 (f957a7d80, 1ace022dd, 27d5d24b9) and main (#469 intake stack); pushed f21e0b345. Fable max admission review + CI/deep gate 37990527717 pending; merge needs user confirmation.



2026-10-09T21:28Z User 21:35 UTC: do NOT merge #475; leave it open, an Astra agent is also working on it. This session stops pushing to claude/modest-pascal-z3nisd. State at df5978cbe: exp-317 accepted, H-341 confirmed, custody uploaded (24 assets on data/n17-x048-session-168-certificates-v1), admission review B1 fixed (retained-json exemption + custody paths); Packing/Pages/mergeability green; deep gate 37992944295 running. Post-merge drafts for #405/#472/#413 saved in scratchpad/post/ (replace MERGE_SHA). #472 stays open until merge.



2026-10-09T21:45Z #475 at df5978cbe fully green: Packing 37992930137, Pages 37992930146, mergeability 37992924253, complete checkpoint 37992944295 12/12. Handoff comment https://github.com/jlevy/squares/pull/475#issuecomment-6089569216 (with post-merge drafts). Held open per owner (Astra agent working on it).
