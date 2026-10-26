---
type: is
id: is-01m5szcqa1r3bdx2xw9dpkf463
title: Review the 28 September rectangle certificates (39d8ecc) and the format_t_problems widening to mass n - 1/1000 (rect_n27_L56), mapped on T-046 (#773)
kind: task
status: in_progress
priority: 3
version: 3
delegate: w-t046-review-1026
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-25T16:48:08.001Z
updated_at: 2026-10-26T04:02:52.654Z
started_at: 2026-10-26T04:02:52.654Z
---
The review T-046's census route still needs before its C3 can be recorded (#773). Opened 2026-10-25 by w-backlog-1025 at the coordinator's request, when think-kf3o and think-sb7a landed the receipts. Unclaimed: a strong-max review lane, not yet started (the owner's token budget).

The format T route review, docs/project/reviews/review-2026-10-06-sqverify-fast-format-t-route.md, section 5 ("T-046, the 27 and 28 September packets") and its check 7, names two things no review has done:

1. Read the mathematics of the 28 September certificates (wand125/square-packing-bounds at 39d8ecc, packet resources/web/wand125-rectangle-certificates-2026-09-28). The 27 September scaling review (review-2026-09-27-wand125-rectangle-scaling.md) covers the 27 September packet only, and E-wand125-rectangle-2026-09-28-source-replay's limitations say no review read the 28 September certificates or their receipts.
2. Read the widening of tests/test_sqverify_fast_census.py's format_t_problems from mass n - 1/100 to n - 1/1000. Of T-046's certificates only rect_n27_L56 (27 September packet) needs it. The theorem uses only M < n, which admission recomputes, but the condition is the route's, so the review that maps the certificates reads it.

The receipts it reads are retained on branch claude/friendly-einstein-gf9z0h-backlog-1 (PR to be linked in the notes), under packing/benchmarks/measure-verifier/census/: the census rows of all 46 standing certificates (22 re-run on 25 October on reviewed source d97758bb, binary 567a0fd5, the other 24 already on 9985c465) and a control receipt for each, <name>.control.json in the 2026-09-27 and 2026-09-28 folders.

## Validation
- Claim: T-046, s(n) lower bounds at 48 counts from n = 18 to 95 by 46 standing rectangle-density certificates (Hosono after Tokoharu and Levy, square-packing-bounds ad43d29 and 39d8ecc); checker sqverify-fast (V-sqverify-fast), the format T census route.
- Run: a stage 4 review at tbd-strong-max, in a worktree of its own, of the 28 September certificates' mathematics and the format_t_problems mass widening, mapped in document-map.yaml and listed in T-046's reviews (accepted, covering T-046). Then widen format_t_problems as the review accepts it, and generate each certificate's entry with `.venv/bin/python3 -m devtools.sqverify_fast_census --evidence --only <name> --audit-record <review> --date 2026-10-25 --binary sqverify_fast/target/release/sqverify-fast --out benchmarks/measure-verifier/census`, checked against section 5's checks 1 to 9, and cite the entries on T-046 (the 27 September certificates may take review-2026-09-27-wand125-rectangle-scaling.md as audit_record if the review lane agrees it read them).
- Cost: the review is token cost, which CPU-hours do not price; --evidence and the checks take seconds; no replay is left to run (the receipts' CPU is on think-kf3o).
- Budget status: gated on decision (the owner's token budget for a strong-max review lane).
- Possible subset under the cap: the ten 27 September certificates with the 2026-09-27 review as their audit record, if that review is judged to have read them; T-046 itself moves only when all 46 carry.
- Depends on: think-kf3o's PR merged (the receipts); think-wcex for C1 is separate and not a prerequisite.
- Done when: the review is retained and mapped, T-046 cites one census evidence entry per standing certificate, tests/test_sqverify_fast_census.py passes with them, and devtools.check_results derives V3/C3 for T-046; #773 gets the stage 7 reply.
- Machine note: none beyond the project interpreter; the sqverify-fast binary is needed only for --evidence's build facts.

## Notes

2026-10-26 w-backlog-1025: the receipts are in PR https://github.com/jlevy/squares/pull/821 (commit dcde87d28), branch claude/friendly-einstein-gf9z0h-backlog-1.
