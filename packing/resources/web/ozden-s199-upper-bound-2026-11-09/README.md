# Doğa Özden’s s(199) Certificate at d03ee0b

This packet retains
[kenaznia-doga/s199-upper-bound](https://github.com/kenaznia-doga/s199-upper-bound/tree/d03ee0bdb223e00fe124e818ed242f6cbd714fad)
at `d03ee0bdb223e00fe124e818ed242f6cbd714fad` (committed 2026-11-09T20:30:58Z), the
repository’s first commit, which [issue #938](https://github.com/jlevy/squares/issues/938)
names 34 seconds later. Doğa Özden’s AI agent, which uses the account kenaznia-doga,
prepared and posted both on his behalf.
One later commit, `4fbff7b` (20:53:14Z), changes one line of `README.md` to add a Kaggle
side-only leaderboard entry; it is read in
[intake-watch.yaml](../../../campaign/intake-watch.yaml) and not retained.

## What the Source Claims

- `n-199-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational scalars,
  199 squares), bounds s(199) by its exact side, a fraction of about 90 digits whose
  16-place ceiling is 14.6146898532862152. #938 prints its 12-place ceiling,
  14.614689853287, and says it is 2.882e-03 below the record, Nate Chaoweeraprasit’s
  packing refined by Siddharth Gupta (T-127). It claims an upper bound only: no KKT,
  local-optimality, rigidity or global-optimality claim.
- **What it is.** Squares 1 to 172 are Özden’s n = 172 witness of
  [#935](https://github.com/jlevy/squares/issues/935) (T-282, adopted at 172 that
  afternoon), its rational corners unchanged; squares 173 to 186 are a row of 14
  axis-aligned unit squares along the top wall and 187 to 199 a column of 13 along the
  right wall. The side is exactly S₁₇₂ + 1. The issue says nothing was searched at 199,
  and that the gain is inherited from #935 through the L step
  s(n + 2⌊s⌋ + 1) ≤ s(n) + 1, with ⌊S₁₇₂⌋ = 13 and 172 + 27 = 199. It says it found no
  automatic propagation of the step in the registry, so it files the bound as its own
  witness, and that it checked every count of the site’s `frontier_all` for the same step
  from any other record: only 199 improves, and s(198) = 14 + 4/7 keeps 199 monotone.
- **The margins.** The 172 part keeps #935’s pair gaps of about 2 × 10⁻¹³. The grid
  squares touch each other, the walls and the 172 part’s bounding square exactly, so the
  exact minimum pair gap is 0. `sqcheck.py` certified the decimal pose,
  `n-199-decimal-pose.yaml`, in interval arithmetic only with a dilation of 10⁻²⁴.
- `n199-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the
  author’s run of this repository’s `packing-witness verify` at main `200f2ebc` (VERIFIED,
  19,701 pairs); `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an
  exact checker the source says was written separately from this repository’s code
  (VALID, exact rational). `.meta.json` repeats the claim’s figures: the exact side, the
  print, the record’s exact side, the gain 2.882e-03 (relative 1.97e-04), both digests and
  19,701 pairs. The issue says the two checkers share only the unit-square, wall and
  non-overlap definitions, and that `packing-witness verify` is not independent of how
  the 172 part’s coordinates were rounded, since this repository’s promotion tool made
  them. Those statements are the author’s; no source program ran here.
- One print in the source’s README is off in its last digit: it writes S₁₇₂ as
  13.6146898532862153…, where the exact side is 13.61468985328621510… (rounded up at 16
  places, 13.6146898532862152, as T-282 prints it). The witness, the issue and the 199
  side’s prints are right.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the whole tree, 13 files: 8 retained under
[source/](source/) and 5 pinned by digest.

| File | Bytes |
| --- | --- |
| `.meta.json` | 565, the claim’s figures as the lab’s tooling wrote them |
| `LICENSE.md` | 1,484 |
| `README.md` | 5,367 |
| `n-199-candidate.yaml` | 543,653 |
| `n-199-decimal-pose.yaml` | 21,717, #935’s search pose with the 27 grid squares at decimal centres |
| `n199-witness.json` | 537,289, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 362 |
| `sqcheck-output.txt` | 272 |
| `LICENSE-evand-square-packing.txt` | 1,068, pinned against the identical copy of Evan Daniel’s MIT notice the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains |
| `records/n-199-packing.png` | 100,454, pinned by digest: a drawing that decides nothing |
| `records/n-199-packing.svg` | 26,785, pinned by digest: the same drawing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [9 November s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256s the issue states for `n-199-candidate.yaml` (`8a85b4c3…8aca`) and the README
and `.meta.json` state for `n199-witness.json` (`88d20ae2…4cb8`) are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about 1.3 megabytes in a checkout and far less as Git stores it, so it is
kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `200f2ebc1` on 9 November
2026):

- **199:** exact side 14.6146898532862152 rounded up at 16 places, below the case’s
  house (T-127, Nate Chaoweeraprasit, improved by Siddharth Gupta) by 2.882e-03, as the
  issue states, and below the two re-certifications of the house’s packing pending
  adoption there, T-174 (PingYou Ltd) and T-193 (Evan Daniel’s exact side), each
  1.46 × 10⁻¹⁹ below the house.

## The Construction

The certificate is T-282’s retained certificate with the L step, pose for pose:
`tests/test_upper_bound_reports_l76_1109.py` reads both packets through their custody and
holds the 199 certificate equal to what `devtools.construction_checker.write_out`, the
maintained checker of recipe rows, writes for one L-border layer on T-282’s certificate:
the same 172 poses, then ⌊S₁₇₂ + 1⌋ = 14 unit squares along the top from the left wall and
⌊S₁₇₂⌋ = 13 up the right wall from the floor, at side S₁₇₂ + 1, 172 + 27 = 199 squares by
the checker’s capacity.

## Report Order and the L Step

The
[ledger of 9 November for this lane](../../../campaign/issue-intake/upper-bounds-938-20261109/README.md)
walks every report at 199 in the order it reached this repository, from starts frozen at
`main` `200f2ebc1`, and records this packet’s claim. The best published Kaggle per-puzzle
side the issue quotes at 199, 14.617572173606 (kirilltym), is above this and states no
packing. The author’s comment of 20:53:05Z adds a side-only leaderboard entry,
14.6132098756 (team OigaZhDn, 31 October), below this side; it states no packing and is
no report.

No rule of the record carries an L step inside the case corpus: the one for recipes on a
certificate, D2, reads rows beyond 324 that a source states, and whether S + 1 on a
published certificate is that publication’s own report inside the corpus is the owner’s
open question RV-4 (think-ruu2). So the bound reaches the record as #938’s report, with
its own witness, and the credit is Özden’s whichever way RV-4 is answered, since #935 is
his too. The record had measured it all the same: X049’s family census, derived again
when T-282 was adopted, has listed 199 as its one `bound_violations` entry since then, a
margin of −0.002882320307 from 172, and nothing reads that list.

`devtools.l_step_scan` decides the step and monotonicity exactly from every case’s
verified ceiling ([measure/l-step-scan.json](measure/l-step-scan.json), main `200f2ebc1`).
It agrees with the issue that 199 is the one count the step improves across its 12-place
print, from 172 by 2.882e-03, and that monotonicity improves none. It also finds what the
census’s tolerance of 10⁻⁹ cannot: ten steps that improve a ceiling by 4.8 × 10⁻³³ to
1.76 × 10⁻¹⁹, inside its print, at 101, 125, 170, 174, 198, 201, 257, 262, 292 and 298,
the padding class think-ruu2’s RV-3 puts to the owner. With this side standing at 199
([measure/l-step-scan-adopted.json](measure/l-step-scan-adopted.json)), 199 is an
L-extension of 172 and the step from it, at 228, stays above that count’s ceiling, so
nothing further moves.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-127’s packing, the house
witness, and its regularized view, and wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **199:** no symmetry pairs it one to one with T-127’s packing by nearest centres; the
  optimal assignment, under a reflection, moves 81 squares beyond 0.1 and 117 beyond 0.01
  (largest 1.006) and turns 69 by more than 10⁻⁶ radians. It has 49 squares tilted beyond
  1 degree, 36 one way and 13 the other, where T-127 has 47, 13 and 34. Against the
  regularized view the assignment moves 66 squares beyond 0.1. So it is another
  arrangement than the house’s at 199. The lineage the record holds connects them: T-257,
  Evan Daniel’s 172 that T-282 rearranges, came from this count’s record by an explorer
  search and the removal of one L-shaped strip (#845).

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 118,206 pair decisions, 42.6 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and the least pair gap is
exactly 0, where the grid squares touch.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
1e-30 past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)). Since its
least far-wall clearance, least pair gap (squares 173 and 174 of the top row) and least
near-wall clearance are all 0, the at-contact half of those three controls is the
certificate itself, which both routes accept, and the 1e-30 half the mutant, which both
refuse, as at the 293 L-strip candidate of 31 October (think-ruu2) and T-156.
The routes refused one square enlarged to its pair (161 against 199, a positive gap) at
contact for its shape alone, accepted square 46, already touching its wall, at contact,
refused each 1e-30 past it for the overlap or the wall as well, and refused a duplicated
square.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the witness through the `witness-corners`
reader. The first route is the `packing-witness verify` the author ran on the same file,
so on that route the replay is reproduced with the producer’s code; the second shares no
verification code with it. Neither is independent of this repository’s `packing-witness
promote`, which made the 172 part’s coordinates. The source’s own `sqcheck.py` was not
run.

## The Gain Against Padding

T-127’s certificate carries padding of its own: contracted uniformly about the origin to
first contact and boxed, its packing loses 1.46 × 10⁻¹⁹ of side (1 − λ\* = 10⁻²⁰).
The gain this certificate states, 2.882 × 10⁻³, is about 2.0 × 10¹⁶ times that margin,
so no share of it worth stating is the house’s padding. This certificate’s own margin,
measured the same way, is exactly 0: λ\* = 1, the binding pair two touching squares of
the top row. `devtools.contraction_margin` wrote both receipts,
[measure/contraction-n199.json](measure/contraction-n199.json) and
[measure/contraction-n199-own.json](measure/contraction-n199-own.json), each contracted
packing decided on both maintained routes; it accepts a witness whose squares touch.

## What Is Not Established

- **Review.** The stage 4 review is a separate lane’s, not yet mapped.
- **Human oversight.** None.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurements above show.

## Credit and Licence

The packing is Doğa Özden’s #935 packing at 172, found from the registry’s 172 (Evan
Daniel (found_by); T-257, #845), with the classical L step; the issue asks that the
improvement be credited to Özden, the base packing to its holders as the record lists
them, and the local optimizer to Evan Daniel.
The issue says the search and its code were written and run by AI agents throughout and
that the checks were run by code that did not produce the packing; the issue and
repository were prepared and posted by his AI agent, and Özden directed the work.
The 172 part starts from this repository’s regularized atlas and its exact coordinates
were made with this repository’s promotion tool, so its lineage builds on this project.
The bibliography key is **[Özden s199 upper bound 2026-11-09]**.

The witness, the JSON, the decimal pose, the checker outputs, the README, the metadata and
the drawings are published under CC BY 4.0, and `verifier/sqcheck.py` under the MIT
licence, copyright (c) 2026 Doğa Özden, as [source/LICENSE.md](source/LICENSE.md) states;
it is byte-identical to the `LICENSE.md` of the lab’s other repositories, announced on
#890 ([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113)).
The drawings are pinned by digest only. The 172 part modifies Evan Daniel’s MIT-licensed
certificate, and the source carries his MIT notice as `LICENSE-evand-square-packing.txt`,
byte-identical to the `LICENSE` the
[evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains, and
pinned against it.

## Commands

From `packing/`, with the project interpreter. The identity measurement and the scans read
the house witness, its regularized view and the case records as they stand at main
`200f2ebc1`, before any adoption at 199 replaces them, so they reproduce there; the rest
read the packets and reproduce anywhere:

```bash
python -m devtools.acquire_source ozden-s199-upper-bound-2026-11-09 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s199-upper-bound-2026-11-09 --check
python -m devtools.upper_bound_reports ozden-s199-upper-bound-2026-11-09 check-claims --write
python -m devtools.upper_bound_reports ozden-s199-upper-bound-2026-11-09 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s199-upper-bound-2026-11-09 check --replay
python -m devtools.upper_bound_reports ozden-s199-upper-bound-2026-11-09 sharp-controls
python -m devtools.measure_identity --n 199 'OZDEN=packet:ozden-s199-upper-bound-2026-11-09' \
  'T-127=witness-center-basis:witnesses/known-best/n-199.yaml' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-199-regularized.yaml.gz' \
  --out resources/web/ozden-s199-upper-bound-2026-11-09/measure/identity.json
python -m devtools.contraction_margin --n 199 'T-127=witness-center-basis:witnesses/known-best/n-199.yaml' \
  --against 'T-284=packet:ozden-s199-upper-bound-2026-11-09' \
  --out resources/web/ozden-s199-upper-bound-2026-11-09/measure/contraction-n199.json
python -m devtools.contraction_margin --n 199 'T-284=packet:ozden-s199-upper-bound-2026-11-09' \
  --out resources/web/ozden-s199-upper-bound-2026-11-09/measure/contraction-n199-own.json
python -m devtools.l_step_scan --out resources/web/ozden-s199-upper-bound-2026-11-09/measure/l-step-scan.json
python -m devtools.l_step_scan --with "199=$(python -c 'import json; print(json.load(open("resources/web/ozden-s199-upper-bound-2026-11-09/acquisition/claims.json"))["results"][0]["exact_side"])')" \
  --out resources/web/ozden-s199-upper-bound-2026-11-09/measure/l-step-scan-adopted.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
