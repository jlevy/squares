---
type: is
id: is-01m5nz4vn63pmrbpsjdp2c8v71
title: "Validate: exact audit of Friedman's four unavoidable points for s(5) (T-237 C3)"
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T03:26:52.582Z
updated_at: 2026-10-24T03:26:52.582Z
---
T-237's owed C3 (PR #750 review A4, https://github.com/jlevy/squares/pull/750#issuecomment-6379115396). T-237's next_rung names a machine check here of the lower half at n = 5: an exact audit of the four unavoidable points (1, 1), (1, 1 + 1/√2), (1 + 1/√2, 1) and (1 + 1/√2, 1 + 1/√2) of [0, 2 + 1/√2]^2 (Friedman DS7, Theorem 2), as T-004 audits Bentz's s(46) (cases/bentz46/verify_cover.py, E-bentz46-theorem8-audit).

Work: an exact checker in Q(√2) whose evidence entry cites [Göbel 1979] / [Friedman DS7] with origin audited-here and a named negative control, and T-237's evidence then cites it; remove the C3 item from unfinished_confirmations when it lands.

Price: compute is negligible. T-004's 45-point audit ran in 6.6 s wall here on 24 October 2026; the register records 0.01 CPU-hours (high 0.1). The cost is writing the checker, which CPU-hours do not price. Listed in T-237's unfinished_confirmations (rung C3).
