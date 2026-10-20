# Review Programs, 20 October 2026

These are the programs that the stage 4 review lane of the 20 October intake wrote and
ran for
[`review-2026-10-20-de-winter-668-upper-bounds.md`](../../../../../../docs/project/reviews/review-2026-10-20-de-winter-668-upper-bounds.md),
the review of Joost de Winter’s three certificates of issue #668 (T-196, bead
`think-455r`), with what they printed.
The lane was an AI agent of the Claude system family (Anthropic), strong sub-agent tier,
maximum reasoning (`c-review-704-fable`), prompted separately from the replay lane that
built the adapter and the receipt and from the records lane of pull request #704. It ran
them on 20 October 2026 in a worktree at `efcd4ddac`, the head of
`claude/intake-2026-10-20-de-winter-668`, under `nice -n 10` on a shared four-core host.

## What Decides What, and What Is Registered

`review_704_check.py` is this review’s own exact route: written for it, standard library
only, importing nothing from this repository, with its own reader of the centre-basis
JSON. It decides the unit circle, half-extent containment, every one of the $n(n-1)/2$
pairs by separating axes on the squares’ unit edge normals, and every pair whose centres
are within $\sqrt2$ a second way, by the exact area one square’s four closed half-planes
clip from the other.
It is registered as `V-de-winter-668-review-check`.

`sharp_controls_704.py` builds six mutants per count and decides them through the
adapter and this repository’s two maintained routes, `sqpack.verify` and the independent
rational corner checker, and through the review checker’s clipping area on the moved
pair. Its decisions are the two routes’; it adds the mutants, the clipping check and the
outcomes it expects.
It is registered as `V-de-winter-668-sharp-controls`.

`margins_704.py` computes each side, each print and every margin against the case
ceilings and the other sides registered or pending at each count.
It decides no geometry.

`E-de-winter-668-upper-exact-feasibility` cites the two registered programs beside the
maintained replay.

## Programs

The programs read decompressed copies of the packet’s three certificates and of its
receipt from a data directory outside the repository; they do not read the packet’s
gzipped and xz-compressed files directly.
From `packing/`, with the project interpreter, `P` this directory’s `programs/`, `DATA`
the data directory and `OUT` a directory for what they write:

```sh
P=resources/web/de-winter-upper-bounds-227-229-260-2026-10-17/review/review-2026-10-20/programs
PACKET=resources/web/de-winter-upper-bounds-227-229-260-2026-10-17
mkdir -p DATA
for n in 227 229 260; do gzip -dc $PACKET/source/n$n/n${n}_exact.json.gz > DATA/n${n}_exact.json; done
xz -dc $PACKET/receipts/exact-certification.json.xz > DATA/receipt.json
uv run --frozen --all-extras --group dev python -I $P/review_704_check.py DATA DATA/receipt.json OUT/out-check.json
uv run --frozen --all-extras --group dev python -I $P/margins_704.py .. OUT/out-margins.json
# sharp_controls_704.py reads REVIEW_DIR/data/ and REVIEW_DIR/out-check.json and
# imports review_704_check from REVIEW_DIR; copy the program and out-check.json there.
uv run --frozen --all-extras --group dev python REVIEW_DIR/sharp_controls_704.py REVIEW_DIR 260 227
```

| Program | What it read | What it printed | Kept output |
| --- | --- | --- | --- |
| `review_704_check.py` | the three certificates, decompressed, and the receipt | 3 of 3 passed: every basis on the unit circle; 25,651, 26,106 and 33,670 pairs decided by separating axes with none overlapping or touching; 459, 530 and 542 pairs within $\sqrt2$ clipped to area exactly 0; each least wall clearance ($10^{-9}$ exactly) and least pair gap equal to both routes’ to every digit; each print the side rounded up at 12 places; 4.8 s, 5.2 s and 2.7 s of CPU | `outputs/out-check.json`, `outputs/check.log` |
| `sharp_controls_704.py` | the 227 and 260 certificates, decompressed, and `out-check.json` | at both counts: W1 (side lowered by exactly the clearance) and P1 (least-gap pair closed by exactly its gap) passed on both routes at exact contact; W2 and P2, each $10^{-30}$ further, refused on both routes with a wall clearance or pair gap of exactly $-10^{-30}$, and P2’s clipping area positive; B1 (a basis $10^{-30}$ off the unit circle) and B2 (a coordinate as a JSON number) refused by the adapter | `outputs/out-controls-n227.json`, `outputs/out-controls-n260.json`, `outputs/controls.log` |
| `margins_704.py` | the certificates, the retained Daniel packet’s T-101 headers, the regularized sides T-155 reads, `acquisition/claims.json` and the #678 header | the sides and margins of the review’s Claims Covered and Adoption per Count tables | `outputs/out-margins.json` |

`outputs/pytest.log` is the review’s run of the packet’s ten tests and the adapter’s
read and refusal tests: 68 passed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
