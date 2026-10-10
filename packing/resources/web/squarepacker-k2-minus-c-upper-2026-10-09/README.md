# Sungjoon Ryu’s Upper Bounds on the Deficiency c*(k), Version 1.0

Retained from
[squarepacker/k2-minus-c-upper](https://github.com/squarepacker/k2-minus-c-upper/tree/700668795e6b95f0bf2a2c6de104adaf3a3ebce0)
at tag `v1.0`, commit `700668795e6b95f0bf2a2c6de104adaf3a3ebce0` (tree
`ecd79f93062ae969ba217358b12ba00366e81b20`), committed 2026-10-09 07:02:13 UTC and
retrieved 2026-10-10 10:54 UTC.
[Issue #471](https://github.com/jlevy/squares/issues/471) reports this release.
The author archives it as DOI
[10.5281/zenodo.23256655](https://doi.org/10.5281/zenodo.23256655), file
`squarepacker/k2-minus-c-upper-v1.0.zip`, 9,284,622 bytes, md5
`667f1a1ea308da2df5d309ec674c82c8` (the Zenodo record’s checksum), sha256
`87de5c9a4ab48d07a1825ba216ce9cc56ab39f5c6c2f1282cbb780282a0dfc26`; concept DOI
[10.5281/zenodo.23256654](https://doi.org/10.5281/zenodo.23256654). Version 1.1 is the
[2026-10-10 packet](../squarepacker-k2-minus-c-upper-v11-2026-10-10/README.md).

## What Is Retained

All 35 files of the tagged tree are in `acquisition/upstream-subtree.sha256`. 33 are
retained byte for byte under `source/`: the paper (`paper/paper.tex`, `paper/paper.pdf`,
`paper/LICENSE`), `README.md`, `.zenodo.json`, `SHA256SUMS`, `LICENSE`, every program
and recorded output under `code/`, and the three smaller certificates of Theorem 1.6 as
their original gzip files.

The two largest certificates, `data/stair_k38250000.json.gz` (2,577,279 bytes) and
`data/stair_k100000000.json.gz` (4,494,252 bytes), are pinned by digest and kept out of
Git under `OR-18`. They are hosted by
[`packing/hosted/squarepacker-k2-minus-c-upper-certificates.yaml`](../../../hosted/squarepacker-k2-minus-c-upper-certificates.yaml)
and are in the Zenodo archive above; their SHA-256 digests in the manifest equal the
source’s own `SHA256SUMS`. Fetch them from `packing/` with
`uv run --frozen --all-extras --group dev python -m devtools.hosted_data fetch --manifest hosted/squarepacker-k2-minus-c-upper-certificates.yaml`.

Every member of the Zenodo archive was compared here with the tagged tree by Git blob:
all 35 are equal, and `sha256sum -c SHA256SUMS` passes.
So the archive’s bytes are the commit’s.

## Credit, Licences and the Source’s Statements

Sungjoon Ryu is the sole author; credit **Ryu after Bui**. The source credits the
staircase of columns and the chained wall stairs to H. D. Bui (arXiv:2508.04603v2,
Sections 3–4), the L-shaped skeleton to Erdős and Graham and to Chung and Graham, and
the tilted block to Arslanov, Mustafin and Shangitbayev, and says its proofs are
self-contained. It cites this repository only as a problem collection.

The paper is licensed CC BY 4.0 (`source/paper/LICENSE`); the programs in `code/` and
the data in `data/` are MIT (`source/LICENSE`). Both notices are retained unchanged.

The source’s own statements, verbatim from `source/README.md`:

> **Status: not refereed.** The paper has not been refereed.
> It was written with AI assistance and has so far been checked only by AI-based reviews
> and by computer programs, some of them independent re-implementations (see
> “Verification status” below).
> No human expert has reviewed it.

> **AI-written.** The proofs, the text and all programs were developed with the
> assistance of Claude (Anthropic); the author takes full responsibility.

> All of these programs were written by AI systems of the same family, which may share
> blind spots. No human has reviewed the programs.

> Developed with the assistance of Claude (Anthropic), including the proofs, the text
> and the programs; the author takes full responsibility.
> Comments and corrections are welcome (please open an issue).

## Reported Claims

Read from `source/paper/paper.tex` and recorded as reported in
`packing/frontier/asymptotic-waste-bounds.yaml` (`deficiency_upper_bounds`), with c*(k)
= max{c : s(k² − c) = k}:

- Theorem 1.3: N(k,b) unit squares pack in a square of side less than k, so c*(k) ≤ k² −
  N(k,b) − 1 < 6b + 4k/b − 3 for 2 ≤ b ≤ k.
- Theorem 1.4: c*(k) ≤ 8⌈√(k−4)⌉ − 1 for every integer k ≥ 6.
- Theorem 1.2: c*(k) < 20.668 k^{2/5} + 0.623 for every integer k ≥ 1.6·10⁷.
- Theorem 1.1: c*(k) < 43.06 k^{3/8} + 2·10⁻⁵ for every integer k ≥ 4·10²⁶ (version 1.1
  keeps this statement and supersedes it by its tier A5).
- Theorem 1.6: c*(10⁵) ≤ 1583, c*(10⁶) ≤ 3972, c*(10⁷) ≤ 10039, c*(3.825·10⁷) ≤ 16988
  and c*(10⁸) ≤ 24790.

None settles a count n ≤ 324. The mathematical review is
[review-2026-10-10-squarepacker-k2-minus-c-upper.md](../../../../docs/project/reviews/review-2026-10-10-squarepacker-k2-minus-c-upper.md).

## Replays

`receipts/replay/replay.json` records, per job, the command, its wall time, its exit
status and how its output compares with the output the source records; the complete
outputs are in `receipts/replay/outputs.jsonl.gz`. They were written by
`packing/cases/asymptotic/ryu_upper_replay.py`, which rebuilds the tree from this packet
and the hosted certificates and runs each program with the project interpreter under
`python -I`. Two kinds of job are here:

- the source’s own programs (`const_stair.py`, `stair_check.py` at all five k and its
  seven negative controls at 10⁵ and 10⁸, `cert3e.py 160 64`, `run_z.py`), each compared
  with its recorded output;
- this repository’s checks written from the text, which share no code with the source:
  `ryu_upper_l_packing` (Theorems 1.3 and 1.4), `ryu_upper_constants` (Theorems 1.2 and
  1.1), `ryu_upper_staircase` (Lemma 7.3 at four sizes) and `ryu_upper_certificates`
  (Theorem 1.6 at all five k, with six controls at 10⁵ and 10⁸).

The replays reproduce what the source says its programs print.
They do not referee the proofs.

## Original Gzip Files

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `source/data/stair_k100000.json.gz` | upstream | `4ac6b650a09cb11754eec90a41430f32c87580df` | `68d858032be5db1622ffeebeecf75caa8fcb4cd59e512bc6a54e16a146987a1c` |
| `source/data/stair_k1000000.json.gz` | upstream | `085ac1586c03d2cc7ea976105baddd4ac09356b9` | `6aeeb2e14b6a9b9f86b81d809d659e3d12e02aa9dfd62b9cdb0d5ad0f5b0dc19` |
| `source/data/stair_k10000000.json.gz` | upstream | `38f322dd1a0b97d2ab4ddac85dbb1e7c8d733e38` | `8e6e12d2a208f5ffbd9968843102041a1671abc013bcf071e6902ee659ec9212` |

## Compressed Files

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |

## Check Retained Bytes

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source squarepacker-k2-minus-c-upper-2026-10-09 --check
```

This checks custody, not mathematical validity.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
