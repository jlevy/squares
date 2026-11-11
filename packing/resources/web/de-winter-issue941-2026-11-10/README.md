# Joost de Winter’s Fifteen Certificates of Issue 941

This packet retains the folder `above324/` of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/71da0d56fd91b7061addca2a728ee72ec9728b0b/above324)
at `71da0d56fd91b7061addca2a728ee72ec9728b0b` (committed 2026-11-10T06:15:17Z), the
commit [issue #941](https://github.com/jlevy/squares/issues/941) names.
The issue, opened at 13:30:51Z on 10 November 2026, asks for the registration of fifteen
upper bounds between 413 and 910, all beyond the case corpus.
Intake lane L90 (think-cen3) retained, replayed and measured them on 11 November 2026.

Two commits make the folder:

| Commit | Committed (UTC) | What it does |
| --- | --- | --- |
| `d3a020eae21f0738a081a335b8f0dca13b41f07b` | 2026-11-09T23:59:23Z | adds `above324/` with `README.md`, `SHA256SUMS`, `verify_cert.py`, the certificates at 413, 494, 539, 543, 547, 590, 809, 810 and 867 and five figures |
| `71da0d56fd91b7061addca2a728ee72ec9728b0b` | 2026-11-10T06:15:17Z | adds the certificates at 738, 739, 753, 794, 851 and 910 and the 753 figure, and updates the folder’s `README.md`, its `SHA256SUMS` and one line of the root README |

`71da0d5` touches no earlier certificate, so each of the fifteen files here is the Git
blob of the commit that first holds it.
No later commit through the head `c4e65d0` changes `above324/`.
`sha256sum -c SHA256SUMS` passes on all 16 lines at the pin.

**Report order.** `d3a020e` published nine of the certificates 13.5 hours before the
issue.
Under the owner’s rule of 14 October 2026 a watched publication with no issue is a
report from its first commit.
Here an issue claims every one of them, so the ledger dates them by the issue and keeps
each first commit, as #763’s ledger did.
No other report reached any of the fifteen counts between `d3a020e` and #941, so the
verdicts are the same either way.

**Push times are not recorded.** GitHub’s activity log and events API both refused this
session. `d3a020e` and `71da0d5` were public by 13:30:51Z, when the issue named
`71da0d5`.

## What the Source Claims

- **The certificates.** Each `nNNNN.cert` holds two comment lines, then `n S` with `S`
  an exact decimal fraction, then `n` rows `x y t`: a rational centre and the rational
  tangent of each unit square’s half-angle.
  It is Evan Daniel’s format with a second comment line, and the `evand-cert` reader
  reads it.

- **The sides.** The issue and the folder’s README print each side rounded up at 10
  places. Each is below “the best value I could find in this repository at commit
  200f2eb”, including monotonicity and border consequences.

- **The construction.** Seven are square sub-windows of Francisco Couzo’s packings at a
  larger count, re-optimized locally:

| n | Sub-window of Couzo’s packing at | The source’s note on the side |
| ---: | ---: | --- |
| 413 | 544 | within 10⁻⁴³ of the arrangement’s local optimum |
| 494 | 539 | about 5 × 10⁻⁹ above the numerical optimum |
| 543 | 590 | within 10⁻⁴³ |
| 547 | 696 | within 10⁻⁴³; the sub-window was already at its local optimum |
| 738 | 851 | about 5 × 10⁻⁹ |
| 739 | 851 | about 5 × 10⁻⁹ |
| 810 | 868 | about 5 × 10⁻⁹ |

The 753 is a sub-window of the 810 here, re-optimized.
Six are borders of axis-aligned squares on these: 539 on 494, 590 on 543, 794 on 739,
851 on 794, 867 on 810 and 910 on 851. The 809 is the 810 with one square removed.

- **What it does not claim.** The local-optimality statements rest on a numerical
  solution of the optimality conditions to 65 digits and have no formal proof.
  The issue adds that public submission files of the Kaggle competition “Squares in
  Squares” hold smaller packings at 14 of the 15 counts, all but 543.

- **The checks.** `verify_cert.py` (`fractions.Fraction`) checks containment and a
  separating-axis test on every pair with centres closer than √2. The issue says a
  second script with separate code by the same author checked the same packings.
  It says the two share one author, the separating-axis test and `Fraction`, and that
  the certificates were not replayed with this repository’s checkers.

- **AI assistance.** The sub-window search, local optimization, high-precision solution,
  rational certificates, checks and figures were produced with Claude (Anthropic) under
  Joost de Winter’s direction.

Those statements are the author’s; no source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the licence, the root README and the whole of `above324/`: 26 files, 19
retained under [source/](source/) and 7 pinned by digest.

| File | Bytes | Kept |
| --- | ---: | --- |
| `above324/n0413.cert` … `n0910.cert`, 15 certificates | 66,356 to 189,130; 1,728,547 in all | retained, each under 1,000 lines |
| `above324/README.md`, `above324/SHA256SUMS` | 3,442 and 1,236 | retained |
| `above324/verify_cert.py` | 2,638 | retained as data, never executed here |
| `README.md` | 1,589 | retained |
| `LICENSE` | 1,072 | pinned against the byte-identical copy the [de-winter-upper-bounds-227-229-260-2026-10-17](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md) packet retains |
| `above324/*.png`, six figures | 53,281 to 141,295 | pinned by digest only |

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `8afdabe8f` on 11
November 2026). Every exact side rounds up at 10 places to the side the issue prints.
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the fifteen rows.

