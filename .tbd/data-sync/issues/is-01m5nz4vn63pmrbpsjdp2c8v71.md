---
type: is
id: is-01m5nz4vn63pmrbpsjdp2c8v71
title: "Validate: exact audit of Friedman's four unavoidable points for s(5) (T-237 C3)"
kind: task
status: closed
priority: 3
version: 4
delegate: w-backlog-1025
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T03:26:52.582Z
updated_at: 2026-10-26T02:15:07.494Z
started_at: 2026-10-25T16:27:09.231Z
closed_at: 2026-10-26T02:15:07.494Z
close_reason: "Exact audit of Friedman's Theorem 2 landed (E-n005-friedman-theorem2-audit); T-237 at C3; PR #821"
resolution: null
duplicate_of: null
---
T-237's owed C3 (PR #750 review A4, https://github.com/jlevy/squares/pull/750#issuecomment-6379115396). T-237's next_rung names a machine check here of the lower half at n = 5: an exact audit of the four unavoidable points (1, 1), (1, 1 + 1/√2), (1 + 1/√2, 1) and (1 + 1/√2, 1 + 1/√2) of [0, 2 + 1/√2]^2 (Friedman DS7, Theorem 2), as T-004 audits Bentz's s(46) (cases/bentz46/verify_cover.py, E-bentz46-theorem8-audit).

Work: an exact checker in Q(√2) whose evidence entry cites [Göbel 1979] / [Friedman DS7] with origin audited-here and a named negative control, and T-237's evidence then cites it; remove the C3 item from unfinished_confirmations when it lands.

Price: compute is negligible. T-004's 45-point audit ran in 6.6 s wall here on 24 October 2026; the register records 0.01 CPU-hours (high 0.1). The cost is writing the checker, which CPU-hours do not price. Listed in T-237's unfinished_confirmations (rung C3).

## Notes

2026-10-26 w-backlog-1025: done in PR https://github.com/jlevy/squares/pull/821 (draft, branch claude/friendly-einstein-gf9z0h-backlog-1, commit f3c07b1e5). packing/cases/friedman5/verify_cover.py audits Friedman's DS7 Theorem 2 exactly over Q(sqrt 2). Ten cells tile [0, 2 + 1/sqrt 2]^2: 4 Lemma 1 corners, 4 Lemma 2 wall rectangles with x = 1/sqrt 2, y = 1 and margin 3 sqrt 2/2 - 2 > 0, and 2 Lemma 3 triangles with hypotenuse exactly 1. Every point is charged. The record cases/friedman5/certificate.json replays byte for byte in about 3 s. tests/test_friedman5.py (7 tests) holds two mutants with false claims, both refused: the gap + 1/100 and the offset + 1/100. E-n005-friedman-theorem2-audit (V-sqpack-cover, independent-implementation, origin audited-here) is cited by T-237 and by n-005's verified lower bound. check_results derives C3, so T-237 goes from C0 to C3. Both unfinished confirmations (C1 think-wuo4, C3 this bead) leave the register, since they lie at or below the rung. think-wuo4's review is still owed in next_rung. It should read the audit's observation that at x = 1/sqrt 2 Lemma 2's lowest-corner minimum is at 0 and 90 degrees (value 1 = y), not at 45. #785 is now "reply due, closeable" in check_requests; no reply is posted (coordinator's instruction). CPU: about 0.001 CPU-hours.
