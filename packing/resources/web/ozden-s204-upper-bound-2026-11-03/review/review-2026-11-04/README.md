# Stage 4 Review of #894: Receipts at 204

These are the 204 receipts of the stage 4 mathematical review of Doğa Özden’s
certificates for $s(299)$ ([#893](https://github.com/jlevy/squares/issues/893)) and
$s(204)$ ([#894](https://github.com/jlevy/squares/issues/894)), dated 4 November 2026
(bead `think-ybep`). The review is
[review-2026-11-04-ozden-893-894-299-204.md](../../../../../../docs/project/reviews/review-2026-11-04-ozden-893-894-299-204.md).

The programs that wrote them serve both packets and are kept once, in the
[ozden-s299-upper-bound-2026-11-03](../../../ozden-s299-upper-bound-2026-11-03/review/review-2026-11-04/README.md)
packet’s `review/review-2026-11-04/`, whose README says what each program does, what it
read, how to run it and what it printed. So are the receipts that cover both counts:
`selftest.json`, `sides.json` and `custody.json`.

| Receipt | Program | Verdict |
| --- | --- | --- |
| [out/check-n204.json](out/check-n204.json) | `oz_check.py`, the deciding program | `ACCEPT`: 204 squares, every basis exactly unit, every wall and all 20,706 pairs decided by both methods; least wall clearance $9.9999999995 \times 10^{-18}$ (square 39, bottom), least pair margin $9.99999978848 \times 10^{-18}$ (squares 23 and 39) |
| [out/controls-n204.json](out/controls-n204.json) | `oz_controls.py` | `EVERY_CONTROL_AS_EXPECTED`: all 16 controls, the 391 near pairs and the 204 squares taken to contact and $10^{-30}$ past it |
| [out/identity-n204.json](out/identity-n204.json) | `oz_identity.py`, a measurement | one to one with T-257’s packing under the identity only, every square keeping its id; 6 squares beyond 0.1 (largest 0.18968); 14 turned beyond 1° (largest 25.58°); 87 turned beyond $10^{-6}$ radians |
| [out/compare-lane-n204.json](out/compare-lane-n204.json) | `oz_compare_lane.py`, a comparison | the maintained routes’ poses are the certificate’s squares exactly, and their minima and the lane’s identity counts equal this review’s |

Each receipt records the SHA-256 of the program that wrote it and of `ozlib.py`, which
equal the bytes the s299 packet retains.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
