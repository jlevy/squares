---
type: is
id: is-01m6na15dgp4fwgm2d24mcwk2w
title: "Validate: Özden s(94) >= 2493/250 (mixed_n94_L9972), census of all 4,972 directions with whole-net controls (~19 CPU-h, runnable after review) (#910)"
kind: task
status: open
priority: 1
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m6n86trbv1javs88wtdd2j24
created_at: 2026-11-05T07:33:33.232Z
updated_at: 2026-11-05T07:33:33.232Z
---
Validation part of think-pi8b for #910 (T-266, registered at V0/C0 on the intake PR of lane L49). Record-changing: with the stage 4 review (its own bead under think-pi8b), this is what moves n-094's verified lower lane from T-262's 1993/200 to 2493/250.

## Validation
- Claim: s(94) >= 2493/250 = 9.972 by certificate/n94-L9972.json.gz (format M; 853 rectangle orbits, mass 9399999/100000; B = 24872661/24875000; proof_net step 1/12000, last 4971, 4,972 directions; stored SHA-256 f59d4c95...360c), Hiroaki Hosono's mixed_n94_L995 dilated by 4986/4975, at kenaznia-doga/s94-lower-bound-9972@7d21f9bdf707102dd4ebf47e52f81b502a01004d, retained as packing/resources/web/ozden-s94-lower-bound-9972-2026-11-05 (census case mixed_n94_L9972, MIXED_FILES; producer relation same-implementation, SAME_CRATE_PACKETS). Checker: this repository's sqverify-fast, reviewed crate source d97758bb (REVIEWED_SOURCES, declared nets), binary 567a0fd5 (rustc 1.98.0, release).
- Run: from packing/, `nice -n 19 uv run --frozen --all-extras --group dev python -m devtools.sqverify_fast_census --family mixed --binary sqverify_fast/target/release/sqverify-fast --out benchmarks/measure-verifier/census-mixed --threads 2 --only mixed_n94_L9972 --resume`; then the same with `--control` (the 99/100 mutant at every direction of the net, the original and the near-threshold mutant at the least-bound direction); then `--evidence --only mixed_n94_L9972 --audit-record <the stage 4 review's path> --date <day>` for E-ozden-910-n94-9972-sqverify-fast-replay. Then extend devtools.audit_dilated_measure compare to read the lab's merged archive (receipts/directions.jsonl.gz; streams B, C and D are compacted to the proof fields) and compare the capture with it direction by direction.
- Cost: about 19.4 CPU-hours: the census 16.4 to 18.8 CPU-h and the whole-net control about 0.6 CPU-h. Bases: (a) the diagnostic sample receipts/sample-diagnostic.json (devtools.fine_net_followup sample, 13 directions at one thread each, two workers, 154.2 process CPU-s, 2026-11-05): 16.4 CPU-h by its mean; (b) its 24.99 us a node times the lab's 2,462,923,881 selected nodes (receipts/native-receipt-audit.json): 17.1 CPU-h; (c) #890's census, 8,138.6 CPU-s over 600 directions and 296,805,699 nodes at two threads: 18.8 CPU-h; #890's whole-net control, 134.9 s of wall at two threads for 600 directions, scaled to 4,972: about 0.6 CPU-h. The sample tool's conservative model, which prices the control as a second full sweep, gives 32.8 CPU-h.
- Budget status: runnable after review, under the owner's standing 40 CPU-hour item cap on every basis above; not held.
- Possible subset under the cap: not needed.
- Depends on: the stage 4 review lane (think-pi8b's review bead), whose acceptance the census row needs before it stands as evidence (the 6 October declared-net soundness review's records-lane item 7); the coordinator's go-ahead to spend the CPU.
- Done when: all 4,972 directions VERIFIED in the census row with the lab's least bound (1.0000000000003892 at 3663) and the exact capture at the least-bound leaf clearing 1; the --control receipt CONTROLS_REFUSED; E-ozden-910-n94-9972-sqverify-fast-replay registered on T-266 with the review as its audit record; check_results derives the rungs; n-094's verified lane moves to 2493/250 and T-262 is superseded there.
- Machine note: about 9.5 to 10 wall-hours at two threads on an idle host; run it outside a validation gate, at nice -n 19, with --resume. The control is about 17 minutes of wall.
