---
type: is
id: is-01m4cj28f0q6ddpj6yr9rx9p4b
title: Import and verify issue432 newly reported ry-xu packings
kind: task
status: in_progress
priority: 1
version: 4
delegate: codex@spud10
labels:
  - result-import
dependencies: []
parent_id: is-01m4bxdtbvasjn91jwhz448s7b
child_order_hints:
  - is-01m4cn48znx4fcgq6tps4gdate
hold: null
hold_until: null
created_at: 2026-10-08T01:29:24.191Z
updated_at: 2026-10-11T05:05:19.631Z
started_at: 2026-10-08T01:29:38.835Z
---
Resume issue432 at immutable ry-xu/square_packing8dc415296f697f5140caea27c7a0193d52deb4e6: retain all25 reported rational source geometries, compare against current stack bounds (author18 survivors is provisional), exact independent feasibility/control replay, separate n51 Q(sqrt2) identity obligation, scoped reviews and stacked PR with full custody. Do not run producer code or claim global optimality. Temporary work on spud-ext1 only.

## Notes

## Stage 7 draft from main at c6bf2d46f, 2026-10-11 — not posted (owner: leave as drafts)

Ledger: closeable (`check_requests --report` at c6bf2d46f: all three results settled, no ask queued). Updates think-mtwe's 10 October draft: links point at `results.html`, and a new paragraph reports the confirmed certificates registered since (T-128, T-130, T-134, T-136 to T-140, T-146) that are smaller at sixteen of the seventeen rational counts (all but 261), pending adoption. The site still credits T-125/T-126 to "ry-xu" (the owner's name decision, think-ijv2, is open); the draft says Ryan Xu as other records do. No case ceiling moved.

@ry-xu, thank you. All 25 rational certificates and the undilated n = 51 construction are registered and confirmed, independently re-implemented, on `main` through [PR #442](https://github.com/jlevy/squares/pull/442):

- **[T-125](https://jlevy.github.io/squares/results.html#t-125), V3/C3:** finite feasibility of all 25 rational certificates, at the exact sides they state.
- **[T-126](https://jlevy.github.io/squares/results.html#t-126), V3/C3:** s(51) ≤ (16 + 5√2)/3 = 7.6903559372884…, the undilated construction over Q(√2).

**Which cases they hold.** Your certificates are the verified upper bound in the case records at 18 counts, the number your title gives. That is the 17 rational certificates at n = 70, 84, 86, 102, 103, 105, 108, 123, 126, 127, 129, 131, 146, 175, 261, 267 and 295, and the radical construction at n = 51. At the other eight counts, a smaller certificate already confirmed here holds the case: T-126 at 51 (in place of your rational n = 51), Siddharth Gupta's #438 refinements at 88, 130, 153, 179 and 236, and SQUISH at 258 and 263. Your certificates there stay confirmed and retained.

**Since then.** Later reports, now confirmed here, are smaller at sixteen of those seventeen rational counts, all but 261; at 51 your T-126 is still the smallest known. Most of them build on your packings:
- Evan Daniel's regularized certificates (T-146) at 70, 102, 103, 123, 129, 146 and 295 regularize your packings for display, at sides his source reports as their exact optima, and T-146 credits each packing to you (at 103 as Mishapolk refined it);
- Eric Deleeuw's refinement of your packing at 70 (T-137), and Evan Daniel's more precise certificate of your arrangement at 126 (T-139), credit you with the arrangement;
- Francisco Couzo's certificates (T-128, T-130, T-134, T-140) refine your packings at 84, 86, 105, 108, 127, 131, 175 and 267;
- Mishapolk's #470 witnesses (T-138) are smaller at 84, 86, 103, 105, 108, 127, 131, 175 and 267, and SQUISH's #481 packing (T-136) at 131.

No case ceiling has moved: the case records keep your certificates until house adoption, which waits for [jlevy/squares#403](https://github.com/jlevy/squares/pull/403), which rewrites every case record; your certificates are then kept as history where a smaller one is adopted.

**How it was checked.** It was independently re-implemented here; neither your Fraction checker nor David Ellsworth's `check_packing.py` ran. Two exact routes decided every rational certificate:
- this repository's `sqpack.verify`, which your issue also ran (at 84881f2), so this route is not independent of your own checks;
- `devtools.check_rational_witness_independent`, written separately here, which shares the exact half-angle conversion with it and decides the geometry separately.

The 75 complete jobs covered the 25 positives, each with a duplicate-square and an outside-container control, and made 2,078,082 pair decisions. Every positive passed both routes and every control failed both. The undilated n = 51 construction was decided by `sqpack.verify` and a separate exact Q(√2) checker, `devtools.ryxu_radical_n51.independent`, in three jobs and 7,650 pair decisions. `devtools.ryxu_house_links` checked the inputs and their binding to the case records. A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-08-ryxu-rational-radical-packets.md) accepted the feasibility and the custody. No human review is claimed.

**The contact count.** Both exact routes find 119 touching pairs and 1,156 strictly separated pairs in the undilated n = 51 construction, not the 191 touching pairs your issue reports. The bound does not depend on the count, so the 191 is left unconfirmed and is not registered.

This confirms finite feasibility only; no optimality or local-minimum claim is registered. Nothing you asked for is queued, so this issue is closed with this comment. If the adoption round changes what this comment says, a follow-up will note it.

---
_Generated by [Claude Code](https://claude.ai/code)_
