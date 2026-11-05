# The n94 Second Dilation Census: mixed_n94_L9972

This folder retains the native receipts of the complete replay of Doğa Özden’s
`certificate/n94-L9972.json.gz` (issue #910), named `mixed_n94_L9972` here by the format
M convention, from the
[5 November packet](../../../../resources/web/ozden-s94-lower-bound-9972-2026-11-05/README.md),
on 5 November 2026, and of its whole-net controls.
Its census row is in [`census.json`](../census.json), and the
[Milestone B census](../README.md), which
`python -m devtools.sqverify_fast_census --family mixed --report` regenerates, shows it
beside every other mixed certificate.

The folder keeps:

- `mixed_n94_L9972.jsonl.gz`, the capture: one row for each of the 4,972 directions of
  the net the certificate declares, and a summary.
  Every direction verified, 2,462,923,881 nodes in all, least leaf bound
  1.0000000000003892 at direction 3663, where the exact capture at the leaf’s centre is
  1.0336. It took 59,956 CPU-seconds at two threads, 09:50 to 18:25Z, with another lane
  sharing the host for part of the run.

- `mixed_n94_L9972.control.json`, the whole-net control receipt
  (`sqverify-fast-control/v2`), status `CONTROLS_REFUSED` (18:25 to 18:36Z):
  - The original verified again at direction 3663.
  - The 99/100 mutant was refused at all 4,972 directions.
    Each refusal is a coverage refusal at an in-domain pose whose capture, evaluated
    apart from the crate, is below 1, and where the original captures at least 1.
  - The near-threshold mutant was refused.

  At the axis the census judges the refusal by the enclosure the vertex sweep held at
  its least vertex, which it recomputes and ties to the crate’s bound to the bit
  (`axis_captures_agree`, #892). The 99/100 mutant’s exact capture there,
  0.993055981881054, lies in [0.9930559807565953, 0.9930559830055209]. The crate’s bound
  sits $1.1245 \times 10^{-9}$ below that capture, beyond the old constant of $10^{-9}$,
  which is F7 of the stage 4 review.

Both runs used `sqverify-fast` built from the reviewed crate source `d97758bb…` (binary
`567a0fd5…`, rustc 1.98.0, release, x86_64-unknown-linux-gnu), under `nice -n 19` on a
shared four-core host.
The author ran the same checker, unmodified, so the capture is reproduced with the
producer’s code. `devtools.audit_dilated_measure compare` holds it to the author’s
selected archive line at every direction, on every field the line keeps, and finds them
equal, with equal node totals (the packet’s `receipts/replay-comparison.json`). On a
declared net the census route carries only beside a passing control receipt and a review
that has read the certificate’s mathematics.
The stage 4 review of 5 November did read it, and accepted it.
With both, the row is `E-ozden-910-n94-9972-sqverify-fast-replay`, the evidence for
T-266 at V3/C3. This README is a hand-maintained index of the folder, not a generated
view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
