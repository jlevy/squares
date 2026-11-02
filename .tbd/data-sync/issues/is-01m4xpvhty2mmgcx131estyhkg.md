---
type: is
id: is-01m4xpvhty2mmgcx131estyhkg
title: "Validate: wand125 s(37) >= 2599/400 (mixed_n37_L64975), census of all 2,073 directions with whole-net controls (~6.5 CPU-h)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: bold-ritchie-l30
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wv27yed1e2wfnq55h1avr0
hold: null
hold_until: null
created_at: 2026-10-14T17:20:12.637Z
updated_at: 2026-11-02T14:37:42.944Z
started_at: 2026-11-02T11:13:37.982Z
---
Validation part of think-u0av for n = 37 (T-177 in the 14 October records PR #602, V0/C1). Record-changing: a complete replay with controls is what takes the bound to C3 and the verified lane.

## Validation
- Claim: s(37) >= 2599/400 = 6.4975 by the check2 measure certificate mixed_n37_L64975 (612 positive rectangles, mass 3699999/100000, candidate digest 23387d7d...4495, core 4999/5000, net {step 1/5002, last 2072}, 2,073 directions) at wand125/square-packing 7a42c16eacaab112b537ab09e89d3485f6f4c75f; release square-lower-bounds-v1 asset certificates__mixed_n37_L64975.tar.gz, 630,375 B, SHA-256 8aa78cc4...1965 (asset 635741442).
- Run: from packing/, `uv run --frozen --all-extras --group dev python -m devtools.sqverify_fast_census --family mixed --only mixed_n37_L64975 --threads 2 --resume`, then the same with `--control` (the 99/100 mutant at every direction, and the original and the near-threshold mutant at the least-bound direction, 1919), then `--evidence`. sqverify-fast built from the reviewed crate source d97758bb (binary 567a0fd5), reading a candidate retained where the census reads it. Packet packing/resources/web/wand125-fine-net-n37-n39-n44-2026-10-13/ (receipts/premises-n37.json, sample-diagnostic-n37.json, control-sample-n37.json).
- Cost: 6.53 CPU-h (full capture 11,739 CPU s + whole-net controls 11,759 CPU s), from this host's ratio 0.871 to the source on an 8-direction sample (43.08 vs 49.45 CPU s, 2026-10-14; packet README, The Price of a Complete Replay); 7.49 CPU-h if this host is no faster than the source (the author's check2 run: 13,474 direction CPU s).
- Budget status (owner, 2026-10-14): runnable (<= 40 CPU-h).
- Possible <= 40 CPU-h subset: n/a (runnable as a whole).
- Depends on: the owner's answer on jlevy/squares#543 to retaining the check2 candidates where the census reads them (in Git or as hosted data, OR-18); the census cannot run before that. Not on think-4uun: n = 37's axis gap (6.9e-11) is inside AXIS_ROUNDING.
- Done when: the census holds all 2,073 directions verified, with the source's node counts and least bounds; the whole-net controls end CONTROLS_REFUSED; the `--evidence` entry is registered on T-177 with the 14 October review (docs/project/reviews/review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md) as the mapped review; noted on think-u0av.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. About 3.3 wall-h at two workers on an idle host; schedule it outside a gate and use --resume.

## Notes

2026-11-02 bold-ritchie-l30 (intake lane L30, epic think-3guf; branch claude/bold-ritchie-xo28us-l30, draft PR #886). Done, for the coordinator to close after merge. Note: since the 14 October renumbering this claim is T-178, not T-177 (T-176 is s(39), T-177 is s(44)).

- Retention (0b34c8da5): release asset certificates__mixed_n37_L64975.tar.gz downloaded 2026-11-02 from wand125/square-packing square-lower-bounds-v1, 630,375 B, SHA-256 8aa78cc44e8ad50a340ffc9636b93af40cb942e7dcdd853a0e46c5739a651965 (the pin); `fine_net_followup retain` copied six data members (about 230 kB) to the packet's release/certificates/mixed_n37_L64975/ and pinned the nested verifier archive and the sealed bundle by digest; check-retained 0 problems. Authority for retention: the owner's 17 October answer (retain fine-net candidates by OR-18's size rule), as the n31 and #446 release packets did. sqverify_fast_census reads the packet from release/ (MIXED_PACKETS, MIXED_ROOTS, SHARED_CRATE_PACKETS) with a test.
- Capture (315a04a83): sqverify-fast from reviewed source d97758bb (binary 567a0fd5, rustc 1.98.0) at two threads under nice -n 19, 11:25:37Z to 13:23:59Z: VERIFIED at 2,073 of 2,073 directions, 864,953,550 nodes, least certified bound 1.0000000000165958 at direction 1919, 12,667.7 CPU-s (wait4), 7,100.6 s wall on a shared host; every direction's node count and least bound equal the source's check2 log; --check: 1 of 1 VERIFIED.
- Whole-net controls (34f8b6451): CONTROLS_REFUSED at r=1919: original verified again, 99/100 mutant refused at 2,073 of 2,073 directions, near-threshold mutant refused (13:23:59Z to 13:33:14Z).
- Records (101002a16): E-wand125-fine-net-n37-64975-sqverify-fast-replay from `--evidence` (audit record the 14 October review); T-178 V0/C1 -> V3/C3 as check_results derives; n-037's lower lanes 161/25 -> 2599/400; T-069 superseded there. Release record and re-pin: 00b7144de, 112bf04d9.
- CPU: about 3.7 CPU-hours for capture and controls (priced 6.53).
