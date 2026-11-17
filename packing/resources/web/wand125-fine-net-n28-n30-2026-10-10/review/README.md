# The Mathematical Review’s Programs, 4 November 2026

These are the programs the
[mathematical review](../../../../../docs/project/reviews/review-2026-11-04-wand125-fine-net-n28-n30.md)
of wand125’s `mixed_n28_L57425` (T-142) and `mixed_n30_L58925` (T-143) wrote and ran on
4 November 2026. They are kept as they ran, with the output each printed in
[`out/`](out/). The review was the stage-4 mathematical review think-4ul6 of the import
think-i85v. It was written by an AI agent, Claude (Anthropic), at the tbd-strong-max
tier with maximum reasoning, prompted separately from the intake and replay lanes and
working in a worktree of its own.

Each program ran with the project interpreter (Python 3.14.7, `python3 -I`, from a
directory of its own), at `nice -n 19` and at most two threads.
Each read as data:

- the packet’s retained `release/` members;
- the two release assets of `square-lower-bounds-v1`, fetched once more into scratch
  space and held to the packet’s size and SHA-256 pins;
- the source’s `README.md`, `bundle.json`, `ASSET.json` and `files-sha256.json` of each
  directory, fetched at the pinned revisions and held to the manifest’s digests.

No program imports anything of the source, the crate or `packing/devtools`, and none
executes anything of the source.
One program run here was not written by the review: this repository’s reviewed
`sqverify-fast`. It was built in the review’s worktree from crate source `d97758bb…`
(binary SHA-256 `567a0fd5…`), and `sample_directions.py` drives it.

## What Its Authors Read

Before writing these programs the lane read several parts of this repository:

- in `packing/sqverify_fast/SOUNDNESS.md`: the claim, N1 to N4, lemma N0, C1, A1, A2, D,
  the acceptance rule, I1, I2, F2, F3 and A3;
- in the crate: `axis.rs` whole; in `certificate.rs`, `d4_images`, `domain_upper`,
  `direction`, the format M reader, the expansion and the premise checks of `admit`;
  `lib.rs`’s `run_direction_inner`; and the branch and bound’s leaf, witness and
  depth-limit bookkeeping in `rotated.rs`;
- the census control’s axis rule in `devtools/sqverify_fast_census.py`, read but not
  run.

It also read the source’s SPEC.md, REPRODUCE.md and `fine_net_check.sh`, as retained in
the 6 October check2 packet with the same Git blobs, and the candidates, receipts and
logs as data.

The producer’s checker is the source’s copy of this repository’s crate.
None of these programs is clean-room with respect to it, and none imports or copies any
of it. `axis_decide.py` decides direction 0 by its own method: exact integer overlaps,
binary64 dot products with a proved a priori error bound, and exact fractions at the
least vertices. It is not a transcription of `axis.rs`.

The source’s commits name Claude as co-author.
These programs were written by a Claude agent, prompted separately from the source and
from the intake and replay lanes.

## The Programs

