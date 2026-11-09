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

This is the intake lane’s first phase (L78, think-2h88). It retains the source and replays
the certificate. The comparison is frozen at `main` `200f2ebc1`, before #938’s import
(lane L76, think-1goz) merged; the register, the evidence and the case are not touched.

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
  says 1.4 × 10⁻⁹⁹. It calls that root the arrangement’s local optimum. The basis is a
  numerical solution of the optimality conditions to 130 digits, in which “all 734
  load-bearing or forced contacts close exactly and all other gaps stay open”. The
  polynomial was identified numerically from 108 digits and reproduces the side to 129.
  Local optimality has no formal proof, as the issue says.
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
(`devtools.upper_bound_reports check-claims`, read from `main` `200f2ebc1`):

- The certificate is below the case’s house, T-127 (Nate Chaoweeraprasit, improved by
  Siddharth Gupta), by 2.882 × 10⁻³.
- It is below the two re-certifications of T-127’s packing pending there, T-174 and
  T-193.
- It is below #938 (Doğa Özden, 20:31Z the same evening), compared by #938’s 12-place
  print, 14.614689853287, since #938’s packet was not on `main`. By the exact sides, it
  is 2.6345292 × 10⁻¹² below #938, whose side is T-282’s plus 1.

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

## What Is Not Established

- **The quintic’s root as the local optimum.** The certificate proves s(199) ≤ S, the
  rational side, and nothing about the root. Optimality of any kind, local or global, is
  not replayed here.
- **The lineage and the measurements for credit.** Identity, contraction margins and the
  comparison with Evan Daniel’s held solve at 172 (think-wju3) were measured in the
  lane’s scratch with the maintained tools. They are written into this packet’s
  `measure/` in the lane’s second phase, once #938’s packet is on `main` to read them
  against.
- **Human oversight.** No human oversight record is retained.

## Credit and Licence

The packing is Evan Daniel’s (T-257, #845) as Doğa Özden improved it (T-282, #935), with
Özden’s L (#938). The re-solve and the certificate are Joost de Winter’s (Delft
University of Technology), and the issue credits the core arrangement to Daniel and
Özden. The issue says the derivation, local optimization, high-precision solution,
rational certificate, checks and figure were produced with Claude (Anthropic) under his
direction. The core is T-282’s arrangement, which starts from this repository’s
regularized atlas, so the lineage builds on this project.
The draft bibliography key is **[de Winter s199 upper bound 2026-11-09]**.

Everything here is published under the MIT licence, copyright (c) 2026 Joost de Winter,
by `LICENSE` at the pin, which the root README says covers all files. The licence is
byte-identical to the copy the October packet retains, and is pinned against it.

## Commands

From `packing/`, with the project interpreter. They read the packet and reproduce
anywhere; `check-claims` reads the case records as they stood at `main` `200f2ebc1`:

```bash
python -m devtools.acquire_source de-winter-s199-upper-bound-2026-11-09 --checkout CHECKOUT
python -m devtools.acquire_source de-winter-s199-upper-bound-2026-11-09 --check
python -m devtools.upper_bound_reports de-winter-s199-upper-bound-2026-11-09 check-claims --write
python -m devtools.upper_bound_reports de-winter-s199-upper-bound-2026-11-09 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports de-winter-s199-upper-bound-2026-11-09 check --replay
python -m devtools.upper_bound_reports de-winter-s199-upper-bound-2026-11-09 sharp-controls
```

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/n199/n199_exact.json.gz` | upstream | `b0d1a8dd8ac5588d89f8f6414f3e832da8ca0ab2` | `11bdfa7ad41f65d0ea7460cb50e11bdf724d52031aabf72274bb356c71135d21` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
