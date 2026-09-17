---
type: is
id: is-01m2m5zjmj7dsycs1x6yxwcwwt
title: Reconcile CI topology PRs 183, 185, and 186 after the no-JS stack
kind: task
status: in_progress
priority: 1
version: 24
labels: []
dependencies:
  - type: blocks
    target: is-01m2mm43z5rhrhwg1ac775r1sc
parent_id: is-01m2k0eqwj7en422j33wtvw5dt
child_order_hints:
  - is-01m2mr9j6bs6xhve2eg1q4zdvg
  - is-01m2nf99em5gccxeaeynqzapm5
  - is-01m2nf9a0cvj36jvzep9mx7wta
  - is-01m2nf9ahn8sf67khhfcwqhxrc
  - is-01m2nhy9mwrebga1xzw3dq98bp
  - is-01m2nhy9nsqpwzpdgccyah2myd
  - is-01m2nz2awrxeaa1pgh6e7x1vjt
  - is-01m2p1yw0f08dvqdapngmdn25w
  - is-01m2pgxc5nk9hprqqt1v5xrzj3
  - is-01m2pgxe49n88xf9jaapk3rxxe
  - is-01m2phfjztg9q7vckn8he9jb9e
  - is-01m2phtqcr35drpbd01xrh0g8q
created_at: 2026-09-16T04:00:45.195Z
updated_at: 2026-09-17T12:07:22.195Z
---
After PRs 175, 178, 179, 181, and 180 reach main, reconcile rather than wholesale-merge the three overlapping CI branches. Preserve PR 183 parallel Pages architecture after fixing its critical-path checkout and remeasuring; selectively port PR 185 fixture, browser-floor, standalone typecheck, and per-file-cost improvements without replacing the admitted suite-a/suite-b sharder; preserve PR 186 wall-measurement framework after fixing its Python 3.14 Ruff syntax and rewiring it to the final topology. Require exact-head hosted measurements, one consistent 180-second wall authority, and clean fast/Page gates.

## Notes

Independent senior reviews and a separate reconciliation audit agree: do not rebase/merge obsolete #185/#186 heads. After #180, create one replacement PR from new main, cross-link both old PRs, and supersede them only after replacement merge. Preserve public suite-a/suite-b and packing-required, but replace internal item-count post-collection sharding with #185's reviewed measured pre-collection selector; port fixture/performance work, standalone typecheck, frontend-owned browser liveness, exact-verification concurrency, verified-tree reuse, and Rust cache key repair. Then port #186 wall machinery into the existing packing-required/pages-required aggregates. Fix think-pu7l first; rebuild active budgets/medians from final-topology hosted runs, keep 180s authority, satisfy think-3919 variance evidence, and require CLEAN exact-head ordinary/Page/deferred/wall gates.


