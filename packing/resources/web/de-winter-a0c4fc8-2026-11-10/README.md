# Joost de Winter’s Six Certificates at a0c4fc8

This packet retains the folder `above324_refined/` of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/a0c4fc80db67e9806026921654dce49a155ac31b/above324_refined)
at `a0c4fc80db67e9806026921654dce49a155ac31b` (committed 2026-11-10T15:37:44Z), which
adds six certificates, at 597, 754, 864, 865, 869 and 991, to the sixteen of
[issue #942](https://github.com/jlevy/squares/issues/942). Intake lane L90 (think-cen3)
retained, replayed and measured them on 11 November 2026.

**The report.** The commit has no issue of its own, but
[#942’s addendum](https://github.com/jlevy/squares/issues/942#issuecomment-6772308414),
posted by the author at 16:02:47Z, 25 minutes after the commit, claims all six and names
`a0c4fc8`. So the six have a report: the ledger dates them by the comment and keeps the
commit as each one’s first commit.
Its push was not read, so it may have made them public before the comment; no other
report reached these counts between the commit and the comment, so the verdicts are the
same if the commit is the report instead.
GitHub’s activity log was not readable from this session, so no push time is recorded.

`a0c4fc8` also changes the folder’s `README.md` and `SHA256SUMS` and one line of the
root README; the folder’s other sixteen certificates and `verify_cert.py` are unchanged
since `a9486ed`. No later commit through the head `c4e65d0` changes the folder.
`sha256sum -c SHA256SUMS` passes on all 23 lines at the pin.

## What the Source Claims

- **The sides.** The addendum and the folder’s README print each side rounded up at 10
  places, beside the register value and the best public competition packing the author
  could find. Each new side is below both.
- **The rest.** “Certificates, checker, margin, lineage and AI assistance are as stated
  above”: the
  [#942 packet](../de-winter-issue942-2026-11-10/README.md#what-the-source-claims) gives
  them. Each certificate’s second comment line reads “public competition packing,
  re-optimized”, and the folder’s README says the arrangements are unchanged.
- **Sixteen or twenty-two.** #942 says sixteen of the file’s 1000 packings still had a
  descent direction. The folder’s README at `a0c4fc8`, retained here, says instead that
  following the descent “improved twenty-two packings by at least 1e-6”, and the
  addendum calls its six “the same procedure” (the review’s F7). The record quotes each
  README at the pin it cites; whether the six fell below the threshold at first or came
  from a later run was the review’s question 1 for the author.

Those statements are the author’s; no source program ran here.

## The Author’s Answers

Joost de Winter answered the review’s questions on 11 November 2026, as the
[#942 packet](../de-winter-issue942-2026-11-10/README.md#the-authors-answers) records,
from
[issuecomment-6806342752](https://github.com/jlevy/squares/issues/942#issuecomment-6806342752)
(20:20:02Z). For the six here:

- **A later run.** The six come from a later run than #942’s sixteen, which took the
  next packings on his list after the first; each improved by more than 10⁻⁶.
- **The README’s “at least 1e-6” is wrong** for three of the issue’s sixteen, not for
  these six: 921, 924 and 935 improved by 3.8 × 10⁻⁷, 1.8 × 10⁻⁷ and 2.8 × 10⁻⁷. And at
  least forty of the file’s 1000 packings had a descent direction, not sixteen.
- **The margin.** By his estimate it is 8.4 × 10⁻⁹ at 754; the other five are among the
  eighteen of the 22 he gives at 5.0 × 10⁻⁹ to 6.4 × 10⁻⁹.
- **The `501cb8d` edition.** His commit `501cb8d` (2026-11-11T19:41:30Z) rewrites the
  folder README’s paragraph on the descent runs and its margin sentence to that account,
  and changes no certificate. This packet keeps the folder at `a0c4fc8`, whose README is
  the one quoted above.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the licence, the root README and the whole of `above324_refined/`: 27
files, 9 retained under [source/](source/) and 18 pinned by digest.

| File | Bytes | Kept |
| --- | ---: | --- |
| `above324_refined/n0597.cert`, `n0754.cert`, `n0864.cert`, `n0865.cert`, `n0869.cert`, `n0991.cert` | 66,742 to 133,825; 604,730 in all | retained, each under 1,000 lines |
| `above324_refined/README.md`, `above324_refined/SHA256SUMS` | 3,351 and 1,775 | retained |
| `README.md` | 1,855 | retained |
| the sixteen certificates of `a9486ed` | 70,156 to 132,720 | each pinned against the byte-identical copy the [#942 packet](../de-winter-issue942-2026-11-10/README.md) retains |
| `above324_refined/verify_cert.py` | 2,638 | pinned against the copy the [#941 packet](../de-winter-issue941-2026-11-10/README.md) retains |
| `LICENSE` | 1,072 | pinned against the copy the [de-winter-upper-bounds-227-229-260-2026-10-17](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md) packet retains |

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `8afdabe8f` on 11
November 2026). Every exact side rounds up at 10 places to the side the addendum prints.
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the six rows.

| n | Side, rounded up | Row it supersedes (side) | Below it by |
| ---: | --- | --- | --- |
| 597 | 24.8969258585 | `couzo-issue763-2026-10-23` (24.901150566387) | 4.22 × 10⁻³ |
| 754 | 27.9075316299 | `couzo-43f666c-2026-10-24` (27.920422831462) | 1.29 × 10⁻² |
| 864 | 29.8530288378 | `couzo-43f666c-2026-10-24` (29.873870986621) | 2.08 × 10⁻² |
| 865 | 29.8693054513 | `couzo-43f666c-2026-10-24` (29.883815809125) | 1.45 × 10⁻² |
| 869 | 29.9122235088 | `couzo-issue763-2026-10-23` (29.913238532580) | 1.02 × 10⁻³ |
| 991 | 31.9019684133 | `couzo-43f666c-2026-10-24` (31.934561612655) | 3.26 × 10⁻² |

Each side is also below Göbel’s construction at its count, by 0.124 (597) to 0.654
(991).

## Exact Replay

`devtools.upper_bound_reports certify` decided every certificate and its
duplicate-square and outside-container controls on both maintained routes, each job in
its own child process, two at a time at `nice -n 19`: 18 jobs, 12,455,844 pair
decisions, 1,831.0 route CPU seconds, the longest job 193.9 seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz), one
receipt for all six).
Every positive passed and every control was refused on both routes, and `check` admits
all 18 jobs. The two routes agree on every least clearance: every wall clears by 1.0 ×
10⁻¹⁰ to 1.3 × 10⁻¹⁰ and every pair by 2.0 × 10⁻¹⁰ to 2.8 × 10⁻¹⁰.

**Sharp controls.** `devtools.upper_bound_reports sharp-controls` took each certificate
to exact contact and 10⁻³⁰ past it on both routes, 11 controls a count as stated in
advance on think-cen3 ([receipts/](receipts/), `sharp-controls-nNNN.json`: 66 controls
at 6 counts, 6,854 CPU seconds), and every control behaved as the module predicts.
The side lowered to the extent, the tightest pair closed and every square moved to its
near wall were accepted at contact with margin exactly 0 and refused 10⁻³⁰ past it.
The square enlarged to its pair and the one enlarged to its wall were refused at contact
for their shape alone and past it for the overlap or the wall as well, and the
duplicated square was refused.

The two routes share a reader and the separating-axis method, as the
[#941 packet](../de-winter-issue941-2026-11-10/README.md#exact-replay) says, and the
author’s `verify_cert.py` was not run.
`check --replay` was not run, to save the 0.5 CPU-hours it costs; `check` admits the
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
| 597 | not one to one; 262 squares beyond 0.1 under the best assignment; another arrangement | 4.78 × 10⁻⁹ | 8.84 × 10⁵ |
| 754 | not one to one; 327 squares beyond 0.1 under the best assignment; another arrangement | 1.42 × 10⁻¹¹ | 9.10 × 10⁸ |
| 864 | not one to one; 349 squares beyond 0.1 under the best assignment; another arrangement | 1.63 × 10⁻¹¹ | 1.28 × 10⁹ |
| 865 | not one to one; 243 squares beyond 0.1 under the best assignment; another arrangement | 6.13 × 10⁻¹² | 2.37 × 10⁹ |
| 869 | not one to one; 279 squares beyond 0.1 under the best assignment; another arrangement | 5.64 × 10⁻¹³ | 1.80 × 10⁹ |
| 991 | not one to one; 343 squares beyond 0.1 under the best assignment; another arrangement | 6.80 × 10⁻¹² | 4.80 × 10⁹ |

None of the six is one to one with the row’s packing under any symmetry: each is another
arrangement, 243 to 349 squares beyond a tenth under the best assignment.
Every gain is at least 8.8 × 10⁵ times its row certificate’s padding (at 597), so none
is think-ruu2’s RV-3 material.

## Report Order and the Register

The
[ledger of 11 November for this import](../../../campaign/issue-intake/upper-bounds-941-942-20261111/README.md)
records all six claims.
Each is a current beyond-horizon row of this source, at assurance `verified`, and
supersedes the row it is below.
The rows rest on this replay, `E-de-winter-a0c4fc8-exact-feasibility`, and the stage 4
review’s clean-room run, `E-de-winter-a0c4fc8-review-exact-feasibility`, as the
[#941 packet](../de-winter-issue941-2026-11-10/README.md#stage-4-review) sets out.
These are bounds below the record, which the record does not call the best known
packings (the review’s F9): each arrangement is another holder’s public Kaggle packing,
re-optimized, and the addendum’s own table puts each side 1.2e-06 to 2.2e-04 below the
best public packing it found, a comparison not checked here; Kaggle files no report
brought here may hold smaller ones.
Beyond the corpus no register entry records them.

## What Is Not Established

As in the
[#942 packet](../de-winter-issue942-2026-11-10/README.md#what-is-not-established).

## Credit and Licence

As in the [#942 packet](../de-winter-issue942-2026-11-10/README.md#credit-and-licence):
Joost de Winter for the local re-optimization, after the public Kaggle packings of the
merged file: the names its README credits, with penguin069 and kmmmvs.
The starting packings’ authors are not identified per puzzle, so some may be
Samanyu-dev’s own.
The repository is MIT-licensed, copyright 2026 Joost de Winter.
No licence is stated for the Kaggle starting packings: public Kaggle notebooks default
to Apache 2.0, and none was traced per packing (the review’s F8 and the author’s
answer).
Retaining a file grants no licence and relicenses nothing.

## Commands

As in the [#941 packet](../de-winter-issue941-2026-11-10/README.md#commands), with this
packet’s name.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
