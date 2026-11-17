# Doğa Özden’s s(292) Certificate at dec930b

This packet retains
[kenaznia-doga/s292-upper-bound](https://github.com/kenaznia-doga/s292-upper-bound/tree/dec930bdaa5f58077af6c05bc13c0fca0a58a3ed)
at `dec930bdaa5f58077af6c05bc13c0fca0a58a3ed` (committed 2026-11-16T15:27:16Z), the
repository’s one commit, which [issue #1005](https://github.com/jlevy/squares/issues/1005)
names 22 seconds later.
Doğa Özden’s AI agent, which uses the account kenaznia-doga, prepared and posted both on
his behalf. The lane fetched the repository at 01:35Z on 17 November, when
`git ls-remote` read the same head; #1005 had no comment and no edit then.

Intake lane c-import-1005-1117 (think-qag8) retained it, replayed it and measured it on
17 November 2026. It is the first of two reports at 292 on 16 November: Joost de
Winter’s [#1006](https://github.com/jlevy/squares/issues/1006), 11 minutes 38 seconds
later, is below it, and the
[de-winter-s292-upper-bound-2026-11-16 packet](../de-winter-s292-upper-bound-2026-11-16/README.md)
retains it.

## What the Source Claims

- `n-292-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational
  scalars, 292 squares), bounds s(292) by its exact side, a fraction whose 16-place
  ceiling is 17.5901042186818347. #1005 prints its 12-place ceiling, 17.590104218682,
  and says it is 0.00127392681586354 below the record at `f9ddfeee`, 17.5913781454976982
  (T-146), relative 7.24 × 10⁻⁵.
  The issue and README also print the exact side to 43 places before an ellipsis,
  17.5901042186818346195918844579867374561574315, and `sqcheck-292.txt` prints it rounded
  up at 15 places, 17.590104218681835.
  It claims an upper bound only: no optimality, KKT or rigidity claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `f9ddfeee` from the lab’s decimal pose,
  `n-292-decimal-pose.yaml`, which the witness’s `source.path` names, with
  `center_dilation: '1'` and no dilation.
  The issue says `sqcheck.py` certified the decimal pose in interval arithmetic at its own
  side, pair margin at least 2.02 × 10⁻¹³ and wall margin at least 1.02 × 10⁻¹³, and that
  translating the least corner coordinates to zero and taking the greatest corner extent
  as the side lowered the side by about 2.0 × 10⁻¹³, which it calls normalization and not
  part of the gain.
- `n292-witness.json` is the same witness as JSON. `verify-292.txt` is the author’s
  unmodified run of this repository’s `packing-witness verify` at `f9ddfeee` (VERIFIED,
  exact-algebraic over Q, 42,486 pairs), and `checks/registry.json` reports the same
  run’s least best pair gap and its least wall clearance, 0.
  `sqcheck-292.txt` is the author’s run of `verifier/sqcheck.py`, an exact checker the
  source says was implemented separately (VALID, exact rational); `checks/exact.json` and
  `checks/interval.json` are its JSON reports on the exact witness and on the decimal
  pose, and `checks/promote.json` the promotion’s report. The issue says promotion shares
  code with `packing-witness verify` and that `sqcheck.py` is separate.
  Those statements are the author’s; no source program ran here.
- **Method.** The issue says the packing is an original AI-run design of the lab’s
  Claude Sonnet 5.5 director `sonnear`, not a donor or transplant start or a public
  recovery, and that no registry packing was used as a seed. A column-band designer
  (`cscan`/`coldp`: tilted squares in columns across a diagonal band, axis-parallel
  squares on wall-anchored staircase lattices, an exact dynamic programme over the
  columns) and one quench with Evan Daniel’s ALM+SLP fq optimizer
  ([evand/square-packing](https://github.com/evand/square-packing), `search/packer`, MIT)
  made the director’s own earlier designs (jobs `s2h292b` and `s3h292a`). A new operator
  the director wrote, `segkick`, then improved them: it rigidly re-angles a contiguous
  tilted segment, loosens and quenches again, and hill-climbs a pool (mode `two`, 25,512
  moves, 1,658 kept). `hit-n292-83-99956.txt` is the filed hit, of job `s5k292t` in
  batch `s5` (rng 83, moves segment 10 by +2.45 degrees and segment 9 by +7.2 degrees),
  final decimal side 17.59010421868203977; `hit-n292-83-99956.json` records that
  metadata. The README says all 114 distinct hit poses of batch `s5` below the record
  are one rigid basin.
- **Identity, as the source measures it.** Against the record’s packing matched up to the
  square’s eight symmetries, 203 of 292 centres move by more than 0.001, 115 by more than
  0.05 (largest 0.996), and 77 squares retilt by more than 1 degree; the packing has 64
  tilted squares against the record’s 49.
- **Other public values.** The issue discloses first a side-only Kaggle leaderboard
  entry at 292, 17.589053943368 (Cats and boxes, 29 October, from a cache of 9 November),
  0.001050 below this side, which this packing does not beat and which states no packing;
  and it quotes the best public Kaggle packing it found, 17.591378145514 (kirilltym, data
  of 11 November), above this side.
- **Credit.** It asks that Doğa Özden be recorded as `improved_by` for this new
  arrangement, the record staying credited to Nate Chaoweeraprasit (itsnaka), improved by
  Evan Daniel, and Evan Daniel credited for the optimizer. Search, checks and filing were
  AI-assisted throughout.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the whole tree, 18 files, 2,100,434 bytes: 13 retained
under [source/](source/), `n292-witness.json` stored as deterministic gzip by the
archive’s rule, and five pinned only. `verifier/sqcheck.py` and `verifier/README.md` are
byte-identical to the copies the
[ozden-s232-upper-bound-2026-11-09](../ozden-s232-upper-bound-2026-11-09/README.md) and
[ozden-s299-upper-bound-2026-11-03](../ozden-s299-upper-bound-2026-11-03/README.md)
packets retain, and `LICENSE-evand-square-packing.txt` to the `LICENSE` the
[issue 845 packet](../evand-issue845-2026-10-29/README.md) retains; each is pinned against
its copy. The two comparison figures under `records/` are pinned by digest only.
`sqcheck.py` is retained as data and was never run here.
The certificate has the SHA-256 the issue and the README state, `90a0e306…8a8a`.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `f9ddfeeef`:

| Compared with | Side | Below it by |
| --- | --- | --- |
| T-146, Nate Chaoweeraprasit’s packing as Evan Daniel improved it, the house in both lanes | 17.5913781454976982 | 1.27393 × 10⁻³ |
| T-193 at 292 (#639), Evan Daniel’s exact contact of that packing, pending adoption | 17.5913781454976981594… | 1.27393 × 10⁻³ |

T-193’s side at 292 lies 1.76 × 10⁻¹⁹ below T-146’s and is staged for want of a writer
(think-ot5c). The lower bounds at 292 lie below the side.

## Report Order

The
[ledger of 17 November for this lane](../../../campaign/issue-intake/upper-bounds-1005-1007-20261117/README.md)
walks both reports at 292 in the order they reached this repository, from a start frozen
on `main` `f9ddfeeef`. #1005 (15:27:38Z) is first and is recorded as a new packing below
the record; #1006 (15:39:16Z), 8.7776 × 10⁻⁵ below it, is recorded after it. This claim
record names no later report, since #1006 came after it; the second packet’s record names
this one. The side-only leaderboard entry both issues quote states no packing and is
context only.

## Pose by Pose

`devtools.measure_identity` wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.
No symmetry of the box pairs the certificate one to one with T-146’s packing by nearest
centres, and the house witness and its regularized view measure as T-146.
The optimal assignment, best under symmetry 3, moves 290 squares beyond 10⁻³, 127
beyond 0.01 and 81 beyond 0.1 (largest 0.907709), and turns 109 squares by more than
10⁻⁶ radians, by up to 41 degrees; aligned by box centres, 77 squares turn by more than a
degree and 26 reverse their tilt.
Tilted beyond a degree: 64 here, at 40.70 to 44.80 degrees, 59 one way and 5 the other,
against T-146’s 49, at 35.68 to 40.97 degrees, all the other way.
So it is a new arrangement relative to the record’s packing, as the issue says.
The issue’s own counts (203 beyond 0.001, 115 beyond 0.05, largest 0.996) use another
placement of the record’s packing, which it does not name; the receipt’s are under the
least total move, and its 77 retilted beyond a degree and 64 against 49 tilted squares
are the issue’s.

## Exact Replay

The checks below were planned before any of them ran: the expected verdict of every gross
and sharp control of this certificate and of de Winter’s three was written down at
01:36:23Z on 17 November (SHA-256
`1f61b6721c29d0750e89572e6d814d2940acc0b63f961d0e80663b51d41d6d28`, recorded on the bead),
with two branches stated in advance, a square that touches its wall exactly and a pair
that touches exactly. Before the plan was hashed only `sha256sum` had read the
certificate.

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 254,916 pair decisions, 91.9 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.0187 × 10⁻¹³, squares 154 and 155, the margin the issue reports for the decimal
pose. `check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it on both routes ([receipts/sharp-controls.json](receipts/sharp-controls.json),
347 CPU seconds), and all 11 came out as stated, the branch for a touching square taken:

- **Wall, pair and near-wall.** The box lowered to the extent (by 0), the tightest pair
  closed (square 155 toward 154, by its gap) and every square moved toward its near wall
  by the least near-wall clearance, 0: each accepted at exact contact and refused 10⁻³⁰
  past it.
- **Enlarged to a pair.** Square 155, enlarged against 154, refused at contact for its
  shape alone, and past it for the overlap as well.
- **Enlarged to a wall.** Square 72, already at its wall, grown by 0: accepted at
  contact, and refused 10⁻³⁰ past it for the wall and its shape.
- **Duplicate.** A duplicated square is refused.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share this repository’s corner-witness reader (certificate parsing and
half-angle conversion), `Fraction` arithmetic and the separating-axis method.
The first is the `packing-witness verify` the author ran, from the package whose
promotion made the coordinates, so on that route the replay is reproduced with the
producer’s code; the independent rational corner checker shares no geometry or
verification code with `sqpack.witness` or `sqpack.verify`, and the replay’s independent
re-implementation rests on it. Neither route is the author’s `sqcheck.py`, which was not
run.

## The Gain Against Padding

`devtools.contraction_margin` contracted each certificate uniformly about the origin to
first contact and boxed it, each contracted packing decided on both maintained routes:

- **The house**, T-146 at 292: margin 1.7591 × 10⁻¹⁹ (1 − λ\* = 10⁻²⁰, squares 68 and 69)
  ([measure/contraction-n292.json](measure/contraction-n292.json)), so the gain,
  1.2739 × 10⁻³, about 7.2 × 10¹⁵ times it, lies outside the house’s padding and RV-3
  (think-ruu2) does not reach it. T-193’s 292 is that contraction’s exact contact.
- **This certificate**: margin 3.3490 × 10⁻¹² (1 − λ\* about 2.0187 × 10⁻¹³, squares 154
  and 155) ([measure/contraction-n292-own.json](measure/contraction-n292-own.json)).
  Contracted, it would be a square that much smaller, which nobody reported and which is
  not registered (RV-3).

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json) is `devtools.l_step_scan` with this
side stood in for 292’s ceiling. It finds main’s L-step and monotonicity consequences
less one: the L step from 259, which reaches 292 1.76 × 10⁻¹⁹ below T-146 on `main`, is
above this side. The L step from this side lands at 327, beyond the corpus, and no bound
carries to another count.

## Stage 4 Review

The blind stage 4 review of this certificate is lane R1’s (think-p3g8), with de Winter’s
three; this lane has not read it. Until it lands and is mapped, the result stands at the
replay’s rungs, and nothing here is its finding.

## What Is Not Established

- **The method’s steps**: the column-band designer, the earlier designs and `segkick` are
  described, not retained, and neither this lane nor any review rebuilt them; the lineage
  beyond the measurements above is the issue’s.
- **Local optimality, rigidity or KKT**: not claimed by the source.
- **Human oversight**: no record is retained.

## Credit and Licence

The packing is Doğa Özden’s, found by his lab’s AI-run search, a new arrangement relative
to the record’s packing at 292, with Evan Daniel’s optimizer credited. The issue asks
for Özden as `improved_by`; since no registry packing seeded it and the measurement finds
a new arrangement, the record credits him as its finder, as for his #983 at 228, and his
lab’s earlier designs as what it continues. The record credits people, not AI agents
([attribution.md](../../../../attribution.md)), and states the assistance in the source’s
words. The bibliography key is **[Özden s292 upper bound 2026-11-16]**.

`LICENSE.md` at the pin licenses the witness, data and text under CC BY 4.0 and
`sqcheck.py` under MIT, copyright 2026 Doğa Özden, byte-identical to the lab’s earlier
repositories’ `LICENSE.md`. `LICENSE-evand-square-packing.txt` is Evan Daniel’s MIT notice
for the quench code.

## Commands

From `packing/`, with the project interpreter:

```bash
P=ozden-s292-upper-bound-2026-11-16
M=resources/web/$P/measure
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 292 "OZDEN=packet:$P" \
  'T-146=packet:evand-regularized-2026-10-10' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-292-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-292.yaml' --out $M/identity.json
python -m devtools.contraction_margin --n 292 'T-146=packet:evand-regularized-2026-10-10' \
  --against "ozden-1005=packet:$P" --out $M/contraction-n292.json
python -m devtools.contraction_margin --n 292 "ozden-1005=packet:$P" \
  --out $M/contraction-n292-own.json
python -m devtools.l_step_scan --with 292=S292 --out $M/l-step-scan.json
```

In the last command `S292` is the `exact_side` in the packet’s claim record.

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/n292-witness.json.gz` | upstream | `cbbf0b707e619bd30b4415dcd0f57b7844385204` | `07b86d44562acf8cd3bbff45ed2f7e6a9573af2f099009cfa1bf320fdfcbd720` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
