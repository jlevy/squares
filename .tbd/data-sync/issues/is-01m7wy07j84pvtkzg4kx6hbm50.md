---
type: is
id: is-01m7wy07j84pvtkzg4kx6hbm50
title: "Import #1039, #1041, #1042: Joost de Winter's raised lower bounds (56 + 34 + 48 counts, 19-218), Hosono-style rectangle measures with coverage proofs; triage, retain, replay within the compute cap"
kind: task
status: in_progress
priority: 1
version: 10
delegate: codex-intake-1119-01a1fb
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T16:52:57.032Z
updated_at: 2026-11-21T14:01:43.821Z
started_at: 2026-11-20T16:53:54.029Z
---

## Notes

## Lane c15-lower (2026-11-20)

Stage 1 done: draft PR #1051 (branch claude/intake-2026-11-20-lower-1039, head 133014bf78). Packet de-winter-lower-bounds-2026-11-19 at JoostdeWinter/square-packing 21d944c (text retained, measures/receipts/zip pinned by digest; both attachment URLs refused by the proxy; the 1039 zip is byte-identical in the folder, digest 9641ca15...). Report-order receipt campaign/issue-intake/lower-bounds-de-winter-20261120/ (devtools.lower_bound_claims): 139 claims all above the record; current 73 (1039: 23 + 7 consequences; 1041: 105, 111; 1042: 47; 161 comment), superseded 59. The 155-count comment on 1042 is think-4iec.

Control plan (17:39:53Z, before any replay it names): packing/resources/web/de-winter-lower-bounds-2026-11-19/receipts/controls-plan.txt, SHA-256 cc6a1bf43e33182bbdc448876ed5e730787e17262c0be6ad854de0ce76589f8e. Compute plan: about 17 CPU-hours central (34 at the upper estimate): 1041 ~2.4, 1042 ~6.6 (+ envelope arithmetic), 1039 ~8 (integer directions ~6.6, heterogeneous ~1, mixed ~0.5); each item under the 40 CPU-hour cap. The 1039 "existing source coverage" rows (sqverify-format receipts, 14.2G nodes, ~67 CPU-h if re-run) are not replayed: compared with the record's census receipts instead.

21 November local checkpoint: b01db0cf45ac454d1411255f83676725b40f1251, rebased by merge on main 1fd323589a. Reviewed first phase preserves the archive, classification and reply receipts, and validates all five execution-source files before producer import. Roster costs measured and all 122 focused/integrity tests passed. Scope is custody and replay preparation. Proof execution and result rungs remain queued, and the exact guarded edit tier is running.

2026-11-21T11:12Z: #1051 merged first-phase custody and register intake records at f1d8c74e01 after required packing, Pages and branch checks passed at 28f5aa4b86. Exact senior approval 6004774083. No submitted proof or lower bound was promoted. Pages run 44898014453. The next step is the separately budgeted source proof case audit/replay. The inherited uncommitted worktree was unavailable.

2026-11-21T11:24Z: Recovered eight n105 payloads from the pinned #1041 source, 198,560 bytes, checked against acquisition and manifest. Exploratory Apple Clang 21/arm64 run through the landed wrapper: first original octagon direction of each K=160,480,1440,4320 passed and matched archived counters exactly; four quarter-density controls all returned UNDECIDED with an unresolved box at 65 nodes. 4.47 CPU-seconds original and 1.48 controls with one worker, including compile and wrapper, under the memory guard. Output SHA-256 a4809d48d82350975cb85a077e2038e244bc4a65da787b91e1a20bd304b80da6 and e785f7270b0473db4095b49eed8680f0c4e73aea73e3044406cbad6f84d9d7fb. Same implementation, host deviation disclosed, no rung moved. Full n105 is 273 directions, plus near-threshold control and separate premise checks.

### Published lower-bound follow-ups, 21 November UTC

PR #1069 merged as 41ed4588f9cdf1aff073ba81428b95bdbcd0006c, with all three required checks green on 8f3203ed34 and successful live audit 44910469696. Main now records the three actual #1039/#1041/#1042 replies and the eight-file n105 exploratory sample. The guarded records tier passed all 55 checks and the methods-survey comparison produced 43 byte-identical files. Original and quarter-mass outputs cover four of 273 directions. The four original rows passed and matched the archived counts; four quarter-mass controls remained unresolved as planned. Apple Clang arm64 is exploratory, same implementation, with no rung or bound promotion. The remaining statements, coverage and original host obligations stay on their open research beads.
