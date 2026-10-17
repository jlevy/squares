# PingYou Ltd: The N29 Certificate of PR 622

[Pull request #622](https://github.com/jlevy/squares/pull/622) (BuddenPing, opened
2026-10-15T18:43:54Z), titled “data: submit a tighter exact N29 packing certificate”, is
read here as an intake report, as #574 was.
It was not merged, approved or pushed to.
Its head is
[`31155575ce1e6b461f77bfc9f3e201adf101115b`](https://github.com/BuddenPing/squares/tree/31155575ce1e6b461f77bfc9f3e201adf101115b)
of the fork BuddenPing/squares, branch `pingyou/n29-certificate-20261015` (tree
`0828044cbd2830dde5d8d717de3a890cf027b103`, committed 2026-10-15T18:43:33Z), three
commits over the base `73d254272da7168f6d4c2e341c009849b5e63b46`, the merge of #621.
It was fetched by commit id from this repository’s `pull/622/head` ref and read at
2026-10-16T20:28Z. The acknowledgement of 16 October 01:38Z pinned the same head and
asset, and the author answered its question on AI assistance at 03:40Z.

The pull request adds four small files: one HostedData manifest and one submission packet.
The geometry is not in Git: the manifest pins one release asset of
[BuddenPing/square-packing-certificates](https://github.com/BuddenPing/square-packing-certificates)
by size and SHA-256, and the certificate is a member of that zip archive.
This packet pins all of it and keeps one derived exact fact.

## What the Pull Request Claims

One complete rational certificate at n = 29, `n29-certificate/certificates/n029.cert.json`
(SHA-256 `a01428c51875679fbe78c11a803742b8d99f44b916a660ab6801bb0fcf76951b`): 29 squares
at rational centres and half-angle tangents in a square whose exact side is a fraction of
2,399 and 2,398 digits, about `5.93383346267692918968946061635201913843383418107788697463883`.
The claim record gives that side as `side_exact` and replaces with it the N29 certificate
of the author’s PR #574 (SHA-256 `0769d793…`).

The submission classifies it as a certificate refinement of the known construction of
Thomas Schadt, improved by David Ellsworth: an 800-digit realization of Evan Daniel’s
five-parameter contact decoder, followed by an exact common-centre scaling and a
bounding-square crop. It claims no new construction, no smaller nominal value and no
optimality. It states three margins, computed from full rational sides: 7.32e-90 below
its PR #574 certificate, 1.57e-36 below this project’s exact N29 bound (T-155, the
regularized view of #549) and 5.93e-20 below Evan Daniel’s batch certificate.
Its own checks are author reports: standard-library exact separating-axis and
polygon-clipping routines accepting all 29 squares and 406 pairs of the certificate and
its three comparators and refusing duplicate-square and outside-container controls, a
lossless conversion to a corners Witness/v2, and this repository’s two exact verifiers,
unchanged at `73d2542`, accepting that witness.

## Source Custody

The pull request adds its files under `packing/resources/`, which the repository’s
`LICENSE` names as third-party material outside its grants, and they state no licence of
their own. The release asset carries `licenses/PingYou-MIT.txt`, which its `NOTICE.txt`
says covers PingYou Ltd’s new code and documentation only, not the construction, the
imported data or the notices. Under the derived-only form of the
[existing retention policy](../known-best-packings/README.md), as for PR #574, this packet
keeps no upstream byte, and no redistribution permission or licence determination is
asserted.

`devtools.acquire_source` wrote the acquisition record from a sparse checkout at the pin;
each file is bound to its Git blob there.
[acquisition/declaration.json](acquisition/declaration.json) is the declaration,
[acquisition/sources.json](acquisition/sources.json) the record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `packing/hosted/pingyou-n29-certificate-2026-10-15.yaml` | `a8d698b124c28b24a021bf8e41d49dc2dbca0fd7` | 569 | `78dbc541f2dea49d7e54c2c1015e7ebc77e42db3dcba6835611acacb74745129` |
| `packing/resources/web/pingyou-n29-certificate-2026-10-15/README.md` | `f56529c8f6ecfe38cf7015f9fb9fd3b02da8c5f0` | 3196 | `fe69d96c1ee535e1fd5bec722a5ab0bcf1cb4c90447a352c6a95255ad5945ee5` |
| `packing/resources/web/pingyou-n29-certificate-2026-10-15/claims.json` | `db62f8a513246b0441a67c87a4f42f61a96b7020` | 6856 | `e36ab2b5af9bb24760222848cd880256e0cafebe58967e338ddfa1de51a05b19` |
| `packing/resources/web/pingyou-n29-certificate-2026-10-15/comparison.json` | `8b4f3189dc4f505c81ec4e131ba298551fa5cf27` | 25098 | `ea92f1f4dd488ddf67b5a3e7fe6df34d34e92f2958da531a7eca379328c0cd3d` |

### The Release Asset

The tag `data/pingyou-n29-certificate-2026-10-15-v1` points at
`318ab94e821ba7280a68fa8ce2942c9ecdbda41d` (`git ls-remote`, 2026-10-16), the commit
that PR #574’s release tags name too.
The asset was downloaded from the release at 2026-10-16T20:28Z, and it has the size and
SHA-256 its manifest pins; the triage of 15 October (think-30n2) also read GitHub’s asset
digest, published 2026-10-15T18:35:51Z, as the same.

| Tag | Asset | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `data/pingyou-n29-certificate-2026-10-15-v1` | `pingyou-n29-certificate-2026-10-15.zip` | 430075 | `0dc9bcd1cf5f2806a4d2e0c4c1c07e4903d91bbea611b8b938bda770b9782537` |

The archive has 34 members, read with `zipfile` and none extracted or run; its own
`SHA256SUMS` agrees with all 33 files it lists. The certificate member has the digest the
claim record prints, and the native witness `n29-certificate/native/pingyou-20261015-n29-rational.yaml`
(SHA-256 `0eff5b4d2a9701e30fe8912fd634c5a7124384366197533c18a5bcc26dfe4a39`) the digest
the claim record prints for it.

## What Is Retained

The certificate enters a decision only through a derived fact, written by `derive` from
a checkout at the pin and the asset: the manifest is read from the checkout, the asset
must have its size and digest, and the member must have the digest the declaration states.

- **One rational fact**, `facts/n-029.yaml.gz`, the certificate as an exact rational
  centre-basis Witness/v2, declared in [acquisition/report.json](acquisition/report.json)
  for `devtools.upper_bound_reports`. It is admitted at the exact fraction the claim
  record prints, and it is equal, pose for pose, to the source’s corners Witness/v2 in
  the same asset.
- The frozen comparison, [acquisition/claims.json](acquisition/claims.json), and the
  replay receipt, `receipts/exact-certification.json.xz`.

The declaration names the house at 29 by T-155’s exact side and states the exact form
n-029.md gives its verified lane, since that record prints the lane at the decimal it
printed before, `5.93383346267692918974379895098`, 5.43e-20 above the exact form
(`register_regularized_bounds.printed_value`; think-gzrw). The importer holds the house’s
side to that exact form rather than to the print.

## Against the Record

Read against `main` at `321d492c77c37e9adddcecec4e58336bc8270466`.

- **T-155**, the verified lane, `296691673133846459484473030817600957/5e34`: the
  certificate is below it by 1.56616581892211e-36.
- **PR #574’s N29 certificate**, a v2 row that T-174 does not register: its exact side,
  as the 14 October ledger transcribed it from that pull request’s `claims.json`, is
  above this one by 7.32482673606514e-90. The frozen comparison holds that report at its
  40-place print, rounded up, which does not separate the two.
- **The reported lane**, the Kingbird catalogue’s `5.93383346267692` for the packing of
  Thomas Schadt, improved by David Ellsworth: the certificate is 9.19e-15 above the
  print and within one unit of its last place, so the print does not order them. The
  lane’s exact side is the root of Evan Daniel’s degree-7213 polynomial (#545), which the
  record does not hold (think-6gti). The certificate realizes the same packing, so it is
  expected just above that root.

So the frozen comparison names no smallest report. How the report-order rule reads this,
and the owner’s decision it leaves, are in the per-count ledger of this pass,
[`upper-bounds-n29-20261016`](../../../campaign/issue-intake/upper-bounds-n29-20261016/README.md).

## The Replay

`devtools.upper_bound_reports` decided the fact through the two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over Q. A
positive job, a duplicate-square control and an outside-container control ran in their
own child processes, two at a time, on 2026-10-16 from 20:39:26Z to 20:40:32Z, on a shared
four-core host. The three jobs made 2,436 pair decisions in 93.53 route CPU seconds and
96.21 job wall seconds, the longest 32.77 seconds; the whole command took 96 CPU seconds.

The positive passes both routes, and both routes refuse both controls: squares 0 and 1
overlap, and square 0 lies outside the box. The certificate is an exact contact solution:
a square touches the box, a least wall clearance of exactly 0, and two squares touch, a
least pair gap of exactly 0, on both routes.
`check --replay` decided the three jobs again, one at a time, in 1 minute 47 seconds
(105 CPU seconds), and every row was equal to the retained one.

## What Is Not Established

- The source’s checkers (`VERIFY.py`, `exact_sat.py`, `exact_polygon.py`,
  `build_comparison.py` and the native converter) were not run; the routes above decide
  the certificate from its own poses. The construction’s derivation from Evan Daniel’s
  decoder and the submission’s comparison receipts were not checked.
- The two routes share certificate parsing, half-angle conversion, Fraction arithmetic
  and the separating-axis method, and the source reports running both itself.
  The stage 4 review of 16 October
  ([review-2026-10-16-pingyou-n29.md](../../../../docs/project/reviews/review-2026-10-16-pingyou-n29.md))
  decided the certificate again with a clean-room checker and ran the third exact route,
  each with sharp controls; its programs and outputs are in [review/](review/README.md).
  It accepted the certificate for finite feasibility, with no blocking defect.
- The comparison with the reported lane’s exact side is not made here.
  A finite certificate establishes an upper bound only.

## Credit

The submission asks that PingYou Ltd be credited with the certificate refinement, that
Thomas Schadt and David Ellsworth keep the construction, and that Evan Daniel be credited
for the source tools and data and this project for the regularized comparator.
The pull request makes no statement about AI assistance. Asked in the acknowledgement,
the author answered on 16 October 2026: “All of our submissions are the same affiliation.
PingYou Ltd, assisted by the PY agentic offering”
([comment](https://github.com/jlevy/squares/pull/622#issuecomment-6207551818)).

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source pingyou-pr622-certificate-2026-10-15 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-pr622-certificate-2026-10-15 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-pr622-certificate-2026-10-15 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-pr622-certificate-2026-10-15 derive --checkout CHECKOUT --assets ASSETS --check
```

`--check`, `check-claims` and `check` run offline from the fact. `derive --check` needs a
checkout at the pin and a directory holding the asset by name, and refuses a checkout
that does not yield this packet’s record and an asset that is not the one its manifest
pins.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-029.yaml.gz` | receipt | `8e2eaa5bd4328159a67b9b9a41522c3658f82986` | `46668379171a13489bc9ed809e1f9d4e9528827fa484e5c44a34a7355ce62642` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
