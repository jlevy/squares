# The Mathematical Review’s Programs, 4 November 2026

These are the programs the
[mathematical review](../../../../../docs/project/reviews/review-2026-11-04-wand125-fine-net-n29.md)
of wand125’s `mixed_n29_L582` (T-132) wrote and ran on 4 November 2026. They are kept as
they ran, with the output each printed in [`out/`](out/). The review was the stage-4
mathematical review think-1lri of the import think-r333. It was written by an AI agent,
Claude (Anthropic), at the tbd-strong-max tier with maximum reasoning, prompted
separately from the intake, records and replay lanes and working in a worktree of its
own.

Each program ran with the project interpreter (Python 3.14.7, `python3 -I`, from a
directory of its own), at `nice -n 19` and on at most two cores.
Each read as data:

- the packet’s retained `release/` members and its `source-manifest.json` and
  `acquisition/release-assets.json`, on `main` at `c03183f66`;
- the release asset of `square-lower-bounds-v1`, fetched once more into scratch space
  and held to the packet’s size and SHA-256 pin;
- the eleven pinned documents of the certificate directory and the enclosing `LICENSE`,
  fetched at the pinned revision and held to the manifest’s digests.

No program imports anything of the source, the crate or `packing/devtools`, and none
executes anything of the source.
One program run here was not written by the review: this repository’s reviewed
`sqverify-fast`. It was built in the review’s worktree from crate source `d97758bb…`
(binary SHA-256 `567a0fd5…`), and `sample_directions.py` drives it.

## What Its Authors Read

Before writing these programs the lane read:

- in `packing/sqverify_fast/SOUNDNESS.md`: the claim, N1 to N4, lemma N0, C1, A1, A2, R1
  to R5 and the acceptance rule, D, B5, Z1, Z2, I1, I2, F2, F3, R6, R7 and A3;
- in the crate: `build.rs`, and `certificate.rs`’s `admit`, `domain_upper` and
  `direction` at `e020eb1e2`; not `axis.rs`, `rotated.rs`, `interval.rs` or `lib.rs`;
- the census control’s axis rule in `devtools/sqverify_fast_census.py` and the header of
  `devtools/sqverify_fast_axis.py`, read but not run;
- the source’s `SPEC.md`, `REPRODUCE.md` and `fine_net_check.sh`, and the candidate,
  receipts and logs, as data;
- the programs of the 4 November review of `mixed_n28_L57425` and `mixed_n30_L58925`
  (bead think-4ul6), line by line.

Eight of the programs adapt that review’s. Each was re-read and re-run against this
certificate, and changed where this packet or a closer reading needed it:

- `selftest.py` adds a reflection as the quarter turn’s negative control, the closure of
  the $D_4$ images and the strict reader’s refusals;

- `fine_net_exact.py` reads every number through a strict reader (a canonical decimal or
  ratio; `Fraction()` alone also accepts spaces, exponents and underscores), takes the
  rotated rectangle’s two half-sizes separately, and writes the shipped script’s control
  mutant;

- `check_candidate.py` and `custody_and_nested.py` read this packet’s single-asset
  manifest, and check also the canonical numbers, repeated rectangles, Tokoharu’s domain
  at every node, the one-member gzip of the retained candidate and the Git blob of every
  member;

- `check_source_logs.py` tells the pre-publication run apart from the check2 run by its
  seconds, and records each control witness’s stopping depth;

- `axis_decide.py` certifies by an exact comparison of the least binary64 vertex with
  $1 + \gamma_{K+4}$, where the precedent compared in binary64, and counts the
  quadrant’s events as lemma A1 defines them, to compare with the crate’s;

- `check_source_docs.py` reads all eleven pinned documents and the `LICENSE`, and
  records what `SOUNDNESS.md` and `SPEC.md` say of the net and of the fold;

- `sample_directions.py` also compares `mean_boundary_rectangles`, `audits` and
  `audit_every`.

`oblique_decide.py`, `oblique_selftest.py` and `oblique_sample.py` are new.
The oblique decision’s bound is the capture of the intersection of every core of a box
of centres, with areas bounded below by a concave section and a trapezoid sum, in
binary64 moved outward one ulp at every step.
It uses no derivative, and no code or search lemma of the crate.
Its idea of a concave section is lemma R2’s, which this lane read.

