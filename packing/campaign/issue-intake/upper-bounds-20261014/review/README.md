# Intake Ledger Review Programs

The independent review of the 2026-10-14 intake ledger,
[`review-2026-10-14-intake-ledger.md`](../../../../../docs/project/reviews/review-2026-10-14-intake-ledger.md),
recomputed the ledger’s verdicts with these programs.
The reviewer wrote them against `packing/devtools/intake_ledger.py` and this directory
on branch `claude/serene-hopper-xxh80m` at commit 1dc253e5e, and changed nothing in the
repository. They were copied here in the fix round that answered the review.
The copy changes what the lint floor requires (formatting and names), reads repository
data by repository path instead of from a scratch copy of `main`, takes `PINNED` as
`recompute.py`’s argument in `main` rather than at import, and ports two programs:
`bug_demos.py` to the module’s current interface, since the `lowered` it exercised is
gone, and `tables.py` to print its two tables instead of writing files.

Run every program from `packing/` with the project interpreter, `.venv/bin/python3`.

## Programs

| Program | Reads | Prints | Output kept here |
| --- | --- | --- | --- |
| `recompute.py PINNED` | each lane’s `claims.json` and `algebraic-claims.json`; `packing/frontier/` (the cases, `results.yaml`, `source-coverage.yaml`); `PINNED/github/` for report times; `PINNED/upstream/` certificate headers; then `ledger.json` and `ledger.yaml` for the comparison | the 306-step verdict comparison with its disagreements; the sensitivity of the verdicts to the verified lane; the special comparisons at 11, 17, 29 and 51; #593’s binary64 prints against the exact sides; the provenance audit of the 280 lane-backed claims; the 26 transcribed claims against the reviewer’s own sources; a seeded sample of 15 claims | `recompute-output.txt` (the run the review cites) and `recompute-rerun.txt` (this round’s ledger) |
| `scan_cases.py` | `packing/frontier/n-NNN.md` at every in-horizon count the ledger claims at | both upper lanes of each case, flagged where the verified lane is below the reported one (none) or the exact forms differ (61 counts) | none: it reproduces the review’s `cases-scan.txt` byte for byte at `main` 7c672f5be |
| `compare_geometry.py A B` | two rational centre-basis Witness/v2 facts, `.yaml` or `.yaml.gz`, by repository path | one line: the best of the box’s 8 symmetries, the largest centre displacement, and how many squares lie within 1e-6, 1e-3 and 0.1 (a measurement; it decides nothing) | `compare_geometry-output.txt`, #573 at 153 and 207 against PingYou Ltd’s T-148 and T-147 |
| `bug_demos.py` | `devtools.intake_ledger` | the two walk defects the review reproduced, as the module now handles them | `bug_demos-output.txt`, what this program prints against the module (the review’s M4 says what the reviewer’s own program printed) |
| `dump_sources.py` | this directory’s `sources.yaml` | report coordinates, lane mappings and transcribed claims | none: `sources.yaml` was regenerated in this round, so the review’s `sources-structure.txt` describes an older file |
| `tables.py PINNED [OUTPUT]` | `recompute.py`’s verdict rows (by default `recompute-output.txt`), `ledger.yaml`, the lane rows behind the sample, `PINNED/github/issue-593.json` | the per-count verdict table and the 15-claim provenance sample | none: both tables are in the review, and this prints them unchanged from `recompute-output.txt` |

## Pinned Bytes

`recompute.py`, `tables.py` and the #573 comparison need bytes `main` does not carry.
They are not retained here, since [OR-18](../../../../../operating-rules.md) keeps bulk
data out of Git: the lane records and certificate headers are files at pinned commits
that can be fetched again, and the GitHub reads are not pinned at all.
That is why their outputs are kept.
`PINNED` is a directory laid out as the reviewer laid it out:

- `lanes/<lane>/<packet>/claims.json` and `algebraic-claims.json`, as
  `packing/resources/web/<packet>/acquisition/` holds them at the lane commits this
  directory’s README names under “Lane Records Read”.
  The programs read the packet from `main` instead wherever `main` carries it, which at
  7c672f5be is `couzo-certificates-2026-10-11`, `dostashev-compositions-2026-10-12`,
  `dostashev-merged-bands-2026-10-13`, `evand-compositions-2026-10-13` and
  `evand-fresh-compositions-2026-10-14`; their bytes equal the reviewer’s copies.
  The couzo packets of 2026-10-12 and 2026-10-13, both mishapolk packets, the seven
  pingyou packets and the pr574 packet are on their lane branches only.
- `github/issue-N.json` (`gh issue view --json ... comments`), `pr-574.json` with its
  commits, and `edits-N.json` (GraphQL `userContentEdits`), all read-only.
- `upstream/`, certificate headers fetched through the GitHub contents API at the pinned
  commits: dostashev n0155, 156, 175, 211, 232 and 264 at a8db6ff, n0176 at fe43a64 and
  n0304 at b909e1b; franciscouzo n154, 211, 241, 339, 379, 380 and 382 at 4596670;
  TheSnakeFang n0380 and n0381 at e646c47 and n0382 at c284cd0; Mishapolk n51.cert at
  46f638c; and the numerical `claims.json` at PR #574’s head 4c319c24a.

The #573 witness facts at 153 and 207 are in the mishapolk lane’s packet
`mishapolk-exact-certificates-2026-10-12`, on its branch only; PingYou Ltd’s T-148 and
T-147 facts are on `main` under
`packing/resources/web/pingyou-n153-certificate-2026-10-11/` and
`pingyou-n207-certificate-2026-10-11/`.

## What the Two Recomputation Runs Say

`recompute-output.txt` is the review’s run against the ledger at 1dc253e5e: 306 steps,
305 agree, and one disagrees, #593 at 51, where the ledger said undecided and the
recomputation said not recorded (M2).

`recompute-rerun.txt` is the same program against the ledger this round wrote: 306
steps, 305 agree, and 51 now agrees.
The one disagreement is PR #574 at 11. The ledger now says not recorded, above the
verified lane’s root of `P_trump11`. The recomputation’s walk says undecided, because
its enclosure of that root is 2.0e-90 wide and holds PR #574’s side.
The program’s own exact sign test, in its “Special comparisons”, puts the side above the
root, which is the verdict M1 asked for.
The module narrows its enclosure until the comparison separates, and the side is above
the root by at least 1.71e-95.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
