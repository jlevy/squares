# Maintained Replay Plan for #1052 at 305

This plan was written on 21 November 2026 UTC before the maintained import replay.
The independent review in #1057 had already finished.
It retains its own frozen controls and results.
The interrupted import lane recorded a hash for its earlier plan.
The takeover recovered no copy of that plan.

Read the primary certificate at JoostdeWinter/square-packing
db8efcb6bf05906e977bc62f1f6d8ccfcaa296ef with the `center-direction-json` adapter.
Its SHA-256 is `e6c7d0280396a2fa61804a24a7c757365320869dbb89e8cf94316bb8b6a7831f`. Check
that the exact side’s 12-place ceiling is 17.945755838742.

- The maintained rational pose and independent corner routes must accept 305 unit
  squares in the stated box and all 46,360 distinct square pairs.
- Both routes must refuse the duplicate-square and outside-container controls.
- Run the maintained sharp controls using the packet’s primary input.
  Each wall or pair control must give its specified verdict at contact and after a
  displacement of $10^{-30}$. The enlarged-square controls must detect non-unit shape
  and report the specified pair or wall witness after the crossing.
- Record every mismatch or timeout as a failed replay and keep the replay receipt.
  Cap each maintained job at 600 seconds.
  Use one worker on a host under the memory guard.

Use the previously accepted stage 4 review and its identity and contraction receipts for
the independence and arrangement comparison.
The maintained replay answers whether the admitted packet still gives the expected exact
verdicts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
