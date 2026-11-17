# Programs and Receipts of the Stage 4 Review of #914 (5 November 2026)

These are the programs, receipts and frozen findings of
[the stage 4 review of Evan Daniel’s seven certificates of #914](../../../../../../docs/project/reviews/review-2026-11-05-evand-914-seven.md),
laid out to be kept as the packet’s `review/review-2026-11-05/`
(`packing/resources/web/evand-issue914-2026-11-05/review/review-2026-11-05/`).
A separately prompted review lane (Claude, strong tier `tbd-strong-max`, maximum
reasoning, bead `think-lrj4`) wrote every program here for this review. None imports
code of this repository or of the source; they read the certificates and the other
files named below as data.

## Layout

| Path | What it is | Keep |
| --- | --- | --- |
| `review-2026-11-05-evand-914-seven.md` | the review | lands in `docs/project/reviews/` |
| `frozen-findings.md`, `frozen-findings.sha256` | the findings as frozen before the lane’s receipts and the earlier reviews were read, and their digest and time | yes |
| `programs/` | the 13 programs and `run_all.sh` | yes |
| `out/` | the receipts of the final run (below) | yes, except as marked |
| `out/controls-v1-g2-misconstructed/`, `out/controls-v2-parallel-axes/` | two earlier control runs, kept because they ran (see `sharp_controls.py`) | yes |
| `out/houses/` | copies of main’s house witnesses and T-257’s three certificates, taken by `git show` at main `81f06acb3` | `SHA256SUMS.txt`, `main-commit.txt` and `ADOPTED-excerpt.txt` only; the rest is main’s own files |
| `out/issue914/` | issue #914 as GitHub’s REST API returned it at about 22:21Z on 5 November, and its body | yes |
| `out/upstream-bb4cc78/` | this review’s own blobless fetch of evand/square-packing at `bb4cc78` | `added-files.txt`, `upstream-sha256.txt`, `commit-log.txt`, `readmes/`; not `repo/` |

`out/program-digests.txt` holds the SHA-256 of every program as the final run read it.

## How to Run

From `packing/`, with the project interpreter (CPython 3.14.7), at most two processes,
at `nice -n 19`:

```bash
R=<this directory>
C=resources/web/evand-issue914-2026-11-05/source/search/packer/candidates
S=resources/web/evand-issue914-2026-11-05/source
bash $R/programs/run_all.sh .venv/bin/python3 $C $S $R
```

The inputs fetched once are `out/houses/` (recreate with
`git show 81f06acb3:packing/witnesses/known-best/n-NNN.yaml` and
`git show 81f06acb3:packing/resources/web/evand-issue845-2026-10-29/source/search/packer/candidates/s{204,260,293}_1028.cert`),
`out/issue914/issue914.json` (`gh api repos/jlevy/squares/issues/914`) and
`out/upstream-bb4cc78/` (a blobless `git fetch --depth 2` of the commit, then
`git diff --name-status` against its parent and `git show bb4cc78:PATH | sha256sum`).
The final run took 6 min 29 s of CPU (3 min 32 s of wall time on two cores).

## The Programs

| Program | Decides | What it does | Reads | Printed (final run) | CPU |
| --- | --- | --- | --- | --- | ---: |
| `cert_reader.py` | (module) | strict reader of the certificate format: one header `n S`, n rows of three rationals, comments, LF only; refuses anything else | — | — | — |
| `exact_geometry.py` | (module) | method A, separating axes in `fractions.Fraction`; method B, exact clipped areas (Sutherland–Hodgman, shoelace) in `gmpy2.mpq` with its own corner construction from t = p/q | — | — | — |
| `decide_feasibility.py` | yes: feasibility of one file | every wall and every pair by both methods, no distance filter; three classes per pair (separated, touching, overlapping) that must agree; `--sense -1` reads the rotation reversed | one certificate | 13 files accepted by both methods, every pair separated; reversed sense: all 13 refused | 107.9 s and 106.8 s |
| `sharp_controls.py` | yes: 14 control instances per file | box at its extent and 1e-30 below; packing at the near walls and 1e-30 past; least-gap pair closed and 1e-30 past; least-clearance square to its wall and 1e-30 past; least closing enlargement and 1e-30 more; duplicate; square outside; all squares turned to t = 0 | one certificate | 182 controls, all as stated | 142.5 s |
| `self_test.py` | premise: the deciders | 19 known answers, 3,000 random rational pairs and 6,000 constructed contacts and 1e-30 overlaps decided by both methods; 14 malformed files refused by the reader | — | PASS | 10.4 s |
| `sides_and_kkt.py` | nothing | header sides against the claim fractions and the issue’s prints; extents; the KKT certificates and views against their 80-digit points; the 260 certificate against its binary64 input; house sides on main | the 13 files, `.exact.txt`, `*_regularized.json`, `.input.txt`, main’s witnesses | as in the review | 0.6 s |
| `house_slack.py` | nothing | exact least wall clearance and least pair gap, and contact lists, of the seven houses, T-257’s 260 and the seven certificates | the same | as in the review | 3.6 s |
| `scale_slack.py` | nothing; written after the freeze | exact least scale about the corner at which each packing touches | the same | as in the review | 3.8 s |
| `identity.py` | nothing | pose-by-pose identity under the box’s eight symmetries: nearest centres, the optimal assignment (own Hungarian, checked against SciPy’s cost), moves, turns, tilts, contacts shared; certificate against house, input and view; calibrations | the same, and `out/slack-and-contacts.json` | as in the review | 5.8 s |
| `island_260.py` | nothing | the 260 tilted island against T-257’s and T-265’s under each symmetry with the best translation | the 260 certificate, T-257’s `s260_1028.cert`, main’s 260 witness | island matches after a half turn and a 1.0011 shift | 3.0 s |
| `tilts.py` | nothing | tilt groups of each certificate and its house, and shared angles | certificates and witnesses | as in the review | 1.2 s |
| `input_260.py` | nothing | the 260 side against its input’s and pre-descent input’s stated sides; the input’s own overlaps at 60 digits | the 260 files | side 1.66e-11 above the input’s, 8.83e-12 above the pre-descent’s; the input overlaps in 19 pairs by up to 3.9e-16 | 0.2 s |
| `custody.py` | premise: digests | the issue’s 13 digests against the packet; the packet against upstream `bb4cc78`; licence; credits | packet source, issue JSON, the upstream fetch’s lists | all digests equal; 55 files equal, 3 equal after gunzip | 0.04 s |
| `run_all.sh` | — | reruns all of the above and writes `out/program-digests.txt` | — | — | — |

The final run’s receipts are `out/self-test.json`, `out/feasibility/*.json`,
`out/reversed-sense/*.json`, `out/controls/*.json`, `out/sides-and-kkt.json`,
`out/slack-and-contacts.json`, `out/scale-slack.json`, `out/identity.json`,
`out/island-260.json`, `out/tilts.json`, `out/input-260.json` and `out/custody.json`,
each with a `.log` where the program prints.

**Development runs, kept or not.** The first runs of every program before the final one
used about 11 CPU-minutes, among them the two kept control runs (143.8 s and 144.9 s):
the first moved square 1 left by 1 for its outside control, which leaves it inside
wherever it sits more than about 1.71 from the left wall (both methods accepted it there,
correctly), and the second left the 1e-30-past expectation unstated where two of a pair’s
axes are parallel. A timing probe of 3,000 pairs and an inline version of `input_260.py`
also ran and decided nothing. In all, the review used about 0.30 CPU-hours.

## For the Registry

Proposed entries for [`verifiers.yaml`](../../../../../frontier/verifiers.yaml), for the
records lane to adapt:

- `decide_feasibility.py` with `exact_geometry.py` and `cert_reader.py`: first-party,
  decides the feasibility of each file (13 files, every wall and every pair: coverage
  `full`), by two exact methods.
  `relationship_to_generator: independent-implementation`.
  Independence: `read: [mathematics, certificate-format, producer-output]` (the format
  from the certificates’ first line and the issue; the producer’s stored points, inputs
  and JSON reports, read to compare); `clean_room: true` (the authors never read
  `verify_cert.py`, `verify_cert2.py` or any producer code, which were hashed only, nor
  this repository’s maintained routes); `shares: []`; `written_by`: Claude (AI review),
  strong tier `tbd-strong-max`, maximum reasoning, the stage 4 review lane;
  `overlaps_producer: system-family`, `separate_prompt: true`, `separate_code: true`,
  noting that issue #914 says the composer, search, checks and request were done with
  Claude, and that the method’s mathematics (separating axes; polygon intersection) is
  the same as the issue describes for the producer’s two checkers.
- `sharp_controls.py`: first-party, decides the control instances (premise for the
  deciders); same independence.
- `self_test.py` and `custody.py`: premise checks; same authorship.
- `sides_and_kkt.py`, `house_slack.py`, `scale_slack.py`, `identity.py`,
  `island_260.py`, `tilts.py`, `input_260.py`: measurements that decide nothing; cited
  by no evidence entry unless the case records cite their measurements.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
