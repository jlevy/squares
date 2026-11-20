# Joost de Winter’s s(270) Certificate of Issue 1022, at a1ba501

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/a1ba5019e787e407646293d7bef81d63c9951b32),
a watched repository, at `a1ba5019e787e407646293d7bef81d63c9951b32` (committed
2026-11-17T22:48:48Z, “Add packings for n = 268 and n = 270 and a smaller certificate
for n = 127”), the commit [issue #1022](https://github.com/jlevy/squares/issues/1022)
names 91 seconds later.
The lane fetched the repository at 01:21Z on 18 November, when `git ls-remote` read the
head as `838c5ea`, which adds only `n270/REGISTRATION.md` and `n270/SHA256SUMS`, whose
digests match this pin’s files.
The same commit’s `n268/` is #1021’s certificate, which the
[de-winter-s268-upper-bound-2026-11-17 packet](../de-winter-s268-upper-bound-2026-11-17/README.md)
retains.

Intake lanes w6-dewinter-1118 and w6r-dewinter-1118 (think-gqzz) retained it, replayed
it and measured it on 18 November 2026; lane c2-imports wrote this README on 20 November
and adopted the packing as the house at 270 that day (think-78aj).

## What the Source Claims

- `n270/n270_exact.json` states 270 unit squares as centre and unit edge direction rows
  of exact rationals, with the side
  16927314216351701364094693919616632628260321141481608494025753/1000000000000000000000000000000000000000000000000000000000000.
  #1022 and the root README round it up at 12 places as 16.927314216352, and
  `n270/README.md` prints 16.927314216351701. `n270/n270_witness.yaml` is the same
  packing as a corner Witness/v2 of rationals.
  The issue names the record’s 16.928148603342855 (T-283) and the gain, 0.00083, and
  says later commits leave these files unchanged.
- **Construction.** The 270-square packing of Asterios Panoras’s public Kaggle
  compilation (version 17, side 16.92746606488242), a merge of many contributors that
  does not name the finder of this arrangement: its two end regions removed and relaxed
  in turn, a 68-square region at the bottom compressed inside a rectangle, then
  reassembled and every square’s position and angle optimized.
- **Checkers.** `verify_exact.py` (separating axes) and `check_area.py` (the area of
  each close pair’s clipped intersection), both `fractions.Fraction` and the standard
  library only; the issue says each reports 270 squares and 642 close pairs, that they
  share no code but have one author and read one input file, and that the witness had
  not been run through this repository’s checker.
  Those statements are the author’s; no source program ran here.
- **Not done.** No test of local optimality, and no optimality claimed.
  The issue quotes the compilation’s 16.92746606488242 and Danil Malyshev’s coordinates
  of #1012 at 16.927469593519, both 1.55 × 10⁻⁴ above this side, and the Kaggle
  per-puzzle table’s 16.927314216351814 at 270 (the team [NUP] Junie is all you need, 9
  November), 1.1 × 10⁻¹³ above it, probably the same local optimum, with no coordinates
  found.
- **Credit and AI assistance.** It asks for credit to Joost de Winter, Delft University
  of Technology, after the arrangement in Panoras’s compilation.
  The issue says the search, optimization and rational certificate were produced with
  GPT-6.2 Astra (OpenAI), where `n270/README.md` names GPT-6.2 Sol, and the repository
  files, checks and figure with Claude (Anthropic), both under his direction.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the licence, the root README and the whole of `n270/`, 8 files: 4 retained
under [source/](source/), `n270/n270_exact.json` stored as deterministic gzip, and four
pinned only. `LICENSE` is byte-identical to the copy the
[de-winter-upper-bounds-227-229-260-2026-10-17](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
packet retains, and `n270/verify_exact.py` and `n270/check_area.py` to the copies the
[de-winter-s90-64d5ee7-2026-11-15](../de-winter-s90-64d5ee7-2026-11-15/README.md) packet
retains; each is pinned against its copy and was never run here.
The figure is pinned by digest only.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `86284ec20` after #1009’s import moved 270 to T-321. `center-direction-json`
reads the certificate, and `witness-corners-opposite` its corner twin; the two state the
same packing exactly.

| Compared with | Side | Below it by |
| --- | --- | --- |
| T-321, Mykhailo Polkovskyi’s re-solve of T-283, Evan Daniel’s packing as Doğa Özden improved it, the house in both lanes from 18 November | 16.9281486033396074 | 8.34387 × 10⁻⁴ |
| T-283, the house before it | 16.9281486033428544 | 8.34387 × 10⁻⁴ |

The
[ledger of 18 November](../../../campaign/issue-intake/upper-bounds-1021-1022-20261118/README.md)
walks #1022 after #1009’s report at 270 and records it.

## Pose by Pose

`devtools.measure_identity` wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **Against T-321.** No symmetry of the box pairs the two one to one by nearest centres.
  The optimal assignment, best under symmetry 3, moves 247 squares beyond 10⁻³, 115
  beyond 0.01 and 94 beyond 0.1 (largest 1.02401), and turns 117 squares by more than
  10⁻⁶ radians, by up to 38.25 degrees; 5 of its tilted squares pair with tilted squares
  of T-321 of the same sign.
- **Against T-283.** Likewise.
- **Tilts.** 78 squares tilted beyond a degree, 19.78 to 35.37 degrees, all one way, as
  `n270/README.md` says; 5 more turned by less than a degree; the other 187 exactly
  upright.

So it is a new arrangement relative to both.

## Exact Replay

The checks below were planned before any of them ran, in
[controls-plan-268-270.txt](../../../campaign/issue-intake/upper-bounds-1021-1022-20261118/controls-plan-268-270.txt),
hashed at 02:27:48Z on 18 November and recorded on the bead before any route read the
certificate.

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes: 3 jobs, 217,890 pair
decisions, 37.71 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
No square touches the box: every wall clears by at least 2.00 × 10⁻⁶⁰, and every pair by
at least 1.58 × 10⁻⁵⁹ (squares 98 and 101). `check --replay` decided the three jobs
again.

`sharp-controls` took the certificate to exact contact and 10⁻³⁰ past it on both routes
([receipts/sharp-controls.json](receipts/sharp-controls.json)), and every control came
out as the module predicts it, by the plan’s branches for a box no square touches (W1,
P1, N1, E1): the box lowered by its far-wall clearance, the tightest pair closed (101
toward 98) and every square moved toward its near wall by the least near-wall clearance,
each accepted at contact and refused 10⁻³⁰ past it; square 108 enlarged to its wall
refused at contact for the shape alone and past it for the wall as well; and a
duplicated square refused.

**One control differs from the plan’s letter**, as lane c2-imports found on 20 November.
The plan says a square enlarged to its pair is refused at contact for its shape alone.
Square 101, grown to its least gap with square 98, already overlaps another neighbour at
contact: none of the near pairs the sharp-controls module tries can be grown to its gap
without closing another pair, and the module then enlarges the tightest pair’s square
anyway and predicts the overlap exactly beforehand.
Both routes refused it at contact and past it for the shape and the overlap, as
predicted. The 18 November records said all 11 came out as the plan states; the register
entry now says so of ten.

The two routes share the centre-direction reader, Fraction arithmetic and the
separating-axis method; neither is the author’s code.

## The Gain Against Padding

`devtools.contraction_margin`, each contracted packing decided on both routes:

- **The house**, T-321: margin 3.3863 × 10⁻²⁷ (squares 164 and 193)
  ([measure/contraction-n270.json](measure/contraction-n270.json)); the gain on it,
  8.3439 × 10⁻⁴, lies wholly outside it, so under the owner’s option D of 17 November
  2026 (think-b0w5) the claim is a new result.
- **This certificate**: margin 2.5584 × 10⁻⁵⁸ (squares 98 and 101)
  ([measure/contraction-n270-own.json](measure/contraction-n270-own.json)).

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json), with this side stood in for 270’s
ceiling, finds main’s consequences unchanged.

## Stage 4 Review

The blind stage 4 review is lane r1021-1118’s, PR #1033:
[review-2026-11-18-de-winter-1021-1022.md](../../../../docs/project/reviews/review-2026-11-18-de-winter-1021-1022.md),
mapped after this packet’s replay, controls, measurements and registration were
committed. It accepts the certificate and its Witness/v2 twin, decided again by a
clean-room checker frozen before any certificate was read, by two exact methods with 45
controls at this count stated in advance, with fourteen findings, none blocking or
major. Its option D measurements and identity agree with this packet’s exactly.
Its Question 2 asks the author about the five slightly turned squares.
T-332 is confirmed, independently re-implemented, at V3/C3, and is the house at 270 from
the pass of 20 November 2026.

## What Is Not Established

- **The search**: the regions and the optimization are described, not retained; the
  lineage beyond the measurements above is the issue’s.
- **Local optimality, rigidity or KKT**: none is claimed or replayed.
- **Human oversight**: no record is retained.

## Credit and Licence

The packing is Joost de Winter’s, a new arrangement at 270 after the packing in Asterios
Panoras’s compilation, whose finder the compilation does not name.
The record credits people, not AI agents ([attribution.md](../../../../attribution.md)),
and states the assistance in the source’s words.
The bibliography key is **[de Winter s270 upper bound 2026-11-17]**. `LICENSE` at the
pin is de Winter’s MIT licence, and the root README says all files are released under
it. The compilation is not in the repository and not retained here.

## Commands

From `packing/`, with the project interpreter:

```bash
P=de-winter-s270-upper-bound-2026-11-17
M=resources/web/$P/measure
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 270 "DEWINTER-270=packet:$P" \
  'T-321=packet:mishapolk-issue1009-2026-11-16' 'T-283=packet:ozden-s270-upper-bound-2026-11-09' \
  --out $M/identity.json
python -m devtools.contraction_margin --n 270 'T-321=packet:mishapolk-issue1009-2026-11-16' \
  --against "DEWINTER-270=packet:$P" --out $M/contraction-n270.json
python -m devtools.contraction_margin --n 270 "DEWINTER-270=packet:$P" \
  --out $M/contraction-n270-own.json
python -m devtools.l_step_scan --with 270=S270 --out $M/l-step-scan.json
```

In the last command `S270` is the `exact_side` in the packet’s claim record.

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/n270/n270_exact.json.gz` | upstream | `e13657550578ce072b659c32f9b02042bf898336` | `2bf77929c5920c6ff5561d0c5c5255f78e8effff96622ce5d4bb75c9c4021148` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