| n | Side, rounded up | Row it supersedes (side) | Below it by |
| ---: | --- | --- | --- |
| 413 | 20.8239520077 | `couzo-issue763-2026-10-23` (20.824764038662) | 8.12 × 10⁻⁴ |
| 494 | 22.7365988643 | `couzo-issue763-2026-10-23` (22.737532875219) | 9.34 × 10⁻⁴ |
| 539 | 23.7365988643 | `couzo-issue763-2026-10-23` (23.736669673811) | 7.08 × 10⁻⁵ |
| 543 | 23.8024287170 | `tymchishin-22-3662-2026-10-23` (23.803053261145) | 6.25 × 10⁻⁴ |
| 547 | 23.8787301198 | `couzo-issue763-2026-10-23` (23.879127653315) | 3.98 × 10⁻⁴ |
| 590 | 24.8024287170 | `couzo-issue763-2026-10-23` (24.802527132871) | 9.84 × 10⁻⁵ |
| 738 | 27.6912062515 | `couzo-43f666c-2026-10-24` (27.691283629524) | 7.74 × 10⁻⁵ |
| 739 | 27.6912835939 | `couzo-issue763-2026-10-23` (27.691450272099) | 1.67 × 10⁻⁴ |
| 753 | 27.9026514302 | `couzo-issue763-2026-10-23` (27.907984230435) | 5.33 × 10⁻³ |
| 794 | 28.6912835939 | `couzo-issue763-2026-10-23` (28.691448980966) | 1.65 × 10⁻⁴ |
| 809 | 28.9079170470 | `couzo-issue763-2026-10-23` (28.908036098650) | 1.19 × 10⁻⁴ |
| 810 | 28.9079170470 | `couzo-issue763-2026-10-23` (28.910451045451) | 2.53 × 10⁻³ |
| 851 | 29.6912835939 | `couzo-issue763-2026-10-23` (29.691448975560) | 1.65 × 10⁻⁴ |
| 867 | 29.9079170470 | `couzo-43f666c-2026-10-24` (29.908036097699) | 1.19 × 10⁻⁴ |
| 910 | 30.6912835939 | `couzo-issue763-2026-10-23-recipes` (30.691448975560) | 1.65 × 10⁻⁴ |

Each side is also below Göbel’s construction at its count, by 1.58 × 10⁻² (739, 794, 851
and 910) to 0.532 (753).

## Exact Replay

`devtools.upper_bound_reports certify` decided every certificate and its
duplicate-square and outside-container controls on both maintained routes, each job in
its own child process, two at a time at `nice -n 19`: 45 jobs, 22,619,004 pair
decisions, 3,821.6 route CPU seconds, the longest job 168.4 seconds
([receipts/](receipts/), `exact-certification-nNNN.json.xz`, one per count).
Every positive passed and every control was refused on both routes, and `check` admits
all 45 jobs. The two routes agree on every least clearance:

