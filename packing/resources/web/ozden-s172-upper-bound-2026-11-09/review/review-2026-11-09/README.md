# Stage 4 Review of Issues 935 and 936: Programs and Receipts

The programs and receipts of
[the stage 4 mathematical review of 9 November 2026](../../../../../../docs/project/reviews/review-2026-11-09-ozden-935-936.md),
lane L72, bead `think-qqyg`. The review decides Doğa Özden’s two rational corner
certificates of [#935](https://github.com/jlevy/squares/issues/935) at 172 and
[#936](https://github.com/jlevy/squares/issues/936) at 270.

This directory holds every program, the frozen files, the receipts shared by both counts
and the receipts at 172. The 270 packet holds its own count’s receipts in
`review/review-2026-11-09/out/`: `check-n270.json`, `plan-facts-n270.json`,
`controls-n270.json`, `identity-n270.json` and `construct-n270.json`.

All programs are the reviewer’s own (Claude, `tbd-strong-max` at maximum reasoning).
They import nothing from this repository or the source repositories, read the
certificates, decimal poses and this repository’s files as data, and run with CPython
3.14 in isolated mode (`python -I -B`), with `gmpy2`, PyYAML, NumPy, SciPy and mpmath
from the project’s environment. Each receipt records the SHA-256 of the programs that
wrote it, and `programs.sha256` lists the bytes kept here.

## The Clean-Room Checker

Written from the Witness/v2 schema, the mathematics and the precedent review’s text
alone, and frozen at 2026-11-09T16:12:07Z, before any producer code or any of this
repository’s witness, verifier or promotion code was read.
`frozen/checker-frozen-digests.txt` holds the six digests, and
`out/program-digests.json` shows that every receipt was written by those bytes.

| Program | What it does |
| --- | --- |
| `l72_reader.py` | Strict reader for rational Witness/v2 corner files: PyYAML’s composed nodes with every scalar a string, aliases, explicit tags and duplicate keys refused, every scalar an integer or `p/q` in canonical form; the JSON twin must hold exactly the same witness. Returns integers only. |
| `l72_sat.py` | Method A: unit squares, walls and pairs by separating axes in `fractions.Fraction`, with exact margins and clearances. |
| `l72_clip.py` | Method B: the same by exact Sutherland–Hodgman clipped areas in `gmpy2.mpq`, with three classes (area, contact, clear) for every pair and wall. |
| `l72_check.py` | Decides one certificate: every square, wall and pair by both methods, no distance filter. |
| `l72_selftest.py` | 80 cases: known answers in both listing senses, walls, refused shapes, 3,000 random pairs taken to exact contact and 1e-30 either side, 1,000 random walls, 41 malformed files. |
| `l72_util.py` | Digests, exact decimal prints, receipts. No geometry. |

## Programs Written After the Checker’s Freeze

| Program | What it does | Receipt |
| --- | --- | --- |
| `l72_freeze.py` | Writes a frozen-digest file; decides nothing | `frozen/checker-frozen-digests.txt` |
| `l72_plan_facts.py` | Exact wall clearances, the side less its 12-place floor and the least pair’s centre-line move, from which the plan was stated; decides no modified file | `plan-facts-nNNN.json`, kept as written before the plan |
| `l72_controls.py`, with `controls-plan.json` | The 23 controls per certificate stated in the plan before the program existed | `controls-nNNN.json` |
| `l72_sides.py` | Sides, prints, extents, the decimal poses’ sides and the gaps against the houses on `main` | `sides.json` |
| `l72_custody.py` | Pins, trees, blobs, digests and licences, by read-only git plumbing and blob ids computed here | `custody.json` |
| `l72_house.py` | Reads a rational centre-basis witness (the houses, the gzip views) as exact corners | none (a module) |
| `l72_houses.py` | The houses decided by the frozen checker, and their exact uniform-contraction margins against each gain | `houses.json` |
| `l72_identity.py` | Lineage against each house and regularized view under the eight symmetries; decides no bound | `identity-nNNN.json` |
| `l72_construct.py` | How the rational corners were made: angles, half-angle heights, wall clearances, pair margins, and each certificate against its decimal pose at 60 digits; decides no bound | `construct-nNNN.json` |
| `l72_digests.py` | Holds every receipt to the kept bytes, the checker to its frozen digests and the plan to its stated digest | `program-digests.json` |

`issue-statements.json` holds the issues’ statements, as data the programs check.
`run_checks.sh` and `run_controls.sh` ran the first passes in scratch space;
`run_all.sh` wrote every receipt kept here.

## What They Printed

- `selftest.json`: `PASSED`, 80 cases.
- `check-nNNN.json`: `ACCEPT` at both, 51,021 pairs strictly apart by both methods.
- `controls-nNNN.json`: `EVERY_CONTROL_AS_STATED` at both, 23 of 23 each.
- `sides.json`: `SIDES_AS_STATED`. `custody.json`: `CUSTODY_HOLDS`.
- `houses.json`: both houses `ACCEPT`, each contraction margin its side times 1e-20, and
  each gain 8.1e13 to 2.4e16 times its margin.
- `program-digests.json`: `ALL_RECEIPTS_MATCH`.

## Rerunning

```bash
bash programs/run_all.sh PYTHON SRC REPO_ROOT OUT172 OUT270
python -I -B programs/l72_digests.py REVIEW172 REVIEW270 REVIEW172/out/program-digests.json
```

`PYTHON` is the project interpreter, `SRC` a directory holding `s172-upper-bound` and
`s270-upper-bound` cloned at their pins, `REPO_ROOT` a checkout of this repository at
`ef1af4933`, `OUT172` and `OUT270` the two packets’ `review/review-2026-11-09/out`, and
`REVIEW172` and `REVIEW270` the two review directories. The final run took about
580 CPU-seconds, two processes at a time.
