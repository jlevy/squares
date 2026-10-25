# The Stage 4 Review of T-241 and T-242: Programs and Receipts

These are the programs and receipts of the stage 4 mathematical review of Francisco
Couzo’s certificate at 304 (T-241) and Evan Daniel’s certificates at 268 and 304 (T-242)
([the review](../../../../../../docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md)).
They were written and run on 24 October 2026 by the review lane
`c-review-t241-t242-math` (bead `think-vm3m`), an AI reviewer of the Claude system
family (Anthropic) at the strongest sub-agent tier (`tbd-strong-max`) and maximum
reasoning.

The certificates are not copied here.
Every program reads them where the packets keep them, and checks each against the
SHA-256 the packets pin: Couzo’s `n304.cert` in the issue-763 packet (`c8433dd7…231d`),
and Daniel’s `s268_lightning.cert` (`c87da316…4a49`) and `s304_pub.cert`
(`5dd7436a…6f21`) in this packet.

All programs ran with CPython 3.14.7 (the project interpreter,
`packing/.venv/bin/python3` of the main checkout, since the review’s worktree lacked the
`vendor/kpress` submodule that `uv run` needs), with `-I`, under `nice -n 10`, one at a
time. The working directory was `packing/` of a worktree at `main` `84d4a75af`. The two
shell scripts read Git and GitHub only.

## What Each Program Does

The programs are in `programs/` and their outputs in `outputs/`.
`outputs/program-digests.sha256` lists the SHA-256 of every program, and each JSON
receipt records the digest of the program that wrote it.

| Program | Role | What it read | Output |
| --- | --- | --- | --- |
| `t241_t242_exact.py` | **decides** finite feasibility of the three certificates, by separating axes and by clipped areas in `Fraction`, all pairs a third time by separating axes; 12 controls per certificate and 9 hand-decided packings; the sides, their 12-place prints and the register’s margins | the three certificates; the side lines of #763’s `n268.cert` and of the known-best witnesses at 268 and 304 | `outputs/t241_t242_exact.json`, `.txt` |
| `t241_t242_identity.py` | decides nothing: identity pose by pose under the box’s eight symmetries, by optimal assignment (summed and squared distance) and nearest centres | the three certificates; #763’s `n268.cert` and its parent `85dbd707…`; the known-best witnesses at 268 and 304; Ostashev’s #575 `n0304.sqcert`; Daniel’s `.input.txt`, `.predescent.txt` and regularized view | `outputs/t241_t242_identity.json`, `.txt` |
| `t241_t242_credits.py` | decides nothing: what the sources say about credit at 268, 303 and 304, and a census of the manifest’s provenance fields | the issue-763 packet’s manifest and `certified_bounds.json` (964ee2b); from scratch copies of the clones, the `fa6237e` manifest, the catalogue at three commits, `RECORD_PROVENANCE.md`, Couzo’s and Daniel’s commit messages, Daniel’s `Completed.md` and `TODO.md` at `659ee62`; Daniel’s `CREDITS.md` | `outputs/t241_t242_credits.txt` |
| `t241_t242_receipts.py` | decides nothing: holds the checker’s least gap and least wall clearance to the packets’ sharp-control receipts, exactly | `outputs/t241_t242_exact.json`; the three `sharp-controls*.json` | `outputs/t241_t242_receipts.txt` |
| `t241_t242_sense.py` | decides nothing about the bounds: the three certificates read with the other rotation sense | the checker, loaded by path; the three certificates | `outputs/t241_t242_sense.txt` |
| `t241_t242_custody.sh` | decides nothing: the Git blob of each file read here against the source’s tree at the pinned commits | scratch copies of the two clones (trees and commits only) | `outputs/t241_t242_custody.txt` |
| `t241_t242_pushes.sh` | decides nothing: the push times of the two publications | GitHub’s repository activity API | `outputs/t241_t242_pushes.txt` |

`t241_t242_exact.py` was written from the mathematics and the certificates’ header
lines, before its author read any of the sources’ checkers or this repository’s routes,
and its author has read none of them since.
It first decided the three certificates at about 20:33Z, without controls, and in full
at 20:39Z after an edit that only printed more digits; no decision has changed since.
It was moved into `programs/` at 20:57Z, with its path to `packing/` and its output
names edited, and run again; its SHA-256 as run is in the receipt and in
`outputs/program-digests.sha256`. `t241_t242_identity.py` was written and run before its
author read the packet’s `measure/identity.json` or any identity code.
`t241_t242_sense.py` was written after the review read the #763 review’s RF-11. The
others were written after the checker decided.