| Program | What it does | Reads | Output | CPU |
| --- | --- | --- | --- | --- |
| [`fine_net_exact.py`](programs/fine_net_exact.py) | The module the others import. It reads a candidate exactly, refusing duplicate keys and multi-member gzip. It provides the eight $D_4$ images (unmerged), the direction $(c_r, s_r)$, lemma D’s per-bin domain, the rotated core, Sutherland–Hodgman clipping, the exact capture, the axis capture and the source’s semantic digest. | (a module) | — | — |
| [`selftest.py`](programs/selftest.py) | Tests the module on synthetic data. A partition of the core’s neighbourhood sums to $B^2$ exactly at five directions. The axis capture equals the product formula. The capture is invariant under the quarter turn (lemma C1). $c^2 + s^2 = 1$ holds. A seeded wrong clip is caught. | nothing | [`selftest.txt`](out/selftest.txt) | 0.2 s |
| [`check_candidate.py`](programs/check_candidate.py) | Recomputes every exact premise of one candidate. It checks the bytes against the pin, the semantic digest, the keys, format M, `points` empty, and `proof_net` with exactly `step` and `last` and no `net`, `certificate` or `scaling_factor` key. It checks the claim’s $n$ and $L$, and the rows: positive, nondegenerate and inside $K$. It checks the exact mass against `total_mass` and $n - 1/100000$, the distinct images and lemma F3’s caps. It recomputes lemma N0’s (a) to (e), the sharp N3 extent, the last bin (H4), and the per-bin domain at all 2,073 nodes. | the retained `candidate.json.gz`; `source-manifest.json` | [`check_candidate-mixed_n28_L57425.json`](out/check_candidate-mixed_n28_L57425.json), [`…n30_L58925.json`](out/check_candidate-mixed_n30_L58925.json) | 0.25 s each |
| [`check_source_logs.py`](programs/check_source_logs.py) | Reads the source’s run log against the candidate: every direction once, each `verified` at threshold `1`, and the sums and premises of the summary. It checks the check2 receipt, `control.json` and the pre-publication receipt against the candidate, the log and each other. In the 197/200 control log it checks the directions rule and the scaled mass, and rebuilds the mutant file to compare with the logged input digest. It evaluates all 31 oblique witnesses exactly. At the 12 tightest directions it evaluates the leaf box’s centre and four corners exactly. | the retained `check2/` and `verification/` members; `check_candidate`’s output | [`check_source_logs-mixed_n28_L57425.json`](out/check_source_logs-mixed_n28_L57425.json), [`…n30_L58925.json`](out/check_source_logs-mixed_n30_L58925.json) | 4.9 s and 3.5 s |
| [`axis_decide.py`](programs/axis_decide.py) | Decides direction 0 over the whole per-bin domain $[1/2, L - 1/2]^2$, not a quadrant. It takes the event grid of every overlap breakpoint, computes the overlaps exactly in int64, and evaluates every vertex in binary64 with the bound $\gamma_{K+4}$. It then evaluates the lowest vertices, the eight-vertex orbit and 40 random vertices in fractions. It also checks the source’s axis rows, the original and the 197/200 control, at their reported vertex. | the retained candidate, `run.jsonl.gz` and `control-197_200.jsonl.gz` | [`axis_decide-mixed_n28_L57425.json`](out/axis_decide-mixed_n28_L57425.json) (and `.log`), [`…n30_L58925.json`](out/axis_decide-mixed_n30_L58925.json) | 17.9 s and 6.9 s (two BLAS threads); a first pair of runs without the subnormal field took 15.2 s and 6.5 s |
| [`custody_and_nested.py`](programs/custody_and_nested.py) | Reads both assets in memory. It checks size and SHA-256 against the pins, every member against the manifest, and the packet’s retained copies against the members. It checks the sealed bundle against its own `files-sha256.json`. It recomputes the nested verifier’s build digest by its own `build.rs` rule, and compares it file by file with `packing/sqverify_fast` at `e020eb1e2`, `34e87a86b` and this tree’s head. | the two assets; the packet; `git show` of the three revisions | [`custody_and_nested.json`](out/custody_and_nested.json) | 0.3 s |
| [`check_source_docs.py`](programs/check_source_docs.py) | Checks the four fetched documents of each directory against their pins. It recomputes `bundle.json`’s net block, digests and comparison exactly. It checks the files the README names against the asset and the sealed bundle, and the README’s pinned edition against the sealed one. It reads the shipped `fine_net_check.sh` for the receipt shape it writes and for its mutant and directions rules. It identifies the bundle’s `SOUNDNESS.md` by Git blob, and checks whether it or the archive’s copy says anything for a declared net. | the fetched documents; the assets; `git show e020eb1e2` | [`check_source_docs.json`](out/check_source_docs.json) | 0.1 s |
| [`sample_directions.py`](programs/sample_directions.py) | Runs the reviewed `sqverify-fast` with `--confirm` and two threads at six directions of each certificate. They are the four least-bound directions of the source’s log, the direction with the most nodes and one seeded random direction, none of them a direction the intake lane sampled. It compares each row with the source’s, evaluates every leaf box’s centre and corners exactly, and reads the summary’s premises as the 6 October checklist’s item 3. It then runs the 99/100 mutant at three directions and evaluates each refusal exactly. | the retained candidate and run log; the binary | [`sample_directions-mixed_n28_L57425.json`](out/sample_directions-mixed_n28_L57425.json), [`…n30_L58925.json`](out/sample_directions-mixed_n30_L58925.json) | binary 29.9 s and 35.0 s; Python 2.0 s and 1.1 s |

