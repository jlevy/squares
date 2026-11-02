# Ryu’s Quarter-Power and Cube-Root Deficiency Preprints: Strongest-Tier Stage 4 Review

**Date:** 2026-11-02. **Subject:** the two preprints of
[#414](https://github.com/jlevy/squares/issues/414) by Sungjoon Ryu, both version 1.0,
and the lemmas they import:

- *Packing k²−c unit squares: a lower bound of order k^{1/4} for the deficiency* (here
  Q), squarepacker/k2-minus-c-quarter at `abbedcf4`, `paper/paper.tex`, 5,471 lines;
- *… a lower bound of order k^{1/3} for the deficiency* (here C),
  squarepacker/k2-minus-c-cube-root at `15045f9c`, `paper/paper.tex`, 584 lines;
- the lemmas of Ryu’s k2-minus-c version 1.2 (here [R], `e16a5cf`) that they import.

All three are retained:
[quarter](../../../packing/resources/web/squarepacker-k2-minus-c-quarter-2026-10-07/README.md),
[cube-root](../../../packing/resources/web/squarepacker-k2-minus-c-cube-root-2026-10-07/README.md)
and
[v1.2](../../../packing/resources/web/squarepacker-k2-minus-c-v12-2026-10-06/README.md).
Bead think-yf8j, lane L23 of the intake pass think-3guf. **Read at:** `main`
`bdf52188a`. **Reviewer:** Claude (Anthropic), strong sub-agent tier (`tbd-strong-max`)
at maximum reasoning, the stage 4 mathematical lane, separately prompted.
It shared no context with the source’s AI sessions or with the lane of the 8 October
review. It read the three TeX sources as data and ran only programs it wrote.
It is not a human oversight record.

**Verdict: accepted, for both preprints.** Both chains are complete for the theorems as
the asymptotic register records them, under the stated conventions.
The proofs are conditional on the imported lemmas of [R]. For Theorem A of Q and Theorem
1.1 of C they also need [R]’s computer-assisted Lemma 4.10, whose per-box labelling is a
separate obligation owned by think-k3tk (F3). No finding is a defect or a gap; there are
eight notes, the last found while comparing with the 8 October review.

- Every step of both chains was re-derived (The Quarter-Power Chain, The Cube-Root
  Chain). So was every lemma of [R] they use, except two parts.
  Proposition 4.5’s case analysis was read and its numbers recomputed.
  Lemma 4.10’s box labels were not decided.
- Every constant and threshold the theorems use reproduces on exact-rational intervals,
  in the direction the proofs need and in every displayed rounding: 193 checks for Q, 95
  for C and 48 for the numbers of [R]’s proofs.
- Q’s supplementary tables had never been executed.
  They reproduce in full: Table 4, Table 5 and every claim of the sensitivity record of
  its Section 12.6, 118 checks.
- Q quotes [R] faithfully: 19 of 19 quoted statements and 12 of 12 quoted sentences.
- C’s 44 citations of Q name the results they mean.

## Summary for the Author

Both arguments hold up.
I re-derived them from the definitions and found nothing wrong.
The constants hold in interval arithmetic of my own, exact rationals with outward
rounding, which shares nothing with your scripts.

- **The quarter-power threshold is fragile, as you say.** At k0 = 4.62·10^12, Ψ̄(k0) =
  146.6242933… against 0.1 k0^{1/4} = 146.6089535…. The bracket B̄ = 38.5067952… may
  grow by a relative 1.0463·10^-4 before condition (i) fails.
  Condition (i) holds exactly from k* = 4,616,673,963,026.36…. Every tolerance in your
  Section 12.6 reproduces to the digit.
- **Your Tables 4 and 5 hold as printed**, every parameter set at its k.
- **The cube-root cases hold as printed.** The tightest margin is case 6’s (iv): γ
  k_b^{1/2} = 34934.2239… against W1 = 34934.6640….
- **Your two liminf constants come from limits, and they can be made explicit.** With τ0
  = 1/6, τ1 = 1/6 − 10^-6 and ν0 = 10^-5, conditions (i)–(iii) of your Proposition 5.1
  hold at k_a = 10^24 for γ = 0.06285, and at k_a = 10^22 for γ = 0.05229 with the
  analytic constants.

Two points about the record of [R] would make Q easier to audit.

- **Proposition 2.1 and Theorem A13 rest on facts about [R]’s proofs, not its
  statements.** Proposition 2.1 bounds families of pairs that need not be edges of a
  visibility graph. Theorem A13 relies on [R, Lemma 4.10] entering [R]’s Lemmas 4.13–4.15
  in only two sentences.
  I checked every such fact against [R]’s text, and they hold (F1). Stating the
  all-pairs bound as a lemma of [R], with proof, would let a reviewer of [R] cover Q’s
  use of it.
- **The k^{1/3} and k^{1/4} constants are sound on [R]’s Lemma 4.9 alone.** Its finite
  angle check reproduces: every class sequence with sum at least 15 fails by more than
  25.94°, and (5,2,5,2) is the only feasible one with sum 14, at 358.92° (F3).

Questions are at the end.

## Scope

**Read.**

- Q in full: Sections 1–12, the tables and the verification status.
  The source README and `reviews/REVIEWS.md`, as data.
- C in full, with its README and review summary, as data.
- [R] v1.2: Sections 2–4 in full (lines 164–985), and Remarks 7.3–7.5 (lines 1284–1355).
- The asymptotic register’s entries for the two preprints and for [R] v1.1 and v1.2
  (`packing/frontier/asymptotic-waste-bounds.yaml`), and #414’s entry in
  `packing/campaign/result-requests.yaml`.
- Stage 4 of `packing/campaign/result-import.md` and `epistemics.md`, Every Run’s Code
  Is Kept and Review Records.
- For format only, `review-2026-11-01-filled-end-lemma.md` and
  `review-2026-10-31-couzo-843-130.md`.

**Run.** Eight programs of my own (What I Ran).
Seven read only the three TeX files; the eighth reads the maintained checker as data.
None of the source’s programs was read or run: `k14_constants_check.py`, the cube-root
packet’s three `check_table_*.py` and the v1.2 programs.

**Not reviewed.**

- The per-box labels of [R, Lemma 4.10] (think-k3tk).
- The coverage of its boxes, which the v1.2 replay decided.
- The numerical analogue tests of both sources, and the AI reviews they report.
- Whether the k^{3/8} upper bounds of #471 and #486, which the C entry’s corollary
  cites, are right.

## The Claims and Their Conventions

The register records, and the primaries state, the following.
Here M(k) is the largest number of closed unit squares in [0,k]² that are pairwise
disjoint *as closed sets*, and W_min(k) = k² − M(k).

| Source | Statement as registered | Primary | Holds |
| --- | --- | --- | --- |
| Q, Theorem A | k² − M(k) ≥ 0.1 k^{1/4} for integer k ≥ 4.62·10^12; liminf (k² − M(k))/k^{1/4} ≥ 0.1696 | L124–135; c_∞ = 0.1696524112… | yes |
| Q, Theorem A₁₃ | 0.1 k^{1/4} from k ≥ 2.17·10^13; liminf ≥ 0.1411, without [R, Lemma 4.10] | L147–156; c_∞^(13) = 0.1411593387… | yes |
| Q, Corollary A | s(k² − c) = k for integers c ≥ 0 and k ≥ max(4.62·10^12, 10^4 c^4 + 1); 2.17·10^13 without Lemma 4.10 | L161–166, L5070–5096 | yes |
| C, Theorem 1.1 | > 10^-4 √k on [10^8, 2.5·10^15]; > 7·10^-5 √k on [2.5·10^15, 3.5·10^17]; > 0.06 k^{1/3} from 3.5·10^17; 0.0625 from 10^21; liminf ≥ 0.06285 | L81–89 | yes |
| C, Theorem 1.2 | 8.5·10^-5 √k on [10^8, 2.4·10^15]; 6·10^-5 √k on [2.4·10^15, 3.39·10^17]; 0.05 k^{1/3} from 3.39·10^17; 0.052 from 10^21; liminf ≥ 0.05229 | L91–95 | yes |
| C, Corollary 1.3 | s(k² − c) = k for integers c between 0 and each bound in its range | L97–106 | yes |

**The conventions.**

- **Closed sets.** The register’s side conditions say “unit squares pairwise disjoint as
  closed sets in [0,k]²”, as both texts do (Q L110–114, C L66–69).

- **The strict-packing equivalence.** Here s(n) is the side of the least square holding
  n unit squares with disjoint interiors.
  [R, Lemma 2.1] gives s(n) < k exactly when n ≤ M(k). I re-derived both directions from
  [R]’s proof (lines 175–186).
  - Dilating the centres of a packing in a square of side s < k by k/s turns every
    separating line into a strict one and keeps every square in [0,k]².
  - Contracting a closed packing about the centre of [0,k]² by a factor close to 1 keeps
    the positive gaps and gives a square of side μk + (1 − μ)√2 < k.

  So s(k² − c) = k exactly when c < W_min(k), as both abstracts say, since s(n) ≤ k for
  n ≤ k².

- **The quantity of the register.** The register’s quantity is W(x), which is 0 at an
  integer side. For x < k, every packing of x has at most M(k) squares, and exactly M(k)
  fit once x ≥ s(M(k)). So k² − M(k) is the limit of W(x) as x → k from below.
  The v1.1 row says so in its side condition; the Q and C rows say it only through their
  kernel field, “at integer sides approached from below” (F5).

## The Quarter-Power Chain (Q), Step by Step

Each row was re-derived from Q’s definitions and the lemmas it cites, with every
inequality’s direction checked.
Numbers are those of the TeX, which match the PDF’s numbering.
I recomputed the numbering (`c_citations.py`), and C cites it correctly.

| Step | Where | What it shows | Verdict |
| --- | --- | --- | --- |
| Rules and flows | Definitions 3.9–3.14, Lemmas 3.12, 3.15, 3.17, 3.18 | A path enters squares only through the relative interior of their bottom sides; centre heights of successive entries increase by at least ½(cos a(X) − sin a(X)) + ½(cos a(Y) − sin a(Y)) > 0, so the recursion of R1 over squares sorted by centre height is well founded, and each entry point has one winner; on finitely many pieces every event point is affine in x with slope ≥ 1 | true |
| Scale flows and T* | Definitions 3.20–3.22, Lemma 3.23 | Truncations of the one master flow; T_s = {T* ≤ s} exactly, which needs R1 decided once and “M before T” (Remark 3.34) | true |
| Height identity | Theorem 4.2, Corollary 4.4 | q_y − m = −Σ(1 − cos φ_i) + Σ g_i cos φ_i, the first sum at most (sec α − 1) q_y because Σ cos φ_i ≤ q_y | true |
| Quantization | Lemma 4.8, Theorem 4.11, Lemma 4.12, Theorem 4.13 | Any F_s path touching Bot(Z) puts both ramps of Z within w(s, Z; q) < w0 − 10^-12 of an integer; a square of Z(s) has a ramp height in H at distance ≥ w0; so no F_s path meets Bot(Z), and μ_Z ≡ 0 | true |
| End collisions | Lemmas 5.5, 5.9, Proposition 5.10 | Per source–target pair, | E_{X,Y} |
| Shadow inequality | Theorem 6.9, Proposition 6.10 | The two bookkeeping identities; μ_Z ≤ c_Z by R1’s unique winner and slope ≥ 1; outside the finite set Exc, Sh = L_T + Λ − U; the wall loss of F_s is at most 2y tan α(s) | true |
| Deaths, merges, overlap | Lemmas 7.4–7.11, Theorem 7.1, Corollary 7.2 | Two sources need δ ≤ ½ cos 2α_max (C6); at most two paths through a point; a double point lies in a δ × w_e rectangle above the upper left vertex; δ | D |
| Tilt terminations | Lemmas 8.5–8.12, Theorem 8.3, Corollary 8.13 | Exit coordinates are injective with slope ≥ 1; the hull slit is waste (a square meeting it would project onto n_X in an interval shorter than δ); the vertical slits are disjoint components of the vertical waste; s_e ≥ θ_e | J′_e |
| Per-scale count | Theorems 9.1, 9.2, Lemma 9.9 | Z(s) ⊂ ℝ × V_s and receives no F_s entry; integrating Σ c_Z ≤ N(s) + Λ*(s) over V_s gives | Z(s) |
| Integration | Theorem 10.3, Steps 1–12 | Kinds (i)–(iii) of lines; [R, Lemma 4.13] for kind (ii) and [R, Lemma 4.15] pointwise for kind (iii); two uses of Tonelli; the window integral ∫_y^{y/(1−ε)} s^{-7/4} ds gives invF; the bracket B and Ψ_π(k) of (10.3) | true |
| Assembly | Lemma 11.1, Propositions 11.2, 11.5, 11.6 | Raising A, A′, C_Λ only lowers Ψ; φ′(k) > y1^{-1}(y1^{1/4} D1 − K_W/(2B)); the family π_n = (c0^opt, c1^opt, n, n^{-1/2}, n^{-1/4}) sends Ψ_∞(π_n) to c_∞, a supremum not attained; Corollary A by [R, Lemma 2.1] | true |

Three places deserve a word, since a reader might doubt them.

1. **The hull slit (Lemma 8.6).** Suppose a square Z meets the open slit 𝒪_e over the
   hull of the exit coordinates.
   - Separating Z from X and from Y puts every point of Z, at every hull coordinate,
     strictly between the top of X and the bottom of Y (Claim 1). This uses the closed
     hull at its ends.
   - Z misses each line ℓ_p with p ∈ I_e, because the gap segments there are waste
     (Claim 2). So Z’s projection onto u_X lies strictly inside the hull.
   - Then Z’s projection onto n_X lies in [0, δ). Every projection of a unit square has
     length at least 1, a contradiction.
2. **One R1 for all scales (Remark 3.25).** The equality T_s = {T* ≤ s} holds because a
   T termination in F_s is at an R1-passed entry of the master flow, and only R1-passed
   entries define T*. Step 7 of Section 10 needs only the inclusion.
   With “T before M” the inclusion could fail, and the paper says so (Remark 6.20).
3. **The window constant invF.** For y in Y_b, the scales with y ∈ 𝒲_s are exactly
   [y, y/(1 − ε)]. So ∫ (c0/2) s^{-3/2} G_b(s)/(εs + b_W) ds ≥ (c0 invF/(2c1)) ∫_{Y_b} f
   dℓ. The bound uses εs + b_W ≤ εs(1 + b_W/(εy0)) for s ≥ y0.

## The Cube-Root Chain (C), Step by Step

C uses only Q’s master flow, with π_θ = (θ, θ/2, 1, ½, ¼) and a threshold θ chosen from
W.

| Step | Where | What it shows | Verdict |
| --- | --- | --- | --- |
| Parameters | Lemma 2.1 | π_θ meets (C0)–(C7), (Q1), (Q2) for 0 < θ ≤ β̄ and k ≥ 14: (C3) is 2^{-1/4}θ < θ; w0 < 1.13·10^-5; (C7) is 2 ≤ (k/2 − 3)/2 | true |
| Choosing θ from W | Section 2.2 | Every result of Q used holds for each closed packing and each admissible π; θ(W) is a number fixed by the packing, the same for ρ𝒫, so the joint floor and ceiling statements apply | sound |
| Tilt budget | Lemma 2.3 | On the disjoint height ranges I_j the line meets Z_j; [R, Lemma 4.13] with β̄ := θ on {ω < ½}, and | {ω ≥ ½} |
| One path | Lemma 2.4 | The pass segments’ height ranges are disjoint (heights increase strictly) and have length cos φ_j; Σ a(Z_j) ≤ B1 W with B1 = (Ā/2 + 2β̄)/cos β̄ | true |
| Lateral drift | Lemma 2.5 | A pass moves a path sideways by | sin φ_j |
| Quantization | Definition 2.6, Lemma 2.7 | D ≤ Σ φ_j²/2 ≤ (θ/2) B1 W ≤ τ1 for θ = min(β̄, 2τ1/(B1W)); at an entry candidate dist(q_y, ℤ) ≤ max(D, δ) ≤ τ1 | true |
| Unreachable squares | Lemma 3.1 | A ramp height y with dist(y, ℤ) ≥ τ0 puts every point of Bot(S) at distance > τ0 − 1.0001β > τ1 from ℤ, using | z_y − y |
| Short chords, budget, terminations | Lemmas 3.2–3.4 | [R, Lemmas 3.5, 4.15] give β | 𝒵_K |
| Main inequality | Theorem 4.1 |  | ℋ |
| Reduction | Proposition 5.1 | β(k) and E fall with k, R⁺(k)/k does not rise (for p = ½ because (iv) keeps W ≤ W1, so 1/θ = 1/β̄), (1 − 2τ0)(k − 6)/k rises; the right side of (4.1) does not fall in W | true |
| Liminf | Section 5 | With b optimal, R⁺(k)/k → γ^{3/2}(ĀĀ′B1/(2τ1(1 − ν0)))^{1/2}; max τ(1 − 2τ)² = 2/27 at τ = 1/6 gives c̄_∞ = ((4/27)/(ĀĀ′B1))^{1/3} | true |

Two checks of the inheritance.

- **[R, Lemma 4.13] for an arbitrary set of lines.** Its proof (R L885–925) works line
  by line, then over the pairs consecutive on a set of lines of positive measure.
  Those are edges of G_h whatever the set is.
  Its constant depends on β̄ only through the cap θ_max = 2β̄ ≤ 3·10^-6. So the lemma
  applies to the union of one path’s crossing ranges, as C says (L258–261).
- **Q’s results for the master flow F_θ.** Q’s Proposition 5.10 and Theorem 7.1 assume 0
  < δ ≤ 10^-5, α_max ≤ 1.5·10^-6 and h_max = k/2 − 1. Theorem 8.3 assumes (C0) and (C1).
  Theorem 6.9 uses only (6.1) (Remark 6.13). All hold for π_θ.

## The Imported Lemmas of [R]

| [R] | Used for | Read | Numbers |
| --- | --- | --- | --- |
| Lemma 2.1, Corollary 3.3 | the equivalence; W ≥ 1 | re-derived | — |
| Lemmas 3.1, 3.2, 3.4, 3.5 | ramp sets; short chords against the excess E(y) | re-derived | — |
| Lemmas 4.1–4.4, Proposition 4.3 | the waste in a Roth–Vaughan rectangle | re-derived | — |
| Proposition 4.5 (Q* = 0.32) | nearly parallel pairs at distance < 10^-5 | case analysis read in full | D(0.344) < 0.19; χ* < 0.29295, an actual 0.29293; the three lower bounds exceed 0.3237, the least 0.32378; 0.3235 − 4ε0 > 0.32 |
| Lemma 4.8(a) | θ(2 − θ)/40 for pairs at distance < 10^-4 | re-derived (area of R + B(1)) | (12/π)Λ + 4 < 10; (12/π)(d + √2/2) + 2 < 5 |
| Lemma 4.9 (K_w = 13) | Theorem A13, C’s Theorem 1.2, Proposition 2.1 | re-derived, finite check redone | γ0 > 41.406°; ρ1 < 0.86611; R3, R4, R5 < 0.75598, 0.56571, 0.50396; γ(2,2) > 70.52°; of the 1,344 sequences of length 3–5, every one with sum ≥ 14 decided; sum ≥ 15 fails by > 25.94°; sum 14 feasible only for (5,2,5,2), at 358.92°; part (c): γ(5,5) > 165.6°, ψ < 7.19° |
| Lemma 4.10 (K*_w = 9) | Theorem A, c_∞, C’s Theorem 1.1, Proposition 2.1 | the reduction to U(I) read; box labels not decided (think-k3tk) | ρ1 < 0.8662, n ≤ 5 |
| Lemmas 4.13, 4.14, 4.15 | kinds (ii) and (iii); C’s tilt budget and short chords | re-derived | A < 10.6067; A13 < 12.7476 |

Q’s Proposition 2.1 and its Remarks 2.2 and 2.4 rely on six facts about [R]’s proofs.
Each is in [R]’s text (F1):

- (a) Lemma 4.9’s proof uses only distances, angles, that p is waste, and that the sides
  are two opposite ones (R L677–738, L740–743);
- (b) Lemma 4.10’s proof counts relevant pairs through U(I), defined without the graph
  (R L751–764);
- (c) all side rectangles containing a waste point stand on one side (R L769–772);
- (d) Lemma 4.10 enters Lemma 4.13’s proof only at R L919–921, for edges of G_h (L894);
- (e) Lemma 4.10 enters Lemma 4.14’s proof only at R L951, for edges of G_v (L944), and
  Lemma 4.15’s only through Lemma 4.14 (L980–983);
- (f) Lemma 4.13’s last step needs only A ≥ 2 (L924–925).

[R]’s Remark 7.5 states A < 12.7476 with K_w = 13 (R L1349–1350), as Q quotes it.

## Constants and Thresholds

`q_constants.py` holds 193 values of Q, every one proved in the direction its proof
needs. The 57 that are displayed as rounded bounds are all tight in their stated
direction.

| Quantity | Theorem A (K = 9) | Theorem A13 (K = 13) |
| --- | --- | --- |
| A, A′ | 10.6066176277…, 10.6066176377… | 12.7475679053…, 12.7475679153… |
| B̄ (bars 10.6067, 10.6068, 1.0000002; resp. 12.7476 twice) | 38.5067952… ≤ 38.506796 | 42.3094563… ≤ 42.309457 |
| Ψ̄(k0) against 0.1 k0^{1/4} | 146.6242933… ≥ 146.6089535… (margin 0.01534) | 215.8353043… ≥ 215.8315519… (margin 0.00375) |
| D1; y1(k0)^{1/4}D1 against K_W/(2B̄) | 0.0086430; ≥ 10.655 against ≤ 0.0044029 | 0.0055791; ≥ 10.125 against ≤ 0.0052311 |
| c_∞ (exact A, A′); with the bars | 0.1696524112…; 0.1696502940… | 0.1411593387…; 0.1411589833… |
| Ψ_∞(π*) with B̄ | 0.1581428… | 0.1375313… |

Among the other checks:

- c_E: 41.93109… and 41.93124… are both ≤ 41.933.
- S_9 ≤ 56.2501 and S_13 ≤ 81.2502; 4/cos(π/4 + 1.5·10^-6) = 5.65686273….
- The disc bound: 4π · 0.70721² < 6.29.
- χ > 0.99999849, and the error term < 8.5·10^-10 (1.22·10^-9 for K = 13).
- The auxiliary inequality: h(2.000133·10^-4) < 0 < h(2.000134·10^-4).
- Every constraint of π* and π*13, (C0)–(C7), (Q1) and (Q2), in exact rationals where
  rational.
- The integer facts of Corollary A: 10^4 · 146^4 + 1 = 4,543,718,560,001, and the
  analogues for 147, 215 and 216.

`c_constants.py` holds 95 values of C, all proved, with 24 of 24 displays tight.

| Case | Range | (1 − 2τ0)(k_a − 6)/k_a | R⁺(k_a)/k_a | (iv): γ k_b^{1/2} ≤ W1 |
| --- | --- | --- | --- | --- |
| 1 | 10^-4 √k on [10^8, 2.5·10^15] | 0.9589999424… | 0.8726600855… | 5000 ≤ 5028.27 |
| 2 | 7·10^-5 √k on [2.5·10^15, 3.5·10^17] | 0.66499999… | 0.6108550034… | 41412.56 ≤ 41986.02 |
| 3 | 0.06 k^{1/3} from 3.5·10^17 | 0.665 | 0.6287165092… | — |
| 4 | 0.0625 k^{1/3} from 10^21 | 0.6664 | 0.6629628085… | — |
| 5 | 8.5·10^-5 √k on [10^8, 2.4·10^15] | 0.9589999424… | 0.8904449457… | 4164.13 ≤ 4183.79 |
| 6 | 6·10^-5 √k on [2.4·10^15, 3.39·10^17] | 0.66499999… | 0.6285433151… | 34934.2239 ≤ 34934.6640 |
| 7 | 0.05 k^{1/3} from 3.39·10^17 | 0.665 | 0.6300939008… | — |
| 8 | 0.052 k^{1/3} from 10^21 | 0.6664 | 0.6628416031… | — |

In every case β(k_a) ≤ 1.2·10^-7 and E ≤ 6.51·10^-7. With the decimal bounds for B1 and
L1 in place of their expressions, (iii) and (iv) still hold in all eight cases.
R⁺(k_a)/k_a then exceeds the printed entries of cases 3 and 4 by 5.20·10^-9 and
4.78·10^-9, as the caption says.
Also: B1 ≤ 5.3033531 and L1 ≤ 100021.23 (6.3738031 and 100025.52 for K = 13); c̄_∞ >
0.062853 and > 0.052297; and the comparisons of C’s Section 1 (4.17·10^12, 460, 214.9, W
≥ 4 from 9·10^8, W ≥ 6 from 2.5·10^9).

## Q’s Supplementary Tables, Executed

The source reports that its own script checks these tables.
Until now this project had read them as source claims and run nothing on them
(think-yf8j). `q_supplementary.py` runs every claim in them, with every parameter set
held to (C0)–(C7) at its k (118 checks, all proved; 41 displays, all tight).

**Table 4 (further thresholds).** Each column satisfies conditions (i)–(iii) at its k0.

| K | c* | k0 | Ψ̄(k0)/k0^{1/4} | D1 | y1^{1/4} D1 against K_W/(2B̄) |
| --- | --- | --- | --- | --- | --- |
| 9 | 0.12 | 2.17·10^13 | 0.1200448… | 0.0067036… | 12.1665… against 0.0062733 |
| 9 | 0.14 | 2.01·10^14 | 0.1400019… | 0.0041135… | 13.0243… against 0.0077586 |
| 9 | 0.15 | 1.18·10^15 | 0.1500058… | 0.0027026… | 13.3200… against 0.0083679 |
| 9 | 0.16 | 2.77·10^16 | 0.1600075… | 0.0012500… | 13.5604… against 0.0088999 |
| 13 | 0.12 | 3.78·10^14 | 0.1200086… | 0.0029558… | 10.9597… against 0.0066855 |

The example after the table holds: (2065/0.16)^4 > 2.77·10^16 > (2064/0.16)^4.

**Table 5 (bounds at single k).** Each parameter set satisfies (C0)–(C7) at its k, and
⌈Ψ̄(k)⌉ is the printed bound for W.

| K | k | B̄ | Ψ̄(k) | W ≥ |
| --- | --- | --- | --- | --- |
| 9 | 10^13 | 36.5253675… | 196.7738… | 197 |
| 9 | 10^14 | 33.8080829… | 426.1698… | 427 |
| 9 | 10^16 | 32.4096691… | 1575.7615… | 1576 |
| 9 | 10^20 | 31.9101623… | 16751.2826… | 16752 |
| 9 | 10^30 | 31.7249406… | 5363347.5264… | 5363348 |
| 13 | 10^13 | 43.8461259… | 163.9198… | 164 |
| 13 | 10^14 | 40.5842257… | 355.0150… | 356 |
| 13 | 10^16 | 38.9055015… | 1312.6666… | 1313 |
| 13 | 10^20 | 38.3368551… | 13948.5192… | 13949 |
| 13 | 10^30 | 38.1280482… | 4462691.4535… | 4462692 |

**Section 12.6 (sensitivity).** Every claim holds:

- B_crit = 38.5108242… ≥ 38.510824;
- the relative margin is 1.04630…·10^-4 < 1.05·10^-4.

Each tolerance below satisfies (i)–(iii) at its printed value.
Condition (i) fails one unit above it in the last digit, and the largest value at which
(i) holds lies in the bracket the program decided:

| Tolerance | Printed | Largest value where (i) holds |
| --- | --- | --- |
| (a) A′, with A ≤ 10.6067 | 10.60905 | 10.6090514692… |
| (b) A, with A′ ≤ 10.6068 | 10.60891 | 10.6089191657… |
| (c) A, with A′ = A + 10^-4 | 10.60781 | 10.6078176004… |
| (d) C_Λ | 1.0150 | 1.0150101658… |
| (e) b_W in Theorem 9.1 | 53.09 | 53.0942386… |
| (f) the wall term, times its bound | 1.434 | 1.4349925… |

The remaining claims also hold:

- **C_Λ = 2.** With C_Λ = 2, (ii) and (iii) hold at 4.62·10^12 and (i) fails there.
  The crossing lies at 4.844966…·10^12, and at 4.845·10^12 conditions (i)–(iii) and (C7)
  hold.
- **The least admissible k.** The least integer with (C7) is 84,216,488,464 for π*, and
  (ii) and (iii) hold there.
- **The threshold k*.** Condition (i) fails at 4,616,673,963,026, where φ =
  −1.67·10^-12, and holds at 4,616,673,963,027, where φ = +2.94·10^-12. So k* =
  4,616,673,963,026.36… and k0/k* − 1 = 7.204…·10^-4.
- **Theorem A13.** The relative margin is 1.73857…·10^-5. The least integer with (C7) is
  120,000,600,012, and (ii) and (iii) hold there.
  Condition (i) fails at 21,695,977,343,082 and holds at …083, so k*13 =
  21,695,977,343,082.4… and 2.17·10^13/k*13 − 1 = 1.854…·10^-4.

## Findings

| Id | Severity | Grade | Where | Finding |
| --- | --- | --- | --- | --- |
| F1 | note | note | Q L528–563, L567–596, L616–636 | Proposition 2.1 and Theorem A13 rest on facts about [R]’s proofs, which [R] states in remarks, one of them marked unused; each fact is in [R]’s text |
| F2 | note | note | Q L544–546 | One quotation of [R, Remark 4.11] drops an emphasis; the 19 statements and 12 sentences quoted are otherwise [R]’s text |
| F3 | note | note | Q L177–186, L5258–5262; C L143–147 | What each theorem needs from [R]: Theorem A and C’s Theorem 1.1 need Lemma 4.10’s box computation (think-k3tk), which the all-pairs reading inherits; Theorem A13 and C’s Theorem 1.2 need only Lemma 4.9, whose finite check reproduces |
| F4 | note | note | Q L140–145, L5329–5391 | The explicit threshold 4.62·10^12 has a relative margin of 1.05·10^-4 in B̄, and A13’s 1.74·10^-5; the record should carry it |
| F5 | note | note | register, the Q and C rows | The side conditions do not say that k² − M(k) is the limit of W(x) from below; the C row’s corollary says “the quarter-power coefficient 0.1” for the bound 0.1 k^{1/4} |
| F6 | note | note | C L498–511 | The two liminf constants are reached by a limit; explicit parameters give finite thresholds 10^24 and 10^22 |
| F7 | note | minor | Q source README L64, paper L5430 | Q names its repository github.com/squarepacker/k2-minus-c-power; it was released as squarepacker/k2-minus-c-quarter |
| F8 | note | note | `review-2026-10-05-squarepacker-k2-minus-c.md` L165; `review-2026-10-08-quarter-cube-proof-chains.md` L78–79 | The earlier reviews state Lemma 4.9’s least margin as “at least 25.942°”; it is 25.9419054…° (added after the comparison; see there) |

**F1. Proposition 2.1 and Theorem A13 rest on facts about [R]’s proofs.** Q applies the
multiplicity bounds of [R, Lemmas 4.9 and 4.10] to three families of pairs, in Sections
5, 7 and 8. Their members are pairs of squares, or a square and the bottom or top side,
at distance < d, and they need not be edges of a visibility graph.
[R] states its two lemmas for edges of G_h or G_v. Q’s Proposition 2.1 bridges the
difference with:

- the paragraph after the proof of Lemma 4.9 (R L740–743);
- the first sentence of [R]’s Remark 4.11 (R L827–834), which ends “This remark is not
  used in the proofs”.

The analytic variant rests in the same way on where Lemma 4.10 enters [R]’s proofs of
Lemmas 4.13–4.15 (Remark 2.2).

I checked the six facts against [R]’s proofs (The Imported Lemmas of [R]):

- Lemma 4.9’s count uses only geometry.
- Lemma 4.10’s computed bound U(I) is defined over centres and directions, never over
  the graph.
- The one-side argument at R L769–772 covers a square near a corner whose rectangle
  stands on a third side.
- Lemma 4.10 enters only the two sentences Q names.

So Q’s use is sound.
But a reader who checks [R] by its statements alone does not cover Proposition 2.1,
which needs the bound for any family of pairs with two opposite sides.
The record should say so wherever it says [R] was reviewed.
A future revision of [R] could state the all-pairs form as a lemma.

**F2. One quotation drops an emphasis.** Section 2 quotes 19 statements of [R], each
identical to [R]’s text up to cross-references.
The 12 sentences it quotes from [R]’s proofs and remarks are found verbatim, with one
exception: at Q L544–546, [R]’s “the number of \emph{all} pairs” is printed without the
emphasis. `q_quotes.py` decides both counts; it does not read the PDF.

**F3. What each theorem needs from [R].**

- Theorem A, its c_∞ and threshold, and C’s Theorem 1.1 use K*_w = 9, through A, A′,
  C_Λ, B1 and L1 (Q Remark 2.2, C L143–147).
- So they rest on [R, Lemma 4.10]’s box computation, whose labels have one
  implementation and a replay with the producer’s code (think-8nv9). think-k3tk owns the
  independent per-box labelling, a separate obligation this review does not discharge.
- Proposition 2.1’s all-pairs form needs nothing more from that computation, because the
  quantity U(I) it bounds is already the all-pairs count (F1). A labelling that
  re-decides U(I) ≤ 9 on [R]’s boxes covers Q’s use as well.
- Theorem A13, its constant 0.1411 and C’s Theorem 1.2 need only Lemma 4.9.
  `r_lemmas_check.py` redid Lemma 4.9’s finite check from the text.
  It enumerates all 1,344 class sequences of length 3 to 5 and decides every one with
  sum at least 14 on intervals:
  - every sequence with sum ≥ 15 violates the angle conditions by more than 25.94°;
  - with sum 14, only the rotations of (5,2,5,2) satisfy them, at 358.92°;
  - part (c) then lowers 14 to 13.

**F4. The threshold’s margin.** Theorem A’s threshold 4.62·10^12 is k* rounded up to
three digits. The bracket B̄ = 38.5067952… may rise only to B_crit = 38.5108242… before
condition (i) fails at k0, a relative 1.0463·10^-4. For Theorem A13 the relative margin
is 1.7386·10^-5.

Q says so in Section 1 and Section 12.6, and every number reproduces.
The asymptotic constants c_∞ and c_∞^(13) do not depend on the margin.
But any upward correction of A, A′, C_Λ, b_W or the wall term beyond the tolerances of
Section 12.6 raises the explicit threshold.
The register’s note says the numerical consequences rest on the reviewed premises; the
margin is worth stating there.

**F5. Two wordings in the register.**

- The Q and C rows’ side conditions read “Integer sides and unit squares pairwise
  disjoint as closed sets in [0,k]^2”. They are accurate.
  Unlike the v1.1 row, they do not say that k² − M(k) is the limit of W(x) as x → k from
  below, the quantity of a register whose W(k) is 0 at every integer.
- The C row’s corollary says the Theorem 1.1 bounds “exceed the quarter-power
  coefficient 0.1 for every k >= 4.62*10^12”. They exceed the bound 0.1 k^{1/4}; the
  coefficient of k^{1/4} is not what they are compared with.

This pull request makes both edits.

**F6. The liminf constants by explicit parameters.** C reaches 0.06285 and 0.05229 by a
limit. Proposition 5.1’s conditions are met at some finite k_a once γ is below c̄_∞.

`c_constants.py` exhibits such k_a. Take τ0 = 1/6, τ1 = 1/6 − 10^-6, ν0 = 10^-5 and b
the optimal value rounded to six digits (1.000014 and 1.000063). Then (i)–(iii) hold:

- at k_a = 10^24 for γ = 0.06285, with the K = 9 constants;
- at k_a = 10^22 for γ = 0.05229, with the K = 13 constants.

So W > 0.06285 k^{1/3} for every integer k ≥ 10^24, and W > 0.05229 k^{1/3} from 10^22
without [R, Lemma 4.10]. The text’s argument needs no such witness; this one only makes
the statement checkable at a stated k.

**F7. The repository name.** Q’s source README (“How to cite”, L64) and its verification
status (L5430) give the programs’ home as github.com/squarepacker/k2-minus-c-power.
The release #414 reports, and the archive DOI 10.5281/zenodo.23211207, are
squarepacker/k2-minus-c-quarter.
C cites Q at the latter (C L579). I could not reach the former from this session, so
whether it redirects is a question for the author.

**F8. The earlier reviews’ margin for Lemma 4.9.** Found while comparing, after F1–F7
were committed. The 5 October review of [R] v1.1 states that every class sequence with
sum ≥ 15 fails Lemma 4.9’s angle conditions “by at least 25.942°”, and the 8 October
review repeats the figure.
The least excess is 25.9419054…°, attained at (3,5,2,5), so the figure is rounded the
unsafe way in its last digit.
[R] states “more than 25°” and needs only a positive margin, so no conclusion changes.
The earlier reviews are left as written; this note records the correction.

## Questions for the Author

1. **The all-pairs bound.** Would you state the form of [R, Lemmas 4.9 and 4.10] that
   Q’s Proposition 2.1 uses, any family of pairs with two opposite sides, as a lemma of
   [R] with its proof? [R]’s Remark 4.11 is marked as not used in [R]’s proofs, while Q’s
   proofs use it.
2. **The repository.** Is github.com/squarepacker/k2-minus-c-power, named in Q’s README
   and its verification status, the same repository as squarepacker/k2-minus-c-quarter?
3. **The threshold.** Theorem A’s threshold sits 7.2·10^-4 above k*. Would you consider
   stating Theorem A from a rounder threshold with more margin, such as 5·10^12, or
   printing k* beside k0? A small upward correction to a constant of [R] would then not
   move the theorem.

## Comparison with the 8 October Review

*Written after the findings above, which were committed (`41dffb13b`) before the 8
October review, its addendum and `cases/asymptotic/quarter_cube_constants.py` were
opened.* After that commit I read the maintained checker and its test, the 8 October
review with its addendum, and the 5 October review’s paragraph on [R, Lemma 4.9].

**Where the two reviews agree.** On every point both cover, they reach the same verdict.

- Both chains are complete, conditional on [R]’s lemmas.
  The K = 9 route keeps Lemma 4.10’s per-box limitation, and the K = 13 route keeps
  Lemma 4.9’s finite check.
- Proposition 2.1 is needed beyond the visibility graphs, and [R]’s proofs support it.
  The 8 October review says Q “supplies” the extension.
  F1 adds that Q supplies it from remarks about [R]’s proofs, which a statement-level
  reading of [R] does not cover.
- In Q, both reviews agree on:
  - the hull slit, and the vertical transfer with its constants (χ > 0.99999849, the end
    loss 1.0000016 δβ̄, the error terms 8.5·10^-10 and 1.22·10^-9);
  - the separation of the floor and ceiling families by heights two apart;
  - the valley width δ tan θ/cos θ, and at most four squares per pair for merges.
- In C, both reviews agree on:
  - choosing θ from W;
  - τ0 − 1.0001β > τ1;
  - the exact band measure for odd k;
  - R⁺ with k/2 in place of k/2 − 1;
  - condition (iv), essential for p = ½, with case 6 the tightest.
    Its margin is 0.440 in W (the earlier “about 0.43” is the printed 34934.66 −
    34934.23).
  - the decimal B1 and L1, which move the last digits of two rows: cases 3 and 4.
- The addendum’s figures are mine:
  - threshold margins 0.0153398 and 0.0037524;
  - D1 = 0.00864298 and 0.00557907;
  - derivative-loss margins above 10.65 and 10.12.

**The 108 predicates.** `qcc_predicates.py` reads the maintained file with `ast`,
without importing or running it.
Its inputs agree with my transcription of the primaries: two quarter rows, eight cube
rows and the two overlaps’ six ceilings.
All 108 predicates hold on my intervals: 2 rosters, 2 × 12 quarter conditions, 8 × 8
cube conditions, and per overlap the seven ceilings and two asymptotic floors.
The two implementations share no code.
The maintained one works in mpmath’s interval context at 60 digits; mine works in exact
rationals, with series written for this review.
The maintained test asserts that all 108 hold; I did not run it.

**What this review adds.**

- Q’s Tables 4 and 5 and its Section 12.6, which the earlier review “read as source
  claims”, now reproduce in full (118 checks).
- Two premises the maintained checker takes as given are now decided:
  - c_E = 41.933, which the addendum leaves as “a proof premise”, in both ranges of |Δ|
    (41.93109… and 41.93124…);
  - the sum 1185.5002 ≤ 1185.6 that makes C_Λ (and 1712.52 ≤ 1712.6).
- Lemma 4.9’s finite check, which the earlier review inherited from the 5 October
  enumeration and did not rerun, is enumerated afresh (F3).
- Q’s quotations of [R] and C’s citations of Q are checked mechanically (F2).
- Every displayed digit of Q’s Tables 2 and 3 is held in its stated rounding direction,
  which the maintained checker does not do.
- Explicit starting scales are given for both of C’s liminf constants.
  The earlier review noted that the text gives none (F6).
- F4, F5 and F7 are new.

**Where they differ: one number.** The 5 October review of [R] v1.1 says every class
sequence with sum at least 15 “fails by at least 25.942°”
(`review-2026-10-05-squarepacker-k2-minus-c.md`, line 165). The 8 October review repeats
the figure (line 78–79). The least excess is 25.9419054…°, at (3,5,2,5) and its
rotations. My interval enumeration found it, and a float cross-check in mpmath at 60
digits agrees.
The safe statement is “at least 25.941°”. [R] claims only “more than 25°”,
and its proof needs only a positive margin, so nothing depends on the digit (F8).

## Verdict

**Accepted, for both preprints.** Q’s Theorems A and A13 and Corollary A, and C’s
Theorems 1.1 and 1.2 and Corollary 1.3, follow from their arguments as written, under
the closed-set convention and the equivalence of [R, Lemma 2.1]. They are conditional on
the imported lemmas of [R]. Theorem A, c_∞, the threshold 4.62·10^12 and C’s Theorem 1.1
also need [R, Lemma 4.10]’s box computation, whose per-box labelling stays think-k3tk’s
obligation. Every number they use, and every number of Q’s supplementary tables,
reproduces on exact intervals.
No finding is a defect or a gap.

This is one adversarial AI review, confirming at the level of a read of the chains with
the constants independently recomputed.
It changes no rung of any result, since neither preprint has a register entry, and it is
not a human oversight record.

## Independence and Disclosure

- **Programs:** written for this review from the three TeX sources.
  The deciding ones import only Python’s standard library: `fractions`, `math`,
  `itertools`, `json`, `hashlib`, `re`, `ast`. The interval arithmetic and every
  elementary function are their own.
  Only the float cross-check of F8 uses mpmath.
  They share no code with the source’s `k14_constants_check.py` or `check_table_*.py`,
  which were never read or run, or with the maintained `cases/asymptotic/` checkers.
- **Read before these findings:**
  - the brief and the bead think-yf8j;
  - the register’s rows for both preprints and for [R], whose notes mention the 8
    October review and the 108 predicates of `quarter_cube_constants.py` without their
    content;
  - #414’s entry in `result-requests.yaml`, which says that review accepted the chains
    “at source-review scope, conditional”;
  - stage 4 of the runbook and the two format examples named in Scope;
  - the packet READMEs, and the source READMEs and review summaries, as data.
- **Not read before these findings:** the 8 October review
  (`review-2026-10-08-quarter-cube-proof-chains.md`), its addendum,
  `cases/asymptotic/quarter_cube_constants.py`, `ryu_k2_minus_c_constants.py`, and the 8
  October review of [R] v1.2.
- **Read after these findings were committed:** `quarter_cube_constants.py` and
  `tests/test_quarter_cube_constants.py`, the 8 October review with its addendum, and
  lines 150–172 of the 5 October review of [R] v1.1. `ryu_k2_minus_c_constants.py` and
  the 8 October review of [R] v1.2 stayed unread.
- **Shared system family:** the reviewer is a Claude agent.
  Both sources say they were developed with extensive assistance from Claude, and their
  earlier reviews were by Claude sessions.

## What This Review Does Not Establish

- It does not decide [R, Lemma 4.10]’s box labels or its coverage.
- It does not decide [R]’s Proposition 4.5 beyond a careful read and its numbers.
- It establishes no human oversight, and no rung for a result that has no register
  entry.
- It does not check the k^{3/8} upper bounds that the C row’s corollary pairs with C.
- It does not test either construction numerically, and runs none of the source’s
  programs.

## What I Ran

All with CPython 3.14.7 (`packing/.venv/bin/python3 -I`), under `nice`, one at a time,
on a shared four-core host.
The programs and receipts are in
[the quarter packet’s `review/quarter-cube-strongest-tier-2026-11-02/`](../../../packing/resources/web/squarepacker-k2-minus-c-quarter-2026-10-07/review/quarter-cube-strongest-tier-2026-11-02/README.md).

| Command | Receipt | Result | Time |
| --- | --- | --- | --- |
| `iv.py` | printed | 8 of 8 self-tests | 0.4 s |
| `q_constants.py outputs/q-constants.json` | `q-constants.json` | 193 of 193 proved; 57 of 57 displays tight | 0.7 s |
| `q_supplementary.py outputs/q-supplementary.json` | `q-supplementary.json` | 118 of 118 proved; 41 of 41 displays tight | 18 s |
| `c_constants.py outputs/c-constants.json` | `c-constants.json` | 95 of 95 proved; 24 of 24 displays tight | 0.4 s |
| `r_lemmas_check.py outputs/r-lemmas.json` | `r-lemmas.json` | 48 of 48 proved | 2.5 s |
| `q_quotes.py Q_TEX R_TEX outputs/q-quotes.json` | `q-quotes.json` | 19 of 19 statements, 12 of 12 sentences | under 1 s |
| `c_citations.py Q_TEX C_TEX outputs/c-citations.json` | `c-citations.json` | 44 of 44 citations resolve to their kind | under 1 s |
| `qcc_predicates.py MAINTAINED_PY outputs/qcc-predicates.json` (after the findings) | `qcc-predicates.json` | 108 of 108 predicates hold; inputs match the primaries | 0.3 s |

In all, well under a CPU-minute.
F8’s cross-check in mpmath, `l49_mpmath_crosscheck.py`, is a float computation that
decides nothing. It is kept with its output, `l49-mpmath-crosscheck.txt`, and registered
nowhere. Each receipt records the SHA-256 of the programs that wrote it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
