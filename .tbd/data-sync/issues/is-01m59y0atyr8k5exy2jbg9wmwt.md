---
type: is
id: is-01m59y0atyr8k5exy2jbg9wmwt
title: Adopt T-218 at n183 and regularize it in the next intake PR
kind: task
status: closed
priority: 2
version: 9
delegate: c-lane-687
labels:
  - result-import
  - regularization
  - validation
dependencies: []
parent_id: is-01m59few7wa6j6yrnw49hjap7r
hold: null
hold_until: null
created_at: 2026-10-19T11:16:02.525Z
updated_at: 2026-10-20T17:15:46.497Z
started_at: 2026-10-19T16:47:23.660Z
closed_at: 2026-10-20T17:15:46.497Z
close_reason: "Done in #687 (merged d588ad987, 2026-10-20): n183 registered as T-220 (renumbered after #692 took T-218/T-219), adopted as the house and regularized; Fable round-2 review B approved; deferred checkpoint 39459276932 green; site v0.8.4."
resolution: null
duplicate_of: null
---
Adopt T-218's original n183 rational certificate in the next intake pull request and finish both maintained strong-generator regularizations in that same pull request. Owner: codex-n183-house-adoption-20261019. This open obligation supplies select_houses.PENDING_ADOPTION n183; the registration slice does not move a house or run a generator. Credit Daniel after Couzo, with Levy acknowledged only for register seed data.

## Validation

- Claim: T-218, n183 exact side 13999580178736252502081470897571/1000000000000000000000000000000, original search/packer/candidates/s183_h183b.cert at evand/square-packing 3a9948c781be668b1547cc2bf64a0d1e614f9bca. Finite feasibility is already confirmed by the complete retained two-route primary replay; do not rerun geometry to re-establish it.
- Run: prepare the bounded upper_bound_houses/adopt_houses source and credit wiring; remove only n183 from PENDING_ADOPTION, then use adopt_houses --dry-run and its printed adoption/atlas/axis/default-drawings commands. Run both strong generators using the exact commands and unique run directories printed by adopt_houses.regularization_owed; admit or settle on their receipts under the maintained guide. Run default_drawings --compare against the PR base and --check-state --base-ref origin/main. No moved-house deferral to PENDING_ALLOWED is permitted.
- Cost: 5-25 CPU-minutes (0.083-0.417 CPU-hours) for this one count, an estimate from the maintained per-count receipt range in packing/campaign/result-import.md; no generator measured on n183 yet.
- Budget status: gated on code slice/ordered registration landing; within the standing 40 CPU-hour item cap. NEXT_PULL_REQUEST staging, not an over-cap or no-writer exception.
- Possible subset under the cap: the complete one-count adoption and both strong generators fit.
- Depends on: registration/source-reader staging under think-chgb and coordinator's ordered T-218 registration publication/main binding; prepare house writer integration before running adoption.
- Done when: reviewed adoption PR removes n183 staging, both case upper lanes and house witness name the original certificate, both strong-generator receipts decide the new witness in that PR, drawings compare/state gates pass, credits remain Daniel after Couzo with limited project seed acknowledgment, and final qualification/CI passes. Close only after the change removing the last staged count has merged.
- Machine note: reuse the existing primary Python 3.14.7 environment and existing checkout; explicit mounted writable external TMPDIR/CARGO_TARGET_DIR/UV_CACHE_DIR. No new clone/environment, bulk restoration or source-program execution; coordinate generator CPU with live gates.

Backlog: this item is listed in packing/campaign/issue-intake/intake-followup-20261019/README.md; coordinator reconciles the existing pass backlog think-wpyh without transferring its owner.

## Notes

2026-10-19 claude-n183-adoption-20261019: claude/intake-n183-adoption 180d04ce4 adopts T-218 as n183 house (s(183) <= 13999580178736252502081470897571/10^30), integer conjecture withdrawn, both strong generators run (~953 CPU-s measured + selection), Evan Daniel same-side view admitted. Pending: independent Fable review (running), integration into claude/intake-2026-10-19 (running; custody SNAPSHOT_MAX_BYTES overage 230,964,958 vs 229,638,144 under investigation).

2026-10-19 lane-680: took over from the handoff (#684). Fresh branch claude/ecstatic-edison-8en33t-680-n183 from main 14fd9e27f carries only the n183 portion: 018eae944 stage 2-4 registration (T-218, from codex/handoff-20261019/intake without #446/#678 work), f81b6b576 adoption (port of 05bb6a7b3), 1c9... witness rebuild byte-identical to d126d43f1, axis view/default drawings byte-identical to d35ad3eda, custody re-run (67 houses, 26 mutations, snapshot 228,867,849 < 219 MiB cap), strong-generator receipts carried from 1c31a3b36 (inputs byte-identical), regenerated views, provisional-wording cleanup. adopt_houses --check OK (67), records tier green except release impact (cut pending). Reproduction of grid-slack 0.5 on this branch: same view, only timings/against-current differ. Next: push, draft PR, review, edition cut, merge, stage 7 reply.

2026-10-19 lane-680: reproduced all four strong-generator runs on branch head (scratch run dirs l680/runs): grid-slack 0.5/1/5 and regularize_evand run give the same views and receipts as the carried 1c31a3b36 runs; differences are only timings, workers, run-dir names and the against-current comparison (the drawn view is now the evand one). ~18 CPU-min at load ~30. CI at ea6a6d97e exposed grid-departure follow-ons (closed-form paragraph order, corpus-count tests, workbench grid fills, poster layout); fixed locally in 102812ec6/09bf45c99, posters being redrawn as infographics v0.6.4.

2026-10-19 23:50Z lane-680: PR #687 (https://github.com/jlevy/squares/pull/687). Review A round 1 (request changes) dispositioned in issuecomment-6278998921: A1-A5 fixed (count contracts, closed-form order, re-pin, verifier notes, merge with main), A6 fixed/withdrawn (reproduction not retained, not cited), A7 fixed, A8 declined (optional under think-1hmn). Posters redrawn as infographics v0.6.4; site v0.7.36 (after #645/#658/#646 took 0.7.33-0.7.35), explainer v0.4.9, no-change records for three papers. Hosted CI green at 1692c96d1; head now 5cda2a1de, records tier green locally. Round 2 review requested.
