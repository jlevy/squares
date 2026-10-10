# Sungjoon Ryu’s Upper Bounds on the Deficiency c*(k), Version 1.1

Retained from
[squarepacker/k2-minus-c-upper](https://github.com/squarepacker/k2-minus-c-upper/tree/5742311db220b4bd8e825167aeae689a1bd65ce9)
at tag `v1.1`, commit `5742311db220b4bd8e825167aeae689a1bd65ce9` (tree
`a88be3b0bc4aa4e12a221121f6fee25fb2d5dbde`), committed 2026-10-10 09:20:20 UTC and
retrieved 2026-10-10 10:54 UTC.
[Issue #486](https://github.com/jlevy/squares/issues/486), opened 27 minutes after the
tag, reports this release.
The author archives it as DOI
[10.5281/zenodo.23278927](https://doi.org/10.5281/zenodo.23278927), file
`squarepacker/k2-minus-c-upper-v1.1.zip`, 9,542,766 bytes, md5
`d9e681e599152a533f056eaf82d85c0c` (the Zenodo record’s checksum), sha256
`2926895f4e6f224271e89fde561e372ec4af56475c1ff31a08a91ab7d2b82ab2`; concept DOI
[10.5281/zenodo.23256654](https://doi.org/10.5281/zenodo.23256654). Version 1.0 is the
[2026-10-09 packet](../squarepacker-k2-minus-c-upper-2026-10-09/README.md), which holds
the credit, licences and the source’s statements in full; version 1.1 states them in the
same words.

## What Is Retained

All 102 files of the tagged tree are in `acquisition/upstream-subtree.sha256`. The 74
files that are new or changed since version 1.0 are retained byte for byte under
`source/`: the paper (`paper/paper.tex`, 2,688 lines, and `paper/paper.pdf`), the
`README.md`, `.zenodo.json`, `SHA256SUMS` and `code/README_code.txt`, the changed
`code/stair_dump.py`, the coverings `code/cert_v3/` and `code/cert_v4/`, the exact tests
`code/zc_tests/`, and their recorded outputs under `code/checker_outputs/`.

The 28 files that keep their version 1.0 Git blob are pinned only.
Twenty-six are bound to the 2026-10-09 packet by `identical_to`, which
`acquire_source --check` compares byte for byte: the two licences, the six programs
`cert3e.py`, `chk.py`, `const_stair.py`, `r38.py`, `run_z.py` and `stair_check.py`, the
fifteen recorded outputs at the top of `code/checker_outputs/`, and the three smaller
certificates, which that packet retains as original gzip and lists in its Original Gzip
Files table, so they are compared as stored and not decompressed.
The two largest certificates are retained by neither packet and are bound by their
digests to
[`packing/hosted/squarepacker-k2-minus-c-upper-certificates.yaml`](../../../hosted/squarepacker-k2-minus-c-upper-certificates.yaml),
which hosts them.

Every member of the Zenodo archive was compared here with the tagged tree by Git blob:
all 102 are equal, and all 99 entries of `SHA256SUMS` verify.

## Credit, Licences and the Source’s Statements

Sungjoon Ryu is the sole author; credit **Ryu after Bui**, as for version 1.0. The paper
is CC BY 4.0 and the programs and data MIT, by the same notices.
Verbatim from `source/README.md`:

> **Status: not refereed.** The paper has not been refereed.
> It was written with AI assistance and has so far been checked only by AI-based reviews
> and by computer programs, some of them independent re-implementations (see
> “Verification status” below).
> No human expert has reviewed it.

> **AI-written.** The proofs, the text and all programs were developed with the
> assistance of Claude (Anthropic); the author takes full responsibility.

> All of these programs were written by AI systems of the same family, which may share
> blind spots. No human has reviewed the programs.

> The programs of the reviews, of the independent coverings and of the re-implementation
> are not included.

## Reported Claims

Theorem 1.1 of version 1.1: for each of twelve tiers, c*(k) < C_i k^{3/8} + a_i for
every integer k ≥ k_i, from 42.09 k^{3/8} + 0.05 for k ≥ 2.48·10¹² (tier C3) to 40.62
k^{3/8} + 1.4·10⁻⁵ for k ≥ 3.4·10²⁶ (tier A5, which supersedes version 1.0’s 43.06
k^{3/8} + 2·10⁻⁵). The tiers B use the variant wall filler ZC′ and Lemmas 8.2–8.5; the
tiers C also the sawtooth accounting and the per-band lift (Lemmas 8.6–8.8 and 8.11).
Theorems 1.2, 1.4 and 1.6 are stated as in version 1.0. The row is recorded as reported
in `packing/frontier/asymptotic-waste-bounds.yaml` (`deficiency_upper_bounds`).

The source reports three further coverings per tier, a direct un-normalised covering of
the tiers C, a 133-instance exact re-implementation and fifteen large end packings; none
of them is in the release, and they remain reported.

## Replays

`receipts/replay/replay.json` records, per job, the command, its wall time, its exit
status and how its output compares with the output the source records; the complete
outputs are in `receipts/replay/outputs.jsonl.gz`. The jobs are the source’s coverings,
replayed at the source’s resolution of 320 × 128 boxes in the source’s two slices per
tier: `cert_v3.py` for the nine tiers A and B and `cert_v4.py` for the three tiers C,
each slice compared field by field with its recorded slice, each pair merged with the
stated constants and compared with the recorded merge, the recorded slices merged again,
and `cert_v3.py`’s regression on the version 1.0 row.
Also `sl_t2_test.py 3000 500`, `p3test.py 10000 0.5 4 3/2 0.65 1` and `a10.py` for
`b2_zcp_102400`. They ran under `packing/cases/asymptotic/ryu_upper_replay.py` with the
project interpreter; `finalize_v3.py` was not run, because it rewrites `tiers_v3.json`
in its working directory and calls `python` from `PATH` (review finding RF-9), and its
merges were run directly instead.

The replays reproduce what the source says its programs print.
They are one covering per tier, the author’s, and they do not check the transcription of
the lemmas into the normalised inequalities.

## Compressed Files

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `receipts/replay/outputs.jsonl.gz` | receipt | `aecceadcb2417572cbec5997245bd2f5e6214203` | `4a5af900cd7c633020bcc8b5947ef550c9067831c3b51d8833a8d0f2cc073728` |

## Check Retained Bytes

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source squarepacker-k2-minus-c-upper-v11-2026-10-10 --check
```

This checks the full version manifest, the retained bytes and the 26 copies bound by
`identical_to`. It does not verify the theorem.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
