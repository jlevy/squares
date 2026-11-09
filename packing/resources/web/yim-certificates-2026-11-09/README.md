# Kaelan Yim’s Certificates at ac14112

This packet retains 14 certificates from
[vitamoon/vitamoon](https://github.com/vitamoon/vitamoon/tree/ac14112009f5668b464170dcd979334a5537521d),
Kaelan Yim’s GitHub profile repository, at `ac14112009f5668b464170dcd979334a5537521d`
(committed 2026-11-09T09:49:17Z), the head of `main` when it was last read at 09:57Z on
9 November 2026 and again at 10:31Z. No issue reports them: the repository is watched
since [#895](https://github.com/jlevy/squares/issues/895), whose s(260) certificate it
also holds (T-265, [its packet](../yim-s260-upper-bound-2026-11-05/README.md)).
By the owner’s rule of 14 October 2026 each certificate is a report from the commit that
first holds it, dated by the push that made that commit public.

Six commits past that packet’s pin `d11a8a1` make the tree:

| Commit | Committed (UTC) | What it does |
| --- | --- | --- |
| `78eb9ea5da43230686941289b9de3ce0f8e34899` | 2026-11-09T07:13:34Z | adds `PACKINGS.md`, `SHA256SUMS`, `packing-certificates.json` and the certificates at 303, 553, 599, 600, 601, 602, 604, 645, 647, 648, 699 and 700 |
| `e4209f6a514937419cd5b23543770e013a25287e` | 07:30:26Z | adds `n299.cert` and its byte-identical copy `n299.cert.txt` |
| `c10e0944b12b66bbc8ee1e121967ff289c2bace6` | 08:42:14Z | adds `n130.cert`, its copy `n130.cert.txt` and `n130-source-LICENSE.txt` |
| `546928a8a3d43822334732f938fd83394e152856` | 09:36:10Z | **overwrites `n303.cert`** with a second certificate, and adds its copy `n303.cert.txt` and `n303-source-LICENSE.md` |
| `576223961cbc072e94f8b8dd1e879b903c78124a` | 09:48:41Z | changes `PACKINGS.md` and `packing-certificates.json` |
| `ac14112009f5668b464170dcd979334a5537521d` | 09:49:17Z | changes `packing-certificates.json` |

Every certificate at the pin is the same Git blob from the commit that adds it, so each
file here is the file first committed. The first `n303.cert`, blob `0e28ca53` of
`78eb9ea`, is a publication of its own: the
[yim-n303-2026-11-09](../yim-n303-2026-11-09/README.md) packet retains it at `78eb9ea`.
`sha256sum -c SHA256SUMS` passes on all 20 lines at the pin.

**Push times are not recorded.** GitHub’s activity log for the repository was not
readable from this session: the activity API and the activity page both refused it.
`78eb9ea` and `e4209f6` were public by 07:56:30Z, when the intake pass’s bead think-h96r
named both; `c10e094` by 08:55Z; and the last three by 09:57Z. No issue reached
jlevy/squares after #931 (06:03:48Z) through these reads, so no verdict here depends on
where in those windows a push fell.

## What the Source Claims

- **What they are.** `PACKINGS.md` calls the files “Exact rational witnesses of
  AI-assisted computational refinements” and “upper-bound certificates, not optimality
  proofs or blanket claims of current public records”, and says: “Do not credit these as
  independent original constructions.” It says that publishing them is not a
  registration request and that none was posted.
- **The format.** Each certificate is in Evan Daniel’s format: a comment line, the header
  `n S` with `S` an exact fraction, then `n` rows `x y t`, a rational centre and the
  rational tangent of each unit square’s half-angle.
  Each comment line names a lineage: at 130 Mishapolk after Francisco Couzo and PR #574’s
  contributors; at 299 Doğa Özden after Evan Daniel and Chris Deotte; at 303 Özden after
  Daniel, Deotte and Griffin Casson; at 604 Couzo and alexchilton; at the other ten
  Couzo and Lavrentev.
- **At 130.** An “archival envelope-only variant” of Mykhailo Polkovskyi’s #846
  certificate (T-259), about 1.96e-14 below it: “Every relative center and orientation is
  unchanged; only a common translation and the containing-box size change.
  This is not a new packing or numerical search gain.” It claims no Atlas credit and
  points to the
  [#846 discussion of padding-only re-certifications](https://github.com/jlevy/squares/issues/846#issuecomment-6543941452).
- **At 299.** A “verified microscopic tightening” of Doğa Özden’s pending #929 witness,
  about 1.18e-12 below it, from “returned-anchor continuation”: “a refinement of his
  arrangement, not a new construction or material gain.” It asks for the credit “Kaelan
  Yim after Doğa Özden, Evan Daniel and Chris Deotte”.
  `packing-certificates.json` names #929’s file by its SHA-256, `dfb0ccf7…5d9d`.
- **At 303.** A “verified microscopic refinement” of Özden’s pending #930 witness, about
  3.29e-12 below it, from a “no-strain control”: “Relative centers change
  microscopically; this is not merely a common translation/reboxing, but neither a
  structural nor material improvement.” It asks for the credit “Kaelan Yim after Doğa
  Özden, Evan Daniel, Chris Deotte and Griffin Casson”, and names #930’s file by its
  SHA-256, `9cbeb7a8…2f3e`, and the certificate it replaces.
  It adds that the author’s own admission protocol was not followed (“Admission remains
  noncompliant”) and that the exact geometry checks passed separately.
- **Above 324.** Refinements of Francisco Couzo’s packings after Vladislav Lavrentev’s,
  and at 604 after alexchilton’s, with no claim of a current record.
- **Checks.** Five local exact checks are said to accept every certificate, “not five
  wholly independent implementations”: evand/square-packing `bb4cc78e`’s `verify_cert.py`
  and `verify_cert2.py`, a local rational repair verifier, and this repository’s two
  maintained routes at `f30d6405` (#917’s merge).
  The checker digests it prints are those of the copies the
  [n183 packet](../evand-n183-subgrid-2026-10-19/README.md) retains.
- **AI assistance.** Hermes Agent was used “for research, numerical search,
  implementation and verification orchestration”.

Those statements are the author’s; no source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is 23 files: 16 retained under [source/](source/)
(2,741,606 bytes) and 7 pinned by digest (342,588 bytes).

| File | Bytes | Kept |
| --- | ---: | --- |
| `n130.cert` … `n700.cert`, 14 certificates | 18,044 to 268,315 | retained |
| `SHA256SUMS` | 1,559 | retained |
| `packing-certificates.json` | 37,764 | retained: each certificate’s side, digest, lineage, credit and checks |
| `PACKINGS.md` | 6,525 | pinned by digest: the author’s prose, quoted above |
| `n130.cert.txt`, `n299.cert.txt`, `n303.cert.txt` | 18,044, 121,708, 126,225 | pinned by digest: the same blobs as their certificates |
| `n130-source-LICENSE.txt` | 1,088 | pinned against the identical Mishapolk `LICENSE` the [mishapolk-issue732-2026-10-22](../mishapolk-issue732-2026-10-22/README.md) packet retains |
| `n303-source-LICENSE.md` | 1,484 | pinned against the identical Özden `LICENSE.md` the [ozden-s299-upper-bound-2026-11-03](../ozden-s299-upper-bound-2026-11-03/README.md) packet retains |
| `n260.cert` | 67,514 | pinned against the copy the [#895 packet](../yim-s260-upper-bound-2026-11-05/README.md) retains |

`README.md`, the author’s profile page, says nothing about packing and is not in the
scope. [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the
manifest and [acquisition/sources.json](acquisition/sources.json) the record.
No file has more than 1,000 lines, and the packet is about 4 MB with its receipts, so it
is kept in Git as stored.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `adca8d352` on 9 November
2026, #932’s merge, which adopted Özden’s #929 and #930 as the houses at 299 and 303,
T-277 and T-278). Each certificate is admitted at the side `PACKINGS.md` prints, its exact
side rounding up to it at 12 places.
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the counts above 324.

| n | Side, rounded up | Standing side it is compared with | Relation |
| ---: | --- | --- | --- |
| 130 | 11.902430645983 | T-259, the house: Couzo’s packing as Polkovskyi re-solved it, 11.902430645983 | below by 1.955e-14, the same 12-place print |
| 299 | 17.801004434255 | T-277, the house: Özden’s #929, 17.801004434256 | below by 1.18e-12, across the print |
| 303 | 17.901789273154 | T-278, the house: Özden’s #930, 17.901789273157 | below by 3.29e-12, across the print |
| 553 | 23.969145238668 | the couzo-issue763-2026-10-23 row, 23.969774299704 | below by 6.29e-4 |
| 599 | 24.936479681246 | the same source’s row, 24.937296174353 | below by 8.16e-4 |
| 600 | 24.951090275321 | the same source’s row, 24.951414939457 | below by 3.25e-4 |
| 601 | 24.958070476928 | the same source’s row, 24.958452262518 | below by 3.82e-4 |
| 602 | 24.981298949631 | the same source’s row, 24.981485660049 | below by 1.87e-4 |
| 604 | 24.995880488226 | the couzo-43f666c-2026-10-24 row, 24.996827861695 | below by 9.47e-4 |
| 645 | 25.881385537401 | the couzo-issue763-2026-10-23 row, 25.883109225944 | below by 1.72e-3 |
| 647 | 25.899272968790 | the same source’s row, 25.899276594081 | below by 3.63e-6 |
| 648 | 25.908803576981 | the same source’s row, 25.908836705326 | below by 3.31e-5 |
| 699 | 26.907311118315 | the same source’s row, 26.907571868006 | below by 2.61e-4 |
| 700 | 26.908036102718 | the same source’s row, 26.908095391467 | below by 5.93e-5 |

Francisco Couzo’s live index at his head `712c6a6` states the same sides as those rows at
all eleven counts above 324, so no later publication of his is lower.
The first n303, in the yim-n303-2026-11-09 packet, is 1.39e-10 above #930.

## Pose by Pose

`devtools.measure_identity` measured each certificate against the packing that holds its
count and wrote the receipts under [measure/](measure/). A measurement for credit; it
decides nothing.

- **130.** T-259’s certificate moved as one: every square shifts by the same
  $(-9.94 \times 10^{-15}, -9.89 \times 10^{-15})$, every half-angle tangent is
  identical and the rows keep their order, as the source says.
- **553 to 700.** Each pairs one to one with the row’s certificate under the identity by
  nearest centres. None moves beyond 0.1 at 600 and 700, so those two are refinements of
  Couzo’s packings. Elsewhere 1 (553) to 22 (699) squares move beyond 0.1, largest 0.566
  at 601, and turns reach 21.8 degrees at 601: further arrangements of his packings,
  one to one with them.

- **299 and 303.** Against T-277’s and T-278’s packets, the 299 certificate pairs one to
  one under the identity with no square beyond $10^{-3}$ (largest $4.25 \times 10^{-4}$,
  largest turn 0.017 degrees), and the 303 certificate with every square within
  $4.4 \times 10^{-12}$ and every turn below $10^{-12}$ degrees: re-solves of Özden’s
  packings. At 303 the first n303 of `78eb9ea` is measured too.

**The houses’ padding.** `devtools.contraction_margin` contracted each house certificate
uniformly to first contact, with no square re-solved, and decided the contracted packing
again on both maintained routes (`measure/contraction-nNNN.json`). It takes each house
below the certificate here:

| n | House | House’s margin | This certificate’s gain | Gain ÷ margin |
| ---: | --- | --- | --- | --- |
| 130 | T-259 | 2.18e-13 | 1.96e-14 | 0.09 |
| 299 | T-277 | 3.40e-12 | 1.18e-12 | 0.35 |
| 303 | T-278 | 3.40e-12 | 3.29e-12 | 0.97 |

The same tool measured two precedents for the owner’s question
(`measure/precedent-contraction-*.json`): T-259 at 130 lies 0.92 of #843’s margin below it,
and T-265 at 260 lies 9.97 times T-257’s margin below it, a re-solve the contraction does
not reach.

## Exact Replay

`devtools.upper_bound_reports certify` decided every certificate of the packet and its
duplicate-square and outside-container controls on both maintained routes, each job in
its own child process: 42 jobs, 13,609,950 pair decisions, 2,116.1 route CPU seconds,
the longest job 84.1 seconds (`receipts/exact-certification-nNNN.json.xz`, one per
count). The 13 certificates `c10e094` and `ac14112` share were decided at `c10e094`, and
the receipt was assembled with the jobs of the second n303 (`certify --finished`).
Every positive passed and every control was refused on both routes, and `check
--replay` decided all 42 jobs again.
The least wall clearance is $10^{-30}$ at 130, $2.8 \times 10^{-17}$ at 299, and
$5 \times 10^{-31}$ to $6.9 \times 10^{-24}$ elsewhere. The least pair gap is $10^{-30}$ at 299,
$1.8 \times 10^{-14}$ at 130 and $2.2 \times 10^{-16}$ to $1.1 \times 10^{-14}$ elsewhere.

`devtools.upper_bound_reports sharp-controls` took each certificate to exact contact and
$10^{-30}$ past it (`receipts/sharp-controls-nNNN.json`, 11 controls a count, 7,968 CPU
seconds in all). It lowered the side by the least far-wall clearance, closed the
least-gap pair by its gap, and moved every square toward the nearer near wall by its
least clearance: both routes accepted each at contact with margin 0 and refused each past
it. It enlarged one square to its pair and one to its wall: both routes refused each at
contact for its shape alone and $10^{-30}$ past it for the overlap or the wall as well.
Both refused a duplicated square. Every control at every count was as expected.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read each certificate through the `evand-cert`
reader. The author says he ran both at `f30d6405`, and neither route’s code has changed
since. So the replay reproduces the producer’s own checks with the producer’s code, as
he reports running them; it is not independent of them.
The source’s checkers were not run.

## Report Order and the Register

The [ledger of 9 November for this import](../../../campaign/issue-intake/upper-bounds-yim-certificates-20261109/README.md)
walks the four publications in commit order, from starts frozen at `main` `adca8d352`.
It records every claim but the first n303, which #930 holds:

- **553 to 700.** Eleven current beyond-horizon rows of this source, each superseding the
  row of couzo-issue763-2026-10-23 or, at 604, couzo-43f666c-2026-10-24.
- **299 and 303.** [T-280](../../../frontier/RESULTS.md), recorded as re-solves of T-277’s
  and T-278’s packings, credited to their finders, with Yim credited for the re-solve as a
  regularization. Each gain lies within its house certificate’s padding. Whether such a
  re-certification is a new result is the owner’s open question (think-ruu2’s RV-3, with
  think-ikku), so T-280 is held below the stage 4 exit, at V0/C0, its replay not entered,
  and neither house moves.
- **130.** [T-281](../../../frontier/RESULTS.md), a sub-print re-certification of T-259 in
  the restatement ruling’s words, which the record applies beyond the corpus only. It is
  held at V0/C0 for think-ikku’s RV-1 (and think-oqjd), as T-260 is, and the house does
  not move.

## What Is Not Established

- **A stage 4 review.** None is retained. A separate blind lane reviews T-280 and T-281;
  its record maps under each entry’s `reviews` and its read under the report evidence’s
  `external_review`, which lifts each to C1 and no further while the holds stand.
- **Human oversight.** No human oversight record is retained.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **Push times.** The activity log was not read; see above.

## Credit and Licence

The certificates are Kaelan Yim’s re-certifications and refinements of other holders’
packings, by his own account and as measured: Polkovskyi’s re-solve of Couzo’s packing at
130, Özden’s at 299 and 303, and Couzo’s, after Lavrentev and at 604 after alexchilton,
above 324. The search was AI-assisted (Hermes Agent).

The repository carries no licence file, and `PACKINGS.md` says that the snapshot “makes no
blanket new license assertion for inherited third-party materials”. The CC BY 4.0 grant
of 5 November names `n260.cert` alone.
`packing-certificates.json` says the n299 cohort’s results “inherit source CC BY 4.0”:
that is Özden’s licence for #929’s files, as the author reads it, and no grant of his
own. The second n303 carries Özden’s licence for #930’s files as
`n303-source-LICENSE.md`. `n130.cert` translates Polkovskyi’s MIT-licensed certificate
and carries its notice.
No source was submitted to this repository, so the presumption of permission from
submission does not apply. The certificates, `SHA256SUMS` and
`packing-certificates.json` are retained as factual data under the owner’s decision of
9 October 2026
([Retained Factual Data](../known-best-packings/README.md#retained-factual-data)).
`PACKINGS.md`, the author’s prose, is pinned by digest only.
Retaining a file grants no licence and relicenses nothing.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source yim-certificates-2026-11-09 --checkout CHECKOUT
python -m devtools.acquire_source yim-certificates-2026-11-09 --check
python -m devtools.upper_bound_reports yim-certificates-2026-11-09 check-claims --write
python -m devtools.upper_bound_reports yim-certificates-2026-11-09 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports yim-certificates-2026-11-09 check --replay
python -m devtools.upper_bound_reports yim-certificates-2026-11-09 sharp-controls
python -m devtools.measure_identity --n 130 'YIM=packet:yim-certificates-2026-11-09' \
  'T-259=packet:mishapolk-issue846-2026-10-30' \
  'house-witness=witness-center-basis:witnesses/known-best/n-130.yaml' \
  --out resources/web/yim-certificates-2026-11-09/measure/identity-n130.json
python -m devtools.measure_identity --n 553 'YIM=packet:yim-certificates-2026-11-09' \
  'couzo-issue763=evand-cert:resources/web/couzo-issue763-2026-10-23/source/certificates/best/n553.cert' \
  --out resources/web/yim-certificates-2026-11-09/measure/identity-n553.json
```

The contraction margins, with the house first and this certificate against it:

```bash
python -m devtools.contraction_margin --n 299 'T-277=packet:ozden-s299-upper-bound-2026-11-09' \
  --against 'YIM=packet:yim-certificates-2026-11-09' \
  --out resources/web/yim-certificates-2026-11-09/measure/contraction-n299.json
```

The other counts above 324 are measured the same way, against
`couzo-issue763-2026-10-23`’s certificate at each, and at 604 against
`couzo-43f666c-2026-10-24`’s.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