## How to Run Them

From `packing/`, with the project interpreter, `R` this folder and `S` a scratch
directory:

```bash
PY=.venv/bin/python3   # or: uv run --frozen --all-extras --group dev python
R=resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24
$PY -I $R/programs/t241_t242_exact.py --all-pairs --out $R/outputs/t241_t242_exact.json
$PY -I $R/programs/t241_t242_identity.py --out $R/outputs/t241_t242_identity.json
$PY -I $R/programs/t241_t242_receipts.py
$PY -I -B $R/programs/t241_t242_sense.py
$PY -I $R/programs/t241_t242_credits.py --scratch $S/data \
    --evand-clone $S/clones/evand_square-packing --couzo-clone $S/clones/franciscouzo_square-packing
bash $R/programs/t241_t242_custody.sh $S/clones/evand_square-packing $S/clones/franciscouzo_square-packing
bash $R/programs/t241_t242_pushes.sh   # needs gh with access to github.com
```

The credit reader needs, in `$S/data`, files fetched in scratch copies of the two
watched clones with `git cat-file -p BLOB > FILE`: `manifest-fa6237e.json` (blob
`49556d49`, SHA-256 `31b0caef…4f30`, the digest the couzo-n304 packet pins),
`catalogue-fa6237e.md`, `catalogue-964ee2b.md` and `catalogue-1c17153.md`
(`certificates/best/README.md` at each), `RECORD_PROVENANCE.md` (blob `e03efd32`), and
`evand-659ee62-Completed.md` and `evand-659ee62-TODO.md`. Its output prints each file’s
digest.

## What They Printed

- `t241_t242_exact.py`: all three certificates valid on both methods, the methods
  agreeing on every pair.
  T-241: least wall clearance $10^{-15}$ (near and far), least pair gap
  $8.18394241446125726760502575632 \times 10^{-11}$ (squares 67 and 68), 46,056 pairs on
  the third pass. T-242 at 268: least wall $5 \times 10^{-21}$, far wall
  $5.00000000046078 \times 10^{-21}$, least gap $9.99999999999998886 \times 10^{-21}$
  (squares 239 and 241), 35,778 pairs.
  T-242 at 304: least wall $5 \times 10^{-21}$, far wall
  $5.00000000060942 \times 10^{-21}$, least gap $9.99999999999999487 \times 10^{-21}$
  (squares 57 and 58). Sides equal to the stated ones; prints 17.926898903393,
  16.874361715870 and 17.926898900357. All 9 hand-decided packings and all 36 controls
  as expected; all five stated margins match.
  53.4 CPU seconds.
- `t241_t242_identity.py`: the identity table of the review, 19 comparisons, 2.2 CPU
  seconds.
- `t241_t242_receipts.py`: least gaps and least walls equal to all three receipts,
  exactly.
- `t241_t242_sense.py`: valid as the headers state; under the other sense, 89, 99 and 92
  overlapping pairs.
- `t241_t242_credits.py`: the manifests’ entries at 268, 303 and 304 (the 304 entry
  identical at `fa6237e` and `964ee2b`); in the `fa6237e` census, 182 of 182 entries
  with a seed of their own name another previous reference; the catalogue rows; the
  `RECORD_PROVENANCE.md` line on `70a033f`; no `SOURCE_NOTICES` file in any commit; the
  two authors’ statements.
- `t241_t242_custody.sh`: every file the review read from a packet is the source’s blob
  at the pinned commit.
- `t241_t242_pushes.sh`: `964ee2b` pushed at 2026-10-23T23:38:42Z, `8a8879a` at
  2026-10-24T04:53:53Z.

Every run of the review together used about 140 CPU seconds, the final runs about 65.

## Registration

`t241_t242_exact.py` decides and belongs in `packing/frontier/verifiers.yaml` with its
independence record, cited by one evidence entry for T-241 and one for T-242
([record-changes.md](record-changes.md)). The other programs decide nothing and are
cited by no evidence entry; they are kept as the review’s measurements and readings.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
