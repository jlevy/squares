# Review Programs, 19 October 2026

These are the programs that the stage 4 review lane of the 19 October intake wrote and
ran for
[`review-2026-10-19-upper-bound-imports-659-664-669-674.md`](../../../../../../docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md),
the review of Evan Daniel’s five certificates (bead `think-s5u5`), with what they
printed. The lane was an AI agent (Claude, strong sub-agent tier, max reasoning),
prompted separately from the import and records lanes.
It wrote the programs here and ran them on 19 October 2026, from 21:16Z to 21:53Z, in a
worktree at `d7413ccdb`, the head of `claude/intake-2026-10-19-evand-singles`. They live
in the n155 packet because it is the first of the five by entry; they read all five:

| Certificate | Packet | Entry | n |
| --- | --- | --- | --- |
| #669 | `evand-n155-explorer-2026-10-17` | T-197 | 155 |
| #674, opening | `evand-n229-dilation-2026-10-17` | T-198 | 229 |
| #674, update | `evand-n229-dilation-update-2026-10-18` | T-199 | 229 |
| #659 | `evand-n236-2026-10-16` | T-218 on the records branch | 236 |
| #664 | `evand-n271-2026-10-17` | T-219 on the records branch | 271 |

T-218 and T-219 are the numbers the records lane gave #659 and #664 on its branch; they
are assigned in merge order and may change.

## What Decides What, and What Is Registered

Two programs here decide certificates.
`third_route_1019.py` is this review’s own exact route: written for it, standard library
only, importing nothing from this repository.
`views_1019.py` runs it on the source’s three regularized views.
`area_route_1019.py` drives `devtools.check_half_angle_area`, which is registered as
`V-check-half-angle-area`, on the five certificates; it adds nothing to that module’s
tables and changes no decision.
No evidence entry cites any of these runs, and `third_route_1019.py` is in no
[`verifiers.yaml`](../../../../../frontier/verifiers.yaml) entry.
The confirming evidence of these entries rests on the maintained replay, the import
lane’s retained receipts, which `check --replay` reproduced here
(`outputs/replay/*.replay.log`); these files are the review’s record of what else it
ran, as RT-8 of the
[16 October review](../../../../../../docs/project/reviews/review-2026-10-16-upper-bound-imports-506-607.md)
kept that review’s. Its RV-6 says how the area route’s decision could be made citable.
`custody.py` checks premises: the pinned trees and files against the packets’
acquisition records.
`dilation_1019.py`, `lineage_1019.py`, `adoption_1019.py` and `receipt_totals_1019.py`
measure or compare, and decide nothing.

## Programs

Run each one from `packing/` with the project interpreter.
`P` is this directory’s `programs/`; `SCRATCH` is a directory outside the repository,
which `custody.py` fills and the third route’s `--upstream` reads:

```sh
P=resources/web/evand-n155-explorer-2026-10-17/review/review-2026-10-19/programs
uv run --frozen --all-extras --group dev python -I $P/custody.py SCRATCH \
    evand-n155-explorer-2026-10-17 evand-n229-dilation-2026-10-17 \
    evand-n229-dilation-update-2026-10-18 evand-n236-2026-10-16 evand-n271-2026-10-17
uv run --frozen --all-extras --group dev python -I $P/third_route_1019.py \
    --json OUT.json --upstream SCRATCH
uv run --frozen --all-extras --group dev python -I $P/area_route_1019.py --json OUT.json
uv run --frozen --all-extras --group dev python -I $P/views_1019.py --json OUT.json
uv run --frozen --all-extras --group dev python -I $P/dilation_1019.py --json OUT.json
uv run --frozen --all-extras --group dev python -I $P/lineage_1019.py --json OUT.json
uv run --frozen --all-extras --group dev python -I $P/adoption_1019.py --json OUT.json
uv run --frozen --all-extras --group dev python -I $P/receipt_totals_1019.py PACKET...
```

