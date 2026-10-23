# T-233’s Fine-Net Censuses: Four #446 Certificates

This folder retains the native receipts of the complete replays of the four certificates
T-233 registers, from the
[release packet](../../../../resources/web/wand125-fine-net-lower-bounds-446-release-2026-10-08/README.md),
run on 23 October 2026 one count at a time.
Their census rows are in [`census.json`](../census.json), and the
[Milestone B census](../README.md), which
`python -m devtools.sqverify_fast_census --family mixed --report` regenerates, shows
them beside every other mixed certificate.

For each certificate the folder keeps `CERT.jsonl.gz`, the capture (one row for each of
the 2,073 directions of the net the candidate declares, and a summary), and
`CERT.control.json`, the whole-net control receipt (`sqverify-fast-control/v2`). The n26
receipt, which failed closed, is kept as `mixed_n26_L5555.control-failed-v2.json`,
outside the receipts the census’s tests hold to `CONTROLS_REFUSED`, as
`mixed_n96_L997.control-failed-v1.json` was before it.

| Certificate | Capture | Nodes (equal to the source’s) | Least certified bound | CPU s | Control |
| --- | --- | ---: | --- | ---: | --- |
| `mixed_n19_L48275` | VERIFIED, 2,073 directions | 377,472,588 | 1.0000000001405505 | 2,539.7 | `CONTROLS_REFUSED` |
| `mixed_n20_L49125` | VERIFIED, 2,073 directions | 410,012,470 | 1.0000000001231197 | 5,987.4 | `CONTROLS_REFUSED` |
| `mixed_n26_L5555` | VERIFIED, 2,073 directions | 663,387,112 | 1.0000000000340534 | 6,115.2 | `CONTROL_FAILED`, on the axis tolerance only (`mixed_n26_L5555.control-failed-v2.json`) |
| `mixed_n27_L5655` | VERIFIED, 2,073 directions | 648,972,154 | 1.0000000000149065 | 9,257.6 | `CONTROLS_REFUSED` |

**The n26 control fails closed on a tolerance, not on a refusal.** The 99/100 mutant was
refused at all 2,073 directions, and each of the 2,072 oblique refusals passes every
predicate. At the axis direction the mutant’s exact capture at the vertex sweep’s least
vertex, $0.99098078325$, is below 1 at a pose in the per-bin domain.
It sits $3.28 \times 10^{-9}$ above the sweep’s certified bound, beyond the census’s
constant allowance `AXIS_ROUNDING` of $10^{-9}$, so `captures_agree` is false there and
the receipt’s status is `CONTROL_FAILED`. The 14 October review’s finding F-1 says the
allowance should come from the sweep’s enclosure, which varies by certificate (n28 at
$2.15 \times 10^{-9}$, n39 at $1.26 \times 10^{-9}$). The fix is a change of control
logic that needs a review, owned by think-tcsl; until it lands, n26 has no accepted
control receipt and T-233 stays below `C3`.

All runs used `sqverify-fast` built from the reviewed crate source `d97758bb…` (binary
`567a0fd5…`, rustc 1.98.0, release, x86_64-unknown-linux-gnu), at two threads under
`nice -n 19` on a shared four-core host.
This README is a hand-maintained index of the folder, not a generated view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
