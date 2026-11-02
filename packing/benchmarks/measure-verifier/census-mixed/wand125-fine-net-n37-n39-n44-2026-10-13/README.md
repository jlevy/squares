# The n37 Fine-Net Census: mixed_n37_L64975

This folder retains the native receipts of the complete replay of `mixed_n37_L64975`
(T-178), the n37 certificate of the
[13 October fine-net packet](../../../../resources/web/wand125-fine-net-n37-n39-n44-2026-10-13/README.md),
on 2 November 2026. Its census row is in [`census.json`](../census.json), and the
[Milestone B census](../README.md), which
`python -m devtools.sqverify_fast_census --family mixed --report` regenerates, shows it
beside every other mixed certificate.

The folder keeps:

- `mixed_n37_L64975.jsonl.gz`, the capture: one row for each of the 2,073 directions of
  the net the candidate declares, and a summary.
  Every direction verified, 864,953,550 nodes in all (the source’s check2 total, and its
  node count and least bound at every direction), least certified bound
  1.0000000000165958 at direction 1919, in 12,667.7 CPU-seconds at two threads (11:25 to
  13:23Z).
- `mixed_n37_L64975.control.json`, the whole-net control receipt
  (`sqverify-fast-control/v2`, `CONTROLS_REFUSED`): the original verified again at
  direction 1919, the 99/100 mutant refused at all 2,073 directions, each a coverage
  refusal at an in-domain pose whose capture, evaluated apart from the crate, is below
  1, and the near-threshold mutant refused (13:23 to 13:33Z).

Both runs used `sqverify-fast` built from the reviewed crate source `d97758bb…` (binary
`567a0fd5…`, rustc 1.98.0, release, x86_64-unknown-linux-gnu), under `nice -n 19` on a
shared four-core host.
The packet’s n39 and n44 certificates are not retained, so they have no rows here.
This README is a hand-maintained index of the folder, not a generated view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
