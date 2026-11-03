# The n94 Dilation Census: mixed_n94_L9965

This folder retains the native receipts of the complete replay of Doğa Özden’s
`certificate/n94_L9965.json.gz` (issue #890), named `mixed_n94_L9965` here by the format
M convention, from the
[3 November packet](../../../../resources/web/ozden-s94-lower-bound-2026-11-03/README.md),
on 3 November 2026. Its census row is in [`census.json`](../census.json), and the
[Milestone B census](../README.md), which
`python -m devtools.sqverify_fast_census --family mixed --report` regenerates, shows it
beside every other mixed certificate.

The folder keeps:

- `mixed_n94_L9965.jsonl.gz`, the capture: one row for each of the 600 directions of the
  net the certificate declares, and a summary.
  Every direction verified, 296,805,699 nodes in all, least certified bound
  1.0000000000314393 at direction 277, in 8,138.6 CPU-seconds at two threads (02:01 to
  03:10Z).
- `mixed_n94_L9965.control-failed-v2.json`, the whole-net control receipt
  (`sqverify-fast-control/v2`), kept as it failed closed (03:12 to 03:14Z): the original
  verified again at direction 277; the 99/100 mutant refused at all 600 directions, each
  a coverage refusal at an in-domain pose whose capture, evaluated apart from the crate,
  is below 1; and the near-threshold mutant refused.
  It fails only on the axis rule: the 99/100 mutant’s exact capture at the vertex
  sweep’s least vertex sits 1.12e-9 above the sweep’s certified bound, beyond the
  constant `AXIS_ROUNDING` of 1e-9 (F-1 of the 14 October review; think-4uun owns the
  fix).

Both runs used `sqverify-fast` built from the reviewed crate source `d97758bb…` (binary
`567a0fd5…`, rustc 1.98.0, release, x86_64-unknown-linux-gnu), under `nice -n 19` on a
shared four-core host.
The author ran the same checker, unmodified, so the capture reproduces the author’s run
with the producer’s code; `devtools.audit_dilated_measure compare` holds it to the
author’s two receipts direction by direction (the packet’s
`receipts/replay-comparison.json`). No evidence entry cites the row yet: on a declared
net the census route carries only beside a passing control receipt and a review that has
read the certificate’s mathematics (think-222u). This README is a hand-maintained index
of the folder, not a generated view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
