---
type: is
id: is-01m5rr21pm1cpb0ryp0pyvmkvy
title: "Read #565's comment of 2026-10-25T00:25:01Z: maximusrufus's second-machine rebuild of T-154 (sq17-lean v1.0.0)"
kind: task
status: closed
priority: 2
version: 5
delegate: c-triage-z2mj-1025
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-25T05:20:43.732Z
updated_at: 2026-10-25T06:31:13.378Z
started_at: 2026-10-25T05:21:00.620Z
closed_at: 2026-10-25T06:31:13.378Z
close_reason: "Triaged: #565's rebuild is the owner's decision (Form A/B, with think-6t6q); #799 V2/preprint folded into #808."
resolution: null
duplicate_of: null
---
Comment https://github.com/jlevy/squares/issues/565#issuecomment-6391388887 (maximusrufus): a clean rebuild of ofitzharding/sq17-lean at 0a7167efa (v1.0.0) on another machine (Lean v4.34.1, Mathlib d13f23b7 via lake exe cache get), receipts at maximusrufus/openai-math-replays@c01398bf8 sq17-rebuild/, offered as the complete build beyond the producer's that C3 asks for. #565 is held for the owner (think-mxhc, think-00y8): no pass posts on it or closes it. Triage read-only: what the rebuild establishes for T-154's rungs, what custody it needs, and what the owner should decide.

## Notes

2026-10-25 c-triage-z2mj-1025 (stage 1, read-only; files in the coordinator scratchpad triage-z2mj/: pins.json, 565-record-draft.yaml). PIN: comment 6391388887 (maximusrufus, 00:25:01Z, the only comment on #565; API JSON sha256 f4953202...7e19). Receipts maximusrufus/openai-math-replays c01398bf897d8688673b0eaac1284aa670607cf8 (committed 22:57:17Z, pushed 00:24:49Z; code MIT, text CC BY 4.0) sq17-rebuild/: BUILD.txt 802 B 7c7c99d9...6ca3, SHA256SUMS 442 B a672b7c0...1641 (all 5 listed digests match), Square17Optimality.log 1,115,493 B 5e74c4af...c241, HalfPlanePositiveControl.log d8ed9f61...4f02, HalfPlaneBoundaryControl.log b40c54d6...4ef1, module_log_count.txt "4951". All three logs are byte-identical to the producer's retained ones (gzip -9 -n of the final log = the packet's .gz, 51f05204...29fb); 13,343 native_decide facts. Execution-specific content: BUILD.txt prose only (WSL Ubuntu, 12 cores, --jobs 12 --proof-jobs 4, exit 0, wall 22,277 s); no per-module logs, stamps, archive/manifest/Mathlib-cache digests, lean --version, CPU time or memory. RUNG: a third party's complete rebuild at the source's pins; Mathlib via lake exe cache get is what the producer, next_rung and think-r109 all specify, so it does not disqualify. Level: reproduced with the producer's code (same sources, driver, compiled checkers, native_decide boundary); checks no certificate separately. Under epistemics.md as written it is the C3 route ("by a third party whose build is retained here"): C1 -> C3, confirmed, reproduced with the producer's code, V3 unchanged, case verified bounds unchanged (verified_here needs a run here; formalization pending adoption). evidence.yaml has 0 independently-external entries; #521's same-shape question (think-6t6q) is still the owner's. CUSTODY: packet maximusrufus-sq17-rebuild-2026-10-25 (~45 KB; final log gz at its own path although its bytes equal the producer's), evidence entry (independently-external, build_receipt BUILD.txt, axioms_receipt the gz, full coverage, proof + new audit_record, informally-verified read), T-154 controls (positive controls only), next_rung/unfinished_confirmations/composition rewritten; FORM B (external report, as #521) if the owner declines. Price for think-r109: <= ~74 core-hours (22,277 s x 12 cores). think-mxhc's draft reply is stale (says V0/C1) and its Q4 is partly answered. Hold stands; no reply drafted. OWNER: Q1 admit as independently-external (decide with think-6t6q)? Q2 ask maximusrufus first for reproduce.py stamps, archive digests and a console transcript? Q3 the owner's #565 reply should credit the rebuild.

2026-10-25 coord-intake-1024 on c-triage-z2mj-1025's report (scratch triage-z2mj/). #565 (owner-held): maximusrufus's receipts at openai-math-replays c01398bf8 pin and byte-match the producer's retained logs; a third party's rebuild with the producer's code (lowest independence level as code, independent as actor), the first single-machine complete build (22,277 s wall on 12 cores, about 74 core-h). OWNER QUESTIONS (not decided here): (a) admit it as a third party's replay moving T-154 C1 -> C3 (Form A) or record it as a report beside T-154 (Form B), decided with think-6t6q (#521's same-shape question); (b) ask maximusrufus for stamp files, archive digests and a console transcript in the owner's #565 reply; the held reply (think-mxhc) is stale (says V0/C1; should credit the rebuild). Drafts: 565-record-draft.yaml (both forms; read_through 2026-10-25T00:25:01Z). No record change or post until the owner decides. #799 V2/preprint: folded into W8 (#808) by the coordinator's decisions; O1 stays with the owner.
