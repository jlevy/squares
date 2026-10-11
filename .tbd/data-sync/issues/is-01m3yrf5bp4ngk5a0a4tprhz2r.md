---
type: is
id: is-01m3yrf5bp4ngk5a0a4tprhz2r
title: "T-046 leftovers: replay the 28 September rectangle certificates n = 51, 57, 58, 72, 73, 91 (n = 37 only if T-069's n37 fails)"
kind: task
status: closed
priority: 2
version: 8
delegate: claude-code@vm
labels:
  - result-import
dependencies:
  - type: blocks
    target: is-01m3yrzkz80qd1wv5sjr0kkkv0
parent_id: is-01m3yrdxte02c7bnygkke34ct4
hold: null
hold_until: null
created_at: 2026-10-02T16:51:56.405Z
updated_at: 2026-10-06T15:55:39.727Z
started_at: 2026-10-06T07:53:22.392Z
closed_at: 2026-10-06T15:55:39.726Z
close_reason: "Done: recorded by lane R5 (T-070, T-046 next_rung) / lane R3 (E-k2m4-evand-bentz4-lean-build) on 6 October, merged in #382"
resolution: null
duplicate_of: null
---
Dispatched to runners r1 (n72 workers 3, n91) and r2 (n73 workers 2, n51, n57+n58); transfer dirs wand125-rect-sept28-r1-*/-r2-* on branches claude/replay-wand125-rect-oct1-r1/-r2. Merge with audit_wand125_rectangles --packet 2026-09-28 --merge, then records. About 24 CPU-h.

## To finish (validation backlog, 2026-10-02)

T-046 (wand125's rectangle bounds of 27 and 28 September, V0/C0). After the runners finish: `.venv/bin/python3 -m devtools.audit_wand125_rectangles --packet 2026-09-28 --out resources/web/wand125-rectangle-certificates-2026-09-28/receipts/replay --merge <run dirs>`, then `--check`, then the records (apply_wand125_rectangles; each count that passes is registered again as replayed, as T-045 and T-070 were). About 24 CPU-hours. Refutes: verify.cpp refusing a direction, or a regenerated input whose digest differs from the upstream run's; the count is then recorded with replay_status failed. Moves the rung: T-046 itself reaches V3/C3 only when every one of its standing certificates has a passing replay; the 16 that T-068 raises would otherwise hold it at V0, so record that decision (replay them, or let the replayed entries carry those counts). C1 comes sooner, by recording the 2026-09-27 scaling review as external_review on the report entries. Run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.

## Notes

2026-10-03 06:05 s1 (n72, n91; claude/replay-wand125-sept28-s1 @8c4f1932) and s2 (n73, n51, n57+n58; sept28-s2 @a57330dd) running since 04:52Z; logs only so far, no verdicts.
2026-10-04 01:05 s1 done (n72, n91; claude/replay-wand125-sept28-s1, not merged). s2: n73, n51, n57 VERIFIED; n58 still running (claude/replay-wand125-sept28-s2 @0421bd77b). Next: the batched records lane after n58 finishes.

2026-10-06 (lane R5, think-wyf4): the six leftover replays (n51, 57, 58 from sept28-s2; n72, n91 from sept28-s1; n73 from sept28-s2), all VERIFIED 201/201 reproducing the upstream records, merged into the 28 September packet's receipts/replay with audit_wand125_rectangles --merge (--check passes); apply_wand125_rectangles raises the verified bound at n = 51 (2977/400), 57 (1567/200) and 72 (437/50); n58, 73, 91 pass but sit below T-091's mixed certificates. T-070 widened to 25 counts (one entry per revision's replays). T-046 next_rung rewritten and its stale activity (link think-20mv) removed: of the 18 standing certificates no replay carries, 16 are T-068's raises and n37, n60 are held by replayed bounds. The census route to T-046 itself is think-kf3o. Commit d07884498. Ready to close.
