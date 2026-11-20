# Joost de Winter’s s(127) Certificate of Issue 1020, at a1ba501

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/a1ba5019e787e407646293d7bef81d63c9951b32),
a watched repository, at `a1ba5019e787e407646293d7bef81d63c9951b32` (committed
2026-11-17T22:48:48Z, “Add packings for n = 268 and n = 270 and a smaller certificate for
n = 127”), the commit [issue #1020](https://github.com/jlevy/squares/issues/1020) names 47
seconds later; it was pushed with the head, `838c5ea`, at 22:48:50Z. It replaces the
certificate, the witness and the figure of `cc20a26`, which
[#1017](https://github.com/jlevy/squares/issues/1017) reports and the
[de-winter-s127-issue1017-2026-11-17](../de-winter-s127-issue1017-2026-11-17/README.md)
packet retains, with a packing 1.7976 × 10⁻¹³ smaller, and adds `n268/` and `n270/`, which
#1021 and #1022 report and think-gqzz imports; they are not in this packet’s scope. The
head adds only the registration texts and checksums. The lane fetched the repository at
01:21Z on 18 November, when `git ls-remote` read the head as `838c5ea`.

Intake lane w6-dewinter-1118 (think-zqot) retained it, replayed it and measured it on 18
November 2026. It is the third and lowest of de Winter’s three reports at 127 that
evening, after [#1015](https://github.com/jlevy/squares/issues/1015) and #1017.

## What the Source Claims

- `n127/n127_exact.json` states 127 unit squares as centre and unit edge direction rows
  of exact rationals, with the side
  5900396863307481119664515678048233366964863482714849291045437/500000000000000000000000000000000000000000000000000000000000.
  #1020 and the root README round it up at 12 places as 11.800793726615, and
  `n127/README.md` prints it with 11.800793726614963. `n127/n127_witness.yaml` is the
  same packing as a corner Witness/v2 of rationals. The issue names the record’s
  11.8017538904864874 (T-305) and the gain, 0.00096, and says later commits leave these
  files unchanged.
- **Construction.** A tilted central band of 57 squares inside a frame of axis-aligned
  squares, from the arrangement in the Chilton and Panoras compilations: the search
  changed the sliding offsets of the band’s columns, shifted two groups of squares in the
  band lengthwise, and optimized the positions and angles of all squares.
- **Checkers.** `verify_exact.py` and `check_area.py`, unchanged from `35b576a`; the issue
  says each reports 127 squares and 308 close pairs. Those statements are the author’s;
  no source program ran here.
- **Not done.** No test of local optimality. The packing is 2.2 × 10⁻¹² below Luka
  Cvetkovic’s Kaggle side, 11.800793726617185 (notebook version 370726548, 16 November),
  so the issue says the two are probably the same local optimum; his coordinates were not
  found.
- **Credit and AI assistance.** Joost de Winter, after the arrangement in the Chilton and
  Panoras compilations. The issue names GPT-6.2 Astra (OpenAI) for the search,
  optimization and rational certificate, where the pin’s `n127/README.md` and the head’s
  `n127/REGISTRATION.md` name GPT-6.2 Sol, and Claude (Anthropic) for the repository
  files, checks and figure, both under his direction.

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
digest only. The pin’s `n127/SHA256SUMS` and `n127/REGISTRATION.md` are `67fb815`’s, which describe #1017’s certificate; the head’s digests of the certificate, the witness, the figure, the two checkers and `n127/README.md` match the pin’s files.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `eb50f54e9`. `center-direction-json` reads the certificate, and
`witness-corners-opposite` its corner twin; the two state the same packing exactly.

| Compared with | Side | Below it by |
| --- | --- | --- |
| T-305, Tomáš Kodaj’s Kaggle packing as JoeGun improved it, the house in both lanes | 11.8017538904864874 | 9.6016 × 10⁻⁴ |
| #1015, de Winter’s certificate | 11.8007956822135694… | 1.9556 × 10⁻⁶ |
| #1017, de Winter’s certificate, filed just before it | 11.800793726615142 | 1.7976 × 10⁻¹³ |

## Report Order

The
[ledger of 18 November for this lane](../../../campaign/issue-intake/upper-bounds-1015-1020-20261118/README.md)
records #1015, #1017 and then this claim at 127, each below the last. Its 12-place print,
11.800793726615, differs from #1017’s, 11.800793726616, so the restatement ruling of 23
October (think-fwa9) does not reach it.

## Pose by Pose

`devtools.measure_identity` wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **Against #1017’s packing.** One to one by nearest centres under the identity of the
  box, which moves 46 squares beyond 10⁻³, 28 beyond 0.01 and 1 beyond 0.1 (largest
  0.107338) and turns squares by up to 3.981 degrees; all 57 tilted squares pair with
  tilted squares of the same sign within 0.1 degrees, 52 of them within 10⁻⁴ degrees. So
  it is #1017’s arrangement, two groups of the band moved, as the issue says.
- **Against #1015’s packing**: one to one too; 5 squares move beyond 0.1 (largest
  0.289626).
- **Against T-305.** No symmetry pairs them one to one; the optimal assignment moves 9
  squares beyond 0.1 (largest 0.789453).

## The Gain Against Padding

`devtools.contraction_margin`, each contracted packing decided on both routes:

- **#1017’s certificate**: margin 4.1903 × 10⁻¹⁴ (squares 35 and 88)
  ([measure/contraction-n127-1017.json](measure/contraction-n127-1017.json)); the step
  from it, 1.7976 × 10⁻¹³, is 4.29 times that, so this side lies 1.3786 × 10⁻¹³ below
  #1017’s certificate shrunk to first contact. Under the owner’s option D of 17 November
  (think-b0w5) this certificate is therefore a new result, not a restatement of #1017’s
  packing; it is the narrowest of the three steps, about four times the padding.
- **The house**, T-305: margin 1.2099 × 10⁻¹⁰
  ([measure/contraction-n127.json](measure/contraction-n127.json)).
- **This certificate**: margin 1.8203 × 10⁻⁵⁸ (1 − λ\* about 1.6483 × 10⁻⁵⁹, squares 84
  and 99) ([measure/contraction-n127-own.json](measure/contraction-n127-own.json)).

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
decisions, 12.90 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes, as planned. No square touches the box: every wall is cleared by at least 2 × 10⁻⁶⁰ (exactly 1/(5 × 10⁵⁹)).
Every pair clears by at least 1.6483 × 10⁻⁵⁹ (squares 84 and 99). `check --replay` decided the
three jobs again.

`sharp-controls` took the certificate to exact contact and 10⁻³⁰ past it on both routes
([receipts/sharp-controls.json](receipts/sharp-controls.json), 51 CPU seconds),
and all 11 came out as the plan stated. No square touches a wall, so the branches taken were those of a clearing certificate: the box lowered to its extent (2 × 10⁻⁶⁰ below the side), the tightest pair closed (99 toward 84) and every square moved toward its near wall by 2 × 10⁻⁶⁰, each accepted at contact and refused 10⁻³⁰ past it; square 99 enlarged to 84 and square 91 enlarged to its wall, each refused at contact for its shape alone and past it for the overlap or the wall as well; and a duplicated square refused. The plan expected the near-wall move to be 0; it was 2 × 10⁻⁶⁰, the branch for a clearing square, and every verdict was the one stated. The two routes, the `sqpack`
rational witness verifier and the independent rational corner checker, share this
repository’s certificate readers (the `center-direction-json` adapter and the half-angle
conversion), `Fraction` arithmetic and the separating-axis method; neither is the
author’s code, and neither shares code with it.

## Stage 4 Review

The blind stage 4 review of the three certificates at 127 is lane R-127’s (under
think-zqot); this lane has not read it.

## What Is Not Established

- **The search**: the search over the band’s column offsets, the shifts of two groups in the band and the optimization are
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
**[de Winter s127 issue 1020 2026-11-17]**. `LICENSE` at the pin is de Winter’s MIT
licence, and the root README says all files are released under it.

## Commands

From `packing/`, with the project interpreter:

```bash
P=de-winter-s127-issue1020-2026-11-17
H=joegun-upper-bounds-2026-11-16
M=resources/web/$P/measure
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 127 "DEWINTER-1020=packet:$P" "T-305=packet:$H" \
  'DEWINTER-1017=packet:de-winter-s127-issue1017-2026-11-17' \
  'DEWINTER-1015=packet:de-winter-s127-issue1015-2026-11-17' --out $M/identity.json
python -m devtools.contraction_margin --n 127 "T-305=packet:$H" \
  --against "DEWINTER-1020=packet:$P" --out $M/contraction-n127.json
python -m devtools.contraction_margin --n 127 \
  'DEWINTER-1017=packet:de-winter-s127-issue1017-2026-11-17' \
  --against "DEWINTER-1020=packet:$P" --out $M/contraction-n127-1017.json
python -m devtools.contraction_margin --n 127 "DEWINTER-1020=packet:$P" \
  --out $M/contraction-n127-own.json
python -m devtools.l_step_scan --with 127=S127 --out $M/l-step-scan.json
```

In the last command `S127` is the `exact_side` in the packet’s claim record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
