---
type: is
id: is-01m3yrf43whatj7rsvfbkqnaca
title: Integrate the stranded 29 September replays of T-048 (s(50) >= 37/5, L740) and T-055 (point-only s(21) = 5)
kind: task
status: open
priority: 2
version: 4
labels:
  - result-import
dependencies:
  - type: blocks
    target: is-01m3yrzkz80qd1wv5sjr0kkkv0
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T16:51:55.131Z
updated_at: 2026-10-02T17:14:12.362Z
---
Lane S: receipts from claude/replay-wand125-n50-l740-local and claude/replay-wand125-n21-point into their packets, n50-compare / n21-compare, controls; then the records lane adds the evidence entries (with verifiers and verifier_relation) and lets check_results derive the rungs.

## To finish (validation backlog, 2026-10-02)

T-048 (s(50) >= 37/5, V0/C0) and T-055 (point-only s(21) = 5, V0/C0). Both complete replays passed on 2026-09-29 and sit on branches claude/replay-wand125-n50-l740-local and claude/replay-wand125-n21-point. From packing/: `.venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n50-compare BUNDLE --out F` must print FULL_REPLAY_MATCHES_SHIPPED; `n21-compare OUT_DIR --m1-linkage M1 --collect RECEIPTS --out F` must match the pinned linkage; two mutated controls refused (`mixed-control n50 --work W` for L740). Then the evidence entries (exact-algebraic for n = 21, interval-certified for n = 50, origin replayed-here, replay_status passed, relationship_to_generator and verifiers) and the verified lanes of n = 50 to 53. Expected CPU: none new (the replays took about 10.5 CPU-hours on three workers and 8,577 s on two at the source); rerun only if the receipts cannot be recovered. Refutes: a comparison mismatch or a control accepted. Moves the rung: check_results derives V3/C3 for T-048 and T-055. Run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.
