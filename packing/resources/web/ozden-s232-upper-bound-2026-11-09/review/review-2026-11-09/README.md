# Stage 4 Review of Issues 927 to 931: Programs and Receipts

The programs and receipts of
[the stage 4 mathematical review of 9 November 2026](../../../../../../docs/project/reviews/review-2026-11-09-ozden-927-931-five.md),
lane L64, bead `think-rd0p`. The review decides Doğa Özden's five rational corner
certificates of [#927](https://github.com/jlevy/squares/issues/927) to
[#931](https://github.com/jlevy/squares/issues/931) at 232, 268, 299, 303 and 307.

This directory holds every program, the frozen files, the receipts shared by all five
counts and the receipts at 232. The packets at 268, 299, 303 and 307 hold their own
count's receipts in `review/review-2026-11-09/out/`: `check-nNNN.json`,
`controls-nNNN.json`, `controls-centre-nNNN.json` and `identity-nNNN.json`.

All programs are the reviewer's own (Claude, `tbd-strong-max` at maximum reasoning).
They import nothing from this repository or the source repositories, read the
certificates and this repository's files as data, and run with CPython 3.14 in isolated
mode (`python -I -B`), with `gmpy2`, PyYAML, NumPy and SciPy from the project's
environment. Each receipt records the SHA-256 of the programs that wrote it, and
`programs.sha256` lists the bytes kept here.

## The Clean-Room Checker

Written from the Witness/v2 schema and the mathematics alone, and frozen at
2026-11-09T07:18:14Z, before any producer code or any of this repository's witness,
verifier or promotion code was read. `frozen/checker-frozen-digests.txt` holds the six
digests, and `out/program-digests.json` shows that every receipt was written by those
bytes.

| Program | What it does |
| --- | --- |
| `l64_reader.py` | Strict reader for rational Witness/v2 files: PyYAML `BaseLoader` (every scalar a string), duplicate keys refused, every scalar an integer or `p/q`; the JSON twin must hold exactly the same witness. Returns integers only. |
| `l64_sat.py` | Method A: unit squares, walls and pairs by separating axes in `fractions.Fraction`, with exact margins and squared distances. |
| `l64_clip.py` | Method B: the same by exact Sutherland–Hodgman clipped areas in `gmpy2.mpq`. |
| `l64_check.py` | Decides one certificate: every square, wall and pair by both methods, no distance filter. |
| `l64_selftest.py` | Known answers, 3,000 random pairs taken to exact contact and 1e-30 either side, 1,000 random walls, 32 malformed files. |
| `l64_util.py` | Digests, exact decimal prints, receipts. No geometry. |

## Programs Written After the Checker's Freeze

| Program | What it does | Receipt |
| --- | --- | --- |
| `l64_controls.py`, with `controls-plan.json` | The 19 controls per certificate stated in the plan before the program existed | `controls-nNNN.json` |
| `l64_controls_centre.py`, with `controls-plan-addendum.json` | The addendum's centre-line closings and the diagnosis of S5, stated before they ran | `controls-centre-nNNN.json` |
| `l64_sides.py` | Sides, prints, extents, and gaps against the houses on `main` | `sides.json` |
| `l64_custody.py` | Pins, trees, blobs, digests and licence, by read-only git plumbing | `custody.json` |
| `l64_house.py`, `l64_identity.py` | Lineage against each house and regularized view under the eight symmetries; decides no bound | `identity-nNNN.json` |
| `l64_construct.py` | How the rational corners are made: angles, half-angle heights, wall clearances, pair margins; decides no bound | `construct.json` |
| `l64_houses.py` | The houses decided by the frozen checker, and their exact scale slack | `houses.json` |
| `l64_digests.py` | Holds every receipt to the kept bytes and the checker to its frozen digests | `program-digests.json` |
| `l64_compare_lane.py` | After the findings' freeze: the import lane's receipts held to this review's | `compare-lane.json` |

`issue-statements.json` holds the issues' statements, as data the programs check.
`frozen/review-2026-11-09-ozden-927-931-five.frozen.md` is the review as frozen at
2026-11-09T08:07:30Z, SHA-256
`222929e07ce91629f049581485823ace65c719773f036d21ccb367b975551a2b`.

## What They Printed

- `selftest.json`: `PASSED`.
- `check-nNNN.json`: `ACCEPT` at all five, 199,849 pairs strictly apart by both methods.
- `controls-nNNN.json`: every whole-file control as stated; S1b at 232 and S5 missed
  through the review's own constructions, as the review explains.
- `controls-centre-nNNN.json`: `EVERY_CONTROL_AS_EXPECTED` at all five.
- `custody.json`: `CUSTODY_HOLDS`. `houses.json`: the five houses `ACCEPT`, and every gap
  above its house's scale slack by at least 5.7e8.
- `program-digests.json`: `ALL_RECEIPTS_MATCH`. `compare-lane.json`: `LANE_EQUALS_REVIEW`.

## Rerunning

```bash
bash programs/run_all.sh PYTHON SRC REPO_ROOT OUT
```

`PYTHON` is the project interpreter, `SRC` a directory of the five source repositories
cloned at their pins, `REPO_ROOT` a checkout of this repository at `19b354a5c`, and `OUT`
the receipt directory. The final runs took 3,524 CPU-seconds, two processes at a time.
`l64_compare_lane.py REPO BRANCH OUT_DIR OUT.json` reads the import lane's packets from a
branch and is run apart.
