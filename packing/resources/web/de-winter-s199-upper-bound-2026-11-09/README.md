# Joost de Winter’s s(199) Certificate at 702c7af

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/702c7af2db04c9b69696455ee3d33883a2935e8a)
at `702c7af2db04c9b69696455ee3d33883a2935e8a` (committed 2026-11-09T21:54:59Z), the head
of `main` when it was cloned, which
[issue #939](https://github.com/jlevy/squares/issues/939) names 9 minutes later.
The commit adds the folder `n199/` and a row of the root README. Its parent, `9bf5d9be`,
is the revision the
[de-winter-upper-bounds-227-229-260-2026-10-17](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
packet retains, and the folders for 227, 229 and 260 are unchanged.

Intake lane L78 (think-2h88) retained the source and replayed the certificate on 9
November 2026, and on 10 November, after #938’s import (lane L76, PR #940) made T-284 the
house at 199, compared it with T-284, measured it and registered it as **T-285, held at
V0/C1** for the owner’s RV-3 (think-ruu2). The house stays T-284, and the case record is
not touched.

## What the Source Claims

- `n199/n199_witness.yaml` states 199 unit squares, each by its centre and the unit
  direction of one edge, every number an exact rational. The side is a fraction with
  denominator 10¹¹⁰. #939 prints it rounded up at 38 places,
  14.61468985328358057514628890087947061619, and its title at 16 places,
  14.6146898532835806.
  - The issue calls this file “the witness format of this project (center-basis,
    rational)”. It follows Witness/v2’s `witness` object, but has no `softschema` block
    and no `claim`, has a `notes` field, and its id `W-n199-de-Winter-locally-optimal`
    has capitals.
  - So this repository’s schema does not admit it, and neither `packing-witness verify`
    nor the `witness-center-basis` reader reads it.
  - `n199/n199_exact.json` states the same packing as `[center_x, center_y, cos, sin]`
    rows, with the side and the coefficients of a quintic.
- **The quintic.** The issue says the side is less than 10⁻⁹⁸ above the real root near
  14.6147 of 62x⁵ − 4426x⁴ + 125017x³ − 1746146x² + 12052670x − 32855154, and the README
  says 1.4 × 10⁻⁹⁹. The issue calls that root the arrangement’s local optimum, by a
  numerical solution of the optimality conditions to 130 digits. The polynomial was
  identified numerically from 108 digits and reproduces the side to 129. Local optimality
  has no formal proof, as the issue says. The source’s README (`n199/README.md`) adds
  that in that solution “all 734 load-bearing or forced contacts close exactly and all
  other gaps stay open”.
- **The construction.** A 172-square core and an L of 27 axis-aligned squares, a row of
  14 and a column of 13: the step s(n + 2⌊s⌋ + 1) ≤ s(n) + 1. The core is the arrangement
  of [#935](https://github.com/jlevy/squares/issues/935) (T-282: Evan Daniel’s packing,
  improved by Doğa Özden), re-optimized to that local optimum, a core side 2.63 × 10⁻¹²
  below T-282’s.
- **The checks.** `verify_exact.py` (Python’s `fractions.Fraction`) checks exact unit
  directions, containment and a separating-axis test on the 481 pairs whose centres are
  closer than √2. It also checks, by an exact sign test, that a root of the quintic lies
  within 10⁻⁹⁸ below the side. The issue says a second script with separate code checked
  the witness file, and that the two share one author, the separating-axis test and
  `Fraction`. Those statements are the author’s; no source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the licence, the root README and the whole of `n199/`,
8 files: 6 retained under [source/](source/) and 2 pinned by digest.

| File | Bytes |
| --- | --- |
| `README.md` | 1,312 |
| `n199/README.md` | 1,896 |
| `n199/SHA256SUMS` | 406; it states the SHA-256 of the five other files of `n199/`, and they match |
| `n199/n199_witness.yaml` | 158,360 |
| `n199/n199_exact.json` | 149,215, stored as deterministic gzip |
| `n199/verify_exact.py` | 2,642, retained as data and never executed here |
| `LICENSE` | 1,072, pinned against the byte-identical copy the October packet retains |
| `n199/n199_record.png` | 115,688, a figure pinned by digest only |

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `f54ad1048`, after PR #940
merged):

- The certificate is below the case’s house, T-284 (#938, Doğa Özden, 20:31Z the same
  evening; Evan Daniel’s packing as Özden improved it), by 2.6345292 × 10⁻¹². That is
  exactly T-282’s side less S − 1, since T-284’s side is T-282’s plus 1. It crosses
  T-284’s 12-place print: 14.614689853284 against 14.614689853287.
- It is below T-174 and T-193, two re-certifications of the former house’s packing
  (T-127), by 2.882 × 10⁻³.
- The
  [ledger of 11 November](../../../campaign/issue-intake/upper-bounds-939-946-20261111/README.md)
  walks it from starts frozen at `f54ad1048` and records it, as a refinement of T-284’s
  packing.

## The Construction

The certificate is the L step on its own core. Squares 1 to 172 lie in
[5 × 10⁻¹⁰¹, S − 1 − 5 × 10⁻¹⁰¹]², and `devtools.construction_checker.write_out` of one
L layer on them, at side S − 1, writes this certificate pose for pose:

- a row of 14 at y = S − ½ from the left wall, as squares 173 to 186;
- a column of 13 at x = S − ½ from the floor, as squares 187 to 199.

That is #938’s L, square for square and in the same order of ids.
[tests/test_upper_bound_reports_l78_1109.py](../../../tests/test_upper_bound_reports_l78_1109.py)
holds it.

## Exact Replay

Two readers were added to `devtools.upper_bound_reports` for this packet:

- `witness-center-basis-bare`, for a centre-basis witness without the schema’s envelope;
- `center-direction-json`, for the JSON’s rows.

Each reads the geometry exactly as `center_basis_json` does, and refuses anything else.
Every read of the certificate holds the two files equal.

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 19,701 pairs a job and route, 35 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes. The least wall clearance
and the least pair gap are both exactly 0: the grid squares touch the walls and each
other.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
1e-30 past it ([receipts/sharp-controls.json](receipts/sharp-controls.json); 138 CPU
seconds), and every control behaved as the module predicts:

- **Wall, pair and near-wall.** The least far-wall clearance, the least pair gap
  (squares 173 and 174 of the top row) and the least near-wall clearance are all 0. So
  the at-contact half of those three controls is the certificate itself, which both
  routes accept. The half 1e-30 past contact is a mutant, which both refuse.
- **Enlarged to a pair.** The core’s near-contacts are dense at 10⁻¹⁰⁰, so no square can
  be enlarged to close one pair alone. The module enlarged square 174 against 173, which
  already touch. Both routes accept it at contact and refuse it 1e-30 past for the wall,
  the overlap and the shape.
- **Enlarged to a wall.** The module enlarged square 48, one of the core’s free squares,
  1.088 × 10⁻³ from its wall. Both routes refuse it at contact for its shape alone, and
  past contact for the wall as well.
- **Duplicate.** Both routes refuse a duplicated square.

The lane wrote down its expectations before either command ran. They held for 9 of the
11 controls; for the two enlargements it had expected different squares.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method. Neither shares code with the author’s `verify_exact.py`,
which was not run. The issue says the certificate was not replayed with this
repository’s checkers.

## The Quintic

Checked exactly by the lane’s test with sympy over Q and sign tests in `Fraction`: the
quintic is irreducible, with three real roots (near 9.670, 14.6147 and 19.065). Exactly
one root r lies in [S − 10⁻⁹⁸, S] (a Sturm count), and the quintic changes sign there.
S lies between 1.36 × 10⁻⁹⁹ and 1.37 × 10⁻⁹⁹ above r, as the README’s 1.4 × 10⁻⁹⁹ says.
The core’s side S − 1 is then 1.36 × 10⁻⁹⁹ above r − 1, a root of the shifted quintic.

## Pose by Pose

`devtools.measure_identity` wrote [measure/identity-n199.json](measure/identity-n199.json)
and [measure/identity-n172-base.json](measure/identity-n172-base.json); a measurement for
credit, which decides nothing.

- **Against T-284.** Nearest centres pair it one to one with T-284’s packing under the
  identity. 84 squares move beyond 10⁻⁹ and none beyond 10⁻³ (largest 1.414 × 10⁻⁴), and
  16 turn by 0.00573 degrees. The L does not move. So it is a refinement of T-284’s
  packing. Against the regularized view at 199, 44 squares move beyond 10⁻³.
- **The 84.** 16 of them are free: no pair or wall touches them. They are the free
  squares of Evan Daniel’s KKT solve below, each moved by about (−10⁻⁴, −10⁻⁴) and turned
  by 10⁻⁴ rad. The other 68 slide along their contacts on the flat motions, each keeping
  a tight pair; 66 keep every pair they had below 10⁻¹² in T-282, and only squares 73 and
  127 lose any. This follows the stage 4 review’s F10 and its `moves.json`. The other 88
  move by less than 10⁻⁹.
- **The base.** Read through `l-base`, the base is T-282’s certificate, pose for pose.

## The Gain Against Padding

`devtools.contraction_margin` contracts a certificate uniformly about the origin to first
contact, boxes it, and decides the contracted packing on both routes. Every receipt is
under [measure/](measure/):

| Certificate (receipt) | 1 − λ\* | Margin | Against | Gain ÷ margin |
| --- | --- | --- | --- | --- |
| T-284 ([contraction-n199.json](measure/contraction-n199.json)) | 0 | 0, the grid pair 173–174 binding | this certificate, 2.634529 × 10⁻¹² | none (the margin is 0) |
| this certificate ([contraction-n199-own.json](measure/contraction-n199-own.json)) | 0 | 0 | — | — |
| T-284’s base, T-282 ([contraction-n172-base.json](measure/contraction-n172-base.json)) | 2.008339 × 10⁻¹³ | 2.533458 × 10⁻¹² | this certificate’s base, 2.634529 × 10⁻¹² | **1.0399** |
| this certificate’s base ([contraction-n172-base-own.json](measure/contraction-n172-base-own.json)) | about 10⁻¹⁰⁰ | 1.361469 × 10⁻⁹⁹ | — | — |
| Evan Daniel’s held solve ([contraction-n172-daniel-held.json](measure/contraction-n172-daniel-held.json)) | 10⁻²⁰ | 1.361469 × 10⁻¹⁹ | this certificate’s base, 1.361469 × 10⁻¹⁹ | **1.0000** |

- **Whole-certificate contraction reads 0** for any certificate built by the L step,
  since its grid squares touch. Its padding is its base’s. The spec
  `l-base:packet:NAME` reads the base: the certificate’s first n squares at its side less
  one, held to `construction_checker.write_out` reproducing the certificate.
- **The gain is 1.0399 of the padding T-284 carries.** Contracting T-282 and writing the
  L on it gives a 199-packing 2.533 × 10⁻¹² below T-284. This certificate is 1.0107 ×
  10⁻¹³ below that, and both round up at 12 places to 14.614689853284.
- **The core is Evan Daniel’s held KKT point.** His regularizer solved T-282’s witness on
  9 November (think-he66), and the record holds that solve unregistered (think-wju3).
  - Its side, printed at 63 places in the run’s retained report, is S − 1 in every
    place.
  - The core gains exactly that certificate’s own padding over it (1.0000).
  - The 88 squares that do not move agree with it within 10⁻⁹, and the other 84 lie on
    its 77 flat motions.
  - The view was regenerated byte for byte from `main`’s T-282 witness by
    `regularize_evand run`, with Git blob `d641e969`, the blob the think-he66 report
    records. It is not retained; the receipts name it by its SHA-256.
- **The base’s own margin is 1.36 × 10⁻⁹⁹**, and the contracted base lies 1.1 × 10⁻¹²⁴
  above r − 1. That is consistent with the source’s local-optimality claim, and is no
  proof of it.

## The Register

- **T-285 records the claim, held at V0/C1, S1**, as T-280 is.
  - Its regularization item names T-284.
  - The replay above is not entered as evidence, and nothing is adopted.
  - Whether a re-certification at the margin its predecessor carries is a new result is
    the owner’s RV-3 (think-ruu2). Its answer settles this entry and the held solve at
    172 alike.
  - The stage 4 review observes (F4) that the gain lies 1.0107 × 10⁻¹³ below the
    contracted predecessor, at its 12-place print and the root’s.
  - Under a rule that counts a re-solve only if its 12-place print falls below the
    predecessor contracted to first contact, through any construction, no certificate of
    this arrangement could count, since its optimum prints as the contracted house does.
  - Under a rule that counts any gain, a gain across the predecessor’s own print, or a
    gain beyond its contraction margin, it counts. A case-by-case judgment of whether the
    4% beyond the margin is padding could go either way.
  - The question and its options are think-ruu2’s (RV-3). The record decides nothing.
- **Nothing at 172 is registered from this packet.** The certificate’s first 172 squares
  at S − 1 prove s(172) ≤ S − 1, 2.63 × 10⁻¹² below T-282. That bound is not claimed here,
  and it is think-wju3’s held solve with less padding. #946 reported the same core a day
  later, 1.36 × 10⁻⁹⁹ lower, and T-286 records it, held alike
  ([de-winter-s172-upper-bound-2026-11-10](../de-winter-s172-upper-bound-2026-11-10/README.md)).

## Stage 4 Review

The stage 4 mathematical review of 11 November 2026
([review-2026-11-11-de-winter-939-946.md](../../../../docs/project/reviews/review-2026-11-11-de-winter-939-946.md),
lane L82, think-o53d) was written in a separate lane, blind to this one until its
findings were frozen. It accepts both #939’s and #946’s certificates, and no finding
blocks.

- **Its checker.** A clean-room checker decides every square, wall and pair by separating
  axes in `Fraction` and by exact clipped areas in `gmpy2.mpq`. It has a self-test of
  1,700 cases and four mutated checkers, and its 21 controls were stated in advance.
- **Its programs and receipts** are in [review/review-2026-11-11/](review/review-2026-11-11/README.md);
  the 172 receipts are in the s172 packet.
- **It agrees with this packet’s receipts.** Its contraction receipts equal them exactly.
- **Mapping.** It is mapped on T-285 and T-286 and on both certificate-report atoms, so
  each entry stands at V0/C1. Its run (`V-de-winter-939-946-review-check`) is not entered
  while the entries are held.
- **F1 and F2** (minor) are answered in the record: the bound is the certificate’s side,
  and #938 is credited for the L step at 199.
- **F10** corrected this README’s account of the 84 moved squares.
- **F11** had the register’s significance rationales state the share neutrally.
- **F12** notes that the float fields of a receipt with margins near 10⁻³¹⁹ fall in
  binary64’s subnormal range (the s172 packet).

### Questions for the Author

The review asks six informational questions. None holds a rung or the issues open.

1. Will #946’s bound be stated as the certificate’s side, or a print at or above it, with
   the root as the asserted optimum (F1)?
2. Will #939 cite #938 for the L step at 199, and give its gain against the house, T-284
   (F2)?
3. The 16 free squares sit at T-282’s positions less about (10⁻⁴, 10⁻⁴), turned by about
   10⁻⁴ rad. Was that chosen, and why?
4. How was the quintic identified from 108 places, and is the 390-place solution an
   independent code path? A derivation from the contact equations would make the closed
   form a theorem about this arrangement.
5. What do the 734 contacts count? The review finds 336 tight pairs at 172, and at 199
   380 tight pairs and 25 grid contacts.
6. Which commit should the record cite for #939, `702c7af2` or `c4e65d0b`? Its files are
   the same at both.

## What Is Not Established

- **The quintic’s root as the local optimum.** The certificate proves s(199) ≤ S, the
  rational side, and nothing about the root. Optimality of any kind, local or global, is
  not replayed here.
- **Human oversight.** No human oversight record is retained.

## Credit and Licence

The packing is Evan Daniel’s (T-257, #845) as Doğa Özden improved it (T-282, #935), with
Özden’s L (#938). The re-solve and the certificate are Joost de Winter’s (Delft
University of Technology), and the issue credits the core arrangement to Daniel and
Özden. The issue says the derivation, local optimization, high-precision solution,
rational certificate, checks and figure were produced with Claude (Anthropic) under his
direction. The core is T-282’s arrangement, which starts from this repository’s
regularized atlas, so the lineage builds on this project.
The bibliography key is **[de Winter s199 upper bound 2026-11-09]**.

Everything here is published under the MIT licence, copyright (c) 2026 Joost de Winter,
by `LICENSE` at the pin, which the root README says covers all files. The licence is
byte-identical to the copy the October packet retains, and is pinned against it.

## Commands

From `packing/`, with the project interpreter. They read the packets and reproduce
anywhere, except two:

- `check-claims` reads the case records as they stood at `main` `f54ad1048`.
- The comparison with the held solve reads its view, which `regularize_evand run`
  regenerates from that commit’s T-282 witness in about a CPU-minute; `VIEW` is its
  `n-172/view-solved.yaml`.

```bash
P=de-winter-s199-upper-bound-2026-11-09
H=ozden-s199-upper-bound-2026-11-09
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 199 "#939=packet:$P" "T-284=packet:$H" \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-199-regularized.yaml.gz' \
  --out resources/web/$P/measure/identity-n199.json
python -m devtools.measure_identity --n 172 "#939=l-base:packet:$P" \
  'T-282=packet:ozden-s172-upper-bound-2026-11-09' "T-284=l-base:packet:$H" \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-172-regularized.yaml.gz' \
  --out resources/web/$P/measure/identity-n172-base.json
python -m devtools.contraction_margin --n 199 "T-284=packet:$H" --against "#939=packet:$P" \
  --out resources/web/$P/measure/contraction-n199.json
python -m devtools.contraction_margin --n 199 "#939=packet:$P" \
  --out resources/web/$P/measure/contraction-n199-own.json
python -m devtools.contraction_margin --n 172 "T-284=l-base:packet:$H" \
  --against "#939=l-base:packet:$P" --out resources/web/$P/measure/contraction-n172-base.json
python -m devtools.contraction_margin --n 172 "#939=l-base:packet:$P" \
  --out resources/web/$P/measure/contraction-n172-base-own.json
python -m devtools.regularize_evand run --run-dir "$TMPDIR/evand" --n 172 --workers 1
python -m devtools.contraction_margin --n 172 "daniel-held=witness-center-basis:$VIEW" \
  --against "#939=l-base:packet:$P" --out resources/web/$P/measure/contraction-n172-daniel-held.json
python -m devtools.measure_identity --n 172 "#939=l-base:packet:$P" \
  "daniel-held=witness-center-basis:$VIEW" \
  --out resources/web/$P/measure/identity-n172-daniel-held.json
```

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/n199/n199_exact.json.gz` | upstream | `b0d1a8dd8ac5588d89f8f6414f3e832da8ca0ab2` | `11bdfa7ad41f65d0ea7460cb50e11bdf724d52031aabf72274bb356c71135d21` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
