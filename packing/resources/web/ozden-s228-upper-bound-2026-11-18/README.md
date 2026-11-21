# Doğa Özden’s s(228) Certificate at 46ab8bf

This packet retains
[kenaznia-doga/s228-upper-bound-1559604311](https://github.com/kenaznia-doga/s228-upper-bound-1559604311/tree/46ab8bf425f5cad886a8bc4023bfff904f43af99)
at `46ab8bf425f5cad886a8bc4023bfff904f43af99` (committed 2026-11-18T23:08:45Z), the
repository’s one commit, which
[issue #1038](https://github.com/jlevy/squares/issues/1038) names 23 seconds later.
Doğa Özden’s AI agent, which uses the account kenaznia-doga, prepared and posted both on
his behalf. The lane fetched the repository at 08:14Z on 20 November; #1038 had no
comment then.

Intake lane i1038 (think-91fu) retained it, replayed it and measured it on 20 November
2026\. Its stage 4 review was a separate lane, blind to this one (think-3ape), and is
mapped below.

## What the Source Claims

- `n-228-candidate.yaml`, a `packing.squares:Witness/v2` file (centre and rational
  half-angle basis, rational scalars, 228 squares), bounds s(228) by its exact side,
  389901077915794162667528670804703057/25000000000000000000000000000000000 =
  15.59604311663176650670114683218812228, which terminates at 35 places.
  #1038 prints its 12-place ceiling, 15.596043116632, and says it is 4.289 × 10⁻⁹ below
  the record, 15.5960431209207917 (T-301, Roberto Ono’s), relative 2.75 × 10⁻¹⁰. It
  claims an upper bound only: no optimality, KKT or rigidity claim.
- **Where the packing comes from.** The issue says it is not the lab’s own search result
  but a public Kaggle packing by jazivxt: the notebook *Boxed In Sub* (run 370961355),
  which copies the `submission.csv` of the dataset *Boxed In* v63, Apache 2.0 as
  declared there. The lab converted jazivxt’s decimal centres and orientations to
  rational half-angle form and applied one uniform clearance factor about the origin,
  2500000000000011391221/2500000000000000000000, so that every pair has strictly
  positive clearance; nothing else changed.
  The issue, the README and the file print the factor as 1 + 4.6 × 10⁻¹⁸; it is 1 +
  4.5564884 × 10⁻¹⁵ (the stage 4 review’s F6 and F15), and the origin is the box centre,
  since jazivxt’s slice is in centred coordinates (F13).
  `checks/source-exact-as-produced.json` is the unmodified conversion output and
  `source/hit-228.txt` jazivxt’s decimal slice, side 15.59604311663169367…, 7.28 × 10⁻¹⁴
  below the certificate’s, the cost of the clearance.
- **Credit, as the source states it.** The packing is jazivxt’s; the dataset describes
  crowdsourced coordinates and the notebook gives no per-count credit, so the original
  finder of this arrangement is unresolved.
  The notebook’s overview credits ChatGPT and Codex.
  The exact certificate and the registration are Özden’s, with his lab’s OpenAI Codex
  assistance, and he claims no discovery.
  Sergio Fernández Rubio (GeiserX), whose round-30 table credits jazivxt’s notebook at
  228, is named as a cross-check source: `source/geiserx-rounded/` holds his rounded
  layout, the same packing to 2.3 × 10⁻¹⁰, and its checks.
- **Checks.** `verify-228.txt` is the author’s unmodified run of this repository’s
  `packing-witness verify` (VERIFIED, exact-algebraic over Q, 25,878 pairs, least wall
  clearance 0), and `checks/registry-verify.json` reports the same run’s least pair gap.
  `sqcheck-228.txt` is the author’s run of `verifier/sqcheck.py`, an exact checker the
  lab wrote separately (VALID, exact rational, the side rounded up at 15 places), and
  `checks/hit-228-independent.json` a second exact `Fraction` separating-axis checker
  the issue says was written independently (VALID, 151 near pairs).
  The issue says the checkers share only the definitions of unit square, wall and
  non-overlap. Those statements are the author’s; no source program ran here.
- **Identity, as the source measures it.** Matched against T-301’s packing up to the
  square’s eight symmetries, 86 of 228 centres move by more than 0.001, 7 by more than
  0.05 (largest 0.238), and 2 squares retilt by more than a degree; a close relative of
  the registry arrangement, with no information on which came first or whether one
  derived from the other.
- **Other public values.** The issue discloses first a side-only Kaggle per-puzzle
  leaderboard entry at 228, 15.596043116631669919627353… (Nevska, 8 November), 9.66 ×
  10⁻¹⁴ below this side, which this packing does not beat and which states no packing.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the whole tree, 28 files, 703,927 bytes: 24 retained under
[source/](source/), three of them stored as deterministic gzip by the archive’s rule,
and four pinned only.
`verifier/sqcheck.py` and `verifier/README.md` are byte-identical to the copies the
[ozden-s232-upper-bound-2026-11-09](../ozden-s232-upper-bound-2026-11-09/README.md) and
[ozden-s299-upper-bound-2026-11-03](../ozden-s299-upper-bound-2026-11-03/README.md)
packets retain, and each is pinned against its copy.
The two comparison figures under `records/` are pinned by digest only.
The certificate has the SHA-256 the issue and the README state, `1b816e2e…3387`.

**Kaggle was not read.** This session’s network proxy refuses `www.kaggle.com` (CONNECT
403 at 08:21Z on 20 November 2026), so neither the notebook nor the dataset was fetched.
jazivxt’s coordinates are retained only as the source holds them, `source/hit-228.txt`,
and the notebook’s and dataset’s dates, licence and credit only as `PROVENANCE.json`,
`checks/AUDIT-228.json` and the README state them.
Nothing here dates jazivxt’s packing.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `935e79c36`:

| Compared with | Side | Below it by |
| --- | --- | --- |
| T-301, Roberto Ono’s packing, the house in both lanes | 15.5960431209207917 | 4.28903 × 10⁻⁹ |

No other register bound was pending adoption at 228. The lower bounds at 228 lie below
the side.

## Report Order

The
[ledger of 20 November for this lane](../../../campaign/issue-intake/upper-bounds-1038-20261120/README.md)
walks #1038 from a start frozen on `main` `935e79c36` and records it, below T-301. The
source classifies the packing neither as a refinement nor as a new arrangement, so the
ledger records it unclassified, with the measurement below.
The side-only leaderboard entry the issue quotes states no packing and is context only.

## Exact Replay

The checks below were planned before any of them ran: the expected verdict of every
gross and sharp control was written down at 08:22Z on 20 November and its SHA-256,
`a8b9a8c6014168a4d750b1e1e9d98899d5abfc7e11877ec7436a2c194a8d61e1`, recorded on the bead
at 08:22:23Z, with two branches stated in advance, a square that touches its wall
exactly and a pair whose gap exceeds the controls’ step.
The plan is retained as
[receipts/controls-plan-1038.md](receipts/controls-plan-1038.md).
Before it, only `sha256sum`, `devtools.contraction_margin` and
`devtools.measure_identity` had read the certificate; the contraction measurement
decided the certificate as given on both routes, which no control repeats.

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 155,268 pair decisions, 16.96 route CPU seconds on a host shared with
other lanes
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 3.62674 × 10⁻²³, squares 156 and 166, the margin the author’s checks report.
`check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it on both routes
([receipts/sharp-controls.json](receipts/sharp-controls.json), 66 CPU seconds), and all
11 came out as stated, the branch for a touching square taken, both routes agreeing on
every verdict and margin:

- **Wall, pair and near-wall.** The box lowered to the extent (by 0), the tightest pair
  closed (square 166 toward 156, by its gap) and every square moved toward its near wall
  by the least near-wall clearance, 0: each accepted at exact contact and refused 10⁻³⁰
  past it.
- **Enlarged to a pair.** Square 166, enlarged against 156, refused at contact for its
  shape alone, and past it for the overlap as well.
- **Enlarged to a wall.** Square 1, already at its wall, grown by 0: accepted at
  contact, and refused 10⁻³⁰ past it for the wall and its shape.
- **Duplicate.** A duplicated square is refused.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share this repository’s centre-basis witness reader (certificate parsing
and half-angle conversion), `Fraction` arithmetic and the separating-axis method.
The first is the `packing-witness verify` the author ran, so on that route the replay is
reproduced with the producer’s code; the independent rational corner checker shares no
geometry or verification code with `sqpack.witness` or `sqpack.verify`. The lab’s own
conversion made the exact coordinates, not this repository’s promotion.
Neither route is the author’s `sqcheck.py` or second checker, which were not run.

## The Gain Against Padding: Option D

The owner’s option D of 17 November 2026 (think-b0w5): a re-certification of a standing
packing is a new result only if its side is below the predecessor’s once the predecessor
is itself shrunk until its squares first touch.
`devtools.contraction_margin` contracted each certificate uniformly about the origin to
first contact and boxed it, each contracted packing decided on both maintained routes:

- **The house**, T-301 at 228: margin 3.4875 × 10⁻⁹ (1 − λ\* about 2.389 × 10⁻¹⁰,
  squares 8 and 21), contracted side 15.59604311743328…, which rounds up at 12 places to
  15.596043117434 ([measure/contraction-n228.json](measure/contraction-n228.json)). The
  gain, 4.2890 × 10⁻⁹, is 1.2298 times the margin: this certificate lies 8.015 × 10⁻¹⁰
  below T-301 shrunk to first contact, so under option D it is a new result.
- **This certificate**: margin 4.3896 × 10⁻²² (1 − λ\* about 3.007 × 10⁻²³, squares 156
  and 166), the clearance factor’s
  ([measure/contraction-n228-own.json](measure/contraction-n228-own.json)). Contracted,
  it would be a square that much smaller, which nobody reported and which is not
  registered.

## Pose by Pose

`devtools.measure_identity` wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.
Nearest centres pair the certificate one to one with T-301’s packing under the identity
of the box, and the house witness measures as T-301’s packet.
The optimal assignment moves 86 squares beyond 10⁻³, 47 beyond 0.01 and 5 beyond 0.1
(largest 0.238073), and turns 50 squares by more than 10⁻⁶ radians, by up to 1.956
degrees; aligned by box centres, 2 squares turn by more than a degree and none reverses
its tilt. Tilted beyond a degree: 54 here, at 41.00 to 42.10 degrees, 19 one way and 35
the other, against T-301’s 55, at 1.29 to 43.68 degrees, 19 and 36. The case’s drawn
view, the axis tool’s view of T-301’s witness, is not paired one to one with it by
nearest centres (18 squares beyond 0.1). Against T-300 no symmetry pairs it one to one,
and 96 squares move beyond 0.1. The optimal assignment against T-301 moves five
squares beyond a tenth. The issue gives seven moves beyond 0.05 for a placement it
does not name. Finder and publication order remain unresolved.

## The Project’s Held Solve at 228

The project’s run of Evan Daniel’s driver on T-301’s witness on 15 November 2026
([think-17ex-2026-11-15](../../../cases/regularized_drawings/think-17ex-2026-11-15/README.md))
reached a local minimum of the side, strict modulo 129 exact flat motions, and its
solved view, which both maintained routes accepted, has side
3899010779157917479945828568311/250000000000000000000000000000 =
15.596043116631669919783314273244, 9.66 × 10⁻¹⁴ below this certificate and below T-301
shrunk to first contact by 8.016 × 10⁻¹⁰. The driver’s KKT certificate did not validate;
the view was held at row 3 as a register candidate, not registered, and is not retained.
Its side agrees with the leaderboard entry the issue quotes at all 24 printed places.
This certificate’s packing may be that minimum opened by its clearance factor. A
pose comparison with the held view remains pending. Özden reported his certificate
while that view remained unregistered. Under the owner’s decision of 18 November 2026
at #1009’s five re-solves (think-frl5), his claim keeps its new-result status, and the
held view stays a candidate
for registration (think-4z8z).

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json) is `devtools.l_step_scan` with this
side stood in for 228’s ceiling.
It finds exactly main’s L-step and monotonicity consequences, so no bound carries to
another count.

## Stage 4 Review

The blind stage 4 review of this certificate is lane r1038’s (think-3ape):
[review-2026-11-20-ozden-1038.md](../../../../docs/project/reviews/review-2026-11-20-ozden-1038.md),
merged at 09:34Z on 20 November and read at 09:37Z, after this packet’s replay,
controls, measurements and registration were committed at 08:50Z, and mapped then.
It accepts the certificate, decided by a clean-room checker by two exact methods with 36
controls stated in advance, with no blocking or major finding.
Its least margin, 3.62672 × 10⁻²³ at squares 156 and 166, is the replay’s; it finds 33
exact wall contacts at all four walls (F1, F4), the factor the source prints as 1 + 4.6
× 10⁻¹⁸ to be 1 + 4.5564884 × 10⁻¹⁵ (F6, F15), and the certificate to be a packing of
side 15.5960431166317 exactly, with 197 pairs at contact and 16 overlapping by up to
5.49 × 10⁻¹⁵, opened by that factor about the box centre (F7, F13). After its freeze it
measured the identity, the contraction margins and the held view’s side as this packet
does, with the same results (F10 to F12), and proposes S2. T-334 is confirmed,
independently re-implemented, at V3/C3.

## What Is Not Established

- **Which came first.** Nothing here dates jazivxt’s packing, and the source has no
  information on whether it and T-301’s derive from each other; Kaggle was not read.
- **The original finder** of the arrangement in the crowdsourced dataset.
- **Local optimality, rigidity or KKT**: not claimed by the source.
- **Human oversight**: no record is retained.

## Credit and Licence

Jazivxt published the public Kaggle snapshot and Doğa Özden prepared the exact
certificate and submitted it.
Roberto Ono retains the packing credit on T-301. The one-to-one measurement compares the
two geometries.
The finder of the published snapshot, the order in which the two packings
appeared, and any derivation remain unresolved.
The packet records AI assistance as stated by the source under the project’s
[attribution policy](../../../../attribution.md).
The bibliography key is **[Özden s228 upper bound 2026-11-18]**.

`LICENSE.md` at the pin licenses the witness, data and text under CC BY 4.0 and
`sqcheck.py` under MIT, copyright 2026 Doğa Özden, byte-identical to the lab’s earlier
repositories’ `LICENSE.md`, and says the coordinates remain jazivxt’s under Apache 2.0.
`source/LICENSE-jazivxt-Apache-2.0` is the Apache License 2.0 text the source bundles.
`source/NOTICE`, `source/CITATION.cff` and `source/LICENSE-CC-BY-4.0.txt` are Sergio
Fernández Rubio’s, kept with his layout as his NOTICE requires.

## Commands

From `packing/`, with the project interpreter.
The identity measurement reads the house witness and its drawn view as they stood at
`main` `935e79c36`, before any adoption replaced them, so it reproduces there; the
contraction margins read the packets and reproduce anywhere
`devtools.contraction_margin` is:

```bash
P=ozden-s228-upper-bound-2026-11-18
M=resources/web/$P/measure
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 228 "OZDEN=packet:$P" \
  'T-301=packet:ono-issue984-2026-11-14' \
  'T-300=packet:ozden-s228-upper-bound-2026-11-14' \
  'house-witness=witness-center-basis:witnesses/known-best/n-228.yaml' \
  'regularized=witness-corners:atlas/known-best/regularized/n-228-regularized.yaml.gz' \
  --out $M/identity.json
python -m devtools.contraction_margin --n 228 'T-301=packet:ono-issue984-2026-11-14' \
  --against "ozden-1038=packet:$P" --out $M/contraction-n228.json
python -m devtools.contraction_margin --n 228 "ozden-1038=packet:$P" \
  --out $M/contraction-n228-own.json
python -m devtools.l_step_scan --with 228=S228 --out $M/l-step-scan.json
```

In the last command `S228` is the `exact_side` in the packet’s claim record.

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/checks/source-exact-as-produced.json.gz` | upstream | `cf85d22ee74154776ceb73867f1e1dd2a0eb8185` | `c149799d7d0efcd3c4c89ede54f836926b9e60098fc935df76b4c1f66478a2d9` |
| `source/n228-witness.json.gz` | upstream | `22c0a1c7aa581ce83917e314eed3815b5a8afdff` | `302b619f5f8c784869b60a411d17bc6c1a62a906a52d332f6cf9836e1e623752` |
| `source/source/geiserx-rounded/hit-228-exact.json.gz` | upstream | `e0a8e66f70ea7d18445ed54a50fd8b7c89ce59d0` | `c7cb523dbc9b75fdf26b5d6be3c55d31ef77f0456945883bda5524d610a40c37` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
