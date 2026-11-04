# The n94 Dilation Census: mixed_n94_L9965

This folder retains the native receipts of the complete replay of Doğa Özden’s
`certificate/n94_L9965.json.gz` (issue #890), named `mixed_n94_L9965` here by the format
M convention, from the
[3 November packet](../../../../resources/web/ozden-s94-lower-bound-2026-11-03/README.md),
on 3 November 2026, and of its whole-net controls.
Its census row is in [`census.json`](../census.json), and the
[Milestone B census](../README.md), which
`python -m devtools.sqverify_fast_census --family mixed --report` regenerates, shows it
beside every other mixed certificate.

The folder keeps:

- `mixed_n94_L9965.jsonl.gz`, the capture: one row for each of the 600 directions of the
  net the certificate declares, and a summary.
  Every direction verified, 296,805,699 nodes in all, least certified bound
  1.0000000000314393 at direction 277, in 8,138.6 CPU-seconds at two threads (02:01 to
  03:10Z).
- `mixed_n94_L9965.control.json`, the whole-net control receipt
  (`sqverify-fast-control/v2`), status `CONTROLS_REFUSED` (4 November, 07:35 to 07:38Z):
  the original verified again at direction 277; the 99/100 mutant refused at all 600
  directions, each a coverage refusal at an in-domain pose whose capture, evaluated
  apart from the crate, is below 1; and the near-threshold mutant refused.
  At the axis the census judges the refusal by the enclosure the vertex sweep held at
  its least vertex, which it recomputes and ties to the crate’s bound to the bit
  (`axis_captures_agree`, #892): the 99/100 mutant’s exact capture there lies in
  [0.9930860126842824, 0.9930860149308234].
- `mixed_n94_L9965.control-failed-v2.json`, the first control receipt (3 November, 03:12
  to 03:14Z), kept as it failed closed.
  It records the same runs and refusals, but the census then held the axis refusal to a
  constant: the exact capture at the least vertex sits 1.12e-9 above the sweep’s
  certified bound, beyond the `AXIS_ROUNDING` of 1e-9 that the enclosure rule replaced
  (F-1 of the 14 October review; think-4uun).

All three runs used `sqverify-fast` built from the reviewed crate source `d97758bb…`
(binary `567a0fd5…`, rustc 1.98.0, release, x86_64-unknown-linux-gnu), under
`nice -n 19` on a shared four-core host.
The author ran the same checker, unmodified, so the capture is reproduced with the
producer’s code; `devtools.audit_dilated_measure compare` holds it to the author’s two
receipts direction by direction (the packet’s `receipts/replay-comparison.json`). On a
declared net the census route carries only beside a passing control receipt and a review
that has read the certificate’s mathematics, which the stage 4 review of 3 November did,
accepting it; with both, the row is `E-ozden-890-n94-9965-sqverify-fast-replay`, the
evidence for T-262 at V3/C3. This README is a hand-maintained index of the folder, not a
generated view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
