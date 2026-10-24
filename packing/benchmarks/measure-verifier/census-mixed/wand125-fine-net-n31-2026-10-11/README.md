# The n31 Fine-Net Census: mixed_n31_L59775

This folder retains the native receipts of the complete replay of `mixed_n31_L59775`
(T-232), the n31 certificate of the
[11 October fine-net packet](../../../../resources/web/wand125-fine-net-n31-2026-10-11/README.md),
on 23 October 2026. Its census row is in [`census.json`](../census.json), and the
[Milestone B census](../README.md), which
`python -m devtools.sqverify_fast_census --family mixed --report` regenerates, shows it
beside every other mixed certificate.

The folder keeps:

- `mixed_n31_L59775.jsonl.gz`, the capture: one row for each of the 2,073 directions of
  the net the candidate declares, and a summary.
  Every direction verified, 787,004,724 nodes in all (the source’s check2 total), least
  certified bound 1.000000000022577 at direction 676, in 14,607.6 CPU-seconds at two
  threads (06:39 to 11:01Z).
- `mixed_n31_L59775.control.json`, the whole-net control receipt
  (`sqverify-fast-control/v2`, `CONTROLS_REFUSED`): the original verified again at
  direction 676, the 99/100 mutant refused at all 2,073 directions, each a coverage
  refusal at an in-domain pose whose capture, evaluated apart from the crate, is below
  1, and the near-threshold mutant refused (11:02 to 11:09Z).

Both runs used `sqverify-fast` built from the reviewed crate source `d97758bb…` (binary
`567a0fd5…`, rustc 1.98.0, release, x86_64-unknown-linux-gnu), under `nice -n 19` on a
shared four-core host.
This README is a hand-maintained index of the folder, not a generated view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
