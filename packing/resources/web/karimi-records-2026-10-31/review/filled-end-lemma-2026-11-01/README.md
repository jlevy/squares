# Stage 4 Review of the Filled-End Lemma: Programs and Receipts

These are the programs and receipts of the stage 4 mathematical review of the
filled-end lemma, which `packing/devtools/filled_end_checker.py` states and proves and
pull request [#870](https://github.com/jlevy/squares/pull/870) uses to decide Mohsen
Karimi’s filled-end rows of [#847](https://github.com/jlevy/squares/issues/847)
([the review](../../../../../../docs/project/reviews/review-2026-11-01-filled-end-lemma.md)).
They were written on 1 November 2026 by a separately prompted review lane, an AI reviewer
of the Claude family (Anthropic) at the strong sub-agent tier (`tbd-strong-max`) and
maximum reasoning, in a worktree of its own at the pull request’s head `7db2baa55`.

`fe_independent.py`, `fe_all_rows.py` and `fe_layer_reasons.py` import only the
standard library and share no code with the checker, the maintained routes or the
author’s programs. They were written
after the reviewer had read the checker and the author’s `filled_ends.py` as data; the
author’s programs never ran. `fe_crosscheck.py` and `fe_checker_mutation.py` run the
checker, which is the object under review, and never edit it: the first only to obtain
the certificate text it writes, the second to delete one check at a time in an in-memory
copy.

All programs ran with CPython 3.14.7 (`packing/.venv/bin/python3`), with `-I`, under
`nice`, at most two at a time, on a shared four-core host.

## What Each Program Does

| Program | Role | What it read | Receipt |
| --- | --- | --- | --- |
| `fe_independent.py` | **decides**: builds each row’s packing from its seven parameters and verifies every square of the construction exactly, in integers over one common denominator (unit squares, walls, separating axes on every pair whose bounding boxes share a unit cell); then the mutants | `source/filled_records.csv`, or the V1.0 archive’s member | `outputs/sample-v2.json` (five edge rows and 20 drawn with seed 20261101, with mutants); `outputs/all-rows-geometry-v2.json` and `outputs/all-rows-geometry-v1.json` (`--all`: every row of each deposit); `outputs/selftest.json` (`--self-test`) |
| `fe_all_rows.py` | holds every row of both deposits to the lemma with `fe_independent`’s construction and compares 16 fields with the lane’s decisions receipts; measures the decimal side and the edges; holds every row’s placed squares in the two `--all` receipts to the decisions receipts’ capacity | both tables; `receipts/filled-end-decisions-v2.json.gz` and `-v1.json.gz`, as data; the two `--all` receipts | `outputs/all-rows.json` |
| `fe_crosscheck.py` | compares the certificate the checker writes with this review’s construction, square for square, after parsing it with its own reader; flips the H band’s tilt sign | the checker’s `certificate_text`; the V2.0 decisions receipt, as data | `outputs/crosscheck-v2.json` |
| `fe_checker_mutation.py` | deletes each `_refuse` call of `decide`, `band` and `_stated` in turn and decides the eleven per-row controls with each variant; with `--baseline-all`, classifies every control’s refusal at every V2.0 row by the check its message names; probes a negative-tilt control | the checker’s source | `outputs/checker-mutation.json` |
| `fe_layer_reasons.py` | decides the sampled rows’ 397 layer-plus-one mutants again and records each one’s own reasons, which the sample receipt keeps only as a union per row | `source/filled_records.csv` | `outputs/layer-reasons.json` |

## How to Run Them

From any directory, with `PACKET` this packet and `PACKING` the repository’s `packing/`:

```bash
PY="$PACKING/.venv/bin/python3 -I"
$PY programs/fe_independent.py --self-test outputs/selftest.json
$PY programs/fe_independent.py "$PACKET" outputs/sample-v2.json
$PY programs/fe_independent.py "$PACKET" outputs/all-rows-geometry-v2.json --all --version 2 --workers 1
$PY programs/fe_independent.py "$PACKET" outputs/all-rows-geometry-v1.json --all --version 1 --workers 1
$PY programs/fe_all_rows.py "$PACKET" outputs/all-rows.json \
  outputs/all-rows-geometry-v2.json outputs/all-rows-geometry-v1.json
$PY programs/fe_crosscheck.py "$PACKING" outputs/crosscheck-v2.json 1188 5265 7439 8524 9517 \
  1244 1807 2154 2266 2447 2944 3317 3501 3650 3747 4807 5528 6247 6564 7080 7748 8227 8306 9141 9929
$PY programs/fe_checker_mutation.py "$PACKING" outputs/checker-mutation.json --baseline-all \
  1188 5265 7439 8524 9517 1244 1807 2154 2266 2447 2944 3317 3501 3650 3747 4807 5528 6247 6564 7080 7748 8227 8306 9141 9929
$PY programs/fe_layer_reasons.py "$PACKET" outputs/layer-reasons.json \
  1188 5265 7439 8524 9517 1244 1807 2154 2266 2447 2944 3317 3501 3650 3747 4807 5528 6247 6564 7080 7748 8227 8306 9141 9929
```

The 20 drawn counts are the ones `fe_independent.py` draws with its default seed; each
receipt records the SHA-256 of the program that wrote it and of the table it read.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
