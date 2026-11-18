# Joost de Winter’s s(127) Certificate of Issue 1015, at 35b576a

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/35b576a355297942bca9c195bee5cd74f0b27f40),
a watched repository, at `35b576a355297942bca9c195bee5cd74f0b27f40` (committed
2026-11-17T22:09:10Z, “Name GPT-6.2 Sol as the model used for n = 127”), the commit
[issue #1015](https://github.com/jlevy/squares/issues/1015) names 323 seconds later. Its
parent, `689bc79` (22:07:57Z, pushed 22:07:59Z), first committed `n127/`; `35b576a`
(pushed 22:09:12Z) renames only the model in three files and their checksums, and leaves
the certificate, the witness and the figure as they were. The lane fetched the
repository at 01:21Z on 18 November, when `git ls-remote` read the head as `838c5ea`.

Intake lane w6-dewinter-1118 (think-zqot) retained it, replayed it and measured it on 18
November 2026. It is the first of three reports at 127 that evening, all de Winter’s:
[#1017](https://github.com/jlevy/squares/issues/1017) (22:27:04Z) names `cc20a26`, which
replaces the certificate with one 1.9556 × 10⁻⁶ smaller, and
[#1020](https://github.com/jlevy/squares/issues/1020) (22:49:35Z) names `a1ba501`, which
replaces it again, 1.7976 × 10⁻¹³ smaller still; the
[de-winter-s127-issue1017-2026-11-17](../de-winter-s127-issue1017-2026-11-17/README.md)
and [de-winter-s127-issue1020-2026-11-17](../de-winter-s127-issue1020-2026-11-17/README.md)
packets retain them. Neither later issue withdraws this one.

## What the Source Claims

- `n127/n127_exact.json` states 127 unit squares as centre and unit edge direction rows
  of exact rationals, with the side
  590039784110678470545925017871932135226358204819969425332092601/50000000000000000000000000000000000000000000000000000000000000.
  #1015 and the root README round it up at 12 places as 11.800795682214, and
  `n127/README.md` prints 11.800795682213569410918500357438642704527.
  `n127/n127_witness.yaml` is the same packing as a corner Witness/v2 of rationals.
  The issue names the record’s 11.8017538904864874 (T-305) and the gain, 0.00096.
- **Construction.** A tilted central band of 57 squares inside a frame of axis-aligned
  squares. The search started from an exact certificate of an arrangement in the public
  Kaggle coordinate compilations of Alex Chilton and Asterios Panoras, whose original
  finder could not be established, changed the sliding offsets of the columns in the
  tilted band, and then optimized the positions and angles of individual squares.
- **Checkers.** `verify_exact.py` (separating axes) and `check_area.py` (the area of each
  close pair’s clipped intersection), both `fractions.Fraction` and the standard library
  only; the issue says each reports 127 squares and 311 close pairs, and that the witness
  has not yet been run through this repository’s checker. They have one author and read
  one input file, and share no code. Those statements are the author’s; no source program
  ran here.
- **Not done.** No test of local optimality, no proof of optimality. On the Kaggle
  per-puzzle leaderboard Luka Cvetkovic reported 11.800793726618 at 127 (16 November),
  2.0 × 10⁻⁶ below this packing, with no coordinates found.
- **Credit and AI assistance.** It asks for credit to Joost de Winter, Delft University
  of Technology, after the arrangement in the Chilton and Panoras compilations. The
  search, optimization and rational certificate were produced with GPT-6.2 Sol (OpenAI),
  and the repository files, checks and figure with Claude (Anthropic), both under his
  direction.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the licence, the root README and the whole of `n127/`,
10 files: 6 retained under [source/](source/) and four pinned only. `LICENSE` is
byte-identical to the copy the
[de-winter-upper-bounds-227-229-260-2026-10-17](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
packet retains, and `n127/verify_exact.py` and `n127/check_area.py` to the copies the
[de-winter-s90-64d5ee7-2026-11-15](../de-winter-s90-64d5ee7-2026-11-15/README.md) packet
retains; each is pinned against its copy and was never run here. The figure is pinned by
digest only. The pin’s `n127/SHA256SUMS` lists the digest of every file of the pin’s `n127/`.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `eb50f54e9`. `center-direction-json` reads the certificate, and
`witness-corners-opposite` its corner twin; the two state the same packing exactly.

| Compared with | Side | Below it by |
| --- | --- | --- |
| T-305, Tomáš Kodaj’s Kaggle packing as JoeGun improved it, the house in both lanes | 11.8017538904864874 | 9.5821 × 10⁻⁴ |

## Report Order

The
[ledger of 18 November for this lane](../../../campaign/issue-intake/upper-bounds-1015-1020-20261118/README.md)
walks #1015 (22:14:33Z), #1017 (22:27:04Z) and #1020 (22:49:35Z) at 127 and records all
three, each below the last. The pushes keep the order, each before its issue.

## Pose by Pose

`devtools.measure_identity` wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **Against T-305.** No symmetry of the box pairs the two one to one by nearest centres,
  and the house witness and its regularized view measure as T-305. The optimal
  assignment, best under the identity, moves 116 squares beyond 10⁻³, 77 beyond 0.01 and
  10 beyond 0.1 (largest 0.789455), and turns 85 squares by up to 33.19 degrees. Tilted
  beyond a degree: 57 here, 1.20 to 30.12 degrees, 55 one way and 2 the other, against
  T-305’s 56 at 26.42 to 31.83 degrees, all one way; 55 of the 57 pair with tilted
  squares of T-305 of the same sign. So the arrangement is close to T-305’s, its band
  rearranged as the issue’s column offsets say, but not one to one with it.

## The Gain Against Padding

`devtools.contraction_margin`, each contracted packing decided on both routes:

- **The house**, T-305: margin 1.2099 × 10⁻¹⁰ (squares 89 and 93)
  ([measure/contraction-n127.json](measure/contraction-n127.json)); the gain on it,
  9.5821 × 10⁻⁴, about 7.9 × 10⁶ times that, lies wholly outside it, so under the
  owner’s option D of 17 November (think-b0w5) the claim is a new result.
- **This certificate**: margin 7.7394 × 10⁻⁶³ (1 − λ\* about 3.7258 × 10⁻⁷⁰, squares 31
  and 34) ([measure/contraction-n127-own.json](measure/contraction-n127-own.json)): its
  squares sit within 10⁻⁶⁹ of contact.

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json), with this side stood in for 127’s
ceiling, finds exactly `main`’s L-step and monotonicity consequences. The L step from 127
lands at 150 at side 12.8008, above 150’s ceiling; no bound carries.

## Exact Replay

The checks below were planned before any of them ran: the expected verdict of every
gross and sharp control of the three certificates at 127 was written down and hashed at
01:26:53Z on 18 November (SHA-256 `7f287382…43ff`, recorded on think-zqot at 01:27Z), and
the plan is retained, committed and pushed before any receipt
([controls-plan-127.txt](../../../campaign/issue-intake/upper-bounds-1015-1020-20261118/controls-plan-127.txt),
commit `da9a33f18`). Before it was hashed the lane had read each certificate’s side field
and square count with a script of its own; no route or program had read them.

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes: 3 jobs, 48,006 pair
decisions, 29.25 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes, as planned. No square touches the box: every wall is cleared by at least 2.3137 × 10⁻⁷⁰.
Every pair clears by at least 3.7304 × 10⁻⁷⁰ (squares 31 and 34). `check --replay` decided the
three jobs again.

`sharp-controls` took the certificate to exact contact and 10⁻³⁰ past it on both routes
([receipts/sharp-controls.json](receipts/sharp-controls.json), 118 CPU seconds),
and all 11 came out as the plan stated. No square touches a wall, so the branches taken were those of a clearing certificate: the box lowered to its extent (7.7394 × 10⁻⁶³ below the side), the tightest pair closed (34 toward 31) and every square moved toward its near wall by the least near-wall clearance (2.3137 × 10⁻⁷⁰), each accepted at contact and refused 10⁻³⁰ past it; square 34 enlarged to 31 and square 46 enlarged to its wall, each refused at contact for its shape alone and past it for the overlap or the wall as well; and a duplicated square refused. The plan expected the near-wall move to be 0, as at every earlier de Winter certificate; it was 2.3137 × 10⁻⁷⁰, the branch for a clearing square, and every verdict was the one stated. The two routes, the `sqpack`
rational witness verifier and the independent rational corner checker, share this
repository’s certificate readers (the `center-direction-json` adapter and the half-angle
conversion), `Fraction` arithmetic and the separating-axis method; neither is the
author’s code, and neither shares code with it.

## Stage 4 Review

The blind stage 4 review of the three certificates at 127 is lane R-127’s (under
think-zqot); this lane has not read it.

## What Is Not Established

- **The search**: the search over the band’s column offsets and the optimization are
  described, not retained; the lineage beyond the measurements above is the issue’s.
- **The compilations’ packing**: the Kaggle compilations of Alex Chilton and Asterios
  Panoras were not read, so the arrangement the search started from is not measured here;
  only its closeness to T-305’s packing is.
- **Local optimality, rigidity or KKT**: the issue claims none, and none was tested.
- **Human oversight**: no record is retained.

## Credit and Licence

The packing is Joost de Winter’s, after the arrangement in the Kaggle compilations of
Alex Chilton and Asterios Panoras, as the issue asks; measured, it is close to T-305’s
packing, Tomáš Kodaj’s Kaggle packing as JoeGun improved it, though not one to one with
it, and whether the compilations’ arrangement is Kodaj’s is not established here. The
record credits people, not AI agents ([attribution.md](../../../../attribution.md)), and
states the assistance in the source’s words. The bibliography key is
**[de Winter s127 issue 1015 2026-11-17]**. `LICENSE` at the pin is de Winter’s MIT
licence, and the root README says all files are released under it.

## Commands

From `packing/`, with the project interpreter:

```bash
P=de-winter-s127-issue1015-2026-11-17
H=joegun-upper-bounds-2026-11-16
M=resources/web/$P/measure
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 127 "DEWINTER-1015=packet:$P" "T-305=packet:$H" \
  'house-witness=witness-center-basis:witnesses/known-best/n-127.yaml' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-127-regularized.yaml.gz' \
  --out $M/identity.json
python -m devtools.contraction_margin --n 127 "T-305=packet:$H" \
  --against "DEWINTER-1015=packet:$P" --out $M/contraction-n127.json
python -m devtools.contraction_margin --n 127 "DEWINTER-1015=packet:$P" \
  --out $M/contraction-n127-own.json
python -m devtools.l_step_scan --with 127=S127 --out $M/l-step-scan.json
```

In the last command `S127` is the `exact_side` in the packet’s claim record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
