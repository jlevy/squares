# Joost de Winter’s s(299) Certificate of Issue 1031, at 497eb47

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/497eb478b790175ea8690671b66785b70c97f9f2),
a watched repository, at `497eb478b790175ea8690671b66785b70c97f9f2` (committed
2026-11-18T06:34:51Z, “Add the packing for n = 299”), the commit
[issue #1031](https://github.com/jlevy/squares/issues/1031) names 594 seconds later.
Lane c2-imports fetched the repository at 07:03Z on 20 November without file contents,
and the files at the pin at 07:06Z, after its controls plan was hashed; the head was
then `21d944c`. The next commit, `3293038`, the same second, adds only
`n299/REGISTRATION.md` and `n299/SHA256SUMS`, whose digests match this pin’s files;
`aae089c` and `7232328` add and remove an `n109_kaggle/` folder and `21d944c` a
`lower_bounds_2026_11_19/` folder, and none of them touches `n299/`.

Lane w6r2-dewinter-1118 triaged the issue on 18 November 2026 (think-10mx); lane
c2-imports retained, replayed and measured the certificate on 20 November.

## What the Source Claims

- `n299/n299_exact.json` states 299 unit squares as centre and unit edge direction rows
  of exact rationals, with the side
  17793636991743040580325825384225613703947282755372586749208848013397/10⁶⁶. #1031 and
  the root README round it up at 12 places as 17.793636991744, and `n299/README.md`
  prints 17.793636991743040580. `n299/n299_witness.yaml` is the same packing as a corner
  Witness/v2 of rationals.
  The issue names the case page’s 17.801004434255294 at 299 on 18 November (T-277, Doğa
  Özden after Evan Daniel) and the gain, 0.0074; #1009’s pass moved the house to T-325,
  3.53 × 10⁻¹² below T-277, that day.
- **Construction.** Diagonal slices, each filled from a reflected or translated copy of
  a public packing: the outer slices from 372 squares and the seven middle slices from
  335, both from Asterios Panoras’s public Kaggle compilation (version 17). The issue
  says Kaggle’s community explorer (nevska) links the 372-square packing to prvsiyan’s
  notebook “A Square Deal” and the 335-square packing to four notebooks with the same
  score, by areebbb, jazivxt, alexchilton and prvsiyan.
  A local optimization exchanged the separating edges of touching pairs; reflecting part
  of one tilted group across the diagonal x + y = S and releasing its neighbours gave
  the final gain. In the final layout 55 squares tilt at least 15 degrees one way and 54
  the other.
- **Checkers.** `verify_exact.py` (separating axes) and `check_area.py` (the area of
  each close pair’s clipped intersection), both `fractions.Fraction` and the standard
  library only; the issue says each reports 299 squares and 714 close pairs, that they
  share no code but have one author and read one input file, and that the witness had
  not been run through this repository’s checker.
  Those statements are the author’s; no source program ran here.
- **Not done.** No test of local optimality, and no optimality claimed.
  The issue quotes the Kaggle per-puzzle leaderboard’s 17.793636991746555 at 299 (Nick
  Sarris, a notebook completed 18 November, 01:07:56 UTC), 3.5 × 10⁻¹² above this side,
  probably the same local optimum, with no coordinates found.
- **Credit and AI assistance.** It asks for credit to Joost de Winter, Delft University
  of Technology, after the 335- and 372-square packings in Panoras’s compilation
  (prvsiyan, areebbb, jazivxt, alexchilton).
  The issue and `n299/README.md` say the search, optimization and rational certificate
  were produced with GPT-6.2 Sol (OpenAI) and the repository files, checks and figure
  with Claude (Anthropic), both under his direction.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the licence, the root README and the whole of `n299/`, 8 files: 4 retained
under [source/](source/), `n299/n299_exact.json` stored as deterministic gzip, and four
pinned only. `LICENSE` is byte-identical to the copy the
[de-winter-upper-bounds-227-229-260-2026-10-17](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
packet retains, and `n299/verify_exact.py` and `n299/check_area.py` to the copies the
[de-winter-s90-64d5ee7-2026-11-15](../de-winter-s90-64d5ee7-2026-11-15/README.md) packet
retains; each is pinned against its copy and was never run here.
The figure is pinned by digest only.
The certificate and the witness have the SHA-256 digests the folder’s `SHA256SUMS` lists
at `3293038`.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `1015fc175`. `center-direction-json` reads the certificate, and
`witness-corners-opposite` its corner twin; the two state the same packing exactly.

| Compared with | Side | Below it by |
| --- | --- | --- |
| T-325, Mykhailo Polkovskyi’s re-solve of Doğa Özden’s T-277, after Evan Daniel, the house in both lanes from 18 November | 17.8010044342517669 | 7.36744 × 10⁻³ |
| T-277, the house before it | 17.8010044342552937 | 7.36744 × 10⁻³ |

The
[ledger of 20 November](../../../campaign/issue-intake/upper-bounds-1031-20261120/README.md)
walks #1031 and records it.

## Pose by Pose

`devtools.measure_identity` wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **Against T-325.** No symmetry of the box pairs the two one to one by nearest centres.
  The optimal assignment, best under symmetry 3, moves 295 squares beyond 10⁻³, 182
  beyond 0.01 and 127 beyond 0.1 (largest 1.07414), and turns 146 squares by more than
  10⁻⁶ radians, by up to 41.72 degrees; 18 of its 114 tilted squares pair with tilted
  squares of T-325 of the same sign, and 95 with upright ones.
- **Against T-277.** Likewise.
- **Tilts.** 114 squares tilted beyond a degree, 2.18 to 27.89 degrees by magnitude, 55
  one way and 59 the other, where T-325’s 85 lean 2 one way and 83 the other; one more
  turned by 0.0065 degrees; the other 184 exactly upright.

The tool aligns the two packings by the box’s symmetries only.
Whether a rigid motion off them, such as a translation along the diagonal, pairs a large
part of this packing with T-325’s is not measured here; the stage 4 review measures it
(below), and the credit relative to T-325 waits on that.

## Exact Replay

The checks below were planned before any of them ran, in
[controls-plan-299.txt](../../../campaign/issue-intake/upper-bounds-1031-20261120/controls-plan-299.txt),
hashed at 07:04:05Z on 20 November and recorded on the bead before any route read the
certificate.

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes: 3 jobs, 267,306 pair
decisions, 73.25 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 1.0475 × 10⁻⁷⁴ (squares 137 and 175). `check --replay` decided the three jobs
again.

`sharp-controls` took the certificate to exact contact and 10⁻³⁰ past it on both routes
([receipts/sharp-controls.json](receipts/sharp-controls.json), 277 CPU seconds), and
every control came out as the module predicts it, by the plan’s branches W1, P1, N0 and
E0: the box lowered by its far-wall clearance, 6.42 × 10⁻⁶⁷, the tightest pair closed
(175 toward 137) and every square moved toward its near wall by 0, a square already
touching one, each accepted at contact and refused 10⁻³⁰ past it; square 175 enlarged to
137 refused at contact for its shape alone and past it for the overlap as well; square
129, at its wall, grown by 0 and accepted; and a duplicated square refused.

**One control differs from the plan’s letter.** The plan says square 129, grown past its
wall, is refused for the wall and the shape.
Both routes refused it for the wall, the shape and an overlap: every pair gap here is
far below 10⁻³⁰, so no square near a wall can grow by 10⁻³⁰ without closing a pair, and
the sharp-controls module then enlarges the square nearest a wall anyway and predicts
the overlap exactly beforehand.
The difference is recorded on the bead and in the pull request.

The two routes share the centre-direction reader, Fraction arithmetic and the
separating-axis method; neither is the author’s code.

## The Gain Against Padding

`devtools.contraction_margin`, each contracted packing decided on both routes:

- **The house**, T-325: margin 3.5612 × 10⁻²⁷ (squares 71 and 140)
  ([measure/contraction-n299.json](measure/contraction-n299.json)); the gain on it,
  7.3674 × 10⁻³, lies wholly outside it, so under the owner’s option D of 17 November
  2026 (think-b0w5) the claim is a new result.
- **T-277**: margin 3.4040 × 10⁻¹² (squares 179 and 194)
  ([measure/contraction-n299-t277.json](measure/contraction-n299-t277.json)).
- **This certificate**: margin 6.4244 × 10⁻⁶⁷ (squares 137 and 175)
  ([measure/contraction-n299-own.json](measure/contraction-n299-own.json)).

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json), with this side stood in for 299’s
ceiling, finds main’s consequences unchanged.

## Stage 4 Review

The blind stage 4 review is lane r1031-1118’s, draft PR #1036, which this lane has not
read. It is mapped once it merges.
Before this lane ran anything, the import bead’s notes of 18 November recorded two
relays of its progress: an accepting verdict, and that its senior review found 210 of
the 299 squares coinciding with T-325’s under one rigid motion, which the review was
measuring as generic or as a continuation.
Nothing in this packet’s measurements came from those relays.

## What Is Not Established

- **The search**: the slices, the optimization and the reflection are described, not
  retained; the lineage beyond the measurements above is the issue’s.
- **The credit relative to T-325’s packing**, until the review’s rigid-motion
  measurement is mapped.
- **Local optimality, rigidity or KKT**: none is claimed or replayed.
- **Human oversight**: no record is retained.

## Credit and Licence

The issue credits the packing to Joost de Winter, after the 335- and 372-square packings
in Panoras’s compilation.
The record credits people, not AI agents ([attribution.md](../../../../attribution.md)),
and states the assistance in the source’s words.
The bibliography key is **[de Winter s299 upper bound 2026-11-18]**. `LICENSE` at the
pin is de Winter’s MIT licence, and the root README says all files are released under
it. The compilation is not in the repository and not retained here.

## Commands

From `packing/`, with the project interpreter:

```bash
P=de-winter-s299-upper-bound-2026-11-18
M=resources/web/$P/measure
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 299 "DEWINTER-299=packet:$P" \
  'T-325=packet:mishapolk-issue1009-2026-11-16' 'T-277=packet:ozden-s299-upper-bound-2026-11-09' \
  --out $M/identity.json
python -m devtools.contraction_margin --n 299 'T-325=packet:mishapolk-issue1009-2026-11-16' \
  --against "DEWINTER-299=packet:$P" --out $M/contraction-n299.json
python -m devtools.contraction_margin --n 299 'T-277=packet:ozden-s299-upper-bound-2026-11-09' \
  --against "DEWINTER-299=packet:$P" --out $M/contraction-n299-t277.json
python -m devtools.contraction_margin --n 299 "DEWINTER-299=packet:$P" \
  --out $M/contraction-n299-own.json
python -m devtools.l_step_scan --with 299=S299 --out $M/l-step-scan.json
```

In the last command `S299` is the `exact_side` in the packet’s claim record.

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/n299/n299_exact.json.gz` | upstream | `0a8e81206df2297ff757ce9276a07da585ea34b8` | `199e6132eeb4104d9894e4296f2bac3d244175f745163f63130e9f2065ed4a9c` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
