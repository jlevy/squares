# Square-packing literature refresh, 2026-09-05

This directory is the frozen discovery packet for the post-3.81 strategy review. It
retains the actual arXiv, Crossref, OpenAlex, and Zenodo responses used in the pass so a
later agent can inspect the same corpus without first repeating the searches. It is a
bounded query receipt, not a claim that every publication surface was exhausted.

## Search receipts

The three arXiv Atom feeds were fetched at 2026-09-05 20:47 UTC with these queries:

```text
all:"unit squares" AND all:packing
ti:"square packing"
all:"congruent squares" AND all:packing
```

Each feed records its query URL, retrieval timestamp, result count, entry version, and
revision timestamp. The OpenAlex response covers works dated 2025-01-01 through
2026-09-05 whose full text matched `packing unit squares square`; the Crossref response
is the first 100 results of the title/topic search used as a DOI backstop. The raw
responses are intentionally retained despite their false positives.

| Receipt | SHA-256 |
| --- | --- |
| `arxiv-query-unit-squares.xml` | `bc0ba4305d85ecd704688d48b86b41d1f070f2fa1fa319ebc807e0a50184073a` |
| `arxiv-query-square-packing.xml` | `d4798ce05eab7783fbf3c7ca9b33d9e327409825dd9280a3840039829e6af90d` |
| `arxiv-query-congruent-squares.xml` | `94f11d443bfba90b0d3c1de55db283bc4fdf6f390d4322e066dcce274d090227` |
| `crossref-query-square-packing.json` | `171ebfcc6e936642fad6091d3fb6954c02f702eac460d0cec36374603dce3cd7` |
| `openalex-query-square-packing.json` | `8efdb9e6d912cd4edda7d558962039fe7f26c5ceaea6f6da921184403709ab4e` |

## Additions and corrections

The refresh changed the useful corpus in five ways:

1. Aranya Kumar Bal’s `arXiv:2607.11318v2` gives an independent, hand-checkable
   64-rectangle counterexample to Wegner’s conjecture and a recursive standard
   clique-LP gap tending to `5/2`. It is archived as PDF plus faithful extraction. It is
   evidence about packing/piercing and configuration relaxations, not a theorem about
   congruent-square packings.
2. Sean Dewar’s `arXiv:2210.10422v2`, published in 2024, supplies primary contact-graph
   context for oriented squares. Its generic-width theorem concerns various-size
   squares; equal widths defeat that hypothesis. It does not justify a finite contact
   atlas or global rigidity for freely rotated congruent squares.
3. Four primary rigidity and jamming sources used by the 2026-09-03 prior-art review are
   now retained rather than left in an ephemeral scratch directory: Connelly–Whiteley
   1996, Donev–Torquato–Stillinger–Connelly 2004, Donev–Connelly–Stillinger–Torquato
   2007, and Connelly’s packing lecture notes. They are method analogues. Their theorems
   do not transfer automatically to hard squares with nonsmooth feature changes.
4. The Kingbird rigid-packing and analytic-minimization pages now have byte-preserved
   HTML captures and searchable Markdown. They record the catalogue author’s
   classifications and stationary-equation method, not completeness or optimality
   proofs.
5. Kim Brandwijk’s July 2026 exact result capsule fills a real `n = 17` chronology and
   certificate-architecture gap; the next section states its scope.

The pass also located Joost de Winter’s mutable August 2026 construction report. Its
conflicting live revisions, proposed `n = 68, 126, 206` sides, failed PDF acquisition,
and exact reopen condition are retained in
[`de-winter-improved-packings-2026`](../de-winter-improved-packings-2026/README.md).

## Brandwijk `s(17) > 89/20` capsule

