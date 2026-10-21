# Review Programs, 21 October 2026

These are the programs that the stage 4 review lane of the 21 October intake (PR #708)
wrote and ran for
[`review-2026-10-21-upper-bound-import-703.md`](../../../../../../docs/project/reviews/review-2026-10-21-upper-bound-import-703.md),
the review of Evan Daniel’s #703 certificate at 270, with what they printed.
The lane was an AI agent (Claude, strong sub-agent tier, max reasoning), prompted
separately from the import and records lanes.
It wrote the programs here and ran them on 21 October 2026, from 02:48Z to 02:54Z, in a
worktree at `0a86f70c3`, the head of `claude/intake-2026-10-21-evand-270`, from
`packing/` with the project interpreter (Python 3.14.7), niced.
The records lane moved them here from the lane’s `review708/` directory: the programs
and the small outputs byte for byte, the two largest JSON outputs compressed with `xz`
(`xz -dc` gives the original bytes), and the lane’s four `*.time` files joined in
`outputs/timings.txt`. The decompressed receipt and the upstream copies the lane had
beside them are left out, since the packet keeps both.

| Certificate | Packet | Entry | n |
| --- | --- | --- | --- |
| #703, `s270_sw.cert` | `evand-n270-sweep-2026-10-20` | T-224 on the records branch | 270 |

T-224 is the number the records lane gave the result on its branch; numbers are assigned
in merge order and may change.

## What Decides What, and What Is Registered

Two programs here decide certificates.
`review_708_check.py` is this review’s own exact route: written for it, standard library
only, importing nothing from this repository.
`sharp_controls_708.py` makes mutants of the certificate at the scale of its margins and
passes each through the `evand-cert` adapter to both maintained routes, which decide
them; it adds nothing to those routes and changes no decision.
No evidence entry cites any of these runs as a verifier, and neither program is in a
[`verifiers.yaml`](../../../../../frontier/verifiers.yaml) entry.
The confirming evidence of T-224 rests on the maintained replay, the import lane’s
retained receipt (`receipts/exact-certification.json.xz` in this packet), which the
review reproduced on both routes; these files are the review’s record of what else it
ran, as the
[20 October review](../../../evand-n308-2026-10-19/review/review-2026-10-20/README.md)
kept its own.
`construction_708.py`, `margins_708.py` and `lineage_708.py` measure or compare, and
decide nothing.

## Programs

Run each one from `packing/` with the project interpreter.
`P` is this directory’s `programs/`, `O` an output directory, and `RECEIPT` the packet’s
receipt decompressed:

```sh
P=resources/web/evand-n270-sweep-2026-10-20/review/review-2026-10-21/programs
C=resources/web/evand-n270-sweep-2026-10-20/source/search/packer/candidates
A=resources/web/evand-n270-sweep-2026-10-20/acquisition
xz -dc resources/web/evand-n270-sweep-2026-10-20/receipts/exact-certification.json.xz > RECEIPT
.venv/bin/python3 -I $P/review_708_check.py $C/s270_sw.cert 270 O/out-check.json RECEIPT
.venv/bin/python3 -I $P/review_708_check.py $C/s270_sw_regularized.cert 270 O/out-check-view.json
.venv/bin/python3 -I $P/sharp_controls_708.py $P $C/s270_sw.cert 270   # writes $P/out-controls-n270.json
.venv/bin/python3 -I $P/construction_708.py $P $C/s270_sw.cert $C/s270_sw.exact.txt O/out-construction.json
.venv/bin/python3 -I $P/margins_708.py $C/s270_sw.cert $A/claims.json O/out-margins.json
.venv/bin/python3 -I $P/lineage_708.py $P $C/s270_sw.cert O/out-lineage.json
```

- **`review_708_check.py`** reads an `evand-cert` file with its own reader, which admits
  only integer and `p/q` literals and refuses a file with other than n rows; holds every
  half-angle map to the unit circle and every corner to the closed box, agreeing with
  the half-extent test; decides all 36,315 pairs by separating axes on the four face
  normals, contact allowed; decides every pair whose centres are within √2 again by the
  exact area of one closed square clipped by the other’s four closed half-planes; and,
  given the receipt, compares the side, least wall clearance, least pair gap, closest
  pair and pair count with both maintained routes’ figures digit for digit.
- **`sharp_controls_708.py`** runs W1 and W2 (the side lowered by exactly the least wall
  clearance, then 10^-30 further), P1 and P2 (the closest pair closed along its
  separating axis by exactly its gap, then 10^-30 further), F1 (a plain decimal literal
  in a coordinate) and F2 (269 rows) through the adapter and both maintained routes,
  with the review checker’s gap and clipped area on each moved pair.
  It imports `devtools.evand_arrangement_reports`, `devtools.evand_exact_certificates`
  and `devtools.upper_bound_reports`, and writes its report into the directory it is
  given first.
- **`construction_708.py`** holds the certificate to the construction the source’s
  `search/exact/README.md` describes: the side as ⌈S*(1 + 10^-20)·10^30⌉/10^30 for the
  retained KKT side, each centre as the scaled KKT centre rounded to 10^-35, each
  tangent as tan(θ/2) rounded to 10^-35 (mpmath).
- **`margins_708.py`** rebuilds every registered side at 270 from its own retained
  packet through the importer’s house readers, compares each exactly with the
  certificate, and rebuilds the frozen claim record’s differences.
- **`lineage_708.py`** measures the certificate pose by pose against T-174 and T-151
  through `devtools.check_half_angle_area`’s readers (`arrangement_gap`, `unmoved`) and an
  optimal assignment (`scipy`, binary64), with each packing’s tilt groups.

## What They Printed

`outputs/` holds each program’s JSON report:

| Output | Program | What it shows |
| --- | --- | --- |
| `out-check.json` | `review_708_check.py` on `s270_sw.cert` | passed; wall 5×10^-21 at square 15; gap 9.999999999999989×10^-21 at (41, 56); `agrees_with_receipt: true` |
| `out-check-view.json` | `review_708_check.py` on `s270_sw_regularized.cert` | passed likewise; 203 upright squares |
| `out-controls-n270.json` | `sharp_controls_708.py` | W1 and P1 passed and W2 and P2 refused on both routes; F1 accepted; F2 refused |
| `out-construction.json` | `construction_708.py` | the side, 270 centres and 270 tangents as the construction makes them |
| `out-margins.json.xz` | `margins_708.py` | every registered side at 270 above the certificate; the frozen record’s 13 differences equal |
| `out-lineage.json.xz` | `lineage_708.py` | against T-174 and T-151, the identity: 255 within a tenth, 15 beyond, at most 0.224 |
| `out-view.json` | `lineage_708.py`’s functions | the regularized view against the certificate: one square turned, none moved beyond 10^-9 |

No retained program writes `out-view.json` as it stands: the lane’s README names
`lineage_708.py`’s functions as its source.
`pytest.log` is the 69 tests the review selected (`test_upper_bound_reports_703.py` and
the general importer tests for the packet), passing in 35.5 s.
`upstream.sha256` holds the digests of the three blobs fetched again at the pin over the
GitHub REST API, which equal the retained files’.
`controls-first-run.log` is the first run of `sharp_controls_708.py`, stopped by a
formatting error in its own report code after W1 was decided; the second run’s
decisions were the same.
`timings.txt` holds the UTC start, exit status and end of the checker, view, controls
and lineage runs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
