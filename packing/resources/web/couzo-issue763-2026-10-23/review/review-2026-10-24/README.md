# Stage 4 Review of #763 at 268 and 303: Programs and Outputs

The code of the stage 4 mathematical review of 24 October 2026
([review-2026-10-24-couzo-n268-n303.md](../../../../../../docs/project/reviews/review-2026-10-24-couzo-n268-n303.md),
bead think-zjus), kept as
[epistemics.md, Every Run’s Code Is Kept](../../../../../../epistemics.md#every-runs-code-is-kept)
requires. It reviews the two certificates of Francisco Couzo’s issue #763 in the case
corpus, `source/certificates/best/n268.cert` and `n303.cert` of this packet, at
franciscouzo/square-packing@964ee2b.

The reviewer wrote all four programs: Claude, strongest tier (`tbd-strong-max`), maximum
reasoning, as lane c-review-t240-math for the intake coordinator.
Each reads the certificates and every other packing as data.
No program runs or imports code from the source, from Evan Daniel’s repository, or from
this repository’s `sqpack` or `devtools`; the only libraries are Python’s standard
library (`fractions` for every exact decision), NumPy, SciPy (`linear_sum_assignment`,
`maximum_bipartite_matching`) and PyYAML. `agree.py` loads `check_certificates.py` by
path for its reader.

## Independence

- **Read:** the mathematics (the separating-axis theorem for convex polygons, exact
  polygon clipping, optimal and bottleneck assignment), and the certificate format as
  the certificates’ own comment line states it, “unit squares, centre (x, y), rotation t
  = tan(theta/2)”.
- **Not read:** the source’s checkers (`verify_bound_certificate.py`,
  `certificate_constructions.py`), Evan Daniel’s checkers and measurement code, and this
  repository’s `sqpack.verify`, `devtools.check_rational_witness_independent`,
  `devtools.upper_bound_reports`, `devtools.evand_exact_certificates`,
  `devtools.evand_arrangement_reports` and every identity tool, among them the
  `measure/identity.py` of the 22 and 23 October packets at 303.
- **Clean-room:** yes.
  The checker shares with the two maintained routes only what the format and the
  mathematics fix: the half-angle conversion, Python’s `Fraction`, and, for route A, the
  separating-axis method.
  Its route B, the exact area of the clipped intersection, is a second method.
- **Who wrote it:** the reviewer, a Claude agent.
  The source’s commit at the pin and its two parents end with “Co-Authored-By: Claude
  Opus 5.5”, so the producer used the same system family.

## The Programs

| Program | What it does | Role |
| --- | --- | --- |
| [check_certificates.py](check_certificates.py) | Parses each certificate strictly; checks its digest against the manifest, its header side against the record’s claim and its 12-place print; decides containment and pairwise disjoint interiors exactly on two routes (A: separating axes over every pair, with corners against the walls; B: exact clipped area over the pairs within √2·(h_i + h_j), with each square’s support against the walls); runs ten controls per certificate | **Decides** s(268) and s(303) at the stated sides |
| [agree.py](agree.py) | Holds the checker’s reader and route A to the maintained replay’s receipt (`receipts/exact-certification.json.xz`): the side and every pose as exact rationals, the pairs decided, the least pair gap and the least wall clearance, and the receipt’s two controls | Decides nothing |
| [identity.py](identity.py) | Pairs each two packings of a count by optimal assignment (least summed squared centre distance) over the 8 symmetries of the box, about the box centres; counts squares moved beyond 0.1 and 1e-3, the largest move, turns, whether nearest centres pair one to one, the bottleneck and reversed tilts, with four alignment and cost variants and the runner-up symmetry | Decides nothing: it measures identity and lineage |
| [sides.py](sides.py) | Reads every stated side exactly and compares it with the #763 sides; checks the record’s decimals; checks that every bound at the later counts 269 to 288 and 304 to 320 lies above | Decides nothing about the bound: it compares stated sides |

Route B’s distance filter is a proof, not a heuristic: a square of half-edge h lies in
the closed disc of radius h√2 about its centre, its interior in the open disc, so two
squares whose centres are at least √2·(h_i + h_j) apart have disjoint interiors.
The comparison is exact, of squared distances against 2(h_i + h_j)².

## The Controls

Each certificate gets ten controls, built in memory by an exact rule from its closest
pair (least separating-axis gap) and its square nearest a wall, and each is decided by
both routes:

| Control | Expected | 268 | 303 |
| --- | --- | --- | --- |
| A square replaced by a copy of its closest neighbour | refused | refused (101, 223) | refused (46, 58) |
| A square moved halfway to its closest neighbour’s centre | refused | refused | refused |
| A square moved to exact contact with its closest neighbour, along the line of centres (2.10e-13 at 268, 2.93e-13 at 303) | accepted, one pair at gap 0 | accepted | accepted |
| The same move plus 1e-30 of the centre distance | refused | refused | refused |
| The square’s half-edge enlarged by the pair’s gap plus 1e-30 | refused | refused | refused |
| The square nearest a wall enlarged by its clearance plus 1e-30 | refused | refused (square 3) | refused (square 4) |
| The box at the packing’s exact extent | accepted | accepted | accepted |
| The box 1e-30 below the extent | refused | refused (15 squares) | refused (square 172) |
| Two malformed texts (header count plus one; a decimal token) | refused by the parser | refused | refused |

Reported, not required: with every rotation reversed (t to −t), 94 pairs overlap at 268
and 106 at 303 on both routes, so the certificates hold under the counter-clockwise
reading of t and not under the other.

## How to Run

From `packing/`, with the project interpreter:

```bash
R=resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24
uv run --frozen --all-extras --group dev python -I $R/check_certificates.py \
  --out $R/out/check-certificates.json
uv run --frozen --all-extras --group dev python -I $R/agree.py --out $R/out/agree.json
uv run --frozen --all-extras --group dev python -I $R/identity.py \
  --evand EVAND --out $R/out/identity.json
uv run --frozen --all-extras --group dev python -I $R/sides.py \
  --evand EVAND --out $R/out/sides.json
```

`agree.py` reads `out/check-certificates.json`, so it runs after the checker.
`EVAND` is a directory holding Evan Daniel’s files at
[evand/square-packing@8a8879a](https://github.com/evand/square-packing/tree/8a8879a2972c32cbd2d906049228cc9f0762b02a)
under their own paths, which this packet does not retain (their import is think-l49q’s),
for example
`git -C CLONE show 8a8879a:search/packer/candidates/s268_lightning.cert > EVAND/search/packer/candidates/s268_lightning.cert`.
The review ran each program on 24 October 2026 with CPython 3.14.7
(`packing/.venv/bin/python3 -I`, the same interpreter) under `nice`, one at a time, from
the `packing/` of a worktree at #789’s head `0329f73d6`.

## What They Read

| Input | SHA-256 |
| --- | --- |
| `source/certificates/best/n268.cert` (#763 at 268; Git blob `7b9a04c2`) | `e9833bf26e1bf7e4719ee983c91979ba51f7319d6caa8dd1911fce820903e07e` |
| `source/certificates/best/n303.cert` (#763 at 303; Git blob `53c90da7`) | `39a150f4cce7e435b0b7d6d82dbf15d172611e07c413e1abe9d61cf90822791a` |
| `source/certificates/parents/85dbd707….cert` (Tymchishin’s v4, the 268 parent) | `85dbd707746197d31f62dd52b4e580dfb90097498a4970c577f776ce7de2df46` |
| `source/certificates/parents/22f07a7c….cert` (Couzo’s Kaggle push, the 303 parent) | `22f07a7c318328d257d1a7efd9c5acb05e3286650a94da751592b21014424244` |
| `source/certificates/best/n304.cert` (the source’s 304, which #763 does not claim) | read for its side only |
| `receipts/exact-certification.json.xz` (the maintained replay) | read by `agree.py` |
| `packing/witnesses/known-best/n-268.yaml` (W-known-best-n268, T-174) | `b76effe9957493699f32a32c643b503f0832785508f578052cb9f120f1d89b4a` |
| `packing/witnesses/known-best/n-303.yaml` (W-known-best-n303, T-239) | `849ad745f1bb049f1c4a9a2be7ed4f566308781f9d1561233e8d662a8413bf1e` |
| `evand-n303-2026-10-22/source/search/packer/candidates/s303_r303w0.cert` (T-230) | `929c2acf72ee54a1850183fc149f06dbf35bffa2f7ee68c8f833d888400e8080` |
| `packing/frontier/n-269.md` to `n-288.md` and `n-304.md` to `n-320.md` | their upper bounds, read by `sides.py` |
| evand 8a8879a `s268_lightning.cert` (blob `74bd5df5`) | `c87da316589dd3843e9344e5461add99c4f80ca495ba862f302bf958bc154a49` |
| evand 8a8879a `s268_lightning.input.txt` (blob `c5be851b`), Lavrentev’s public packing as Daniel’s input | `7823b7158619c3f971a469d9eadc02015b49babba638e2661b83ea8aecd9cfbe` |
| evand 8a8879a `s268_lightning.predescent.txt` (blob `357d575c`) | `b413d658b629f8a5dd35723f61109d32f5b800fc3ab1d72e45fb49c0116997ac` |
| evand 8a8879a `s303_cdeotte.cert` (blob `ea0ebc42`), Deotte’s public packing as Daniel certifies it | `6cf9cc95a48f957d6dc5c283430da4d453af3a3635eb58b34a8d7af93e09e746` |

`sides.py` also holds four side-only Kaggle leaderboard values as constants, each with
the file it was read from: Minal kharat123’s and Lucas Boesen’s from the retained
`source/public_bounds.json.gz` at 964ee2b, and panpanpanda’s and pjmathematician’s from
`public_bounds.json` at the source’s later commit `43f666c`, read from a watched clone
and not retained.

## What They Printed

The transcripts are in `out/` beside the JSON receipts, which hold every figure.

- **check_certificates.py** ([transcript](out/check-certificates.txt)): “verdict: all
  positives accepted and all controls met”.
  Both digests match the manifest, both header sides equal the claimed exact sides, and
  both 12-place prints round up to the claimed 16.874361715874 and 17.906978233799.
  Route A decided all 35,778 pairs at 268 and all 45,753 at 303; route B decided the 668
  and 701 pairs within the discs.
  Least gap on the edge normals 2.0963e-13 at 268 (squares 101 and 223) and 2.0718e-13
  at 303 (46 and 58); least wall clearance 1e-15 at both (squares 3 and 4); each
  packing’s extent is 2e-15 below its stated side.
  Every control met its expectation, both routes agreeing.
  34.6 CPU seconds. A second run gave a receipt identical apart from its CPU times
  ([out/second-run/](out/second-run/check-certificates.txt)).
- **agree.py** ([transcript](out/agree.txt)): 24 of 24 checks equal.
  The maintained run read the same sides and the same 268 and 303 poses, literal for
  literal; both of its routes decided every pair, and their least pair gaps and least
  wall clearances equal route A’s exactly; both refused the receipt’s two controls.
- **identity.py** ([transcript](out/identity.txt)): the table in the review.
  At 268 no square of #763 is beyond 0.1 of Tymchishin’s v4 parent (largest 5.91e-2, 176
  beyond 1e-3, under the reflection x ↦ s − x, nearest centres one to one), and 118 are
  beyond 0.1 of T-174’s (119 under the sum-of-distances cost; one to one under no
  symmetry); at 303 three are beyond 0.1 of Couzo’s push parent (squares 230, 264 and
  289; largest 0.309; one to one), and 125 and 133 beyond 0.1 of T-230’s and T-239’s
  (123 to 125 and 131 to 134 across the variants; one to one under no symmetry).
  Run on T-230 against T-239 it gives 12 beyond 0.1, 31 beyond 1e-2, 72 beyond 1e-3, the
  largest move and bottleneck 0.547, 16 turned beyond 1° and 91 and 96 tilted squares.
  2.1 CPU seconds.
- **sides.py** ([transcript](out/sides.txt)): #763 is 4.453e-3 below T-174, 1.106e-3
  below its 268 parent and 4.480e-12 above Daniel’s 8a8879a certificate at 268; 2.784e-3
  below T-239, 2.794e-3 below T-230, 4.948e-4 below its 303 parent and 2.600e-4 below
  Daniel’s certificate of Deotte’s packing at 303. Every bound at 269 to 288 lies above
  the 268 side (least margin 2.715e-2, at 269) and every bound at 304 to 320 above the
  303 side (2.245e-2, at 304); the source’s own 304 certificate is 1.992e-2 above.
  The record’s 303 decimal is a truncation of the exact side and its 268 decimal a
  rounding (…8254… printed …83…). 0.2 CPU seconds.

The whole review used about 0.08 CPU-hours on the shared host, most of it the checker’s
two runs, a trial run at 268 and reading the source’s history;
`out/program-digests.sha256` lists every program’s SHA-256 as run.

## Changes After the 23 October Review Was Read

The review’s findings were written before its author read the 23 October review at 303.
Afterwards `agree.py` was added, `identity.py` gained the one-to-one test, the
bottleneck and the reversed tilts, and `sides.py` gained the later counts, each to
report in the record’s words what that review reports; `check_certificates.py` did not
change, and its second run came after.
No figure of the earlier runs changed.

## Evidence

`check_certificates.py` decides both bounds and is the program the review’s evidence
entry cites. `agree.py`, `identity.py` and `sides.py` decide nothing and are cited by no
evidence entry; they are kept as the review’s measurements.
The drafted `verifiers.yaml` records and evidence entries are in
[record-changes.md](record-changes.md); the records lane registers them.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
