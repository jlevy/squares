# Review code: project candidates at 130, 293 and 307 (think-ruu2)

Written by the stage 4 reviewer `bold-ritchie-rv-ruu2` (Claude, tier `tbd-strong-max`,
reasoning max) for `review-2026-10-31-project-candidates-130-293-307.md`. Every program
here was written for this review from the mathematics and the certificate formats the
files state in their own headers.
None imports or copies code from the repository, from Evan Daniel’s
`evand/square-packing`, from the regularizer’s driver, or from any earlier review; the
inputs are read as data.

Run with the project interpreter (Python 3.14.7, standard library only), from this
directory, with `INPUTS` the review’s `inputs/` and `OUT` its `out/`:

```bash
PY=/root/.local/bin/python3.14
$PY run_checks.py INPUTS OUT          # both exact routes on every subject
$PY consistency.py INPUTS             # view versus native certificate, square by square
$PY identity.py INPUTS OUT            # pose-by-pose measurement against each house
$PY contract.py INPUTS OUT            # uniform contraction of each house to first contact
$PY sides.py INPUTS OUT INPUTS/cases  # exact margins, 12-place prints, ceilings above
$PY controls.py INPUTS OUT            # 64 sharp controls on both routes (~3 CPU-minutes)
$PY build293.py INPUTS OUT            # write the 293 construction as .cert files and re-decide them
```

The whole set takes under five CPU-minutes on one core.

## Inputs (`../inputs/`, git blob and SHA-256 prefixes)

| File | Blob | SHA-256 | What it is |
| --- | --- | --- | --- |
| `n130-view-solved.yaml` | `8a991c289379` | `95deb14bcbed5da0` | The 130 candidate view, run `adopt-2026-10-31-n130-307-evand` |
| `n307-view-solved.yaml` | `6030dd50c588` | `0297fb2719e0ecc0` | The 307 candidate view, same run |
| `n130-solve-witness.cert` | `1908228e71dc` | `9d4b4c29e038adc9` | That run’s KKT solve certificate at 130 |
| `n307-solve-witness.cert` | `ee44c7caa47c` | `f54749107b0a5ee1` | That run’s KKT solve certificate at 307 |
| `n130-regularize.cert` | `aef1e6765c54` | `6d32160c21071a0b` | That run’s regularized certificate at 130 (the view’s source) |
| `n307-regularize.cert` | `e0d1ee4b16ea` | `4f87c91ae8872a27` | The same at 307 |
| `s260_1028.cert` | `6114e28fe8ab` | `d6d6f45f600f6552` | T-257’s 260 certificate, from `e482345fe` |
| `s293_1028.cert` | `589516caccee` | `236bc05f057a28df` | T-257’s 293 certificate, from `e482345fe` |
| `house-n130.yaml`, `house-n293.yaml`, `house-n307.yaml` | `69923004685f`, `4b9fa4b23084`, `5876651631d9` | `138767d0cd46fb24`, `76496d476e1b04fd`, `ac27836a5f8db132` | The house witnesses at `e482345fe` |
| `mishapolk846-n130.cert`, `couzo844-n307.cert` | `e4dcd1c5e871`, `e9267546832e` | `1e00cd74ccf3495b`, `1fd01ff42e7679f1` | The houses’ source certificates at `e482345fe` |
| `cases/n-130.md` … `cases/n-324.md` |  |  | Case records at `e482345fe`, for the ceilings above each count |

## Programs

- **`qio.py`** reads the inputs and builds the 293 strip; it decides nothing.
  A view is read line by line under a strict pattern (a centre-basis rational witness:
  `n`, `side`, then per square two centre and two basis rationals); a `.cert` is
  `n side` then `n` rows `cx cy t`, with
  `(cos, sin) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))` as each certificate’s own header
  states. `l_strip(S, variant)` returns 33 axis-aligned unit squares in
  `[S, S+1]x[0, S+1] U [0, S+1]x[S, S+1]`: `16+16+1` (a column of 16 from the floor, a
  row of 16 from the left wall, a corner square), `17+16` (a column of 17 from the
  floor), and `17top+16` (a column of 17 flush with the top wall, the 293 house’s own
  placement).
- **`route_sat.py`** (route A) decides a packing exactly: every basis has
  `a^2 + b^2 = 1`; every square’s support-function extent lies in `[0, side]` on both
  axes; every pair, with no pruning, is separated on one of its four edge normals with
  `|u . d| >= (1 + |cos D| + |sin D|)/2`. It reports the least pair slack and the least
  wall clearance with where they occur, and the extent.
- **`route_area.py`** (route B) decides it again by areas: corners counter-clockwise,
  unit edges, right angles and area 1; each square clipped to the box keeps area exactly
  1; every pair whose corner bounding boxes overlap in their interiors is clipped
  (Sutherland-Hodgman, exact) and must have area exactly 0. It shares only `qio` with
  route A.
- **`run_checks.py`** runs both routes on each subject and writes
  `out/check-<label>.json`.
- **`consistency.py`** compares each view with the run’s native certificates.
  Decides nothing.
- **`identity.py`** measures each candidate against its house under the box’s eight
  symmetries in binary64 (nearest-centre pairing, moves and turns), and the 293 house’s
  260 block and strip apart.
  Decides nothing.
- **`contract.py`** scales a certificate’s centres about the origin by the least
  `lambda*` that keeps every pair interior-disjoint (`max over pairs of T/M`, exact),
  translates it into the corner, boxes it, and decides the result on both routes.
  It shows how much of a margin is the house certificate’s own padding.
- **`sides.py`** prints exact sides, margins and upward 12-place prints, and the least
  verified ceiling over `n < m <= 324` (Decimal at 60 digits; the five `root(...)`
  ceilings it cannot read are read from their case records’ decimal values in the
  review).
- **`build293.py`** writes the 293 construction as two certificate files
  (`out/n293-s260-plus-L-17top+16.cert`, `out/n293-s260-plus-L-16+16+1.cert`): the 260
  rows of `s260_1028.cert` verbatim, then 33 strip rows, header `293 S+1`; reads each
  back and decides it on both routes.
  It printed both accepted, with SHA-256 `10eac4aa…` and `55c2bb43…`
  (`out/build293.log`).
- **`controls.py`** runs the sharp controls of the review’s section on controls on both
  routes.

## What they printed

`out/` keeps every log and JSON receipt: `run_checks-*.log`, `check-*.json`,
`consistency.log`, `identity.log` and `identity.json`, `contract.log` and
`contract.json`, `sides.log` and `sides.json`, `controls.log` and `controls.json`. The
review quotes them.

No program here is registered in `verifiers.yaml` and no evidence entry cites one yet.
If the record cites this review’s decisions, `route_sat.py` and `route_area.py` are the
deciding programs (clean room: their authors read the certificate formats from the
files’ headers and the record’s prose, never the producer’s checkers or the maintained
routes); the others decide nothing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