The receipts name the candidate by the scratch path it was read from, which was the
packet’s `release/certificates/<directory>/candidate.json.gz`, and carry its SHA-256.

## How to Run Them

From a directory of its own, with `$PY` the project interpreter, `$PACKET` this packet,
`$C` one of `$PACKET/release/certificates/mixed_n28_L57425` or `…/mixed_n30_L58925`,
`$ASSETS` a directory holding the two release assets, `$DOCS` a directory holding `n28/`
and `n30/` with the four fetched documents each, `$REPO` the repository root and
`$BINARY` the reviewed build:

```sh
$PY -I programs/selftest.py
$PY -I programs/check_candidate.py $PACKET mixed_n28_L57425 28 2297/400 --out out/check_candidate-mixed_n28_L57425.json
$PY -I programs/check_candidate.py $PACKET mixed_n30_L58925 30 2357/400 --out out/check_candidate-mixed_n30_L58925.json
$PY -I programs/check_source_logs.py $C out/check_candidate-<directory>.json --out out/check_source_logs-<directory>.json
OPENBLAS_NUM_THREADS=2 $PY -I programs/axis_decide.py $C/candidate.json.gz \
    --source-run $C/check2/run.jsonl.gz --control $C/check2/control-197_200.jsonl.gz \
    --out out/axis_decide-<directory>.json
$PY -I programs/custody_and_nested.py $PACKET $ASSETS $REPO e020eb1e2 34e87a86b HEAD --out out/custody_and_nested.json
$PY -I programs/check_source_docs.py $PACKET $DOCS $ASSETS $REPO --out out/check_source_docs.json
$PY -I programs/sample_directions.py $BINARY $C 28 2297/400 --directions 1088,1989,1883,1397,2070,463 \
    --mutant-directions 0,1088,2070 --mutant-factor 99/100 --threads 2 --out out/sample_directions-mixed_n28_L57425.json
$PY -I programs/sample_directions.py $BINARY $C 30 2357/400 --directions 1585,692,283,1267,2071,1185 \
    --mutant-directions 0,1585,2071 --mutant-factor 99/100 --threads 2 --out out/sample_directions-mixed_n30_L58925.json
```

The documents were fetched from
`https://raw.githubusercontent.com/wand125/square-packing/<pin>/problems/square-lower-bounds/certificates/<directory>/<file>`,
and the assets from the release’s download URLs in `source-manifest.json`.

## What They Printed

- **`selftest`.** Six passes, the seeded wrong clip among them.
- **`check_candidate`.** Both: `ALL_PREMISES_HOLD`.
  - The bytes equal the pins (`5ef20511…`, `981a17db…`) and the semantic digests are
    `a1ea15ca…` and `716bcb62…`.
  - There are 631 and 463 rows, all positive, nondegenerate and inside $K$, with masses
    $2799999/100000$ and $2999999/100000$, equal to `total_mass` and to $n - 1/100000$.
  - The images number 5,036 and 3,672 distinct of 5,048 and 3,704: 3 and 8 rows have
    coincident images. The merged images integrate to the mass.
  - The densest image density is 77,055 and 53,206; eight times the densest row is
    $4.93 \times 10^6$ and $3.41 \times 10^6$, below $2^{32}$.
  - Lemma N0 holds with $B(1 + D) = 25009997/25010000$,
    $t_{\max}^2 + 2t_{\max} - 1 = 367/6255001$ and the tangent form
    $500400014977/500400075000$. The last bin $[4143/10004, 4145/10004]$ holds
    $\tan(\pi/8)$.
  - The per-bin domain is nonempty and increasing at every node.
    Its least width is 4.328 and 4.478, at node 2072.
