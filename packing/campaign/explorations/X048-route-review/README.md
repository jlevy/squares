# X-048 Route Review: Exploratory Receipts

Two Fable reviewers at extra-high effort wrote fourteen exploratory scripts while
assessing the merged PR 265 record for the
[n17 route review](../../../../docs/project/reviews/review-2026-10-01-n17-route-after-pr265.md).
This directory keeps the scripts’ outputs, re-run under the project interpreter, and
says what each script computed, so the next agent can see where every exploratory number
in the review came from.

The outputs are **planning evidence, not admitted results**. No number here enters a
hypothesis verdict until an instrument with controls and independent review reproduces
it (OR-1).

## Where the Sources Are

The scripts follow the convention of earlier planning probes and stay outside the
record, in the ignored `attic/n17-route-review/` of the session checkout; the owner also
received them as an archive.
They are not committed because the lint floor admits no unlinted Python inside
`packing/`, and its exclusion list lives in `packing/pyproject.toml`, which the n11
native audit pins byte for byte to its proof commit.
Each one uses only the standard library and runs from its own directory with the project
interpreter. The lanes that need them rebuild the computation as an admitted instrument:
BC-402 and BC-407 for the endpoint lane, BC-408 for the census.

## Endpoint Lane (Exact Rational Arithmetic Unless Noted)

| Script | What it computes | Feeds |
| --- | --- | --- |
| `endpoint/n17_endpoint.py` | Exact reconstruction of the H254 chart at the H255 root midpoint with H256 centroid sliders, and an independent packing and contact-feature check | H257 inventory reproduction |
| `endpoint/n17_firstorder.py` | The 58-row, 52-column first-order model and its finite-difference control | Everything below |
| `endpoint/n17_stress.py` | The H258 stress: the exact identity $A^\top\lambda=Ke_\sigma$, all 58 weight signs, the oblique moment capacities, and the rank and kernel of the positive rows | H-258, H-261 |
| `endpoint/n17_more.py` | The identity at three unrelated rational points; floating-point LP duals for the 90 signed non-slider coordinates; margins of the 135 unavailable owner options | H-261 |
| `endpoint/n17_radius.py` | Floating-point estimate of the n11-style focused-rectangle radius modulo sliders | H-261 radius estimate |
| `endpoint/n17_radius2.py` | Residual audit of the radius script’s duals | The ten duals to redo exactly |

## Route Lane (Floating Point Unless Noted)

| Script | What it computes | Feeds |
| --- | --- | --- |
| `route/endpoint.py` | Floating-point endpoint reconstruction, derivative signs on the frozen and extended boxes, cell and slider geometry | Scope of the conditional minimum; the seam finding |
| `route/derivs.py` | Monotonicity signs on extended boxes, the $W_{15}$ and $W_{17}$ support bounds over all orientations, and a global scan of the necessary system | Scope of the conditional minimum |
| `route/globalscan.py` | A finer global scan of $S_{\min}(\theta,\beta)$ | The minimum over common orientations |
| `route/stress.py` | A double-precision check of the H258 stress | H-258 (second reconstruction) |
| `route/nullspace.py` | The six slider directions in the kernel of the positive rows; weight extremes | H-261 |
| `route/census.py` | Exact H259 and H260 counts by Burnside, and survivor counts under subcontainer cuts (exact integers) | H-262 |
| `route/wallrow.py` | Least tangential spacing of two squares in a wall layer | Refutes a four-per-row cut |
| `route/rowdp.py` | A consecutive-pair bound on five squares in one boundary row | Refutes a four-per-row cut |

In `route/census.py`, only the 3 × 3 block cap of nine and the 2 × 2 block cap of five
follow from settled cases.
The cap of four per boundary row that the script also counts is not established;
`route/wallrow.py` and `route/rowdp.py` show why.
Its orbit figures divide state counts by eight and are approximate.

## Receipts

`receipts/` holds each script’s output from the re-run on 2026-10-01 under Python
3.14.7, and `receipts/run-summary.txt` holds the exit status and wall time of each.
All fourteen exited 0. The census took 1,068 seconds; every other script took under 35
seconds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
