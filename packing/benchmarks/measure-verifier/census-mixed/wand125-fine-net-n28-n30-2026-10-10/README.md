# T-142’s and T-143’s Fine-Net Censuses: n28 and n30

This folder retains the native receipts of the complete replays of `mixed_n28_L57425`
(T-142) and `mixed_n30_L58925` (T-143), the certificates of the
[10 October n28 and n30 packet](../../../../resources/web/wand125-fine-net-n28-n30-2026-10-10/README.md),
run on 4 November 2026 one count at a time, after the
[stage 4 review of that day](../../../../../docs/project/reviews/review-2026-11-04-wand125-fine-net-n28-n30.md)
(think-4ul6) had read both.
Their census rows are in [`census.json`](../census.json), and the
[Milestone B census](../README.md), which
`python -m devtools.sqverify_fast_census --family mixed --report` regenerates, shows
them beside every other mixed certificate.

For each certificate the folder keeps `CERT.jsonl.gz`, the capture (one row for each of
the 2,073 directions of the net the candidate declares, and a summary), and
`CERT.control.json`, the whole-net control receipt (`sqverify-fast-control/v2`).

| Certificate | Capture | Nodes (equal to the source’s) | Least certified bound, at direction | CPU s | Control |
| --- | --- | ---: | --- | ---: | --- |
| `mixed_n28_L57425` | VERIFIED, 2,073 directions | 594,284,796 | 1.0000000000106595, 1088 | 7,096.9 | `CONTROLS_REFUSED` |
| `mixed_n30_L58925` | VERIFIED, 2,073 directions | 702,952,674 | 1.000000000029295, 1585 | 10,667.1 | `CONTROLS_REFUSED` |

`devtools.fine_net_followup capture-agreement` finds every direction’s node count and
least certified bound equal to the source’s check2 log (the packet’s
`receipts/capture-agreement-n28.json` and `capture-agreement-n30.json`). The captures
ran from 18:38Z to 19:39Z (n28, 3,644 s of wall) and from 19:39Z to 21:15Z (n30, 5,784
s), and the controls after them: n28’s from 21:15Z to 21:26Z (675 s of wall and 1,111
CPU-seconds), n30’s from 21:26Z to 21:36Z (597 s and 985 CPU-seconds).
Each control verified the original again at its least-bound direction, refused the
99/100 mutant at all 2,073 directions, each a coverage refusal at an in-domain pose
whose capture, evaluated apart from the crate, is below 1, and refused the
near-threshold mutant.

**The axis legs, by the enclosure rule.** Since #892 (think-4uun) the census judges an
axis refusal by the enclosure the vertex sweep held at its least vertex, recomputed
apart from the crate: its lower end must be the crate’s bound to the bit, and the exact
capture must lie inside it.
At n28 the 99/100 mutant’s capture, $0.99140000844$, lies in
$[0.9914000062838418, 0.991400010590911]$, $2.15 \times 10^{-9}$ above the certified
bound, the gap the review measured (its F-7); under the census’s former constant
`AXIS_ROUNDING` of $10^{-9}$ this control would have failed closed, as n26’s and n39’s
did. At n30 the capture, $0.99173535469$, lies in
$[0.9917353545019875, 0.9917353548785199]$, $1.88 \times 10^{-10}$ above the bound,
inside either rule.

All runs used `sqverify-fast` built from the reviewed crate source `d97758bb…` (binary
`567a0fd5…`, rustc 1.98.0, release, x86_64-unknown-linux-gnu), at two threads under
`nice -n 19` on a shared four-core host, from #903’s head `bdb744251`, into a working
directory of the lane’s own; the receipts were copied here unchanged.
T-142 and T-143 are `V3/C3` on these receipts.
This README is a hand-maintained index of the folder, not a generated view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
