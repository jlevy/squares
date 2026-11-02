# squarepacker’s `k² − M(k) ≥ 0.033 log k`, Pinned 2026-10-05

Sungjoon Ryu (GitHub `squarepacker`) reports a preprint on the integer-side case of the
asymptotic problem. Let `M(k)` be the largest number of unit squares that fit in
`[0,k]²` pairwise disjoint as closed sets.
The preprint’s Theorem 1.1 says that for every integer `k ≥ 2`,

`k² − M(k) ≥ 0.033 log k` (natural logarithm),

and `k² − M(k) ≥ (0.99977 log k + 0.3819)/30.147` for `k ≥ 10¹³`.
Its Lemma 2.1 shows that `s(n) < k` exactly when `n ≤ M(k)`. Corollary 1.2 follows:
`c*(k) := max{c : s(k² − c) = k}` is at least `0.033 log k − 1`. Hence, for every fixed
`c`, `s(k² − c) = k` for all large `k`.
The constant `0.033` uses the computer-assisted Lemma 4.10. With the analytic Lemma 4.9
alone, the same proof gives `0.027`.
The claim reached this repository as
[jlevy/squares#368](https://github.com/jlevy/squares/issues/368), opened by
squarepacker on 2026-10-05 at 14:16 UTC.

The result is squarepacker’s, after Roth and Vaughan: the proof sharpens the fundamental
lemma of their 1978 paper and builds on it.
This packet holds the source repository whole at a pinned commit, and the replay run
here. What the record makes of the claim is in
[`asymptotic-waste-bounds.yaml`](../../../frontier/asymptotic-waste-bounds.yaml).

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/squarepacker/k2-minus-c> |
| Revision | [`25f645e8fcadb3c2768f4da42d80e977fb1a508d`](https://github.com/squarepacker/k2-minus-c/tree/25f645e8fcadb3c2768f4da42d80e977fb1a508d), `main` when fetched, tree `d384face` |
| Committed | 2026-10-05T15:15:50Z (`2026-10-06T00:15:50+09:00` by the author’s clock). Seven commits in all. The first, `987c8068` at 14:00:55Z, adds the preprint, every program and the data |
| Versions | Tag `v1.0` is `0eb29d44` (released 14:07Z). Tag `v1.1` is `525da4e3` (released 15:10Z). The pin is `v1.1` plus the DOI line in `README.md`. Version 1.1 adds `code/coverage_independent/` and one sentence in the proof of Lemma 4.10, and changes the preprint’s date line. The README says “The mathematics is unchanged”, and the diff of `paper/paper.tex` bears that out |
| Archive | Zenodo, as the source’s `README.md` gives it: [10.5281/zenodo.23165736](https://doi.org/10.5281/zenodo.23165736) for `v1.1` and [10.5281/zenodo.23164302](https://doi.org/10.5281/zenodo.23164302) for `v1.0`, which the issue cites; the concept DOI is `10.5281/zenodo.23164301`, and the preprint alone is [10.5281/zenodo.23165916](https://doi.org/10.5281/zenodo.23165916). The session that made this packet could not reach Zenodo; the three records were read from 22:54Z the same day, [below](#the-zenodo-records) |
| Retrieved | 2026-10-05T17:10Z, a complete clone; tags at 17:15Z |
| Licence | MIT for `code/` and `data/` (`LICENSE`, copyright Sungjoon Ryu). CC BY 4.0 for `paper/paper.tex` and `paper/paper.pdf` (`paper/LICENSE`) |
| Request | [jlevy/squares#368](https://github.com/jlevy/squares/issues/368) |

**Credit and AI assistance, as the source states them.** The README and the preprint
name Sungjoon Ryu as the sole author. The README says the work was “developed with
extensive assistance from Claude (Anthropic), including the proofs, the text, the
programs and the computation for Lemma 4.10; the author takes full responsibility. Not
peer reviewed.” The preprint’s “Use of AI” section says the same and adds that Claude
“is not an author”. `reviews/REVIEWS.md` summarises the reviews the author ran. All of
them were by AI reviewers, which it says “are AI systems of the same family and may share
blind spots”, and no human has refereed the manuscript.

## What Is Retained

Every file of the tree, 78 files and 1,679,573 bytes, under
[`k2-minus-c/`](k2-minus-c/), byte-identical. The manifest is
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) and the
record [`acquisition/sources.json`](acquisition/sources.json). Both are written by
`devtools.acquire_source` from
[`acquisition/declaration.json`](acquisition/declaration.json). The source’s own
`SHA256SUMS` lists 75 of the 78 files; all 75 match. It omits `README.md`, `.zenodo.json`
and itself, as its README says.

| Upstream path | What it is |
| --- | --- |
| `paper/paper.pdf`, `paper/paper.tex` | The preprint, version 1.1, 25 pages |
| `data/kw9_data.zip` | The certificate of Lemma 4.10: the 13 lists of accepted boxes (`*_T9_*_final_leaves.jsonl`, 78,673 boxes in all), with the author’s verification and coverage outputs and logs. 435,000 bytes, SHA-256 `32634874…`; 29,515,409 bytes in 94 files unpacked |
| `code/verify_leaves2.py`, `code/verify_leaves.py` | The Arb re-verification. `verify_leaves2.py` is the certificate’s checker, and it imports `verify_leaves.py` |
| `code/bnb.py`, `code/bnb_wall.py` | The floating-point branch-and-bound searches. Their cell, mask, split and point-count routines are also called by the verifier |
| `code/coverage_check.py` | The author’s coverage check, which rebuilds the bisection tree with the search’s own split rule |
| `code/coverage_independent/` | Two coverage checks written apart from the search, by exact volumes and by recursive covering, with their results |
| `code/verify_v10.py`, `code/consts_v10.py`, `code/kw13_check.py`, `code/check_hand9_indep.py` | The preprint’s numerical constants in `mpmath`, the facts used in Lemma 4.9(c), and the nine-pair configuration at 80 digits |
| `code/make_stats_v10.py`, `code/run_v2.py`, `code/run_seq.py` | Statistics and job runners |
| `code/SUPERSEDED.md` | Why the first verifier, which left one-ulp gaps between direction cells, is withdrawn |
| `code/experiments/` | Search programs behind the numerical experiments of Remark 7.5, not part of the proof |
| `reviews/REVIEWS.md` | The author’s summary of the AI reviews |

From `packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source squarepacker-k2-minus-c-2026-10-05 --check`
re-derives the packet from its manifest.

## The Zenodo Records

Zenodo was read from 2026-10-05T22:54Z, after the environment’s egress policy was widened
(bead `think-cdzc`), by
[`devtools.capture_web_source`](../../../devtools/capture_web_source.py) `zenodo`.
For each record it kept the record and its files listing as Zenodo served them, checked
each deposited file’s size and MD5 against the record, and compared each archive’s
members with the trees named below.
The archives themselves are not retained: they are pinned by digest here and the DOIs
serve them.
Everything is under [`zenodo/`](zenodo/).

| Record | Version, created | Deposited file | Bytes | MD5, as stated and as computed | SHA-256 |
| --- | --- | --- | ---: | --- | --- |
| [23164302](https://doi.org/10.5281/zenodo.23164302), the DOI #368 cites | 1.0, 2026-10-05T14:07:11Z | `squarepacker/k2-minus-c-v1.0.zip` | 1,083,690 | `8fab14ded131e118a8d0f78f26bd8598` | `d65623cf799b1615a76f52e376aceb929b926ce2a1b7045e7c84e8680e297bfa` |
| [23165736](https://doi.org/10.5281/zenodo.23165736) | 1.1, 2026-10-05T15:10:45Z | `squarepacker/k2-minus-c-v1.1.zip` | 1,130,274 | `6d2d1b0633a8e35f26b8de514addd3ba` | `c9d3f6de5ff7693a3f6f69a07bf753e16c91462ff662191bd29139a3547a40d6` |
| [23165916](https://doi.org/10.5281/zenodo.23165916), the preprint, CC BY 4.0 | none, 2026-10-05T15:24:25Z | `paper.pdf` | 556,058 | `d83b37b0f77b19dceb9f73a4c41cb858` | `71c4d6b627cf7674b3557d433a0613fb3be502d2b5e41072ed470f50891041bf` |

The concept DOI `10.5281/zenodo.23164301` resolves to version 1.1, and Zenodo lists no
third version. Version 1.1 names record 23165916 as its preprint.

**What each record holds.**

- **Version 1.0 is tag `v1.0`, `0eb29d44`, byte for byte.** Its archive is GitHub’s
  release archive of that commit: 55 files under one directory
  `squarepacker-k2-minus-c-0eb29d4`, each equal to the tag’s
  ([`zenodo-23164302.sha256`](zenodo/zenodo-23164302.sha256),
  [receipt](zenodo/zenodo-23164302-receipt.json)).
- **Against this packet’s pin, version 1.0 differs in six files and lacks 23.** It lacks
  `code/coverage_independent/`, the two independent coverage checks. It differs in
  `paper/paper.pdf`, `paper/paper.tex`, `README.md`, `reviews/REVIEWS.md`,
  `.zenodo.json` and `SHA256SUMS`. The other 49 files are the same: `data/kw9_data.zip`,
  the certificate, and every program the replay above ran except the two of
  `code/coverage_independent/`. So the certificate the replay re-verified is the one
  version 1.0 deposits, and so is the checker that re-verified it.
- **The two papers differ in two places, and the mathematics does not.** In
  `paper.tex` the date line gains “version 1.1”. In the proof of Lemma 4.10, version
  1.0’s “The computation has not been reproduced by an independent implementation” is
  replaced by a sentence saying the coverage was confirmed by two independent checks and
  the Arb re-verification of the boxes has not yet been reproduced. Both PDFs have 25
  pages; their extracted text differs in those two places and in the reflow of page 16.
  The version 1.0 PDF is retained as
  [`zenodo/zenodo-23164302/paper/paper.pdf`](zenodo/zenodo-23164302/paper/paper.pdf),
  555,663 bytes, SHA-256
  `da00630c891919e5fdc6e6065da83c8ac638eb07d8cfe4e74e43c11f129d9789`, under the paper’s CC
  BY 4.0 licence. `reviews/REVIEWS.md` gains the row for the blank-slate review of
  “v10”, and `README.md` its version 1.1 notes.
- **Version 1.1 is tag `v1.1`, `525da4e3`, byte for byte,** 78 files. Against this
  packet’s pin it differs only in `README.md`, by the DOI line the pin adds
  ([`zenodo-23165736.sha256`](zenodo/zenodo-23165736.sha256),
  [receipt](zenodo/zenodo-23165736-receipt.json)).
- **Record 23165916’s `paper.pdf` is this packet’s `paper/paper.pdf`,** the version 1.1
  preprint, byte for byte ([receipt](zenodo/zenodo-23165916-receipt.json)).

From `packing/`, with `V10` and `V11` checkouts of the two tags, the records are read
again with:

```bash
P=resources/web/squarepacker-k2-minus-c-2026-10-05
uv run --frozen --all-extras --group dev python -m devtools.capture_web_source zenodo 23164302 \
  --out $P/zenodo --extract paper/paper.pdf --compare-manifest $P/acquisition/upstream-subtree.sha256 \
  --compare-dir "squarepacker/k2-minus-c tag v1.0, 0eb29d4468dd1ed6c8a06841d4d6f0fd83945e0f=V10"
uv run --frozen --all-extras --group dev python -m devtools.capture_web_source zenodo 23165736 \
  --out $P/zenodo --compare-manifest $P/acquisition/upstream-subtree.sha256 \
  --compare-dir "squarepacker/k2-minus-c tag v1.1, 525da4e301cb8dd86778fba944de461a82877a6e=V11"
uv run --frozen --all-extras --group dev python -m devtools.capture_web_source zenodo 23165916 \
  --out $P/zenodo --compare-manifest $P/acquisition/upstream-subtree.sha256 \
  --compare-manifest $P/zenodo/zenodo-23164302.sha256
```

## The Replay of Lemma 4.10

The source’s own checker ran here on the retained bytes, in full, on a four-core Linux
container shared with four other lanes at load averages of 10 to 18. So every wall time
below is contended, and the CPU times are the measure.
The interpreter was CPython 3.12.3 in a scratch virtual environment with python-flint
0.9.0 and NumPy 2.5.3, the versions the preprint names. The preprint names Python
3.12.10; `verify_v10.py` ran with its mpmath 1.4.1.
The 13 box lists were unpacked from `data/kw9_data.zip` beside a copy of `code/`, without
the author’s outputs, so nothing could resume from them.
[`receipts/verify-leaves2/inputs.sha256`](receipts/verify-leaves2/inputs.sha256) gives
the digest of every program and list that ran; the packet test holds each to the
retained bytes.
Each receipt is written by `devtools.replay_receipt` (command, working directory, load,
exit status, wall and CPU).

| Step | Program | Wall | CPU | Result |
| --- | --- | ---: | ---: | --- |
| The labels, in four parts | `run_v2.py W` for `W = 0…3`, which runs `verify_leaves2.py LIST 9 W 4` on every list; parts 0 and 1, then 2 and 3, two at a time under `nice -n 10` | 4,434, 4,375, 4,878 and 4,991 s | 1,447.7, 1,435.6, 1,557.0 and 1,597.6 s; 6,037.9 s in all | All 78,673 boxes accepted, no failure, largest rigorous bound 9, 59,238 further bisections, 66,967 rigorous pieces. Each of the 52 output records equals the author’s ([receipts](receipts/verify-leaves2/), [outputs](receipts/verify-leaves2/outputs/)) |
| The author’s coverage check | `coverage_check.py` on each list | 23.1 s | 14.0 s | All 13 tile their initial boxes: tree rebuilt, every box used once, exact volumes equal. Each record equals the author’s ([receipt](receipts/coverage/coverage-check.log)) |
| The statistics | `make_stats_v10.py` | 0.1 s | 0.1 s | `COMPLETE`, `stats_v10.json` equal to the author’s ([receipt](receipts/verify-leaves2/make-stats-v10.log)) |
| The constants and completeness | `verify_v10.py` | 29.0 s | 18.6 s | `ALL OK`, 132 checks ([receipt](receipts/verify-leaves2/verify-v10.log)) |
| Exact volumes, written apart from the search | `coverage_independent/exact_volume/indep_cover.py LIST 40000 12345`, one list at a time (its `run_all.py` runs four at once) | 429.3 s | 280.7 s | Method A passes on all 13: interior-disjoint boxes, exact volume equal to the domain’s. Method B located 3,333,005 points, none uncovered. Each report equals the author’s apart from its timing ([receipt](receipts/coverage/indep-cover.log)) |
| Recursive cover, written apart from the search | `coverage_independent/recursive_cover/coverage_lowmem.py ../.. OUT --slabs 32` | 171.5 s | 108.2 s | All 258 slabs, 0 gaps, 4,568,856 nodes. Each row equals the author’s apart from timing and memory ([receipt](receipts/coverage/coverage-lowmem.log), [rows](receipts/coverage/results-replay.jsonl)) |

This reproduces the computation with the producer’s code.
It does not re-implement it: `verify_leaves2.py` imports the search’s cell grid, its float
prefilter, its split rule and its float point count `max_points` (the review’s RF-1 and
RF-2). The two independent coverage programs were written by AI reviewers in sessions
apart from the search, as `code/coverage_independent/README.md` says.
[A second implementation of the labelling](#an-independent-labelling-of-lemma-410),
written here on 2 November, is below.

`summarize.py` prints its totals and then exits 1 on Linux.
Its memory guard reports unlimited free memory off Windows, and the summary’s last line
calls `round` on that infinity. The totals print first
([receipt](receipts/coverage/coverage-lowmem-summary.log)).

## Controls

[`devtools.write_k2_minus_c_controls`](../../../devtools/write_k2_minus_c_controls.py)
derives both from the retained certificate
([record](receipts/controls/controls.json)). The box it picks is box 23 of
`bnb_n2_T9_0of1_final_leaves.jsonl`, the first that holds two inner centres at radius
`1/2` and angles `0` and `π`: the nine-pair configuration of `code/attack_kw/hand9.json`,
with `U = 1 + 4 + 4 = 9`.

| Control | Checker | Result |
| --- | --- | --- |
| That box alone, at threshold 9 | `verify_leaves2.py … 9 0 1` | Accepted in one piece at bound 9; 0.3 s CPU ([receipt](receipts/controls/verify-leaves2-sharp-leaf-T9.log)) |
| The same box at threshold 8 | `verify_leaves2.py … 8 0 1` | Refused: after 4,097 bisections the box fails, 616.8 s CPU ([receipt](receipts/controls/verify-leaves2-sharp-leaf-T8.log), [output](receipts/controls/verify2-sharp-leaf-T8.json)) |
| The n = 2 list without that box | `coverage_check.py` | Refused: “FAIL: reached a tiny unmatched box”, exit 1 ([receipt](receipts/controls/coverage-check-n2-drop.log); the retained list passes, [receipt](receipts/controls/coverage-check-n2-base.log)) |
| The same | `indep_cover.py` | Refused: Method A fails, the volume short by `1/256` of the domain, uncovered points found ([receipt](receipts/controls/indep-cover-n2-drop.log); the retained list passes) |
| The same | `coverage_lowmem.py --only 0,2` | Refused: gaps in slabs 17 and 18, two in all ([receipt](receipts/controls/coverage-lowmem-n2-drop-summary.log); the retained list has none) |

## An Independent Labelling of Lemma 4.10

On 2 November 2026 (`think-k3tk`) every box was decided again by
[`cases/asymptotic/ryu_k2_minus_c_labels.py`](../../../cases/asymptotic/ryu_k2_minus_c_labels.py),
written here from the proof of Lemma 4.10 and the disc model of the TeX. Its authors never
read or ran the source’s programs; [its receipts and read log](receipts/independent-labels/README.md)
say what they did read. It shares with `verify_leaves2.py` the box lists and the proof’s
model, and nothing of its code: no cell grid, prefilter, split rule or float count, and no
Arb. It works in binary64 with one-ulp outward rounding after every operation and with
constants from mpmath intervals. It tests dyadic direction cells exactly in the radius `t`,
and it counts directions exactly, in integers.

| Label | Boxes | Certified as labelled |
| --- | ---: | ---: |
| `inf` | 72,174 | 72,174 |
| `nowall` | 1,094 | 1,094 |
| `closed` | 5,405 | 5,405 |

Every box was certified under its own label: none needed another label, and none failed.
The largest bound of a `closed` piece is 9. The run took 1,880.8 CPU seconds on two
cores, 16 minutes of wall time. A price came first: 500 boxes extrapolated to 0.54
CPU-hours, against a cap of 40. Four negative controls are refused,
each with an exactly checked witness that its claim is false: the sharp box at threshold 8,
an `inf` box widened to hold an admissible pair, a `nowall` box widened to hold a side
edge, and the count’s separation halved.

So the labels of Lemma 4.10 have two implementations: the replay above, with the
producer’s code, and this one, independently re-implemented, clean-room, by a Claude agent,
a system family the producer also used. That the boxes cover the domain still rests on the
source’s three coverage programs. That the bound `U(I)` is the right one still rests on the
proof, which the review re-derived. Version 1.2’s Lemma 4.10 decides the same lists under
the same model, so this run covers it too.

## The Constants

[`cases.asymptotic.ryu_k2_minus_c_constants`](../../../cases/asymptotic/ryu_k2_minus_c_constants.py)
re-decides every numerical step from the lemmas’ stated inputs to Theorem 1.1, in exact
rationals where the step is rational and on 60-digit intervals otherwise. It was written
from the preprint’s text, not from `verify_v10.py`. All 31 steps hold with the overlap
bound 9, giving `0.033`, the `k ≥ 10¹³` formula and `log k > 120.23375…` for `c = 4`. All
28 hold with the analytic 13, giving `0.027`
([receipts](receipts/constants/)).

The source’s quick checks also ran, with mpmath 1.4.1
([receipts](receipts/source-checks/)). `kw13_check.py` passes its 18 checks, but its
second half checks the previous draft’s 13-bound constants (bracket below `36.081` at
`k₂ = 10¹⁶`), not version 1.1’s (`36.212` at `10¹³`). `verify_v10.py` and the module
above check the version 1.1 values. `check_hand9_indep.py` finds nine pairs at `d =
10⁻⁶`, `10⁻⁵`, `10⁻⁴`, `10⁻³` and `10⁻²`. `consts_v10.py 9` passes its 30 checks.

## The Review

[The review of 5 October](../../../../docs/project/reviews/review-2026-10-05-squarepacker-k2-minus-c.md)
was run separately, blind to the replay, by one AI reviewer. It re-derives the proof and
accepts it with nine findings, none blocking. No human has refereed the preprint.

## Reproduce

From `packing/`, with `SCRATCH` any directory outside the repository and a Python 3.12
virtual environment `VENV` holding python-flint 0.9.0, NumPy 2.5.3 and mpmath 1.4.1:

```bash
cp -r resources/web/squarepacker-k2-minus-c-2026-10-05/k2-minus-c/code SCRATCH/code
unzip -j -d SCRATCH/code \
  resources/web/squarepacker-k2-minus-c-2026-10-05/k2-minus-c/data/kw9_data.zip '*_final_leaves.jsonl'
(cd SCRATCH/code && for w in 0 1 2 3; do VENV/bin/python run_v2.py $w; done)
(cd SCRATCH/code && for f in *_final_leaves.jsonl; do VENV/bin/python coverage_check.py $f; done)
(cd SCRATCH/code && VENV/bin/python make_stats_v10.py && VENV/bin/python verify_v10.py)
uv run --frozen --all-extras --group dev python -m cases.asymptotic.ryu_k2_minus_c_constants
uv run --frozen --all-extras --group dev python -m devtools.write_k2_minus_c_controls SCRATCH/controls
```

The independent labelling runs with the project interpreter alone; its commands are in
[its README](receipts/independent-labels/README.md#reproduce).

## Compressed Files

The label rows of the nine lists of more than 1,000 boxes are stored as deterministic
gzip by `devtools.retained_data.write_retained`. They are receipts the labeller writes
again with new timings at each run, so their digest cells are empty.

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `receipts/independent-labels/labels/bnb_n3_T9_0of1.jsonl.gz` | receipt |  |  |
| `receipts/independent-labels/labels/bnb_n4_T9_0of2.jsonl.gz` | receipt |  |  |
| `receipts/independent-labels/labels/bnb_n4_T9_1of2.jsonl.gz` | receipt |  |  |
| `receipts/independent-labels/labels/bnb_n5_T9_0of2.jsonl.gz` | receipt |  |  |
| `receipts/independent-labels/labels/bnb_n5_T9_1of2.jsonl.gz` | receipt |  |  |
| `receipts/independent-labels/labels/bnbw_n3_T9_0of1.jsonl.gz` | receipt |  |  |
| `receipts/independent-labels/labels/bnbw_n4_T9_0of2.jsonl.gz` | receipt |  |  |
| `receipts/independent-labels/labels/bnbw_n4_T9_1of2.jsonl.gz` | receipt |  |  |
| `receipts/independent-labels/labels/bnbw_n5_T9_0of1.jsonl.gz` | receipt |  |  |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
