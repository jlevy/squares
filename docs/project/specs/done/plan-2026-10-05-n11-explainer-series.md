# N11: A Three-Paper Explainer Series

**Date:** 2026-10-05 (merged the same day from two reviewed revisions of the first
draft; see the [Review Record](#appendix-review-record))

**Status:** Plan. The defaults below apply unless the owner changes them.

**Beads:** epic `think-92ar`; slices `think-4fe0` (S2), `think-3snx` (S3), `think-mjih`
(S4a), `think-22wm` (S4b), `think-eqw0` (S4c), `think-0uti` (S5), `think-jnt2` (S6),
`think-2py3` (S7), `think-n5dh` (S8). Related: `think-ny2u` (the T-064 paper, a separate
fourth paper), `think-yf6t` (the C5 question), `think-4lye` (crediting T-025’s threshold
atom in the n = 17 line).

This plan adds a review paper for Kleddamag’s `s(11) > 31/8` (T-037). It also binds the
three n = 11 papers into one linked series with one division of content, one notation,
one figure vocabulary, a define-before-use rule enforced by a test, and links between
the papers. Everything ships in *one pull request* that passes CI and is documented in
`development.md`, `conventions.md` and `paper-design.md`.

| # | Slug | Subject | Result | Kind |
| --- | --- | --- | --- | --- |
| I | `n11-lower-bounds-explainer` (exists, v0.4.3) | Point and two-of-three certificates (“proof by dots”) | T-018 3.81, T-025 3.82, T-026 3.8264474… | Explainer of the project’s own proofs |
| II | `n11-threshold-bound-review` (*new*) | k-of-m charges, parents with strict cores over angle rows, the exact sweep | T-037 `s(11) > 31/8` | Stage 6 review of an external proof |
| III | `n11-optimality-review` (exists, Draft v0.1.4) | Cover, pose invariant, charge transfer, symmetry, capture, isolation | T-060 `s(11) = T ≈ 3.8770836` | Stage 6 review of an external proof |

Sources:

- Kleddamag’s proof at `6a733f3` (v1.0.2). The original repository and the archived copy
  at `packing/resources/web/external-square-certificates-2026-09-22/kleddamag-11/` have
  identical `PROOF.md` and `ATTRIBUTION.md`.
- The project’s two reviews of 2026-09-22:
  `review-2026-09-22-kleddamag-n11-mathematics.md` (“the audit”) and
  `review-2026-09-22-native-n11-parent-core.md`.
- The native verifier `devtools.verify_kleddamag_n11_native` and its row journal
  `campaign/agent-sessions/session-153-native-full.rows.jsonl`; the audit instrument
  `devtools.audit_kleddamag_n11`; the T-059 replay journal
  `resources/web/wand125-tools-2026-09-29/receipts/n11-bound-full.jsonl.gz` (all 12,028
  exact row minima with exact witnesses).
- The register (`packing/frontier/results.yaml`): T-010, T-018, T-025, T-026, T-032,
  T-033, T-037, T-038, T-059, T-060, T-061. Lineage facts come from the register and the
  source’s notices, not from memory.

Why it is warranted:

- T-037 is confirmed (V3/C3) and scored S5, which meets the Stage 6 trigger in
  `packing/campaign/result-import.md` (§“Stage 6: Explain”).
- The register says T-037 was superseded on 2026-09-29 by Wang and Li’s reweighted and
  scaled certificate (T-061, 3.9 × 10⁻⁹ higher) and by T-060. Paper II states both.

## Owner Decisions (Defaults Applied)

| Decision | Default | Reason |
| --- | --- | --- |
| Reading order | **I → II → III** in every listing: Papers page, home cards, README, bridges | A numbered series out of order reads as a mistake; each bridge points forward; the concept spine assumes reading order. The Papers page lead sentence keeps T-060’s standing: “T-060 settles the case; Part III explains it.” |
| Slug | **`n11-threshold-bound-review`** | Case–subject–kind rule (`conventions.md` §2) |
| Title | **“A Review of the Certified Lower Bound s(11) > 31/8 for 11 Squares”** | Follows III’s “A Review of …” form. The math in the hero needs the `HERO_TITLE` `.tex` treatment Paper I uses for “n = 11”; `TITLE` stays plain text for metadata |
| Threshold terminology | **“k-of-m”** (threshold k, m sites); never “m-of-k” | Used by the source, the register and `evidence.yaml` |
| “Charge” or “atom” | **“charge”**: a *point charge* and a *k-of-m charge* are the objects; *the charge C(Q)* is what a core receives. “Atom” appears only to gloss Paper I’s name | III says “charge” for the object and the quantity (III L476, L501, L506) and the source does too (PROOF.md:33–39). I is published and keeps “atom”; II and III gloss it once |
| I’s Figure 3 | **Unchanged.** The series bound ladder appears in II and in III’s lineage section | I’s Fig 3 is a linear number line with its own guards; a T-037 tick would sit about 0.002 from T |
| Home cards | Three paper cards on one line: `SECTION_CARD_LINES = {"pages": (1, 3, 2)}` | Keeps one card per paper |
| III and I edits | Ship in this PR: III v0.1.5, I v0.4.4 | One-PR requirement |
| Three-change wording | Fixed in §5.2 Section 1 and reused on the Papers card; III’s lineage links to II instead of repeating the list (series review of 2026-10-05) | One wording, checked against §4; a second copy in III was duplication |

## 1. Series Principles

1. **Every paper stands alone.** A reader starting at II or III gets every definition
   they need. A definition may be a one-paragraph recap that links to the paper that
   derives it in full.
2. **Each concept has one owner.** One paper derives each concept in full (§2). The
   others give a recap of at most one paragraph with a deep link to the owner’s section.
3. **Every term is defined before it is used, in reading order.** This holds for symbols
   and lemmas too. A roadmap or preamble may name a later concept only with an explicit
   forward marker (“defined in Section 4”). A caption may use a term defined earlier but
   may not define one. §5.3 gives II’s concept spine, §7.2 gives III’s audit, and §9.4
   makes the rule a test.
4. **The papers form a linked series.** Each lineage section names the previous paper as
   an antecedent, not a premise (as III already treats I). Each closing bridge names the
   next paper. Each front carries a series strip, “Part N of 3”.
5. **One notation** (§3). Paper I’s symbols are fixed because I is published and older.
   II fits around them.
   III renames a symbol only where it clashes with I, and only to a symbol that collides
   with nothing in I, II, III or `TUTORIAL.md` §10.
6. **One figure vocabulary** (§6). II and III draw the same object the same way.
   I keeps its canvas figures.
7. **The form follows III.** Provenance, Theorem, roadmap figure, mechanism before
   census, and a closing section on what was verified and what that means.
   One departure: II’s unheaded preamble is at most five lines, so the theorem and the
   three changes are on the first screen.
   Figures are static SVG generated in Python from hash-pinned data.
8. **Credit is accurate and early.** II says in its first two sections what the source
   proof added and what it inherited, each item named by result id or source file.
   §4 is the single source for that.
   Where the sources do not name one originator, II writes “inherited through the
   Levy/Guzhou0806/Mira line”.
9. **One PR, documented end to end.** The paper, the infrastructure, the edits to I and
   III, the reference inventory (§8) and the documentation land together.

## 2. Content Ownership

| Concept | Owner | Recap in |
| --- | --- | --- |
| s(n), the problem, upper and lower bounds, bound history | I | II, III (one paragraph plus the series bound ladder) |
| Site, atom (I) = point charge (II, III), core, mass, the mass–budget contradiction | I | II (§3 maps the terms) |
| Event cells, least covered mass, the sweep as an idea | I | II (II owns the parent-centre envelope, slabs, y-cells and the signed segment-tree sweep) |
| Direction net, rational half-tangents, orientation mod π/2, **D**₄ folding to [0, π/4]: reflect, choose the core, reflect back (I L419–428, L572–586) | I | II (one paragraph, adapted to parents and rows). III works on [0, π/2] because its cover has only the half-turn symmetry (III L591–597); II’s bridge says so |
| Threshold atom (S, k, w) for any 1 ≤ k ≤ \|S\|; budget w⌊\|S\|/k⌋ by pigeonhole; the general counting theorem (I L609–631); 2-of-3 at T-025 | I | II recaps with a link, then extends (next row) |
| **Which k-of-m families pay** (the price comparison, no saving when k divides m), **2-of-5 as the first family that pays two disjoint cores**, budgets adding across shared sites | **II** | III (one sentence in “Charge Budgets”, contrasting capacity one with ⌊m/k⌋) |
| **Parent side A < 1, scaling to L₀/A, one concentric closed core per angle row, strict containment over a row, the parent-centre envelope** (inherited, §4) | **II** | III (one sentence; III’s strict core over an interval links to II’s Strict-core lemma) |
| Rational dilation q < c (T-026) | I | II relates the shrunken parent to it: both scale the certificate against unit squares |
| **Signed inclusion–exclusion into rectangles (T-025’s identity), first exposed in a paper; the exact integer sweep** | **II** | — |
| **Upper semicontinuity at boundaries; compactness and attainment** (I L598–599 has a one-sentence remark) | **II** | — (III needs neither: its witness attains T) |
| Exact construction of Trump’s packing, Voronoi cover, pose invariant | III | — |
| Median-projection charge with capacity one; charge transfer | III | II’s bridge relates it to k-of-m (§5.2 Section 10) |
| Symmetry overlay, capture tree, local isolation, the rational cap and frame change | III | — |
| Receipts; rungs V/C/S (`epistemics.md`); what a replay does and does not establish | III | I and II use the same obligation → evidence table form |

**What each paper proves, and with which sign:**

| Paper | Statement | Sign | Why that sign |
| --- | --- | --- | --- |
| I | s(11) ≥ 3.8264474… (T-026), via 3.81 (T-018) and 3.82 (T-025) | ≥ | The verifier’s theorem is stated with ≥; I L598–599 remarks that compactness gives > |
| II | s(11) > 31/8 (T-037) | > | Exclusion at exactly 31/8 plus attainment of the minimum |
| III | s(11) = T (T-060) | = | The construction attains T; every S < T is excluded |

## 3. Notation and Terminology

Collision checks were run by grep over the templates of I and III and over
`TUTORIAL.md`. III already uses ρ, η, ζ, τ, λ, σ, θ, Δ, ε, M_j, R; `TUTORIAL.md` §10
uses β (a field element) and κ_j (a multiplier).
Γ, “rot” and ξ occur nowhere in the three.

| Object | I | II (source’s symbol) | III today → change |
| --- | --- | --- | --- |
| Quantity under study | s(11) | s(11); the source’s functions c(t), s(t) become cos θ, sin θ, never `s(·)` | III’s c, s (L160–163) are constants of the construction, not functions: **keep** |
| Container side under test | L₀ (L151) | L₀ = 191/50 (L) | S (L79, L101, L213, L870–872 and the figure labels in `n11_optimality_overview_figures.py`) → **L₀** |
| Proved bound | L (L25) | 31/8, or L₀/A; never called L or T | T |
| Parent side | — (I’s A at L707 is the LP’s site set) | A = 764/775 | III’s A(a, b) (App. A) and A_i (L806) are local; listed clash |
| Core side | B, “shrink” (L251) | B, one per row | B is the file scale (L218, L226, L883) → **drop the symbol**, write (191/50)/U |
| Core | Q_i (L575), P (L611) | Q | Q is a convex core (L367, L376): keep. Quarter-turn Q (L875, L879) → **rot**, written rot(x, y) = (−y, x) |
| Charge of a core | μ(Q), mass | C(Q) | III’s cells C_j stay; III writes “charge at least Γ_i”, no C |
| Binomial coefficient | — | \binom{j−1}{k−1}; never C(·,·), which is the charge | — |
| Per-core floor; total budget | 1; Σw | Γ, M (both unnormalised) | q_i (L471, L536, L542; Fig 7 labels “q₁ = q₂ = 1”) → **Γ_i**, mirroring II’s Γ. **b stays** (L508), because M_j is taken (L829); II’s bridge says b plays the role of M |
| Threshold set, size | S, \|S\| (L609) | S, m = \|S\| | — |
| Cores paid by one charge | r (L617) | r (source: q, which is I’s dilation) | — |
| Dilation | q (L667) | q (recap only) | — |
| Packed square or parent angle | φ (L423) | φ; a row covers tan(φ/2) ∈ [a, b] (source: u, which is Trump’s root u in III and `TUTORIAL.md`) | III’s θ_i, t_i stay; II’s bridge names them |
| Net or core direction | θ_k = 2 arctan t_k (L250) | θ = 2 arctan t, the row’s core (source: t) | — |
| Angle mismatch | d (L436; `TUTORIAL.md` §10) | d (source: δ, which is `TUTORIAL.md`’s inflation slack) | — |
| Envelope inset | — | ρ = A·min(cos φ + sin φ at a, b)/2 (source: r, which is I’s count) | III’s ρ is a constant of Appendix A (L1019); listed clash |
| Symmetry group | **D**₄ (bold) | **D**₄ | D_4 (L603) → **D**₄ |

Line numbers in the III column are of `n11-optimality-review-article.md` v0.1.4; those
in the I column are of `n11-lower-bounds-explainer-article.md` v0.4.3. New II symbols
(A, Γ, M, ρ, the row (a, b, t, B)) are added to `TUTORIAL.md` §10 or marked local in II,
as `conventions.md` §5 requires.
The renames touch SVG labels, so L₀, Γ and the subscripts must pass
`tests/test_site_glyphs.py`; otherwise they are typeset in the caption, not the SVG.

**Terminology map:** Each series term is glossed once at first use in II; III changes a
term only where it collides.

| Series term (II) | Paper I | Source (Kleddamag) | Paper III |
| --- | --- | --- | --- |
| site (a position) | “site” for an atom’s point | site | Voronoi “sites” (L241) → “cover site”; charge sites (L476) → “charge site” |
| point charge | atom (L280) | ordinary weighted site | “weighted charges at single points” (L506): keep |
| k-of-m charge (S, k, w) | threshold atom (L609) | charge, feature; legacy “triples”, “movable support” (status string in `exact_mixed.py`) | “feature” (L506–507), undefined → “charge”; “separation feature” (L772) keeps its name |
| capture (a closed core contains a site) | trace P ∩ S (L611) | capture | — |
| charge C(Q) | mass μ (points), total weight (thresholds) | logical charge | charge, first used L148 → defined in III’s lineage paragraph |
| budget; capacity ⌊m/k⌋ | at most ⌊\|S\|/k⌋ cores (L617) | budget floor(m/k)w | budget b; capacity one (L501); “a cell has capacity one” (Fig 4) → “holds at most one centre” |
| row | net direction | catalogue row (a, b, t, B) | row: a closed t-interval (L316) |
| event cell, slab, y-cell | event cell | slab, open cell | — (III’s cells are Voronoi cells) |
| bound gap | “gap” (Fig 3 caption) | gap | “gap” (L145) → “bound gap” (`conventions.md` §5); the projection gap (L175) stays |
| threshold = k | threshold k | threshold | “threshold one” (L512) → “a required charge of one” |

“Field” has one sense in II, which uses no number field.
III resolves its three senses (L183, L217, L469; adversarial review §3.2) in §7.2.

**Theorems and lemmas:** Each paper states one unnumbered **Theorem**. Lemmas are
bold-named, unnumbered, and unique across the series: I’s **Conditions 1–5**; II’s
**Budget**, **Scaling**, **Folding**, **Strict-core**, **Envelope**,
**Signed-expansion**, **Boundary** and **Attainment** lemmas; III’s **Center-cover**,
**Pose-preservation**, **Symmetry** and **Local-isolation** lemmas.
A cross-paper reference reads “Paper I’s Condition 4” or “Paper II’s Budget lemma” and
is deep-linked.

## 4. What Is New in T-037

This table is the credit inventory II states in Section 2. *Inherited* means a
registered or cited antecedent has the idea; *new data* means T-037’s instance of an
inherited idea; *new* means no antecedent is registered.

| Ingredient | Status | Evidence |
| --- | --- | --- |
| General threshold atom (S, k, w), budget w⌊\|S\|/k⌋, budgets summed across atoms that share sites | Inherited: Paper I (T-025) | I L609–631; `sqpack/fractional/threshold.py` docstring (names 2-of-5 and 3-of-5); audit Integration Finding 4; ATTRIBUTION.md:5–7, 18–22 (“does not claim independent invention”) |
| Signed inclusion–exclusion of a k-of-m indicator into rectangle terms; integer difference sweep | Inherited: T-025 | `review-2026-09-09-threshold-certificate-theorem.md` F6; `threshold.py` docstring; same coefficients |
| Point and 2-of-3 charges over contiguous parent-angle intervals | Inherited: Kleddamag’s own s(17) release (T-038), 2-of-3 only, 7,853 intervals | T-038 claim and `next_rung` in the register |
| Parent side A < 1 and bound L/A; one concentric closed core per angle interval; coverage only over the legal parent-centre square | Inherited through the Levy/Guzhou0806/Mira line. First registered certificate: Guzhou0806’s R012 (T-032, 2026-09-20). The centre restriction’s analytic antecedent is this project’s unit-parent centre note | `results.yaml` L2592–2597; `NOTICES/Mira-ATTRIBUTION.md`:40–45; `packing/cases/n11_five_dot_cover/unit-parent-centre-contract.md` |
| Smaller rational parent side; strict-containment transfer | Inherited through the line: R038 states it adds both; Mira’s attribution lists strict-core transport as prior work in this project | `NOTICES/Guzhou-NOTICE.md`:9; `NOTICES/Mira-ATTRIBUTION.md`:40 |
| Adaptive interval refinement, maximal safe rational cores, certified parent envelopes | Inherited through the line: the 4.614153 continuation recorded in Mira’s attribution, which names no single author | `NOTICES/Mira-ATTRIBUTION.md`:29–32; ATTRIBUTION.md:16 |
| Checkers: Python generalised from Kleddamag’s s(17) checker; JavaScript adapted from R038’s `exact_parent_side_scan.js` | Inherited code lineages | ATTRIBUTION.md:14–15 |
| **2-of-5 (10 orbits, 76 features, budget 2w each) and 3-of-5 (142 orbits, 1,124 features) in a retained certificate**; 2-of-5 is the first family in the series that pays two disjoint cores | **New** (the families are named in `threshold.py`; no earlier registered certificate uses them: T-025, T-026 and T-038 are 2-of-3 only, and R052’s 3-of-5, T-039, is dated 2026-09-25) | PROOF.md:9–14; I L637; the 2026-09-10 five-site study (`review-2026-09-10-n11-weighted-five-site-atoms.md`) produced no certificate |
| **Certificate re-optimised from T-026’s**: sites moved and rounded (denominator 10¹⁰), families added, weights re-optimised (10⁹), the catalogue replaced by 12,028 rows (widths 3.6 × 10⁻⁹ to 4.8 × 10⁻⁴, strict margin ≥ 10⁻¹²) | **New data** | ATTRIBUTION.md:13; PROOF.md:7, 22–23 |
| **Threshold charges in the parent-interval framework at n = 11** | **New at n = 11** (T-038 did this at n = 17 with 2-of-3 only) | T-037 and T-038 claims |
| The bound 31/8, strict by attainment | New | PROOF.md:3, 83 |
| Not claimed | A better packing, the exact minimum, external review, priority, how the certificate was found | PROOF.md:5, 85 |

The audit’s Integration Finding 4 notes that the certificate changes several ingredients
together, with no ablation that attributes the gain to any one; II says so.

## 5. Paper II

### 5.1 Front and Length

Front, written by `paper_front` from II’s `PaperFront`:

- Source: “From the original proof by **Kleddamag**” (`paper_front.Source.lead`),
  linking `github.com/Kleddamag/11-squares-certified-bound` at `6a733f3`.
- Human oversight and agent lines; “Draft v0.1.0”; dates “Original proof September 22,
  2026 · Last revised …”.
- The series strip “Part II of 3” (§9.2).
- `AUTHORS.md`’s statement that OpenAI Codex developed the mathematics and computation
  under Kleddamag’s direction goes in the preamble: `paper_structure.CREDIT_KINDS` has
  no slot for it.

Target: about 6,000 words of body including captions, between I and III, plus
appendices; at most 12 numbered figures (III has 11).

### 5.2 Sections

“Section N” is a section of Paper II; “§N” is a section of this plan.
Each entry gives what the section establishes, the PROOF.md lines it rests on, and its
figures.

0. **Provenance preamble** (unheaded, at most five lines).
   Links to proof, data and reproduction pinned to `6a733f3`; the Codex statement; one
   credit sentence (the proof develops this project’s T-026 certificate).
   It uses no symbol: “a lower bound of 31/8 for eleven squares”, not `s(11)`.
1. **The Result.** → `PROOF.md:3-7`.
   - Defines unit squares, packing (interiors disjoint, boundaries may touch), s(11),
     and orientation mod π/2.
   - The unnumbered **Theorem** `s(11) > 31/8`.
   - **Three changes from T-026**, fixed wording, k-of-m first, each forward-linked:
     1. **five-site k-of-m charges** (2-of-5 and 3-of-5 beside 2-of-3);
     2. **threshold charges on shrunken parents with strict cores** (side A = 764/775 in
        the container 191/50), a framework inherited through the Levy/Guzhou0806/Mira
        line;
     3. **a re-optimised certificate over 12,028 adaptive angle rows**, each with its
        own core.
   - Scope: no better packing; a bound gap of 0.0020836 to Trump’s T; superseded by
     T-061 (+3.9 × 10⁻⁹, this certificate reweighted) and by T-060. Why read it: it is
     the furthest the charge method reached, and III’s field certificates are easiest to
     follow against it.
   - **Fig II.1** what changed; **Fig II.2** series bound ladder; **Fig II.3** roadmap
     with the reader’s questions in order (as
     `review-2026-09-30-n11-explainer-intuition.md` “Proposed Reader Roadmap” revised
     III’s).
2. **What Is New, and What It Inherits.** The §4 inventory in plain language, each item
   labelled inherited, new data or new, with forward markers.
   - The k-of-m charge *informally*, on charge orbit 72: a 3-of-5 charge of weight
     0.067038144 (the largest in the certificate) on the sites (1.1938, 1.7190),
     (1.0314, 1.5280), (0.9858, 1.4579), (0.4584, 1.4898), (0.4966, 1.4898). A core
     holding any three is paid w; across disjoint cores the charge pays at most ⌊5/3⌋w =
     w. Formal in Section 3.
   - The contradiction previewed with its numbers: eleven cores need 10.999587808; the
     budget is 10.999479944. Formal in Section 4.
   - **Fig II.4** one k-of-m charge.
3. **From Points to k-of-m Charges.** → `PROOF.md:31-39`.
   - Recap of I in one paragraph: site, point charge (I’s atom), core strictly inside
     its square, capture, mass, the budget contradiction, I’s Conditions 1–5 by name.
   - The single generalisation: I’s 2-of-3 threshold atom with 2 and 3 replaced by k and
     m. The k-of-m charge (S, k, w), m = \|S\|; the charge C(Q) as the sum over point
     and k-of-m charges.
   - **Budget lemma** (recap of I L614–619 with a link, I’s letters): r disjoint cores
     each capturing at least k of m sites have disjoint captured subsets, so rk ≤ m.
     Then what I does not say: the inequalities add when charges share sites, because
     each is valid on its own; 2-of-5 (budget 2w) is the first family in the series that
     pays two disjoint cores.
   - **Why thresholds pay:** Guaranteeing w to every core that captures k of m sites
     with point weights w/k costs mw/k; the k-of-m charge costs ⌊m/k⌋w. Ratios 3/2
     (2-of-3), 5/3 (3-of-5), 5/4 (2-of-5). When k divides m there is no saving (2-of-4
     costs 2w either way), as `threshold.py` notes.
     The price: capturing fewer than k sites pays nothing.
   - Data motivation: points carry 79% of T-026’s budget and 20% of T-037’s. T-025’s
     ceiling family shows no **D**₄-symmetric point measure of mass below eleven exists
     at side 191/50 (`results.yaml` L1912–1913).
   - Credit, per §4.
4. **Parents and the One Inequality.** → `PROOF.md:16-29,79-83`.
   - A **parent** is a side-A square in [0, L₀]². **Scaling lemma**: eleven parents fit
     in L₀ exactly when eleven unit squares fit in L₀/A; (191/50)/(764/775) = 31/8
     because 764 = 4 · 191. It is I’s dilation q read the other way.
   - Each parent has an assigned core strictly inside it (forward link to Section 6).
   - Γ, the least charge of any assigned core; M, the sum of budgets.
     Eleven disjoint cores, each with C ≥ Γ, total ≤ M; 11Γ = 10.999587808 > M =
     10.999479944, a surplus of 107,864 units of 10⁻⁹. Neither is normalised; M/Γ ≈
     10.99989.
   - **Fig II.5** budget bars.
5. **The Certificate’s Charges.** → `PROOF.md:7-14`.
   - **D**₄ orbits and the **D**₄-invariant certificate.
     679 orbits become 5,284 sites: 496 carry point weight (66 orbits), 144 of them also
     in k-of-m charges; 4,788 are in k-of-m charges only; 4,932 sites are in some k-of-m
     charge; none is unused.
   - Point weight concentrates near the four lines x, y ∈ {A, L₀ − A}, where the inner
     edge of an axis-aligned parent touching a wall lies: 22 of the 66 orbits, 58% of
     the point weight, within 0.005; 78% within 0.05. The largest point weight,
     0.026140599, sits at (0.9596, 0.9858).
   - Family table (orbits, features, budget per feature, family budget); “physical
     feature” glossed as one copy of a charge orbit.
   - **Fig II.6** site map and gallery.
6. **Parents, Cores and the Angle Catalogue.** → `PROOF.md:41-51`.
   - Half-angle coordinates: cos θ and sin θ rational in t = tan(θ/2).
   - **Folding lemma** (recap of I with a link, adapted): each parent is folded
     separately into [0, π/4] and its core reflected back; the packing is not assumed
     symmetric. Closes G1.
   - **Rows** (a, b, t, B): 12,028 contiguous intervals of tan(φ/2) over
     [0, 207107/500000] ⊃ [0, √2 − 1] (t² + 2t − 1 = 309449/(2.5 × 10¹¹) > 0 at the
     end), widths 3.6 × 10⁻⁹ to 4.8 × 10⁻⁴, B from 0.98537 to 0.98581.
   - **Strict-core lemma**: A > B(cos d + \|sin d\|) on the whole row.
     The endpoint dot/cross checks keep d in [−π/4, π/4] throughout (2 arctan is
     monotone), and cos d + \|sin d\| increases with \|d\| there, so the endpoints bound
     the row (G5). The 48,112 rational quadratic inequalities (four per row) check it
     independently. Closed cores in interior-disjoint parents are pairwise disjoint even
     when parents touch.
   - **Fig II.7** parent and core; **Fig II.8** catalogue strip.
7. **Every Legal Centre Collects at Least Γ.** → `PROOF.md:51-77`.
   - **Envelope lemma**: at parent angle φ the legal centres are
     [A(cos φ + sin φ)/2, L₀ − A(cos φ + sin φ)/2]²; cos φ + sin φ has no interior
     minimum on [0, π/4], so the union over a row is [ρ, L₀ − ρ]² (G5).
   - **Capture rectangles**: in the core frame a site’s capture set is a closed
     rectangle of centres; a set of sites is captured exactly when the centre lies in
     the intersection.
   - **Signed-expansion lemma** (T-025’s identity, credited), full proof: coefficient
     (−1)^{j−k}\binom{j−1}{k−1} on j-subsets; the first difference via Pascal; the
     identity \binom{j−1}{k−1}\binom{h−1}{j−1} = \binom{h−1}{k−1}\binom{h−k}{j−k} that
     PROOF.md omits (G2); the alternating sum.
     Absolute coefficient sums 5, 49, 31.
   - **Exact sweep**: event lines, slabs, y-cells, a lazy segment tree with range-add
     and range-minimum, integer units; the absolute expansion weight 184,231,386,320 <
     2⁵⁰. Scale: 86,299,918 slabs and 511,649,694,680 cells, counted by range queries,
     not enumerated.
   - **Why the floor/ceiling query is exact** (G4): event coordinates are integers, so a
     comparison with a rational projection endpoint equals a comparison with its floor
     or ceiling; the query range is exactly the open cells that meet the domain.
   - **Boundary lemma**: the unexpanded charge is a nonnegative sum of indicators of
     closed sets, hence upper semicontinuous; every centre is a limit of generic
     centres, so C ≥ Γ on event lines, tangencies and domain boundaries.
     The signed form is used only at generic points (G6).
   - **Fig II.9** envelope (with a one-dimensional semicontinuity inset); **Fig II.10**
     signed rectangles; **Fig II.11** charge field of row 11962.
8. **The Contradiction and the Strict Bound.** → `PROOF.md:79-83`.
   - Assembles Sections 3–7: no eleven parents of side A fit in [0, L₀]², so no eleven
     unit squares fit in side 31/8.
   - **Attainment lemma** (G3): eleven unit squares fit in side 4; parameters below that
     form a compact set; containment and disjoint interiors are closed conditions; the
     infimum is attained, so exclusion at 31/8 gives s(11) > 31/8. Set against I’s
     stated ≥ and its remark (I L598–599).
9. **What Was Verified, and What the Verification Means.**
   - Obligation → evidence table, III’s form: human lemma; source checkers (Python,
     JavaScript); this project’s native branch and bound and controls.
   - Γ is purely computational; no human-readable reason explains why every core reaches
     0.99996.
   - The two source checkers are one method with two code lineages
     (ATTRIBUTION.md:14–15); the register counts them as one.
     The native verifier is the method-distinct decision: an interval branch and bound
     that certifies a lower bound ≥ Γ on every row, not minima.
   - T-059 (wand125’s checker) reproduces all 12,028 exact row minima with replayed
     witnesses; it is an audit of the source’s row-scan claim, not a new proof.
   - The JavaScript source is not bundled; `prepare_secondary.py` reconstructs it from
     hash-pinned upstream bytes.
   - The source’s boundary controls (14 rows, 5,586 centres) never reach the three tight
     rows: their minimum is 1.000047518. The audit’s polygon-clipping control does cover
     row 11962 (audit L280–291).
   - How the certificate was found is not in the source and is not claimed.
   - V3/C3/S5; `think-yf6t`.
   - **Fig II.12** per-row minima.
10. **Bridge to Paper III.** One paragraph, register facts only: T-060 closed the case
    with different machinery.
    - When 2k > m, a core containing k of m sites meets the hull of every k of them (two
      k-subsets of an m-set intersect), so it receives III’s median-type charge on the
      same sites, also of budget w. III’s charge pays more cores for the same price;
      2-of-3 and 3-of-5 are such cases; 2-of-5 (budget 2w) has no counterpart in III.
    - II’s Γ and M play the roles of III’s Γ_i and b.
    - II folds to [0, π/4]; III does not, because its cover is only half-turn symmetric.
    - III’s rows are also closed angle intervals.

Appendices: **A** certificate schema and family census; **B** coefficient tables for
2-of-3, 2-of-5, 3-of-5; **C** reproduction (commands; recorded runtimes 9.5 and 7.6
minutes on the source’s machine, 1,501 s and 1,790 s here; evidence files; the warning
that `verify_threshold_algebra.py` rewrites the committed `threshold-algebra.json`);
**D** series glossary (§10, rendered from the term registries).
Then **Sources and Verification Record** and **Version History**.

### 5.3 Concept Spine

Every term, symbol and lemma of II in definition order.
II’s term registry (§9.4) is seeded from this table.
Nothing is used before its row except in Sections 0–2 with a forward marker.

| # | Concept | Section | Depends on |
| --- | --- | --- | --- |
| 1 | unit square, packing (disjoint interiors, contact allowed), container | 1 | — |
| 2 | s(11); orientation mod π/2 | 1 | 1 |
| 3 | Theorem s(11) > 31/8; T; bound gap; bound ladder | 1 | 2 |
| 4 | the three changes (named only, forward-linked) | 1 | 3 |
| 5 | inherited / new data / new (credit labels); k-of-m charge and the inequality, informal and forward-marked | 2 | 4 |
| 6 | site; point charge (I’s atom), weight | 3 | 1 |
| 7 | core (closed, strictly inside a packed square); capture | 3 | 1, 6 |
| 8 | charge C(Q); mass as the point-only case | 3 | 6, 7 |
| 9 | k-of-m charge (S, k, w), m = \|S\| | 3 | 6, 7 |
| 10 | disjoint cores; Budget lemma rk ≤ m; budget w⌊m/k⌋; budgets add over shared sites | 3 | 7, 9 |
| 11 | why k-of-m pays; no saving when k divides m | 3 | 8, 10 |
| 12 | parent, parent side A, container side L₀ | 4 | 1 |
| 13 | Scaling lemma L₀/A = 31/8 | 4 | 2, 12 |
| 14 | assigned core of a parent (forward link to Section 6) | 4 | 7, 12 |
| 15 | M (sum of budgets), Γ (least assigned charge), the inequality 11Γ > M | 4 | 8, 10, 14 |
| 16 | **D**₄, orbit, **D**₄-invariant certificate | 5 | 6, 9 |
| 17 | families; site system; physical feature | 5 | 9, 16 |
| 18 | half-angle t; rational cos and sin; parent angle φ | 6 | 2 |
| 19 | Folding lemma | 6 | 2, 16 |
| 20 | row (a, b, t, B); catalogue | 6 | 12, 14, 18 |
| 21 | mismatch d; Strict-core lemma; margin; disjointness | 6 | 20 |
| 22 | legal centre domain; Envelope lemma; inset ρ | 7 | 12, 20 |
| 23 | core frame; capture rectangle; captured set = intersection | 7 | 7, 20 |
| 24 | Signed-expansion lemma; binomial identity | 7 | 9, 23 |
| 25 | event line, slab, y-cell, generic centre | 7 | 23 |
| 26 | exact sweep; 2⁵⁰ bound; exact floor/ceiling query | 7 | 24, 25 |
| 27 | upper semicontinuity; Boundary lemma; row minimum ≥ Γ | 7 | 8, 15, 26 |
| 28 | compactness; Attainment lemma; strict bound | 8 | 13, 15, 21, 27 |
| 29 | receipt, replay, method-distinct decision, rungs (recap with link); native branch and bound; T-059 | 9 | 26 |
| 30 | III’s median charge relative to k-of-m | 10 | 10 |

### 5.4 Gaps in the Source That II Writes Out

The audit has no numbered gap list; these numbers are this plan’s.

| # | Gap | Section | Prior statement |
| --- | --- | --- | --- |
| G1 | Folding each parent separately (PROOF.md:43, one sentence) | 6, by recap of I | I L572–586 (point case) |
| G2 | The binomial identity behind the first difference (PROOF.md:59–63) | 7 | Audit L106–108 |
| G3 | Compactness and attainment (PROOF.md:83, two sentences) | 8 | Audit “Arithmetic and boundary points” |
| G4 | Why the floor/ceiling query is exact (code only, `exact_mixed.py`:85) | 7 | Audit L177–181 |
| G5 | Endpoint monotonicity over a row (PROOF.md:49) and the envelope union (PROOF.md:51) | 6, 7 | Audit L132–135 |
| G6 | The boundary argument, with a picture (PROOF.md:73–77) | 7 | — |

That Γ is computational only is a limit, not a gap; Section 9 states it.

## 6. Figure System

### 6.1 Series Rules

Added to `paper-design.md` “Figures”:

- **One stroke and colour role per object** in II and III: container, neutral outline;
  parent, filled square; core, dashed inner square; point charge, dot with area
  proportional to weight (I’s convention); k-of-m charge, thin hull through its m sites
  with a `k/m` badge; centre domain, hatched.
  The roles live in `devtools/paper_figures.py`, with fixed inks (III draws in fixed ink
  on a light ground,
  `test_a_diagram_drawn_in_fixed_ink_keeps_a_light_ground_on_the_dark_theme`) and the
  `_svg`, `_text`, `_polygon` helpers III’s three figure modules each copy today.
  I’s canvas figures (`certificate.js`) keep their palette.
- **The series bound ladder** (`paper_figures.bound_ladder(highlight=…)`): rungs
  Stromquist (T-010), T-018, T-025, T-026, T-033, T-037 with T-061, T-060 with Trump;
  evenly spaced and labelled with values from `results.yaml` headlines, with no linear
  axis (on a linear axis T-037 to T is 0.0021 of the range and T-037 to T-061 is 3.9 ×
  10⁻⁹). It appears as Fig II.2 and in III’s lineage section.
- **Static SVG from hash-pinned data.** Every caption number comes from
  `caption_facts()`. Labels use only glyphs the shipped face has
  (`tests/test_site_glyphs.py`; 14 of III’s 21 labels once failed, adversarial review
  §3.4); Γ, L₀, ≤ and subscripts are typeset in the caption otherwise.
  Figures fit 390 px without horizontal scrolling (new for II).
- **A paper opens on its object.** I and III open on the Trump packing; II opens on Fig
  II.1. This amends “Both papers open on a packing” in `paper-design.md`.

### 6.2 Paper II Figures

| Fig | Shows | Data source | Feasibility | Bound by test to | Priority |
| --- | --- | --- | --- | --- | --- |
| II.1 | What changed T-026 → T-037: families and point share (T-026: 584 point atoms, 320 2-of-3, points 79% of budget; T-037: four families, points 20%); containment (unit square with core B = 249507/250000 on a net direction, against parent A with a row core); angle coverage (T-026’s 1,440-step net against 12,028 rows) | `packing/cases/n11_threshold_certificate/certificate-191-50-net1440.json`; `global-certificate.json` | Counts only; no new computation | counts, shares, A, B, row count; both certificate hashes | must |
| II.2 | Series bound ladder, T-037 highlighted | `results.yaml` | Shared generator | headline values and ids | must |
| II.3 | Roadmap | certificate and evidence counts | Schematic | 12,028; 5,284; 11Γ; M | should |
| II.4 | One k-of-m charge: orbit 72’s five sites, a core holding three (paid), a disjoint core holding two (unpaid); inset: point weights w/3 on three sites against one 2-of-3 charge | certificate | Core placement found by hand and checked exactly with `Fraction` (milliseconds) | weight 0.067038144; capture checked exactly | must |
| II.5 | Budget bars: four families stacked to M against 11Γ, zoom inset on the surplus (10⁻⁵ of M) | certificate | Arithmetic | family budgets sum to M; surplus 107,864 | must |
| II.6 | (a) site map, 5,284 sites by role; (b) largest 2-of-3 (orbit 206, w = 0.019257662, one site 0.054 from the centre); (c) largest 2-of-5 (orbit 130, w = 0.014211519) with two disjoint paid cores | certificate | Exact placement as II.4 | 496, 144, 4,788; weights; captures | must |
| II.7 | Parent, concentric core, mismatch d, margin (exaggerated; the real margin is 10⁻¹² and the caption says so) | rows 0 and 11962 | Row data only | A, B, d at row endpoints | must |
| II.8 | Catalogue strip: row density over 0°–45°; the three rows below 1 marked: 11962 (44.58°–44.59°, Γ = 0.999962528) and 8844–8845 (30.63°–30.65°, 0.999970079) | `entries`; `evidence/portable/python.json` | Data only | rows and minima | should |
| II.9 | Envelope polygon in the core frame, with a 1-D semicontinuity inset | row geometry | Data only | ρ and L₀/2 − ρ | should |
| II.10 | Signed rectangles of one real 2-of-3 charge: +1 on pairs, −2 on the triple | certificate, one row | Rectangles rebuilt with `Fraction` as `exact_mixed.geometry` builds them | coefficients from \binom{j−1}{k−1} | must |
| II.11 | Charge field of row 11962 with its minimiser | certificate; exact witness from the T-059 journal (row 11962, minimum 999962528, `witness_replayed`) | Raster of direct charge evaluation (about 400² centres × 5,284 sites, numpy, seconds); the witness’s coordinate frame must be established first | exact charge at the witness = 999962528 | should |
| II.12 | Per-row minimum against parent angle, Γ, the three tight rows, the native lower bounds as a band | `python.json` rows; native row journal | Data only. A JavaScript per-row series cannot be drawn: its evidence holds histograms and per-range records only | histogram equals the source’s (11 values; 11,981 rows at 1.000047518); every native lower bound ≥ Γ | must |

Twelve figures, numbered in reading order as §5.2 places them.

Captions state what an interval method certifies: of the native rows, 10,541 have a
certified lower bound below 1 and 384 equal the Python minimum, so II.12 draws a band,
not a second minimum series.

**Implementation constraint:** Load the certificate through
`sqpack.fractional.parent_core.load_kleddamag_parent_core`. Never import the archived
`exact_mixed.py`: it imports numba through `integer_sweep.py`, which is not a project
dependency, and the archive is not an execution cache.

## 7. Changes to Papers I and III

### 7.1 Content Changes

| Paper | Change |
| --- | --- |
| I | The frontier update (renderer `render_n11_lower_bounds_explainer.py`, about L2332–2341) names T-037 and links II, and links III’s page, not only the review record |
| I | Further Reading gains “The n = 11 series”; the `[^other-results]` footnote (Kleddamag at n = 17) is unchanged |
| I | Series strip (§9.2). Fig 3 unchanged (owner default) |
| I | `EXPLAINER_HISTORY` v0.4.4 and `EXPLAINER_REVISED`; `EXPECTED_PAGE_COUNT` in `render_n11_lower_bounds_explainer_pdf.py` if the PDF grows |
| III | `[earlier]` (L1254) and `[^lineage]` (L1159) point at Paper I’s page, not the site root |
| III | Provenance antecedents (L22–25) and the lineage section (L133–155) cite II, with the three changes in §5.2 Section 1’s words; “wand125’s row-minimum check” (L154) links T-059 and II |
| III | “Charge Budgets” (L466 on) cites II and states the 2k > m relation in one sentence |
| III | The §3 renames: S → L₀; B → (191/50)/U; quarter-turn Q → rot; q_i → Γ_i (text and Fig 7 labels); D_4 → **D**₄; “feature” → “charge”; “threshold one” → “a required charge of one” |
| III | The ladder in the lineage section; adding it renumbers III’s Figures 3–11 and their prose references |
| III | The §7.2 fixes; `OPTIMALITY_REVIEW_HISTORY` v0.1.5 and `OPTIMALITY_REVIEW_REVISED` |
| Both | Series strip “Part N of 3” with the other two titles |

### 7.2 Paper III Define-Before-Use Audit

This audit starts from the adversarial review’s §3.2
(`review-2026-10-03-n11-optimality-paper-adversarial.md`), rerun on v0.1.4. Already
fixed there: s(11) (about L48), orientation mod π/2, update and step, live row and
proposal, predecessor and self-containment, common prior, node, leaf and root round,
tied, available. Line numbers are of the v0.1.4 article.

| Term | First use | Defined | Change |
| --- | --- | --- | --- |
| s(11) | L25 (preamble) | about L48 | Preamble: “a lower bound of 31/8” |
| threshold (certificate) | L22 (link text), L141 | never | Lineage gloss: “charges a core for holding at least k of m sites (Paper II)” |
| composer | L82 | L988 | One clause at L82 |
| charge | L148 | L469–476, implicitly | Define in the lineage paragraph (L135–140) |
| cell | L225 (frames table) | L243 | Move the frames table after the Center-cover lemma |
| case | L118 (Fig 2 caption) | L298 | Gloss in the caption, or “pattern” until L298 |
| branch | L227 (capture split); L793 (128 linear systems) | L683, L793 | “branch” for the capture tree; “contact branch” for the linear systems |
| receipt | L268 (Fig 3 link text) | L986 | Define in “The Result” where the components are introduced |
| capacity | L276 (Fig 4 caption, a cell) | L501 (a charge) | Fig 4: “holds at most one centre”; capacity is the charge’s |
| seed | L346 | L450 | Move the definition ahead of the invariant paragraph |
| cut | L350 | never | Define once: a closed half-plane condition on a centre that a branch assumes |
| common-core inclusion; compression | L405–406 (Fig 6 caption) | L444, L446 | Move Fig 6 after “Keeping everything else”, or mark “defined below” |
| residual | L189 (floating-point), L349 (row) | L349 | L189 → “floating-point error” |
| label | L256 | never formally | One clause: the label of a centre is the index of a cell containing it |
| feature (charge) | L506–507 | never | “charge” (§3), defined at L506; “separation feature” (L772) keeps its name |
| site | L241 (cover), L476 (charge) | L241 | “cover site”, “charge site” |
| threshold one | L512 | — | “a required charge of one in each of cells 1 and 2” |
| field (three senses) | L183, L217, L469 | partial | Keep “number field”; “file coordinates” at L217; define “charge field” at L469 |
| ban | L613 (Fig 8 caption) | L628 | Move the ban paragraph ahead of Figure 8 |
| inclusion checker | L714 | never | “the pose-inclusion check”, with what it proves |
| working box | L740 | L740; “analytic working box” L1076 | One name |
| gap | L145 | — | “bound gap” |
| rung, ladder | L958 | never in the text | One clause and an `epistemics.md` link |
| wall contact | L196 | never | One-clause gloss |
| Q, S, B, q_i, D_4 | L875, L79, L218, L471, L603 | — | §3 renames |

Moves of existing text: the frames table, the receipt definition, the ban paragraph, Fig
6 and the seed sentence.
None changes a claim, receipt or rung.

## 8. Series Presentation and Reference Inventory

**Titles and one-liners** (title case on the page, sentence case on cards):

| Part | Title | One line (cards, README) |
| --- | --- | --- |
| I | New Lower Bounds for Square Packing for n = 11 (the owner’s, unchanged) | How weighted points and 2-of-3 threshold atoms prove T-018, T-025 and T-026, s(11) ≥ 3.8264…, with interactive figures. |
| II | A Review of the Certified Lower Bound s(11) > 31/8 for 11 Squares | Explains Kleddamag’s proof that s(11) > 31/8 (T-037): five-site k-of-m charges, threshold charges on shrunken parents with strict cores, and a re-optimised certificate over 12,028 angle rows. |
| III | A Review of the Optimality Proof of the Trump Packing of 11 Squares (unchanged) | Explains Ahmed’s proof that Trump’s packing is optimal, s(11) = 3.8770835… (T-060): construction, case exclusions, capture and local isolation. |

**Inventory** of every place that lists, links or describes the papers (found by `git
grep` of both slugs and the paper constants):

| Place | Holds | Change |
| --- | --- | --- |
| `README.md` L60–69 | Papers paragraph: III, then the explainer | Three parts in order, one-liners, page/PDF/source links |
| `SYNOPSIS.md` about L1518–1530 | “Dedicated optimality paper” paragraph | Name the series; add II |
| `SYNOPSIS.md` T-037 narrative (about L355–366) | T-037 | Link II. L362 claims “C4” for T-037 where the register holds V3/C3: report separately as a defect, not fixed here |
| `TUTORIAL.md` L137 | Link to I’s `#proof-of-the-new-lower-bound` | Add II and III after it |
| `TUTORIAL.md` §10 (L1437 on) | Notation card | Add A, Γ, M, the row (a, b, t, B), or mark them local in II |
| `overview_sections.py` `OPTIMALITY_PAPER`, `LOWER_BOUNDS_PAPER`, `PAPERS` (L1503–1548) | Papers page cards, labels, order comment | Add II; order I, II, III; labels “Part I/II/III”; one-liners |
| `overview_sections.py` `PAGES` (L1587 on), `SECTION_CARD_LINES` (L240) | Home cards | Three paper cards in order; `(1, 3, 2)` |
| `render_overview.py` `PAPERS_DESCRIPTION` (L146) | Papers page meta | Mention the n = 11 series |
| `render_overview.py` slug constants, `paper_path`, `SITE_PAGES` (L199–232); heads and forwarder previews | Slugs and pages | Add II (§9.1). `MOVED_PAGES`: no change |
| `templates/papers-article.md` L10–15 | Papers intro | Series lead (Owner Decisions) |
| `templates/overview-article.md` L24 | “New lower bounds” link to I (the owner’s words) | No change without the owner |
| III article L22–25, L133–155, L466 on, L1159, L1254 | Antecedents, lineage, charges, links | §7.1 |
| I article Further Reading (L791 on); renderer frontier update | Forward links | §7.1 |
| `packing/frontier/n-011.md` (T-037 and T-060 narrative, about L197–270) | Case record | One line: “Explained in Papers I, II and III”, with links |
| `packing/frontier/results.yaml` T-037 (L3212) | Register | Dated note when II publishes, as T-060 has; no schema change |
| `development.md` “Publishing the Explainer” (L1009 on; “The site’s two papers”, L1018, L1102) | Build and serve | Three papers; II’s build, outputs and Pages job |
| `conventions.md` §2 Naming (slug examples L156–161) | Slugs | Add `n11-threshold-bound-review` |
| `packing/campaign/result-import.md` §Stage 6 | Model paper is III | Optional: “the n = 11 series” |
| `templates/paper-design.md` “The Papers’ Front” (L2437 on), “Figures” (L2521 on) | “Both papers” | “Each paper”; series strip; figure roles; opening-figure rule; define-before-use rule |
| `docs/project/document-map.yaml`; `SYNOPSIS.md` Document Map | Plans and reviews | Enter this plan and II’s reviews |

## 9. Infrastructure

Paper II is modelled on `render_n11_optimality_review.py`, not on I’s renderer.

### 9.1 One Paper Registry and New Files

Replace the hard-coded pairs with one record list in `render_overview.py`: a `PAPERS`
tuple in reading order of `(slug, module, label, part)`. `SITE_PAGES`,
`paper_structure`, `pages_scope`, `preview_site`, `check_published_site` and the
overview cards read it, so a new paper is one entry plus its renderer.

New files (in `packing/devtools/` unless noted):

- `templates/n11-threshold-bound-review-article.md`, `-shell.html`, `.css`,
  `-terms.yaml`; `templates/n11-series-terms.yaml`.
- `render_n11_threshold_bound_review.py`: `TITLE`, `HERO_TITLE`, `FRONT`, `FIGURE_KEYS`,
  `page_meta`, `link_revision`; `RENDER_INPUTS` (certificate, evidence files, T-026
  certificate, T-059 journal, native row journal, `sqpack/fractional/parent_core.py`);
  `ARCHIVED_CITATION_SOURCES` for the archived Kleddamag files it links.
- `n11_threshold_figures.py` (`render_figures()`, `caption_facts()`),
  `paper_figures.py`, `paper_terms.py`.
- Tests: `tests/test_render_n11_threshold_bound_review.py`,
  `tests/test_n11_threshold_figures.py`, `tests/test_paper_figures.py`,
  `tests/test_paper_terms.py`.
- `packing/src/sqpack/release.py`: `THRESHOLD_REVIEW_HISTORY`, `_STATUS`, `_VERSION`,
  `_EDITION`, `_REVISED`, and `THRESHOLD_PROOF_PUBLISHED = "September 22, 2026"`, on the
  `OPTIMALITY_REVIEW_*` pattern.

Places that assume two papers:

| Place | Change |
| --- | --- |
| `paper_structure.py` `PAPERS` (L49), `compare` (pairwise) | N papers, each compared with I |
| `tests/test_paper_structure.py` | All papers against the reference |
| `render_overview.py`, `overview_sections.py` | §8 |
| `artifact_dates.py` | II’s article, dates rows and PDF |
| `preview_site.py` | Build step and `--skip` name |
| `pages_scope.py` | II’s scope from its `RENDER_INPUTS` |
| `.github/workflows/pages.yml` | Paths, scope outputs, II’s job and `-unchanged` job |
| `gate-budgets.yaml` (entries at L1582, L1678, L1696) | II’s job and `-unchanged` budgets |
| `check_published_site.py` | II’s page, Markdown, PDF; cross-paper links |
| `measure_site_pages.py`, `measure_release_assets.py` | II in usage, defaults and build steps |
| `repo_links.py` | Docstring: II pins citations as III does |
| `tests/test_colour_tokens.py`, `test_site_glyphs.py`, `test_site_head.py`, `test_site_preview_checks.py`, `test_overview.py`, `test_pages_scope.py`, `test_pages_workflow.py`, `test_artifact_dates.py`, `test_check_published_site.py` | II’s entries; glyph and front checks over all papers at 1280 and 390 px |
| `suite-file-costs.json` | Record II’s tests (`python -m devtools.suite_files record`) |

### 9.2 Series Strip and Cross-Paper Links

- **Series strip:** A `series` field on `paper_front.PaperFront` (series name, parts,
  this part’s index), rendered on the page, the Markdown edition and the PDF. It is a
  new form axis, so `paper_structure.CREDIT_KINDS`, `measure_site_pages credits` and
  `test_site_glyphs` learn it in the same change (S2).
- **Cross-paper links:** III’s renderer pins every `./` or `../` link to a repository
  blob (`RELATIVE_LINK`, `_repository_links`), and
  `test_relative_link_must_resolve_to_a_repo_file` refuses a sibling paper page.
  A link to another paper is therefore a placeholder `{{PAPER:<slug>#<anchor>}}`, filled
  with the page-relative `<slug>.html#anchor` from `render_overview.paper_path` and with
  the absolute site address in the Markdown edition.
  A test checks every anchor exists among the target paper’s heading ids.
  I’s data-dependent headings (for example “From a Continuum of Angles to
  {{N_DIRECTIONS}}”) are not link targets.
- In one PR, II is not live when the links are checked: `preview_site --serve` builds
  all three papers and `check_published_site --site <local>` runs against that build.

### 9.3 Tests and Gates for Paper II

| Gate | Model in III |
| --- | --- |
| Every figure slot used once; every caption fact used | `test_a_caption_fact_the_article_does_not_use_is_refused` |
| Each figure refuses a changed input hash; labels bound to data (II.11 witness charge; II.5 sums to M; II.8 rows) | `tests/test_n11_optimality_figures.py`, `test_*_mechanism_figures.py` |
| Every figure input in `RENDER_INPUTS` | `test_new_figure_dependencies_are_declared_to_publication_scope` |
| Page offline, figures present | `test_rendered_page_is_offline_and_contains_proof_figures` |
| Local citations pinned; archived files resolve | `test_local_citation_is_pinned`, `test_relative_link_must_resolve_to_a_repo_file` |
| Front in the shared form | `test_the_front_is_the_shared_components_in_the_owners_form`, `test_paper_structure.py` |
| PDF math and print geometry | `test_pdf_refuses_a_math_host_without_rendered_katex`, `test_a_print_can_ask_for_every_formula_at_once` |
| Colour tokens; glyphs and 390 px centring | `check_colour_tokens`, `test_site_glyphs` |
| Terms defined before use; cross-paper anchors exist | new, §9.4 |
| Register consistency: every result number in II is in the register | new: reads T-037’s `claim` and `composition` and the figure facts |

### 9.4 Define-Before-Use Gate

**Registry:** `templates/<slug>-terms.yaml`, one per paper; II’s seeded from §5.3, III’s
from §7.2. Fields: `term`; `uses` (a prose regex, or a TeX regex for a symbol);
`defined_by` (exact substring of the defining sentence); `anchor` (heading id of the
defining section); `requires`; `forward` (allowed earlier uses, each an exact substring
with a reason: `roadmap`, `heading`, `link-to-definition`).

**Scanner:** `paper_terms.py` walks the rendered HTML in document order: headings,
prose, tables, figcaptions.
It skips credits, `<svg>`, `<script>`, navigation and footnotes, and matches math on the
TeX source the page carries.
Running on the rendered page means placeholders are filled and anchors are the generated
ones.

**Rules** (`tests/test_paper_terms.py`, parametrised over papers):

1. Each `defined_by` occurs once, inside the section named by `anchor`.
2. No match of `uses` precedes the definition except at a declared `forward` substring.
3. Each prerequisite is registered and defined earlier.
4. Every bold run in body prose is some term’s definition (figure labels exempt), so a
   new definition must enter the registry.
5. Optional per paper: banned bare forms (bare “gap”, bare “field” in III).
6. Cross-paper: `n11-series-terms.yaml` names each shared concept’s owner and anchor.
   A nonowner’s first use sits in a paragraph linking the owner (principle 2). A symbol
   defined in two papers with different meanings fails unless §3 lists the clash (A, ρ,
   C(Q)/C_j are listed).
   Runs in `preview_site` or `check_published_site`, which hold all papers.

**Feasibility:** III’s test module already renders the page (fixture `rendered`), and
the scan is cheap. Paper I is advisory at first: its page needs the `--prepare-math`
pipeline and stamps figures per certificate.
Expected first failures on III are §7.2’s rows; the gate lands with III’s registry and
those fixes together.

## 10. Series Glossary

Rendered from the term registries into each paper’s glossary appendix.
First version:

| Term | Owner | Meaning |
| --- | --- | --- |
| s(n) | I | The least side of a square holding n unit squares with disjoint interiors |
| Container side L₀ | I | The side under test in a certificate |
| Core | I | A smaller closed square strictly inside a packed square (or parent) |
| Site | II | A position in the container |
| Point charge (I: atom) | I | A site with a nonnegative weight, paid to any core containing it |
| k-of-m charge (I: threshold atom) | I / II | Pays w to a core capturing at least k of its m sites; budget w⌊m/k⌋ |
| Charge C(Q) | II | The total a core receives from point and k-of-m charges |
| Budget, M | I / II | The most the charges can pay across pairwise disjoint cores; M is its total |
| Γ | II | The certified minimum charge of an assigned core |
| Mass μ | I | The point-only charge of a region |
| Event cell | I | A region of centres on which the captured set is constant |
| Net, half-tangent | I | Finitely many directions 2 arctan t with t rational |
| Parent | II | A side-A square in [0, L₀]²; parents in L₀ stand for unit squares in L₀/A |
| Row | II | An interval of parent half-angles with its assigned core (t, B) |
| Envelope | II | The union of legal centre domains over a row |
| Signed expansion | II | The rectangle-sum form of a k-of-m indicator |
| Upper semicontinuity | II | The property that extends Γ from generic centres to boundaries |
| Cap U | III | A rational side slightly above T used for the global computations |
| Cell, mask, case | III | A Voronoi region of the centre cover; an 11-subset of cells; a half-turn class of masks |
| Pose, owner, owned hull | III | A square’s centre and angle; the square assigned to a cell; a guaranteed interior |
| Field certificate, capacity | III | A charge certificate on occupied cells; the most disjoint cores one charge pays |
| Capture, node, leaf | III | Enclosure of surviving poses; the tree of checked states |
| Local isolation | III | No nonzero displacement in the checked rectangle is feasible |
| Receipt | III | A checked execution’s verdict, input hashes, command and replay script |

## 11. Slices

All slices land in one pull request, as commits in this order; CI runs on the PR.

| Slice | Content | Exit | Depends on |
| --- | --- | --- | --- |
| S1 Series spec | This plan; §3, §6.1, the define-before-use and opening-figure rules in `paper-design.md`; beads for S2–S8 | Beads open and claimed; `tbd sync` | — |
| S2 Infrastructure | One paper registry (§9.1); series strip and `{{PAPER:…}}` links (§9.2); `paper_figures.py` with III’s helpers moved in | I and III render byte-identical except the strip; `paper_structure` shows no form difference; `--edit` tier passes | S1 |
| S3 Term gate and III | `paper_terms.py`; III’s registry; §7.2 fixes and moves; §3 renames in III | `test_paper_terms` passes for III with no allowances; III renders | S2 |
| S4a Figure contract | II’s `FIGURE_KEYS` and caption-fact names (§6.2) frozen in a renderer stub | Stub renders with placeholder figures | S2 |
| S4b Figures | `n11_threshold_figures.py`, must-have first | §9.3 figure gates; glyph and 390 px checks | S4a |
| S4c Article | II to §5.2, each implication cited to PROOF.md lines plus a checker or receipt; II’s registry from §5.3 | `test_paper_terms` passes for II; register-consistency test passes | S4a, merges with S4b |
| S5 II in the build | II’s Pages job, scope and gate budgets; Draft v0.1.0 | PR’s Pages build renders II’s page, Markdown and PDF; `check_published_site --site` passes on `preview_site` | S4b, S4c |
| S6 I and III content | §7.1; I v0.4.4, III v0.1.5; ladder in III | Cross-paper anchor test passes; I’s and III’s PDF checks pass | S3, S5 |
| S7 Series presentation and docs | §8 inventory; `development.md`, `conventions.md`, `paper-design.md` | Every §8 row done; `test_overview` and card-centring checks pass | S5 |
| S8 Review | W2 exposition review of II (Stage 6); adversarial review in III’s format with a credit check against §4; cross-paper pass over notation, links, glossary and figure roles; close `think-4lye` in step with II’s Section 2 and add the lineage II states to T-037’s register note | Findings dispositioned and recorded in II’s history; full checkpoint and all PR CI jobs green | S6, S7 |

Parallelism: S3 beside S4; S4b and S4c after S4a; S6 and S7 after S5.

## Appendix: Review Record

Two revisions of the first draft were merged: “Fable” (fact-checking, credit, spine,
glossary) and “Opus” (implementation, inventory, reader experience, III audit, gate).
Where they agreed, the union was taken.
Conflicts:

| # | Question | Fable | Opus | Deciding source | Outcome |
| --- | --- | --- | --- | --- | --- |
| 1 | III’s file scale B | B → β | Drop B, write (191/50)/U | `TUTORIAL.md` L1483 uses β (field element); III uses B only at L218, L226, L883 | Opus: drop B |
| 2 | III’s quarter-turn Q | Q → rot | Q → R_{π/2}, and R → r_max | “rot” occurs nowhere in I, III or TUTORIAL; R_{π/2} forces renaming R at L814, L848, L852, L856 | Fable: rot (two lines change) |
| 3 | III’s charge floor q_i | q_i → κ_i | q_i → Γ_i | `TUTORIAL.md` L1031–1050, L1488 use κ_j; Γ occurs nowhere in I, III or TUTORIAL | Opus: Γ_i, mirroring II’s Γ |
| 4 | III’s budget b | keep | keep | M_j at III L829 | Keep b |
| 5 | III’s c, s | keep constants | → \cos a, \sin a | III L160–163: constants, not functions; renaming touches Appendix A throughout | Fable: keep |
| 6 | Gap G4, the floor/ceiling query | conservative superset | exact | `exact_mixed.py` L85 (`bisect_right(ye, bn//bd)−1`, `bisect_left(ye, ceil)`) on integer event coordinates; audit L177–181 | Opus: exact. A superset would also be sound, but it is not what the code computes |
| 7 | Half-angle symbols | t parent, t̂ row core | φ parent angle, t row core | I L250, L423: φ is the packed square’s angle, θ_k = 2 arctan t_k the net direction; source PROOF.md:43 uses t for the core | Opus |
| 8 | Charge or atom/feature | “threshold feature”, charge as quantity | “k-of-m charge or feature” | III L476, L501, L506 and PROOF.md:33–39 say charge; I says atom | “Charge” (owner default); III’s “feature” → “charge” |
| 9 | Credit: parent side, cores, centre restriction | R012 (T-032) | R038 | `results.yaml` L2592–2597; Guzhou-NOTICE.md:9; Mira-ATTRIBUTION.md:40–45 | First registered in R012; R038 adds the smaller rational side and strict-containment transfer; centre restriction’s antecedent is this project’s note; “inherited through the line” |
| 10 | Credit: adaptive catalogue | Kleddamag’s own builder (PROOF.md L85; T-038) | Mira’s continuation | Mira-ATTRIBUTION.md:29–32 records adaptive refinement, maximal safe cores, parent envelopes; PROOF.md:85 says only that catalogue construction supplies proposals | Inherited through the line; the 12,028 rows are T-037’s data |
| 11 | Credit: k-of-m and signed sweep | inherited (I, T-025) | inherited (I, `threshold.py`) | I L609–631; review-2026-09-09 F6; audit Finding 4 | Agree; new are the 2-of-5/3-of-5 families in a certificate, the re-optimised data, and thresholds on parents at n = 11 (T-038 is 2-of-3 only) |
| 12 | Line references in ATTRIBUTION.md | L177–186 | — | The file has 46 lines | Corrected to L13–22 |
| 13 | Section order of II | Result → What Is New → Points to Thresholds → Charges → Inequality → … (11) | Result with changes → Points to k-of-m → Inequality → Charges → … (9) | User requirement: innovations up front, k-of-m first, define before use | Result (three changes) → What Is New → k-of-m charges → parents and inequality → census → … (10) |
| 14 | Figure list | 15 figures | 13 figures | III has 11; Opus’s data checks | 12 figures; site map merged into the gallery; pigeonhole folded into II.4 |
| 15 | Fig II.11 (charge field) | stretch: no minimiser recorded | should: T-059 has witnesses | T-059 journal row 11962: minimum 999962528, exact witness, `witness_replayed` | Should-have |
| 16 | Per-row figure | Python, JavaScript, native histogram | Python minima with native band | Native journal: 10,541 lower bounds below 1e9, 384 equal Python’s; JS evidence has histograms only | Opus |
| 17 | Slices | S1–S7 sequential | S1–S8, II live before links | One-PR requirement; `check_published_site --site` runs on a local build | S1–S8 inside one PR; link checks on `preview_site` |
| 18 | Title | user default | “A Review of the Threshold-Charge Lower Bound for 11 Squares” | `HERO_TITLE` precedent in I | Default kept with `.tex` hero treatment |
| 19 | Stage 6 reference | `result-import.md` L181 | L185 | Stage 6 is at L322 | Cited by section name |
| 20 | Bead ids | unprefixed | `think-` prefix, unchecked | `.tbd/config.yml` `id_prefix: think`; tbd sync branch: `think-ny2u`, `think-yf6t`, `think-4lye` exist and are open | Prefixed, verified |

Not verified: the word counts of I and III; that L₀, Γ and Γ_i labels pass the shipped
face (left to `test_site_glyphs`); the coordinate frame of T-059’s witnesses.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
