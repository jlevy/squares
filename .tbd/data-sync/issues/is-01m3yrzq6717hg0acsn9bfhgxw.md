---
type: is
id: is-01m3yrzq6717hg0acsn9bfhgxw
title: "T-036: a replay mode for the Trump isolation radius, and its replayed entry (C2 to C3)"
kind: task
status: closed
priority: 2
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m3yrzkz80qd1wv5sjr0kkkv0
created_at: 2026-10-02T17:00:58.951Z
updated_at: 2026-10-23T06:12:08.733Z
closed_at: 2026-10-23T06:12:08.733Z
close_reason: "Tracker audit 2026-10-23 (c-audit-a-1023, think-s4ld), checked by coord-intake-1023: DONE. T-036 evidence includes E-n011-trump-isolation-radius; next_rung says 'The replay mode the closed-tree review asked for exists, and the radius has its own exact-algebraic entry'"
resolution: null
duplicate_of: null
---
T-036 (Trump's pose is optimal among six-plus-five packings near its tilt, our own result) is V3/C2: E-n011-trump-local-theorem-first-clause is proof-audited, which derives no higher than C2.

How to finish:
1. Give packing/cases/trump11/isolation_radius.py a replay mode that recomputes rho_row from the retained bc-199 record's inputs and per-face dual witnesses and compares it field for field with campaign/series/series-000-smoke-and-calibration/results/bc-199-trump-isolation-radius.json (the closed-tree review's residual 3, docs/project/reviews/review-2026-09-24-rung0-closed-tree.md), retaining the per-face witnesses it needs.
2. Run it from packing/ (`uv run --frozen --all-extras --group dev python -m cases.trump11.isolation_radius --replay <record>`), with a control that a perturbed radius or witness is refused.
3. Record an exact-algebraic evidence entry, origin replayed-here, with certificate, replay command and replay_status passed, and a `composition` note on T-036 judging that BC-240's audited prose steps do not set the confirmation minimum. Run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.
Expected CPU: about 6 minutes (the record's elapsed_seconds is 350).
What refutes: the replay disagreeing with the retained radius rho_row = 808514697/200000000000, or the review finding a prose step load-bearing; T-036 then stays C2 with the finding recorded.
What moves the rung: check_results derives C3 from the new entry; V stays V3.
