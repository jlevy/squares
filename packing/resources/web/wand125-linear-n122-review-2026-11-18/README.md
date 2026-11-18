# Stage 4 Review of T-144: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane r144-1118’s blind stage 4 review
of T-144, wand125’s linear certificate `mixed_n122_L1126` for $s(122) \ge 563/50$ and
its transfer to $n = 123$ to $126$:
[`docs/project/reviews/review-2026-11-18-wand125-linear-n122.md`](../../../../docs/project/reviews/review-2026-11-18-wand125-linear-n122.md).

The source is not retained here, and this directory is review-only.
On `main` the import packet
[`wand125-linear-n122-2026-10-10`](../wand125-linear-n122-2026-10-10/README.md) holds
the manifest, not the candidate or the certificate, so this lane fetched them itself:
the documents from wand125/square-packing at
`a9f76c382d023b4095899c4eb7ea7483b8b87ecf` (blobless, 05:38Z on 18 November 2026), and
the release asset `certificates__mixed_n122_L1126.tar.gz` of `square-lower-bounds-v1`
(05:41:37Z). The asset is 31,784,537 bytes with SHA-256
`6443eae03c56dc99051965246dbf97f5f3540feb9c011eac96e6d094521f5deb`, the release API’s
digest. Both stayed in the lane’s scratch space and were deleted when the review ended.
The programs take their paths as arguments, so a rerun needs a fetch of the same pin
and asset.

## Layout

- `programs/`: the review’s programs and the controls plan (`controls-plan.json`).
- `frozen/`: the digests of the checker and the plan at their freeze
  (`checker-frozen-digests.txt`, 06:03:49Z), the findings’ digests at theirs
  (`findings-frozen-digest.txt`), and the frozen review text.
- `out/`: the receipts. `out/bnb-all/` holds the complete decision of nodes 1 to 200,
  one file per range of 25 nodes.

## Programs

Every program is the lane’s own, written for this review from the mathematics and the
certificate’s documents (its README, `manifest.json`, `completion-audit.json` and the
shape of `candidate.json` and `input.txt`). None imports anything from this repository
or from the source, and none was written after reading the source’s checker or code:
`code/` was hashed, not opened, until the checker froze.
They ran under CPython 3.14.7, the project interpreter, as `python -I -B` at
`nice -n 19`, one process at a time, with numpy 2.5.2 on one OpenBLAS thread.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `r144_common.py` | nothing (a module): the strict readers, the $D_4$ images, the net node’s exact $t$, $\cos$, $\sin$ and $E_j$ | the bytes it is handed | nothing |
| `r144_exact.py` | nothing alone (a module): the exact capture of a core at a pose, by two methods written apart | a measure and a pose | nothing |
| `r144_premises.py` | every exact premise, the custody of the pinned documents, the asset and the 810 bundle files, the 201 records, and the comparisons with Green’s $G_{11}$, Nagamochi’s $1 + \sqrt{105}$ and $\sqrt N$ | the pinned documents, the packet manifest on `main`, the asset and the bundle | `out/premises.json.gz` |
| `r144_inputs.py` | that each of the 201 checker inputs encloses the recomputed $L$, $B$, $E_j$, $\cos$, $\sin$, $\gamma$ and exactly the multiset of the 14,184 images | the bundle | `out/inputs.json` |
| `r144_axis.py` | node 0 completely, by the vertex argument, in exact integers and a bounded binary64 matrix product | the candidate | `out/axis-node0*.json` |
| `r144_bnb.py` | nodes 1 to 200 completely, by a rigorous branch and bound on boxes of centres | the candidate | `out/bnb-sample*.json`, `out/bnb-all/` |
| `r144_run_all.sh` | nothing itself: drives `r144_bnb.py` over nodes 1 to 200 in ranges, under a CPU budget | the bundle path | `out/bnb-all/` |
| `r144_poses.py` | nothing: exact captures at 1,608 fixed poses and a seeded search at 24 nodes, compared with 1 and with the source’s least leaf bounds | the candidate and the 201 records | `out/poses.json.gz` |
| `r144_lanes.py` | which lanes of the case records 563/50 would raise at 122 to 127 | `packing/frontier/n-122.md` to `n-127.md` | `out/lanes.json` |
| `r144_release_sums.py` | whether the release’s `SHA256SUMS` lists the asset | that file and its API digest | `out/release-sums.json` |
| `r144_selftest.py` | nothing about the certificate: the controls on the programs above | synthetic measures, and mutated copies of the real candidate and node 37’s input | `out/selftest-*.json` |

