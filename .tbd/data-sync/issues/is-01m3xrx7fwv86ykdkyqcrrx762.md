---
type: is
id: is-01m3xrx7fwv86ykdkyqcrrx762
title: "Import wand125: independent second checker for Valid7 (T-064) (#296)"
kind: task
status: closed
priority: 2
version: 5
labels:
  - result-import
  - packing
dependencies: []
parent_id: is-01m3wvgebtkjqb3km59h7768zx
created_at: 2026-10-02T07:40:22.908Z
updated_at: 2026-10-03T23:46:41.573Z
closed_at: 2026-10-03T23:46:41.572Z
close_reason: "PR #329 merged at eb9fbb730: wand125's independent Valid7 checker replayed in full here with D-1 guarded (14 shards, 33 runs, 156,800 roots VERIFIED, compare ok); E-k2m3-wand125-valid7-independent verified/passed; T-064 stays V3/C3, now confirmed by an independent implementation as well as the producer's code."
resolution: null
duplicate_of: null
---
Result import process, K. wand125/valid7-independent-check (MIT), records in release records-v1; verify.sh fetches records, checks SHA-256, reruns check_record.py (RECORD OK) and three mutant tests; 156,800 roots over the whole pose space, exact rationals, written from FORMAT.md only (READ_LOG.md). About 626 core-hours to regenerate. Register action: evidence update to T-064 (no new entry), with the replay of the record check; T-064 claim text and next_rung per #296's suggestions after review. Also s(78) = 9 second route via s(77) = 9 (T-067).

## Notes

2026-10-03 06:05 wand125 independent Valid7 checker with --guard-d1: w5 DONE, shards 13-14 all VERIFIED (claude/replay-valid7-w5 @8cfcb5aa; 0 uncertified, 0 counterexamples). w4: 10_1-10_3, 11_1 VERIFIED; 11_2, 12_1 left (@2e8570b0). w3: shards 7, 8 and 9_1 VERIFIED; 9_2, 9_3 left (@1e6ec98c; 8_3 receipt shows already-done 0 after a relaunch overwrote the partial receipt, record rebuilt in full). w2: shard 4, 5_1, 5_2 VERIFIED; 5_3, shard 6 left (@02eb2c1e). w1: shard 1, 2_1 VERIFIED; 2_2 resumed, then 2_3, shard 3 (@c7e4c660). When all finish, the records lane merges w1-w5 receipts as independent-implementation evidence on T-064.
2026-10-03 17:40 Valid7 independent checker (--guard-d1): w3 DONE (shards 7-9, nine runs VERIFIED exit 0; claude/replay-valid7-w3; also pushed a stray sync.sh helper, drop it at merge), w4 DONE (shards 10-12, six runs VERIFIED; claude/replay-valid7-w4), w5 DONE (13-14). w2: runs 1-7 done, shard 6 run 3 (last) running. w1: shards 1-2 done, shard 3 resumed (181/448 roots at the 2 h cut). After all pass: merge w1-w5 receipts as independent-implementation evidence on T-064, in the follow-up branch after the stack lands (scope freeze).
2026-10-03 23:40 Recorded in jlevy/squares#329 (branch claude/t064-valid7-independent-replay; records commit 1eacc3ee3, re-pin 441972e64). All five runner branches' receipts brought in by path checkout to packing/resources/web/wand125-valid7-independent-check-2026-10-02/receipts/replay/ (33 records, 53 logs with the 20 retries; w3's sync.sh dropped). plan_valid7_replay compare --checker wand125 --guard-d1 against records-v1: ok, 156,800 roots, 9,808,968 leaves, 124,975 V2 roots with the published leaves (wand125_replay_compare.json). E-k2m3-wand125-valid7-independent is now verified, exact-algebraic, replayed-here, independent-implementation, replay_status passed. T-064 stays V3/C3; its derived code now reads independently re-implemented. Not closed: the coordinator closes after the merge. Left for the coordinator: packing/resources/README.md's row for the key still says the run was not repeated (outside this lane's write set).
