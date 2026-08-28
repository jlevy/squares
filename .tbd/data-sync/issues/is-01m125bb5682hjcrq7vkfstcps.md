---
type: is
id: is-01m125bb5682hjcrq7vkfstcps
title: Regenerate the n=29 rational certificate at a tighter rational_digits
kind: task
status: closed
priority: 2
version: 2
labels:
  - packing
dependencies: []
created_at: 2026-08-27T17:47:40.575Z
updated_at: 2026-08-28T01:36:55.509Z
closed_at: 2026-08-28T01:36:55.508Z
close_reason: "BC-039 complete. Regenerated at rational_digits 36, the CLI default; relaxation 4.933898e-11 -> 4.933884e-31. Argued reason is that n-029.md described the artifact as the output of 'the generic promotion command' without naming the non-default flag; the tighter bound is a side effect. Corrected an earlier overstatement: the artifact was properly pinned by test_witness_contract and was never irreproducible."
resolution: null
duplicate_of: null
---
Q-BC032-a (session 029, phase 3) established that the 4.94e-11 side relaxation in E-n029-schadt-rational-upper is an artifact of the promotion route, not a property of the Schadt pose.

The recorded witness carries rational_digits: 16 and center_dilation: 100000000001/100000000000. promote_rational walks a dilation ladder whose first rung is 1 + 10^-(rational_digits - 5), and the achieved relaxation tracks that rung exactly. Measured, each independently verified by devtools.check_rational_witness_independent over 29 squares and 406 pairs:

  d=18 -> 4.933899e-13
  d=24 -> 4.933965e-19
  d=30 -> 4.933868e-25
  d=36 -> 4.933884e-31
  d=48 -> 4.933849e-43
  d=60 -> 4.933851e-55

All six are strictly smaller than the recorded 4.9339e-11.

Scope: regenerate witnesses/schadt-n029-2025-rational.yaml at a chosen rational_digits, update its certificate metadata (rational_digits, center_dilation), update the E-n029-schadt-rational-upper limitations text which currently states 'about 4.94e-11 larger than the source decimal', and confirm the full gate stays green (the witness is checked by two independent paths in packing-validate).

Choose the value deliberately: this route has no minimum, so the relaxation shrinks without bound as rational_digits rises. The tradeoff is literal size, since the corner rationals grow with d. Record the reason for whatever value is chosen.

Claim boundary is unchanged and must stay unchanged: this remains an upper bound at a relaxed rational side, weaker than the reported record. It does not certify the source decimals, improve a record, establish rigidity, or prove optimality.