2026-09-16 recovery (Claude session after both Codex continuation threads stopped at ~22:17Z): local head da2259fb is 15 commits ahead of GitHub (remote c5a33270, stale CI, shows CONFLICTING only because it predates the main merge; local is 0 behind origin/main 035d84c6). cb705c67 (review gaps, think-f5cc) was independently approved; 27a53a8a differs from it only by the 192 MiB cap; da2259fb restores 160 MiB with a dated note. Gate receipts: 27a53a8a pre-push 6,558 passed / 28 skipped, browser floor unrun (no node_modules); da2259fb pre-push running. Remaining: exact-head pre-push pass, push, PR body refresh, green hosted Packing+Pages aggregates under 180 s, fresh independent review of that head, merge, then think-lop3 (#185) and think-z74z (session record). Child bead evidence audit in progress.


2026-09-17 update: pushed 7d76b044 (c5a33270..7d76b044) after the pre-push gate passed there (6,599 passed, 9 skipped, 49 of 80 steps). New since the recovery note: 2def8265 Pages deploy fix (think-w7oy), 9bac5b7f negative tests (think-pu7l, think-ysy5, think-iwxt), 7d76b044 session 137 record and plan checklist corrections (think-z74z, closed). think-30sx closed on the da2259fb receipt. Remaining: hosted exact-head aggregates at 7d76b044 and their wall readings into gate-budgets.yaml (which moves the head), fresh independent review of the final head, merge, then think-lop3 and the first post-merge deploy (think-w7oy).


2026-09-17 hosted evidence at 21642ed8: Pages run 35176748416 green. Packing run 35176748398 attempt 1 failed only the suite_b drift rule (work 82.6 s vs recorded 143.98 s, 0.57x; 4,003 passed); attempt 2 passed suite_b (137-141 s) but packing-required failed the pull-request wall at 216 s against 180 s (suite-b last: queued 3 s, setup 60 s including a 49 s full-history checkout, work 141 s). At 7d76b044 the wall was 178 s. Hosted variance on identical code is up to 1.8x per tier. Independent review of cb705c67..21642ed8: APPROVE WITH NITS for the code; merge blocked by the red required aggregate. Should-fix: session 137 must record 21642ed8, the push and these runs. Nits: agendas 031 and 033-035 wording, cap-comment diff description, SYNOPSIS "repaired" wording, exact deploy-condition test, guard empty artifact ids. In progress: wall stability (checkout cost, multi-cohort shard rebalance), code nits, then register recalibration from new exact-head runs (a record between ~92 and ~138 s accepts all three suite_b readings; 82.6 would not).


2026-09-17 owner decision: make the pull-request wall advisory on #188 (measured and reported, not failing the required aggregates) until think-g4n9 brings the worst case under 180 s and re-enforces it; everything else stays blocking. Committed on #188: 957e37af (review nits: exact deploy conditions, guarded artifact-id downloads, pruning comment), c4f0660d (suite shards rebalanced from same-speed cohort 35175474610; 16 phantom cost rows removed; blobless and sparse suite checkouts measured and refused). In progress: advisory wall implementation; then pre-push gate, push, three exact-head hosted samples with per-attempt artifact capture, register recalibration from those, session 137 update (review S1, N2, N3), final review of the delta.


2026-09-17 05:50Z: PR 188 pushed at 16d5e14d. be28ad5a: push tier passed locally (6,628 passed, 49 of 80 steps); hosted Packing run 35182460400 attempt 1 failed (think-g4n9 not yet on tbd-sync), attempt 2 failed suite_a drift (133.91 s vs 84 s), attempt 3 passed every job; Pages green; PR was CLEAN. 16d5e14d recalibrates suite_a to 109.92 s (attributed: ~1,000 tests moved into shard A by c4f0660d, prior record one fast-runner reading) and suite_b to 124.78 s, corrects the earlier suite_b attribution, and adds a Session 137 phase covering 21642ed8..be28ad5a plus the review's record nits (N1, N2, N3). Remaining: green aggregates on 16d5e14d, merge, close PR 185 (think-lop3), first Pages deploy (think-w7oy). PR 190 is mergeable (CLEAN) at 903e2277.


2026-09-17: independent review of 21642ed8..16d5e14d APPROVE WITH NITS, no blockers; a disposition audit of all 44 findings across every review round found 32 fixed, 6 accepted by owner decision or deferred to beads, 6 partial or unaddressed. A fix pass for the should-fixes (tree-reusable budget step, wall-reading comment), the stale wall records and suite prose, the session 137 push-order correction, dead suite_shard.py and nits is in progress. Merge rehearsal: GO for #188 at an exact head (merge tree equals CI-tested tree; deploy path traced; delete_branch_on_merge true, no branch protection). Still needed: green aggregates on the fix commit, the Deferred checkpoint via the deep-gate label, the review-disposition comment on the PR, owner go-ahead to merge.


2026-09-17 05:06 PT: #188 head 7f387990 (0d10d6c4 final review fixes; 7f387990 unmarks a sub-floor slow test). Hosted Packing and Pages aggregates green; Deferred checkpoint run 35213757305 passed every job; review-disposition comment posted (issuecomment-5714064819: 44 findings, 37 fixed, 3 owner decision, 3 deferred, 1 kept); PR description rewritten. Ready to merge on owner go-ahead, first in the sequence #188 -> #185 -> #190 -> #191 -> #192.
