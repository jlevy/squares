# Özden’s s(94) ≥ 1993/200 by a Dilated Measure: Stage 4 Mathematical Review

**Date:** 2026-11-03. **Subject:** `certificate/n94_L9965.json.gz` of
[kenaznia-doga/s94-lower-bound@9d76ad5](https://github.com/kenaznia-doga/s94-lower-bound/tree/9d76ad5549e99e952c899462b36d2bd765517969),
issue [#890](https://github.com/jlevy/squares/issues/890), retained as the packet
[ozden-s94-lower-bound-2026-11-03](../../../packing/resources/web/ozden-s94-lower-bound-2026-11-03/README.md).
It is Hiroaki Hosono’s `mixed_n94_L995` measure (T-091) dilated by
$\lambda = 1993/1990$, in format M on a net the file declares: step $83/120000$, `last`
599, 600 half-angle directions.
Pull request [#891](https://github.com/jlevy/squares/pull/891) registers it.
Bead `think-222u`. **Reviewed at:** branch `claude/bold-ritchie-xo28us-l33`, head
`e78e5963a`. **Reviewer:** Claude (AI review), strong tier (`tbd-strong-max`) at maximum
reasoning, the stage 4 mathematical lane, separately prompted.
It shared no context with the import lane, read the source and the receipts as data, and
ran only programs of its own, kept with their receipts in the packet under
[`review/dilated-measure-2026-11-03/`](../../../packing/resources/web/ozden-s94-lower-bound-2026-11-03/review/dilated-measure-2026-11-03/README.md).
It is not a human oversight record.

**Verdict: accepted.** The measure, read in format M on its declared net, proves
$s(94) \ge 1993/200 = 9.965$ by the measure-capture theorem under lemma N0, given the
coverage the replay decides at all 600 directions.

- **Premises.** Every premise but coverage holds in exact rationals, recomputed here
  apart from the crate.
  The values are $B(1 + D) = 2387749705363/2388000000000$,
  $t_{\max}^2 + 2t_{\max} - 1 = 3860089/14400000000$, the tangent form
  $1146119721592254871/1146239862908900000$, and the mass $94 - 1/100000$.
- **Net and domain.** The bins cover $[0, \tan(\pi/8)]$ with no gap, and 599 is the
  least `last` that does.
  The per-bin domain is nonempty at all 600 nodes.
- **Coverage.** Three runs of `sqverify-fast` decide it: the author’s two and this
  repository’s census.
  They are identical at every direction.
- **Checks here.**
  - Direction 0 is decided here in full by a separate implementation.
    Its least capture is $1.003117\ldots$, at the wall, in the strip the dilation adds.
  - At every other direction, the exact capture at the five corners and centre of the
    crate’s least-bound box is at or above the box’s certified bound.
  - A search at 19 directions found no capture below $1.0017633$. The author’s referee
    found a lower one, $1.0011230$ at $r = 144$, which this review reproduces exactly
    (added after reading it).
- **The dilation** is exact and is only how the candidate was found:
  - the centre domain grows toward the walls by $3/3986$ at $r = 0$ in Hosono’s
    coordinates, and by $6.5 \times 10^{-5}$ to $1.06 \times 10^{-3}$ at the other 199
    shared directions;
  - 400 of the 600 directions are new;
  - Hosono’s own net cannot admit the dilated core.

No finding is a defect of the certificate or of its mathematics.
One gap belongs to this repository’s records lane:

- **F1.** The control receipt fails closed on the census tool’s fixed $10^{-9}$ axis
  tolerance, so item 6 of the declared-net checklist is not met.
  Every refusal in it holds exactly here, and the verified lane should wait for
  `think-4uun`.

Five notes follow (F2 to F6). The draft significance S3 is confirmed.

## Scope

**Read.**

- `packing/sqverify_fast/SOUNDNESS.md` in full.
- The crate at the reviewed source `d97758bb…`, unchanged since `910b6b12c` on this
  branch: the format reader, `admit`, `declared_net`, `domain_upper` and `direction` in
  `src/certificate.rs`, and the lines that set each direction’s search box in
  `src/rotated.rs`, `src/axis.rs` and `src/lib.rs`. The author decided the certificate
  with this crate, so that is the producer’s code.
- Hosono’s description of format M, from his own specification in another packet.
- `packing/campaign/result-import.md` (stage 4), `epistemics.md` (confirmation,
  independence, review records, significance), and the 6 October declared-net soundness
  review (§1, §7, its findings and “For the Records Lane”).
- `review-2026-11-01-filled-end-lemma.md`, for form.
- From the packet:
  - the packet README and the source README;
  - `tools/rescale.py` and `verify.sh`;
  - the author’s two receipts;
  - `notes/n31-negative/`;
  - the import lane’s `receipts/dilation-audit.json` and `replay-comparison.json`.
- The census row, capture and control receipt.
- The pull request’s change to `devtools/sqverify_fast_census.py`.
- After every program here was written: the second checker’s `README.md`,
  `INTEGER-SOUNDNESS.md`, `independent.py`, `intcheck_final.cpp` and `run.sh`.

**Run.** Seven programs of my own before the findings were committed, and an eighth
after, all importing nothing from this repository or from the packet
([What I Ran](#what-i-ran)). They do five things:

- recompute every premise of the theorem except coverage, exactly;
- decide direction 0 in full;
- evaluate captures exactly at 3,000 sampled poses, and every control witness;
- refuse five mutants;
- after the findings, hold the referee report’s values to the same evaluator.

None of the author’s code ran, and neither did the crate, the census tools or the import
lane’s audit tool.

**Not read before my findings were committed.** The second checker’s `GRADE.md` and
`GRADE.json`, the author’s referee report.
I read them afterwards for
[the comparison](#comparison-with-the-authors-referee-report).
The bead’s brief named direction 144 as the one where that report finds its lowest
sampled capture; that is all I knew of it beforehand.

**Never read.** The referee’s own `exact_audit.py`, `finalize.py` and
`final_summary.json`, and `devtools/audit_dilated_measure.py` (only its two receipts).

**Not reviewed.** The crate’s soundness, which the 3 and 6 October reviews hold, beyond
the paths this certificate takes; whether any coverage leaf the crate accepted is right,
which only a second complete implementation could decide; the licence question
(`think-0so3`); the register entry.

## The Argument, Re-Derived

Notation as in `SOUNDNESS.md`: $K = [0, L]^2$, $L = 1993/200$, $B = 19884161/19900000$,
$D = 83/120000$, nodes $t_r = rD$ for $r = 0, \dots, 599$, $\theta_r = 2\arctan t_r$,
$g$ the $D_4$-symmetrised density of the 853 rows, and $F_r(c) = \int_{Q_r(c)} g$ for
the closed square of side $B$, centre $c$ and angle $\theta_r$.

1. **The measure.** Each row `{"rectangle": [x1, y1, x2, y2], "mass": m}` is an orbit
   representative whose eight images carry $m/8$ each, spread uniformly.
   Hosono’s own specification states the field order, and the crate reads it the same
   way. The other order would make 68 of the 853 rows degenerate.
   Every row is a nondegenerate rectangle inside $K$ with a positive mass.
   The images merge into 6,720 distinct rectangles, the receipts’ `expanded_rectangles`,
   and integrate back to $M = 9399999/100000 = 94 - 1/100000$ exactly.
   The expanded measure is invariant under all eight symmetries.
2. **Net (N1, N0 (a), (c)).** $D > 0$ and $N_\theta = 600 \in [2, 2^{16}]$. The bins
   $[t_r - D/2, t_r + D/2]$ tile $[-83/240000, 99517/240000]$ with no gap.
   Since $t_{599}^2 + 2t_{599} - 1 = 3860089/14400000000 > 0$, the last node
   $t_{599} = 49717/120000$ lies above $\tan(\pi/8) = \sqrt 2 - 1$. That tangent lies in
   bin 599 alone: $t_{598} + D/2 = 33117/80000 < \sqrt 2 - 1$. So `last` = 599 is the
   least value that meets (c), and every node is needed.
   N0 (d) holds: $t_{599} \le 1/2$.
3. **Fold (N2).** A unit square’s angle $\varphi \in [0, \pi/2)$. For
   $\varphi \in [0, \pi/4]$ take the node whose bin holds $u = \tan(\varphi/2)$. Then
   $z = \tan(\delta/2) = |u - t_r|/(1 + u t_r) \le D/2$, since $1 + u t_r \ge 1$. For
   $\varphi > \pi/4$, use the core at angle $\pi/2 - \theta_r$, with $\theta_r$ the node
   for $\pi/2 - \varphi$. Its capture is $F_r(\sigma c)$, $\sigma$ the reflection in the
   diagonal, because $g$ is $\sigma$-invariant and $\sigma$ maps the core at $\theta_r$
   centred at $c$ to the core at $\pi/2 - \theta_r$ centred at $\sigma c$. The domain is
   $\sigma$-invariant. This is per square (F2).
4. **Shrink (N3, N0 (b)).** The core’s extent along the unit square’s axes is
   $B(1 + 2z - z^2)/(1 + z^2) \le B(1 + 2z) \le B(1 + D)$, which is
   $2387749705363/2388000000000 < 1$ (margin $250294637/2388000000000$). So the core
   lies in the open unit square.
   The sharp form at $z = D/2$ is $1146119721592254871/1146240137091100000 < 1$. N0 (e),
   the tangent form, is $1146119721592254871/1146239862908900000 < 1$; it is implied by
   (b) and only refuses.
5. **Per-bin domain (lemma D).** Let $a_r = \max(0, t_r - D/2)$ and
   $\rho(a) = (1 + 2a - a^2)/(2(1 + a^2))$, half the axis-parallel extent of a unit
   square at half-angle tangent $a$. $\rho$ increases on $[0, \sqrt 2 - 1]$. A unit
   square assigned to node $r$ therefore has its centre in
   $[\rho(a_r), L - \rho(a_r)]^2$. Every bin meets $[0, \sqrt 2 - 1]$ (bin 599’s lower
   end, $0.4139625$, lies below $\sqrt 2 - 1$). The domain is nonempty at all 600 nodes.
   As a consistency check of N3, $\rho(a_r)$ exceeds the core’s half-extent
   $B(\cos\theta_r + \sin\theta_r)/2$ at every node; the least margin is
   $5.30 \times 10^{-5}$, at node 1.
6. **Quarter turn (C1).** The rotation by $\pi/2$ about $(L/2, L/2)$ preserves $g$, maps
   $Q_r(c)$ to $Q_r$ at the image centre and maps the domain to itself.
   Every point of the domain has an image in the quadrant $[L/2, U_r]^2$, with
   $U_r = L - \rho(a_r)$.
7. **Counting (N4).** The 94 cores are disjoint closed sets inside $K$. With $g \ge 0$,
   $94 \le \sum_i \int_{Q_i} g \le \int_K g = M < 94$, a contradiction.
   So 94 unit squares do not pack in a square of side $1993/200$, and
   $s(94) \ge 1993/200$.

`dm_premises.py` decides items 1, 2, 4 and 5 in exact rationals
(`outputs/premises.json`: `PREMISES_HOLD`). Where the import lane’s audit computes the
same quantity, its receipt holds the same values.

## What the Dilation Carries and What It Does Not

**What carries.** $L$, $B$ and each of the 853 rows, in order, are exactly $\lambda$
times Hosono’s, and each mass is his.
So for every shared direction the capture is preserved:
$F^{\text{new}}_{3k}(c) = F^{\text{Hosono}}_k(c/\lambda)$, since the core, the
rectangles and their densities scale together.
Old node $k$ (step $83/40000$) is new node $3k$. `dm_sample.py` evaluates both sides
exactly at eight poses, at Hosono’s nodes 1, 50, 92 and 199, and finds them equal.
Hosono’s verified coverage would carry to the 200 shared directions, for centres whose
image lies in his own domain.
The bound does not use that.

**What does not carry.**

- **Hosono’s net.** On his net the dilated core gives
  $B(1 + 83/40000) = 797016825363/796000000000 > 1$, so the finer net is forced.
  Its extra 400 nodes ($r \not\equiv 0 \bmod 3$) carry nothing from Hosono’s run.
- **The domain grows toward the walls.** Unit squares do not scale, so in Hosono’s
  coordinates each shared node’s domain is larger than his:
  - at $r = 0$, by $1/2 - (1/2)/\lambda = 3/3986$ exactly;
  - at the other 199 shared nodes, by between $6.55 \times 10^{-5}$ ($r = 3$) and
    $1.062 \times 10^{-3}$ ($r = 597$). The finer net’s narrower bins raise $\rho(a_r)$
    and offset part of the growth (F5).
- **The route’s ceiling.** As the step goes to zero, the route reaches
  $L_0/B_0 = 99500/9977 \approx 9.97294$, above $1993/200$.

The strip matters at $r = 0$. There the least capture on the whole quadrant,
$1.003117185664$, is at the domain’s end $y = 1893/200$, inside the added strip.
On Hosono’s domain alone the least is $1.003181702094$, at its end $y = 376677/39800$.
So the dilation moves direction 0’s least capture into the region it adds.
The full replay decides it there, and so does this review.

## Does `sqverify-fast` Decide What the Lemma Needs?

Yes, for this certificate.
By the code at the reviewed source:

- **Format.** `sources` reads format M when the first row is an object, refuses a
  nonempty `points` list, and reads each row as `[x1, y1, x2, y2]`.
- **Unread keys.** `derived_from` is not read by the crate or by the theorem, and
  neither is `scaling_factor`, which is absent here.
- **The net.** `declared_net` (`certificate.rs:448`) admits only `step`, `last` and
  `count = last + 1`.
- **N0 (a) to (d).** `admit` (`certificate.rs:554`) checks them in exact rationals on
  that net, together with $0 < B < 1$, $L^2 \ge 2B^2$ and each row’s containment and
  nondegeneracy. It also checks `total_mass`, $0 < M < n$, and that the expansion
  integrates to $M$.
- **N0 (e)** is checked for the per-bin domain (`certificate.rs:685`).
- **Directions.** `direction` (`certificate.rs:536`) takes $t = rD$ from the admitted
  step, with exact cosine and sine.
- **The per-bin domain.** `domain_upper` (`certificate.rs:508`) computes
  $U_r = L - \rho(\max(0, t_r - D/2))$ exactly and refuses $U_r \le L/2$.
- **Search boxes.** Each oblique direction’s root box is $[L/2, U_r]^2$ rounded outward
  (`rotated.rs:771`–772). The axis sweep runs on $[L/2, U_0]$ with $U_0 = L - 1/2$
  (`lib.rs:105`).
- **Threshold.** It is 1 for format M.

The receipts agree. Each summary reports:

- `format` M, `net_origin` `proof_net`, $D = 83/120000$, `angle_count` 600, and
  `net_last_tangent` $49717/120000$;
- `centre_domain` `per-bin`;
- `shrink_bound` $2387749705363/2388000000000$;
- `mass_exact` $9399999/100000$;
- 6,720 expanded rectangles, and no expanded points or segments.

All equal this review’s exact values.
So the crate checks the theorem’s premises (plus refusals the theorem does not need) and
decides coverage on a superset of the quadrant at each node.
By C1 and the fold, that is every centre and orientation the theorem quantifies over.

## All 600 Directions, With No Gap

There is no gap in angle: the bins of the 600 nodes tile half-angle tangents from $-D/2$
to $t_{599} + D/2$, which contains $[0, \sqrt 2 - 1]$.

There is no gap in the receipts.
`dm_receipts.py` reads the author’s rustc 1.98 receipt, his rustc 1.93 receipt and this
repository’s census capture.
Each has:

- indices exactly 0 to 599, once each, every one `verified` at threshold `1`;
- status `VERIFIED`, `refused_directions` empty and `fault_injected_at_box` null;
- 296,805,699 nodes, and least certified bound $1.0000000000314393$ at direction 277.

The three agree at every direction in verdict, least bound, nodes, leaves, least-bound
box, axis argmin and vertex count.
Within each direction the crate’s leaves cover the root box, since each split yields two
closed boxes whose union is the parent; that is the crate’s, held by the reviewed
source.

**What the least certified bound means.** $1.0000000000314$ is where a leaf was accepted
just above the threshold.
It is not the certificate’s slack.

- **Least-bound boxes.** At every oblique direction, `dm_sample.py` evaluates the exact
  capture at the centre and four corners of the census capture’s least-bound box.
  All 2,995 values are at or above the box’s certified bound and above 1. The closest is
  $0.00231$ above, at $r = 537$.
- **Lowest capture found.** A binary64 search at 19 directions, refined by Nelder–Mead
  and confirmed exactly, found its lowest capture, $1.0017633082$, at $r = 277$, pose
  $(8.34506, 5.33187)$. The directions searched were 1, 2, 3, 144, 277, 298, 299, 301,
  597, 598 and 599, and eight new directions drawn with a fixed seed.
- **Near the walls.** In the strips along the walls the least found was $1.0031003$
  ($r = 2$, at $x = U_2$). These are samples; they decide nothing.
- **A lower point the search missed** (added after reading `GRADE.md`). The author’s
  referee reports $1.001123004124$ at $r = 144$, centre $(5.56017, 7.43963)$.
  `dm_compare.py` evaluates it exactly and gets a value inside the referee’s stated
  interval, at a centre in the domain.
  My search at $r = 144$ stopped at $1.0036158$, so its grid and starts were too coarse
  there.

## The Records Against the Declared-Net Checklist

Items 1 to 8 of “For the Records Lane” (b), in the 6 October declared-net soundness
review, against this certificate:

| Item | Holds? | Evidence |
| --- | --- | --- |
| 1. The file | yes | format M, `points` empty, no `scaling_factor` (the crate does not read the key, so absence reads as 1), `proof_net` exactly `step` and `last`, no top-level `net`, no `certificate` metadata; 8 × the densest row’s density is $315799.9 \le 2^{32}$ |
| 2. The case | yes | `census.json` row `mixed_n94_L9965`: $n = 94$, $L = 1993/200$, `VERIFIED`, `returncode` 0, `refused_directions` empty, `directions_verified` 600, indices 0–599 each `verified`, `threshold` 1, `least_bound_leaf_exact.clears_threshold` true; my exact capture at that leaf ($r = 277$) equals the crate’s and the census tool’s |
| 3. The premises | yes | every summary premise equals this review’s exact value; N0 (a)–(e) recomputed apart from the crate by `dm_premises.py` (and by the import lane’s audit) |
| 4. The candidate | yes | `candidate_sha256` `116c8342…16f8` is the retained file’s; its JSON text is `b8b03ee8…749c`, as stated |
| 5. The build | yes | `source_sha256` `d97758bb…`, profile `release`, rustc 1.98.0 |
| 6. The control | **no** | the receipt is `CONTROL_FAILED` (F1). Its 99/100 mutant is refused at all 600 directions, and its near-threshold mutant with an exact witness; `captures_agree` is true. Every refusal holds exactly here |
| 7. The mathematics | yes, with this review | this document |
| 8. The words | to adapt | the producer ran this crate, so the evidence must say *reproduced with the producer’s code*, not item 8’s *independently re-implemented* (F6) |

## What the Two Checkers Share

**The author’s runs and this repository’s replay** are one implementation.
The rustc 1.98 build is the reviewed source `d97758bb…`. The rustc 1.93.1 build had only
its `rust-version` line removed (source digest `85f02254…`, not a reviewed digest), and
its receipt is identical direction by direction.
The census replay reproduces the result with the producer’s code; it cannot find an
error in that code.

**The author’s second checker** (an OpenAI Codex agent’s fixed-point integer branch and
bound, retained and not run here) shares the following with `sqverify-fast`:

- the theorem and lemmas as `SOUNDNESS.md` states them, which its author read: N0 to N4,
  the fold at $\pi/4$, lemma D’s per-bin domain, C1’s quadrant and threshold 1;
- the branch-and-bound design:
  - inside and outside classification against eroded and dilated cores;
  - the concave-section trapezoid lower bound (R2);
  - derivative bounds by edge lengths (R4, R5);
  - the mean-value step (R3) and inheritance (R6);
- the certificate bytes, and the reading of format M ($D_4$ orbits, $m/8$ per image,
  `[x1, y1, x2, y2]`).

It shares no code, language or arithmetic: integers at scale $2^{42}$ with directed
rounding, against binary64 intervals.
It also adds an erosion-area bound, and treats $r = 0$ by branch and bound where the
crate uses the vertex sweep.
Its domain is $U_r = L - \max(\rho(a_r), B(\cos\theta_r + \sin\theta_r)/2)$
(`independent.py:49`). That is the intersection of lemma D’s domain with the set of
centres whose core lies in $K$. Every admissible centre lies in both, since N3 puts the
core inside the unit square, so checking the intersection is sound on any certificate.
Here it is exactly the per-bin domain, because $\rho(a_r)$ exceeds the core’s
half-extent at every node (item 5 above).
It checks the quadrant $[L/2, U_r]^2$, which its README and the source README call each
direction’s “full” or “whole” centre domain (F4). (Corrected after reading `GRADE.md`:
the committed text said this domain equalled the per-bin domain “only because” of item
5, as though the larger margin could be unsound.
It cannot; see the comparison below.)

So an error in `SOUNDNESS.md`’s mathematics, or in the format’s reading, would be common
to both checkers; an error in the crate’s code would not.
The two authors are of different system families, but one worked from the other’s prose.
The source’s statement that the Codex agent did not read the crate’s code is the
source’s; it is not evidence here.

**This review’s programs** share no code with either.
They share the mathematics, from `SOUNDNESS.md`, and the format, whose field order I
took from Hosono’s specification and the crate alike.
I read the crate’s admission and domain code (the producer’s code) before writing them,
so they are not clean-room.
Their author is a Claude agent, the system family of the crate’s authors and of the
author’s lab.

## Independent Checks

| Check | Program | Coverage | Result |
| --- | --- | --- | --- |
| Every premise but coverage, exactly | `dm_premises.py` | full | `PREMISES_HOLD` |
| Direction 0, completely: 5,430 × 5,430 events (the crate’s counts), 29,484,900 vertices, 2,272 active rectangles, one matrix product with a rigorous rounding bound of $3.19 \times 10^{-9}$ | `dm_axis.py` | 1 of 600 directions, full | least $1.003117185664$ at $(6.4945\ldots, 1893/200)$ and its mirror, the crate’s argmin; decided at least 1 with margin $0.0031$; the crate’s certified bound there is $1.13 \times 10^{-9}$ below the exact value |
| Every oblique direction’s least-bound box, centre and corners, exactly | `dm_sample.py` | 2,995 poses (5 at each of 599 directions) | all at or above their certified bounds and 1 |
| Search for low captures, then exact | `dm_sample.py` | 19 directions, sampled | least found $1.0017633082$ ($r = 277$); at the walls $\ge 1.0031$ |
| The dilation identity at shared nodes | `dm_sample.py` | 8 poses | exactly equal |
| All 600 refusals of the control’s 99/100 mutant, exactly | `dm_receipts.py` | 600 witnesses | each equals the recorded capture, lies below 1, lies in the per-bin domain, and the original there is at least 1; the largest witness capture is $0.99999999999989$ ($r = 21$) |
| The evaluators themselves | `dm_selftest.py` | 12 synthetic cases, 50 poses, 2 external values | exact on known areas; two exact methods agree; binary64 within $4.4 \times 10^{-13}$; equal to the crate’s exact capture at the $r = 277$ leaf and to the $n = 31$ receipt (F3) |

The rigorous bound at $r = 0$ rests on three things:

- binary64 rounding of each input, with the error measured exactly ($\le 8.9 \times
  10^{-16}$);
- each overlap within $7.3 \times 10^{-15}$;
- the standard bound on any summation order, with or without fused multiply-adds, which
  the BLAS product is trusted to meet.

## Mutants

`dm_mutants.py` builds each in memory and refuses it with this review’s own code:

| Mutant | Refused by |
| --- | --- |
| The dilated certificate on Hosono’s net (step $83/40000$, `last` 200) | N0 (b): $B(1 + D) = 797016825363/796000000000 \ge 1$; also (e), and a core leaves $K$ at some domain end |
| `last` 598 | N0 (c): $t^2 + 2t - 1 = -6076511/3600000000$; tangents in $(33117/80000, \sqrt 2 - 1]$ are in no bin |
| The container and measure dilated, the core left at $9977/10000$, on Hosono’s net | every premise holds; coverage fails: exact capture $0.67849$ at $(9.465, 9.465)$, $r = 0$, in the domain |
| Every mass × 99/100 | premises hold; exact capture $0.99175$ at $r = 277$, $(8.34506, 5.33187)$, the lowest pose this review’s own search found |
| Every mass × $199647959/200000000$ | premises hold; exact capture $0.9999999994$ at the same pose |

The third shows why the core must be dilated with the measure.
The fifth shows that the uniform mass slack at that pose is at most $0.18\%$; at the
referee’s pose at $r = 144$ it is at most $0.11\%$ (added after reading `GRADE.md`).

## Findings

| Id | Severity | Where | Finding |
| --- | --- | --- | --- |
| F1 | gap (records lane; holds the verified lane, not the claim) | `devtools/sqverify_fast_census.py:653`, `:706`; the control receipt | The control fails closed on a fixed $10^{-9}$ axis tolerance, so checklist item 6 is not met |
| F2 | note | `packing/sqverify_fast/SOUNDNESS.md:43`–47 | N2 reads “reflect the whole configuration”; the fold must be per square |
| F3 | note | `source/notes/n31-negative/d529.jsonl`; `source/README.md:61`–65 | The $n = 31$ receipt is a run on an input not retained, and the README’s capture is in no retained receipt |
| F4 | note | `source/README.md:86`; `source/second-checker/README.md:5`–6 | The second checker checks the quadrant, which the READMEs call each direction’s full centre domain (narrowed after reading `GRADE.md`) |
| F5 | note | `source/tools/rescale.py:4` | The docstring’s domain growth $\rho(1 - 1/\lambda)$ holds on the same net, not on the finer one |
| F6 | note (records lane) | checklist item 8; the evidence text | The replay is reproduced with the producer’s code; item 8’s words do not apply as written |

For the author, no finding is blocking or major.
F3 to F5 are minor; F1, F2 and F6 are this repository’s.

**F1. The control receipt fails closed on the census tool’s axis tolerance.** Item 6
asks for a `CONTROLS_REFUSED` receipt.
This one is `CONTROL_FAILED` for one reason only.
At $r = 0$ the vertex sweep’s certified bound for the 99/100 mutant at its least vertex
is $0.9930860126843$. The exact capture there is $0.9930860138075$, which is
$1.123 \times 10^{-9}$ above the bound.
That is beyond `AXIS_ROUNDING` $= 10^{-9}$. The refusal is sound: the bound lies below
the capture, and the capture lies below 1. The original shows the same thing at its own
least vertex: its certified bound $1.0031171845297$ sits $1.134 \times 10^{-9}$ below
the exact $1.003117185664143$. So the constant is too tight for this sweep, with 5,430
events and 2,272 active rectangles, and the receipt does not show a wrong vertex.
This is the 14 October review’s F-1, which `think-4uun` owns.
Every one of the 600 refusals, and the near-threshold witness, holds exactly by this
review’s evaluator.

The fix is `think-4uun`’s: tie the tolerance to the sweep’s accumulated interval width,
or record the sweep’s own enclosure of the least vertex.
A change to control logic needs a reviewer’s reading, as the 6 October review says.
Until a receipt passes, item 6 is open and n-094’s verified lane should stay at T-091’s
$199/20$.

**F2. The fold is per square.** `SOUNDNESS.md` lines 43–47 justify $\varphi \le \pi/4$
by reflecting the whole configuration in the diagonal.
One reflection cannot fold a packing whose squares lie on both sides of $\pi/4$. The
proof needs, and N4 allows, a core per square: for $\varphi > \pi/4$ the core at angle
$\pi/2 - \theta_r$, whose capture is $F_r(\sigma c)$ by $g$’s invariance under the
diagonal reflection $\sigma$ (step 3 above).
The 5 October route review uses the same wording under the heading “per square”, so the
intent is plain. A one-line rewording would make it exact.
No verdict depends on it.

**F3. The $n = 31$ note’s receipt is for an input the packet does not keep.** The
summary of `d529.jsonl` names `input_sha256` `e61e0e6b…` and mass
$31 - 7.00003 \times 10^{-7}$. The retained `n31_L5978.json.gz` is `d46ce612…`, with
mass $31 - 10^{-5}$. My exact capture of the retained file at the receipt’s witness
pose, times $10000003/10000000$, equals the receipt’s exact capture.
So that input is the retained file with every mass scaled by that ratio, the “mass slack
spent” variant the README mentions.
At the same pose the retained file itself captures $0.99999969508 < 1$. The pose is in
the per-bin domain, $3.5 \times 10^{-9}$ from its end at the wall.
The README’s figure $0.99999999719$ appears in no retained receipt.
The note claims no bound, and its conclusion stands; the packet would be clearer if it
kept the scaled input or the retained file’s own receipt.

**F4. “Full centre domain” is the quadrant.** The source README (line 86) and the second
checker’s README (lines 5–6) say the second checker verified each direction “over their
full centre domains”.
Its front end checks $[L/2, U_r]^2$, the quadrant, which covers the whole domain only
through C1 and the measure’s symmetry, as `INTEGER-SOUNDNESS.md` says.
The README’s wording is worth a sentence.

*Corrected after reading `GRADE.md`.* The committed F4 also said that the second
checker’s $U_r$, which takes the larger of $\rho(a_r)$ and the core’s half-extent,
“would shrink the checked set below what lemma D requires” if the larger were the
core’s. That was wrong.
Every admissible centre also has its core inside $K$, since N3 puts the core inside the
unit square, so the intersection of the two domains contains every centre the theorem
needs. The larger margin is sound on any certificate.
Here the two coincide anyway, since $\rho(a_r)$ is larger at every node (least margin
$5.30 \times 10^{-5}$, node 1).

**F5. The growth formula in `rescale.py` assumes the same net.** Its docstring says the
centre domain grows by $\rho(1 - 1/\lambda)$. That holds at $r = 0$ ($3/3986$) and on an
unchanged net. On the finer net the narrower bins raise $\rho(a_r)$. The growth at the
shared nodes then runs from $6.55 \times 10^{-5}$ to $1.062 \times 10^{-3}$ in Hosono’s
coordinates, and the new nodes have no old domain.
The README’s account (“the dilation is only how the candidate was found”) is right; only
the docstring’s formula is narrower than its use.

**F6. The words for the replay.** Checklist item 8 asks the evidence text to say
*independently re-implemented*. It was written for Hosono’s certificates, whose producer
did not run this crate.
Here the producer did, so the census row is *reproduced with the producer’s code*. The
pull request’s `SAME_CRATE_PACKETS` branch (`sqverify_fast_census.py:1403`) writes
`same-implementation` and says so.
Item 8 should be read that way for this row.
The evidence should also name the declared net’s step and count and the accepted build,
as item 8 asks. This review’s direction-0 decision and samples are, beside it,
independently re-implemented after reading the producer’s code: one direction in full
and the rest sampled.
They are not a second complete implementation.

## Questions for the Author

1. Is `notes/n31-negative/d529.jsonl` the run on the retained $n = 31$ file with every
   mass times $10000003/10000000$? Where does $0.99999999719$ come from?
   Would you keep that run’s input, or the retained file’s own refusal, in the
   repository?
2. (Withdrawn after reading `GRADE.md`: the committed question asked whether the $\max$
   in `independent.py:49` was deliberate.
   It is sound on any certificate; see F4.)
3. The dilation preserves every capture at the shared directions.
   The least captures known are interior: $1.0011230$ at $r = 144$, which your referee
   found and this review reproduces exactly, and $1.0018$ at $r = 277$. Those this
   review found near the walls are higher ($\ge 1.0031$). Did the lab try a side between
   $9.965$ and the route’s ceiling $9.9729$ on a finer net?

## What I Ran

All with CPython 3.14.7 (`packing/.venv/bin/python3 -I`) under `nice -n 10`, at most two
processes at a time, on a shared four-core host whose load was between 4 and 9 from
other lanes. The receipts are in the packet’s
`review/dilated-measure-2026-11-03/outputs/`, each with the SHA-256 of the program and
of `dmlib.py` that wrote it, equal to the committed bytes.

| Command | Receipt | CPU |
| --- | --- | --- |
| `dm_selftest.py CERT CONTROL N31 D529 OUT` | `selftest.json`: `PASSED` | 1.2 s |
| `dm_premises.py CERT HOSONO OUT` | `premises.json`: `PREMISES_HOLD` | 1.2 s |
| `dm_axis.py CERT OUT CAPTURE` (two BLAS threads) | `axis-r0.json`: `decided_at_least_1` true | 6.5 s |
| `dm_sample.py CERT HOSONO CAPTURE OUTDIR` | `sample.json` (`CONSISTENT`) and `leaf-poses.jsonl` | 100.2 s |
| `dm_receipts.py CERT R198 R193 CAPTURE CENSUS CONTROL PREMISES OUT` | `receipts.json`: `RECORDS_HOLD`, control `CONTROL_FAILED` | 11.0 s |
| `dm_mutants.py CERT HOSONO SAMPLE OUT` | `mutants.json`: `EVERY_MUTANT_REFUSED` | 13.2 s |
| `dm_compare.py CERT HOSONO GRADE_JSON OUT`, written and run after the findings were committed | `compare-grade.json`: `REFEREE_VALUES_HOLD` | 4.5 s |

The final runs took 138 CPU-seconds.
With the development runs that their receipts replace, the review used about seven
CPU-minutes in all.

What went wrong along the way, and was redone:

- My first $n = 31$ check compared the retained file’s capture with the receipt’s and
  failed. Reading the receipt’s summary showed the input differed, which is F3.
- A first search clipped poses to a rounded domain end, leaving one pose ($r = 44$) an
  ulp outside the exact domain.
  The search now clips to the largest double inside it, and the receipt records per-bin
  membership.
- The dilation’s node correspondence was first counted among the theorem’s premises,
  which would have refused the core-not-dilated mutant for the wrong reason.
  It is now reported apart.
- A compact JSON writer first wrote integer keys unquoted; it was fixed.
  Every final receipt was then rewritten, so that each records the bytes that ran.

## Significance

**S3, confirmed.** If correct, the claim is the strongest lower bound on record at
$n = 94$, $3/200$ above T-091. It uses T-091’s own measure and certificate kind, with a
declared net (#366) and the dilation move, so it brings no new technique.
That matches “a substantive case result” (S3) and T-091’s own S3. It is not S4: no
reusable technique or bound family is new here, and the dilation can fail, as at
$n = 31$.

## Verdict

**Accepted.** The certificate proves $s(94) \ge 1993/200$ by the measure-capture theorem
on its declared net.
Every premise holds exactly.
The net covers every orientation with no gap, and `sqverify-fast` decides exactly the
coverage the theorem needs, at all 600 directions, in three identical runs.

This review decided direction 0 independently and in full.
At every other direction its exact samples meet the certified bounds.
Every mutant is refused for the reason it names.

No defect is open. F1 is a gap in the records: until a control receipt passes, checklist
item 6 is not met, and the verified lane should wait for it.
F2 to F6 are notes.

## Comparison With the Author’s Referee Report

Everything above this section, except the passages marked as added or corrected after
reading it, was committed and pushed as `5ad487b72` before I opened
`second-checker/GRADE.md` and `GRADE.json`. Beforehand I knew only what the bead’s brief
said: that the report’s lowest sampled capture is at direction 144. After reading them I
wrote one program, `dm_compare.py`, which holds the report’s values to this review’s
evaluator.

**What the report is.** It is the referee report the author commissioned, finalized
2026-11-02 and written by an OpenAI Codex agent, with verdict SOUND. Its “supplied
checker” is the author’s lab’s own floating-point checker.
The source README already declines to offer that checker as evidence, and the report
shows it accepting a false certificate.
That is not `sqverify-fast`. The report’s `prep.premises()`, `runall.sh` and long-double
fallback, and its “SOUNDNESS §4”, belong to the lab checker, not to
`packing/sqverify_fast/SOUNDNESS.md`. So the report does not review this repository’s
checker. Its verdict rests on the second checker’s full run, which this repository has
not replayed. It is evidence of the source’s own (a review with `relation: source`, in
the terms of [epistemics.md](../../../epistemics.md#review-records)), and this review
reads it as data.

**Where we agree, reached apart.**

| Point | The report | This review |
| --- | --- | --- |
| Exact premises | the same values for $B(1 + D)$, the tangent form, the reach polynomial and the mass | the same, by `dm_premises.py` |
| Expanded terms | 6,824, counting coincident images separately | 6,720 distinct images after merging, the crate’s count; the same measure |
| The fold | “One global reflection cannot fold differently oriented squares simultaneously”; a minor prose repair, said of the lab’s text | F2, of `SOUNDNESS.md`’s identical wording |
| The dilation | $3/3986$ at $r = 0$; every shared angle’s domain strictly larger; 400 new angles; nothing carries | the same, with the growth at every shared node and the exact capture identity |
| The ceiling | $99500/9977$, correcting an earlier draft’s $9.9725$ | $99500/9977$ |
| Mass mutant | ×0.998 refused at $r = 144$, capture $0.99912075811569$ | reproduced exactly at its pose |
| Heaviest orbit removed | refused at $r = 0$, capture $0.73804$ | refused at $r = 0$ by $0.24998$, at $(9.45001, 9.4635)$ |
| $L = 9.975$, $B$ held | refused at $r = 144$, capture $0.99811$ | refused at $r = 144$ by $0.99766$, at the wall |

**Where it corrects this review.** Two points, both marked in place above:

- F4’s second half and Question 2. Taking the larger of the two margins cannot drop a
  needed centre.
- The lowest known capture.
  Its $1.001123004124$ at $r = 144$ is below this review’s $1.0017633$, and
  `dm_compare.py` reproduces it exactly.
  The certificate’s uniform mass slack is therefore at most $0.11\%$, not $0.18\%$.

**What only the report has.** A second complete implementation’s run: 600 of 600
directions verified, 166,440,592 nodes, least certified bound $4398046511113/2^{42}$. It
also documents the lab checker’s false acceptance.
Its own weakest point, as it says, is the manual audit of the integer code’s derivative
enclosures, inheritance and overflow bounds.

**What only this review has.**

- Direction 0 decided independently in full, with its least capture in the strip the
  dilation adds.
- The records against the declared-net checklist: F1’s control tolerance and F6’s words.
- All 600 control witnesses held exactly.
- The $n = 31$ receipt’s input (F3) and `rescale.py`’s growth formula (F5).

Nothing in the report changes the verdict.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