- **The borders.** At 539, 590, 794, 851, 867 and 910 the border’s axis-aligned squares
  touch the box and each other, so the least wall clearance and the least pair gap are
  both exactly 0.
- **The 65-digit solutions.** At 413, 543 and 547 every wall clears by 5 × 10⁻⁴⁶ and
  every pair by 10⁻⁴⁵.
- **The rest.** At 494, 738, 739, 753, 809 and 810 the walls clear by 1.0 × 10⁻¹⁰ to 4.2
  × 10⁻¹⁰ and the pairs by 2.0 × 10⁻¹⁰ to 8.8 × 10⁻¹⁰, not the 5 × 10⁻⁹ the issue gives
  as its margin above the numerical optimum, which is a margin in the side.

**Sharp controls.** `devtools.upper_bound_reports sharp-controls` took each certificate
to exact contact and 10⁻³⁰ past it on both routes, 11 controls a count as stated in
advance on think-cen3 ([receipts/](receipts/), `sharp-controls-nNNN.json`: 165 controls
at 15 counts, 14,154 CPU seconds), and every control behaved as the module predicts.
The side lowered to the extent, the tightest pair closed and every square moved to its
near wall were accepted at contact with margin exactly 0 and refused 10⁻³⁰ past it.
The square enlarged to its pair and the one enlarged to its wall were refused at contact
for their shape alone and past it for the overlap or the wall as well, and the
duplicated square was refused.
At the six borders the least far-wall clearance, pair gap and near-wall clearance are 0,
so the at-contact half of those three controls is the certificate itself.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method.
Neither shares code with the author’s `verify_cert.py`, which was not run.
`check --replay`, which decides every job again, was not run, to save the 1.1 CPU-hours
it costs; `check` admits the retained rows.

## Pose by Pose and Padding

`devtools.measure_identity` measured each certificate against the row’s certificate at
its count ([measure/](measure/), `identity-nNNN.json`): a measurement for credit, which
decides nothing.
`devtools.contraction_margin` contracted the row’s certificate uniformly
about the origin to first contact and boxed it (`contraction-nNNN.json`), and compared
this certificate’s gain with that margin.
Where the row is an L-border recipe its padding is its base’s, measured at the base’s
count (`contraction-nNNN-base-nMMM.json`). The lane ran it with `--no-routes`: the
margin is exact without the two route decisions, which would only prove the contracted
packing a bound of its own.

| n | Against the row’s packing | Row certificate’s margin | Gain ÷ margin |
| ---: | --- | --- | ---: |
| 413 | not one to one; 50 squares beyond 0.1 under the best assignment; another arrangement | 4.00 × 10⁻⁹ | 2.03 × 10⁵ |
| 494 | one to one (identity); 0 squares beyond 0.1, largest 0.0991599; a refinement of it | 1.95 × 10⁻¹¹ | 4.79 × 10⁷ |
| 539 | one to one (identity); 5 squares beyond 0.1, largest 0.173133; a further arrangement of it | 1.87 × 10⁻¹² | 3.79 × 10⁷ |
| 543 | not one to one; 104 squares beyond 0.1 under the best assignment; another arrangement | 9.14 × 10⁻⁹ | 6.83 × 10⁴ |
| 547 | one to one (symmetry 7); 16 squares beyond 0.1, largest 0.614324; a further arrangement of it | 4.80 × 10⁻¹² | 8.27 × 10⁷ |
| 590 | not one to one; 40 squares beyond 0.1 under the best assignment; another arrangement | 4.77 × 10⁻¹³ | 2.07 × 10⁸ |
| 738 | not one to one; 406 squares beyond 0.1 under the best assignment; another arrangement | 5.34 × 10⁻⁹ | 1.45 × 10⁴ |
| 739 | one to one (identity); 19 squares beyond 0.1, largest 0.19485; a further arrangement of it | 7.18 × 10⁻⁸ | 2.32 × 10³ |
| 753 | not one to one; 338 squares beyond 0.1 under the best assignment; another arrangement | 5.67 × 10⁻¹² | 9.40 × 10⁸ |
| 794 | one to one (identity); 27 squares beyond 0.1, largest 0.864893; a further arrangement of it | 9.92 × 10⁻⁹ | 1.67 × 10⁴ |
| 809 | not one to one; 208 squares beyond 0.1 under the best assignment; another arrangement | 5.73 × 10⁻¹² | 2.08 × 10⁷ |
| 810 | not one to one; 122 squares beyond 0.1 under the best assignment; another arrangement | 5.83 × 10⁻¹² | 4.34 × 10⁸ |
| 851 | one to one (identity); 28 squares beyond 0.1, largest 0.977634; a further arrangement of it | 4.83 × 10⁻⁹ | 3.42 × 10⁴ |
| 867 | not one to one; 367 squares beyond 0.1 under the best assignment; another arrangement | 3.82 × 10⁻¹² | 3.12 × 10⁷ |
| 910 | no n-square certificate: the row is an L-border recipe on Couzo’s 851 | 4.83 × 10⁻⁹ (its base at 851) | 3.42 × 10⁴ |

