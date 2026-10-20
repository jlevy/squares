# Review Programs, 20 October 2026

These are the programs that the stage 4 review lane of the 20 October intake (PR #699)
wrote and ran for
[`review-2026-10-20-upper-bound-imports-689-694.md`](../../../../../../docs/project/reviews/review-2026-10-20-upper-bound-imports-689-694.md),
the review of Evan Daniel’s #689 (308) and #694 (154) certificates, with what they
printed. The lane was an AI agent (Claude, strong sub-agent tier, max reasoning),
prompted separately from the import and records lanes.
It wrote the programs here and ran them on 20 October 2026, from 18:51Z to 19:10Z, in a
worktree at `34d72a95a`, the head of `claude/intake-2026-10-20-evand-308-154`. They live
in the n308 packet because it is the first of the two by entry; they read both:

| Certificate | Packet | Entry | n |
| --- | --- | --- | --- |
| #689 | `evand-n308-2026-10-19` | T-221 on the records branch | 308 |
| #694 | `evand-n154-sweep-2026-10-20` | T-222 on the records branch | 154 |

T-221 and T-222 are the numbers the records lane gave the two on its branch; they are
assigned in merge order and may change.

## What Decides What, and What Is Registered

Two programs here decide certificates.
`third_route_1020.py` is this review’s own exact route: written for it, standard library
only, importing nothing from this repository, with six controls per certificate.
`area_route_1020.py` drives `devtools.check_half_angle_area`, which is registered as
`V-check-half-angle-area`, on the two certificates with its six controls; it adds
nothing to that module’s tables and changes no decision.
`construction_1020.py` runs the third route on the two same-side regularized views,
without controls.
No evidence entry cites any of these runs, and `third_route_1020.py` is
in no [`verifiers.yaml`](../../../../../frontier/verifiers.yaml) entry.
The confirming evidence of these entries rests on the maintained replay, the import
lane’s retained receipts, which `check --replay` reproduced here
(`outputs/chain_replay.log`); these files are the review’s record of what else it ran,
as the
[19 October review](../../../../../../docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md)
kept its own. `custody_1020.py` checks premises: the pinned trees and files against the
packets’ acquisition records.
`construction_1020.py` (its measurements), `lineage_1020.py`, `adoption_1020.py` and
`receipt_totals_1020.py` measure or compare, and decide nothing.

## Programs

Run each one from `packing/` with the project interpreter.
`P` is this directory’s `programs/`; `CLONE` is a blobless clone of
`evand/square-packing` outside the repository, which `custody_1020.py` reads:

```sh
P=resources/web/evand-n308-2026-10-19/review/review-2026-10-20/programs
C308=resources/web/evand-n308-2026-10-19/source/search/packer/candidates
C154=resources/web/evand-n154-sweep-2026-10-20/source/search/packer/candidates
uv run --frozen --all-extras --group dev python -I $P/third_route_1020.py \
    --json OUT.json $C308/s308_d308.cert $C154/s154_sw.cert
uv run --frozen --all-extras --group dev python -I $P/custody_1020.py \
    --clone CLONE --json OUT.json evand-n308-2026-10-19 evand-n154-sweep-2026-10-20
uv run --frozen --all-extras --group dev python -I $P/construction_1020.py --json OUT.json
uv run --frozen --all-extras --group dev python -I $P/area_route_1020.py --json OUT.json
uv run --frozen --all-extras --group dev python -I $P/receipt_totals_1020.py --json OUT.json
uv run --frozen --all-extras --group dev python -I $P/adoption_1020.py --json OUT.json
uv run --frozen --all-extras --group dev python -I $P/lineage_1020.py --json OUT.json
```

- **`third_route_1020.py`** reads a certificate with its own reader; holds each square
  to the unit circle and to four unit edges at right angles with area 1; every corner to
  the closed box; decides pairs with centres more than 2 apart by circumscribed discs
  and every closer pair on the closed squares by exact orientation tests (a corner of
  one in the other, or two edges meeting), with the exact squared distance of disjoint
  pairs and the Minkowski difference for meeting pairs.
  Its controls: square 1 replaced by square 0 (refused); square 0 moved by S + 2
  (refused); the side at far-wall contact (accepted, the box being closed) and
  $10^{-40}$ past it (refused); the closest pair translated into contact (that pair
  alone, accepted as a contact) and $10^{-30}$ of the centre difference further
  (refused). It read the two certificates, nothing else.
- **`custody_1020.py`** held, for each packet, the pinned commit’s tree and date, every
  manifest line, every retained file (one after decompression), every `pinned_only`
  entry and its `identical_to` copy, the digests the issue prints, and the default
  branch’s history of each certificate path, to the clone.
- **`construction_1020.py`** held each side to $\lceil S^*(1 + 10^{-20}) 10^{30} \rceil
  / 10^{30}$ for the retained 70-digit KKT side, each centre to the KKT centre scaled by
  $1 + 10^{-20}$ and rounded to the nearest $10^{-35}$, and each tangent to
  $\tan(\theta/2)$ of the KKT angle at 60 digits; counted the KKT rows printed at
  binary64 precision; and decided the two views on the third route.
- **`area_route_1020.py`** ran `check_half_angle_area.verdict` on both certificates.
- **`receipt_totals_1020.py`** summed the receipts.
  **`adoption_1020.py`** re-read every side at 154 and 308 from retained bytes and held
  the packets’ claim records to them.
  **`lineage_1020.py`** measured each certificate pose by pose against the packings its
  credit names, through `check_half_angle_area`’s readers and `scipy`’s assignment.
- **`chain_review.sh`**, **`chain_review2.sh`** and **`chain_review3.sh`** ran each
  program niced from `packing/` and logged its UTC start, end, wall and exit status.

## What They Printed

`outputs/` holds each program’s log and JSON report, and the chain logs.
The maintained replays’ log is `outputs/chain_replay.log`. Three runs stopped on errors
in this review’s own report code before writing anything, and were fixed and run again:
`adoption_1020.py` on the case record’s front-matter indentation, `lineage_1020.py`
twice on entries (T-135, T-182) that the area module’s reader table does not name, and
`area_route_1020.py` on the name of the verdict’s success field (its decision was the
same on both runs). Every first log is kept beside the second (`*.first-run-failed.log`,
`*.second-run-failed.log`, `*.first-run-wrong-field.log`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
