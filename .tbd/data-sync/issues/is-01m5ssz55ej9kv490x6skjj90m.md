---
type: is
id: is-01m5ssz55ej9kv490x6skjj90m
title: "Import #804's 297: Hyukdong Kim's degree-21 exact side of T-174's packing, with its exact configuration (s297-exact-configuration.zip e08b5d0a, CC0)"
kind: task
status: in_progress
priority: 2
version: 7
delegate: bold-ritchie-l20
labels:
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-25T15:13:20.558Z
updated_at: 2026-11-02T00:24:34.277Z
started_at: 2026-10-25T15:44:28.505Z
---
From read-only triage w-triage-1025b, 2026-10-25 ~15:20Z (findings: coordinator scratchpad triage-1025b.md). HyukdongKim on #804, comments 6397363927 (12:00:41Z) and 6397593690 (12:23:57Z): s(297) <= S*, the only real root of an irreducible degree-21 polynomial, claimed 3.36e-90 below T-174's certificate, with an exact configuration s297-exact-configuration.zip (SHA-256 e08b5d0a...47a7) under CC0, reported VALID on verify_exact.py. Checked here with SymPy: degree 21, irreducible, one real root matching the print, T-174 exact side minus root = +3.3591e-90 (decides nothing). Nothing else reports 297 below T-174. Disposition: a new register entry, a sibling of T-244 (next free id after main's T-246 is T-247; reserve before registering), decided on both exact routes (~2-8 CPU-h; needs an owner budget or the cap), sharing think-4rzl's tooling; draft S2. The attachment could not be fetched from this session (proxy blocks user-attachments). Coordinate with think-4rzl (c-decide-4rzl-1025), which edits the same #804 entry, packet and T-244 evidence.

## Notes

2026-11-01 bold-ritchie-l14 (PR #868): s297-exact-configuration.zip kept from HyukdongKim/square-packing-exact-sides f480441e (zip e08b5d0a...47a7, n297.minpoly.json e5c340b8...2826, both = comment's digests) under hyukdongkim-s297-2026-10-25/source/. Route B route 2 (verify_exact.py): VALID, 1,750 identities in K, 4/4 mutated controls refused; side held to T-247's. T-247 now V3/C3 (E-hyukdongkim-804-s297-verify-exact, deferral to think-vv1q/think-ot5c); #804 ask done. Route 1 (exact_verify, positive + 2 controls) is chained to start when the gradec replay exits (scratchpad/chain-route1.sh, PID 23164, jobs dir scratchpad/s297-route1); its receipt is receipts/algebraic-route1-n297.json.xz, then add an exact-feasibility evidence entry as T-244's. #804 follow-up owed after merge (think-8r92).

2026-11-02 bold-ritchie-l20 (lane L20, delegated from L14): route 1 of route B recorded on draft PR #876 (branch claude/bold-ritchie-xo28us-l20, head cd0d994ff, labels intake + S2). The receipt receipts/algebraic-route1-n297.json.xz (SHA-256 6736b3e4...dfed, byte-identical to the one the run wrote in L14's worktree) was assembled by `configuration_fact_replay --packet s297 route1 --jobs-dir <copy of scratchpad/s297-route1> --workers 2`, which reused the three finished job outputs and re-ran none; `--packet s297 check` admits it. Positive accepted (43,956 pairs), duplicate-square refused on overlap, outside-container refused on containment; 5,630 CPU-s on 1 November, nice -n 10, 2 workers. New evidence E-hyukdongkim-804-s297-exact-feasibility on T-247 (V3/C3 unchanged; status now independently re-implemented) and on #804's side-297, with a citation deferral (think-vv1q, blocked on think-ot5c, think-ikku). T-247 carries no unfinished_confirmations: #868 removed the route-A item (C3) when T-247 reached C3, and route A raises no rung. check_requests: #804 reply due for the new evidence; draft in think-8r92's notes, not posted. No-public-change record 2026-11-02-bold-ritchie-l20-t247-route1.yaml (four papers, 69 files byte-identical). Left open for the coordinator to close after merge.
