# Evan Daniel’s Exact-Data Release: s(29) and Grade C

Evan Daniel published the data behind two exact reports of
[evand/square-packing](https://github.com/evand/square-packing) as the release
[`exact-data-2026-10-12`](https://github.com/evand/square-packing/releases/tag/exact-data-2026-10-12),
in answer to the request of
[issue #545](https://github.com/jlevy/squares/issues/545#issuecomment-6126076974).
Neither report is a bound.
The release is tagged at `31523f87316bdfda00f5459dd9077928e264f133` (committed
2026-10-12T13:59:32Z) and was published at 2026-10-12T14:14:15Z. It is not marked
immutable, so its assets are pinned here by digest. The assets were downloaded at
2026-10-12T14:41Z.
The reports themselves, and the scripts that produced them, are retained at `ad86d42` by
the [evand-exact-and-local-reports-2026-10-12](../evand-exact-and-local-reports-2026-10-12/README.md)
packet; nothing under `search/exact/` or `tasks/` changed between that pin and the tag.

| Asset | Bytes | SHA-256 | Here |
| --- | --- | --- | --- |
| `s29-minpoly.tar.zst` | 87,237,962 | `708e1b8b45894667f90a0d18b55bb35ed6079b84d33f9656976fd5cfa6f3729c` | pinned by digest; three small files retained |
| `gradec-233.tar.zst` | 238,231 | `c71633f3850eb8b06c40ba04f824e9b6262b27b7996f62f69c6ad014a4ea9fa3` | retained as published |
| `SHA256SUMS` | 171 | `cd98b11150843e1a38b1f1afb943b17c2464c9df0d4088bfcb9dd96dab860e03` | retained |

Both archive digests match the release’s `SHA256SUMS`, the digests GitHub reports, and
the digests the issue comment prints.
[acquisition/release.json](acquisition/release.json) records the release, each asset,
and every member of the s(29) archive with its size and digest.

## The s(29) Archive

The archive holds 21 files, 201,735,244 bytes unpacked: the polynomial $p$
(`n29_poly_q4.json`), the shape-lemma parametrization of the five class angles
(`n29_param_t1.json` to `n29_param_t5.json`), the exported system (`n29_system.jl`), the
Krawczyk box (`n29_krawczyk.json`), the side to about 40,000 digits (`n29_S0.txt`), the
four roots the homotopy missed (`n29_q4_ref133k.txt`), and the original logs.
Every member was read here as a stream and matches the archive’s own `SHA256SUMS`; none
was unpacked to disk but the three retained.
Retained under [acquisition/release/s29/](acquisition/release/s29/): the archive’s
README, with the five replay commands, its `SHA256SUMS`, and `n29_krawczyk.json`.

Read from `n29_poly_q4.json` here: 7,214 integer coefficients, so degree 7,213; a
positive leading coefficient of 325 digits; a height of 5,074 digits; a constant term of
4,566 digits. The file’s own metadata reports 165 real roots and irreducibility by degree
patterns, with no possible factor degree.
The Krawczyk box gives the zero $t^\ast$ to radius $10^{-50}$ and the side
$S = 5.933833462676929189689460616352019138433834181077886974638\ldots$ with radius
$1.07 \times 10^{-48}$, the value the case record compares with its verified rational
ceiling.

**Not run.** The replay costs about 2.5 CPU-hours by the author’s measure, almost all in
`verify_mod.py`, and needs `PREC=220000` for `link.py`; its two identity steps are Monte
Carlo, and the packing’s non-overlap at the exact point is checked by none of it.
Irreducibility, the enclosure, the link and the identities were not checked here.

## The Grade-C Archive

The archive holds 723 files, 15,787,809 bytes unpacked: `n-N.contacts.json` and
`n-N.gradec.json` for the 233 configurations `gradec.py` reports VALID, the run logs of
all 250, three `GRADEC_DROPZERO=1` logs (10, 230 and 261) and the two status files.
Each file is a single-line JSON or a short log, so the packet keeps the archive itself,
[acquisition/release/gradec-233.tar.zst](acquisition/release/gradec-233.tar.zst), bound to
the digest the release states, and not its 15.8 MB of contents.
Python 3.14’s standard library reads it (`tarfile`, mode `r:zst`).
Unpacked in scratch space, all 722 files its `SHA256SUMS` lists match.
Its README and the two status files are also kept unpacked, under
[acquisition/release/gradec/](acquisition/release/gradec/).

**Recomputed at n = 10.** The source’s `gradec.py`, read first and run from a copy
outside the repository under the package versions `env.sh` pins, rebuilt the n = 10
certificate from the committed exact form, `search/exact/minpoly/data/n-10.minpoly.json.gz`
(retained here as its upstream gzip), and the archive’s `n-10.contacts.json`.
The output is byte-identical to the archive’s `n-10.gradec.json`, SHA-256
`ffc0c1ee41b0c2037ab241806215b0df9d2a0111893256fa2a2116e3df02208f`: VALID, 36 rows, a
2-dimensional flat family, least multiplier 1/16.
It took 9.2 seconds of wall time and 2.5 CPU seconds.
[receipts/gradec-n10-recompute.json](receipts/gradec-n10-recompute.json) records the
program, the inputs, the environment and the output.
This is the author’s own checker on the author’s data: it shows the published certificate
is what `gradec.py` computes from the published inputs, not that Theorem C or
`gradec.py` is sound.

**The price of the rest.** The logs print each VALID run’s build time. They sum to
38,026 seconds, about 10.6 CPU-hours: 154 runs took under a minute (1,249 seconds in
all), 212 under ten minutes (3.9 hours), and the longest, 313, took 1,741 seconds.
Those are the author’s times with eight jobs in parallel, so a re-run here may be slower.
The 17 timeouts would not finish under `gradec.py` as written.
Ten stop after the multipliers, in the reduced-Hessian step, with $\dim W$ from 12 to
16, while every run that finished has $\dim W \le 11$; `gradec.py` sums each leading
minor over all $k!$ permutations.
The other seven, 274, 275 and 308 to 312, stop before the null vectors, with flat
families of dimension 210 to 274.

## Original Gzip Files

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `source/search/exact/minpoly/data/n-10.minpoly.json.gz` | upstream | `1b8b87ba186f28adf4e8a1a0e335bd527ca64c43` | `efe6d26daf56f866a3d8b7bfc245a94074e4786b8c3e5150b18738ca349be438` |

## Retained Here

`devtools.acquire_source` wrote the tree part of the packet from a sparse checkout at the
tag commit, from the declaration in
[acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
10 files, 79,342 bytes.
Retained: `LICENSE`, `CREDITS.md` and `search/exact/minpoly/data/n-10.minpoly.json.gz`.
Pinned by digest against the identical copies the `ad86d42` packet retains:
`gradec.py`, `localmin.py`, `verify_exact.py`, `geom.py`, `env.sh`,
`search/exact/homotopy/N29.md` and `tasks/exact-minpoly/grade-C.md`.
The release assets are not in the Git tree; `acquisition/release.json` binds them.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`, which says the repository’s work was produced by Claude (Anthropic) under
human direction. The archives carry no licence file of their own; their READMEs name the
repository.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-exact-data-2026-10-12 --check
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
