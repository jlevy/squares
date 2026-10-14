# Daniil Ostashev’s Composition Packings at a8db6ff

[Issue #528](https://github.com/jlevy/squares/issues/528) reports new packings of 175,
232 and 264 unit squares from
[dostashev/square-packing](https://github.com/dostashev/square-packing/tree/a8db6ff941fc93d1d68d4d7aed90bb2a18a3a41f),
at the commit it names. This packet pins that commit, the repository’s `main` head when
read, `a8db6ff941fc93d1d68d4d7aed90bb2a18a3a41f` (tree
`7badc73ba04ca00588f52888b413d8595dbcfc5f`, committed 2026-10-12T03:05:21Z), retrieved
at 2026-10-12T08:03Z. The six SHA-256 values the issue gives are those of the files at
the pin.

| n | The issue prints (38 places, rounded up) | The README prints (15 places) |
| --- | --- | --- |
| 175 | 13.76417431748659662942782322004234282577 | 13.764174317486597 |
| 232 | 15.76417431748659662944782322004234282577 | 15.764174317486597 |
| 264 | 16.77473513238783284261026458732177098083 | 16.774735132387833 |

Each certificate, `records/n0NNN.sqcert`, gives a rational side and, for every unit
square, a rational centre in $[0, S]^2$ and a rational $t = \tan(\theta/2)$. Each exact
side rounds up to the issue’s print at 38 places, and is admitted at it.

## Which Revision

Against `c3d17ab`, the commit the issue-501 packet
([dostashev-records-2026-10-11](../dostashev-records-2026-10-11/README.md)) pins,
`a8db6ff` adds the six files of these three counts and changes the README, and changes
nothing else. The issue also restates #501’s three sides at this commit; those
certificates are byte-identical to the ones the issue-501 packet retains, whose exact
sides T-149 states, so they are not read again here.

## Retained Here

The repository is MIT-licensed (`LICENSE`, Copyright (c) 2026 Daniil Ostashev, added in
`c6893aa`), and its README says the licence covers the verification code and the record
packings and certificates. `devtools.acquire_source` wrote the packet from a checkout at
the pin, from the declaration in
[acquisition/declaration.json](acquisition/declaration.json). It retains under `source/`
the eight files the commit adds or changes and the licence, byte-identical, 456,760
bytes, and pins the other 36 files of the tree but `.gitignore` by digest, each compared
with the identical copy the issue-501 packet retains.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.

| Upstream path | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- |
| `records/n0175.sqcert` | 89011 | `a84adbcf843c32a02e5e571c1f345559547ff43e7369df34ba4ae32cb50d97b2` | The n = 175 certificate |
| `records/n0232.sqcert` | 111168 | `fa276f8c54510872cf41a94a7289839e4dd43261e3c3f30f5f7b0c2e9a5500f9` | The n = 232 certificate |
| `records/n0264.sqcert` | 136278 | `aa0fa6cba29b40912f8ca1a770a059de2fddfc0b6a6cf6e948443c4dd0ee980d` | The n = 264 certificate |
| `records/n0175.sqpk` | 29111 | `102ebbc6f30c20e314e8c15713a118da58aaa273b6cadd15dd8849558598dcc8` | The 60-digit decimal packings the certificates were built from |
| `records/n0232.sqpk` | 37924 | `cbabcefb341fb061a867599de9561c06ab6f405d3db045ba36e3e58e2442b381` | |
| `records/n0264.sqpk` | 45388 | `26aabf639ded34d83e4a446e1e7e3b02eafd453ff95d1d8c37d8fc2730de1b28` | |
| `README.md`, `LICENSE` | | in the manifest | Author prose and the licence |
| `verify/`, `tools/`, `verify_all.sh`, the #501 records | | pinned, identical to the issue-501 packet’s | The author’s C++ GMP checker, mpmath cross-check and driver, not run |

## The Format

The certificates are in the author’s `.sqcert` format, read by the `sqcert` adapter of
`devtools.upper_bound_reports` that the #501 import added; the
[issue-501 packet](../dostashev-records-2026-10-11/README.md#the-format) describes it.
As there, each certificate’s centres and side are the 60-digit optimum multiplied by
$1 + 10^{-60}$, and a test holds each retained side to its `claimed_s` header times
$1 + 10^{-60}$.

## Exact Replay

Only the retained certificates enter geometry decisions, through the maintained two-route
kernel of `devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and
the independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$ after an exact half-angle conversion. Each count ran a positive job, a
duplicate-square control and an outside-container control, each in its own child
process, on one worker.

All three positives pass both routes, and both routes refuse all six controls. In every
positive the two routes find the same least wall clearance and the same least pair gap,
$5.000000 \times 10^{-21}$ to seven digits, from the $1 + 10^{-20}$ scaling of the
load-bearing squares that the issue describes, far above the $10^{-60}$ dilation. The
nine jobs made 460,422 pair decisions in 647.47 route CPU seconds and 1,544.83 job wall
seconds, summed; the longest, the 264 positive, took 291.46 seconds. The one-worker run
took 26 minutes 15 seconds of wall time with the machine at a load of 15 to 17. A fresh
serial `check --replay` decided all nine jobs again, equal to the retained rows apart
from timing, in 28 minutes 38 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code. The third exact route
(`devtools.check_half_angle_area`), which imports neither route’s parsing or deciding
code, decided all three certificates again with six controls each in the stage 4
[review of 12 October](../../../../docs/project/reviews/review-2026-10-12-upper-bound-imports-528-529.md),
agreed with both routes at every number they share, and held each retained file to its
upstream bytes; its credit measurements are below.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each certificate against the
record at layer 4’s head `dead83f0e` (12 October 2026), which carries `main` at
`ad00d7f84` and the open import and adoption layers; `check-claims` rebuilds it, each
case ceiling and each other report from its holder’s own packet.

| n | Case ceiling on layer 4, holder | Below it by | Other reports | Smallest |
| --- | --- | --- | --- | --- |
| 175 | 13.7671207246923133, Francisco Couzo’s refinement of ry-xu’s packing (T-140) | $2.95 \times 10^{-3}$ | Couzo’s certificate at `337078c`, not registered (think-9fjl), above by $2.94 \times 10^{-3}$; ry-xu’s (T-125), the house on `main`, above by $4.72 \times 10^{-3}$ | this certificate |
| 232 | 15.7674283499418417, SQUISH (Nate Chaoweeraprasit, T-136) | $3.25 \times 10^{-3}$ | none | this certificate |
| 264 | 16.77817459305202, the catalogue’s $9 + \tfrac{11}{2}\sqrt2$, which the issue calls Göbel’s pattern, verified by Evan Daniel’s exact ceiling (T-101) | $3.44 \times 10^{-3}$ | none | this certificate |

At 175 the reports T-130, T-138 and #476 are above T-140. On `main`, where the adoption
layer has not merged, 175’s house is T-125 and 232’s is the catalogue’s
$8 + \tfrac{11}{2}\sqrt2$ with T-136 pending; each certificate is below those too. The
previous bests the issue names are these, and its improvements agree with the distances
above.

## Against the Packings They Are Built From

Measured for the credit with the third exact route’s own `arrangement_gap` and
`patch_lineage` (`devtools.check_half_angle_area`, called from a scratch driver and not
changed), with each certificate read through this packet’s custody and each parent
through the reader the route keeps for it:

- **None of the three is a placement of the packing the record holds at its count.** No
  symmetry of the box matches the 175 square for square with T-140, Couzo’s `337078c`
  certificate or T-125, the 232 with T-136, or the 264 with Evan Daniel’s exact
  certificate of the catalogue’s packing (T-101). They are new arrangements, as the issue
  says.
- **The pieces the issue names reappear where the record retains them.** In the 175, 66
  of the 171 squares of Evan Daniel’s exact certificate of David Ellsworth’s s(171)
  (T-101) land within $10^{-9}$ of a square under a half turn of that box, none turned;
  of Thomas Schadt’s s(50), whose piece the new block replaces, only 11 do. In the 264,
  88 of the 126 squares of Evan Daniel’s exact optimum of Joost de Winter’s s(126)
  (T-098) land within $10^{-9}$ under a half turn, none turned. Friedman’s s(85) has no
  exact certificate in the record, so the 232’s piece was not measured.
- **The three share the new block.** The whole 175 placed in the 232 moved by $(0, 2)$
  puts 122 of its squares within $10^{-9}$ of a square of the 232, 46 of them exactly,
  and 64 of them land in the 264 under a reflection; the squares were not sorted into
  block and aligned squares, so this is consistent with the shared 38-square rectangle
  the issue describes and does not identify it.

These are measurements for the credit and decide nothing.

## What Is Not Established

The issue states that each side is the exact first-order optimum of its packing’s contact
topology, with nonnegative KKT multipliers at a 60-digit solution and the load-bearing
squares scaled by $1 + 10^{-20}$. That is the author’s report of local optimality, not a
bound, and nothing here checks it. Neither the author’s C++ checker nor the mpmath
cross-check ran here. The certificates establish finite upper bounds only.

## Credit

The issue credits Daniil Ostashev with the three packings, and asks that the pieces’
sources be acknowledged as the record sees fit. Each is a composition, built from a
library of the best known packings of unit squares in $(h + d) \times h$ rectangles: two
library pieces in opposite corners of the box and aligned squares around them. All three
use a new packing of 38 unit squares in an $(h + 2) \times h$ rectangle,
$h = 5.76417431748659662929\ldots$, which the author found by a GPU soft-to-rigid search
after Yohei Nakajima’s idea. At 175 it replaces the pieces of David Ellsworth’s s(171)
template, cut from Thomas Schadt’s s(50); at 232 it sits beside a 76-square piece of
Erich Friedman’s s(85); at 264 beside a 93-square piece of Evan Daniel’s exact optimum of
Joost de Winter’s s(126). The issue states AI assistance: the author set up an
AI-assisted research loop and drove it with his own ideas, the rectangle library and the
composition being his, and AI agents wrote and ran the search, composition and
verification code.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source dostashev-records-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports dostashev-records-2026-10-12 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports dostashev-records-2026-10-12 check --replay
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