The producer’s checker is the source’s copy of this repository’s crate.
None of these programs is clean-room with respect to it, and none imports or copies any
of it.

The source’s commit names Claude as co-author.
These programs were written by a Claude agent, prompted separately from the source and
from the intake and replay lanes.

## The Programs

| Program | What it does | Reads | Output | CPU |
| --- | --- | --- | --- | --- |
| [`fine_net_exact.py`](programs/fine_net_exact.py) | The module the others import. It reads a candidate exactly, refusing duplicate keys, multi-member gzip and any number not a canonical decimal or ratio. It provides the eight $D_4$ images (unmerged), the direction $(c_r, s_r)$, lemma D’s per-bin domain, the rotated rectangle, Sutherland–Hodgman clipping, the exact capture, the axis capture, the source’s semantic digest and the shipped script’s control mutant. | (a module) | — | — |
| [`selftest.py`](programs/selftest.py) | Tests the module on synthetic data: a partition of the core’s neighbourhood sums to $B^2$ exactly at six directions; the axis capture equals the product formula; the capture is invariant under the quarter turn (lemma C1) and not under a reflection; $c^2 + s^2 = 1$; the $D_4$ images are closed under the generators; the strict reader refuses 13 non-canonical spellings; a seeded wrong clip is caught. | nothing | [`selftest.txt`](out/selftest.txt) | 0.2 s |
| [`check_candidate.py`](programs/check_candidate.py) | Recomputes every exact premise: the bytes against the pin, the semantic digest, the keys, format M, `points` empty, `proof_net` exactly `step` and `last`, no `net`, `certificate`, `schema` or `scaling_factor` key; the claim’s $n$ and $L$; the rows (positive, nondegenerate, inside $K$, none repeated); the mass against `total_mass` and $n - 1/100000$; the distinct images and lemma F3’s caps; the coordinate grid; lemma N0’s (a) to (e), the sharp N3 extent, the last bin (H4), and the per-bin domain and Tokoharu’s at all 2,073 nodes. | the retained `candidate.json.gz`; `source-manifest.json` | [`check_candidate-mixed_n29_L582.json`](out/check_candidate-mixed_n29_L582.json) | 0.2 s |
| [`check_source_logs.py`](programs/check_source_logs.py) | Reads the source’s run log against the candidate: every direction once, each `verified` at threshold `1`, the sums and premises of the summary. Checks the check2 receipt, `control.json` and the pre-publication receipt against the candidate, the log and each other, and tells the two runs apart. In the 197/200 control log, checks the directions rule and the scaled mass, rebuilds the mutant file to compare with the logged input digest, and evaluates all 31 oblique witnesses exactly. At the 12 tightest directions, evaluates the leaf box’s centre and four corners exactly. | the retained `check2/` and `verification/` members; `check_candidate`’s output | [`check_source_logs-mixed_n29_L582.json`](out/check_source_logs-mixed_n29_L582.json) | 4.9 s |
| [`axis_decide.py`](programs/axis_decide.py) | Decides direction 0 over the whole per-bin domain $[1/2, L - 1/2]^2$: the event grid of every overlap breakpoint, overlaps exact in int64, every vertex in binary64 under the bound $\gamma_{K+4}$, certified by an exact comparison; then the lowest vertices, the eight-vertex orbit and 40 random vertices in fractions; and the source’s axis rows, original and control, at their reported vertex. | the retained candidate, `run.jsonl.gz` and `control-197_200.jsonl.gz` | [`axis_decide-mixed_n29_L582.json`](out/axis_decide-mixed_n29_L582.json) (and `.log`) | 16.5 s (two BLAS threads) |
| [`custody_and_nested.py`](programs/custody_and_nested.py) | Reads the asset in memory: size and SHA-256 against the pin, every member against the manifest (size, SHA-256, Git blob), the retained copies against the members, the sealed bundle against its own `files-sha256.json`. Recomputes the nested verifier’s build digest by the crate’s `build.rs` rule and compares it file by file with `packing/sqverify_fast` at `e020eb1e2`, `34e87a86b` and this tree’s head. | the asset; the packet; `git show` of the three revisions | [`custody_and_nested.json`](out/custody_and_nested.json) | 0.3 s |
| [`check_source_docs.py`](programs/check_source_docs.py) | Checks the eleven documents and the `LICENSE` against their pins; recomputes `bundle.json`’s net block, digests and comparison exactly; checks the files the README names, its stated seconds and its pinned edition against the sealed one; reads the shipped `fine_net_check.sh` for the receipt shape it writes and its rules; identifies `SOUNDNESS.md` and `INDEPENDENCE.md` by Git blob and records what `SOUNDNESS.md` and `SPEC.md` say of the net and the fold; looks up the stated verifier commits. | the fetched documents; the asset; `git show` | [`check_source_docs.json`](out/check_source_docs.json) | 0.1 s |
| [`sample_directions.py`](programs/sample_directions.py) | Runs the reviewed `sqverify-fast` with `--confirm` and two threads at seven directions: the four least-bound directions of the source’s log, the one with the most nodes, the one whose leaf captured least, and one seeded random direction, none of them a direction the intake lane sampled. Compares each row with the source’s, evaluates every leaf box’s centre and corners exactly, and reads the summary’s premises as the 6 October checklist’s item 3. Then runs the 99/100 mutant at three directions and evaluates each refusal exactly. | the retained candidate and run log; the binary | [`sample_directions-mixed_n29_L582.json`](out/sample_directions-mixed_n29_L582.json) | binary 38.7 s; Python 2.2 s |
| [`oblique_decide.py`](programs/oblique_decide.py) | Decides one oblique direction over its whole per-bin domain by a branch and bound of its own: the capture of the intersection of a box’s cores (lemma S) or each image’s least corner value (lemma Q), areas bounded below by a concave section and trapezoids in binary64 moved outward one ulp at every step, classification with slack $10^{-12}$, and an exact screen for counterexamples. | the retained candidate | [`oblique/`](out/oblique/), one receipt and log a direction | 29.0 to 521.7 s a direction, one thread; 2,161.4 s for the nine; 7.4 s for the 99/100 control; 45.2 s for the two scaled controls |
| [`oblique_selftest.py`](programs/oblique_selftest.py) | Holds `oblique_decide`’s bounds to exact rational geometry: the area bound on 3,000 random pairs, two seeded errors, lemma Q at 1,600 interior points, and both box bounds against exact captures at the centre, corners and interior points of 24 boxes of the candidate’s measure. | synthetic data; the retained candidate | [`oblique_selftest.txt`](out/oblique_selftest.txt) | 8.8 s |
| [`oblique_sample.py`](programs/oblique_sample.py) | Runs `oblique_decide.py` over a list of directions, two at a time, and writes a summary. It decides nothing itself. | — | — | — |