- **`check_source_logs`.** Both: `SOURCE_RECORDS_CONSISTENT`.
  - Each run log has 2,073 rows, every one `verified` at `1`, with the summary’s sums
    and premises recomputed.
  - Each receipt embeds that summary.
    The control is the 197/200 mutant at $\mathrm{round}(2072 i/31)$.
  - The mutant files rebuilt by the shipped script’s rule have the logged input digests
    (`10db6906…`, `545519bb…`).
  - All 62 oblique witnesses lie in the per-bin domain, with captures below one equal to
    the crate’s rationals.
  - All 120 leaf poses capture at least their bound and one, the least 1.00225 and
    1.00257.
- **`axis_decide`.** Both directions 0 are decided: `decided_verified` true.
  - The least vertex is 1.0014141499366 for n = 28 (8,212² vertices) and 1.0017528835255
    for n = 30 (6,032²). Each least vertex lies on an orbit of eight vertices, which
    holds the source’s argmin.
  - The source’s certified axis bounds lie $2.18 \times 10^{-9}$ and
    $1.90 \times 10^{-10}$ below the exact captures.
  - The 197/200 control’s axis refusals are exact, 0.98639 and 0.98673.
- **`custody_and_nested`.** Both assets, every member and every retained copy equal
  their pins. Each sealed bundle matches its own manifest.
  - The nested archive has 20 files and the build digest `ab6e33e1…`. Against
    `e020eb1e2`, 16 files are byte-identical and `src/certificate.rs` is +32 −2.
  - Its duplicate-key reader is identical to the one at all three revisions.
  - Its admission reads `proof_net` with exactly `step` and `last`, refuses it beside
    metadata or outside format M, and checks the tangent form for the per-bin domain.
    It reads no `count` and has no refusal of a top-level `net` key.
    These are recorded as facts only, and no line of the archive is kept.
  - The head’s crate digest is `d97758bb…`.
- **`check_source_docs`.**
  - The documents equal their pins, and `bundle.json`’s exact values hold.
  - The README names the absent `check2/control.jsonl.gz`. Its pinned edition adds the
    four-line “Pre-publication check” section to the sealed one.
  - The shipped script writes the `build` receipt shape, not the published
    `fine-net-check2-receipt/v1`.
  - The bundle’s `SOUNDNESS.md` is Git blob `cadf59b6…`, the edition at `e020eb1e2`,
    with nothing on `proof_net`.
- **`sample_directions`.** Both: `SAMPLE_AGREES`.
  - Twelve directions are `verified`, each row equal to the source’s in verdict, nodes,
    leaves, depth, bound and least-bound box.
    Every leaf pose captures at least its bound and one (least 1.0037, n = 30, direction
    2071).
  - The summaries give `net_origin proof_net`, `net_last_tangent 1036/2501`,
    `shrink_bound 25009997/25010000` and source `d97758bb…`.
  - Six 99/100 mutant directions are refused with exact witnesses below one.
    At the axis the exact capture is $2.15 \times 10^{-9}$ (n = 28) and
    $1.88 \times 10^{-10}$ (n = 30) above the sweep’s bound.

## What Decides What

- `fine_net_exact.capture` decides the capture at the poses it evaluated: the 62 oblique
  control witnesses, the 120 leaf poses of the source’s tightest directions, and the 60
  leaf poses, 4 oblique mutant witnesses and 2 mutant axis vertices of the runs here.
- `axis_decide.py` decides direction 0 of each certificate over its whole per-bin
  domain, by code that shares nothing with the producer’s.
- `sample_directions.py` decides with the reviewed binary the 12 directions it ran, and
  the 99/100 mutant’s refusal at six more.
- Everything else checks premises.

No program here is a replay, and none is cited by an evidence entry yet; the review
proposes the registry entries.

The computation totalled about four CPU-minutes.
That is about 85 CPU-seconds at most for the build (42 seconds of wall at two jobs), 68
for the two direction samples, 31 for a first n = 28 sample run superseded by the one
kept (its driver misread the `input_sha256` of a gzip input), 47 for two pairs of
`axis_decide` runs, and about 15 for all the rest.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