Six are one to one with the row’s packing at the same count.
The 494 pairs with Couzo’s 494 under the identity with no square beyond a tenth (largest
0.0992), so by the record’s word it is a refinement of that packing, although the issue
calls it a sub-window of his 539; the ledger classes it as that refinement (the review’s
F14). The 539, 739, 794 and 851 are further arrangements of his, 5 to 28 squares beyond
a tenth, and the 547 pairs with his under a reflection (symmetry 7), 16 beyond a tenth.
The other eight are other arrangements than the rows’.

Every gain is at least 2.3 × 10³ times its row certificate’s padding, the least at 739,
whose row certificate is padded by 7.2 × 10⁻⁸. So no gain re-certifies a predecessor’s
padding, and none is think-ruu2’s RV-3 material.

## Report Order and the Register

The
[ledger of 11 November for this import](../../../campaign/issue-intake/upper-bounds-941-942-20261111/README.md)
walks #941, #942 and #942’s addendum from starts frozen at `main` `8afdabe8f`, and
records all fifteen claims here.
Fourteen are new packings in the issue’s own words, 809 among them.
The 494 is classed as a refinement of Couzo’s packing at 494, after Vladislav
Lavrentev’s, since the identity measurement pairs it one to one with that packing, no
square beyond a tenth; the issue calls it a sub-window of his 539, and both can hold
(the stage 4 review’s F14).

- **Fourteen rows.** Each is a current beyond-horizon row of this source, at assurance
  `verified`, and supersedes the row it is below.
- **809 is held.** The 809 is the 810 certificate less its last square, at 810’s side: a
  one-square deletion bound the issue claims beside the 810 it is taken from (the
  review’s F5). Whether an issue-claimed deletion bound gets a row is the owner’s open
  question, think-kzme, and the record gives none at 743, 798, 855 and 985, where #715
  and #732 claim such bounds.
  So 809 has no row, the row of `couzo-issue763-2026-10-23` stays current there, the
  declaration requests no row at 809, and think-kzme’s notes name it.
  Both routes and the review accept the 809 certificate.

These are bounds below the record, not the best known packings: the issue itself says
public Kaggle submissions hold smaller packings at 14 of its 15 counts, all but 543,
though none of them reached this repository as a report (the review’s F9). Beyond the
corpus no register entry records them.

## Stage 4 Review

The
[stage 4 review of 11 November](../../../../docs/project/reviews/review-2026-11-11-dewinter-941-942-upper-bounds.md)
(lane L96) was written in a separate lane, blind to this one until its findings were
frozen. Its programs, frozen inputs and shared receipts are under
[`review/review-2026-11-11/`](review/review-2026-11-11/README.md), and each count’s
receipts are in its own packet.

- **Verdict.** It accepts all 37 certificates, nothing blocking: `l96_check.py` decides
  every square, wall and pair by separating axes in `Fraction` and by exact clipped
  areas in `gmpy2.mpq`, the two agreeing everywhere, and all 333 controls of its frozen
  plan came out as stated.
