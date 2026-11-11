# Stage 4 Review Programs and Receipts: #941, #942 and the Addendum

The programs, frozen files and receipts of the stage 4 mathematical review
[review-2026-11-11-dewinter-941-942-upper-bounds.md](../../../../../../docs/project/reviews/review-2026-11-11-dewinter-941-942-upper-bounds.md)
(lane L96), which decides Joost de Winter’s 37 `.cert` certificates (15 of #941, 16 of
#942, 6 of the addendum comment on #942) with a clean-room exact checker.
Everything here was written for the review. None of it imports this repository’s code or
the author’s, and none of it was run from inside a packet directory: the programs ran from
a scratch directory and are kept here byte for byte, as `out/program-digests.json` shows.

## Layout

| Path | What |
| --- | --- |
| `programs/` | the thirteen Python programs and modules, `run_all.sh`, and `issues-941-942.json` (the two issue bodies and the addendum comment, fetched through the REST API) |
| `frozen/checker-frozen-digests.txt` | the five checker files’ SHA-256, frozen at 2026-11-11T15:10:54Z, before the controls plan and before anything of the import lane’s was opened |
| `frozen/controls-plan.json`, `frozen/controls-plan-digest.txt` | the nine controls’ stated outcomes for every file, and their digest, recorded at 15:11:17Z before any modified file was decided |
| `frozen/review-2026-11-11-dewinter-941-942-upper-bounds.frozen.md`, `frozen/findings-frozen-digest.txt` | the review text as frozen at 15:19:48Z before the import lane’s work was read, and its digest; committed as `9b6c522bf` |
| `out/` | the shared receipts (`selftest.json`, `record-rows.json`, `claims.json`, `construct.json`, `custody.json`, `extent.json`, `compare-lane.json`, `program-digests.json`) and the fifteen #941 counts’ `check-nNNNN.json` and `controls-nNNNN.json` |

The sixteen #942 counts’ receipts are in
`de-winter-issue942-2026-11-10/review/review-2026-11-11/out/`, and the six addendum
counts’ in `de-winter-a0c4fc8-2026-11-10/review/review-2026-11-11/out/`.

## The Programs

| Program | What it does | What it read | What it printed |
| --- | --- | --- | --- |
| `l96_read.py` | the strict `.cert` reader, failing closed; integer pairs only | each certificate | (module) |
| `l96_sat.py` | method A: separating axes in `fractions.Fraction`; pairs whose exact bounding boxes are strictly apart are decided by that line | (module) | (module) |
| `l96_clip.py` | method B: exact clipping and shoelace areas in `gmpy2.mpq`; pairs with centres more than $\sqrt 2$ apart are decided by the disc lemma | (module) | (module) |
| `l96_check.py` | decides every square, wall and pair by both methods and requires them to agree exactly | the 37 certificates | `ACCEPT` at all 37 |
| `l96_selftest.py` | 72 hand-derived and randomized cases for the reader and both methods | nothing | `PASSED 72` |
| `l96_record_rows.py` | lists `main`’s register entries and beyond-horizon rows at the 37 counts, and the least current row at any larger count; decides no certificate | `main`’s `source-coverage.yaml` and `results.yaml` at `591644a9e` | no count inside 1 to 324; 655 has no row |
| `l96_claims.py` | holds every printed number of the three tables to the exact sides and to `main`’s rows | `issues-941-942.json`, `record-rows.json`, the check receipts | 37 rows, none not as printed |
| `l96_controls.py` | `plan` states nine controls per file from exact facts; `run` decides the modified files by both methods | the 37 certificates, the frozen plan | `EVERY_CONTROL_AS_STATED` at all 37 |
| `l96_construct.py` | holds #941’s border and deletion statements to the files exactly; decides no packing | the fifteen #941 certificates | `AS_STATED` |
| `l96_custody.py` | digests the retained files, holds them to the SHA256SUMS beside them, and compares the README tables with the reports | the three packets’ `source/` trees, `issues-941-942.json` | every file equal; every table equal |
| `l96_extent.py` | each packing’s exact extent and slack under its side; decides nothing about overlap | the 37 certificates | slack $5 \times 10^{-46}$, 0, or $2.0 \times 10^{-10}$ to $1.19 \times 10^{-9}$ |
| `l96_compare_lane.py` | after the freeze: holds the import lane’s ledger and upstream manifests to this review’s receipts | the lane’s `ledger.json` and three `upstream-subtree.sha256`, `main`’s 227/229/260 `LICENSE`, this review’s receipts | `LANE_AGREES` |
| `l96_digests.py` | holds every receipt naming programs to the kept bytes, and the checker and plan to their frozen digests | `programs/`, `frozen/`, the three `out/` directories | `ALL_RECEIPTS_MATCH`, 82 receipts |

The receipts of `l96_check.py`, `l96_selftest.py` and `l96_controls.py` record the
digests of the programs that wrote them. The other programs’ receipts do not, and
`program-digests.json` records every program’s digest at the audit.

## Rerunning

From `packing/` in a checkout holding the three packets, with `main`’s two registers at
`591644a9e` exported to `MAIN`:

```bash
bash resources/web/de-winter-issue941-2026-11-10/review/review-2026-11-11/programs/run_all.sh \
  REPO_ROOT OUT MAIN
```

`run_all.sh` lists the commands in the order they ran.
Each ran under `nice -n 19` with at most two processes, on CPython 3.14.7 with `gmpy2`
2.3.1 and PyYAML 6.0.3. The whole run takes about 10 CPU-minutes, nine of them in the
controls.
