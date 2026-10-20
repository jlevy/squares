---
type: is
id: is-01m4xpw83n12s71g17jgfd8msr
title: "Validate: cfcheck complete replay of the closed form's intervals 1 and 34, 8 records (~320-650 CPU-h; HELD)"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4x2z8wp9dzqk43j4gxdwr79
created_at: 2026-10-14T17:20:35.445Z
updated_at: 2026-10-14T17:20:35.445Z
---
Validation part of think-3n1x (wand125's independent checker cfcheck for the closed form, problems/closed-form/indep-checker at 746e2c5, #600; evidence on T-180 in the 14 October records PR #602). HELD by the owner's cap. This is the only second route for the closed form: cfcheck was written from SPEC.md, shares no code with replay4d (measured), and is an independent implementation of the producer's specification.

## Validation
- Claim: cfcheck accepts every leaf of intervals 1 and 34 of closed-form-v1 (8 records: 91,044 roots, 3,138,681 leaves, 0 refusals, as the source's two reports state). Interval 34 carries the record's 33 proved counts m^2-1, m^2-2, m^2-3 (m = 8..18); interval 1 carries none.
- Run: cfcheck built from the copy retained at packing/resources/web/wand125-closed-form-cfcheck-2026-10-14/square-packing/problems/closed-form/indep-checker/ (rustc 1.97.0, locked crates; 42 tests pass), driven by that packet's replay/cfcheck_replay.py `run` on each of the 8 records of intervals 1 and 34 (release closed-form-v1 assets interval_0_0.02.tar.gz and interval_0.99_1.tar.gz), full premises and every leaf, with the three re-sealed mutants as controls; then `price --calibration` re-run on the receipts.
- Cost: 288.45 worker-h at the source's rates (242.02 recorded + 46.43 for interval 1's 24,226 resumed roots, which carry no timing), which is about 320 CPU-h at this host's ratio on the smallest record (1.11) and about 650 CPU-h at the ratio over all twelve sampled region runs (2.39; range 0.43-5.71); receipts/price.json. B4U alone is 61.1 h at the source: 111 leaves of about 33 min each. For scale, replay4d did the same 8 records in 124.65 CPU-h.
- Budget status (owner, 2026-10-14): HELD (> 40 CPU-h, awaiting the owner).
- Possible <= 40 CPU-h subset (proposal only; never to be run without the owner's word): the two `top.rec` records in full, interval 1 (2,673 roots, 171,634 leaves; 1.85 worker-h at the source, about 2.1 CPU-h at the measured 1.11) and interval 34 (5,643 roots, 71,393 leaves; 3.58 worker-h, about 10.3 CPU-h at that region's sampled ratio 2.88): about 12-13 CPU-h for two of the eight records. It decides those two records only and no count, since every count needs all four regions of its interval. Interval 1's right.rec (16.59 worker-h, about 34 CPU-h at 2.03) is the next record that fits.
- Depends on: the owner's budget. The source's checkpoints for interval 1's resumed roots are not published, so a complete interval-1 run here is from scratch.
- Done when: all 8 records end `CFCHECK OK` (not PARTIAL) with the source's root and leaf counts, the 3 mutants end `CFCHECK REFUSE`, the receipts are kept in the packet, and the evidence plan (evidence-plan.md: E-wand125-closed-form-cfcheck-report, E-wand125-closed-form-cfcheck-sample, V-wand125-cfcheck) gains a replayed-here entry on T-180; noted on think-3n1x.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. The full replay is 80-160 wall-h on four dedicated cores; even the top.rec subset is several wall-hours.
