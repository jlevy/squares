# Evan Daniel’s Exact Sides for 23 Current Records

Evan Daniel published exact algebraic forms of the record’s current best-known packings
at 23 counts in [evand/square-packing](https://github.com/evand/square-packing), under
`search/exact/cur/`, and asked for their registration in
[issue #639](https://github.com/jlevy/squares/issues/639) (opened 2026-10-16T03:37:13Z).
The directory was added by `058b67133f4130ce36bf43ee1c13b53948289343` (committed
2026-10-16T03:30:10Z) and annotated by `7d1407a0b66c46e32cdbcbd5619586fe2bdd52a1`
(committed 2026-10-16T03:33:01Z), the head of `main` when it was read and the commit the
issue names, which is the pin.
The clone was made at 2026-10-16T06:02Z.

## What the Source Claims

For each $n$ in 51, 70, 88, 102, 123, 126, 153, 172, 175, 199, 204, 207, 232, 258, 259,
263, 266, 267, 292, 295, 297, 301 and 302, `data/n-N.minpoly.json.gz` holds an exact
configuration of the packing the record listed as best known at that count on 15
October: a number field $K = \mathbb{Q}[t]/f$, a rational interval isolating one real
root $t^\ast$ of $f$, every square’s centre $(x, y)$ and angle parameter
$u = \tan(\theta/2)$ in $K$, and the side $S \in K$ with an integer polynomial $p$ and a
rational interval in which $S^\ast = S(t^\ast)$ is the only root of $p$.
The claim is $s(n) \le S^\ast$, with $p$ of degree 2 to 41; three are quadratic,
$s(51) \le (16 + 5\sqrt2)/3$, $s(126) \le 15/2 + 3\sqrt2$ and
$s(295) \le 22(1 + \sqrt2)/3$.
[RESULTS.md](source/search/exact/cur/RESULTS.md) tabulates them.

The source checked them twice.
`verify_data.sh` runs `search/exact/verify_exact.py`, a standard-library checker in exact
rationals, on all 23 files: 23 of 23 VALID, about four minutes on eight processes
([data/verify.txt](source/search/exact/cur/data/verify.txt)).
`crosscheck.py` places the solver’s 64-digit Newton side inside the interval of each $p$
and, at 51, 102, 126 and 295, recovers $p$ from those digits with `mpmath.findpoly`
([crosscheck.json](source/search/exact/cur/crosscheck.json)).
The issue says each $p$ is irreducible; no program in the directory or in
`verify_exact.py` checks irreducibility, so minimality is the source’s assertion.

The [README](source/search/exact/cur/README.md) compares each $S^\ast$ with the
register’s reported value at `main` `4e8c898` and says that at 153 and 207 a re-run on
the register’s own witnesses gives the same $p$; at 207 that re-run did not verify pair
(73, 74), so the committed form there is from a copy that ties the register’s witness.
It lists 52 counts still without an exact form; that list is not a claim.

## Retained Here

`devtools.acquire_source` wrote the packet from a blobless clone at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
35 files, 21,552,062 bytes, over `search/exact/cur/`, `search/exact/verify_exact.py`,
`LICENSE` and `CREDITS.md`.
Retained: 30 files, 787,378 bytes, among them 19 of the 23 exact forms as their upstream
gzip (720,878 bytes), listed under [Original Gzip Files](#original-gzip-files).

Pinned by size and SHA-256 and not retained:

| Upstream path | Bytes | SHA-256 | Why |
| --- | --- | --- | --- |
| `search/exact/cur/data/n-204.minpoly.json.gz` | 3,534,100 | `59cd30fc2b68ce65beb86fd5a5a881e4256ce375305e510ce4b23ee6e02c70bb` | bulk data (OR-18) |
| `search/exact/cur/data/n-263.minpoly.json.gz` | 8,960,033 | `d07bda8a3e78e0af0390cc09d4fb820f373e26cff5147791ca0587d6eac4020f` | bulk data (OR-18) |
| `search/exact/cur/data/n-267.minpoly.json.gz` | 1,545,171 | `09a7ca619f96a240ec7416008e1d40f3768596a2d6e0a18bba0505eec4b47907` | bulk data (OR-18) |
| `search/exact/cur/data/n-297.minpoly.json.gz` | 6,714,645 | `6037de6de4d2c28a2a3bd92bca26fea64f31cbbfdc94519276059e158bade939` | bulk data (OR-18) |
| `search/exact/verify_exact.py` | 10,735 | `a0f38ca87c13c7e1b1d6ca99d69adea47df6008a645e3b4dbb79e8e0af35bab4` | byte-identical to [the copy retained at `ad86d42`](../evand-exact-and-local-reports-2026-10-12/source/search/exact/verify_exact.py) |

The four large forms are 20.75 MB of the directory’s 21.5 MB.
Anyone can fetch them from the pinned commit and check them against these digests; a
replay here does so before it reads them.
The rest of the repository is pinned by the commit alone, and nothing of it was executed
in the repository.

## Replay of the Source’s Checker

On 16 October 2026 `verify_exact.py`, read in full first, ran unchanged from the
[retained copy](../evand-exact-and-local-reports-2026-10-12/source/search/exact/verify_exact.py)
on all 23 exact forms, the four pinned-only ones from a copy fetched from the pinned
commit and held to the manifest, each in its own `python -I` process under CPython
3.14.7, two at a time on a shared 4-core host
([review/replay_verify_exact.py](review/replay_verify_exact.py),
[review/README.md](review/README.md)).

- **23 of 23 VALID**, each with the statement `data/verify.txt` prints for it, in 1,427
  CPU seconds; 263, 297, 204 and 267 took 568, 351, 241 and 136 s.
- **76 of 76 controls refused**, four at each of the 19 retained forms: a square moved
  $10^{-6}$ through the wall it touches, the side raised by $10^{-6}$ in the field, the
  side’s interval moved below its root, and a duplicate square, in 58 CPU seconds.
- **Every polynomial squarefree and irreducible** over the integers by SymPy 1.14.0’s
  `factor_list`: one factor, of multiplicity 1 and of the polynomial’s degree, the four
  pinned-only forms included, so each side is algebraic of the degree the source states.

The receipt is [receipts/replay-verify-exact.json](receipts/replay-verify-exact.json),
refreshed on 16 October after PR #651’s review A (A5, A6) by the fixed driver, which
refuses a perfect power as irreducible and keys its resume cache by input, checker and
control. Its first invocation was stopped by the session’s background-time limit after
four positives and resumed from that cache; the counts above are summed over both.
This is the source’s own checker on the source’s data, one route: it shows each
configuration passes the checks `verify_exact.py` makes, and its soundness is that
program’s. The checker does not itself check that a file lists exactly $n$ squares; the
16 October ledger’s `exact_sides.py` does, at every count.

## Witnesses for the House Best Packings

On 23 October 2026 the house rule adopted T-193 at the six counts whose forms the
packet retains and whose regularization items owe no correction: 102, 123, 258, 259,
295 and 302 (think-ot5c).
A house best packing’s witness is a Witness/v2, so
[acquisition/algebraic.json](acquisition/algebraic.json) declares each of the six as a
retained exact form, and `devtools.algebraic_witness_reports derive-forms` writes it as a
derived fact, `facts/alg-n-NNN.yaml.gz`: the form’s field, side and centres exactly, and
each square’s basis $R^m((1 - u^2)/(1 + u^2), 2u/(1 + u^2))$ computed exactly in the
field from its half-angle tangent $u$ and quarter turns $m$, as `verify_exact.py` reads
them.
No upstream byte is copied into a fact; `derive-forms --check` derives them again from
the retained forms, each held to its pinned digest.

`certify` then decided each fact on `sqpack`’s exact verifier over its field, a positive
with its duplicate-square and outside-container controls, each job in its own process,
two at a time on a shared 4-core host: 18 jobs, 504,102 pair decisions, 684.99 route CPU
seconds, the longest job 230.72 s wall (302).
The six positives pass and the twelve controls are refused, and
`receipts/algebraic-route1-nNNN.json.xz` keep them.
This is a second decision of the six configurations, by the one route over a number
field this repository maintains, beside the source’s own checker; no evidence entry
registers it yet, and the house’s witness carries its positive’s native result.
The other ten of T-193’s counts have no fact: eight wait for think-8ido to correct their
regularization items, and 204 and 267 are pinned only, 204 now housed by a smaller
packing.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`, unchanged since the earlier evand packets.
The packings are their finders’: the issue says “The packings are their finders’ (the
register’s credits in the table). Method and code as in #419.”
On AI assistance the issue says: “The solver, checkers and this batch were written and
run with Claude (Anthropic) as a coding and research agent, directed and reviewed by
me.” Both commits carry a Claude co-author trailer.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/alg-n-102.yaml.gz` | receipt | `009e7dccc3589739a733cf38b47cc67ade1d88dc` | `2697e89a0a5f1a4698ee973f7af45b3b005303594988a7de14b3b35a6596c14b` |
| `facts/alg-n-123.yaml.gz` | receipt | `a07ee718e938c73bf5760dc7ecdc097966eb7aff` | `12edcc1f6014122eb241c2f105dd9e6656a2c871f86f889b026b2d0381afa197` |
| `facts/alg-n-258.yaml.gz` | receipt | `5ed766fc9b5c5e1e5a5d20bcfd63b9d0dff94bea` | `f55d0c95ca55912ec957751a3c3e7931966fd2e3fc03e60969d469f1fd7c59d8` |
| `facts/alg-n-259.yaml.gz` | receipt | `5331176ce8cf5ed030881362c13b53724e090847` | `e0a345be4ffe32b10b8b50de9f2d88d9e961504d401e069a57be8d111b4574cb` |
| `facts/alg-n-295.yaml.gz` | receipt | `6c3547e2c0134c84f7bfae018132e1137dd99f6c` | `93cc8c4d1f36f9f4b22cbc43321e608c1265c4cb7e79ef5fbad9f0b93712a1aa` |
| `facts/alg-n-302.yaml.gz` | receipt | `3b6e20fbc097097972521adfe28896cb722a0fcb` | `e7510f0f604ec641d1c285694af2b950555ba92ad1f4844c7b182ed527a0e612` |

## Original Gzip Files

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `source/search/exact/cur/data/n-51.minpoly.json.gz` | upstream | `05ff2dc8ca2f8341c18025634a4c048bc55dad3d` | `d5c90fb3bdb28d5a0f2f5482ad9f65e6f2c721783940681b7bec079fc3a563d6` |
| `source/search/exact/cur/data/n-70.minpoly.json.gz` | upstream | `a3fec5fc9803676dff789e46cb8588866c221e56` | `ebcdfbe8ef670dcd26f4f2e87b961174eb2d818aeaab537f9682b5df6c7bcf8c` |
| `source/search/exact/cur/data/n-88.minpoly.json.gz` | upstream | `d224596a204aadf27aca10cb0a34b14ac2681a0a` | `a2994e3e1b15e2768898e73ed70ac58273e11535980e68cecbf2465b8c62a3ae` |
| `source/search/exact/cur/data/n-102.minpoly.json.gz` | upstream | `7c057e0674ab529e1bbd39f64c564b6b0a37bd97` | `f18300ab42162acd060ac5e85878c3aa79ea460d5284f69da2e746dabfdd985f` |
| `source/search/exact/cur/data/n-123.minpoly.json.gz` | upstream | `0a5aeac48758ad28d25a306d3163edab02eb0365` | `891d9aa5e11e60ddfb710dd707451192ff034d6b1e276940168bf3f657c21cd6` |
| `source/search/exact/cur/data/n-126.minpoly.json.gz` | upstream | `bda1b3ff60293b8341ff90f38173b19533ad6eea` | `ca327d76bad09ed7d292db14d19050de4afc28f75d61655af327b4cf0be69004` |
| `source/search/exact/cur/data/n-153.minpoly.json.gz` | upstream | `5d5281d06ca25e4e5107b216da58b46cfb147d07` | `0e87edab97190413602ea7f04248dc928e4347878fca35a33e32d015a9e9b5dc` |
| `source/search/exact/cur/data/n-172.minpoly.json.gz` | upstream | `8ccd3099ab5d6e2094c18f67c2ee952b650b2b6a` | `e1fdda84c70abe8a0f787baf725bda363cf6fd282d3732dac5cdf092731fffa5` |
| `source/search/exact/cur/data/n-175.minpoly.json.gz` | upstream | `4f6ea76add0e3274c4c3c514ca5530ac9f154a43` | `c612cbbe465ad8f8b7f1a50f7b9c85737041fe15fdcd758c850bae888ca3c13c` |
| `source/search/exact/cur/data/n-199.minpoly.json.gz` | upstream | `11354eb686fd14e3da81e4418c0165f26123a685` | `9374939e4ed7ba0c9486c3f7dbb1177423da86d0e7e948100600ce3ec6783516` |
| `source/search/exact/cur/data/n-207.minpoly.json.gz` | upstream | `f611b5bbca6549c8aa27836af44ea04892bff6c9` | `f39fedbf8b64411ee31973ddce92343c9dd922f937831ef42d69d8104f0cef85` |
| `source/search/exact/cur/data/n-232.minpoly.json.gz` | upstream | `5baf1d1130c8b0ea8f7736a7838ab6c7aecb6719` | `7386edf3c3066102e8fb7ce1dccca0bdea729fcd92f80384aed3289b9fd1bbc7` |
| `source/search/exact/cur/data/n-258.minpoly.json.gz` | upstream | `75e9eeec2b96f97c2298cebd9162fc6a01c815c4` | `e0656208342c530bf4b013e69b2c7113cd1c2d7ce54ab7a443aaa74ac0fe73bf` |
| `source/search/exact/cur/data/n-259.minpoly.json.gz` | upstream | `5d84bbb833bb9df0bcf6c347a420d4eae3aa68e6` | `5e9ffafc766a0a5a5090b66a418383e83c6b4b3f7efd9f1c94c5213185ca565f` |
| `source/search/exact/cur/data/n-266.minpoly.json.gz` | upstream | `08aa9e16acd3036f680c4894890f8f03367b716d` | `e5221442c72ba92d11969106808ca90024c68e1f3c1d4394efb00348ed220ff1` |
| `source/search/exact/cur/data/n-292.minpoly.json.gz` | upstream | `cc088e54e7945bb38038348458da0609f6285cef` | `1e6c03a90eb75f0cbe77b77800cc3790b6bd4e431461d493146267b4b9e57ecc` |
| `source/search/exact/cur/data/n-295.minpoly.json.gz` | upstream | `dd57152404b7374037b6f75552bc95a201fd2812` | `40ef2669ce031f832806c0f8942eae2a7b533064d027d8e82e020e891bf82d94` |
| `source/search/exact/cur/data/n-301.minpoly.json.gz` | upstream | `ad4b54281094d98f5cc19499eedff0e18dd0037b` | `5d262ea23a4f86601798b8def37308cf6a788be080b5225e02677c4a64e847f5` |
| `source/search/exact/cur/data/n-302.minpoly.json.gz` | upstream | `9dff4f51ee61281c756ac50570d959f5a42706e7` | `8da6f8b0fd660fe46e7c9487b24ccc4e8a64253e0c0bdb46e3d42c238ff2c049` |

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-exact-cur-2026-10-16 --check
uv run --frozen --all-extras --group dev python -m devtools.algebraic_witness_reports evand-exact-cur-2026-10-16 derive-forms --check
uv run --frozen --all-extras --group dev python -m devtools.algebraic_witness_reports evand-exact-cur-2026-10-16 check
```

`check --replay` decides the 18 jobs again, about 11 CPU minutes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