The receipts name the candidate by the path it was read from, which was the packet’s
`release/certificates/mixed_n29_L582/candidate.json.gz` in the review’s worktree, and
carry its SHA-256.

## How to Run Them

From a directory of its own, with `$PY` the project interpreter, `$PACKET` this packet,
`$C` its `release/certificates/mixed_n29_L582`, `$ASSETS` a directory holding the
release asset, `$DOCS` a directory holding the eleven fetched documents at their paths
in the certificate directory and `LICENSE`, `$REPO` the repository root and `$BINARY`
the reviewed build:

```sh
$PY -I programs/selftest.py
$PY -I programs/check_candidate.py $PACKET mixed_n29_L582 29 291/50 --out out/check_candidate-mixed_n29_L582.json
$PY -I programs/check_source_logs.py $C out/check_candidate-mixed_n29_L582.json --out out/check_source_logs-mixed_n29_L582.json
OPENBLAS_NUM_THREADS=2 $PY -I programs/axis_decide.py $C/candidate.json.gz \
    --source-run $C/check2/run.jsonl.gz --control $C/check2/control-197_200.jsonl.gz \
    --out out/axis_decide-mixed_n29_L582.json
$PY -I programs/custody_and_nested.py $PACKET $ASSETS $REPO e020eb1e2 34e87a86b HEAD --out out/custody_and_nested.json
$PY -I programs/check_source_docs.py $PACKET $DOCS $ASSETS $REPO --out out/check_source_docs.json
$PY -I programs/sample_directions.py $BINARY $C 29 291/50 --directions 1947,603,1595,1173,2068,886,312 \
    --mutant-directions 0,1947,2068 --mutant-factor 99/100 --threads 2 --out out/sample_directions-mixed_n29_L582.json
$PY -I programs/oblique_selftest.py $C/candidate.json.gz
for r in 886 1595 1947 2068 2072; do
    OPENBLAS_NUM_THREADS=1 $PY -I programs/oblique_decide.py $C/candidate.json.gz $r --out out/oblique/oblique-r$(printf %04d $r).json
done
for r in 1 312 603 1173; do
    OPENBLAS_NUM_THREADS=1 $PY -I programs/oblique_decide.py $C/candidate.json.gz $r --split adaptive \
        --out out/oblique/oblique-r$(printf %04d $r).json
done
OPENBLAS_NUM_THREADS=1 $PY -I programs/oblique_decide.py $C/candidate.json.gz 1947 --scale 99/100 --out out/oblique/oblique-mutant99-r1947.json
for sc in 9991 9993; do
    OPENBLAS_NUM_THREADS=1 $PY -I programs/oblique_decide.py $C/candidate.json.gz 312 --split adaptive --scale $sc/10000 \
        --out out/oblique/oblique-scaled$sc-r0312.json
done
```