- **Against this lane.** Its frozen comparison with this lane’s ledger, manifests and
  margins prints `LANE_AGREES`.
- **Mapped.** This replay is `E-de-winter-941-exact-feasibility`, the review’s run
  `E-de-winter-941-review-exact-feasibility`, and the review is recorded under
  `external_review` on `E-de-winter-941-certificate-report`. Its checker is
  `V-de-winter-941-942-review-check`, clean room, of the producer’s system family
  (Claude). The fourteen rows are verified from the two runs.
- **Its findings on the record**, answered here and in the other two packets: F5 (809,
  above), F7 (the refined README’s twenty-two, in the
  [a0c4fc8 packet](../de-winter-a0c4fc8-2026-11-10/README.md#what-the-source-claims)),
  F8 (the Kaggle starting packings’ licences, in the
  [#942 packet](../de-winter-issue942-2026-11-10/README.md#credit-and-licence)), F9
  (above) and F14 (494, above).
  F10’s dating of the addendum is the ledger’s already.

## Questions for the Author

The review’s five questions, informational; none bears on a verdict:

1. #942 says sixteen packings still had a descent direction, and the README at
   `a0c4fc80` says twenty-two improved by at least 1e-6. Were the six addendum counts
   below the 1e-6 threshold at first, or found by a later run?
2. Under what licence did the Kaggle notebooks and datasets publish the starting
   packings, and does the merge file state one?
3. Can the individual authors of the 22 refined arrangements be identified, for example
   by the notebook each came from?
4. What does “a margin of about 5e-9 above the numerical optimum” measure?
   The certificates leave about 10⁻¹⁰ at each wall and 2 × 10⁻¹⁰ between nearest pairs.
5. Is 809 meant as its own claim, or as the deletion bound from 810?

## What Is Not Established

- **Human oversight.** The stage 4 review is an AI review, by the producer’s system
  family; no human oversight record is retained.
- **Push times.** The activity log was not read; see above.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The consequences.** The sides here also bound counts the issue does not claim, by
  deletion (one to three squares fewer) and by the border step s(n + 2⌊s⌋ + 1) ≤ s(n) +
  1\. Those bounds have no rows.
  Whether a deletion bound gets a row, claimed or not, is the owner’s open question
  (think-kzme).

## Credit and Licence

Credit Joost de Winter (Delft University of Technology), whose sub-window search found
square windows of Francisco Couzo’s packings that hold more squares than the best
recorded packing of the same side.
The issue credits the source arrangements to Couzo (#763, `franciscouzo/square-packing`
`43f666c`). The work was AI-assisted (Claude).

The repository is MIT-licensed, copyright 2026 Joost de Winter, by its `LICENSE`, and
the root README says every file is released under it.
Retaining a file grants no licence and relicenses nothing.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source de-winter-issue941-2026-11-10 --checkout CHECKOUT
python -m devtools.acquire_source de-winter-issue941-2026-11-10 --check
python -m devtools.upper_bound_reports de-winter-issue941-2026-11-10 check-claims --write
python -m devtools.upper_bound_reports de-winter-issue941-2026-11-10 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports de-winter-issue941-2026-11-10 check --replay
python -m devtools.upper_bound_reports de-winter-issue941-2026-11-10 sharp-controls
python -m devtools.measure_identity --n 413 'DE-WINTER=packet:de-winter-issue941-2026-11-10' \
  'couzo-issue763=evand-cert:resources/web/couzo-issue763-2026-10-23/source/certificates/best/n413.cert' \
  --out resources/web/de-winter-issue941-2026-11-10/measure/identity-n413.json
python -m devtools.contraction_margin --n 413 \
  'couzo-issue763=evand-cert:resources/web/couzo-issue763-2026-10-23/source/certificates/best/n413.cert' \
  --against 'DE-WINTER=packet:de-winter-issue941-2026-11-10' --no-routes \
  --out resources/web/de-winter-issue941-2026-11-10/measure/contraction-n413.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
