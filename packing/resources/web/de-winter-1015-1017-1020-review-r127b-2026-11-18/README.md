# Stage 4 Review of Record of #1015, #1017 and #1020: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane r127b-1118’s blind stage 4
review of Joost de Winter’s three certificates of $s(127)$, issues
[#1015](https://github.com/jlevy/squares/issues/1015),
[#1017](https://github.com/jlevy/squares/issues/1017) and
[#1020](https://github.com/jlevy/squares/issues/1020), run at the strongest tier and
maximum reasoning:
[`docs/project/reviews/review-2026-11-18-de-winter-1015-1017-1020-r127b.md`](../../../../docs/project/reviews/review-2026-11-18-de-winter-1015-1017-1020-r127b.md).

The sources are `n127/n127_exact.json` and `n127/n127_witness.yaml` of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing) at
`35b576a355297942bca9c195bee5cd74f0b27f40` (#1015),
`cc20a26845789c2502950041c26709eda8a71081` (#1017) and
`a1ba5019e787e407646293d7bef81d63c9951b32` (#1020). This packet does not retain them; the
earlier review R-127’s packet,
[`de-winter-1015-1017-1020-review-2026-11-18`](../de-winter-1015-1017-1020-review-2026-11-18/README.md),
does, and `frozen/sources-pins.sha256` checks its copies. The house certificate, T-305’s,
is `../joegun-upper-bounds-2026-11-16/source/n-127-candidate.yaml`.

| Issue | File | SHA-256 |
| --- | --- | --- |
| #1015 | `n127_exact.json` | `a4c9beb8b7b656072fa60150c70d2ea685907bc0e10e19e77963464c0f946772` |
| #1015 | `n127_witness.yaml` | `c1d4ee460abe4cbcd0479af32b0b28c4ad1793786120dc0111b892c2bfb65bb0` |
| #1017 | `n127_exact.json` | `bb883631dc01343198a07826d2a84faf029789b13beb88403478db736ac27c9b` |
| #1017 | `n127_witness.yaml` | `8245da32e92e9780a22a5cf9cd42911674e3be4d816c235fe42743f9a90a085d` |
| #1020 | `n127_exact.json` | `3a66f38276be9e986fc46fa1f859de54754ec77fc4694b3442de58381056a835` |
| #1020 | `n127_witness.yaml` | `19597239cdf162cbac5c12a6e60547ce0771f0b02078446517ad3e5d3dabb31e` |
| T-305 | `n-127-candidate.yaml` | `9bde48b76afce9ab7d20d6d180650d0a6bbe46b7f106573f8155dfe9ed9d06f0` |

## Layout

- `programs/`: the review’s programs, the controls plan (`controls-plan.json`) and the
  three issues’ saved REST responses (`issue-1015.json`, `issue-1017.json`,
  `issue-1020.json`, fetched at 02:43:56Z to 02:43:57Z on 18 November).
- `frozen/`: the checker’s and plan’s digests at their freeze (`checker-frozen.sha256`,
  with `checker-freeze-notes.txt`), the sources’ digests (`sources-pins.sha256`,
  `sources-repo.sha256`), the findings’ digests at their freeze
  (`findings-frozen.sha256`, with `findings-freeze-notes.txt`), and the frozen review
  text. Each digest list checks from this directory with `sha256sum -c`.
- `out/`: the receipts; `out/second-route/` holds the repository tools’ receipts.

## Programs

Every program is the lane’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the source and reuses no
code of any earlier review. All were run with CPython 3.14.7, the project interpreter,
as `python -I -B`, under `nice -n 19`.

Frozen with the checker at 03:18:41Z on 18 November (commit `7987712380`):

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `rb127_read.py` | the strict readers of form J (the centre file) and form C (the corner witness); a centre-basis reader used only to compare the house witness | the bytes it is handed | nothing (a module) |
| `rb127_axes.py` | method A: separating axes in Python integers, from poses | poses | nothing (a module) |
| `rb127_clip.py` | method B: exact Sutherland–Hodgman clipping in GMP rationals, from corners | corners | nothing (a module) |
| `rb127_decide.py` | a packing by both methods, every square, wall and pair, with no distance filter and no tolerance | poses, corners, the side | nothing (a module) |
| `rb127_twin.py` | nothing about a packing: each form in the other’s terms, and the twin relation | rows and corners | nothing (a module) |
| `rb127_contract.py` | nothing about feasibility: the exact contraction to first contact and the contraction margin | rows and the side | nothing (a module) |
| `rb127_identity.py` | nothing: one packing against another under the box’s eight symmetries | two packings | nothing (a module) |
| `rb127_fmt.py`, `rb127_write.py`, `rb127_issue.py` | nothing: exact prints, writers of both forms, the issues’ stated numbers | fractions, rows, `issue-*.json` | nothing (modules) |
| `rb127_check.py` | one certificate: both files, natively and crossed, the twin, the side and the issue’s numbers | a report’s two files and its issue, or T-305’s file and the house witness | `out/check-*.json` |
| `rb127_controls.py` | the plan’s 35 controls on a report, 29 on the house | the files, `controls-plan.json` | `out/controls-*.json` |
| `rb127_measure.py` | option D exactly: the gains, each certificate’s contraction margin, each step’s test, and identity | the four certificates and the issues | `out/measure.json` |
| `rb127_custody.py` | nothing about a packing: the files’ custody in the source’s history | a clone, fetched copies, the issues | `out/custody.json`, `out/custody-raw.json` |
| `rb127_selftest.py` | the programs against 4,729 checks derived by hand, and seven broken copies | nothing | `out/selftest.json` |
| `rb127_trial.py` | a priced trial on synthetic packings, and three broken copies against the controls | nothing | `out/trial.json` |

Written after the checker’s freeze and frozen with the findings at 03:42:54Z (commit
`ee8cbc0b12`); they decide nothing:

| Program | What it does | Writes |
| --- | --- | --- |
| `rb127_routes.py` | compares this review’s measurements with the repository tools’ receipts, as exact fractions | `out/routes.json` |
| `rb127_e1p.py` | runs control E1p with its rule restated (the review’s F3) | `out/e1p-restated-*.json` |
| `rb127_describe.py` | sides against extents, walls, near pairs and near-upright tilts | `out/describe.json` |

Written after the findings’ freeze:

| Program | What it does | Writes |
| --- | --- | --- |
| `rb127_constant.py` | runs the controls against an accept-everything and a refuse-everything checker | `out/constant-1017.json`, `out/constant-1020.json` |
| `rb127_e1p_walls.py` | written after review A of PR #1028 (its A2): lists the squares of E1c’s packing within $10^{-40}$ of the right and the top wall; decides nothing | `out/e1p-walls.json` |

## How to Run Them

From `packing/` of this repository, with `R` this directory, `T305` T-305’s certificate,
and `PIN` a directory holding `NNNN/n127_exact.json` and `NNNN/n127_witness.yaml` for
`NNNN` = 1015, 1017 and 1020 (the review’s Frozen Findings section builds it from R-127’s
retained copies), for each report `N` with its claim `C` (11.800795682214,
11.800793726616 and 11.800793726615):

```bash
PY="nice -n 19 .venv/bin/python3 -I -B"
T305=resources/web/joegun-upper-bounds-2026-11-16/source/n-127-candidate.yaml
$PY $R/programs/rb127_selftest.py $R/out/selftest.json
$PY $R/programs/rb127_check.py pair N PIN_COMMIT $PIN/N/n127_exact.json $PIN/N/n127_witness.yaml \
  $R/programs/issue-N.json $R/out/check-N.json
$PY $R/programs/rb127_check.py house T-305 $T305 witnesses/known-best/n-127.yaml $R/out/check-T305.json
$PY $R/programs/rb127_controls.py pair N $PIN/N/n127_exact.json $PIN/N/n127_witness.yaml \
  $R/programs/controls-plan.json C $R/out/controls-N.json
$PY $R/programs/rb127_controls.py house T-305 $T305 $R/programs/controls-plan.json 11.801753890487 \
  $R/out/controls-T305.json
$PY $R/programs/rb127_measure.py $T305 $PIN/1015/n127_exact.json $PIN/1017/n127_exact.json \
  $PIN/1020/n127_exact.json $R/programs/issue-1015.json $R/programs/issue-1017.json \
  $R/programs/issue-1020.json $R/out/measure.json
```

The other programs run from the same place, with `S` an empty scratch directory, `CLONE`
a full clone of JoostdeWinter/square-packing (its head is still `838c5ea`), and `APIDIR`
the six files as fetched at the pins, in `PIN`’s layout (the contents API’s copies for
`custody.json`, `raw.githubusercontent.com`’s for `custody-raw.json`; `PIN`’s copies are
the same bytes). `rb127_constant.py` runs for `N` = 1017 and 1020:

```bash
$PY $R/programs/rb127_trial.py $S $R/out/trial.json
$PY $R/programs/rb127_custody.py CLONE APIDIR $R/programs/issue-1015.json \
  $R/programs/issue-1017.json $R/programs/issue-1020.json $R/out/custody.json
$PY $R/programs/rb127_routes.py $R/out/measure.json $R/out/second-route $R/out/routes.json
$PY $R/programs/rb127_e1p.py pair N $PIN/N/n127_exact.json $PIN/N/n127_witness.yaml \
  $R/out/e1p-restated-N.json
$PY $R/programs/rb127_e1p.py house T-305 $T305 $R/out/e1p-restated-T305.json
$PY $R/programs/rb127_describe.py $T305 $PIN/1015/n127_exact.json $PIN/1017/n127_exact.json \
  $PIN/1020/n127_exact.json $R/out/describe.json
$PY $R/programs/rb127_constant.py N $PIN/N/n127_exact.json $PIN/N/n127_witness.yaml C \
  $R/out/controls-N.json $R/out/constant-N.json
$PY $R/programs/rb127_e1p_walls.py $PIN $R/out $R/out/e1p-walls.json
```

To compare a run with its retained receipt, write it to another directory.
On 18 November, after review A, the six programs before `rb127_e1p_walls.py` were run
again that way, with a fresh clone at `838c5ea` as `CLONE` and `PIN` as `APIDIR`, and
each wrote its receipt’s bytes; `trial.json` differs only in its times.

The second route ran from `packing/` as
`python -m devtools.contraction_margin --n 127 SPEC --against SPEC --out ...` and
`python -m devtools.measure_identity --n 127 VIEW AGAINST... --out ...`, with
`center-direction-json:` for the centre files and `witness-corners:` for T-305’s file.

## What They Printed

- `rb127_selftest.py`: `PASSED`, 4,729 checks, none failed; the seven broken copies fail
  309, 6, 459, 1, 2, 2 and 24 checks.
- `rb127_trial.py`: every job ran on the synthetic packings; three broken copies made 8,
  1 and 2 of the 35 controls come out other than stated, the intact programs none.
- `rb127_check.py`: `ACCEPT` for #1015, #1017, #1020 and T-305.
- `rb127_controls.py`: 35, 35, 35 and 29 controls; all as stated but E1p at #1020.
- `rb127_measure.py`: every step’s successor below its shrunk predecessor; #1017 → #1020
  at 4.2899266 times #1017’s contraction margin.
- `rb127_custody.py`: the three pins on the source’s one linear branch in issue order, its
  head `838c5ea`; each file’s SHA-256 the same by both routes and equal to its blob at the
  pin; `n127/SHA256SUMS` listing the pinned files at #1015’s pin, the previous
  certificate’s at #1017’s and #1020’s, and the pinned files’ at the next commit; #1017’s
  statement that later commits leave its files unchanged true when it was opened and not
  now. `custody-raw.json` has the same bytes.
- `rb127_describe.py`, which decides nothing: #1015’s side is its extent rounded up at 62
  places and #1017’s at 15, #1020’s lies $4 \times 10^{-60}$ above its extent and T-305’s
  is its extent; with each certificate’s walls touched, its near pairs by decade, and the
  squares turned by less than a degree (71, 70, 1 and 6 at T-305, #1015, #1017 and
  #1020).
- `rb127_routes.py`: the two routes equal everywhere; `rb127_e1p.py`: E1p as restated at
  all four; `rb127_constant.py`: both constant checkers caught at #1017 and #1020.
- `rb127_e1p_walls.py`: at #1020, squares 51, 75, 105, 106, 107, 121, 125 and 127 within
  $10^{-40}$ of the right wall, only 107 touching it, and 113, 115, 119, 120, 121, 122
  and 124 within $10^{-40}$ of the top, the 14 that E1p’s restated rule names; at #1015
  and #1017, exactly the squares the frozen rule names.

In all, about 0.2 CPU-hours before review A, and under 4 CPU-minutes after it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
