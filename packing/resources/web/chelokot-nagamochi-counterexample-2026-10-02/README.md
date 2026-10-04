# chelokot’s Counterexample to Nagamochi’s Lemma 1

This packet retains one note from chelokot’s public repository
[`chelokot/square-packing-archive`](https://github.com/chelokot/square-packing-archive),
cited here as **[chelokot Nagamochi counterexample 2026]**. The note,
`docs/nagamochi-score-counterexample.md`, exhibits a square of side $1.0001$ in the
$4 \times 4$ container whose score under the weights of Nagamochi 2005, Section 3, is
below 1, contradicting that paper’s Lemma 1.
The X-049 literature lane found it on 2026-10-02 as one of the sources outside this
archive, and it was retrieved the same day.

It is an unrefereed repository note, cited for what its author says.
Nothing in it was replayed here: neither its Python checker nor its Lean proof was run.

## What Was Retrieved

Retrieved 2026-10-02 at 06:47 UTC by `git clone --depth 50` of the default branch
`main`, whose head was `753079eb37d8d16225a5dc1f56e493a3c3b243f4` (committed
2026-09-06T00:42:12+03:00). The note was last changed at
`b22137f74663cbb55015ad54488c272db5474ae5` (2026-09-05T02:39:33+03:00), first added at
`257a2456846b147708d61da70863fd86cacb5407` (2026-09-04T23:32:45+03:00), and is unchanged
from there to the head.

| Retained path | Upstream path | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `upstream/docs/nagamochi-score-counterexample.md` | `docs/nagamochi-score-counterexample.md` | `7df93500d0ee709a94429c45b5c8f42c9d064f35` | `a41f30bb438c8379ce2f11c27d38ca901bacff1d5e72d697fb0f4b35adf8c1f0` |
| `upstream/docs/assets/nagamochi-counterexample.svg` | `docs/assets/nagamochi-counterexample.svg` | `68cc97e30ccf80b22f737ca427d653f6235e639e` | `22209dc1705847498955cf39ddb5f433d8769ca39d065c47ea69c91b314bd289` |
| `upstream/LICENSE-DATA` | `LICENSE-DATA` | `51a386b7c7a253c22cb610ca883acba9ebb085de` | `21603ef75b2d0373f70212259e3846090e67b78c518de3fb9f7eb1a5eda51a96` |
| `upstream/NOTICE` | `NOTICE` | `229a75984321a5d12d56f5b56ad2380e6df03ef9` | `248c771cae0fadc047555a71987d322244b23996113b4535ecfd4da55e50b5e5` |

The four files are byte-identical to the upstream blobs.
The note’s raster figure, which duplicates the retained vector one, and the files the note
links to are pinned by digest and not retained:

| Upstream path | Last changed | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `docs/assets/nagamochi-counterexample.png` | `964e9b3` | `5c2ac1a15c797d4c29957de5eff26d10b44d7962` | `338c14252fa6e699d6e059f39fd9a7b34bdc4cb34b6de2d1a1a63f435c6c0911` |
| `scripts/check-nagamochi-counterexample.py` | `964e9b3` | `846282b63270b88a01f21f87e2773daac6970cd6` | `e960c0d24f2e5b72a8e0322deb7c82382cedd9aa014af09fee525e9462cda48b` |
| `formal/SquarePackingArchive/NagamochiCounterexample.lean` | `257a245` | `9b68f6a4d2073ea3028ae57019e91bdbbda9cf59` | `c167e2560de804dd85d037443bef6faa3a78a561f89c6ede8fbe751c7f92d10e` |
| `docs/nagamochi-compensation-proof.md` | `b22137f` | `f1e56138e628b7057b5ac8df5979d6a434328f36` | `5dde19136ad0e00bf47fdc0961d9db305ec81172457f5c0489309cf61487e2f6` |
| `formal/SquarePackingArchive/NagamochiPackingTheorem.lean` | `b22137f` | `da209bad1b6739f52f4b74c1af9b2ca6e788c6d1` | `5b758d113191196d6f3b86bb2ffb76fdfa8eceac1952616c01f89a4b22e6e185` |
| `docs/nagamochi-counterexample-search.md` | `b22137f` | `a082c96f94db7ae9c4425ac9d73954d9a5a1e145` | `ef5464fc66eb132315702c7aa3a15daa48dc42748d11571542fc2c7c82f23edb` |
| `ATTRIBUTION.md` | — | `abbb98d95b6850f6a25d64687b6ad140d1b5c97e` | `b2c24979e99a14e044465dfa570fb8377b6adb3f7ac7ca3d4a5d874d98e90108` |
| `LICENSE` | — | `0689722091a56c5b1a9e1c75fd1f09ce9596db5b` | `0ca42234e7e75daa9d94096c6d24b54ea9c77060d9471e769ba0ab43cacc189f` |

## Licence and Attribution

The repository’s README licenses code and Lean sources under Apache-2.0 (`LICENSE`) and
“archive metadata, original prose, and generated visualizations” under CC BY 4.0
(`LICENSE-DATA`). The retained note is original prose and its figure a generated
visualization, so both are retained under CC BY 4.0, with `LICENSE-DATA` and `NOTICE`
kept beside them. Attribution: chelokot, Square Packing Archive contributors, 2026.
`ATTRIBUTION.md` names chelokot as project creator and credits AI-produced research and
Lean formalizations to an AI system; it is pinned above rather than retained.
The repository does not cite this project.

## What the Note Claims

- A square of side $\lambda = 10001/10000$, cosine $80/1601$ and sine $1599/1601$, with
  bottom vertex $(10419467/5330000, 0)$, lies in $[0,4]^2$ and scores exactly
  $25009470849041/25584000000000 \approx 0.977543 < 1$: area $0.023883$, half the
  horizontal line length $0.489160$, half the vertical $0.0145$, and the point
  $(1, 0.9)$ at $9/20$. The point $(2, 0.9)$ lies $0.0001$ outside.
- The Lean file proves the weaker bound $\text{score} \le 199/200$, with only the
  standard axioms; the Python checker computes the exact fraction.
- The gap is Case 6 of Nagamochi’s proof: Lemma 6 needs the edge touching $(2, 0.9)$ to
  cross $y = 1$, and after a shift of $1/10000$ it does not.
- The note does not claim a packing that beats any bound, and says it does not disprove
  $s(n^2 - 2) = n$.

[Karakuş 2026](../../papers/karakus-2026-counterexample-nagamochi-scoring-lemma.md)
locates the same gap, the missing edge incidence in the application of Lemma 6 in
Section 5.5, Case 6, with a different one-parameter family; that paper does not cite
this note, which predates it by 25 days.

## Pointer for the T-007 Review

The note links `docs/nagamochi-compensation-proof.md`, pinned above, which states a
closed Lean theorem, `Records.NearSquare.squareMinusTwo_isMinimumSide`, that
$s(n^2 - 2) = n$ for every integer $n \ge 2$, by compensating low-scoring squares with
other squares of the packing rather than assuming Lemma 1. Karakuş 2026 says its own
argument does not establish that identity. The claim is neither retained nor checked
here; it bears directly on the review of T-007 against Karakuş 2026 (`think-589i`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
