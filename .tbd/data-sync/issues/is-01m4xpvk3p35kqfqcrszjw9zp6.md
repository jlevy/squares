---
type: is
id: is-01m4xpvk3p35kqfqcrszjw9zp6
title: "Validate: wand125 s(39) >= 533/80 (mixed_n39_L66625), census of all 2,073 directions with whole-net controls (~7.1 CPU-h; control needs think-4uun)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: bold-ritchie-l32
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wv27yed1e2wfnq55h1avr0
hold: null
hold_until: null
created_at: 2026-10-14T17:20:13.941Z
updated_at: 2026-11-02T20:52:26.617Z
started_at: 2026-11-02T19:05:31.040Z
---
Validation part of think-u0av for n = 39 (T-175 in the 14 October records PR #602, V0/C1). Record-changing, but the whole-net control cannot pass until think-4uun lands.

## Validation
- Claim: s(39) >= 533/80 = 6.6625 by the check2 measure certificate mixed_n39_L66625 (687 positive rectangles, mass 3899999/100000, candidate digest 3b464f3f...9cfc, core 4999/5000, net {step 1/5002, last 2072}) at wand125/square-packing dfb2cf85fdf9ee5f95c5ec2c67fd49210854f146; release square-lower-bounds-v1 asset certificates__mixed_n39_L66625.tar.gz, 639,558 B, SHA-256 8e88ca06...851f (asset 635702665).
- Run: from packing/, `uv run --frozen --all-extras --group dev python -m devtools.sqverify_fast_census --family mixed --only mixed_n39_L66625 --threads 2 --resume`, then `--control` (99/100 mutant at every direction; original and near-threshold mutant at the least-bound direction, 1804), then `--evidence`; sqverify-fast from the reviewed crate source d97758bb (binary 567a0fd5). Packet packing/resources/web/wand125-fine-net-n37-n39-n44-2026-10-13/ (receipts/premises-n39.json, sample-diagnostic-n39.json, control-sample-n39.json).
- Cost: 7.09 CPU-h (full capture 12,758 CPU s + whole-net controls 12,781 CPU s), from this host's ratio 0.945 to the source on an 8-direction sample (48.06 vs 50.86 CPU s, 2026-10-14; packet README); 7.50 CPU-h at the source's own CPU (author's check2 run: 13,502 direction CPU s).
- Budget status (owner, 2026-10-14): runnable (<= 40 CPU-h).
- Possible <= 40 CPU-h subset: n/a (runnable as a whole).
- Depends on: think-4uun (the axis refusal judged against the sweep's enclosure; n = 39's axis gap is 1.26e-9 > AXIS_ROUNDING 1e-9, so under today's rule the control ends CONTROL_FAILED although the refusal is sound; owner's choice of option on jlevy/squares#543 for T-142); and the owner's #543 answer on retaining the check2 candidates where the census reads them.
- Done when: all 2,073 directions verified with the source's nodes and least bounds; the whole-net controls end CONTROLS_REFUSED under the fixed rule; the `--evidence` entry is registered on T-175 with the 14 October review as the mapped review; noted on think-u0av.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. About 3.5 wall-h at two workers on an idle host.

## Notes

2026-11-02 bold-ritchie-l32 (intake lane L32, epic think-3guf; branch claude/bold-ritchie-xo28us-l32, draft PR #889): the census ran; the whole-net control failed closed on the axis allowance only, as F-1 predicted, so T-176 stays V0/C1 (check_results: unchanged).
- Retention (commit 219bc1268): fine_net_followup retain held certificates__mixed_n39_L66625.tar.gz (639,558 B, 8e88ca06...851f) to its pin and copied its six data members to the 13 October packet's release/ (candidate 192,393 B, 03eef5c3..., the premises receipt's), by the owner's answer of 17 October; check-retained 0 problems; the census reads the packet from release/.
- Capture (commit fc7f4661d): sqverify-fast from reviewed source d97758bb (binary 567a0fd5, rebuilt here byte-identical, rustc 1.98.0) at two threads under nice -n 19, 19:05:17Z-20:41:53Z: VERIFIED at all 2,073 directions, 881,271,470 nodes, least certified bound 1.0000000000654117 at direction 1804, 11,404.3 CPU-s (3.17 CPU-h; priced 12,758), wall 5,796 s; --check 1 of 1 VERIFIED. capture-agreement (new, commit deb0811ca) against the source's check2/run.jsonl.gz: CAPTURE_AGREES_WITH_SOURCE_LOG at every direction (receipts/capture-agreement-n39.json).
- Control, 20:42:07Z-20:49:48Z (450 s of wall for the sweep): CONTROL_FAILED at r = 1804. The original verified again; the 99/100 mutant was refused at all 2,073 directions (summary REFUSED), 2,072 of them passing every predicate; at r = 0 the axis refusal is a coverage refusal in the domain with exact capture 0.99207... < 1 and the original at least 1, but captures_agree is false: the exact capture sits 1.26e-9 above the sweep's certified bound 0.9920712485323058, beyond AXIS_ROUNDING 1e-9. The near-threshold mutant was refused (counterexample-candidate). Kept as benchmarks/measure-verifier/census-mixed/wand125-fine-net-n37-n39-n44-2026-10-13/mixed_n39_L66625.control-failed-v2.json, as n26's (T-233) is.
- Records: T-176's claim, artifacts, next_rung (think-tcsl), unfinished_confirmations (re-judge or rerun the control under think-tcsl's fix, 0.01-0.26 CPU-h) and notes; the packet and census-folder READMEs, coverage note, bibliography note and resources index; census views regenerated. No evidence entry: --evidence refuses a row without CONTROLS_REFUSED, and the evidence is held as T-233's n = 26 is.
- What remains: think-tcsl (reviewed axis-allowance fix), then re-judge this receipt and map the replay evidence (the 14 October review is this certificate's review); no capture rerun. Claim kept (in progress) for the PR; not closed.
