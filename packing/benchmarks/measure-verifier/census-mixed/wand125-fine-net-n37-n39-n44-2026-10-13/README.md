# The n37 and n39 Fine-Net Censuses

This folder retains the native receipts of the complete replays of `mixed_n37_L64975`
(T-178) and `mixed_n39_L66625` (T-176), the n37 and n39 certificates of the
[13 October fine-net packet](../../../../resources/web/wand125-fine-net-n37-n39-n44-2026-10-13/README.md),
on 2 November 2026. Their census rows are in [`census.json`](../census.json), and the
[Milestone B census](../README.md), which
`python -m devtools.sqverify_fast_census --family mixed --report` regenerates, shows
them beside every other mixed certificate.

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
- `mixed_n39_L66625.jsonl.gz`, the n39 capture: every one of the 2,073 directions
  verified, 881,271,470 nodes in all, least certified bound 1.0000000000654117 at
  direction 1804, in 11,404.3 CPU-seconds at two threads (19:05 to 20:41Z).
  `devtools.fine_net_followup capture-agreement` finds every direction equal to the
  source’s check2 log (the packet’s `receipts/capture-agreement-n39.json`, beside
  n37’s).
- `mixed_n39_L66625.control-failed-v2.json`, the n39 whole-net control receipt, which
  failed closed (`CONTROL_FAILED`, 20:42 to 20:49Z) and is kept outside the receipts the
  census tests hold to `CONTROLS_REFUSED`, as n26’s and n96’s are.
  The original verified again at 1804, the 99/100 mutant was refused at all 2,073
  directions and the near-threshold mutant was refused; 2,072 of the refusals pass every
  predicate, and at the axis direction the mutant’s exact capture, below 1 at an
  in-domain pose, sits 1.26e-9 above the vertex sweep’s certified bound, beyond the
  census’s constant `AXIS_ROUNDING` of 1e-9 (F-1 of the 14 October review).
  think-tcsl owns the fix; its receipt, once the allowance is judged against the sweep’s
  enclosure, is to be written as `mixed_n39_L66625.control.json` beside this one.

All four runs used `sqverify-fast` built from the reviewed crate source `d97758bb…`
(binary `567a0fd5…`, rustc 1.98.0, release, x86_64-unknown-linux-gnu), under
`nice -n 19` on a shared four-core host.
The packet’s n44 certificate is not retained, so it has no row here.
This README is a hand-maintained index of the folder, not a generated view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
