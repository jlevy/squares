---
type: is
id: is-01m4qkwr49aszyn8q68yde48q9
title: "Import E. Summins: independent replay of T-037 (Kleddamag s(11) > 31/8 v1.0.2), a confirmation record (#521)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T08:32:59.529Z
updated_at: 2026-10-12T08:57:43.829Z
started_at: 2026-10-12T08:52:51.093Z
---
https://github.com/jlevy/squares/issues/521 (2026-10-12T04:12:24Z). Esummins/packing at 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb: attempts/A242-replay-31-8/ (replay242.{md,json}, spot242.{json,jsonl}, controls, integrity, ext/PIN.json), writeup/outreach/08-t037-replay.md. A third party's full re-run of Kleddamag's exact Python sweep (12,028/12,028 rows, 0 differ) plus an independent exact spot check; no new result. Stage 1 triage and stage 2 retention in the esummins-packing-2026-10-12 packet; cheap spot-check re-run here.

## Notes

## Stage 1 triage (2026-10-12, lane intake-esummins, worktree branch intake-esummins from l4 dead83f0e)

- Pin: Esummins/packing 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb on master, committed 2026-10-12T04:11:54Z (author date 2026-10-11T21:11:54-07:00), "LICENSE: code MIT, documents/data CC BY 4.0 (PI, 2026-10-11)". Head at the read eb3ae15 (04:13:07Z) adds only writeup/outreach/POSTED.md. Issue filed 2026-10-12T04:12:24Z, label intake. Licence at the pin: code MIT, documents and data CC BY 4.0. AI assistance: the lab's campaigns, code, certificates, Lean files and notes "were produced by AI agents (Claude, Anthropic) under the PI's direction".
- Claims (stage 1 table): one confirmation record about a registered entry, T-037. "New evidence about a registered entry: no new entry; the source retained at the revision that holds it, and an evidence update." Nothing claims a bound.
  - The row replay: Kleddamag's own exact_mixed.py + integer_sweep.py (the kernel of V-kleddamag-n11-verify) driven by the lab's rows242.py in two shards, numba replaced by an identity shim (same kernel source, uncompiled), verify.py and replay_parallel.py not used; 12,028/12,028 rows, 0 differ from both evidence files (initial, portable), histogram equal, min 999962528 at row 11962, budget 10999479944, surplus 107864, 86,299,918 slabs, 511,649,694,680 cells, 8,089 CPU-s. These agree with E-n011-kleddamag-3875-source-replay's receipt.
  - The controls (independent_controls.py, 48,112 containment checks, 5,586 boundary centres, min 1000047518) and the integrity check (54 files, twice) re-run.
  - The spot check spot242.py, the lab's own Fraction/int code sharing nothing with the release: (a) (191/50)/(764/775) = 31/8; (b) M re-summed over the D4-expanded data = 10999479944 (point 2247714156, 2-of-3 3188007592, 2-of-5 989672288, 3-of-5 4574085908), D4 invariance; (c) 3,240 exact poses (2,000 random rows, 1,000 draws from the 47 critical rows, 60 corner domains), 0 failures, min charge 1000047518; (d) 11G - M = 107864 > 0. A sample, so a diagnostic by stage 4's rule, not a decision.
  - Not run by the lab: the secondary JavaScript checker (prepare_secondary.py fetches the R038 upstream file).
