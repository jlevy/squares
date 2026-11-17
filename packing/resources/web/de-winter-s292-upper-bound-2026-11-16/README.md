# Joost de Winter’s s(292) Certificate at 796ff3b

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/796ff3b76e7816f9df24bf4f6ef0bb3b9cacef24),
a watched repository, at `796ff3b76e7816f9df24bf4f6ef0bb3b9cacef24` (committed
2026-11-16T15:37:03Z, “Add a packing of 292 unit squares with side 17.590016442847”), the
commit [issue #1006](https://github.com/jlevy/squares/issues/1006) names 133 seconds
later. The lane fetched the repository at 01:35Z on 17 November, when `git ls-remote`
read the head as `d02237a`. The next commit, `fe13d47`, adds only `n292/REGISTRATION.md`,
the issue’s text in the registration template’s form, and `n292/SHA256SUMS`, whose
digests match this pin’s files; `853b92e` and `d02237a` add the 262 and 295 folders,
which the
[de-winter-upper-bounds-262-295-2026-11-16 packet](../de-winter-upper-bounds-262-295-2026-11-16/README.md)
retains, and leave `n292/` unchanged.

Intake lane c-import-1005-1117 (think-qag8) retained it, replayed it and measured it on
17 November 2026. It is the second of two reports at 292 that day: Doğa Özden’s
[#1005](https://github.com/jlevy/squares/issues/1005), 11 minutes 38 seconds earlier,
which the
[ozden-s292-upper-bound-2026-11-16 packet](../ozden-s292-upper-bound-2026-11-16/README.md)
retains, lies 8.7776 × 10⁻⁵ above it.

## What the Source Claims

- `n292/n292_exact.json` states 292 unit squares as centre and unit edge direction rows
  of exact rationals, with the side
  33872522175917279266554668306659248043633029180856810473/1925667453806884053962316529711800854170000000000000000.
  #1006 and the root README round it up at 12 places as 17.590016442847, and
  `n292/README.md` prints 17.5900164428464147126481796, rounded up at 25 places.
  `n292/n292_witness.yaml` is the same packing as a corner Witness/v2 of rationals.
  The issue names the record’s 17.5913781454976982 (T-146) at `f9ddfeeef` and the gain,
  0.00136, and says later commits leave these files unchanged.
- **Construction.** One continuous ribbon of 59 squares, tilted by 40 to 42 degrees,
  runs along the diagonal; the other 233 squares are axis-aligned in the two triangular
  regions beside it. The ribbon extends the 37-square ribbon of a packing of 146 squares
  with side 12.583782190152, which the issue says the record credits to David W.
  Cantrell (2025): that ribbon repeats after a shift of (5, 5), and two copies, at (0, 0)
  and (5, 5), share 15 squares and form the ribbon of 59. The coordinates of the 146
  packing came from a public Kaggle notebook (sigmaborov, “Squares in Squares: certified
  contact polish”, Apache License 2.0, as included in areebbb’s “merge 28” notebook). An
  integer program placed the axis-aligned squares, a numerical optimization of all 292
  followed, and the result was rounded to exact rationals.
- **Checkers.** `verify_exact.py` (separating axes) and `check_area.py` (the area of each
  close pair’s clipped intersection), both `fractions.Fraction` and the standard library
  only; the issue says each reports 292 squares and 668 close pairs, that this
  repository’s `check_rational_witness_independent.py` reports “VERIFIED: 292 squares,
  42486 pairs” on the witness, and that the witness validates against this repository’s
  schema. They have one author and read one input file, and share no code.
  Those statements are the author’s; no source program ran here.
- **Not done.** A linear program over all 292 squares, every contact linearized, found no
  first-order improvement, a test of one set of contacts; the certificate keeps a smallest
  gap of 3 × 10⁻¹², so an exact solution of the contact equations would be smaller by an
  amount of that order; no local or global optimality is proved. The issue quotes the
  Kaggle competition’s per-team table (Samanyu-dev/squares_in_squares, 8 November 2026),
  17.589053943368 at 292 for the team “Cats and boxes”, with no public packing, and a
  public merged submission (bestbryant/claude_code_squaresinsquares, 16 November 2026),
  17.591378147172.
- **Credit and AI assistance.** It asks for credit to Joost de Winter, Delft University
  of Technology, as an extension of Cantrell’s ribbon. The construction and the search
  were run with Gemini Carbon (Google); the checking, the witness file, the figure and the
  comparison with other values were produced with Claude Fable 5.2 (Anthropic), both
  under his direction.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the licence, the root README and the whole of `n292/`,
8 files: 4 retained under [source/](source/), `n292/n292_exact.json` stored as
deterministic gzip, and four pinned only. `LICENSE` is byte-identical to the copy the
[de-winter-upper-bounds-227-229-260-2026-10-17](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
packet retains, and `n292/verify_exact.py` and `n292/check_area.py` to the copies the
[de-winter-s90-64d5ee7-2026-11-15](../de-winter-s90-64d5ee7-2026-11-15/README.md) packet
retains; each is pinned against its copy and was never run here. The figure is pinned by
digest only. The certificate and the witness have the SHA-256 digests the folder’s
`SHA256SUMS` lists at `fe13d47`.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `f9ddfeeef`. `center-direction-json` reads the certificate, and
`witness-corners-opposite` its corner twin, which lists each square’s corners from the
vertex opposite the one `witness-corners` starts from, as at #997; the two state the
same packing exactly.

| Compared with | Side | Below it by |
| --- | --- | --- |
| T-146, Nate Chaoweeraprasit’s packing as Evan Daniel improved it, the house in both lanes | 17.5913781454976982 | 1.36170 × 10⁻³ |
| T-193 at 292 (#639), its exact contact, pending adoption | 17.5913781454976981594… | 1.36170 × 10⁻³ |
| #1005, Doğa Özden’s certificate, filed before it | 17.5901042186818346… | 8.7776 × 10⁻⁵ |

## Report Order

The
[ledger of 17 November for this lane](../../../campaign/issue-intake/upper-bounds-1005-1007-20261117/README.md)
walks #1005 (15:27:38Z) and then #1006 (15:39:16Z) at 292 and records both: #1005 below
the record, and this claim below #1005. The first commits keep the order, `dec930b` at
15:27:16Z before `796ff3b` at 15:37:03Z.

## Pose by Pose

`devtools.measure_identity` wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **Against T-146.** No symmetry of the box pairs the two one to one by nearest
  centres, and the house witness and its regularized view measure as T-146. The optimal
  assignment, best under symmetry 6, moves 290 squares beyond 10⁻³, 119 beyond 0.01 and
  69 beyond 0.1 (largest 0.927764); aligned by box centres, 49 squares turn by more than
  a degree and none reverses its tilt. Tilted beyond a degree: 59 here, at 39.82 to 42.40
  degrees, all one way, against T-146’s 49 at 35.68 to 40.97 degrees the other way, as the
  issue’s one ribbon against two blocks says.
- **Against #1005’s packing.** No symmetry pairs them one to one either; the optimal
  assignment, best under symmetry 2, moves 156 squares beyond 10⁻³ and 44 beyond 0.1
  (largest 0.897925), and 35 tilted squares pair with tilted squares of the same sign.
  So it is a new arrangement relative to the record’s packing and to #1005’s.
- **Cantrell’s ribbon** is in a packing of another count, which the measurement cannot
  pair. The side the issue names for that packing, 12.583782190152, is the record’s house
  at 146 rounded up at 12 places, [Daniel n146 2026-10-14], which the case’s lanes credit
  to Evan Daniel; the case’s prose still names Cantrell (2025), the Kingbird catalogue’s
  earlier packing at 12.60090777851301. Whether sigmaborov’s coordinates are Daniel’s
  packing was not measured: the notebook was not read.

## Exact Replay

The checks below were planned before any of them ran, in the plan the
[#1005 packet](../ozden-s292-upper-bound-2026-11-16/README.md#exact-replay) describes
(SHA-256 `1f61b672…6d28`, 01:36:23Z on 17 November).

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes: 3 jobs, 254,916 pair
decisions, 34.41 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 3.0312 × 10⁻¹² (squares 278 and 279), the smallest gap the issue states.
`check --replay` decided the three jobs again.

`sharp-controls` took the certificate to exact contact and 10⁻³⁰ past it on both routes
([receipts/sharp-controls.json](receipts/sharp-controls.json), 128 CPU seconds), and all
11 came out as stated, the branch for a touching square taken: the box lowered by 0, the
tightest pair closed (279 toward 278) and every square moved toward its near wall by 0,
each accepted at contact and refused 10⁻³⁰ past it; square 279 enlarged to 278 refused at
contact for its shape alone; square 71, at its wall, grown by 0 and accepted; both
refused past contact for the overlap or the wall as well; and a duplicated square
refused. The two routes share what the
[#1005 packet’s README](../ozden-s292-upper-bound-2026-11-16/README.md#exact-replay)
says they share; neither is the author’s code, and neither shares code with it.

## The Gain Against Padding

`devtools.contraction_margin`, each contracted packing decided on both routes:

- **The house**, T-146: margin 1.7591 × 10⁻¹⁹ (squares 68 and 69)
  ([measure/contraction-n292.json](measure/contraction-n292.json)); the gain on it,
  1.3617 × 10⁻³, lies wholly outside it.
- **#1005’s certificate**: margin 3.3490 × 10⁻¹² (squares 154 and 155)
  ([measure/contraction-n292-1005.json](measure/contraction-n292-1005.json)); the step
  from it, 8.7776 × 10⁻⁵, is about 2.6 × 10⁷ times that, so RV-3 (think-ruu2) reaches
  neither comparison.
- **This certificate**: margin 5.0288 × 10⁻¹¹ (1 − λ\* about 3.0312 × 10⁻¹², squares 278
  and 279) ([measure/contraction-n292-own.json](measure/contraction-n292-own.json)), the
  order of the issue’s estimate of what an exact contact solution would gain; that side
  is not registered.

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json), with this side stood in for 292’s
ceiling, finds main’s consequences less the L step from 259 to 292, which this side is
below. The L step from 292 lands at 327, beyond the corpus; no bound carries.

## Stage 4 Review

The blind stage 4 review is lane R1’s (think-p3g8); this lane has not read it.

## What Is Not Established

- **The search**: the integer program and the optimization are described, not retained;
  the lineage beyond the measurements above is the issue’s.
- **Local optimality, rigidity or KKT**: the linear program’s statement is the author’s
  and was not replayed.
- **Human oversight**: no record is retained.

## Credit and Licence

The packing is Joost de Winter’s, a new arrangement at 292 whose ribbon extends David W.
Cantrell’s, as the issue says. The record credits people, not AI agents
([attribution.md](../../../../attribution.md)), and states the assistance in the source’s
words. The bibliography key is **[de Winter s292 upper bound 2026-11-16]**.
`LICENSE` at the pin is de Winter’s MIT licence, and the root README says all files are
released under it. The sigmaborov notebook, Apache License 2.0 by the issue, is not in
the repository and not retained here.

## Commands

From `packing/`, with the project interpreter:

```bash
P=de-winter-s292-upper-bound-2026-11-16
O=ozden-s292-upper-bound-2026-11-16
M=resources/web/$P/measure
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 292 "DEWINTER=packet:$P" \
  'T-146=packet:evand-regularized-2026-10-10' "OZDEN-1005=packet:$O" \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-292-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-292.yaml' --out $M/identity.json
python -m devtools.contraction_margin --n 292 'T-146=packet:evand-regularized-2026-10-10' \
  --against "de-winter-1006=packet:$P" --out $M/contraction-n292.json
python -m devtools.contraction_margin --n 292 "ozden-1005=packet:$O" \
  --against "de-winter-1006=packet:$P" --out $M/contraction-n292-1005.json
python -m devtools.contraction_margin --n 292 "de-winter-1006=packet:$P" \
  --out $M/contraction-n292-own.json
python -m devtools.l_step_scan --with 292=S292 --out $M/l-step-scan.json
```

In the last command `S292` is the `exact_side` in the packet’s claim record.

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/n292/n292_exact.json.gz` | upstream | `eeac012bc478d689354cb43deee800df4f2dfebd` | `3d6fb90c9b79bc9dee984ec0e4b6ecc89bb1306afb266d0b75dcecea4a972b4a` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
