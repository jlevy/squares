# T-132’s Fine-Net Census: `mixed_n29_L582`

This folder retains the native receipts of the complete replay of `mixed_n29_L582`
(T-132), the certificate of the
[10 October n29 packet](../../../../resources/web/wand125-fine-net-n29-2026-10-10/README.md),
run on 4 November 2026. Its census row is in [`census.json`](../census.json), and the
[Milestone B census](../README.md), which
`python -m devtools.sqverify_fast_census --family mixed --report` regenerates, shows it
beside every other mixed certificate.

The folder keeps:

- `mixed_n29_L582.jsonl.gz`, the capture: one row for each of the 2,073 directions of
  the net the candidate declares, and a summary.
  Every direction verified, 649,871,818 nodes in all, least certified bound
  1.0000000000046825 at direction 1947, whose least-bound leaf’s centre captures
  1.0329575907 exactly, in 9,296.0 CPU-seconds at two threads (21:27 to 22:50Z, 4,992.5
  s of wall). `devtools.fine_net_followup capture-agreement` finds every direction equal
  to the source’s check2 log in verdict, nodes, leaves, depth, least bound and the axis
  vertices and argmin (the packet’s `receipts/capture-agreement-n29.json`).
- `mixed_n29_L582.control.json`, the whole-net control receipt
  (`sqverify-fast-control/v2`, `CONTROLS_REFUSED`, 22:53 to 23:07Z, 854 s of wall at two
  threads): the original verified again at direction 1947, the 99/100 mutant refused at
  all 2,073 directions, each a coverage refusal at an in-domain pose whose capture,
  evaluated apart from the crate, is below 1, and the near-threshold mutant (every mass
  scaled by 2420232468913/2500000000000) refused as a counterexample candidate.
  At the axis direction #892’s enclosure rule judges the refusal: the mutant’s exact
  capture at the sweep’s least vertex, 0.99086435438, lies in
  [0.9908643538541804, 0.9908643548997059], an enclosure 1.05e-9 wide whose lower end is
  the crate’s bound to the bit, 5.23e-10 above that bound and so near the enclosure’s
  midpoint, as F-8 of the review expected.
  #892 adopted that rule for the census, and #543’s question to the owner on the axis
  tolerance is still open; the gap is also inside the former constant allowance of 1e-9,
  so the control passes under either rule.
  The receipt records wall time only, so the control’s CPU is at most 1,708 seconds.

Both runs used `sqverify-fast` built from the reviewed crate source `d97758bb…` (binary
`567a0fd5…`, rustc 1.98.0, release, x86_64-unknown-linux-gnu), rebuilt for this run byte
for byte, at two threads under `nice -n 19` on a shared four-core host.
The
[mathematical review of 4 November](../../../../../docs/project/reviews/review-2026-11-04-wand125-fine-net-n29.md)
read the certificate before either run was mapped.
On 4 November 2026 this census, its controls and the stage 4 review ran ahead of the
owner’s order of 11 October, which queued the replay after the regularization of every
packing (think-ux1v); the owner has not lifted that order, and the adoption is pending
the owner’s decision on it (#909, think-r333). This README is a hand-maintained index of
the folder, not a generated view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
