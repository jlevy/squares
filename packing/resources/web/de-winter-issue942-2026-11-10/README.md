# Joost de Winter’s Sixteen Certificates of Issue 942

This packet retains the folder `above324_refined/` of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/a9486ede74cd75996f488605f27d7fce32a73b3a/above324_refined)
at `a9486ede74cd75996f488605f27d7fce32a73b3a` (committed 2026-11-10T14:39:52Z), the
commit [issue #942](https://github.com/jlevy/squares/issues/942) names 1 minute 26
seconds later. The issue asks for the registration of sixteen upper bounds between 632
and 989, all beyond the case corpus.
Intake lane L90 (think-cen3) retained, replayed and measured them on 11 November 2026.

`a9486ed` adds the folder: `README.md`, `SHA256SUMS`, `verify_cert.py` and the sixteen
certificates. `a0c4fc8`, 58 minutes later, adds six more certificates and changes the
folder’s README and `SHA256SUMS`; the
[de-winter-a0c4fc8-2026-11-10](../de-winter-a0c4fc8-2026-11-10/README.md) packet retains
those. No commit through the head `c4e65d0` changes the sixteen here.
`sha256sum -c SHA256SUMS` passes on all 17 lines at the pin.
GitHub’s activity log was not readable from this session, so no push time is recorded;
the issue dates the claims.

## What the Source Claims

- **The certificates.** Each `nNNNN.cert` is in the format of the `above324/` folder
  (see the [#941 packet](../de-winter-issue941-2026-11-10/README.md)), its second
  comment line “public competition packing, re-optimized”.
- **The sides.** The issue and the folder’s README print each side rounded up at 10
  places. Beside each they print the best public packing of the Kaggle competition
  “Squares in Squares” the author could find, and this repository’s register value at
  `f54ad104`. Each new side is below both.
- **The construction.** The starting packings come from
  `data_out/best_certified_22.2226173_before_clearance.csv` in
  `Samanyu-dev/squares_in_squares` at `53551d7`, a per-puzzle merge of public Kaggle
  notebooks and datasets.
  Its README credits Chris Deotte, lightningv08, alexchilton, kirilltym, malyshevdanil,
  prvsiyan, busyaprime, nilanjansaha123, jazivxt and the register of Francisco Couzo.
  The file does not name the author of each packing.
  - A linear program on the contact constraints found a remaining descent direction in
    sixteen of the file’s 1000 packings.
  - Following it to convergence gave these sides, “the arrangements of the squares are
    unchanged”. Each certificate carries a margin of about 5 × 10⁻⁹ above the numerical
    optimum.
  - The issue claims only the local re-optimization and cannot credit the sixteen
    arrangements individually.
- **The checks.** `verify_cert.py`, byte-identical to `above324/verify_cert.py`, and a
  second script by the same author, as for #941. The certificates were not replayed with
  this repository’s checkers, the issue says.
- **AI assistance.** The descent test, local optimization, rational certificates and
  checks were produced with Claude (Anthropic) under Joost de Winter’s direction.

Those statements are the author’s; no source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the licence, the root README and the whole of `above324_refined/`: 21
files, 19 retained under [source/](source/) and 2 pinned by digest.

| File | Bytes | Kept |
| --- | ---: | --- |
| `above324_refined/n0632.cert` … `n0989.cert`, 16 certificates | 70,156 to 132,720; 1,566,026 in all | retained, each under 1,000 lines |
| `above324_refined/README.md`, `above324_refined/SHA256SUMS` | 2,932 and 1,313 | retained |
| `README.md` | 1,852 | retained |
| `above324_refined/verify_cert.py` | 2,638 | pinned against the byte-identical copy the [#941 packet](../de-winter-issue941-2026-11-10/README.md) retains |
| `LICENSE` | 1,072 | pinned against the copy the [de-winter-upper-bounds-227-229-260-2026-10-17](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md) packet retains |

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `8afdabe8f` on 11
November 2026). Every exact side rounds up at 10 places to the side the issue prints.
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the sixteen rows.

| n | Side, rounded up | Row it supersedes (side) | Below it by |
| ---: | --- | --- | --- |
| 632 | 25.6456954277 | `couzo-43f666c-2026-10-24` (25.656854249498) | 1.12 × 10⁻² |
| 637 | 25.7447388658 | `couzo-43f666c-2026-10-24` (25.769289510287) | 2.46 × 10⁻² |
| 655 | 25.9996711101 | none; the grid, 26 | 3.29 × 10⁻⁴ |
| 684 | 26.6456964776 | `couzo-43f666c-2026-10-24` (26.656854249498) | 1.12 × 10⁻² |
| 685 | 26.6870020013 | `tymchishin-reclosure-v3-2026-10-23` (26.692388159732) | 5.39 × 10⁻³ |
| 744 | 27.7601633593 | `couzo-43f666c-2026-10-24` (27.786715806974) | 2.66 × 10⁻² |
| 750 | 27.8595204745 | `couzo-issue763-2026-10-23` (27.874585541193) | 1.51 × 10⁻² |
| 756 | 27.9245802503 | `couzo-43f666c-2026-10-24` (27.949602638227) | 2.50 × 10⁻² |
| 805 | 28.8450303356 | `couzo-issue763-2026-10-23` (28.858216341607) | 1.32 × 10⁻² |
| 814 | 28.9549571055 | `couzo-issue763-2026-10-23` (28.961440808824) | 6.48 × 10⁻³ |
| 918 | 30.7867372035 | `couzo-43f666c-2026-10-24` (30.796057688423) | 9.32 × 10⁻³ |
| 921 | 30.8271449853 | `couzo-issue763-2026-10-23` (30.839621660274) | 1.25 × 10⁻² |
| 924 | 30.8553857463 | `couzo-43f666c-2026-10-24` (30.870828693406) | 1.54 × 10⁻² |
| 935 | 30.9800571865 | `couzo-964ee2b-2026-10-23` (30.994174058119) | 1.41 × 10⁻² |
| 970 | 31.6389903231 | `couzo-issue763-2026-10-23-recipes` (31.656854249499) | 1.79 × 10⁻² |
| 989 | 31.8889473785 | `couzo-43f666c-2026-10-24` (31.909679351448) | 2.07 × 10⁻² |

Each side is also below Göbel’s construction at its count, by 2.01 × 10⁻² (685) to 0.707
(655).

## Exact Replay

`devtools.upper_bound_reports certify` decided every certificate and its
duplicate-square and outside-container controls on both maintained routes, each job in
its own child process, two at a time at `nice -n 19`: 48 jobs, 31,483,980 pair
decisions, 4,686.1 route CPU seconds, the longest job 189.2 seconds
([receipts/](receipts/), `exact-certification-nNNN.json.xz`, one per count).
Every positive passed and every control was refused on both routes, and `check` admits
all 48 jobs. The two routes agree on every least clearance: every wall clears by 1.0 ×
10⁻¹⁰ to 5.3 × 10⁻¹⁰ and every pair by 2.0 × 10⁻¹⁰ to 1.4 × 10⁻⁹, the padding of the
rationalization; the 5 × 10⁻⁹ the issue gives is a margin in the side above the
numerical optimum.

**Sharp controls.** `devtools.upper_bound_reports sharp-controls` took each certificate
to exact contact and 10⁻³⁰ past it on both routes, 11 controls a count as stated in
advance on think-cen3 ([receipts/](receipts/), `sharp-controls-nNNN.json`: 176 controls
at 16 counts, 17,423 CPU seconds), and every control behaved as the module predicts.
The side lowered to the extent, the tightest pair closed and every square moved to its
near wall were accepted at contact with margin exactly 0 and refused 10⁻³⁰ past it.
The square enlarged to its pair and the one enlarged to its wall were refused at contact
for their shape alone and past it for the overlap or the wall as well, and the
duplicated square was refused.

The two routes share a reader and the separating-axis method, as the
[#941 packet](../de-winter-issue941-2026-11-10/README.md#exact-replay) says, and the
author’s `verify_cert.py` was not run.
`check --replay` was not run, to save the 1.3 CPU-hours it costs; `check` admits the
retained rows.

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
| 632 | no n-square certificate: the row is an L-border recipe on Couzo’s 583 | 4.90 × 10⁻¹² (its base at 583) | 2.28 × 10⁹ |
| 637 | not one to one; 320 squares beyond 0.1 under the best assignment; another arrangement | 5.47 × 10⁻¹² | 4.48 × 10⁹ |
| 655 | no row certificate (the grid) | — | — |
| 684 | not one to one; 278 squares beyond 0.1 under the best assignment; another arrangement | 5.42 × 10⁻¹² | 2.06 × 10⁹ |
| 685 | not one to one; 433 squares beyond 0.1 under the best assignment; another arrangement | 2.88 × 10⁻¹⁰ | 1.87 × 10⁷ |
| 744 | no n-square certificate: the row is an L-border recipe on Couzo’s 691 | 5.59 × 10⁻¹² (its base at 691) | 4.75 × 10⁹ |
| 750 | not one to one; 255 squares beyond 0.1 under the best assignment; another arrangement | 3.17 × 10⁻¹² | 4.75 × 10⁹ |
| 756 | not one to one; 279 squares beyond 0.1 under the best assignment; another arrangement | 5.64 × 10⁻¹² | 4.44 × 10⁹ |
| 805 | not one to one; 333 squares beyond 0.1 under the best assignment; another arrangement | 5.82 × 10⁻¹² | 2.27 × 10⁹ |
| 814 | not one to one; 233 squares beyond 0.1 under the best assignment; another arrangement | 1.58 × 10⁻¹¹ | 4.10 × 10⁸ |
| 918 | not one to one; 250 squares beyond 0.1 under the best assignment; another arrangement | 6.28 × 10⁻¹² | 1.49 × 10⁹ |
| 921 | not one to one; 383 squares beyond 0.1 under the best assignment; another arrangement | 6.24 × 10⁻¹² | 2.00 × 10⁹ |
| 924 | not one to one; 176 squares beyond 0.1 under the best assignment; another arrangement | 1.68 × 10⁻¹¹ | 9.18 × 10⁸ |
| 935 | not one to one; 410 squares beyond 0.1 under the best assignment; another arrangement | 6.32 × 10⁻¹² | 2.23 × 10⁹ |
| 970 | no n-square certificate: the row is an L-border recipe on Couzo’s 850 | 6.12 × 10⁻¹² (its base at 850) | 2.92 × 10⁹ |
| 989 | not one to one; 427 squares beyond 0.1 under the best assignment; another arrangement | 6.47 × 10⁻¹² | 3.20 × 10⁹ |

None of the thirteen measured is one to one with the row’s packing under any symmetry:
each is another arrangement, 176 to 433 squares beyond a tenth under the best
assignment. At 632, 744 and 970 the row is Couzo’s L-border recipe, which no n-square
certificate states, and at 655 the grid.
Every gain is at least 1.9 × 10⁷ times its row certificate’s padding (at 685), so none
is think-ruu2’s RV-3 material.

## Report Order and the Register

The
[ledger of 11 November for this import](../../../campaign/issue-intake/upper-bounds-941-942-20261111/README.md)
records all sixteen claims.
Each is a current beyond-horizon row of this source, at assurance `verified`, and
supersedes the row it is below, at 655 the grid.
The rows rest on this replay, `E-de-winter-942-exact-feasibility`, and the stage 4
review’s clean-room run, `E-de-winter-942-review-exact-feasibility`, as the
[#941 packet](../de-winter-issue941-2026-11-10/README.md#stage-4-review) sets out.
Beyond the corpus no register entry records them.

These are bounds below the record, which the record does not call the best known
packings (the review’s F9): each arrangement is another holder’s public Kaggle packing,
re-optimized, and the issue’s own table puts each side 1.8e-07 to 3.8e-04 below the best
public packing it found, a comparison not checked here; Kaggle files no report brought
here may hold smaller ones.
Against this record the sides are 3.3 × 10⁻⁴ (655, below the grid) to 2.7 × 10⁻² lower.

## What Is Not Established

- **Human oversight**, **push times**, **optimality** and **the consequences** stand as
  in the
  [#941 packet](../de-winter-issue941-2026-11-10/README.md#what-is-not-established).
- **Each packing’s finder.** The merged file names no author per packing, so the record
  cannot credit the arrangements individually either.

## Credit and Licence

Credit Joost de Winter (Delft University of Technology) for the local re-optimization,
after the public Kaggle packings of the merged file, whose README credits Chris Deotte,
Vladislav Lavrentev (lightningv08), Alex Chilton (alexchilton), Kirill Tymchishin
(kirilltym), malyshevdanil, prvsiyan, busyaprime, nilanjansaha123, jazivxt and Francisco
Couzo’s register. The work was AI-assisted (Claude).

The repository is MIT-licensed, copyright 2026 Joost de Winter, by its `LICENSE`, which
the packet pins against the byte-identical copy `main` retains.
The licence of the starting packings, the public Kaggle notebooks and datasets and the
merge file `Samanyu-dev/squares_in_squares` `53551d7`, is not given: neither the issue
nor the repository states one, and none is retained (the review’s F8; its question 2
asks). Retaining a file grants no licence and relicenses nothing.

## Commands

From `packing/`, with the project interpreter, as in the
[#941 packet](../de-winter-issue941-2026-11-10/README.md#commands) with this packet’s
name; a row on Couzo’s `43f666c` is read from
`resources/web/couzo-43f666c-2026-10-24/source/certificates/best/`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
