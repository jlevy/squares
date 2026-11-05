# Özden’s s(94) ≥ 2493/250, Hosono’s Measure Dilated Again: Stage 4 Mathematical Review

**Date:** 2026-11-05. **Subject:** `certificate/n94-L9972.json.gz` of
[kenaznia-doga/s94-lower-bound-9972@7d21f9b](https://github.com/kenaznia-doga/s94-lower-bound-9972/tree/7d21f9bdf707102dd4ebf47e52f81b502a01004d),
Doğa Özden’s certificate for $s(94) \ge 2493/250 = 9.972$, posted as issue
[#910](https://github.com/jlevy/squares/issues/910) and retained as the packet
[ozden-s94-lower-bound-9972-2026-11-05](../../../packing/resources/web/ozden-s94-lower-bound-9972-2026-11-05/README.md).
Draft pull request [#912](https://github.com/jlevy/squares/pull/912) registers it.
Bead `think-xzxd`, child of `think-pi8b`.

**Reviewed at:** branch `claude/bold-ritchie-xo28us-l49`, head `31698c39b`.

**Reviewer:** Claude (AI review), strong tier (`tbd-strong-max`) at maximum reasoning, the
stage 4 mathematical review lane, separately prompted.
It shared no context with the import lane.
It read the sources and the lab’s receipts as data and ran only programs of its own. The
programs, with their README and receipts, are kept in the packet’s
`review/review-2026-11-05/` directory. It is not a human oversight record.

## Summary for the Author

**Verdict: accepted.** The certificate proves $s(94) \ge 2493/250$ provided that every
core it declares captures mass at least 1, at all 4,972 directions of its net. Your
receipts say so. This repository’s complete replay will decide that whole-net condition.
The argument from the certificate to the claim is complete, and every other premise
holds in exact arithmetic. I found no defect; the findings below are notes.

- **The premises.** In exact rationals:
  - $B(1 + D) = 99498934887/99500000000 < 1$, with a margin of $1065113/99500000000$;
  - $t_{\max}^2 + 2t_{\max} - 1 = 1649/16000000 > 0$, and $\tan(\pi/8)$ lies in the
    last node’s bin and in no earlier one;
  - the tangent form $B(1 + D/(1 - D^2/4)) = 14327846598855339/14327999975125000 < 1$;
  - the total mass is $94 - 1/100000$;
  - the 853 orbits expand to 6,720 distinct rectangles, a density invariant under all
    eight symmetries of the box;
  - each row is exactly $4986/4975$ times Hosono’s, with its mass unchanged.

  Your certificate’s text and its gzip regenerate byte for byte from Hosono’s candidate
  by a rule this review wrote for itself.
- **Decided here.** Code written for this review decided 26 of the 4,972 directions,
  each over its whole per-bin quadrant, and every one is verified.
  - Direction 0 was decided exactly: all 29,495,761 vertices, minimum
    $1.003086850384903\ldots$, on the wall edge $y = L - 1/2$, in the strip the
    dilation adds.
  - The other 25 directions were decided with proved binary64 bounds. They include 3663,
    4971, 1198, four directions from each of your compacted streams B, C and D, three
    shared nodes and the two nearest the axis.
- **The margins are not $10^{-13}$.** The least certified bound in your archive,
  $1.0000000000003892$ at direction 3663, is where one search leaf stopped, as your
  README says.
  - At 3663 the least capture lies between $1.0035$ (proved here) and
    $1.0036681552\ldots$ (an exact pose). Your least-bound box there captures at least
    $1.03004$ throughout, decided exactly.
  - The smallest capture seen in the sample is at 1198, where the least capture lies
    between $1.0010$ (proved here) and $1.001120207\ldots$, the original’s capture at
    your own control witness.
- **Your control holds exactly.** At 1198 your rational witness gives the 99/100 mutant
  exactly the stated capture $0.991109005346039\ldots$, and so does the checker’s binary64
  witness ($0.99764492\ldots$). Both lie in the per-bin domain and the quadrant, where the
  original captures $1.001120207\ldots$ and $1.007722142\ldots$. At direction 0 the mutant’s
  least vertex is $0.993055981881054\ldots$.
  At each of the 26 sampled directions an exact in-domain pose takes the mutant below 1.
- **Your receipts, read as data, hold together.**
  - The six streams cover each index 0 to 4971 once, and every row of every stream is
    verified.
  - Each selected line is byte for byte its stream’s line.
  - The 67 directions run twice agree in bound and in node count.
  - What compaction removed bears on nothing the proof needs.
- **The dilation carries the measure, not the coverage.** In Hosono’s coordinates your
  cores are his, of side $9977/10000$.
  - 4,952 of your 4,972 angles are new.
  - At the 20 shared angles the centre domain grows by $1.934 \times 10^{-4}$ to
    $1.516 \times 10^{-3}$, and by $11/9972$ at the axis.
  - At the axis the minimum capture moves into that new strip: $1.0031817\ldots$ on
    Hosono’s domain, $1.0030869\ldots$ on yours.
- **Your answers to the earlier review’s notes F3 to F5** are right as far as this packet
  shows.
- **Significance.** The draft score S3 is confirmed.

Findings F1 to F3 are notes for you, and F4 to F6 notes for this repository’s records.

## Scope

**Read and checked:**

- the certificate as stored (SHA-256 `f59d4c95…360c`) and its JSON text (`d1df3bc6…951c`);
- the packet’s README and `source/README.md`, and issue #910’s text;
- the receipts: `receipts/INDEX.json.gz`, `selection.csv`, `directions.jsonl.gz`, and
  `native/{A..F}.jsonl.gz` with their summaries;
- the controls: `controls/mass-99-100.json.gz`, `native-mutant.jsonl` and `control.json`;
- Hosono’s `candidate.json.gz` in the
  [wand125-mixed-bounds-evening-2026-10-04](../../../packing/resources/web/wand125-mixed-bounds-evening-2026-10-04/README.md)
  packet (`df3ae678…d27c`, JSON `64d81953…0667a`), with his `mixed_n94_L995` README and
  replay record;
- `packing/sqverify_fast/SOUNDNESS.md` and the crate’s README, as the specification of
  the theorem and of the checker’s verdicts;
- the
  [declared-net soundness review](review-2026-10-06-sqverify-fast-declared-net-soundness.md#for-the-records-lane)
  and the
  [control review](review-2026-10-06-sqverify-fast-census-control-fc1.md#for-the-records-lane),
  for their records-lane checklists.

**Not read before the findings were written:**

- the crate’s `src/` and the lab’s copy of it under `verifier/`;
- the lab’s `tools/`, `checks/` and `exploratory/`;
- `devtools.audit_dilated_measure`;
- the review of #890’s certificate and its programs;
- the import lane’s `receipts/dilation-audit.json`, `native-receipt-audit.json` and
  `sample-diagnostic.json`.

Their SHA-256 at the start were `8e2eca2d…57d2`, `190368fd…3630` and `5c8d71df…6d5f`.

**Seen first, disclosed:**

- The packet README describes the import lane’s audit and states some of its numbers:
  the growth figures, the witness captures and the 13-direction sample.
- The bead `think-xzxd` states the import lane’s three N0 values and summarizes the
  earlier review’s notes F3 to F5.
- The parent bead’s draft reply quotes one figure from that earlier review: the growth
  on #890’s net, $6.55 \times 10^{-5}$ to $1.062 \times 10^{-3}$.
- For this document’s layout I read the opening, headings, findings table, run log and
  verdict of the
  [review of 4 November](review-2026-11-04-ozden-893-894-299-204.md). That review is of
  other results, and it mentions #890 once.
- Before freezing the findings I read issue #910’s text, to check the credit sentence.
  It refers to the earlier review’s $n = 31$ note: a “mass-scaled d529 receipt” and a
  value $0.99999999719$ that the issue does not use.

Every value above was recomputed here and none was copied.

## The Claim and What It Needs

The certificate gives
$L = 2493/250$, $B = 24872661/24875000$, a declared net (`proof_net`) of step
$D = 1/12000$ and last index 4971, and 853 orbit representatives
$R_j = [x_1, x_2] \times [y_1, y_2]$ with masses $w_j \ge 0$, listed as
`[x1, y1, x2, y2]`. All 853 rows are valid in that order, against 785 in the other.
Its density on $K = [0, L]^2$ is
$g = \sum_j \frac{w_j}{8|R_j|} \sum_{S \in D_4} \mathbf 1_{S(R_j)}$, which is
nonnegative and $D_4$-invariant, with $\int g = M = 9399999/100000$.

I re-derived the argument for this certificate as follows. Let 94 unit squares with
disjoint interiors lie in $K$.

1. **Fold (N2).** Take each square’s angle $\varphi \in [0, \pi/2)$. If $\varphi > \pi/4$,
   reflect that square alone in $y = x$. The reflection maps $K$ to itself and preserves
   $g$, and the angle becomes $\pi/2 - \varphi$. So assume $\varphi \in [0, \pi/4]$.
2. **Net (N1).** $\tan(\varphi/2) \le \tan(\pi/8)$. The nodes $t_r = r/12000$,
   $r = 0, \dots, 4971$, are spaced by $D$, and $t_{4971} = 1657/4000$ exceeds
   $\tan(\pi/8)$ by $3.64 \times 10^{-5}$, about $0.44D$. So some node has
   $|\tan(\varphi/2) - t_r| \le D/2$. The last node’s bin contains $\tan(\pi/8)$, and
   the one before it does not.
3. **Shrink (N3).** The concentric core of side $B$ at angle $\theta_r = 2\arctan t_r$
   is turned by $\delta$ relative to the square, with
   $z = \tan(\delta/2) = |\tan(\varphi/2) - t_r|/(1 + t_r\tan(\varphi/2)) \le D/2$.
   Its extent along the square’s axes is
   $B(1 + 2z - z^2)/(1 + z^2) \le B(1 + D) < 1$, so the closed core lies in the open
   square.
4. **Domain (lemma D).** The square’s centre is at least
   $\rho(\varphi) = (\cos\varphi + \sin\varphi)/2$ from each wall. In terms of
   $a = \tan(\varphi/2)$, $\rho = (1 + 2a - a^2)/(2(1 + a^2))$, which increases on
   $[0, \sqrt2 - 1]$ since its derivative’s numerator is $2(1 - 2a - a^2)$. So the
   centre lies in $[\rho(a_r), L - \rho(a_r)]^2$, with $a_r = \max(0, t_r - D/2)$.
5. **Quarter turn (C1).** The rotation by $\pi/2$ about $(L/2, L/2)$ preserves $g$ and
   maps a core at angle $\theta_r$ to a core at the same angle, so the capture
   $F_r(c) = \int_{Q_r(c)} g$ is invariant under it. Every point of the per-bin domain
   has an image in the quadrant $[L/2, U_r]^2$, $U_r = L - \rho(a_r)$. No reflection is
   used here, since a reflection would reverse the angle.
6. **Count (N4).** If $F_r \ge 1$ on each quadrant, the 94 cores are pairwise disjoint,
   each captures at least 1, and $94 \le \int_K g = M < 94$.

So no packing exists in $K$, and $s(94) \ge 2493/250$.
The only premise not decided in exact arithmetic is the coverage in step 6, at every
$r$.

Two facts of this certificate deserve a sentence each:

- **The domain is never limited by the core.** At every node the per-bin margin
  $\rho(a_r)$ exceeds the core’s own half-extent $B\rho(t_r)$, least by
  $5.36 \times 10^{-6}$ at $r = 1$. So the per-bin margin, not the core, sets the domain
  everywhere.
- **The symmetry holds for this measure.** The expanded density is invariant under all
  eight symmetries, checked image by image on the 6,720 rectangles, the quarter turn
  among them. So your README’s domain sentence (`source/README.md:27`) is right.

## The Exact Premises

`premises.py` recomputes everything from the retained bytes:

| Premise | Value | Holds |
| --- | --- | --- |
| Format M: keys, `points` empty, `proof_net` of `step` and `last` only, no `net`, no metadata | as stated | yes |
| Every mass $\ge 0$, every rectangle nondegenerate in $[0, L]^2$, total the exact sum | $M = 9399999/100000$ | yes |
| N0 (a): $D > 0$, $2 \le N_\theta \le 2^{16}$ | $D = 1/12000$, $N_\theta = 4972$ | yes |
| N0 (b): $B(1 + D) < 1$ | $99498934887/99500000000$ | yes |
| N0 (c): $t_{\max}^2 + 2t_{\max} - 1 > 0$ | $1649/16000000$ | yes |
| N0 (d): $t_{\max} \le 1/2$ | $1657/4000$ | yes |
| N0 (e): $B(1 + D/(1 - D^2/4)) < 1$ | $14327846598855339/14327999975125000$ | yes |
| $\tan(\pi/8)$ in the last bin only | lower end $t_{\max} - D/2$ below it, bin 4970’s upper end below it | yes |
| $0 < B < 1$, $L^2 \ge 2B^2$, $L \le 1000$, rows $\le 10^6$ | | yes |
| Expansion: distinct images, integral | 6,720 rectangles, integral exactly $M$ | yes |
| $D_4$ invariance of the expanded density | every image present with equal density | yes |
| Densest row, $8 w/\lvert R\rvert \le 2^{32}$ (checklist item 1) | $8 \times 315356.7\ldots$ | yes |
| Expanded density $\le 2^{96}$ | at most $39419.59\ldots$ | yes |
| $U_r > L/2$ at every node | $U_r \in [9.264893, 9.472]$, $U_0 = 1184/125$ | yes |
| Each row $\lambda$ times Hosono’s, mass equal; $L = \lambda L_0$, $B = \lambda B_0$ | $\lambda = 4986/4975$ | yes |
| Regenerated JSON text and gzip (level 9, mtime 0, OS byte 255) | byte for byte | yes |
| Mutant: every mass $99/100$ of the certificate’s, rectangles equal | differs only in masses, `total_mass` and `derived_from` | yes |

The three N0 values equal those the bead states, recomputed rather than copied.

## What the Dilation Carries and What It Does Not

$B/\lambda = 24872661/24930000 = 9977/10000 = B_0$. So, in Hosono’s coordinates, your
certificate asks his measure for exactly what his certificate asked: mass at least 1 in
every core of side $9977/10000$. It asks this at other angles and over larger domains.
The unit square becomes a square of side $1/\lambda$, which may come closer to the
walls.

**What it carries:**

- the measure itself: positivity, containment, the $D_4$ symmetry, and the total
  mass, which a similarity leaves unchanged;
- coverage at the 20 shared angles over Hosono’s old domain, where the two claims
  coincide.

**What it does not carry:**

- **New angles.** Your net shares 20 nodes with Hosono’s 201: $r = 249j$ for
  $j = 0, \dots, 19$, which are his nodes $10j$. The other 4,952 angles were never
  decided for this measure before.
- **Domain growth.** At the shared nodes the centre domain grows by
  $m_0(t) - m(t)/\lambda$ in his coordinates, where $m$ and $m_0$ are the per-bin
  margins $\rho(\max(0, t - D/2))$ on each net. The growth runs from
  $1.934 \times 10^{-4}$ at $r = 249$ to $1.516 \times 10^{-3}$ at $r = 4731$, and is
  exactly $11/9972$ at the axis.
- **Hosono’s net.** It cannot carry the dilated core:
  $B(1 + 83/40000) = 996970870863/995000000000 > 1$.
- **The ceiling.** As $D \to 0$ the route needs $\lambda B_0 < 1$, so $L < L_0/B_0 =
  99500/9977 \approx 9.97294$. Your $L$ is $9.378 \times 10^{-4}$ below it.

The axis shows the uncarried part directly. On Hosono’s own axis domain (margin
$\lambda/2$ here), this review’s exact sweep has 5,426 events a side, so
$5425^2 = 29{,}430{,}625$ cells, the number his replay record states.
Its minimum is $1.0031817020942837\ldots$, on that domain’s wall edge.
His record’s integer table gives $1.0031738677875834$, $7.8 \times 10^{-6}$ lower,
consistent with a conservative integer table (his checker was not read).
On your domain the minimum is $1.0030868503849\ldots$, on your wall edge $y = 1184/125$,
in the strip the dilation adds.
Near the axis it is much the same. At $r = 1$ the least value found anywhere, $1.0034$,
lies in a strip along the wall edge as wide as the axis growth. At $r = 2$ that strip’s
least is $1.0031$, above an interior value of $1.0027$.
At the oblique shared nodes 249, 2490 and 4731 the added strips are covered with room to
spare (least centre values $1.0064$ to $1.0081$), and those directions’ least captures
lie inside the old domain.

## Directions Decided Here

**Direction 0** (`axis_exact.py`). At $\theta = 0$ the capture is a sum of products
$\rho_k\, o_k(x)\, o_k(y)$ of window overlaps, bilinear on each cell of the grid of
overlap breakpoints. So its minimum over the closed quadrant is at a grid vertex.
The program evaluates all 5,431 × 5,431 vertices exactly, as integers over a common
denominator of 34,803 bits, by exact column sweeps, and confirms the least by direct
evaluation. The minimum is $1.003086850384903\ldots$ at
$(40416310002402601137/6218750000000000000,\ 1184/125)$, the transpose of your
receipt’s argmin.
Your checker’s certified bound $1.003086849249175$ lies $1.1 \times 10^{-9}$ below it,
as a bound should.

**Oblique directions** (`bnb.py`). This is a branch and bound over boxes of centres,
written from the mathematics. The programs’ README gives its proofs and error budget.

- The capture at a box’s centre is bounded below by trapezoid sums of the vertical
  sections, which are concave, at nodes that include every breakpoint.
- The gradient is $C^1$ and is $\sum_k \rho_k (\sigma_k(x_1) - \sigma_k(x_2))$ in $x$,
  where $\sigma_k$ are edge lengths inside the core. The same holds in $y$.
- Each edge length is enclosed over the box from its corner values. It is concave in
  the centre, so its least value is at a corner.
- Where all active pieces are the same at the four corners, the edge length is affine
  and is summed exactly. This keeps the cancellations between rectangles that make the
  bound sharp.
- The mean value theorem gives the box’s bound.
- Every binary64 quantity carries an explicit error budget, the largest $1.09 \times
  10^{-9}$ over all runs, and every acceptance clears it.

Before any run, `validate_bnb.py` checked the components against exact polygon
clipping at 48 random poses at four directions:

- the centre estimate was within $7.5 \times 10^{-13}$ of the exact capture, and the
  centre bound was never above it, and at most $2.7 \times 10^{-8}$ below it (at
  $r = 1$, where $1/s$ is largest);
- 192 of 192 gradient enclosures contained the exact difference quotient;
- no rectangle was misclassified.

| r | your stream | node | your bound | here | nodes here | least bound here | least centre here | CPU s |
| ---: | --- | --- | ---: | --- | ---: | ---: | ---: | ---: |
| 0 | E | shared | 1.0030868492491749 | verified, exact | 29,495,761 vertices | 1.003086850385 | 1.003086850 | 96.4 |
| 1 | E | new | 1.0000000709435026 | verified | 103,965 | 1.000002101419 | 1.004091427 | 76.3 |
| 2 | E | new | 1.0000002681850386 | verified | 104,121 | 1.000001785891 | 1.002717714 | 71.7 |
| 20 | B | new | 1.0000000322457634 | verified | 103,631 | 1.000001016117 | 1.003025155 | 68.8 |
| 132 | C | new | 1.0000000001831773 | verified | 91,237 | 1.000000498812 | 1.004217504 | 74.2 |
| 249 | C | shared | 1.0000000387263885 | verified | 85,107 | 1.000001500309 | 1.004678366 | 64.3 |
| 733 | D | new | 1.0000000003292442 | verified | 83,847 | 1.000001741076 | 1.001625505 | 69.9 |
| 981 | B | new | 1.0000000000827345 | verified | 85,575 | 1.000000648844 | 1.002534365 | 74.8 |
| 1118 | D | new | 1.0000000062517893 | verified | 86,615 | 1.000000191747 | 1.001411149 | 68.5 |
| 1198 | F | new | 1.0000000635063402 | verified | 87,005 | 1.000001206189 | 1.001139629 | 69.9 |
| 1214 | B | new | 1.0000000002138310 | verified | 86,795 | 1.000001925228 | 1.001212589 | 70.5 |
| 1289 | C | new | 1.0000000001716707 | verified | 87,279 | 1.000000341084 | 1.001784229 | 77.7 |
| 1307 | C | new | 1.0000000000511857 | verified | 87,139 | 1.000000662147 | 1.001577259 | 72.5 |
| 1979 | D | new | 1.0000000003030902 | verified | 86,131 | 1.000000062434 | 1.002910288 | 72.1 |
| 2103 | D | new | 1.0000000000085920 | verified | 86,141 | 1.000000137777 | 1.003017722 | 70.6 |
| 2479 | B | new | 1.0000000001475295 | verified | 87,139 | 1.000000529974 | 1.001859520 | 75.6 |
| 2490 | A | shared | 1.0000000406223992 | verified | 87,265 | 1.000000267553 | 1.001962057 | 86.7 |
| 2684 | A | new | 1.0000000052733129 | verified | 87,279 | 1.000000584495 | 1.002558691 | 85.7 |
| 2900 | A | new | 1.0000001148154907 | verified | 87,661 | 1.000000708542 | 1.003049121 | 76.2 |
| 3284 | A | new | 1.0000000303145764 | verified | 88,383 | 1.000000445454 | 1.002798522 | 81.2 |
| 3663 | A | new | 1.0000000000003892 | verified | 88,797 | 1.000000229779 | 1.003668155 | 71.2 |
| 4034 | A | new | 1.0000000351927467 | verified | 89,735 | 1.000000060210 | 1.002853256 | 76.1 |
| 4579 | A | new | 1.0000000000231128 | verified | 97,491 | 1.000000611714 | 1.002458492 | 92.0 |
| 4731 | A | shared | 1.0000000496648556 | verified | 99,527 | 1.000000338246 | 1.002613345 | 90.4 |
| 4960 | A | new | 1.0000000207635720 | verified | 101,163 | 1.000000087168 | 1.003285691 | 83.7 |
| 4971 | A | new | 1.0000000442538448 | verified | 101,681 | 1.000000378675 | 1.003382298 | 87.1 |

The 25 oblique directions were fixed before any of them was run:

- 3663, 4971 and 1198;
- three of the five lowest bounds in your archive in each of B, C and D (B: 981, 1214,
  2479; C: 132, 1289, 1307; D: 733, 1979, 2103), A’s second lowest (4579), and B’s
  first index, 20;
- the shared nodes 249, 2490 and 4731;
- the two angles nearest the axis, 1 and 2;
- six new angles drawn with a fixed seed: 1118, 2684, 2900, 3284, 4034 and 4960.

That puts four directions in each of B, C and D, ten in A, three in E (the axis
included) and one in F.

“Least centre here” is the least capture at a box centre the search visited. It is an
exact capture at a pose, so it bounds the minimum from above; it is not the minimum.
`poses_exact.py` recomputed each of them in rationals, and each equals its binary64
estimate to $2 \times 10^{-13}$.

**Controls of this decider:**

- **The mutant.** The 99/100 mutant stops as a counterexample candidate at 1198 (511
  nodes) and at 3663 (255 nodes).
- **Thresholds.** At 1198, threshold $1.0012$ fails, at $(5.5635, 7.4443)$ beside your
  witness, and $1.0010$ verifies. At 3663, $1.0035$ verifies. The least captures are
  therefore in $[1.0010, 1.0011203]$ and $[1.0035, 1.0036682]$.
- **The least-bound box.** Your checker’s least-bound box at 3663 (centre
  $(8.0666936\ldots, 6.6730465\ldots)$, half-widths $0.0041914$ and $0.0020957$) was
  decided by `bnb_exact.py` entirely in rationals, in one box. The capture there is at
  least $1.0300449806\ldots$, and $1.0336467437\ldots$ at its centre.
- **The other least-bound centres.** Your rows keep a least-bound box at 13 of the
  sampled directions (those from A, E and F). Their centres capture $1.0073$ to
  $1.0986$ exactly.

None of this decides the other 4,946 directions. A sample can find an error and cannot
show that the rest has none.

## Your Receipts, Read as Data

`read_receipts.py` checks the archive against the premises recomputed above, and every
check holds:

- **The streams.** Each stream’s digests match the index. Its rows hold its scope
  exactly, once each. Its last line is its summary, equal as JSON to the separate
  summary file, with return code 0, no refusal and no injected fault. Its `premises`
  are the recomputed ones, with `input_sha256` the stored certificate’s.
- **The build.** Every stream records crate source `d97758bb…`, release and rustc 1.98.0.
  The receipts record no binary digest.
- **Every row.** All of them, selected or not, are verified at threshold 1 with a finite
  bound of at least 1.
- **The merge.** It holds 4,972 lines, indices 0 to 4971 once each, and each is byte for
  byte the line of the stream that `selection.csv` names.

**One complete run.** A union of these partial runs counts as one complete run, for
these reasons:

- The theorem’s coverage premise is a conjunction over directions. Each `verified` line
  asserts one conjunct, its own direction’s quadrant, decided by its own search.
- What a summary adds that depends on scope is the status (`VERIFIED` for the whole
  net, `PARTIAL` for a strict subset), the direction count, nodes, times and threads.
  The crate’s README defines `PARTIAL` as every requested direction verified on a
  subset, with exit 0. The premises and the build do not depend on scope, and they are
  the same in all six streams.
- No stream refused any direction, so the selection could not have chosen a verified
  line over a refusal.
- The 67 directions run twice (66 in A and E, and direction 0 in E and F) agree in bound
  67 times out of 67, and in node count 66 times out of 66.

So the union proves what one run would, provided these lines are what the reviewed build
printed for this input. That proviso is a statement of the lab’s, not something the
packet can show. The replay here settles it.

**The compaction of B, C and D** kept `method`, `min_certified_lower_bound`, `r`,
`threshold` and `verdict`. A verified row has no others among the proof fields the index
lists. It removed:

- `audit_every` and `audits`: the release audit’s sampling and count. A failed audit
  would have made the verdict `audit-failed`;
- `cpu_seconds` and `seconds`;
- `least_bound_box`, `leaves`, `nodes`, `max_depth` and `mean_boundary_rectangles`.

None bears on soundness.
What is lost is a reproduction fingerprint: node counts for 2,401 directions. The
certified bound remains, so the census can still compare every direction’s bound with
your line.

**Stream E** is an explicit list of 150 indices. It is exactly $\{0, \dots, 19\}$, plus
$\mathrm{round}(4971k/128)$ for $k = 0, \dots, 128$, plus $1195$ and $2590$. Of it, 84
lines are selected (0 to 19 and 64 more below 2486). The other 66 repeat A’s
directions, with equal bounds and nodes. It is honest as described, though the packet
states its formula only in your audit code (F3).

**Stream F** is the original certificate (input digest `f59d4c95…`) at 0 and 1198, both
verified: the positive half of your control. Its 1198 line is the only one at that index
and is selected. Its 0 line agrees with E’s in bound, and E’s is selected. It is honest as
described.

## The Control

Your `mass-99-100.json.gz` is the certificate with every mass, `total_mass` included,
exactly $99/100$ of the original. Rectangles and everything else are equal, apart from
`derived_from`. Your checker refuses it at 0 (axis sweep, least vertex $0.99305598\ldots$)
and at 1198 (counterexample candidate). `poses_exact.py` evaluates each stated witness
exactly:

| Witness | Mutant capture | Equal to the stated value | Original’s capture | In the per-bin domain and quadrant |
| --- | --- | --- | --- | --- |
| `control.json`, $(3477717289/625000000,\ 7444849783253/10^{12})$ at 1198 | $0.991109005346039\ldots$ | yes | $1.001120207420\ldots$ | yes |
| checker’s binary64 witness at 1198 | $0.997644921\ldots$ | yes | $1.007722142071\ldots$ | yes |
| checker’s axis argmin at 0 | $0.993055981881\ldots$ | (not stated exactly) | $1.003086850385\ldots$ | yes |

The control shows that the checker’s acceptance is not vacuous at two directions. It
says nothing about the other 4,970, as your README says. This review’s sample adds an
exact in-domain pose with mutant capture below 1 at each of its 26 directions. That is
expected everywhere: the least captures seen are $1.0011$ to $1.0047$, under $1/0.99
= 1.0101$.

## What the Census Row and Its Control Must Show

For `think-qcms`, by the
[checklist of 6 October](review-2026-10-06-sqverify-fast-declared-net-soundness.md#for-the-records-lane),
items 1 to 8, as this certificate needs them:

1. **The file.** Format M, `points` empty, a `proof_net` of exactly `step` and `last`,
   no top-level `net`, no certificate metadata, and eight times the densest row’s
   density at most $2^{32}$, as recomputed above. There is no `scaling_factor` key at
   all (F4).
2. **The case.** `n` 94 and `L` $2493/250$, status `VERIFIED`, return code 0,
   `refused_directions` empty, `directions_verified` 4,972, indices exactly 0 to 4971,
   each verified, threshold 1, and `least_bound_leaf_exact.clears_threshold` true.
3. **The premises.**
   - `format` M, `centre_domain` per-bin, `net_origin` proof_net;
   - `D` $1/12000$, `angle_count` 4972, `net_last_tangent` $1657/4000$,
     `B` $24872661/24875000$;
   - `mass_exact` $9399999/100000$, `shrink_bound` $99498934887/99500000000$;
   - no points or segments, `fault_injected_at_box` null.

   Lemma N0 is recomputed apart from the crate in `premises.py` here.
4. **The candidate.** `candidate_sha256` `f59d4c95…360c`, and
   `devtools.retained_data check` passes on the packet.
5. **The build.** `source_sha256` `d97758bb…`, release, rustc 1.98.0.
6. **The control.** `CONTROLS_REFUSED` over the whole net, with the 99/100 mutant at
   every direction, judged under CC-1 to CC-5 of the
   [control review](review-2026-10-06-sqverify-fast-census-control-fc1.md#for-the-records-lane):
   - only coverage refusals count;
   - every refusal pose lies in $[L/2, U_r]^2$ with $U_r$ computed exactly;
   - the original captures at least 1 at every refusal pose;
   - the rows reconcile with the summary;
   - captures are kept exact.

   The sample here predicts a refusal at every direction. A direction where the mutant
   verifies would not touch the claim, but it should be reported with its slack.
7. **The mathematics.** This review.
8. **The words.** The evidence text names the net, step $1/12000$ and 4,972 directions,
   and the accepted build. For this certificate it does not say “independently
   re-implemented”: your runs used this crate, so the replay is *reproduced with the
   producer’s code* (F5).

**Beyond the checklist.**

- The census should compare its certified bound with your selected line at every
  direction, and its node count wherever your line keeps one. Your own repeated runs
  agree exactly, so equality is the expectation. A difference would not weaken the
  census’s own verdicts, but it would mean your receipts did not come from this build and
  input, and should be reported.
- Neither the least certified bound of the census nor of your archive is a margin
  (F6).

## The Source’s Statements About Independence and Review

These are data, not evidence, and are graded as such.

- **What is not claimed.** “No proof-assistant formalization, human review of this new
  certificate, or independent institution’s replay of 9.972 is claimed”
  (`source/README.md:64`). This is accurate; nothing in the packet is any of these.
- **The exploratory checker.** “That C checker is not interval arithmetic”, offered as
  supplementary (`source/README.md:62`). This is accurate as a description. It was not
  read here and is not evidence.
- **Independence of the checker.** “Running third-party sqverify-fast in the lab gives
  an independent implementation” (`source/README.md:64`). The issue says it is
  independent relative to your exploratory C checker. That is true: neither was written
  from the other. In this record’s sense, though, it is the same implementation the
  replay here will run. See F2.
- **Authenticity.** “Every final direction has an authentic individual native receipt”
  (`source/README.md:39`). This is consistent as data, but the receipts carry no binary
  digest, so authenticity is your statement until the replay reproduces the lines.
- **T-262’s replay.** “jlevy/squares’ published replay of T-262 was of 9.965, not this
  new 9.972 certificate.” This is correct.

## Your Answers to #890’s Notes

The note numbers are those of the earlier review, which was not read before these
findings. What it asked is taken from the bead’s summary.

- **F3, the quadrant.** It stands for the whole per-bin domain through the quarter turn
  and the $D_4$-invariant measure (`source/README.md:27`). This is right. Only the
  quarter turn is used, and the invariance was checked here image by image.
- **F4, the growth.** It is $m_{\mathrm{old}}(t) - m_{\mathrm{new}}(t)/\lambda$ with each
  net’s own per-bin margin, and there is no universal $\rho(1 - 1/\lambda)$
  (`source/README.md:29`–35). This is right: recomputed at all 20 shared nodes.
- **F5, the $n = 31$ aside.** It is not reused, and the $n = 94$ mutant has its own
  inputs and witnesses (`source/README.md:127`). This is right for this packet. The
  mutant is exactly the 99/100 scaling, and both stated witnesses evaluate exactly to
  the stated captures.
- **The second question.** The ceiling $99500/9977$ stays, and nothing is claimed for
  the 9.97285 partial (`source/README.md:35`, 126). The ceiling is $L_0/B_0$, as
  derived above.

## Significance

**S3, confirmed.** The claim moves the best lower bound at $n = 94$ by $7/1000$, from
T-262’s $1993/200$ to $2493/250$. That is a substantive case result. It is on the route
of T-262, T-091 and T-178, each scored S3: a rectangle measure of Hosono’s on a net its
file declares, decided by this repository’s checker.
It is the T-262 technique again, a dilation of T-091’s `mixed_n94_L995` measure onto a
finer net, with nothing new in method, so not S4.
It is more than a citable detail, so not S2.
Since $s(94) \le s(95) = 10$, the gap at $n = 94$ narrows from $0.035$ to $0.028$.

## Credit

The record’s form, “Doğa Özden after Hiroaki Hosono, Tokoharu and this project”, is
right.

- The measure is entirely Hosono’s.
- The method is Tokoharu’s rectangle-density certificate.
- The declared-net theory and the checker are this project’s.
- Özden’s part is the choice of $\lambda$ and the net, and the runs.

The AI assistance should be stated as the source gives it. AI agents in his lab
constructed and rescaled the certificate, ran the checks and prepared the submission
under his direction. Both Claude (Anthropic) and OpenAI Codex agents assisted
(`source/README.md:131`). The record’s draft adds that they audited the receipts, which
the issue says. The record should claim no human review of the new certificate.

## Findings

| Id | Severity | Where | Finding |
| --- | --- | --- | --- |
| F1 | note (author) | `source/README.md:35` | The C front end’s maximum with the core’s half-width never binds: $\rho(a_r) - B\rho(t_r) \ge 5.36 \times 10^{-6}$ at every node, so its quadrant is never smaller |
| F2 | note (author) | `source/README.md:64`, also `:39` | “An independent implementation” is meant relative to your exploratory checker; to this record it is the producer’s checker, and the replay here reproduces with it |
| F3 | note (author) | `receipts/INDEX.json.gz` (stream E), `source/README.md:49`; `controls/mass-99-100.json.gz` | E’s formula, and why 1195 and 2590, are stated only in the audit code; the mutant’s `derived_from` reads “by99/100” |
| F4 | note (records lane) | [checklist item 1](review-2026-10-06-sqverify-fast-declared-net-soundness.md#for-the-records-lane) (line 579) | “`scaling_factor` 1”: this file has no `scaling_factor` key; read the item as absent or 1 |
| F5 | note (records lane) | checklist item 8 (line 629); the census evidence entry | “Independently re-implemented” does not apply: the replay is `same-implementation`, *reproduced with the producer’s code*; this review’s sample is the independent part, a sample with no rung |
| F6 | note (records lane) | packet `README.md:31`, 141 and 180; the draft reply in `think-pi8b` | The least certified bound $1.0000000000003892$ is quoted without saying it is a leaf bound; the least capture in the sample is above $1.0010$ |

**F1. The exploratory front end’s maximum never binds.** Your README says the C front
end “additionally takes the maximum with the B-core’s half-width, so its quadrant can be
smaller”.
By N3, the core at node $r$ fits inside every unit square of its bin, the one at
half-angle tangent $a_r$ included. So $B\rho(t_r) < \rho(a_r)$ always, and exactly here
the least difference is $5.36 \times 10^{-6}$, at $r = 1$. The maximum is $\rho(a_r)$ at
every node, and the two quadrants coincide.
Nothing depends on it.

**F2. Which implementation.** This repository counts a confirmation by the code that ran
against the code the producer used.
Your lab checked the certificate with `sqverify-fast`, so this repository’s replay with
the same crate is *reproduced with the producer’s code*. It is not an independent
implementation in this record’s sense. Your sentence is right in the sense the issue
gives it, independent of your exploratory C checker. Saying “independent of our
exploratory checker” in the README too would remove the ambiguity.
In the same spirit, “authentic” (`:39`) is your statement: the receipts carry no binary
digest.

**F3. Stream E’s rule.** The index lists E’s 150 indices explicitly and the README calls
them a “declared sample (formula checked by audit)”.
They are $\{0..19\} \cup \{\mathrm{round}(4971k/128)\} \cup \{1195, 2590\}$, a rule the
packet states only in `tools/audit.py`. Stating it, with the reason for 1195 and 2590,
in the README or the index would let a reader check E without your code.
Separately, the mutant’s `derived_from` reads “every mass multiplied by99/100”.

**F4. `scaling_factor`.** Checklist item 1 asks for `scaling_factor` 1. Your file has no
such key, as the packet README says. Your native runs admitted it, and the census’s own
admission will show whether the maintained build does. The item should be read as
“absent or 1” for this certificate.

**F5. The words for the replay.** Item 8 of the checklist was written for certificates
whose producer used another checker. Here the producer ran this crate, as the packet
README already records (`same-implementation`, `SAME_CRATE_PACKETS`).
- The census evidence, the claim and the reply should say *confirmed, reproduced with
  the producer’s code*, and cite this review beside the route review.
- This review’s programs are an independent clean-room implementation, but they decided
  26 of 4,972 directions. They are stated beside the rung as a sample: *sampled, 26 of
  4,972 directions, independently re-implemented*. They are never called confirmation.

**F6. A leaf bound is not a margin.** The packet README and the draft reply quote
“the least certified bound is 1.0000000000003892” without your README’s qualifier.
- At your least-bound box the capture is at least $1.03004$, decided exactly.
- At 3663 it is at least $1.0035$ everywhere.
- The least capture found anywhere in the sample is above $1.0010$, at 1198.

Wherever the record quotes the number, it should call it the least leaf bound of the
search.

## Questions for the Author

1. What chose E’s indices 1195 and 2590?
2. Do the pre-compaction streams B, C and D still exist? They are not needed for the
   proof, but their node counts would let a replay be compared row for row.
3. The 49,707-direction run toward 9.97285: did any direction refuse, or were all
   unfinished? A refusal would locate where coverage first fails on this route, below
   the ceiling $99500/9977$.

## What I Ran

All with CPython 3.14.7 (`packing/.venv`, through `run.sh`: `-I -B`, `nice -n 19`), at
most two processes at a time, on a shared four-core host.
The programs and their README are in `review/review-2026-11-05/programs/`, the receipts
in `review/review-2026-11-05/out/`.

| Command | Receipt | CPU |
| --- | --- | --- |
| `premises.py PACKET HOSONO OUT` | `premises.json`: `ALL_CHECKS_HOLD` | 0.4 s |
| `axis_exact.py CERT OUT` | `axis-r0.json`: verified, exact minimum | 96.5 s |
| `axis_exact.py CERT OUT 471177/49750` (Hosono’s axis domain) | `axis-r0-hosono-domain.json` | 106.2 s |
| `validate_bnb.py CERT OUT 1 3663 1198 4971` | `validate-bnb.json`: `ALL_HOLD` | 4.0 s |
| `bnb.py CERT R OUT` at 25 directions (`sample.sh`) | `sample/bnb-rR.json`: all verified | 1,908 s |
| `controls.sh` (mutant at 1198 and 3663, thresholds, exact box) | `controls/`: as stated beforehand | 202 s |
| `bands_regions.py`, `bands.sh` (added strips, near-axis strips) | `bands/`: all verified | 8 s |
| `poses_exact.py PACKET SAMPLE RECEIPTS OUT` | `poses-exact.json`: `ALL_HOLD` | 0.7 s |
| `read_receipts.py PACKET PREMISES OUT` | `receipts-read.json`: `ALL_CHECKS_HOLD` | 0.4 s |
| `tabulate.py PACKET OUT` | `sample-table.md`, `sample-summary.json` | 0.1 s |
| exploratory programs (decide nothing) | printed | 30 s |

In all, about 39.5 CPU-minutes, about 25 minutes of wall at two processes.

What went wrong along the way, and was redone:

- The receipt reader first failed on each stream’s last line, which is the summary. It
  now reads it and checks it against the summary file.
- `-I` alone leaves bytecode caches; `run.sh` added `-B` after the first runs, and the
  caches were removed.

## Verdict

**Accepted.** Every premise but the whole-net coverage holds in exact arithmetic, and the
argument from the certificate to $s(94) \ge 2493/250$ is complete given that coverage.

- Code of this review’s own decided 26 directions over their whole quadrants: the axis
  exactly, the rest with proved bounds. All are verified, and the least capture found
  lies above $1.0010$.
- Your control’s witnesses hold exactly, and your receipts hold together as data.
- No defect is open. F1 to F3 are notes for you, and F4 to F6 notes for this
  repository’s records lane.

Mapped as an adversarial review with verdict `accepted`, and beside a complete census
replay (`think-qcms`) whose row and control meet the list above, it supports `V3` and
`C3`. The rungs would read *confirmed, reproduced with the producer’s code*, with the
independent clean-room sample stated beside them.
`V4` and `C4` would need a second accepted adversarial review by a distinct reviewer and
a human oversight record.
The significance S3 is confirmed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
