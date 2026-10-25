# Review: Couzo’s s(304) and Daniel’s Descents at 268 and 304

- **Date:** 24 October 2026
- **Reviewer:** Claude, strongest tier, maximum reasoning (the stage 4 mathematical
  review lane `c-review-t241-t242-math`, for the intake coordinator; bead `think-vm3m`)
- **Subject:** T-241, Francisco Couzo’s `certificates/best/n304.cert` at
  [franciscouzo/square-packing@fa6237e](https://github.com/franciscouzo/square-packing/tree/fa6237e288cf3fc53b53fc43438c91f3f59c40e9),
  retained in
  [couzo-issue763-2026-10-23](../../../packing/resources/web/couzo-issue763-2026-10-23/README.md)
  and pinned by
  [couzo-n304-2026-10-23](../../../packing/resources/web/couzo-n304-2026-10-23/README.md);
  and T-242, Evan Daniel’s `s268_lightning.cert` and `s304_pub.cert` at
  [evand/square-packing@8a8879a](https://github.com/evand/square-packing/tree/8a8879a2972c32cbd2d906049228cc9f0762b02a),
  retained in
  [evand-kaggle-descents-2026-10-24](../../../packing/resources/web/evand-kaggle-descents-2026-10-24/README.md)
- **Read at:** `main` `84d4a75af`
- **Verdict:** accepted, for finite feasibility.
  All three bounds hold at the exact sides stated, and no finding is blocking.
  One major finding is on the record’s credit at 304 (M-1); four are minor and four are
  notes.
- **Code:**
  [review/review-2026-10-24/](../../../packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/README.md)

## Summary for the Authors

Francisco Couzo’s certificate at 304 and Evan Daniel’s certificates at 268 and 304 are
valid.
This review decided each one again with a clean-room exact checker written for it.
That checker shares no code with either author’s checkers or with this repository’s two
exact routes. Every square lies in the box and no two overlap, decided in exact rational
arithmetic by two methods that agree on every certificate and every control.
Each side is the certificate’s own header side, and each 12-place print rounds it up
correctly.

| Certificate | Exact side | Print, rounded up | Least wall clearance | Least pair gap |
| --- | --- | --- | --- | --- |
| Couzo, 304, `fa6237e` (T-241) | 42654…087439 / 23793…000000 = 17.926898903392643… | 17.926898903393 | 1e-15 exactly | 8.18394241446e-11 |
| Daniel, 268, `8a8879a` (T-242) | 8437180857934672912242411148233 / (5 × 10^29) = 16.874361715869345824484822296466 | 16.874361715870 | 5e-21 exactly | 9.99999999999998886e-21 |
| Daniel, 304, `8a8879a` (T-242) | 1792689890035674158972360842897 / 10^29 = 17.92689890035674158972360842897 | 17.926898900357 | 5e-21 exactly | 9.99999999999999487e-21 |

The pose-by-pose measurements agree with the packets’.
At 268, Daniel’s certificate is Vladislav Lavrentev’s public Kaggle packing, descended:
no square moves more than 1.41e-4. It is one arrangement with Couzo’s #763 packing
(mirrored) and with Kirill Tymchishin’s notebook packing, with no square more than 0.1
from either.
At 304, Couzo’s certificate is a different arrangement from the case’s house
best packing (54 squares beyond 0.1), and Daniel’s 304 is Couzo’s packing descended (no
square beyond 4.60e-4).

One finding matters for credit.
The record reads Couzo’s manifest as saying that Tymchishin’s 304 notebook started from
Mykhailo Polkovskyi’s packing.
The manifest uses those fields for the packing its catalogue held before at the count,
not for the notebook’s seed.
So the chain after Tymchishin at 304 is not something the source states (M-1). Nothing
here blocks either bound.
The questions at the end ask each author what only they can answer.

## The Claims

- **T-241.** $s(304) \le
  42654421699169959072564987841514227093543746926117736119087439/2379353056489745832681562849107891444171481219500000000000000
  = 17.92689890339264\ldots$, by `certificates/best/n304.cert` of
  franciscouzo/square-packing, first committed at `fa6237e` (blob `953dc2e5`) and
  unchanged at `964ee2b` and the head `1c17153`. The source credits the packing to
  Kirill Tymchishin’s Kaggle notebook “CPU Alternating Reclosure” v3 and claims no
  refinement of it.
- **T-242.** $s(268) \le 16.874361715869345824484822296466$ and
  $s(304) \le 17.92689890035674158972360842897$, by `s268_lightning.cert` and
  `s304_pub.cert` of evand/square-packing at `8a8879a`. The source describes them as
  exact descents of Lavrentev’s public Kaggle packing at 268 and of “the public Kaggle
  packing at 17.9268989004 (finder unknown; earliest public copy: kozykappa’s notebook)”
  at 304.

Each is a finite packing, so each claim is an upper bound and nothing more.
The argument from certificate to claim has one step: $n$ closed unit squares with
pairwise disjoint interiors inside $[0, S]^2$ show $s(n) \le S$. The hypotheses a
checker must establish are that the parsed file is the pinned file, that each line is a
unit square, that the squares lie in the box, and that no two interiors meet.

## Exact Verification

**Custody.** Each file this review read from a packet has the Git blob the source’s tree
holds at the pinned commit
([custody](../../../packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/outputs/t241_t242_custody.txt)).
Couzo’s `n304.cert` is blob `953dc2e5` at `fa6237e`, `964ee2b` and `1c17153`, and the
only earlier version of that path, at `4e4c8ce`, holds other bytes.
Daniel’s two certificates, his inputs and `CREDITS.md` are the blobs at `8a8879a`.
GitHub’s activity log
([pushes](../../../packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/outputs/t241_t242_pushes.txt))
has `964ee2b`, carrying `fa6237e`, pushed at 2026-10-23T23:38:42Z, and `8a8879a` pushed
at 2026-10-24T04:53:53Z. That is the report order the ledger and both entries use.

**The checker.** `t241_t242_exact.py` reads `n S` and $n$ lines `x y t` of integers or
fractions, refusing anything else.
Each line becomes a square of half side 1/2 with edge directions $u = (c, s)$ and
$v = (-s, c)$, where $c = (1 - t^2)/(1 + t^2)$ and $s = 2t/(1 + t^2)$, so
$c^2 + s^2 = 1$ holds exactly, and the checker asserts it.
It decides each certificate twice:

- **Separating axes.** A square lies in the box exactly when its four corners do.
  Two convex polygons have disjoint interiors exactly when an edge normal of one of them
  weakly separates their projections, because their Minkowski difference has only those
  edge normals. So each pair is decided on $u_i, v_i, u_j, v_j$, and its gap is the
  largest projected gap.
- **Clipped areas.** Clipping a square to the box must leave area 1, and clipping one
  square to another must leave area 0 (Sutherland–Hodgman clipping and the shoelace
  formula, in `Fraction`).

A pair whose centres are at least 2 apart has disjoint interiors, since each unit square
lies in a disc of radius $\sqrt2/2$ about its centre.
Its separating-axis gap is then at least $|d|/\sqrt2 - 1/2 - \sqrt2/2 > 0.2$, since one
of square $i$’s axes carries at least $|d|/\sqrt2$ of the centre offset $d$. Every
nearer pair, chosen exactly by a grid of 2 × 2 cells and the exact squared distance, is
decided by both methods.
A third pass decided every one of the $n(n-1)/2$ pairs by separating axes alone.
Nine hand-decided packings test the checker first: edge contact, a duplicated square, a
square slid half along its neighbour’s edge, corner-to-corner contact, a turned square
touching all four walls, a turned square’s corner touching an edge, and a square outside
the box, with the two turned cases also moved 1e-30 too far.
All nine come out as decided by hand.

**Results**
([transcript](../../../packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/outputs/t241_t242_exact.txt),
[receipt](../../../packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/outputs/t241_t242_exact.json)):

|  | T-241, 304 | T-242, 268 | T-242, 304 |
| --- | --- | --- | --- |
| SHA-256 as pinned | `c8433dd7…`, yes | `c87da316…`, yes | `5dd7436a…`, yes |
| Valid, both methods | yes | yes | yes |
| Tilted squares | 135 | 110 | 120 |
| Least near-wall clearance | 1e-15 (2 squares) | 5e-21 (23 squares) | 5e-21 (11 squares) |
| Least far-wall clearance | 1e-15 (square 298) | 5.00000000046078e-21 | 5.00000000060942e-21 |
| Least pair gap, squares | 8.18394241446126e-11, 67–68 | 9.99999999999998886e-21, 239–241 | 9.99999999999999487e-21, 57–58 |
| Pairs with gap below 1e-9 | 783 | 612 | 678 |
| Pairs decided by both methods | 1,170 | 1,018 | 1,170 |
| All pairs, separating axes | 46,056, least gap as above | 35,778, as above | 46,056, as above |

Squares are numbered from 1 in file order.
The least gaps are separating-axis gaps, and for these pairs the Euclidean distance
agrees to the digits shown.
Daniel’s certificates are a contact packing dilated by $1 + 10^{-20}$: near-wall squares
sit at $0.5 + 5 \times 10^{-21}$, and 611 pairs at 268 and 676 at 304 have gaps below
1e-18. Couzo’s carries the manifest’s witness dilation of $1 + 10^{-10}$ and a wall pad
of exactly 1e-15, and none of its pairs is closer than 8.18e-11.

**Controls.** Each certificate went through twelve mutations, each decided in full by
both methods, with the expected outcome fixed before the run.
All 36 came out as expected and the two methods agreed on every one:

- The side lowered by the least far-wall clearance is accepted at contact with margin 0.
  Lowered by 1e-30 more, or by twice the clearance, it is refused.
- The least-gap pair, one square moved along the separating axis by the gap, is accepted
  with that pair at contact.
  Moved 1e-30 further, it is refused.
- A square moved 1e-3 toward its neighbour’s centre is refused.
- A square enlarged to side $1 + 2(\text{gap} + 10^{-30})$, past its least-gap pair, is
  refused, and so is a square enlarged past its far wall by its clearance and 1e-30.
- A duplicated square is refused, and so is a square moved past its near wall by its
  clearance and 1e-30.
- Every centre drawn toward the box centre by the factor $1 - 10^{-9}$ is refused.
- The least-gap pair’s square turned by about $2 \times 10^{-9}$ radians is refused by
  both methods.

**Against the packets’ sharp controls.** The packets’ `sharp-controls*.json` receipts
report each certificate’s least pair gap and least wall clearance as exact fractions.
[A comparison](../../../packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/outputs/t241_t242_receipts.txt)
finds both equal to this review’s, fraction for fraction: 1e-15 and 8.18394241446e-11
for T-241, and 5e-21 with gaps of 9.99999999999998886e-21 and 9.99999999999999487e-21
for T-242. The receipts lower the side to the least far-wall clearance, which this
review finds to be 1e-15 for T-241 and $5.00000000046078 \times 10^{-21}$ and
$5.00000000060942 \times 10^{-21}$ for T-242. The register’s “at least 9.99e-21” is that
gap cut at three places.
Daniel’s JSON reports state `cert_min_pair` 9.999999999999989e-21 and
9.999999999999995e-21, the binary64 values of the same gaps.

**Trust boundary.** The checker trusts Python’s `fractions` and integer arithmetic, the
parsing of the file’s decimal integers, and the two geometric facts above.
It shares nothing with Couzo’s `verify_bound_certificate.py` or `sqpack/verify.py`, with
Daniel’s `verify_cert.py`, or with this repository’s routes and `sharp_controls.py`,
none of which its author read.
It shares with every route the reading of `t` as $\tan(\theta/2)$, turning
counter-clockwise, which Daniel’s headers state and Couzo’s header leaves to the
`verify_cert.py` it names.
Read the other way, every certificate overlaps: 89 pairs in T-241’s, 99 and 92 in
T-242’s
([sense](../../../packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/outputs/t241_t242_sense.txt)).

## Sides and Prints

- **T-241.** The header side equals the fraction the claim states exactly.
  Its decimal cut at 14 places is the claim’s 17.92689890339264, and rounded up at 12
  places it is 17.926898903393, Couzo’s catalogue print.
- **T-242.** The header sides equal both the fractions the packet states and the
  decimals the claim states, which end exactly.
  Rounded up at 12 places they are 16.874361715870 and 17.926898900357, the ledger’s
  prints.
- **The margins** the register states are the exact differences, read from the
  comparison files’ own headers: 4.47965e-12 below #763’s entry at 268, 4.45311e-3 below
  T-174 (house print 16.878814821007), 2.52885e-3 and 2.52886e-3 below T-186
  (17.929427758076), and 3.03590e-9 between the two 304 certificates.
  #763’s side at 268 rounds up to 16.874361715874, so the two 268 prints differ, as the
  ledger says.
- **Daniel’s padding.** From his JSON, `S_cert` exceeds `S_exact` by 1.6874e-19 at 268
  and 1.7927e-19 at 304, a relative padding of $10^{-20}$, as the register says.

## Identity and Lineage

`t241_t242_identity.py` measures centres with each of the box’s eight symmetries applied
to the second packing.
It takes the optimal assignment minimising the summed centre distance, and checks it
against the assignment minimising summed squared distance and against nearest centres.
Orientations are compared modulo 90°, with a reflection reversing them.
Both packings are anchored at the origin
([transcript](../../../packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/outputs/t241_t242_identity.txt)).
The program was written and run before this review read the packet’s `identity.json` or
any identity code.

| First | Second | Best symmetry | Nearest centres one to one | Beyond 0.1 | Beyond 1e-3 | Largest move | Largest turn |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| T-242, 268 | #763’s entry at 268 (`964ee2b`) | mirror $x \mapsto S - x$ | yes | 0 | 135 | 7.08e-2 | 1.36° |
| T-242, 268 | T-174, the house | mirror $x \mapsto S - x$ | no | 119 (118 by squared distance) | 173 | 1.46 (1.07) | 44.2° |
| T-242, 268 | Tymchishin’s EDA+Seam LP v4 (`85dbd707`) | identity | yes | 0 | 147 | 2.49e-2 | 0.90° |
| T-242, 268 | Lavrentev’s packing, Daniel’s `.input.txt` | identity | yes | 0 | 0 | 1.41e-4 | 0.0057° |
| T-242, 268 | Daniel’s `.predescent.txt` | identity | yes | 0 | 147 | 2.49e-2 | 0.90° |
| T-242, 268 | Daniel’s regularized view | rotation 180° | no | 9 | 69 | 0.647 | 1.06° |
| #763’s entry at 268 | Tymchishin’s v4 | mirror $x \mapsto S - x$ | yes | 0 | 265 | 5.99e-2 | 0.81° |
| Tymchishin’s v4 | Lavrentev’s packing | identity | yes | 0 | 147 | 2.50e-2 | 0.91° |
| Tymchishin’s v4 | Daniel’s `.predescent.txt` | identity | yes | 0 | 0 | 2.47e-10 | 0° |
| Tymchishin’s v4 | T-174, the house | mirror $x \mapsto S - x$ | no | 122 | 173 | 1.45 | 44.0° |
| T-241, 304 | T-186, the house (Polkovskyi’s `70a033f`) | diagonal $(x, y) \mapsto (y, x)$ | no | 54 | 269 | 1.13 | 26.0° |
| T-241, 304 | T-175 (Ostashev’s #575) | diagonal | no | 54 | 269 | 1.13 | 26.0° |
| T-241, 304 | Daniel’s `s304_pub.input.txt` | identity | yes | 0 | 0 | 2.05e-9 | 4.7e-9° |
| T-242, 304 | T-241 | identity | yes | 0 | 0 (73 beyond 1e-6) | 4.60e-4 | 0.019° |
| T-242, 304 | T-186, the house | diagonal | no | 54 | 269 | 1.13 | 26.0° |
| T-186 | T-175 | identity | yes | 0 | 0 | 1.8e-15 | 0° |

The receipt also gives each comparison with the boxes centred.
That changes no count beyond 0.1, and changes counts beyond 1e-3 only where the two
sides differ by more than 1e-3. The two assignments differ only between different
arrangements, and the table then gives both.

**Against `measure/identity.json`.** Every figure the packet records agrees with this
review’s at the precision it prints: the pairing, the counts beyond each threshold, the
largest move and turn, and the best symmetry.
The packet numbers that symmetry 4 for the mirror $x \mapsto S - x$ and 7 for the
diagonal its README names, as `devtools.check_half_angle_area.symmetric`, which its
program uses, counts them.
There is one exception, Daniel’s 268 against T-174. There the packet’s 118 beyond 0.1
and largest move 1.07388 are this review’s squared-distance assignment exactly, the
objective its program’s docstring states (N-3). The register’s sentences built on the
measurement read correctly: T-242’s notes and regularization at 304, and the 250 within
and 54 beyond 0.1 for T-241.

**What the measurements say.** At 268 four placements are one arrangement: Lavrentev’s,
Tymchishin’s, #763’s and Daniel’s are pairwise one to one with no square beyond 0.1.
Daniel’s certificate is Lavrentev’s placement descended.
Tymchishin’s is close to Lavrentev’s under the identity, and #763’s is Tymchishin’s
mirrored and refined.
The house at 268 is a different arrangement from all four.
At 304, T-241 and T-242 are one packing, and that packing is a different arrangement
from T-186’s: 54 squares beyond 0.1, turns of 26°, and no symmetry pairing nearest
centres one to one. Within 0.1 of the house are 250 of 304 squares.
That overlap does not show descent: Daniel’s 268 shares 149 of 268 squares within 0.1
with the house at 268, a different arrangement.

## Credit Chains

**At 268.** Daniel’s commit message credits “Vladislav Lavrentev’s (Kaggle lightningv08)
public packing, exact descent (shrink-only)”. His JSON gives the descent’s input side as
16.87436171586941, which is `s268_lightning.input.txt`, and the certificate is that file
moved by at most 1.41e-4. His `TODO.md` at `659ee62` (line 11) adds that “the packing
first appears in lightningv08’s CUDA Packing Search output, kirilltym’s input”.
Couzo’s manifest at `fa6237e` agrees in its own terms.
Its lineage for Tymchishin’s 268 begins at a `cuda` step of the 22 October portfolio
before `kirilltym-seam-lp`, and at 303 the same manifest ties the `cuda` source to
Lavrentev’s “CUDA Packing Search” v11. So “Daniel after Lavrentev” is the chain both
sources support, and the adoption’s rule (the house credit follows the placement
adopted) gives it at 268. Daniel’s `CREDITS.md` at `8a8879a` is about his lower-bound
work and says nothing about these packings.
It states that the repository’s work was “Produced by Claude (Anthropic) in a single
session under human direction”, and the commit carries a Co-Authored-By trailer naming
Claude.

**At 304.** Couzo’s catalogue row, `certified_bounds.json` and manifest credit the
packing to “Kirill Tymchishin (kirilltym), Kaggle “CPU Alternating Reclosure” v3”. They
defer earlier credits to the notebook’s source notices and to “provenance”.
The notices (`submissions/kaggle-public-portfolio-20261022/SOURCE_NOTICES.md`) are in no
commit of the source’s history as cloned.
The manifest’s `witnesses/304` entry is identical at `fa6237e` and `964ee2b`, and its
own `lineage` lists a single step, `kaggle-public-portfolio-20261022 / alternating`.
Daniel calls the finder unknown and kozykappa’s notebook the earliest public copy.
His `TODO.md` (line 30) notes that his Kaggle imports keep no finder field.
So the sources support “Tymchishin”, certified by Couzo and descended by Daniel, and
neither supports a link past Tymchishin (M-1). Attribution’s chain rule (attribution.md,
Credit Text and Lineage) keeps every link a source supports and infers none from
resemblance. By that rule the 304 chain is *Couzo after Tymchishin* for T-241, with Levy
for the manifest’s first checker as #763’s key has it, and *Daniel after Tymchishin* for
T-242’s 304. Couzo’s commits `fa6237e`, `964ee2b` and `efef7d1` each carry a
Co-Authored-By trailer naming Claude (M-5).

## Significance

- **T-241, S3, confirmed.** The claim improves the best known side at 304 by 2.53e-3
  with a different arrangement from the house’s, as T-175 (1.38e-4 to 2.64e-3) and T-230
  (1.86e-4) are, far above T-226’s 1.88e-5 at the low end of S3. That the packing is
  Tymchishin’s and Couzo only certified it does not change a score of the claim.
  The rationale’s second and third sentences rest on M-1’s reading and should go.
- **T-242, S2, confirmed.** At 304 it is the solved side of T-241’s packing, as T-225’s
  and T-231’s are (S2). Of its 3.04e-9 margin, 1.45e-9 is the height of T-241’s side
  above the binary64 packing Daniel started from, which T-241 certifies to 2.05e-9, and
  1.58e-9 is Daniel’s descent.
  At 268 it is a descent of another placement of the arrangement #763’s entry holds,
  4.48e-12 below it, with no square beyond 0.1 of it.
  That is below T-239’s case (S2, 12 squares beyond 0.1) and above padding alone (S1,
  T-174, T-186). The rationale’s print sentence needs the correction in M-2.

## Findings

No finding is blocking: every certificate decides its bound.
Line numbers are at `main` `84d4a75af`.

### M-1 (major): The chain after Tymchishin at 304 reads a field of Couzo’s manifest as lineage

**Where.** `packing/frontier/results.yaml` lines 33732–33736 (T-241 claim), 33750–33757
(T-241 rationale), 33807–33809 (T-241 notes), 33860–33865 (T-242 claim);
`packing/resources/bibliography.yaml` lines 3864 and 3871–3876
(`[Couzo n304 2026-10-23]`) and 3885 and 3892–3896
(`[Daniel Kaggle descents 2026-10-24]`);
`packing/resources/web/couzo-n304-2026-10-23/README.md` lines 49–63, 109–112, 128–135,
140–144 and 150–156; `packing/resources/web/evand-kaggle-descents-2026-10-24/README.md`
lines 190–198 and 204–208.

**What.** The record states that the manifest’s `witnesses/304` entry “gives the
notebook’s previous source and seed as Mykhailo Polkovskyi’s #593 certificate”.
On that reading it credits the packing after Polkovskyi and then T-186’s recorded chain
(Ostashev, Couzo, PingYou Ltd, Levy).
In the manifest, `provenance.previous_source` and
`provenance.previous_reference.seed_credit` name the packing the catalogue held at the
count before this one:

- At 303 at `fa6237e`, one entry names Lavrentev in `source_provenance.seed_credit`, the
  packing Couzo refined.
  The same entry names Evan Daniel, the record it replaced, in both `previous_source`
  and `previous_reference.seed_credit`.
- Across the `fa6237e` manifest, 182 entries carry both fields, and in all 182
  `previous_reference.seed_credit` names someone other than the packing’s own
  `source_provenance.seed_credit`
  ([credits](../../../packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/outputs/t241_t242_credits.txt)).
- At 268 at `fa6237e`, the same fields of Tymchishin’s entry name PingYou Ltd’s
  certificate, T-174’s packing.
  Tymchishin’s packing is a different arrangement from it (122 squares beyond 0.1,
  nearest centres not one to one).
- #763’s entry at 268 reads the same field as “the source’s previous record, not
  lineage” (results.yaml lines 33677–33678).

The 304 entry is a public submission with no `seed_credit` of its own, and its `lineage`
names only the notebook’s output.
The 250 squares within 0.1 of T-186 are a resemblance, and attribution.md (Credit Text
and Lineage) and epistemics.md (Parallel Projects and Their Credit) bar inferring
lineage from one.

**Fix.** Credit T-241 *Couzo after Tymchishin*, keeping Levy for the manifest’s first
checker as #763’s key does.
Credit T-242’s 304 *after Tymchishin* through T-241, and drop Polkovskyi, Ostashev,
Couzo and PingYou Ltd from both keys and from the claims.
Keep the measurement against T-186 in the notes as a measurement: “another arrangement”,
not “found from the house’s”. Reword the packet’s question 1 to Couzo as question C1
below, and make the change before the adoption at 304 sets the house credit.

### M-2 (minor): T-242’s rationale names the wrong print as the case’s

**Where.** `packing/frontier/results.yaml` lines 33877–33878.

**What.** It says the 268 side “moves the case’s 12-place print (16.874361715874 to
16.874361715870)”. On `main` the case’s print is T-174’s, 16.878814821007. The figure
16.874361715874 is #763’s entry’s, pending adoption.

**Fix.** “moves the 12-place print of #763’s entry, which the case takes when that entry
is adopted”, or name the print against T-174.

### M-3 (minor): The declined construction credit cites only this record’s measurement

**Where.** `packing/frontier/results.yaml` lines 33738–33741;
`packing/resources/web/couzo-n304-2026-10-23/README.md` lines 62–63 and 132–133;
`packing/resources/bibliography.yaml` lines 3875–3876.

**What.** The record declines the manifest’s construction credit to Nate Chaoweeraprasit
for Polkovskyi’s 304 because “the record’s measurement does not support it”.
The source contradicts it as well.
Its `RECORD_PROVENANCE.md` line 53, the same blob at `fa6237e`, `964ee2b` and `1c17153`,
says the `70a033f` update “preserves Ostashev’s packing credit at
129/175/176/204/232/264/303/304”. Under M-1’s reading the construction credit describes
the replaced record, not T-241’s packing, so once M-1 is fixed it no longer bears on
T-241 at all.

**Fix.** Cite the source’s own statement beside the measurement, and keep the question
to Couzo (C2) about the inconsistency.

### M-4 (minor): Daniel’s key takes its lineage and its Levy link from T-241’s chain

**Where.** `packing/resources/bibliography.yaml` lines 3884–3885 and 3895–3896.

**What.** The key is `builds-on-project` and credits Levy “through 304, T-241’s chain
(the manifest’s first checker is this project’s sqpack/verify.py)”. That checker
certified Couzo’s file, which Daniel did not use: his input is the public binary64
packing. For these descents his source names nothing of this project’s beyond the
comparison its `_prior.json` files draw from the register.
`CREDITS.md` lists the Squares Project as parallel work.

**Fix.** With M-1, derive the lineage and any Levy link from Daniel’s source alone.

### M-5 (minor): T-241’s record states no AI assistance

**Where.** `packing/resources/web/couzo-n304-2026-10-23/README.md` lines 126–144;
`packing/frontier/results.yaml` lines 33715–33743; `packing/resources/bibliography.yaml`
lines 3866–3878.

**What.** The commit that first holds the certificate, `fa6237e`, ends “Co-Authored-By:
Claude Opus 5.5”, as do `964ee2b` and `efef7d1`. The packet README, the claim and the
key say nothing of it.
The runbook asks the README for what the source says about AI assistance, and
attribution.md asks the record to preserve it.
It also bears on this review’s independence, which shares the system family.
This finding was written after reading the #763 review’s RF-1. The trailers themselves
were in this review’s credit reading before that.

**Fix.** State the trailers in the packet README and in T-241’s notes, as the evand
packet does for Daniel’s.

### N-1 (note): Daniel’s descent at 268 started from Lavrentev’s placement

`s268_lightning.json` gives `S_input` 16.87436171586941, the side of `.input.txt`, and
the certificate is that file moved by at most 1.41e-4. This answers half of the packet’s
third question to Daniel (its README, lines 222–225). What `.predescent.txt` is remains
his to say: it is Tymchishin’s v4 packing to 2.47e-10, at side 16.875467950172816, and
the certificate is 2.49e-2 from it.

### N-2 (note): At 268 both sources put Lavrentev before Tymchishin

The `cuda` step in Couzo’s `fa6237e` lineage and Daniel’s `TODO.md` line 11 both place
Lavrentev’s packing ahead of Tymchishin’s. #763’s own credit at 268 names Tymchishin
only. That is for #763’s entry.
For the adoption it is consistent with “Daniel after Lavrentev”.

### N-3 (note): `identity.json` names neither its objective nor its symmetry numbering

Its figures for Daniel’s 268 against T-174 are the squared-distance assignment exactly:
118 beyond 0.1 and largest move 1.07388, against 119 and 1.46 for summed distance.
The program it names (`evand-regularized-2026-10-20/measure/identity.py`) states that
objective in its docstring, and takes its numbering from
`devtools.check_half_angle_area.symmetric`. No identity the record states depends on
either, since every one-to-one pairing above is the same under both objectives.
Writing both into the receipt would let the figures be read from the receipt alone.

### N-4 (note): Every certificate overlaps under the other rotation sense

Read clockwise, T-241’s certificate has 89 overlapping pairs and T-242’s 99 and 92, so
the sense is load-bearing.
Daniel’s headers state $(c, s)$. Couzo’s says only “rotation t = tan(theta/2); check
with verify_cert.py”, and the named checker fixes the sense.
Written after reading the #763 review’s RF-11.

## Questions for the Authors

For Francisco Couzo:

1. **C1.** In your manifest, do `previous_source` and `previous_reference.seed_credit`
   name the packing your catalogue held before at that count, or the packing a search
   started from? At 303 they name Evan Daniel’s certificate while `seed_credit` names
   Lavrentev. Did Tymchishin’s “CPU Alternating Reclosure” v3 start from Polkovskyi’s
   `70a033f` packing at 304?
2. **C2.** Your manifest credits the construction of Polkovskyi’s `70a033f` 304 to Nate
   Chaoweeraprasit, and your `RECORD_PROVENANCE.md` keeps Daniil Ostashev’s packing
   credit there. Which do you intend?
3. **C3.** At 268, is the `cuda` step before `kirilltym-seam-lp` in your lineage
   Lavrentev’s “CUDA Packing Search”, as at 303?
4. **C4.** Could you publish the notebooks’ `SOURCE_NOTICES.md` files your manifest
   names at 268 and 304? No commit of the repository holds them.

For Evan Daniel:

1. **D1.** What is `s268_lightning.predescent.txt`, Tymchishin’s v4 packing to 2.47e-10,
   and did any step of the descent use it?
   Your JSON’s input side is `.input.txt`’s.
2. **D2.** Is “finder unknown” at 304 the missing finder field your `TODO.md` notes for
   Kaggle imports? Do you know who first published that packing, and which notebook
   versions and dates hold Lavrentev’s 268 and kozykappa’s 304?

C1, C3 and C4 overlap the #763 review’s questions 1 and 6 and the packets’ drafted
questions; the replies can merge them.

## Rungs

**`V3`/`C3`, confirmed, independently re-implemented**, for both entries once the
records lane’s replay evidence and this review’s are entered and this review is mapped
as accepted. The maintained replay is the records lane’s. This review’s checker is a
clean-room re-implementation by a Claude agent, and the producers’ commits name Claude
as co-author: *independently re-implemented, clean-room, by a Claude agent, a system
family the producers also used*.

By the house rule both entries then hold the smallest validated sides: T-242 at 268,
once #763’s entry is adopted there, and T-242 at 304 with T-241 as the packing it
regularizes. The adoption change (`think-hx0e`) regularizes each new house with both
strong generators. At 268 the house credit follows the placement adopted, *Daniel after
Lavrentev*. At 304 it follows T-241’s packing, credited as M-1 proposes.
Neither entry reaches `V4`/`C4`, which need a second accepted adversarial review by a
distinct reviewer and a human oversight record.
No lower bound, optimum, local minimum, rigidity or priority follows.

## Proposed Record Changes

For the records lane; this review writes none of them, and
[record-changes.md](../../../packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/record-changes.md)
gives each in full.

- **`verifiers.yaml`:** register `t241_t242_exact.py` (decides) with its independence
  record. The other programs decide nothing and are kept unregistered.
- **`evidence.yaml`:** an entry for this review’s checker for each of T-241 and T-242,
  `independent-implementation`, `coverage: full`; this document as `external_review` on
  each reported entry and on the records lane’s replay entries.
- **`results.yaml`:** each entry’s `reviews` gains this document (`kind: adversarial`,
  `reviewer_kind: ai`, `relation: project`, `verdict: accepted`). The significance stays
  S3 and S2 with the rationales in the drafts, `by` naming this review.
  The claims, notes and keys change as M-1 to M-5 say.
- **The packets’ READMEs:** M-1, M-3 and M-5 for `couzo-n304-2026-10-23`; M-1 and N-1
  for `evand-kaggle-descents-2026-10-24`.

## Independence and Disclosure

- **Programs:** written for this review, clean-room for what they decide.
  Their author read the mathematics, the certificates’ header lines and the record’s
  summaries listed below.
  It read none of Couzo’s `verify_bound_certificate.py`, `sqpack/verify.py`, Daniel’s
  `verify_cert.py` or `verify_cert2.py`, the maintained routes, `sharp_controls.py`,
  `devtools.measure_identity` or the packet’s `identity.py`. After the identity run it
  read that program’s docstring and the `symmetric` function it uses, to reconcile N-3.
- **Read before these findings:** the brief; the runbook’s stages 1 to 5 and
  epistemics.md’s Confirmation, Significance and Results by Others; attribution.md; the
  register entries of #763’s 268, T-241 and T-242, and the significance of T-146, T-162,
  T-174, T-175, T-186, T-195, T-225, T-226 and T-230 to T-239; both packet READMEs; the
  evand ledger README; the two bibliography keys; the house witnesses’ metadata at 268
  and 304; and the sources as data, through their commits to `1c17153` and `659ee62`.
  The packets’ sharp-control receipts and `identity.json` were read after this review’s
  own programs had run.
- **Seen first:** the brief named the #763 review and placed its RF-6 at 268. The evand
  packet README (lines 124–126 and 172) and T-242’s notes (results.yaml lines
  33933–33939) summarize its 268 and 303 measurements, and the packets and the ledger
  state the identity figures.
  So the measurement at 268 was not blind to that conclusion or those figures.
  The register’s summaries of the producers’ reported clearances were read before the
  checker decided.
- **Not read before these findings,** which were written by 20:55Z on 24 October: the
  #763 review, read at about 21:00Z, and the 23 October review of T-239 and its
  programs, read for layout at about 20:57Z.
- **Shared system family:** the reviewer is a Claude agent, and both producers’ commits
  name Claude as co-author.

## Comparison with the Stage 4 Review of #763’s Entries

The [#763 review of 24 October](https://github.com/jlevy/squares/pull/794)
(`docs/project/reviews/review-2026-10-24-couzo-n268-n303.md` on PR #794, not on `main`)
reviewed Couzo’s 268 and 303. It was read only after the findings above, M-5 and N-4
excepted, were written.

**Agreements.**

- **The method.** Both decide finite feasibility with a clean-room checker of two exact
  methods, separating axes and clipped area, with sharp controls 1e-30 past contact.
- **Identity at 268.** Its figures are this review’s within the anchoring.
  Daniel’s certificate is Lavrentev’s placement descended (1.41e-4), and #763’s packing
  is its mirror image with 135 squares beyond 1e-3 and the largest move 7.08e-2. #763
  against Tymchishin’s v4 gives 5.91e-2 and 176 beyond 1e-3 with the boxes centred, as
  this review’s centred variant does.
  The `.predescent.txt` is the v4 parent to 1.2e-10 centred and 2.47e-10 anchored.
  Its RF-6, that Daniel’s 268 is a sibling placement, so that the house credit follows
  the placement adopted, is this review’s conclusion at 268.
- **Notices and lineage.** Its RF-7, that the notebook notices are unpublished, holds at
  304 as at 268. Its question 1 asks whether the 268 credit should name Lavrentev, from
  the same `cuda` step that N-2 ties to Lavrentev through the 303 entry.
- **The significance line.** S2 for further arrangements and refinements, S3 for new
  arrangements from about 2e-5, as applied here.

**Disagreement.** Its RF-2 says the manifest’s top-level `previous_source` is “the
lineage one level up”, the parent each search refined, and proposes saying so in #763’s
packet README and entry.
That holds at 964ee2b’s 268 and 303, which it measured, because there the catalogue’s
previous record is the packing Couzo refined.
The field itself names the previous record:

- `fa6237e`’s 303 names Daniel there and Lavrentev as the seed.
- `fa6237e`’s 268 names PingYou Ltd’s packing, which Tymchishin’s is not a refinement
  of.
- 182 of 182 `fa6237e` entries with a seed of their own name a different previous
  reference (M-1).

Read as a general rule, RF-2 would make T-241’s misreading look right.
If PR #794 applies RF-2, its wording should say that at 268 and 303 the previous record
is also the parent each search refined, as measured, and not that the field records
lineage.

**Carried over, not checked here.** Its RF-4 finds that the maintained replay shares the
producer’s first checker, `sqpack/verify.py`, and the `evand-cert` reader with Daniel’s
checkers. If so, the records lane’s replay entries for T-241 and T-242 are
`shared-components` too, and “independently re-implemented” rests on this review’s
entries. This review did not read the maintained routes.

**Changed after reading.** M-5 (from its RF-1) and N-4 with `t241_t242_sense.py` (from
its RF-11) were added.
No other finding and no figure changed.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty or priority, and no human
oversight. No run or reading of the sources’ checkers, this repository’s maintained
routes or `sharp_controls.py`, and no check of the KKT, flat-motion or second-order
statements in Daniel’s JSON. The Kaggle notebooks and their notices are not retained and
were not fetched. Whether Tymchishin’s notebook started from any recorded packing is
stated by no source.
No identity is decided: identity is measured.
The 303 certificate of `8a8879a`, which no entry registers, was not checked.
No house adoption, case-record change or regularization was made.

## Files

- [README.md](../../../packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/README.md):
  the programs, what each read, how to run them and what they printed.
- `programs/`: `t241_t242_exact.py` (decides), `t241_t242_identity.py`,
  `t241_t242_credits.py`, `t241_t242_receipts.py`, `t241_t242_sense.py`,
  `t241_t242_custody.sh` and `t241_t242_pushes.sh`, with their outputs in `outputs/`.
- [record-changes.md](../../../packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/record-changes.md):
  the drafted `verifiers.yaml` record, evidence entries and register changes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