The documents were fetched from
`https://raw.githubusercontent.com/wand125/square-packing/22a23c8a99aa4e9616d596bc2f28555bacbee3dd/problems/square-lower-bounds/certificates/mixed_n29_L582/<file>`
(and `…/problems/square-lower-bounds/LICENSE`), and the asset from the release’s
download URL in `source-manifest.json`.

## What They Printed

- **`selftest`.** Nine passes, the seeded wrong clip and the reflection’s change among
  them.
- **`check_candidate`.** `ALL_PREMISES_HOLD`.
  - The bytes equal the pin (`c9171c92…`); the semantic digest is `377bcd7b…`; the
    retained `.gz` is `16750ea3…`.
  - There are 650 rows, all positive, nondegenerate, inside $K$ and none repeated, with
    mass $2899999/100000$, equal to `total_mass` and to $29 - 1/100000$. Every number is
    a canonical decimal or ratio, and the coordinates lie on the grid $10^{-17}$.
  - The images number 5,156 distinct of 5,200: eleven rows have coincident images.
    The merged images integrate to the mass.
  - The densest image density is 50,974; eight times the densest row is
    $3.26 \times 10^6$, below $2^{32}$.
  - Lemma N0 holds with $B(1 + D) = 25009997/25010000$,
    $t_{\max}^2 + 2t_{\max} - 1 = 367/6255001$ and the tangent form
    $500400014977/500400075000$. The last bin $[4143/10004, 4145/10004]$ holds
    $\tan(\pi/8)$.
  - The per-bin domain is nonempty and increasing at every node, never wider than
    Tokoharu’s. Its least width is 4.406, at node 2072.
- **`check_source_logs`.** `SOURCE_RECORDS_CONSISTENT`.
  - The run log has 2,073 rows, every one `verified` at `1`, with the summary’s sums and
    premises recomputed.
    The receipt embeds that summary.
  - The pre-publication receipt is the shipped script’s shape, with 4,306 s against the
    check2 run’s 1,057.9 s.
  - The control is the 197/200 mutant at $\mathrm{round}(2072 i/31)$; the mutant file
    rebuilt by the shipped script’s rule has the logged input digest `8e786a9c…`.
  - All 31 oblique witnesses lie in the per-bin domain, with captures below one equal to
    the crate’s rationals; nine stopped at depth 60.
  - All 60 leaf poses capture at least their bound and one, the least 1.000990.
- **`axis_decide`.** `decided_verified` true.
  - The least vertex is 1.0008730852291343 ($8{,}580^2$ vertices), on a plateau that
    holds the eight-vertex orbit of $(1/2, 2.4994977524465363)$ and the source’s argmin.
  - The quadrant has 4,291 events per axis, the crate’s count.
  - The source’s certified axis bound lies $5.28 \times 10^{-10}$ below the exact
    capture; the 197/200 control’s axis refusal is exact, 0.98586.
- **`custody_and_nested`.** `CUSTODY_HOLDS`. The asset, every member and every retained
  copy equal their pins, and the retained `release/` holds exactly the six stored
  members. The sealed bundle matches its own manifest.
  - The nested archive has 20 files and the build digest `ab6e33e1…`. Against
    `e020eb1e2`, 16 files are byte-identical and `src/certificate.rs` is +32 −2.
  - Its duplicate-key reader is identical to the one at all three revisions.
  - Its admission reads `proof_net` with exactly `step` and `last`, refuses it beside
    metadata or outside format M, and checks the tangent form for the per-bin domain.
    It reads no `count` and has no refusal of a top-level `net` key.
    These are recorded as facts only, and no line of the archive is kept.
  - The head’s crate digest is `d97758bb…`.