| Program | What it does | What it read | What it printed | Kept output |
| --- | --- | --- | --- | --- |
| `custody.py SCRATCH PACKET...` | Makes one blobless Git clone of `evand/square-packing` over HTTPS and holds each packet’s pinned scope to it: the pin an ancestor of the default branch, its tree the recorded `git_tree`, every manifest line’s blob at its SHA-256, every `pinned_only` entry at its digest and byte count and equal to any identical copy it names, every retained file under `source/` byte for byte its blob (a `.gz` after decompression), and each certificate and file whose digest the issue prints at that digest, with every default-branch commit touching it. Writes the pinned files under `SCRATCH/PACKET/tree/`. Runs no program of the source. | each packet’s `acquisition/sources.json`, `acquisition/upstream-subtree.sha256` and `source/`; the source at the five pins and its default branch | one JSON line per packet: 74 manifest lines in all, 15 `pinned_only` entries and 59 retained files, the default branch’s head `3a9948c`, and no problem; 21:20:28Z to 21:20:38Z | `outputs/custody.json`, `outputs/custody.log` |
| `third_route_1019.py` | Decides each certificate from its retained bytes, with its own reader: the unit circle and the unit square, every corner in the closed box, pairs 2 or more apart by circumscribed discs, every closer pair on the closed squares by exact orientation tests with the exact squared Euclidean distance, a meeting pair by its Minkowski difference; then six controls each. Holds each side and pose to the receipt’s positive input, each least wall clearance to both maintained routes’ exactly, each least distance to at least their separating-axis gap, each side to its register claim (copied by hand at `d7413ccdb`) and its issue’s print, and each file to its fetched bytes. | the five certificates, the five receipts, `SCRATCH` | 5 certificates passed, 128,462 pairs (4,145 measured exactly), 30 of 30 controls at their required outcome, no problem; exit 0, 339 s, 21:35:59Z to 21:41:38Z | `outputs/third-route-2026-10-19.json`, `outputs/replay/third-route.log` |
| `area_route_1019.py` | Admits each packet with `upper_bound_reports.read_facts`, reads its certificate with `check_half_angle_area.parse_certificate` and runs that module’s `verdict`: half-extent containment, the disc rule, exact clipped area, least distance and six controls. | the five packets | 5 passed, 2,552 pairs clipped, 30 of 30 controls; exit 0, 93 s, 21:47:58Z to 21:49:31Z | `outputs/area-route-2026-10-19.json`, `outputs/replay/area-route.log` |
| `views_1019.py` | Decides the three same-side regularized views on the third route, without controls, and holds each view’s side to its certificate’s. | the three `*_regularized.cert` files and their certificates | all three passed at their certificates’ sides; exit 0, 41 s, 21:51:00Z to 21:51:41Z | `outputs/views-2026-10-19.json`, `outputs/replay/views.log` |
| `dilation_1019.py` | Re-derives each 229 certificate from its binary64 input by the construction `dilate_cert.py` documents, written again here (factor `1 + Fraction(1e-12)`, side rounded up and centres to the nearest at 30 places, tangents by `limit_denominator(10**15)`), and splits each least margin exactly into the input’s own, the dilation’s and the rounding’s; holds the other three certificates to their 70-digit KKT points scaled by $1 + 10^{-20}$. | the two inputs and certificates, the three KKT points and certificates, the two 229 receipts | both 229 sides, all 458 centres and all 458 tangents as the construction makes them; both margin identities exact and equal to the receipts’ margins; the three KKT sides exact, 661 of 662 centres; exit 0, 10 s, 21:50:49Z to 21:51:00Z | `outputs/dilation-2026-10-19.json`, `outputs/replay/dilation.log` |
| `lineage_1019.py` | Measures each certificate against the packings its credit names with `check_half_angle_area`’s `arrangement_gap`, `unmoved` and readers (adding the five packets and T-186’s packet to its import table in process), an optimal assignment over the eight symmetries (`scipy`, binary64), and each packing’s folded tilt groups; reads de Winter’s #668 witness at 229 itself. | the five packets; T-136, T-146, T-149, T-151, T-161, T-174, T-186 and T-196 through their packets | the review’s Credit and Lineage tables; exit 0, 89 s, 21:51:41Z to 21:53:10Z | `outputs/lineage-2026-10-19.json.xz` (`xz -9` of the program’s 1,458-line output, as the 16 October review stored its report; SHA-256 `083065d8…` before compression), `outputs/replay/lineage.log` |
| `adoption_1019.py` | Compares each certificate exactly with its case ceiling, read from the case record, and with every report its frozen claim record compares, and holds the claim record’s case side to the case record. | `packing/frontier/n-155.md`, `n-229.md`, `n-236.md`, `n-271.md`; the five `acquisition/claims.json` | the review’s Adoption per Count comparisons, no problem | `outputs/adoption-2026-10-19.json`, `outputs/adoption-2026-10-19.txt` |
| `receipt_totals_1019.py PACKET...` | Sums each receipt with `upper_bound_reports.receipt_summary` and prints each positive job’s two margins on both routes. | the five receipts | 15 jobs, 770,772 pair decisions, 398.75 route CPU seconds | `outputs/receipt-totals.txt` |
| `run_serial.sh`, `chain_replay.sh`, `chain_review.sh`, `chain_review2.sh` | The shell scripts that ran every heavy command. `run_serial.sh` ran each one niced under one lock file and logged its UTC start, end, wall and exit status. `chain_replay.sh` ran the maintained commands (`acquire_source --check`, `check-claims`, `check` and `check --replay` for each packet); `chain_review.sh` ran the third route and the first runs of the dilation and lineage programs, which stopped (below), and `chain_review2.sh` the area route and the views; the dilation and lineage programs then ran again through `run_serial.sh` directly. They name this lane’s scratch directory, so they are a record of the commands, not scripts to run as they stand. |  | the logs | `outputs/replay/` |

`adoption_1019.py` and `receipt_totals_1019.py` read only small records and ran outside
the lock, in under two seconds each.
`outputs/replay/` holds one log per heavy command, as `run_serial.sh` wrote it: a start
line with the command, then its output, then an end line with the exit status and wall.

## Runs That Stopped

Two runs stopped on errors in this review’s own report code, before writing any output,
and their logs are kept:

- `outputs/replay/dilation-first-run-failed.log`: `dilation_1019.py` took the minimum of
  an empty list, the update’s input having no wall clearance below $10^{-14}$. The count
  now uses $10^{-12}$ and allows an empty list; the program then ran as above.
- `outputs/replay/lineage-first-run-failed.log`: `lineage_1019.py` named T-186 by an
  entry that `check_half_angle_area`’s readers do not map.
  It now reads T-186 through the `70a033f` key it adds; the program then ran as above.
  The measurements the stopped run printed before it stopped are the same as the second
  run’s.

## Not Kept

- The blobless clone of `evand/square-packing` and the pinned files `custody.py` wrote
  under `SCRATCH`: the author’s bytes, which each packet retains as its declaration
  allows and `custody.py` fetches again at the pins.
- The issues #639, #659, #664, #668, #669, #670, #672, #674, #675 and #678 as fetched
  with `gh issue view` on 19 October and read as data, for the printed sides, digests,
  credit requests and the counts later reports name; they are public at their URLs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