Zenodo record [21422426](https://doi.org/10.5281/zenodo.21422426), published 2026-07-18
by Kim Brandwijk, contains an externally published computer-assisted proof capsule for
`s(17) > 89/20 = 4.45`. It supersedes the separately deposited record
[21422428](https://doi.org/10.5281/zenodo.21422428), which claimed
`s(17) > 8893/2000`. Both metadata responses are retained; only the latest tarball is
retained.

The capsule uses 16 exact rational unavoidable points and an exact interval
branch-and-bound replay over centre coordinates and `t = tan(theta/2)`. Its result is
historically and methodologically relevant, but it has since been numerically
superseded by Burns, Massaccesi, and the project’s retained `n = 17` certificates. It is
not evidence for the correctness of the project’s weighted shrink-and-angle-net
verifier.

| Artifact | Deposit checksum | Local checksum |
| --- | --- | --- |
| `s17-gt-89-20.tar.gz` | MD5 `d07d3396161568f5f9ffcc8cfa8f6c22` | SHA-256 `5541c60a16fb8a6dcae9e9a714fd24ece01f203fc289aeb3d3487710258933c2` |
| `brandwijk-s17-gt-89-20-CLAIM.md` | MD5 `98a9d2371dde209a755a2c60ed809f7b` | SHA-256 `27053d71a571e2419333e31baf9f328ca0d167d108d7858552f04dbd303528cc` |

The full tarball is retained because its 43,790,068-byte replay already accounts for
almost all of the 43,853,327-byte archive. Selective extraction would save almost
nothing while losing offline build dependencies, licenses, and provenance.

Local checks matched every artifact hash in `capsule.toml`; the vendored Rust checker
built offline, all 55 tests passed, both mutation witnesses were accepted as valid
counterexamples, and the replay’s fast checksum check returned
`VALID (fnv1a64 6120e60e07a28340)`. The full 60,393,653-node replay was started and then
stopped rather than spending roughly 30 minutes during this source pass. The capsule’s
own transcript reports a valid full replay in 1790.92 seconds; that remains
source-provided evidence, not a local replay result.

Preserve these trust-chain qualifications:

- FNV-1a64 is not cryptographic; integrity comes from the Zenodo deposit checksum and
  the locally recorded SHA-256.
- The tar has no signed manifest. Its internal manifest does not hash every checker,
  specification, vendor, and documentation file; the whole-tar hash is the outside
  binding for those bytes.
- The producer revision and claimed signed tag are not included, so discovery cannot
  be regenerated from this capsule. The packaged operation is proof replay.
- “Independent verifier” describes the author’s asserted development separation. The
  checker is standalone, offline, and source-visible, but this deposit cannot establish
  independent authorship.
- Mutation witnesses exercise a separate witness path; they do not by themselves test
  the main replay’s completeness logic.

## Screened nearby work

The broad queries returned several papers whose titles can be mistaken for this
project’s finite congruent-unit-square problem:

| Source | Actual problem | Disposition |
| --- | --- | --- |
| Haobo Yang, *Three Squares in a Rectangle*, `arXiv:2608.13595v2`, revised 2026-08-27 | Maximizes the sum of side lengths of three variable-size squares in a `1 × x` rectangle; also proves a five-square guillotine-cut result | PDF and raw extraction retained here as a screened source, not entered in the core paper table |
| Singh, `arXiv:2601.22163`; withdrawn predecessor `arXiv:2506.23284`; Baek et al., `arXiv:2411.07274` | Erdős’s variable-side sum objective | Query receipt only |
| Dósa–Lángi–Tuza, `arXiv:2601.16535v3` | Covering a square by congruent squares, with overlap permitted | Query receipt only |
| AlphaEvolve `squares_in_square` experiment | Variable-side sum objective | Do not cite as a congruent-unit-square baseline |

Yang’s retained PDF has SHA-256
`555c43c5b772eba02a488b74a7f8c9a9795cf1493cb41b985ecc1c3e52ccdea3`.

## Currentness decisions

Direct revision and byte checks found no newer archived version of the existing Bui
`2504.09489v1`, Bui `2508.04603v2`, McClenagan `2602.01484v1`, Caoduro–Sebő
`2206.02185v3`, Ajwani et al. `2606.17854v2`, Alvarado-Garduño–González
`2510.17707v1`, or Alpert et al. `2010.14480v2` papers. The four first-listed live PDFs
were byte-identical to the local copies. UnitSquare still exposes Release 1; no Release
2 was found. The retained Burns page is byte-identical to the live page. Massaccesi’s
article body is unchanged; only Blogger’s rotating widget/token metadata differs.
Kingbird’s main and comparison pages are byte-identical to their local captures.

The historical `n17-lower-bounds-2026/README.md` remains byte-identical at SHA-256
`b48c0c31cf62366d44cd12f02cf321dd38b5a23391caec95f04445938e0b3d75`. The resumable
n=17 certificate machinery uses that file as a frozen source input. Current adoption
and supersession status therefore lives in the archive index and this refresh packet;
do not reword the historical README without versioning the dependent checkpoint.

Arslanov–Bui 2025 remains paywalled. Crossref fixes its online publication date at
2025-08-03; the source-availability record now carries the new check date. Plakhta 2021
also remains unretrieved: the tempting institutional PDF is the preceding Bonnot et al.
article plus an issue contents page, not Plakhta’s paper.

## September Acquisition Manifest

The six additions below are the retained acquisition artifacts. Paths are repository
relative. Each raw extraction is byte-identical to `pdftotext -layout` on its retained
PDF; no PDF or raw source was modified while preparing this manifest.

| Source | Local PDF | PDF SHA-256 | Local raw extraction | Raw SHA-256 | Primary acquisition URL | Retrieval timestamp | Extraction method |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Bal 2026 | `packing/resources/papers/bal-2026-64-rectangle-wegner-lp-gaps.pdf` | `4a375f1086fb84536c467966b3ef1de37c85fb3c76618ffc8c4a5543c37c9cf0` | `packing/resources/papers/bal-2026-64-rectangle-wegner-lp-gaps.raw.md` | `d13323a8106bd0116053fd22ed0dbe0b869a3ac661e94df880ba25e189c273cb` | <https://arxiv.org/abs/2607.11318v2> (embedded PDF identifier) | Not recoverable; first retained in commit `5214b57b` on 2026-09-05, which is not an acquisition timestamp | `pdftotext -layout` |
| Dewar 2024 | `packing/resources/papers/dewar-2024-contacts-oriented-squares.pdf` | `1de373c8e229ce98ab5294953acbc345ed8589b782e6141f6fcb309be9e1059e` | `packing/resources/papers/dewar-2024-contacts-oriented-squares.raw.md` | `3665eac0ba926d080fd03b8e8339fd13a1b4ec4352d5f5b6b726da4f0333941e` | <http://arxiv.org/abs/2210.10422v2> (embedded PDF identifier) | Not recoverable; first retained in commit `5214b57b` on 2026-09-05, which is not an acquisition timestamp | `pdftotext -layout` |
| Connelly–Whiteley 1996 | `packing/resources/papers/connelly-whiteley-1996-second-order-rigidity.pdf` | `ba6a1ef37a9c423eb19bc5c609f957c9e85d4326d714da377873ad1b3307e8b2` | `packing/resources/papers/connelly-whiteley-1996-second-order-rigidity.raw.md` | `009be244216a1706376f18fb10f92ea4df9be8c14d7a85cd778555f3db254afa` | <https://pi.math.cornell.edu/~connelly/pdf/10.1137_S0895480192229236.pdf> | 2026-09-03 (time not retained) | `pdftotext -layout` |
| Donev et al. 2004 | `packing/resources/papers/donev-torquato-stillinger-connelly-2004-jamming-lp.pdf` | `bed4073f28564aa7689fa5adaf079362839a32cc9d08c739f2ec5e6788cd08ed` | `packing/resources/papers/donev-torquato-stillinger-connelly-2004-jamming-lp.raw.md` | `31cdaaeb245fc3a1b5ebbc716ab41d108e949a4205d66fcca5f50276d96180fd` | Not recoverable from the retained evidence | Not recoverable; first retained in commit `5214b57b` on 2026-09-05, which is not an acquisition timestamp | `pdftotext -layout` |
| Donev et al. 2007 | `packing/resources/papers/donev-connelly-stillinger-torquato-2007-underconstrained-jammed-packings.pdf` | `b45a31dc7172fff8bd8075ba36e0efa10e494354f1e2dea6bca330bb0d669d06` | `packing/resources/papers/donev-connelly-stillinger-torquato-2007-underconstrained-jammed-packings.raw.md` | `f97e82e83cc17841b84eee6bdbd8198e12aec3b50e138ac80b4940f02e6c3c52` | <https://pi.math.cornell.edu/~connelly/pdf/10.1103_PhysRevE.75.051304.pdf> | 2026-09-03 (time not retained) | `pdftotext -layout` |
| Connelly notes | `packing/resources/papers/connelly-packings-of-circles-and-spheres-lecture-notes.pdf` | `5160747aece2fe51ab8a24799d92582382ba63f61ae4a6494e7c7031659b8ca2` | `packing/resources/papers/connelly-packings-of-circles-and-spheres-lecture-notes.raw.md` | `59bdb4dc724a4fd490d239610e29c993b784c147141f9c4fdcd50c6a8d882723` | <https://pi.math.cornell.edu/~connelly/PackingsIII.IV.pdf> | 2026-09-03 (time not retained) | `pdftotext -layout` |

The 2026-09-03 dates come from the prior-art review’s retained acquisition record and
are dates only. The Bal and Dewar URLs are the versioned arXiv identifiers embedded in
their PDFs, not an independently retained transfer log. Donev 2004’s paper identity,
local bytes, and extraction are retained, but its acquisition URL and retrieval time
cannot be reconstructed from the repository; no publisher URL is inferred here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