- **`check_source_docs`.**
  - The documents and the `LICENSE` equal their pins, and `bundle.json`’s exact values
    hold.
  - The README names the absent `check2/control.jsonl.gz`, and states the
    pre-publication receipt’s 4,306 s. Its pinned edition adds the four-line
    “Pre-publication check” section to the sealed one.
  - The shipped script writes the `build` receipt shape, not the published
    `fine-net-check2-receipt/v1`.
  - `SOUNDNESS.md` and `INDEPENDENCE.md` are the editions at `e020eb1e2`; `SOUNDNESS.md`
    has nothing on `proof_net`, names the standard net and $t_{200}$, and reflects the
    whole configuration (line 43), as `SPEC.md` does (lines 46 and 47).
  - Neither `fe12e036c` nor `42534d959…` is in this full clone.
- **`sample_directions`.** `SAMPLE_AGREES`.
  - Seven directions are `verified`, each row equal to the source’s in verdict, nodes,
    leaves, depth, bound, least-bound box, mean straddling rectangles and audits.
    Every leaf pose captures at least its bound and one (least 1.000990, direction 886).
  - The summary gives `net_origin proof_net`, `net_last_tangent 1036/2501`,
    `shrink_bound 25009997/25010000`, source `d97758bb…`, and the retained `.gz`’s
    digest as `input_sha256`.
  - Three 99/100 mutant directions are refused with exact witnesses below one.
    At the axis the exact capture is $5.23 \times 10^{-10}$ above the sweep’s bound.
- **`oblique_selftest`.** Nine passes (§4 of the review).
- **`oblique_decide`.** Nine directions `VERIFIED` over their whole per-bin domains (1,
  312, 603, 886, 1173, 1595, 1947, 2068, 2072); the least capture found is 1.0005828, at
  direction 886. The 99/100 mutant is `REFUTED` at 1947, with the exact witness
  0.99100523 at depth 20. At 312, the measure scaled by 9991/10000 is `REFUTED` after
  14,042 boxes, with the exact witness 0.9999948560, and scaled by 9993/10000 it is
  `VERIFIED` after 45,367 boxes.

## What Decides What

- `fine_net_exact.capture` decides the capture at the poses it evaluated: the 31 oblique
  control witnesses, the 60 leaf poses of the source’s 12 tightest directions, the 35
  leaf poses, 2 oblique mutant witnesses and the mutant axis vertex of the reviewed
  crate’s runs here, and the least-capture centres and witnesses of the oblique
  decisions.
- `axis_decide.py` decides direction 0 over its whole per-bin domain, by code that
  shares nothing with the producer’s.
- `oblique_decide.py` decides the nine oblique directions it ran, each over its whole
  per-bin domain, the 99/100 mutant’s refutation at direction 1947 and the two scaled
  controls at 312, by code that shares nothing with the producer’s. `oblique_sample.py`,
  a driver, ran once and was stopped during its first direction, which a later run with
  the adaptive split decided; it decided nothing.
- `sample_directions.py` decides with the reviewed binary the seven directions it ran,
  and the 99/100 mutant’s refusal at three.
- Everything else checks premises.

No program here is a replay, and none is cited by an evidence entry yet; the review
proposes the registry entries.

The computation totalled about 69 CPU-minutes.
That is 26 CPU-seconds for the build (19.8 seconds of wall at two jobs), 41 for the
crate’s sample, 2,214 for the oblique decisions and their controls kept here, about 33
for four runs of the oblique self-tests, about 44 for two runs of every other program
(at `6a02a660e`, then at `c03183f66` for the receipts kept), and about 1,761 for timing
runs of earlier versions of `oblique_decide.py` that were stopped or superseded: the
first version at 312, 1947 and 2068 (about 470 seconds), the corner bound before and
after batching at 312, 1947 and 2068 (about 730), and direction 1 split across the
longer side (560, stopped unfinished).
The decision at 1947 ran with `--bound intersection` given, before it became the
default, and those at 1947 and 2068 ran before the `--split` option was added, with the
behaviour of its default; nothing else in the program changed after them but its
docstring.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
