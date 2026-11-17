# Joost de Winter’s s(262) and s(295) Certificates at 853b92e

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/853b92ee2236f418160782dd2871d38ea75271a4),
a watched repository, at `853b92ee2236f418160782dd2871d38ea75271a4` (committed
2026-11-16T21:26:15Z, “Add packings of 262 and 295 unit squares with sides
16.699693441904 and 17.699693441716”), the commit
[issue #1007](https://github.com/jlevy/squares/issues/1007) names 132 seconds later. The
lane fetched the repository at 01:35Z on 17 November, when `git ls-remote` read the head
as `d02237a` (21:26:39Z), which adds only `REGISTRATION.md` to each folder and a line for
it to the folder’s `SHA256SUMS`; every file retained here has the same blob at the pin and
the head.

Intake lane c-import-1005-1117 (think-qag8) retained it, replayed it and measured it on
17 November 2026. No other report reached 262 or 295 before it; Polkovskyi’s #1009,
filed two hours later and claiming both counts, is walked by its own ledger.

## What the Source Claims

- `n262/n262_exact.json` and `n295/n295_exact.json` state 262 and 295 unit squares as
  centre and unit edge direction rows of exact rationals, with the sides
  166996934419035177/10¹⁶ and 35399386883430443/(2 × 10¹⁵). #1007 and the root README
  round them up at 12 places as 16.699693441904 and 17.699693441716; the folders’
  READMEs print them at 25 places, 16.6996934419035177 and 17.6996934417152215 followed by
  zeros. Each folder’s `n…_witness.yaml` is the same packing as a corner Witness/v2 of
  rationals.
- **Against the record**, the issue names the values at `f9ddfeeef`, 16.70710678118655
  (16 + √2/2) at 262 and 17.70423279073603036 ((22 + 22√2)/3) at 295, and the gains, 0.00741
  and 0.00454, and says a separately written exact checker compared each side with the
  irrational record side in exact arithmetic: 2(s − 16)² < 1 at 262 and
  (3s − 22)² < 968 at 295.
- **Construction.** A band of 72 squares, tilted by 25 to 30 degrees and arranged 4 wide
  and 18 long, runs along the diagonal, built from a closed-form layout; the other squares
  are axis-aligned, 190 at 262 and 223 at 295. An integer program placed them, a numerical
  optimization followed, and the result was rounded to exact rationals. No coordinates of
  other packings were used. The issue says the 295 packing is the 262 packing with an
  L-shaped border of 33 axis-aligned squares, so its side is larger by exactly 1.
- **Checkers.** `verify_exact.py` and `check_area.py` in each folder, as at #1006; the
  issue says they report 558 and 626 close pairs, that this repository’s
  `check_rational_witness_independent.py` reports “VERIFIED: 262 squares, 34191 pairs” and
  “VERIFIED: 295 squares, 43365 pairs”, and that both witnesses validate against this
  repository’s schema. Those statements are the author’s; no source program ran here.
- **Not done.** No local optimality test; the packings show small gaps, so a further
  small reduction is likely possible; no local or global optimality is proved.
- **Credit and AI assistance.** It asks for credit to Joost de Winter, Delft University
  of Technology. The construction, the search and the rational certificates were produced
  with Gemini Carbon (Google), and the conversion to the witness format and the checks
  were run with Claude (Anthropic), both under his direction.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the licence, the root README and the whole of `n262/`
and `n295/`, 16 files: 9 retained under [source/](source/), the two certificates stored as
deterministic gzip, and seven pinned only. `LICENSE` is byte-identical to the copy the
[de-winter-upper-bounds-227-229-260-2026-10-17](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
packet retains, and both folders’ `verify_exact.py` and `check_area.py` to the copies the
[de-winter-s90-64d5ee7-2026-11-15](../de-winter-s90-64d5ee7-2026-11-15/README.md) packet
retains; each is pinned against its copy and was never run here. The figures are pinned
by digest only. Every line of each folder’s `SHA256SUMS` at the pin matches its file.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `f9ddfeeef`. `center-direction-json` reads each certificate and `witness-corners`
its corner twin, which here lists each square’s corners from the vertex
`witness-corners` starts from, not the opposite one as at #997 and #1006; each pair
states the same packing exactly.

| n | Side, 12 places | House | Below it by |
| ---: | --- | --- | --- |
| 262 | 16.699693441904 | 16 + √2/2 in the Kingbird catalogue’s print, verified by T-155’s rational ceiling 16.707106781186547524567915429917 | 7.41334 × 10⁻³ |
| 295 | 17.699693441716 | T-193, (22 + 22√2)/3, Ryan Xu’s packing as Evan Daniel and PingYou Ltd improved it | 4.53935 × 10⁻³ |

The 295 house is algebraic: the claim record reads it from the derived number-field fact
of the [evand-exact-cur-2026-10-16 packet](../evand-exact-cur-2026-10-16/README.md), and
decides the relation by an exact sign, with the difference enclosed to within a part in
a million. No register bound is pending adoption at either count, and the lower bounds lie
below both sides.

## Report Order

The
[ledger of 17 November for this lane](../../../campaign/issue-intake/upper-bounds-1005-1007-20261117/README.md)
records #1007 at 262 and at 295 as new packings, the only reports there in this walk.

## Pose by Pose

`devtools.measure_identity` wrote the `identity-nNNN.json` receipts under
[measure/](measure/). A measurement for credit; it decides nothing.

- **262**, against T-155’s exact view of the house’s packing: no symmetry pairs them one
  to one by nearest centres; the optimal assignment moves 261 squares beyond 10⁻³, 91
  beyond 0.01 and 78 beyond 0.1 (largest 0.897603). 72 squares are tilted beyond a
  degree, at 24.94 to 29.73 degrees, all one way, against the house’s 20 at 45 degrees.
- **295**, against T-146’s packing at 295, the house’s 45-degree arrangement, which T-193
  states at its exact contact: no symmetry pairs them one to one; the optimal assignment
  moves 292 squares beyond 10⁻³, 220 beyond 0.01 and 209 beyond 0.1 (largest 1.11514).
  The same 72 tilted squares, against T-146’s 160 at 45 degrees.
- **295 against 262.** The side at 295 is 1 − 1.883 × 10⁻¹⁰ above the side at 262, not
  1 above it, so the 295 certificate is below the L step on the 262 one, and
  `measure_identity`’s `l-base` reading, which rebuilds one L step on a certificate’s
  first squares, refuses it as no such step. The two share the band, by the issue and by
  their tilt ranges, equal to twelve places; the squares were not paired across counts.

So each is a new arrangement relative to the record’s packing, as the issue says.

## Exact Replay

The checks below were planned before any of them ran, in the plan the
[#1005 packet](../ozden-s292-upper-bound-2026-11-16/README.md#exact-replay) describes
(SHA-256 `1f61b672…6d28`, 01:36:23Z on 17 November).

`devtools.upper_bound_reports certify` decided both certificates and their
duplicate-square and outside-container controls on both maintained routes: 6 jobs,
465,336 pair decisions, 33.09 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). Both
positives passed and every control was refused on both routes.
Squares touch the box in both, a least wall clearance of exactly 0, and every pair clears
by at least 4.4768 × 10⁻¹² at 262 and 1.5200 × 10⁻¹² at 295.
`check --replay` decided the six jobs again.

`sharp-controls` took each certificate to exact contact and 10⁻³⁰ past it on both routes
([receipts/sharp-controls-n262.json](receipts/sharp-controls-n262.json) and
[receipts/sharp-controls-n295.json](receipts/sharp-controls-n295.json)), and all 22 came
out as stated, the branch for a touching square taken at both counts (59 and 71 CPU
seconds). At each the box lowered by 0, the tightest pair closed (square 37 toward 33 at
262, 56 toward 55 at 295) and every square moved toward its near wall by 0 were accepted
at contact and refused 10⁻³⁰ past it; the pair’s square enlarged to its partner was
refused at contact for its shape alone; square 81 at 262 and square 77 at 295, each at
its wall, grew by 0 and were accepted; each was refused past contact for the overlap or
the wall as well; and a duplicated square was refused.
The two routes share what the
[#1005 packet’s README](../ozden-s292-upper-bound-2026-11-16/README.md#exact-replay)
says they share; neither is the author’s code, and neither shares code with it.

## The Gain Against Padding

`devtools.contraction_margin`, each contracted packing decided on both routes:

- **262’s house**, T-155’s exact view: margin 1.6707 × 10⁻¹⁹ (squares 244 and 245)
  ([measure/contraction-n262.json](measure/contraction-n262.json)); 16 + √2/2 is its
  exact contact. The gain, 7.4133 × 10⁻³, lies wholly outside it.
- **295’s house**, T-146’s rational packing at 295: margin 1.7704 × 10⁻¹⁹ (squares 206
  and 220) ([measure/contraction-n295.json](measure/contraction-n295.json)); T-193’s
  (22 + 22√2)/3 is its exact contact, 1.80 × 10⁻¹⁹ below it. The gain, 4.5393 × 10⁻³, lies
  wholly outside it, so RV-3 (think-ruu2) reaches neither count.
- **The certificates’ own margins**: 6.8888 × 10⁻¹¹ at 262 (squares 33 and 179) and
  2.5384 × 10⁻¹¹ at 295 (squares 55 and 56) (`contraction-n262-own.json`,
  `contraction-n295-own.json`); those sides are not registered.

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json), with both sides stood in, finds
main’s consequences less the L step from 231 to 262, which reaches 262 10⁻²⁰ below the
case’s rational ceiling on `main` and is above this side. The L step from this 262 gives
17.699693441904 at 295, 1.883 × 10⁻¹⁰ above this 295; the one from 295 lands at 330,
beyond the corpus. Monotonicity carries neither side to a smaller count below its record,
so no bound carries to another count.

## Stage 4 Review

The blind stage 4 review is lane R1’s (think-p3g8); this lane has not read it.

## What Is Not Established

- **The search**: the closed-form layout, the integer program and the optimization are
  described, not retained.
- **The L border**: the issue’s account; the certificates are not one L step apart.
- **Local optimality, rigidity or KKT**: not claimed.
- **Human oversight**: no record is retained.

## Credit and Licence

The packings are Joost de Winter’s, new arrangements at 262 and 295 that use no other
packing’s coordinates, as the issue says. The record credits people, not AI agents
([attribution.md](../../../../attribution.md)), and states the assistance in the source’s
words. The bibliography key is **[de Winter upper bounds 262 295 2026-11-16]**.
`LICENSE` at the pin is de Winter’s MIT licence, and the root README says all files are
released under it.

## Commands

From `packing/`, with the project interpreter:

```bash
P=de-winter-upper-bounds-262-295-2026-11-16
M=resources/web/$P/measure
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 262 "DEWINTER=packet:$P" \
  'T-155=witness-center-basis:cases/regularized_bounds/views/n-262.yaml.gz' \
  --out $M/identity-n262.json
python -m devtools.measure_identity --n 295 "DEWINTER=packet:$P" \
  'T-146=packet:evand-regularized-2026-10-10' --out $M/identity-n295.json
python -m devtools.measure_identity --n 262 "L-BASE-295=l-base:packet:$P" \
  "DEWINTER-262=packet:$P"   # refused: not one L step
python -m devtools.contraction_margin --n 262 \
  'T-155=witness-center-basis:cases/regularized_bounds/views/n-262.yaml.gz' \
  --against "de-winter-1007=packet:$P" --out $M/contraction-n262.json
python -m devtools.contraction_margin --n 262 "de-winter-1007=packet:$P" \
  --out $M/contraction-n262-own.json
python -m devtools.contraction_margin --n 295 'T-146=packet:evand-regularized-2026-10-10' \
  --against "de-winter-1007=packet:$P" --out $M/contraction-n295.json
python -m devtools.contraction_margin --n 295 "de-winter-1007=packet:$P" \
  --out $M/contraction-n295-own.json
python -m devtools.l_step_scan --with 262=166996934419035177/10000000000000000 \
  --with 295=35399386883430443/2000000000000000 --out $M/l-step-scan.json
```

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/n262/n262_exact.json.gz` | upstream | `21b793a22d5b7aaa24332461b2a926d3fcec776c` | `95875def0a2784e980ff92cacbe0508d84cc1ee03d6104130d9db4007a0ffa04` |
| `source/n295/n295_exact.json.gz` | upstream | `25ce13f541c711b924e995cc9755700819cf7dbf` | `9a0b4bc14803a43fb46e0370a3ad25faaa5a1f7f47186248455c90fae91b13a0` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
