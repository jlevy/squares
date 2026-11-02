---
type: is
id: is-01m4xpvm51z8nvp3j5xxjgdhr0
title: "Validate: wand125 s(44) >= 2799/400 (mixed_n44_L69975), census of all 2,073 directions with whole-net controls (~17 CPU-h)"
kind: task
status: open
priority: 1
version: 5
delegate: null
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wv27yed1e2wfnq55h1avr0
hold: null
hold_until: null
created_at: 2026-10-14T17:20:15.009Z
updated_at: 2026-11-02T11:29:35.724Z
started_at: 2026-11-02T11:29:20.653Z
---
Validation part of think-u0av for n = 44 (T-176 in the 14 October records PR #602, V0/C1). Record-changing.

## Validation
- Claim: s(44) >= 2799/400 = 6.9975 by the check2 measure certificate mixed_n44_L69975 (606 positive rectangles, mass 4399999/100000, candidate digest 02f4933f...24ef, core 4999/5000, net {step 1/5002, last 2072}) at wand125/square-packing 9f24185c602c8c0b83cf6a88b11a69ea8d668673; release square-lower-bounds-v1 asset certificates__mixed_n44_L69975.tar.gz, 631,497 B, SHA-256 b4cf96d5...3eb4 (asset 635703292). 1/400 below the upper bound 7.
- Run: from packing/, `uv run --frozen --all-extras --group dev python -m devtools.sqverify_fast_census --family mixed --only mixed_n44_L69975 --threads 2 --resume`, then `--control` (99/100 mutant at every direction; original and near-threshold mutant at the least-bound direction, 622), then `--evidence`; sqverify-fast from the reviewed crate source d97758bb (binary 567a0fd5). Packet packing/resources/web/wand125-fine-net-n37-n39-n44-2026-10-13/ (receipts/premises-n44.json, sample-diagnostic-n44.json, control-sample-n44.json).
- Cost: 16.95 CPU-h (full capture 30,492 CPU s + whole-net controls 30,533 CPU s), from this host's ratio 0.850 to the source on an 8-direction sample (107.87 vs 126.98 CPU s, 2026-10-14, load 4.6-9.3; packet README); 19.94 CPU-h at the source's own CPU (author's check2 run: 35,894 direction CPU s).
- Budget status (owner, 2026-10-14): runnable (<= 40 CPU-h).
- Possible <= 40 CPU-h subset: n/a (runnable as a whole).
- Depends on: the owner's answer on jlevy/squares#543 to retaining the check2 candidates where the census reads them. Not on think-4uun: n = 44's axis gap (1.3e-10) is inside AXIS_ROUNDING.
- Done when: all 2,073 directions verified with the source's nodes and least bounds; the whole-net controls end CONTROLS_REFUSED; the `--evidence` entry is registered on T-176 with the 14 October review as the mapped review; noted on think-u0av.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. About 8.5 wall-h at two workers on an idle host; run it outside a gate, with --resume.

## Notes

2026-11-02 bold-ritchie-l30 (intake lane L30, epic think-3guf): not run, by the coordinator's brief. The claim this bead validates, s(44) >= 2799/400 (now T-177 after the 14 October renumbering; T-176 is s(39), T-178 is s(37)), is superseded by T-252, s(44) = 7 (#842/#851, V3/C3, Khalili and Gharabaghi, merged at 90b79dbe1): the case is proved, and T-177's census would raise the rung of a lower bound 1/400 below a proved value, so it is low value for about 17 CPU-hours (20 at the source's CPU). The census itself is unchanged and still runnable (candidate not retained; add mixed_n44_L69975 to the 13 October packet's release/ as think-w76a did for n37). Whether to spend the 17 CPU-hours is the owner's call (think-u0av's 31 October note says the same). Released back to open.
