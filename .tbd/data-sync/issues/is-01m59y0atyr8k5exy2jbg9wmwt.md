---
type: is
id: is-01m59y0atyr8k5exy2jbg9wmwt
title: Adopt T-218 at n183 and regularize it in the next intake PR
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-n183-adoption-20261019
labels:
  - result-import
  - regularization
  - validation
dependencies: []
parent_id: is-01m59few7wa6j6yrnw49hjap7r
hold: null
hold_until: null
created_at: 2026-10-19T11:16:02.525Z
updated_at: 2026-10-19T18:47:43.192Z
started_at: 2026-10-19T16:47:23.660Z
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
