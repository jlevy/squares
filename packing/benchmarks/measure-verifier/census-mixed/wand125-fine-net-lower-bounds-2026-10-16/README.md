# Accepted Mac Checkpoints: n68, n84 and n85

This folder retains the native receipts of the 16 October 2026 fine-net packet’s
certificates that this repository has decided completely.
Three of them, `mixed_n68_L853` (T-205), `mixed_n84_L94225` (T-206) and
`mixed_n85_L9475` (T-207), are the Mac checkpoints accepted on 19 October 2026. The
fourth, `mixed_n108_L1062` (T-216), is the Linux replay of 18 October 2026. Their census
rows are in [`census.json`](../census.json), and the [Milestone B census](../README.md),
which `python -m devtools.sqverify_fast_census --family mixed --report` regenerates,
shows them beside every other mixed certificate.

For each certificate the folder keeps:

- `CERT.jsonl.gz`, the capture: one row for each of the 201 directions of the net the
  candidate declares, and a summary.
- `CERT.control.json`, the whole-net control receipt (`sqverify-fast-control/v2`).
- `CERT.execution.json`, for the three Mac checkpoints only: the checkpoint’s authentic
  execution record of commands, exits and aggregate driver timing, which is separate
  from the census row’s `wait4` CPU. The n68 record keeps the capture’s unobserved outer
  exit beside the recovered native exit, zero.

The Mac checkpoints’ per-command logs and timing files, exact audits and platform
evidence are in
[`review-mac`](../../../../resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/README.md).
This README is a hand-maintained index of the folder, not a generated view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
