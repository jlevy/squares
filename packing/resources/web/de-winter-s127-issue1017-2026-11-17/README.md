# Joost de Winter’s s(127) Certificate of Issue 1017, at cc20a26

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/cc20a26845789c2502950041c26709eda8a71081),
a watched repository, at `cc20a26845789c2502950041c26709eda8a71081` (committed
2026-11-17T22:26:24Z, “Add the new n = 127 certificate, the lower bound for n = 108 and
the packings for n between 1,036 and 9,928”), the commit
[issue #1017](https://github.com/jlevy/squares/issues/1017) names 40 seconds later; it was
pushed with the next commit, `67fb815`, at 22:26:28Z. It replaces the certificate, the
witness and the figure of `35b576a`, which
[#1015](https://github.com/jlevy/squares/issues/1015) reports and the
[de-winter-s127-issue1015-2026-11-17](../de-winter-s127-issue1015-2026-11-17/README.md)
packet retains, with a packing 1.9556 × 10⁻⁶ smaller. It also adds `lower_n108/`, the lower
bound #1018 reports, which the de-winter-s108-lower-bound-2026-11-17 packet of
think-i5en’s change retains at this pin, and `above1000/`, which #1019 reports and think-1tkk holds;
neither is in this packet’s scope. The lane fetched the repository at 01:21Z on 18
November, when `git ls-remote` read the head as `838c5ea`.

Intake lane w6-dewinter-1118 (think-zqot) retained it, replayed it and measured it on 18
November 2026. It is the second of three reports at 127 that evening, all de Winter’s;
[#1020](https://github.com/jlevy/squares/issues/1020) (22:49:35Z) replaces it at `a1ba501`
by a packing 1.7976 × 10⁻¹³ smaller, which the
[de-winter-s127-issue1020-2026-11-17](../de-winter-s127-issue1020-2026-11-17/README.md)
packet retains.

## What the Source Claims

- `n127/n127_exact.json` states 127 unit squares as centre and unit edge direction rows
  of exact rationals, with the side 5900396863307571/500000000000000 =
  11.800793726615142, which #1017 states exactly and its title rounds up at 12 places as
  11.800793726616, as the root README does. `n127/n127_witness.yaml` is the same packing
  as a corner Witness/v2 of rationals. The issue names the record’s 11.8017538904864874
  (T-305) and the gain, 0.00096, and says later commits leave these files unchanged.
- **Construction.** The band and frame of #1015, the search over the column offsets and
  the optimization of individual squares, then a second stage that repeatedly changed the
  aspect ratio of the enclosing rectangle while moving and rotating squares, and returned
  to a square, which shifted the tilted cap at the top of the band and changed some of its
  contacts.
- **Checkers.** `verify_exact.py` and `check_area.py`, unchanged from `35b576a`; the issue
  says each reports 127 squares and 312 close pairs. Those statements are the author’s;
  no source program ran here.
- **Not done.** No test of local optimality. The packing is 2.04 × 10⁻¹² below Luka
  Cvetkovic’s Kaggle side, 11.800793726617185 (16 November), so the issue says the two
  are probably the same local optimum; his coordinates were not found.
- **Credit and AI assistance.** As #1015: Joost de Winter, after the arrangement in the
  Chilton and Panoras compilations; GPT-6.2 Sol (OpenAI) and Claude (Anthropic), under
  his direction.

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
digest only. The pin’s `n127/SHA256SUMS` and `n127/REGISTRATION.md` are still `35b576a`’s, so the checksums’ lines for the certificate, the witness, the figure and `n127/README.md` do not match the pin’s files; `67fb815`’s match them.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `eb50f54e9`. `center-direction-json` reads the certificate, and
`witness-corners-opposite` its corner twin; the two state the same packing exactly.

| Compared with | Side | Below it by |
| --- | --- | --- |
| T-305, Tomáš Kodaj’s Kaggle packing as JoeGun improved it, the house in both lanes | 11.8017538904864874 | 9.6016 × 10⁻⁴ |
| #1015, de Winter’s certificate, filed before it | 11.8007956822135694… | 1.9556 × 10⁻⁶ |

## Report Order

The
[ledger of 18 November for this lane](../../../campaign/issue-intake/upper-bounds-1015-1020-20261118/README.md)
records #1015 and then this claim at 127, below #1015, and #1020 after it.

## Pose by Pose

`devtools.measure_identity` wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **Against #1015’s packing.** One to one by nearest centres under the identity of the
  box, which moves 63 squares beyond 10⁻³, 27 beyond 0.01 and 5 beyond 0.1 (largest
  0.328312) and turns squares by up to 1.495 degrees; all 57 tilted squares pair with
  tilted squares of the same sign. So it is #1015’s arrangement, its cap moved as the
  issue says.
- **Against T-305.** No symmetry pairs them one to one; the optimal assignment moves 11
  squares beyond 0.1 (largest 0.789453), as #1015’s does.

## The Gain Against Padding

`devtools.contraction_margin`, each contracted packing decided on both routes:

- **#1015’s certificate**: margin 7.7394 × 10⁻⁶³ (squares 31 and 34)
  ([measure/contraction-n127-1015.json](measure/contraction-n127-1015.json)); the step
  from it, 1.9556 × 10⁻⁶, lies wholly outside it, so under the owner’s option D of 17
  November (think-b0w5) this certificate is a new result, not a restatement of #1015’s
  packing.
- **The house**, T-305: margin 1.2099 × 10⁻¹⁰
  ([measure/contraction-n127.json](measure/contraction-n127.json)).
- **This certificate**: margin 4.1903 × 10⁻¹⁴ (1 − λ\* about 3.8484 × 10⁻¹⁵, squares 35
  and 88) ([measure/contraction-n127-own.json](measure/contraction-n127-own.json)).

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json), with this side stood in for 127’s
ceiling, finds exactly `main`’s consequences; no bound carries.

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
decisions, 4.81 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes, as planned. Squares touch the box at the near walls, a least clearance of exactly 0; the far walls clear by 3.3728 × 10⁻¹⁶.
Every pair clears by at least 3.8484 × 10⁻¹⁵ (squares 35 and 88). `check --replay` decided the
three jobs again.

`sharp-controls` took the certificate to exact contact and 10⁻³⁰ past it on both routes
([receipts/sharp-controls.json](receipts/sharp-controls.json), 19 CPU seconds),
and all 11 came out as the plan stated. The box lowered to its extent (3.3728 × 10⁻¹⁶ below the side), the tightest pair closed (88 toward 35) and every square moved toward its near wall by 0, each accepted at contact and refused 10⁻³⁰ past it; square 88 enlarged to 35 refused at contact for its shape alone; square 43, at its wall, grown by 0 and accepted; both refused past contact for the overlap or the wall as well; and a duplicated square refused. The two routes, the `sqpack`
rational witness verifier and the independent rational corner checker, share this
repository’s certificate readers (the `center-direction-json` adapter and the half-angle
conversion), `Fraction` arithmetic and the separating-axis method; neither is the
author’s code, and neither shares code with it.

## Stage 4 Review

The blind stage 4 review of the three certificates at 127 is lane R-127’s (under
think-zqot); this lane has not read it.

## What Is Not Established

- **The search**: the search over the band’s column offsets, the second stage’s changes of aspect ratio and the optimization are
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
**[de Winter s127 issue 1017 2026-11-17]**. `LICENSE` at the pin is de Winter’s MIT
licence, and the root README says all files are released under it.

## Commands

From `packing/`, with the project interpreter:

```bash
P=de-winter-s127-issue1017-2026-11-17
H=joegun-upper-bounds-2026-11-16
M=resources/web/$P/measure
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 127 "DEWINTER-1017=packet:$P" "T-305=packet:$H" \
  'DEWINTER-1015=packet:de-winter-s127-issue1015-2026-11-17' --out $M/identity.json
python -m devtools.contraction_margin --n 127 "T-305=packet:$H" \
  --against "DEWINTER-1017=packet:$P" --out $M/contraction-n127.json
python -m devtools.contraction_margin --n 127 \
  'DEWINTER-1015=packet:de-winter-s127-issue1015-2026-11-17' \
  --against "DEWINTER-1017=packet:$P" --out $M/contraction-n127-1015.json
python -m devtools.contraction_margin --n 127 "DEWINTER-1017=packet:$P" \
  --out $M/contraction-n127-own.json
python -m devtools.l_step_scan --with 127=S127 --out $M/l-step-scan.json
```

In the last command `S127` is the `exact_side` in the packet’s claim record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
