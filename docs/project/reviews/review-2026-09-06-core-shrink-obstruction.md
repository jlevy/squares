# Independent Review of the Fixed-Weight Core-Shrink Obstruction

Disposition: **accepted at the ordinary-containment scope**. The reviewed transport is
`96ff47516c827621334c51a8c8ba54ab21d09527`, authored by `/root/endpoint_epsilon_spike`
and independently reviewed by `/root/core_shrink_reviewer` at `max` reasoning.
The coordinator retained this review after the reviewer returned its terminal report on
2026-09-06.

The reviewed
[exp-111 packet](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-111-h-091-core-shrink.md)
excludes every smaller core that could improve T-022 using ordinary containment while
keeping T-018’s sites, direction net, and relative weights.
This is a bounded method obstruction; it changes no registered packing bound.

## Mathematical Checks

The reviewer independently reconstructed direction 97 from `t = 97*(207107/90000000)`
and recomputed the inclusion spectrum directly from all 1,121 frozen atoms.
All 1,118 events and the retained center agree.
The first event exceeding the usable mass `434547/440000` is
`1696802860582378979/1700716629721128200`. The mass immediately below it is
`96377/100000`, and the center remains admissible through the event.

The exact positive square difference in exp-111 also agrees.
An ordinary-containment improvement requires `b < B/sqrt(1+D^2)`, which is below that
event. Nonnegative weights make the same placement a low-mass witness throughout the
improvement window. A common rescaling of those weights cannot repair the contradiction
criterion.

The remaining refined-containment interval is not excluded: its width is
`106044519531307/85035831486056410000`, approximately `1.24705689e-6` in core side.
The prospective target `b=997699/1000000`, `q=400003/400000` satisfies the refined
containment and improvement comparisons, conditional on exact coverage.
It was not measured in this review.
`think-xsma` owns that distinct test.

## Provenance and Validation

Both hypotheses precede their measurements, the retained tool digests match the named
clean commits, and the rejected verdicts apply the original strict mass threshold.
No candidate certificate was emitted by either failed experiment.

The reviewer identified one integration requirement: preserve the original commit
ancestry. Exp-110 pins `48a161ba`, and exp-111 pins `aeb683d5`; the campaign gate checks
that an experiment’s engine commit is an ancestor of the integrated head.
The coordinator therefore merged the transport in `f9ba790a` instead of copying its
commits onto new identities.

Using Python 3.14.7 against the isolated source tree, the reviewer ran the reusable
`devtools.core_shrink --inspect-witness` check, seven focused tests, the ledger check,
the synopsis check, schema validation, Ruff, and BasedPyright.
All passed; the type checker reported zero errors and warnings.
The reviewer made no file changes and ran no new sweep.
The coordinator separately reproduced the witness and exact square difference.
Validation of the integrated branch is recorded in the recovery checkpoint.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