`r144_run_all.sh`, `r144_lanes.py` and `r144_release_sums.py` were written after the
controls plan, and two frozen programs changed after the checker’s freeze. Both changes
are disclosed in the review’s [What This Review Ran](../../../../docs/project/reviews/review-2026-11-18-wand125-linear-n122.md#what-this-review-ran).
`r144_premises.py` takes its square roots of 2 and 22 to 200 digits instead of 60,
since the source’s bound on $G_{11}$ lies within $2 \times 10^{-60}$ of it.
`r144_poses.py` gained `--draw`, which draws the six seeded search nodes.

## Running Them

From the repository root, with `PIN` the pinned tree, `ASSET` the asset, `OUTER` its
extraction and `BUNDLE` the extracted inner bundle (`n122-L11.26-proof-bundle/`):

```bash
R=packing/resources/web/wand125-linear-n122-review-2026-11-18
PY="packing/.venv/bin/python3 -I -B"
export OPENBLAS_NUM_THREADS=1
$PY $R/programs/r144_selftest.py --synthetic --work /tmp/r144 --out $R/out/selftest-synthetic.json
$PY $R/programs/r144_premises.py --pin $PIN \
  --manifest packing/resources/web/wand125-linear-n122-2026-10-10/source-manifest.json \
  --asset $ASSET --outer $OUTER \
  --bundle-tar $OUTER/certificates/mixed_n122_L1126/n122-L11.26-proof-bundle.tar.gz \
  --bundle $BUNDLE --repo . --out $R/out/premises.json
$PY $R/programs/r144_inputs.py --bundle $BUNDLE --out $R/out/inputs.json
$PY $R/programs/r144_selftest.py --real $BUNDLE --work /tmp/r144 --out $R/out/selftest-real.json
$PY $R/programs/r144_axis.py --bundle $BUNDLE --out $R/out/axis-node0.json
$PY $R/programs/r144_axis.py --bundle $BUNDLE --factor 99/100 --out $R/out/axis-node0-99_100.json
$PY $R/programs/r144_bnb.py --bundle $BUNDLE --angles 37,108,180,200,1 --out $R/out/bnb-sample.json
$PY $R/programs/r144_bnb.py --bundle $BUNDLE --angles 37,180 --factor 99/100 \
  --out $R/out/bnb-sample-99_100.json
$PY $R/programs/r144_poses.py --bundle $BUNDLE \
  --search-nodes 0,1,2,25,36,37,83,108,150,155,157,163,164,180,185,196,199,200 --draw 6 \
  --out $R/out/poses.json
$PY $R/programs/r144_lanes.py --frontier packing/frontier --out $R/out/lanes.json
$R/programs/r144_run_all.sh $BUNDLE $R/out/bnb-all 7200
```

`r144_release_sums.py` takes the release’s `SHA256SUMS`, downloaded beside the asset,
and the digest and update time that `gh api repos/wand125/square-packing/releases/tags/square-lower-bounds-v1`
gives for it.
Each program exits 0 and prints its verdict. Two receipts over 1,000 lines are kept as
`gzip -9n` (table below), as the packet rule in
[`packing/resources/README.md`](../../README.md) asks; a rerun writes them plain.

## What They Printed

| Program | Printed | CPU (s) |
| --- | --- | ---: |
| `r144_selftest.py --synthetic` | `SELFTEST_PASS` (S1 to S6) | 1.5 |
| `r144_premises.py` | `PREMISES_HOLD`, 79 checks | 3.1 |
| `r144_inputs.py` | `INPUTS_ENCODE_CANDIDATE`, 201 headers, one shared body | 3.9 |
| `r144_selftest.py --real` | `SELFTEST_PASS` (S4 to S7) | 7.3 |
| `r144_axis.py` | `AXIS_DECIDED`, least capture $1.0039577044\ldots$ | 0.5 |
| `r144_axis.py --factor 99/100` | `AXIS_REFUSED`, exact witness $0.99391820956\ldots$ | 0.5 |
| `r144_bnb.py`, nodes 37, 108, 180, 200, 1 | `NODE_DECIDED` at each | 121 |
| `r144_bnb.py --factor 99/100`, nodes 37, 180 | `NODE_REFUTED` at each, exact witnesses $0.99953$ and $0.99910$ | 0.2 |
| `r144_poses.py` | `NO_COUNTEREXAMPLE_FOUND`; methods A and B agree at all 1,608 fixed poses | 53 |
| `r144_lanes.py` | raises the reported lane at 122 to 125 and the verified lane at 122 to 126 | 0.1 |
| `r144_release_sums.py` | `SUMS_DO_NOT_LIST_ASSET`, 465 entries | 0.1 |
| `r144_run_all.sh` | FULL_RUN_PLACEHOLDER | FULL_RUN_CPU |

The first `r144_premises.py` run printed `PREMISES_FAIL`, with one failed check: at 60
digits, its enclosure of $G_{11}$ could not separate it from the source’s bound. The
200-digit rerun holds; nothing else failed along the way.

## Compressed Files

| Stored file | Origin | Git blob (decompressed) | SHA-256 (decompressed) |
| --- | --- | --- | --- |
| `out/premises.json.gz` | receipt | `40cb2b3ee5566e5730e50935562de43ad56ee927` | `57918dcc47f892d96f2f18921f46cc4961e580d27a1cc28bea4c73317192a6b3` |
| `out/poses.json.gz` | receipt | `1a6a1fc5076a8ebd93d32941a9c49b9598a3abd6` | `cac19bdf026e914dcc8d3dff2638968e19c617df1327a4106770d2370bbc0d88` |

Restore a plain copy with `gunzip -k out/premises.json.gz out/poses.json.gz`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
