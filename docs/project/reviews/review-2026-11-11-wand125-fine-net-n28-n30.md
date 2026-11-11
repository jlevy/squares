# wand125’s Fine-Net Certificates for $s(28) \ge 2297/400$ and $s(30) \ge 2357/400$: Mathematical Review

2026-11-11. Reviewer: Claude (Anthropic), `tbd-strong-max` tier at maximum reasoning,
lane L93 (bead `think-4ul6`, under the import `think-i85v`), prompted separately from
the replay lane and sharing none of its context beyond the brief and the committed
record. Workflow:
[result-import.md, stage 4](../../../packing/campaign/result-import.md#stage-4-validate),
“The review”, by the checklist of the
[declared-net soundness review](review-2026-10-06-sqverify-fast-declared-net-soundness.md#for-the-records-lane)
of 6 October. Scope: `mixed_n28_L57425` (wand125/square-packing at `36b85b9`) and
`mixed_n30_L58925` (at `ff9f269`), as retained in the packet
[`wand125-fine-net-n28-n30-2026-10-10`](../../../packing/resources/web/wand125-fine-net-n28-n30-2026-10-10/README.md),
and the register entries T-142 and T-143 on `main` at `8afdabe8f`. A first launch of
this review on 4 November was lost and left nothing; this one started fresh.
This review moves no bound and adopts nothing.

## Summary for the Author

**Decision: accept both certificates.** For each, the argument from the certificate to
the claim is correct and complete, and every hypothesis it needs holds in exact
arithmetic. If 28 unit squares fitted in the closed square of side $2297/400$, or 30 in
the square of side $2357/400$, their cores at the declared net’s angles would be
disjoint sets of measure at least one each, against total masses of $28 - 1/100000$ and
$30 - 1/100000$. Each certificate in fact proves the strict bound $s(n) > L$.

The one condition that needs a large computation is the capture: at each of the 2,073
net directions, every core centred in its per-bin domain must hold mass at least one.
That rests on your complete runs of `sqverify-proof-net`, which this review read as data
and did not repeat. What it could decide cheaply, it decided with programs of its own
that share no code with yours or with this repository’s verifier:

- every exact premise of both files, and the net’s reach over every orientation;
- direction 0 of each net, completely, by a vertex argument: least captures
  $1.00141414993662$ and $1.00175288352551$, each equal to the exact capture at your
  sweep’s logged argmin;
- the exact capture at the centre of your least-bound box at all 2,072 rotated
  directions of each net, each at least your certified bound;
- the exact capture at all 62 oblique witnesses of your 197/200 controls, equal to your
  logged fractions digit for digit, and at both axis argmins;
- a seeded search at 33 rotated directions of each net, every end point evaluated
  exactly: least captures found $1.00079$ (n = 28) and $1.00071$ (n = 30).

So the certificates keep a few ten-thousandths of slack where your certified bounds stop
within $10^{-10}$ of one.
There is no blocking or major finding.
Four minor findings concern the bundles’ prose, manifest and pre-publication receipt,
not the mathematics: the README names a control log that does not exist (M-1),
`files-sha256.json` gives the sealed README’s digest (M-2), the receipt and README call
the check independent where it is this repository’s verifier with one change (M-3), and
the README describes a pre-publication run that its receipt does not separate from the
check2 run (M-4). The notes and questions concern margins, threads, the verifier’s
public copy and the axis gap at n = 28.

## The Claims

|  | n = 28 | n = 30 |
| --- | --- | --- |
| Certificate | `mixed_n28_L57425` at `36b85b9` | `mixed_n30_L58925` at `ff9f269` |
| Claim | $s(28) \ge 2297/400 = 5.7425$ | $s(30) \ge 2357/400 = 5.8925$ |
| Rows; images; distinct after merging | 631; 5,048; 5,036 | 463; 3,704; 3,672 |
| Total mass | $2799999/100000 = 28 - 1/100000$ | $2999999/100000 = 30 - 1/100000$ |
| Candidate SHA-256 (decompressed) | `5ef20511…0107` | `981a17db…677e` |
| Lower lanes on `main` | T-107’s $1147/200$; gain $3/400$ | T-109’s $11767/2000$; gain $9/1000$ |
| Upper bound on `main` | $5.82444461667405$ | $6$ |

Each is a format M rectangle measure in $D_4$ orbits, with no point or segment, on the
net its file declares, `proof_net {"step": "1/5002", "last": 2072}`, at core side
$B = 4999/5000$. At n = 28 the claim is also $1/400$ above the $287/50$ of
jlevy/squares#446, which was never adopted.

## What Was Read

**As data.** The packet’s README, acquisition record, source manifest and follow-up
facts; the two retained candidates; each certificate’s `check2/receipt.json`,
`check2/control.json`, run log, control log and pre-publication receipt; each
certificate’s published `README.md` and `files-sha256.json`, fetched at the pins and
held to the manifest’s SHA-256 (`f0e782cf…`, `42ba3e43…`, `b6929e9c…`, `566e5a42…`); the
source’s `SPEC.md` (`2ba83bc0…`) and `UPSTREAM_COMMIT` (`b6fb3b20…`) as the 6 October
check2 packet retains them, byte for byte the bundles’ copies by the manifest’s digests;
T-142, T-143, their two evidence entries, and `n-028.md` and `n-030.md`.

**As method.** `result-import.md` stage 4; the 6 October declared-net soundness review
in full; the n = 31 and #446 fine-net reviews of 23 October in full, as format models
(they are of other certificates on the same net); and, for the axis question only, the
description of #892’s rule: the module docstring of `devtools/sqverify_fast_axis.py` and
its `VERIFIERS.md` summary.

**Not read.** The source’s adapted crate (pinned by digest, unopened), its check script,
the sealed inner bundle, this repository’s `packing/sqverify_fast/` source, the census
driver and every program of `packing/devtools/` and `sqpack`, and any receipt of the
replay lane. The parent bead `think-i85v`, which the brief named, carries a note of the
replay lane (4 November) giving census figures; this review saw them there, says so
here, and decided nothing from them.
Earlier reviews that name these entries were read only after the findings below were
written ([Comparison With Earlier Reviews](#comparison-with-earlier-reviews)).

## The Argument, Re-Derived

Write $D = 1/5002$, $t_j = jD$ for $j = 0, \ldots, 2072$, $\theta_j = 2\arctan t_j$,
$b = B/2$, and $r(t) = (1 + 2t - t^2)/(2(1 + t^2))$, which is
$(\cos\varphi + \sin\varphi)/2$ at $\varphi = 2\arctan t$. Let $\mu$ be the
certificate’s measure and $Q_j(c)$ the closed square of side $B$, centre $c$ and angle
$\theta_j$.

1. **The measure.** Each row $[x_0, x_1] \times [y_0, y_1]$ of mass $m$ puts $m/8$
   uniformly on each of its eight images under the symmetry group $D_4$ of
   $K = [0, L]^2$, the field order being `[x0, y0, x1, y1]` (`SPEC.md` §2). So
   $\mu \ge 0$ is $D_4$-invariant, absolutely continuous, supported in $K$, and
   $\mu(K) = M$. The order was checked, not assumed: the other order gives rows of no
   positive area (3 at n = 28, 12 at n = 30), and only this reading reproduces the
   source’s exact control captures.
2. **Fold.** A unit square’s orientation is defined modulo $\pi/2$, and a reflection of
   $K$ maps $\varphi$ to $-\varphi$. So each square $S$ of a packing has an image $gS$,
   $g \in D_4$, with orientation in $[0, \pi/4]$, half-angle tangent
   $t \in [0, \tan(\pi/8)]$. The fold is square by square; no single symmetry needs to
   fold the whole packing.
3. **Bins.** The bins $[t_j - D/2, t_j + D/2]$ abut and cover $[0, (2072 + 1/2)D]$,
   which contains $[0, \tan(\pi/8)]$ because $t_{2072} = 1036/2501$ gives
   $t^2 + 2t - 1 = 367/6255001 > 0$. The last bin is needed: its lower end $4143/10004$
   gives $-22423/100080016 < 0$.
4. **Containment.** The turn $\delta$ between $gS$ and $\theta_j$ has
   $z = \tan(|\delta|/2) = |t - t_j|/(1 + t t_j) \le D/2$, since $t, t_j \ge 0$. The
   concentric square of side $B$ turned by $\delta$ lies in the open unit square if
   $B(\cos\delta + \sin|\delta|) < 1$, and
   $\cos\delta + \sin|\delta| = (1 + 2z - z^2)/(1 + z^2) \le 1 + 2z \le 1 + D$, with
   $B(1 + D) = 25009997/25010000 < 1$. The sharp value, at the upper end of bin 0, is
   $500400014977/500400085000$, a clearance of $70023/500400085000$, about
   $1.4 \times 10^{-7}$.
5. **Centre domain.** $gS \subset K$ puts its centre in $[r(t), L - r(t)]^2$, and
   $r'(t)$ has the sign of $1 - 2t - t^2$, positive below $\tan(\pi/8)$. Every
   $a_j = \max(0, t_j - D/2)$ lies there, so every square of bin $j$ has its centre in
   $C_j = [r(a_j), L - r(a_j)]^2$.
6. **Capture.** The certificate asserts $\mu(Q_j(c)) \ge 1$ for every $j$ and every
   $c \in C_j$. Then $g^{-1}Q_j(c)$, with $c$ the centre of $gS$, is a closed square in
   the open interior of $S$ with $\mu(g^{-1}Q_j(c)) = \mu(Q_j(c)) \ge 1$, by invariance.
7. **Count.** The cores of distinct squares lie in their disjoint interiors, so
   $n \le \sum_S \mu(\mathrm{core}(S)) \le \mu(K) = n - 1/100000$, a contradiction.
   No packing fits at side $L$, nor at any smaller side, so $s(n) > L$.

**The quarter turn.** At a fixed angle the rotation by $\pi/2$ about $(L/2, L/2)$ maps
$Q_j(c)$ to $Q_j$ at the rotated centre and preserves $\mu$, and the four images of the
quadrant $[L/2, U_j]^2$, $U_j = L - r(a_j)$, tile $C_j$. So step 6 needs the quadrant
only.
The source’s checker decides the quadrant (`SPEC.md` §5), and so does this review’s
axis decision.

**What is computed.** Steps 1 to 5 and 7 are exact arithmetic on the file, recomputed
here. Step 6 at 2,073 directions is the whole computational content, and only a complete
run of an interval checker decides it.
The measure is far from smooth: 339 of the 631 rows at n = 28 and 243 of the 463 at n =
30 are strips thinner than $1/500$, carrying $19.2$ of 28 and $23.2$ of 30 units of
mass, with row densities (mass over area) up to $616{,}441$ and $425{,}644$. A core
moved by a thousandth can gain or lose much of a unit, which is why the capture needs
fine boxes near the strips.

## Hypotheses Each Checker Assumes

| Hypothesis | Where it enters | Status here |
| --- | --- | --- |
| H1. The format’s meaning: `[x0, y0, x1, y1]`, mass $m/8$ per $D_4$ image, densities adding | every checker | read from `SPEC.md` §2; checked against the source’s 62 exact fractions |
| H2. Every mass positive, every row inside $K$ | steps 1, 7 | holds: all 631 and 463 |
| H3. $M < n$, threshold one | step 7 | holds: $n - M = 1/100000$ exactly |
| H4. $B(1 + D) < 1$, and $t_{2072}$ past $\tan(\pi/8)$ | steps 3, 4 | hold, values above |
| H5. Every $a_j$ below $\tan(\pi/8)$, every domain nonempty | step 5 | holds: narrowest widths $4.3283$ and $4.4783$ |
| H6. $D_4$-invariance of $\mu$ | steps 2, 6, quarter turn | holds exactly on the merged expansion, all eight symmetries |
| H7. The capture at every centre of every quadrant | step 6 | the computation: decided at direction 0 here, at all 2,073 by the source’s runs, by the census once it is recorded |
| H8. The crate’s implementation conditions: $t_{\max} \le 1/2$, the tangent form $B(1 + D/(1 - D^2/4)) < 1$, eight times the densest image density at most $2^{32}$ | the crate’s frame bounds | hold: $1036/2501$; $500400014977/500400075000$; $616{,}441$ and $425{,}644$ |

## What This Review Ran

Every program is this lane’s own, kept in the packet’s
[`review/review-2026-11-11/`](../../../packing/resources/web/wand125-fine-net-n28-n30-2026-10-10/review/review-2026-11-11/README.md)
with its outputs and the SHA-256 of each program as it ran.
They use CPython 3.14.7 (`fractions`, `hashlib`, `json`, `zlib`) and numpy 2.5.2 on
OpenBLAS at one thread, and import nothing from this repository, the source or the
maintained route.

| Program | Decides | Result | CPU (s) |
| --- | --- | --- | ---: |
| `premises.py` | premises | `PREMISES_HOLD` at both | 0.6 |
| `receipts_check.py` | poses | `ALL_CONSISTENT` | 115.8 |
| `axis_decide.py` | direction 0, completely | `AXIS_DIRECTION_DECIDED` at both | 3.7 |
| `axis_decide.py --factor 99/100` | the mutant’s direction 0 | refused at both, exact witnesses | 3.9 |
| `direction_sample.py` | poses | `NO_COUNTEREXAMPLE_IN_SAMPLE`, 66 directions | 112.8 |
| `selftest.py` | nothing (a test) | `PASS` | 18.5 |

**Premises.** The reader is strict: one gzip member, no float token, no duplicate key,
every number a decimal or `p/q`, exactly the keys `n`, `L`, `B`, `proof_net`,
`total_mass`, `points` and `rectangles`, so no top-level `net`, no `certificate`
metadata and no `scaling_factor`. Each decompressed candidate has the pinned SHA-256,
and the source’s `candidate_digest` (the SHA-256 of the JSON with sorted keys and
compact separators) was reproduced at both.
The claim’s $n$, $L$, $B$, net and mass are the file’s; `proof_net` has exactly `step`
and `last`. Every row lies in $K$ with positive extents and positive mass, every
coordinate is a multiple of $10^{-17}$, the masses sum exactly to $n - 1/100000$, and
the merged expansion (5,036 and 3,672 distinct images, the counts the source’s summaries
print) integrates exactly to the same mass and is invariant under all eight symmetries.
Lemma N0’s (a) to (e) hold with the values of step 3 and 4 above and
$t_{\max} = 1036/2501 \le 1/2$. At both ends of all 2,073 bins (4,146 tangents), the
core turned by the exact $z$ lies strictly inside the unit square, every $a_j$ lies
below $\tan(\pi/8)$ and every quadrant is nonempty.
Informational: at the far corner of every quadrant the core at the node’s angle still
lies in $K$, by at least $1.0994 \times 10^{-7}$ (node 1).

**The source’s receipts and logs.** Each run log has 2,073 rows, indices 0 to 2072 once
each, every one `verified` at threshold `1` with a bound of at least one; the axis row’s
vertices are the product of its event counts; every rotated search tree is complete
(nodes $= 2 \times$ leaves $- 1$); nodes and CPU sum to the summary’s 594,284,796 and
9,204.0 s (n = 28) and 702,952,674 and 14,334.5 s (n = 30); the summary is `VERIFIED`
with no refused direction and no injected fault, and its premises equal this review’s
(format M, per-bin domain, $D = 1/5002$, 2,073 angles, 631 and 463 rows, 5,036 and 3,672
images, the mass, the input digest).
Each `check2/receipt.json` embeds that summary unchanged and states the same digests.
Each 197/200 control ran at the 32 directions $\mathrm{round}(k \cdot 2072/31)$ with
mass $197/200 \cdot M$ and refused all 32.

**Direction 0, decided.** `axis_decide.py` decides the axis direction of each
certificate completely.
At angle 0 the capture is $F(x, y) = \sum_k d_k\,o^x_k(x)\,o^y_k(y)$ with overlap
lengths $o_k$ piecewise linear in their argument, so on every cell of the grid of all
breakpoints in $[L/2, L - 1/2]$ the capture is bilinear and its least value is at a
vertex. Every coordinate, $B/2$ and the quadrant’s ends are multiples of $10^{-17}$, so
the events and overlaps are exact int64 integers.
The vertex values are one binary64 matrix product of nonnegative terms, the overlaps
rounded to nearest and the densities rounded down, so the true value is at least the
computed one divided by $(1 + \gamma_K)(1 + 2^{-53})^3$ in any summation order, with or
without fused multiply-add.
The comparison with one is made in fractions, and the 64 smallest vertices are evaluated
again in fractions by two methods.

|  | n = 28 | n = 30 |
| --- | --- | --- |
| Events, vertices (the source’s counts) | 4,107; 16,867,449 | 3,017; 9,102,289 |
| Rigorous least capture | $1.0014141499363902$ | $1.0017528835253350$ |
| Exact at the least vertex found | $1.00141414993662\ldots$ | $1.00175288352551\ldots$ |
| Least vertex found | $(4.2428000208779879, 5.0809308983748918)$ | $(3.3927271495265631, 3.4992997713380972)$ |
| The source’s argmin and certified bound | $(4.2428000208779879, 2097/400)$; $1.0014141477613605$ | $(3.4992997713380972, 3.3927271495265631)$; $1.0017528833353533$ |
| Exact capture minus the source’s bound at its argmin | $2.1753 \times 10^{-9}$ | $1.9016 \times 10^{-10}$ |

At both counts the exact capture at the source’s argmin equals the least vertex value
found here, as fractions: a tie in the same column at n = 28, and the transpose under
the swap symmetry at n = 30. So index 0 of each net is decided by an implementation that
shares nothing with the source, 1 of 2,073 directions per certificate.

**Poses at every rotated direction.** At each of the 2,072 rotated directions of each
net, the exact capture at the centre of the source’s least-bound box is at least one and
at least that box’s certified bound: 4,144 poses, none below, every centre inside its
quadrant.
These are where the source’s branch and bound stopped, not where the capture is
least.

|  | n = 28 | n = 30 |
| --- | --- | --- |
| Least certified margin (direction) | $1.07 \times 10^{-11}$ (1088) | $2.93 \times 10^{-11}$ (1585) |
| Exact capture at that box’s centre | $1.114$ | $1.0171$ |
| Least exact capture at a least-bound centre (direction) | $1.0009048$ (1357) | $1.0008386$ (1945) |
| Median exact capture at the least-bound centres | $1.00758$ | $1.01118$ |

**The controls, exactly.** At each of the 31 oblique control directions the source’s
`exact_coverage`, a rational of hundreds of digits at n = 30, equals this review’s exact
capture at the witness pose times $197/200$ as fractions: 62 of 62 across the two
certificates. Every witness lies in its quadrant, and the unscaled captures there run
from $1.0017$ to $1.0152$. At index 0, where the source’s sweep logs a refusal without
an exact flag, the capture at the logged argmin times $197/200$ is $0.98639293768757$ (n
= 28) and $0.98672659027263$ (n = 30): all 32 refusals of each control have an exact
witness below one.

**A seeded search at sampled directions.** `direction_sample.py` searched for the least
capture at 33 rotated directions of each net, fixed before any ran: one drawn from each
of 24 strata by a generator seeded from the candidate’s SHA-256, and named directions
(1, 2, 1036, 2071, 2072, the source’s two least certified and the two least exact
least-bound centres).
At each, a $65 \times 65$ binary64 grid over the quadrant, a compass search from its ten
best points, one from the source’s least-bound centre and two from the axis argmin and
its transpose; every end point evaluated exactly.
This decides nothing between the points it evaluates: it can only find a capture below
one, or below the source’s certified bound, and it found neither.

|  | n = 28 | n = 30 |
| --- | --- | --- |
| Directions; exact end points | 33; 429 | 33; 429 |
| Least capture found (direction, centre) | $1.0007906$ (1703, $(3.4770, 3.9282)$) | $1.0007095$ (2038, $(3.3968, 3.6849)$) |
| Median of the per-direction least | $1.00167$ | $1.00160$ |
| A 99/100 witness found at every sampled direction | yes, 33 of 33 | yes, 33 of 33 |

**Controls on this review’s checker.** `selftest.py` holds the evaluators to each other
and to wrong readings:

- the polygon-clipping capture and a second exact method written apart from it (vertical
  chords integrated exactly) agree as fractions at 174 random and adversarial poses at
  directions 1, 2, 7, 296, 1036, 1777, 2071 and 2072, and the binary64 estimate the
  search uses is within $4 \times 10^{-13}$ of them;
- at the 31 oblique control witnesses of each certificate, this review’s reading
  reproduces every logged fraction, and each wrong reading reproduces none of the
  angle-sensitive ones (27 of 31 at n = 28, where four witnesses lie where the density
  is constant; 31 of 31 at n = 30): the standard step $83/40000$, half the declared
  step, and the rows without their $D_4$ images; the other field order is refused;
- the reader and the premises refuse a duplicate key, a float token, a second gzip
  member, a negative mass, a total mass of $n$, a step of $1/4999$ (so $B(1 + D) = 1$)
  and a last index of 2071 (the net stops short of $\tan(\pi/8)$);
- the axis decision refuses the 99/100 mutant of both: rigorous least captures
  $0.99140000843703$ and $0.99173535469008$, each with an exact witness below one.

## T-142’s Axis Gap Under #892’s Enclosure Rule

The census control counts the 99/100 mutant’s axis row as a refusal when the sweep
refused, its least vertex lies in the domain, the exact capture $F$ there is below one,
and $F$ is consistent with the bound $b$ the sweep reported.
Until #892 that last clause was $b \le F \le b + 10^{-9}$ (`AXIS_ROUNDING`); at n = 28
the gap $F - b$ is $2.15 \times 10^{-9}$, so the control would have failed closed.
#892 replaced the constant: the control recomputes, by a transcription of the crate’s
column walk, the enclosure $[\ell', u']$ the sweep holds at that vertex, and requires
$\ell' = b$ to the bit and $\ell' \le F \le u'$.

What this review established apart from the crate and the census:

- **The gap belongs to the certificate’s axis vertex, not to the control.** In the
  source’s own run of the original, the sweep reported $1.0014141477613605$ at
  $(4.2428000208779879, 2097/400)$, where the exact capture is $1.00141414993662\ldots$,
  a gap of $2.1753 \times 10^{-9}$. In the source’s 197/200 control the same vertex
  gives $2.1426 \times 10^{-9}$, a ratio of $0.98499$. Scaled by $99/100$ the original’s
  gap is $2.1535 \times 10^{-9}$, the census’s figure.
  At n = 30 the same computation gives $1.90 \times 10^{-10}$ and $1.88 \times 10^{-10}$
  at 99/100.
- **The vertex is the last of its column.** $2097/400 = L - 1/2$ is the quadrant’s upper
  edge, reached after about 4,100 steps of a column walk, each of which widens its
  interval. The exact capture is the same, to the last digit, at an interior vertex of
  the same column ($y = 5.0809308983748918$). A direct binary64 evaluation, such as this
  review’s matrix product, is within its a priori bound of $2.3 \times 10^{-13}$
  (relative) at every vertex, and was within $3 \times 10^{-16}$ at that tied vertex.
  So $2.2 \times 10^{-9}$ is the width the sweep’s method builds there, the mechanism
  the 14 October review found at n = 39, where the least vertex was also last in its
  column. At n = 30 the source’s argmin is interior, and the gap is ten times smaller.
- **The refusal is genuine.** The mutant’s exact capture at that vertex is
  $99/100 \cdot F = 0.99140000843726 < 1$, at a vertex of the quadrant
  $[L/2, L - 1/2]^2$; this review’s complete axis decision refuses the mutant with the
  same value.

**Judgment.** #892’s rule judges this gap correctly.
The clauses that decide whether the refusal counts are exact, a capture below one at a
vertex in the domain, and this review established both from the certificate.
The enclosure clause ties the reported bound to the walk; the walk’s interval contains
the exact capture whatever its width, so a $2.15 \times 10^{-9}$ gap passes it when the
transcription is faithful and shows nothing wrong.
No constant could do the same job, since the gap varies with the vertex’s place in its
column. The gap is no defect of the certificate: the original’s least axis capture is
$1.0014$, $1.4 \times 10^{-3}$ above one.
Whether the census receipt meets the rule ($\ell' = b$ to the bit and $F \le u'$) is for
the replay lane and whoever reads its receipts; this review did not read them.

## Trust Boundaries and What the Checkers Share

| Checker | Decides | Trusts |
| --- | --- | --- |
| The source’s `sqverify-proof-net` (build source `ab6e33e1…`, binary `ec04d332…`, 12 threads) | Coverage at all 2,073 directions of each net, one reported run each; the 197/200 control at 32 | This repository’s crate as adapted by the source, whose changed `certificate.rs` nobody here has read; rustc 1.98.0; its machine; that the logs are the run’s |
| The maintained `sqverify-fast` (source `d97758bb…`), for the census | Coverage at all 2,073 directions with whole-net controls, once its receipts are recorded | The reviewed crate, census driver and controls, including #892’s rule; rustc 1.98.0; this host |
| This review’s programs | Every exact premise; direction 0 of each net completely; the capture at 4,144 least-bound centres, 66 control poses and 858 search end points | CPython 3.14.7’s `fractions`; IEEE binary64 in OpenBLAS `dgemm` under the stated bound; its own code |

The source’s checker and the maintained crate share the whole crate apart from the
declared-net reader, so the census is a re-implementation sharing the producer’s
components, as the entries’ `composition` already says.
This review’s programs share no code with either: they were written from the mathematics
and `SPEC.md` before any of the producer’s or the crate’s code was read, which it never
was. All three share the mathematics (steps 1 to 7 and the quarter turn) and the reading
of the format; the reading is checked against the source’s own exact values, and the
mathematics was re-derived above.
An error in that shared mathematics would pass all three; none was found.
Authorship overlaps at the system family: each source commit names Claude Opus 5.5 as
co-author, the crate the source adapted was written by a Claude agent of this project,
and this review is a Claude agent with its own prompt and files.

## Findings

No finding is blocking or major for either certificate.
Grades: blocking, major, minor, note.
Paths are the source’s, under
`problems/square-lower-bounds/certificates/mixed_n28_L57425/` at `36b85b9` and
`mixed_n30_L58925/` at `ff9f269`; both READMEs have the same line numbers.

**M-1 — minor, author.
`README.md` line 15 names a control log that does not exist.** It lists
`check2/control.json, check2/control.jsonl.gz`; the release asset holds
`check2/control-197_200.jsonl.gz`, which `files-sha256.json` also lists.
The same correction was asked for the n = 31 and #446 bundles.

**M-2 — minor, author.
`files-sha256.json` line 2 gives the sealed README’s digest.** It lists `README.md` as
`6c2e71ff…` (n = 28) and `314be456…` (n = 30), the editions in the sealed bundles; the
published READMEs are `f0e782cf…` and `42ba3e43…`, because the pre-publication paragraph
(line 54) was added after the manifest.
So the published directory’s manifest does not verify its own README.

**M-3 — minor, author.
The check is called independent.** `check2/receipt.json` line 90 calls it “an
independent second-system check (built from the certificate specification only, without
reading the search code)”, `README.md` line 12 “the independent second-system check”,
and line 54 “the independently implemented `sqverify_fast`”. It is independent of the
search code, but the verifier is this repository’s `sqverify_fast` with one change
(receipt line 89, README lines 17 to 19). A reader of the bundle alone could count it as
a second implementation beside jlevy/squares’ verifier; it is not, which is why a replay
here is recorded as sharing the producer’s components.

**M-4 — minor, author.
The README describes a second run that the receipts do not show.** Line 54 says the
candidate “was checked again” before publication on “a fresh Ubuntu 24.04 … machine”.
At n = 30 the pre-publication receipt is the check2 receipt’s own run record: the same
start `2026-10-10T12:01:39Z`, the same 1,790.3 s, 12 threads and binary `ec04d332…`
(`verification/prepublication-receipt.json` lines 28 and 29). At n = 28 it states 772 s
against the check2 run’s 771.9 s (receipt line 35), with no start time or binary digest.
So each certificate carries one evidenced complete run, as the record already says.
Publish the second run’s own receipt and log, or say that the pre-publication receipt
restates the check2 run.

**N-1 — note. The certificates prove the strict bound.** No packing fits at side exactly
$L$ (`README.md` line 3), so $s(n) > L$; line 5 and the record state $\ge$, which is
what a lower-bound entry means.
Nothing to change.

**N-2 — note. The source’s control is sampled and 1.5% below the threshold.** It shows
the check is not vacuous, and every one of its refusals is genuine (above).
It is not the whole-net control the route requires (the 99/100 mutant at every
direction), which the census runs.
Expect that control to refuse everywhere: the search found a 99/100 witness at all 66
sampled directions, the axis decision refuses the mutant at index 0, and the least-bound
centre is itself a witness at 1,187 (n = 28) and 979 (n = 30) of the 2,072 rotated
directions. It still has to run.

**N-3 — note.
The margins are wider than the logs suggest.** The source’s least certified
bounds go down to $1 + 1.07 \times 10^{-11}$ (n = 28, direction 1088) and
$1 + 2.93 \times 10^{-11}$ (n = 30, direction 1585). That is where its branch and bound
stopped: the exact captures at those boxes’ centres are $1.114$ and $1.017$. The least
captures this review found are $1.00079$ and $1.00071$ over the sample, $1.0014$ and
$1.0018$ at the axis.

**N-4 — note.
The runs rest on an adapted crate nobody here has read, and its public copy
was not checked.** Both receipts give build source `ab6e33e1…`, and both bundles’
`check2/src/UPSTREAM_COMMIT` name `42534d959d668c5e03839dc87f9e628fa4fc2d83`, the commit
the #446 review found that jlevy/squares does not hold (its F-8); the archive is
`e495f9bf…`, as in the n = 29 and #446 packets.
Receipt line 89 now also names a public copy, `fine_net_verifier/` in
wand125/square-packing-tools at `5fba675`. This review could not check that commit
(GitHub access to that repository is not enabled for this session) and did not read the
crate in any case. This is why the runs stand at `V0` and the census with the reviewed
`d97758bb…` is the step that counts.
It is not a defect of either certificate.

**N-5 — note. The soundness document beside the archive predates the declared net.** By
the manifest, each bundle’s `check2/src/SOUNDNESS.md` is `16f1e679…`, the file the #446
review identified (its F-7) as this repository’s of 3 October, before lemma N0.
`SPEC.md` §5 states the premises the checker relies on, so nothing in the mathematics is
wrong; a reader of the bundle finds an outdated note beside the archive.

**N-6 — note. The n = 30 run’s wall time exceeds its CPU.** Its summary gives 21,422.2
direction-seconds of wall against 14,334.5 of CPU (`check2/receipt.json` lines 61 and
62), where n = 28’s agree (9,214.0 and 9,204.0). Its 12 threads probably shared fewer
cores than the n = 28 run’s. This matters only for pricing a replay from the source’s
figures.

**N-7 — note. `README.md` lines 47 to 50 compare CPU-hours with wall time.** “About 24
CPU hours per certificate” for the earlier bundles stands beside “minutes per
certificate” for this check, which took 9,204 and 14,335 direction CPU-seconds (2.6 and
4.0 CPU-hours), 772 s and 1,790 s of wall at 12 threads.

**R-1 — note, record.
The pending-review clauses.** T-142’s and T-143’s `next_rung`,
`unfinished_confirmations` and `notes`, the two report entries’ `limitations`, and the
`source-evidence` blockers of `n-028.md` and `n-030.md` say that a review which reads
the certificate is pending.
The change that maps this review rewrites them to say it is retained, and the entries
derive `C1`. Their claims are otherwise accurate in every number checked: the rows, the
masses, the net’s premises and margins, and the gains of $3/400$, $1/400$ and $9/1000$.
As the #446 review noted of its entry, “every such core capturing mass at least one”
means every core at a net angle centred in its per-bin domain.

## Questions for the Author

1. Would you correct the control log’s name in the README (M-1) and regenerate
   `files-sha256.json` after the pre-publication paragraph, or say that it describes the
   sealed bundle (M-2)?
2. Could the receipt and README say that the check is independent of the search and is
   jlevy/squares’ `sqverify_fast` with the declared-net change (M-3)?
3. Was the pre-publication check a second run?
   If so, would you publish its own receipt (start time, binary digest) and log (M-4)?
4. Is `fine_net_verifier/` at wand125/square-packing-tools `5fba675` byte for byte the
   archive `sqverify-proof-net-fe12e036c.tar.gz` (`e495f9bf…`), and could
   `UPSTREAM_COMMIT` name a public commit (N-4)?
5. How many physical cores did the n = 30 run use (N-6)?
6. Your search must have aimed at some least capture.
   This review finds about $7 \times 10^{-4}$ of slack at the tightest sampled
   directions (N-3); is that the margin you targeted, and is the least capture over all
   2,073 directions recorded?

## Rungs and Significance

**Now.** Each entry stood at `V0/C0`. With this review recorded as the `external_review`
of its reported entry (state `informally-verified`) and listed in the entry’s `reviews`
(kind `adversarial`, verdict `accepted`), each derives `V0/C1`, a read of a recorded
claim, as the change that maps this review records.
This review’s own runs are a sample (direction 0 of 2,073 decided, and poses); they set
no rung and belong in the case records.

**Once the census and its controls are recorded.** For each certificate, the 6 October
checklist items about the file, the premises and the mathematics hold: item 1 (format M
with no points, no `scaling_factor` key, `proof_net` with exactly `step` and `last`, no
top-level `net`, no metadata; eight times the densest image density $616{,}441$ and
$425{,}644$, far below $2^{32}$), item 3 (lemma N0’s (a) to (e) in exact arithmetic
apart from the crate, the mass $n - 1/100000$) and item 7 (this review).
Items 2, 4, 5, 6 and 8 concern the census’s receipts and words.
A complete `sqverify-fast` capture at all 2,073 directions with a `CONTROLS_REFUSED`
whole-net receipt, held to those items and with T-142’s axis leg judged by #892’s rule
as above, supports `V3/C3`, confirmed, re-implemented sharing the producer’s components.
Beside it: decided at 1 of 2,073 directions and evaluated at poses, independently
re-implemented (clean-room), by a Claude agent, a system family the producer also used.
`V4/C4` would further need a second adversarial review by a distinct reviewer and a
human oversight record.

**Significance: S3 for both, as drafted.** If correct, each is the strongest lower bound
on record at its count, by the certificate kind and declared net of T-132 and T-232,
with no new technique: a substantive case result, as T-102 to T-111, T-132 and T-232
are. Neither is a reusable technique or bound family (S4), and n = 28 and n = 30 are not
central open cases (S5). Once adopted, the gap to the upper bound narrows from $0.0894$
to $0.0819$ at n = 28 and from $0.1165$ to $0.1075$ at n = 30.

## Reproduction

From the repository root, with the project interpreter and one BLAS thread:

```bash
PKT=packing/resources/web/wand125-fine-net-n28-n30-2026-10-10
R=$PKT/review/review-2026-11-11
REL=$PKT/release/certificates
PY="packing/.venv/bin/python3 -I"
export OPENBLAS_NUM_THREADS=1
$PY $R/programs/premises.py --release $REL --out $R/outputs/premises.json
$PY $R/programs/receipts_check.py --release $REL --premises $R/outputs/premises.json \
  --out $R/outputs/receipts-check.json
$PY $R/programs/axis_decide.py --release $REL --out $R/outputs/axis-decision.json
$PY $R/programs/axis_decide.py --release $REL --factor 99/100 \
  --out $R/outputs/axis-decision-99_100.json
$PY $R/programs/direction_sample.py --release $REL --receipts $R/outputs/receipts-check.json \
  --out $R/outputs/direction-sample.json
$PY $R/programs/selftest.py --release $REL --out $R/outputs/selftest.json
```

Each exits 0 on the retained packet and prints its verdict.
The two outputs over 1,000 lines are kept gzip-compressed (`receipts-check.json.gz`,
`direction-sample.json.gz`), as the packet’s retained-data rule requires; a rerun writes
them plain. The programs ran at `nice -n 19`, at most two at a time, from a scratch copy
outside the packet that is byte for byte the retained one
(`outputs/program-digests.sha256`); the packet’s
[README](../../../packing/resources/web/wand125-fine-net-n28-n30-2026-10-10/review/review-2026-11-11/README.md)
lists what each printed and what failed along the way.
The final pass took 255 CPU-seconds; with trials and earlier passes, about 11
CPU-minutes in all.

## Comparison With Earlier Reviews

No earlier review read either certificate.
After the findings above were written, this lane searched `docs/project/reviews/` for
the two certificates, their sides, T-142 and T-143. Three reviews and three tracker
files name them:

- **The 11 October final review of PR 487’s lower bounds** read the records and the
  intake’s premises only.
  Its exact differences ($3/400$, $1/400$, $9/1000$) and net facts are the ones
  recomputed here, and it kept `S3` on both pending the review that reads the
  certificates; this review keeps `S3`.
- **The 11 October review of register rungs** found both at `V0/C0` and T-142’s
  whole-net control held on an owner decision.
  #892 has since replaced that decision with the enclosure rule judged above.
- **The 14 October review of the n = 37, 39 and 44 certificates**, §5 and F-1, named
  T-142’s gap of $2.15 \times 10^{-9}$ and found, by emulating the crate’s column walk
  at n = 37, 39 and 44, that the census’s gap is half the sweep’s enclosure, widest at
  the last vertex of a column, and that every axis refusal is sound under every option;
  #892 implemented its option 2. This review reached the same reading of T-142’s gap
  without the walk: from the source’s own logs (the gap is present in the original run
  and scales with the control’s factor), from the vertex’s place at the column’s end,
  and from an exact witness of its own.
- The tracker files (`review-2026-10-12-bead-reconciliation-*.json`) dispose of beads
  and read no certificate.

The n = 31 and #446 reviews of 23 October were read before this one began, as format
models. Of their findings, M-1, M-2 and M-3 of the n = 31 review recur here as M-1 to
M-3, and F-7 and F-8 of the #446 review as N-5 and N-4; each was re-established here
from these bundles’ own files and digests.
M-4 and N-6 are new to these bundles.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