- How it would be recorded (epistemics.md Confirmation; precedents E-n061-wand125-point-cover-evand-replay-report and E-k2m4-wand125-validtilt9-report, the only two performed_by: independent-external entries, both origin external, assurance reported, replay_status not-attempted even with the run records retained): a new evidence entry on T-037, assurance reported, origin external, performed_by independent-external, relationship_to_generator same-implementation (the deciding programs are the producer's; rows242.py only orchestrates), verifiers [V-kleddamag-n11-verify] with spot242.py as a premise check (independent arithmetic, a sample), certificate the retained Kleddamag global-certificate.json. Owner decision: whether a third party's own full re-run with retained receipts is instead origin independently-external, the confirming origin epistemics.md defines as "a third party's own replay, retained here"; the precedents chose external.
- Does it change T-037's confirmation? No. T-037 is V3/C3 on two methods here (source sweeps replayed, native parent-core). A third party's same-implementation re-run is the "third party's retained replay" attribute beside the rung, not a rung, and it cannot make the result read as independently re-implemented. next_rung (two adversarial reviews, oversight record) is untouched.
- Checked here: the join keys. Their ext/PIN.json certificate sha256 57e9927d...cd44458 and evidence/portable/python.json sha256 68b6f360...7bc0 equal this repository's retained copies (external-square-certificates-2026-09-22/kleddamag-11). rows242.py and spot242.py read before running: no network, no writes outside results/, a Windows-only priority call caught by try/except. Re-ran spot242.py here from a scratch layout (code/, ext/repo/, results/ outside both repositories) against the retained certificate and evidence, CPython 3.14.7, args 2000 1000 242: all_pass true, 3,240 poses, 0 failures, min charge 1000047518, M = 10999479944, 11G - M = 107864; results/spot242.jsonl byte-identical to the lab's retained rows (sha256 256a47d4ba2f491842880b322ea86218ea8a6ac84ce9970c486710539f38bcb9); 67.1 s wall at load average 18 on four cores (10.7 s at the lab). Receipt: packet receipts/spot242-rerun-2026-10-12.{json,sha256}.
- Not checked: the row sweep (8,089 CPU-s at the lab; the source replay here already decides it), their controls run, the integrity check on their clone, the ThresholdBound.lean file beyond reading it (axiom threshold_bound_31_8 documented as external; budget_lemma, counting, scaling_arith trivial theorems; not a formalization of the sweep).
- CRLF note: verify_threshold_algebra.py writes threshold-algebra.json into the tree; on their Windows checkout it rewrote the pinned file with CRLF. The replay here ran on a writable copy (E-n011-kleddamag-3875-source-replay, limitations), so it is a portability note for the Kleddamag packet README, not a defect.
- Their ask 3 (an offline copy of the JavaScript secondary): the external-square-certificates-2026-09-22 packet retains the R038 reconstruction hash-pinned and the source replay here ran both scanners; the reply can say so.
- Review route and price: no mathematics to review; a records-lane evidence entry (30 minutes) and a one-line note on the Kleddamag packet README.
- Retained: packet packing/resources/web/esummins-packing-2026-10-12/ (whole series; attempts/A242-replay-31-8/ in full, the two shard jsonl and spot242.jsonl stored gzip).

## Acknowledgement draft (stage 1; not posted)

@Esummins, thank you. Received: your replay of Kleddamag's v1.0.2 certificate (T-037) at [Esummins/packing@651a9a5](https://github.com/Esummins/packing/tree/651a9a54688341880e9c0dc9fcfc19f2c04cd3cb/attempts/A242-replay-31-8), committed 2026-10-12T04:11:54Z and pinned at that commit. The series index and its section 4 manifest are retained with it.

What was checked: the certificate and evidence digests in your `ext/PIN.json` join the copies this repository retains, and your `spot242.py` was read and re-run here against them with your seed; it reproduced your 3,240 rows byte for byte. Your row-by-row totals agree with the replay recorded here. What this is in the record's terms: a third party's re-run of the author's own checker, recorded as your report beside T-037; it does not change T-037's rung, which rests on the replays and reviews already recorded. On your third question: the secondary JavaScript checker's R038 reconstruction is retained here hash-pinned and both scanners were run here, so no network fetch is needed to run it on your pin.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-12 09:00Z: packet committed on worktree branch intake-esummins at 7d4cc96c1 (not pushed); acquire_source --check PACKET_MATCHES_ITS_CONTRACT; proposed result-requests.yaml and intake-watch.yaml entries in the lane scratch file proposed-entries.yaml (reported to the coordinator), nothing applied to the shared records.
