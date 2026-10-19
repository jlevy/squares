# Evan Daniel’s n229 Dilation Bound: Author Update

This packet retains one chronological version of the upper-bound claim in
[issue #674](https://github.com/jlevy/squares/issues/674). It is source custody only.
No source verifier, source control or stage 4 review was executed during acquisition.

## Source, Licence and Dates

| Field | Value |
| --- | --- |
| Source | [evand/square-packing](https://github.com/evand/square-packing) |
| Pin | `00e68dfbe1d29ab5dbab1cddfb8f6ca19d5470db` |
| Source publication | 2026-10-18T01:35:40Z; author and committer dates agree, and this commit adds the named certificate and input |
| Report publication | 2026-10-18T01:36:21Z |
| Licence | MIT, copyright 2026 Evan Daniel; [LICENSE](source/LICENSE) retained |
| Retrieval | Exact UTC time in [acquisition record](acquisition/sources.json) |
| Custody | [Declaration](acquisition/declaration.json), [manifest](acquisition/upstream-subtree.sha256), [inspection receipt](acquisition/custody-review.json) |

## Claim and Chronology

The single reported claim is
`s(229) <= 7825080756947776580756939951343/500000000000000000000000000000`, reported as
the upward-rounded bound `15.650161513896`.

The [author update](https://github.com/jlevy/squares/issues/674#issuecomment-6244298663)
asks to register this smaller side in place of the opening `15.650163254859`. The
[opening packet](../evand-n229-dilation-2026-10-17/README.md) preserves the earlier
report at `e0338c7`. The source calls the update a nearby configuration with the same
tilted structure. Its introductory words say “lower bound,” but the table, certificate
and surrounding claim are an improved upper bound; no lower-bound claim is recorded
here.

| File | Role | SHA-256 |
| --- | --- | --- |
| [s229_v2.cert](source/search/packer/candidates/s229_v2.cert) | Exact rational certificate | `1a35a7806b6cc01b232d5c634efdbe789c7df979cec6ab28d6ab283ac2b47e23` |
| [s229_v2.input.txt](source/search/packer/candidates/s229_v2.input.txt) | Source binary64 packing | `7b2bf80771e8d96f11931e5080f18c0d623b3d4373b9693e4d338acbf4ffcf53` |

Both versions are dilation certificates for upper bounds only.
Neither the issue nor this acquisition establishes optimality or local minimality.
Comparison with the current register and other intake reports is separate work.

## Credit and AI Disclosure

The issue names Evan Daniel and asks for Francisco Couzo’s #672 packing to be credited
as the start, following Joost de Winter’s #668. It describes the same tilted structure
as #672, with upright squares rearranged; the update continues that lineage.
The issue’s stated comparison is against Couzo’s `15.650174740273`, after de Winter’s
`15.650174756949`, rather than against the older register alone.
Those are the author’s historical comparison statements, not a fresh standing check.

The retained [CREDITS.md](source/CREDITS.md) discloses Claude (Anthropic) working under
human direction and states no peer review.
The pinned certificate commit names Claude Opus 5.5 as co-author.
Both exact checkers share authorship and certificate format; algorithmic differences do
not establish outside independent authorship.

## Checker Dependencies and Source Assertions

The retained `search/exact/verify_cert.py` and `verify_cert2.py` each read the named
certificate directly and import only `sys` and `fractions.Fraction`. The first uses
separating axes; the second tests exact polygon containment and edge intersection.
Both use a circumscribed-disc shortcut.
No other repository, compiled engine, network data or numerical solver is required by
these standalone exact-replay entry points.

The source reports both accept this certificate and gives pair separation about
`1.2e-12` and wall clearance about `6.0e-13`. These are author-reported outcomes, not
acquisition measurements.
No per-claim corrupted-input or analytic control receipt accompanies the two claim
files. This packet claims no new controls or acceptance verdicts.

The retained `search/packer/dilate_cert.py` documents the construction: scale centres
and the box by approximately `1 + 10^-12`, keep unit square size, round coordinates to
rationals and replace each angle with a rational half-angle tangent.
The script imports only standard-library `argparse`, `math`, `sys` and `fractions`; it
is a numerical producer, separate from exact-certificate acceptance.
It was read as source and never executed here.

## Retained and Omitted Material

`devtools.acquire_source` retained nine files, 84,052 bytes: the licence, credits, root
and exact-format READMEs, both standalone checkers, dilation producer and this version’s
certificate and binary64 input.
No retained data file crosses the repository’s 1,000-line compression threshold.

The opening `s229.cert` and `s229.input.txt` are additionally pinned by digest, 46,546
bytes in two files. Acquisition checks that their bytes equal the copies retained in
[the opening packet](../evand-n229-dilation-2026-10-17/README.md); the updated pin
leaves those files unchanged.

Other certificates, numerical search tools and their dependency closures, run histories,
site assets, figures and bulk source data are omitted and pinned by the source commit
only. The opening and updated pins also differ in unrelated site files; this packet does
not retain or review those changes.
It does not reproduce numerical search or independently certify the dilation argument.

## Custody Check

From `packing/`, with the project interpreter and external scratch configured:

```bash
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  evand-n229-dilation-update-2026-10-18 --check
```

The [inspection receipt](acquisition/custody-review.json) records the command and
outcome. The check establishes declaration, manifest and retained-byte consistency.
Geometric replay, dedicated review, registration and any house adoption remain separate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
