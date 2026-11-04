# Stage 4 Review of #893 and #894: Programs and Receipts

These are the programs and receipts of the stage 4 mathematical review of Doğa Özden’s
certificates for $s(299)$ ([#893](https://github.com/jlevy/squares/issues/893)) and
$s(204)$ ([#894](https://github.com/jlevy/squares/issues/894)), dated 4 November 2026
(bead `think-ybep`). The review is
`docs/project/reviews/review-2026-11-04-ozden-893-894-299-204.md`.

They were written by Claude, an AI system, in the stage 4 mathematical review lane, at
the strong tier (`tbd-strong-max`) with maximum reasoning.
That lane was prompted separately from the import lane and shared no context with it.
The programs were written from the mathematics, from the Witness/v2 schema text in
`packing/witnesses/witness.schema.yaml` and from the certificates themselves.
Before any program was written and run, the authors had read neither the author’s
`verifier/sqcheck.py` (nor its README) nor any of this repository’s witness verifiers:
`sqpack`’s `packing-witness verify`, the independent rational corner checker or
`devtools.upper_bound_reports`. The author ran `packing-witness verify` on these files,
so that verifier is the producer’s code here.
The authors did read the author’s printed outputs (`packing-witness-verify.txt` and
`sqcheck-output.*`) and, after their own results were computed, the import lane’s
receipts, which `oz_compare_lane.py` compares with them.

Every program imports only the standard library, `gmpy2` (exact arithmetic), and `numpy`
and `scipy` for the identity measurement.
None imports anything from this repository or from the packets.

## Layout

The programs serve both packets and are kept once, here, in [programs/](programs/),
with their SHA-256 digests in [programs.sha256](programs.sha256).
The receipts are named by count.
This directory’s [out/](out/) holds the `-n299` receipts and the three that cover both
counts, `selftest.json`, `sides.json` and `custody.json`.
The [ozden-s204-upper-bound-2026-11-03](../../../ozden-s204-upper-bound-2026-11-03/review/review-2026-11-04/README.md)
packet’s `review/review-2026-11-04/out/` holds the `-n204` receipts.
Each receipt records the SHA-256 of the program that wrote it and of `ozlib.py`, which
equal the retained bytes, and the absolute input paths of the run, a worktree of
`claude/bold-ritchie-xo28us-l36` at `8668f03c6`.
[frozen/](frozen/) keeps the review as it stood when its findings were frozen.

An earlier review of these packets, at the strong tier (`tbd-strong`) and the xhigh
reasoning setting, accepted both certificates before this one ran. It is not the review
of record, and neither it nor its programs are retained; this review’s reconciliation
section reads each of its findings.

## How to Run

From any directory, with a checkout of this repository at `REPO`:

```bash
PY=REPO/packing/.venv/bin/python3 programs/run.sh REPO OUT [UPSTREAM]
```

`UPSTREAM` is an optional directory holding the bare clones `s299.git` and `s204.git` of
kenaznia-doga/s299-upper-bound and kenaznia-doga/s204-upper-bound (`git clone --bare`).
Without it the custody step is skipped.
The script runs each program as `python3 -I -B`, one at a time, with BLAS pinned to one
thread. The final run on 4 November 2026 took 40 wall seconds and 34.0 CPU-seconds, on a
shared four-core host under `nice -n 10`. The host’s load from other lanes was between 5
and 8.

## The Programs

| Program | What it does | Decides | CPU (final run) |
| --- | --- | --- | --- |
| `ozlib.py` | The library: a fail-closed reader for the Witness/v2 block layout, a JSON reader, a reader for Evan Daniel’s `.cert` layout, method 1 (separating axes over the four edge normals in `fractions.Fraction`) and method 2 (exact corners, Sutherland–Hodgman clipping and shoelace areas in `gmpy2.mpq`) | — | — |
| `oz_check.py` | Decides one certificate: every format hypothesis (Witness/v2 envelope, `n`, count, unique ids, side, unit size, centre-basis, rational, lower-left origin, axes); the export’s squares equal exactly; every basis exactly unit in both kernels and every square’s corner area 1; every wall by both methods; every pair by both methods with no distance filter; the methods agree everywhere. It also reports the exact squared distance of the 40 nearest pairs | **yes**: the bound | 5.88 s (299), 2.84 s (204) |
| `oz_controls.py` | Sixteen sharp controls and mutants, each with its expected outcome stated before it runs, decided by both methods. A, B, C: the box, a translation and the least-margin pair at exact contact and $10^{-30}$ past it. D: every pair below $10^{-9}$ closed the same way. E: every square alone to its nearest wall. F, G: one square enlarged to its pair and to its wall. H: a duplicate. I: a square out of the box. J: a non-unit basis. K: the count and the ids. L: the reversed rotation sense | controls only | 11.71 s (299), 5.73 s (204) |
| `oz_selftest.py` | The two methods on cases with known answers: edge, corner and vertex-edge contacts and their $10^{-30}$ overlaps; a duplicate; the concentric overlap $5/6$ of a unit square and its rotation by basis $(3/5, 4/5)$. Also walls, a non-unit basis, and 3,000 random rational pairs taken to exact contact, $10^{-30}$ past it and $10^{-30}$ short of it | the evaluators’ correctness on known cases | 3.62 s |
| `oz_sides.py` | Each side’s exact decimal, its floor and ceiling at 12 and 16 places, each issue’s print against it, the house’s side, and the lane’s stated decimals, ceilings and differences | nothing about feasibility | 0.01 s |
| `oz_identity.py` | Checks the house witness against Daniel’s `.cert` exactly. Measures the candidate against the house under the box’s eight symmetries, by nearest centres and by an optimal assignment, counting moves, turns, tilts and the order of the squares | nothing (a measurement) | 0.09 s (299), 0.04 s (204) |
| `oz_compare_lane.py` | Turns the maintained routes’ $(x, y, t)$ poses back into bases and holds them to the certificate exactly. Compares the routes’ minima and the lane’s identity and sharp-control receipts with this review’s | nothing (a comparison) | 0.02 s, 0.02 s |
| `oz_custody.py` | Read-only git plumbing on the bare clones: refs, the commit count, the pin, its tree, author and committer; every blob’s SHA-256 against the packet’s manifest, its retained copy (gzip decompressed, header checked) and the issue’s stated digests; licence files and licence words in every text blob | custody only | 0.03 s |
| `oz_repair.py` | Undoes the 299 export’s stated “exact radial repair” (scaling about $(1/2, 1/2)$ by $r = 1 + 9.00000001 \times 10^{-14}$). It reports the decimal places of the pre-images and the pre-repair packing’s overlaps, exactly | nothing (how the certificate was made) | 3.97 s |
| `run.sh` | Runs everything above | — | — |

`oz_check.py` with `ozlib.py` is the deciding program; `oz_controls.py` and
`oz_selftest.py` are its controls.
`oz_sides.py`, `oz_identity.py`, `oz_compare_lane.py`, `oz_custody.py` and
`oz_repair.py` decide nothing about the bound.
An evidence entry may cite them as measurements, or none may.

## What They Printed

| Receipt | Verdict | The numbers |
| --- | --- | --- |
| `check-n299.json` | `ACCEPT` | 299 squares, ids 1–299, all 1,196 scalars in lowest terms; 117 bases off the axes, all exactly unit; the export identical; walls: least clearance exactly 0, 43 square–wall contacts on all four walls (9 left, 11 right, 8 bottom, 15 top), all of upright squares; 44,551 pairs disjoint by both methods, no disagreement, none touching; least margin $99991899999991/10^{36} \approx 9.99919 \times 10^{-23}$ (squares 224 and 235), then $2.0 \times 10^{-14}$; 562 pairs below $10^{-12}$; for the 40 nearest pairs the exact distance equals the margin |
| `check-n204.json` | `ACCEPT` | 204 squares; 83 bases off the axes, all exactly unit; the export identical; walls: least clearance $9.9999999995 \times 10^{-18}$ (square 39, bottom), exactly $10^{-17}$ on the other three walls; 20,706 pairs disjoint by both methods, none touching; least margin $9.99999978848 \times 10^{-18}$ (squares 23 and 39); 387 pairs below $10^{-15}$ |
| `controls-n299.json`, `controls-n204.json` | `EVERY_CONTROL_AS_EXPECTED` | All 16 controls, the 562 and 391 near pairs of D, and the 299 and 204 squares of E were decided as stated beforehand, by both methods. Under the reversed sense 100 pairs overlap at each count |
| `selftest.json` | `PASSED` | 13 pair cases, 5 wall cases, the non-unit basis, and 3,000 random pairs, each at contact, past and short |
| `sides.json` | — | 299: the side is $17.801238533979062111469738103353397755$, exactly (36 places). Its 12-place ceiling is $17.801238533980$; #893’s $17.801238533979$ is the floor, $6.2111 \times 10^{-14}$ below, and bounds nothing. The side is $1.5409521973210 \times 10^{-8}$ below the house. 204: the side is $14.807620995585208018039159918$ (27 places). #894’s $14.807620995586$ is the 12-place ceiling and bounds. The side is $6.4762963716094 \times 10^{-6}$ below the house. The lane’s decimals, ceilings and differences are all exact |
| `identity-n299.json` | — | The house witness equals `s299_1028.cert` exactly. Only the identity pairs the squares one to one by nearest centres, and that pairing is the optimal assignment. Moves: 290 squares beyond $10^{-9}$, 198 beyond $10^{-6}$, 156 beyond $10^{-3}$, 119 beyond $10^{-2}$, 44 beyond 0.05, 12 beyond 0.1, 6 beyond 0.25 and 1 beyond 0.5; the largest is 0.501947, and 255 squares lie within 0.05. The largest turn is 14.90°, by one square, and 5 squares turn by more than 1°. Beyond 1° there are 85 tilted squares against 87, all of one sense. No square keeps its id |
| `identity-n204.json` | — | The house witness equals `s204_1028.cert` exactly. Only the identity pairs the squares one to one, and every square keeps its id. Moves: 191 squares beyond $10^{-6}$, 118 beyond $10^{-3}$, 81 beyond $10^{-2}$, 24 beyond 0.05 and 6 beyond 0.1; the largest is 0.18968. The largest turn is 25.58°, and 14 squares turn by more than 1°. Beyond 1° there are 76 tilted squares against 79, all of one sense |
| `compare-lane-n299.json`, `compare-lane-n204.json` | — | The routes’ positive poses are the certificate’s squares exactly. Their duplicate and outside controls differ from it only where they say. Their least gap, least clearance and pair counts equal this review’s, and so do their identity counts. Their `turned_beyond_1e-6` is a count beyond $10^{-6}$ radians (71 and 87; `identity-n*.json` records `turned_beyond_1e-6_rad`) |
| `custody.json` | `CUSTODY_HOLDS` | Each upstream repository holds one commit, at its pin, and the trees match `sources.json`. Every blob matches the packet’s manifest and its retained copy, and the gzip header carries no name or time. The issue-stated digests match. There is no licence file and no licence word in any text blob |
| `repair-n299.json` | — | Every centre maps back to a decimal of at most 14 places (61 to one place), and $S_0 = 17.80123853397755$. The pre-repair packing has 79 overlapping pairs, the worst $-9.0 \times 10^{-14}$ (squares 224 and 235), and one square $2.6 \times 10^{-15}$ outside its box; the repair clears them all |

The whole review, with its development runs, used about three CPU-minutes.

## After the Freeze

The review’s findings were frozen at SHA-256
`343acbda38ec7b70e3b2ad1a2f78ab2b894f1ae5faf4ce87803f4fc9adb123f6`
(2026-11-04T06:53:07Z), kept as
`frozen/review-2026-11-04-ozden-893-894-299-204.frozen.md`. Only then did its author
read the earlier review of these packets, the wording diff to `b7946bd41`, the author’s
`verifier/sqcheck.py` and `verifier/README.md`, and the registry record of
`V-check-rational-witness-independent`. Every program and receipt here was last written
before the freeze (06:49:51Z at the latest), and none changed afterwards.

## Suggested Registry Records

For the records lane; nothing here writes them.

- **`verifiers.yaml`.** One deciding program, `oz_check.py` with `ozlib.py`, at the
  digests the receipts record, with `oz_controls.py` and `oz_selftest.py` as its
  controls. Its `independence` record:
  - `read`: `mathematics`, `specification` (the Witness/v2 schema text),
    `certificate-format`, `producer-output`. The bytes were final before `producer-code`
    (`sqcheck.py`) and `earlier-review` were read, and the note should say so;
  - `clean_room: true`, `shares: []`;
  - `written_by`: Claude, the stage 4 mathematical review lane of `think-ybep`, strong
    tier `tbd-strong-max` at maximum reasoning;
  - `overlaps_producer`: `extent: system-family`, `separate_prompt: true`,
    `separate_code: true`. The author’s own check ran this repository’s
    `packing-witness verify`, co-authored by Claude agents, and the same lab’s #890 says
    Claude agents ran its checks.
    The 299 search used GPT-based agents.
- **`evidence.yaml`.** At each count, an exact-feasibility entry for this review’s run:
  `method: exact-algebraic`, `origin: replayed-here`, `performed_by: repository`,
  `relationship_to_generator: independent-implementation`, `replay_status: passed`,
  coverage `full` (every wall and every pair by two methods), the certificate path, and
  `programs/run.sh` or the `oz_check.py` command as the replay.
  Its controls are `out/controls-nNNN.json` and `out/selftest.json`. The review document
  is the `independence_record` and the `external_review` on
  `E-ozden-893-certificate-report` and `E-ozden-894-certificate-report`.
- **`results.yaml`.** Both entries list the review under `reviews` (`adversarial`, `ai`,
  `accepted`) and keep S2 with `by` naming it.
- **Measurements.** `oz_sides.py`, `oz_identity.py`, `oz_compare_lane.py`,
  `oz_custody.py` and `oz_repair.py` decide nothing.
  They are kept and may be cited as measurements, or by no entry.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
