# Unit squares in a rectangle, small n: what is proved (2026-10-20)

Question: for n ≤ ~12 congruent unit squares, rotations allowed, in an a × b rectangle, what is known exactly?
Is the feasible region R_n = {(a, b) : n unit squares fit in a × b}, or its frontier H_n(w) = least height at
width w, characterised for any n ≥ 2?  Also: smallest-area or smallest-perimeter rectangles, strips of width w < 3,
formalisations, and whether the small s(n) proofs are stated for rectangles.

Labels: **[read]** = I read the primary source (section cited); [S] = secondhand (another note, an abstract, a
listing); [I] = my own inference or derivation, not stated in any source.  "Not found" means searched and not found,
not "does not exist".

Sources fetched this session (PDFs in the session scratchpad, not kept): Nagamochi EJC 12 (2005) #R37; Karakuş
arXiv:2609.37410v1; Yang arXiv:2608.13595v2; Kearney–Shiu EJC 9 (2002) #R14; Stromquist EJC 10 (2003) #R8 (grep
only); Friedman DS7 (current HTML, erich-friedman.github.io/papers/squares/squares.html); Friedman's Packing Center
index and "Squares in Dominoes" page; arXiv abstracts 2610.22622, 2610.28504, math/0412443, 2609.28791; chelokot's
square-packing-archive docs (local read-only snapshot e1e9ef5).  MathOverflow could not be fetched (crawler blocked),
so MO 396776 is known only through Yang's summary.

## 0. Summary

* **R_n is characterised in print for no n ≥ 2.**  No paper states the rectangle region even for n = 2.
* **n = 2 is easy and follows from a known proof [I].**  The proof of the two-square theorem in Yang's Appendix A
  (attributed there to Erdős) works verbatim in an A × B rectangle.  It gives **R_2 = {min(a, b) ≥ 1, max(a, b) ≥ 2}**,
  and more generally s₁ + s₂ ≤ max(A, B) for two squares of sides s₁, s₂ (§1.1).
* **n = 3 is partly determined, by Yang's G₃ [read] plus scaling [I].**  Every w × h box with w ≤ h is settled
  except the region 1.5 ≤ w < 2, max(w, 3 − w/2) ≤ h < 3 (§1.2).  The conjecture R_3 = {min ≥ 2} ∪ {max ≥ 3} is false (correction in §1.2): the true boundary, with a 45° piece,
  is already tabulated (constructions) in Friedman's Math Magic, June 2010 (§2 correction, 10-21).  Proved in Lean on 10-21
  (`rect3_iff`).
* **From n = 4 on, the frontier is not just the axis grid.**  Friedman's "Squares in Dominoes" page lists 4 unit
  squares in 1.930+ × 3.861+ (Stenlund, 2010) [read: listing only; packing not checked here].  So "width < 2 forces
  height ≥ n" is false at n = 4.  Similar tilted entries: n = 9, 11, 12, 13 at widths 2.47–2.98.
* **The only rectangle-general lower bounds are the integer-box ones.**
  * Karakuş Cor. 6.1 [read] (a correct proof): mn − 1 unit squares do not fit in an m′ × n′ box with m′ < m and n′ < n.
  * Nagamochi Thm 1 [read] is stronger, ν(a, b) < ab − Δ(a) − Δ(b) for real a, b ≥ 2, but its proof has a gap.
  * Both forbid only shrinking *both* sides.  Neither gives H_n(w) for w below an integer.
* **Smallest area is trivial** (the 1 × n strip has area n).  **Smallest perimeter**: nothing found for squares; the
  circle analogue is Lubachevsky–Graham (math/0412443).  Friedman's Packing Center has no squares-in-rectangles page.
  It has "Squares in Dominoes" (the 1:2 rectangle), with no proofs.
* **Strips:** there is no exact result for unit squares in a strip of width 1 ≤ w < 3 beyond n = 2, 3 above.  The
  "strip packing" literature (bin/strip packing with orthogonal placement) is a different problem.
* **Formalisations:** all of them are for square containers: chelokot (Lean/Bend: s(5), s(6), s(8), s(10), s(13), s(22),
  s(33), s(n²−1), s(n²−2)), the s(11) Lean projects, and our own `lean/`.  No rectangle-container theorem is formalised
  anywhere I found.  chelokot says explicitly that Nagamochi's rectangle theorem is *not* verified.
* **The small s(n) proofs (n = 2, 3, 5, 6, 7, 8, 10) are all stated for square containers.**  Their lemmas are local
  (a corner, a side strip, a triangle), so they adapt to rectangles, but nobody has written that down (§5).

## 1. Is R_n (equivalently H_n(w)) characterised?

Trivial facts [I]:
* R_1 = {a, b ≥ 1}: every unit square has width ≥ 1 in every direction.
* R_n ⊇ {⌊a⌋·⌊b⌋ ≥ n} (the axis grid).
* R_n is monotone (a superset of any feasible box is feasible) and symmetric in (a, b).

### 1.1 n = 2 (not stated anywhere; derivable in a few lines [I])

* Yang 2608.13595, Appendix A, Theorem 12 [read]: two interior-disjoint squares of sides a, b in the unit square have
  a + b ≤ 1.  Yang says the result "is attributed to Erdős in an early article in a Hungarian journal for
  secondary-school students" (via the erdosproblems.com #106 history notes) [S], and gives a self-contained
  reconstruction:
  * Lemma 13 (corner depth): a square of side s in the first quadrant contains a point z with z_x, z_y ≥ s.
  * Proof: take a separating line px + qy = t, normalised by reflections to p, q ≥ 0.  Lemma 13 on one square gives
    t ≥ a(p + q).  Lemma 13 on the other square, reflected through the centre, gives t ≤ (1 − b)(p + q).
* **Rectangle version [I].**  Run the same proof in [0, A] × [0, B].  The reflections x ↦ A − x and y ↦ B − y are
  symmetries of the box, and reflecting through the centre maps the box to itself.  This gives
  p(A − s₁ − s₂) + q(B − s₁ − s₂) ≥ 0 with p, q ≥ 0, p + q > 0, hence **s₁ + s₂ ≤ max(A, B)**.
  For unit squares: **R_2 = {min ≥ 1, max ≥ 2}**, so H_2(w) = 2 for 1 ≤ w < 2.
* The same fact also follows from Nagamochi Thm 1 at a = b = 2: ν(2, 2) < 4 − 1 − 1 = 2.  That is gap-tainted, and the
  separating-line proof is simpler.  DS7 Theorem 1's unavoidable point (1, 1) [read] does not transfer directly: in
  an a × b box with a, b < 2 the four corner applications of Lemma 1 give four different points.

### 1.2 n = 3: half done via Yang's G₃

* Yang Theorem 9 [read]: G₃(x) = max total side of three arbitrarily rotated, interior-disjoint squares in 1 × x:
  * x + ½ on [1, 3/2];
  * 2 on [3/2, 2];
  * x on [2, 3];
  * 3 for x ≥ 3.

  Theorem 1 (the "strip theorem"): three squares in [0, 1] × [0, H] with H ≥ 2 have total side ≤ H.  Theorem 9 also
  settles MO 396776 (three squares in 1 × 2 have total side ≤ 2) and Stanley's 2021 n = 3 question.  The extremal
  configurations use *unequal* squares, so for equal squares the result is only a necessary condition.
* **Consequences for three unit squares in w × h, 1 ≤ w ≤ h [I, by scaling: 3/w ≤ G₃(h/w)]:**
  * h ≥ 2w ⇒ need h ≥ 3.  This is sharp (stack of three).  **Exact on this region.**
  * 1.5w ≤ h ≤ 2w ⇒ need w ≥ 1.5.
  * w ≤ h ≤ 1.5w ⇒ need h + w/2 ≥ 3.  At h = w this recovers s(3) = 2.
  * **Left open: 1.5 ≤ w < 2, max(w, 3 − w/2) ≤ h < 3**, e.g. 1.9 × 2.9.  The natural conjecture is
    R_3 = {min ≥ 2} ∪ {max ≥ 3}.  Yang's Remark 8 [read] says H ≥ 2 is used only in Step 1 (pairwise sums > 1,
    automatic for equal sides > ½) and in Step 6.  For equal squares Step 6's inequality would need
    3 − h > C_α(w − 1), which is not automatic [I].  So the open region needs a new argument.  It is a cheap target
    for our point/segment certificate machinery. **Correction (main session, 10-20): this conjecture is false.**  (The counterexample family below is the piece
x + 2y = 4 + 2√2 of S_2 in Friedman's Math Magic, June 2010; we re-found it without knowing that.  Credit: Friedman's page.)  Two uprights at the ends of the long side and a 45° square in the gap between them, touching their inner corners and the far wall, fit three squares in w × h with w + h/2 = 2 + √2 (w short side, 2√2 ≤ h < 3), e.g. (1 + 2√2/3) × (2 + 2√2/3) ≈ 1.9428 × 2.9428, inside the open region (exact by hand: the diamond's L1 ball touches the corners (1,1), (1+g,1) and the wall; `search/rectfront/RECTFRONT.md`).  Conjectured boundary there: w ≥ 2 + √2 − h/2.
* Not found: any paper on three *equal* squares in a rectangle.

### 1.3 n ≥ 4

* **Not characterised anywhere; nothing found.**
* The frontier has tilted pieces from n = 4 on.  Friedman, "Squares in Dominoes" (erich-friedman.github.io/packing/
  squindom/, updated 10/18/26) [read; values only, packings not checked] lists the smallest known s × 2s box:
  * n = 4: s = 1.930+ (Stenlund 2010), i.e. 4 squares in 1.931 × 3.861, beating both 1 × 4 and 2 × 2 in that aspect;
  * n = 9: s = 2 + √2/3 ≈ 2.471 (vs. axis 2.5);
  * n = 11: 2.779+;
  * n = 12: 6(1 + √2)/5 ≈ 2.897 (Morandi);
  * n = 13: 2.976+ (Cantrell 2012);
  * n = 19: 3 + 1/√5;
  * entries up to n = 50 (Wolk, Gomes, 2026).

  Friedman labels n = 1–3, 5–8, 10, 14–18, … "Trivial", which refers to the packing, not a proof of optimality.
* **Which "trivial" domino entries are actually proved optimal [I, from the read sources]:**
  * n = 3, s = 3/2: by Yang, three equal squares of side t in 1 × 2 have 3t ≤ G₃(2) = 2.
  * n = 7, 8, s = 2: Karakuş Cor. 6.1 with (m, n) = (2, 4).
  * n = 17, 18, s = 3: (3, 6).
  * n = 31, 32, s = 4: (4, 8).
  * n = 49, 50, s = 5: (5, 10).
  * n = 6 (s = 2) only via Nagamochi (gap).
  * Not settled by anything found: n = 5 at s = 2, n = 10 at s = 5/2, n = 14–16, 20–21, ….
  * The n = 4, 9, 11, … entries have no lower bounds at all.

## 2. Smallest-area / smallest-perimeter rectangle for n unit squares

* **Area: trivial**, the minimum is n, attained by 1 × n (and by any a × b grid with ab = n) [I].
* **Perimeter: nothing found for squares.**  The lower bound is a + b ≥ 2√n, and the grid gives min{a + b : ab ≥ n,
  a, b ∈ ℤ}.  Whether tilting ever beats the grid's semi-perimeter is untouched in the literature.  It is an easy
  question to pose and a natural companion to H_n(w) [I].
  * Circle analogue: Lubachevsky–Graham, "Minimum perimeter rectangles that enclose congruent non-overlapping circles",
    math/0412443 [read: abstract]: computational, n ≤ 5000; aspect ratio → 1.
  * Companion min-area paper for circles, math/0405148 [S: search snippet].
* **Friedman's Packing Center** [read: index page fetched 2026-10-20]: there is no "Squares in Rectangles" page.
  * Rectangle-related pages: "Circles in Rectangles" (perimeter section), "Consecutive Rectangles in Similar Rectangles",
    "Animated Rectangles in Squares".
  * The 1:2 container appears as "… in Dominoes" (Squares in Dominoes, above).
  * This agrees with `notes/wishlist-literature-2026-10-03.md` §4 ("no squares-in-rectangles page").  The Dominoes page
    was not mentioned there; it is new here.
* Not found: a Friedman Math Magic problem on this. **Correction (10-21): wrong.** Math Magic, June 2010 (erich-friedman.github.io/mathmagic/0610.html) tabulates the boundaries of S_n = {s(x,y) ≤ n} for unit squares in rectangles, n ≤ 9 (solvers Morandi, Stenlund, Cantrell, Hosono).  S_2's boundary is x = 3, x + 2y = 4 + 2√2, y = 2: exactly R_3, wedge included (constructions, no proofs).  Found via wand125/square-packing `problems/rectangles/` (F_k edges, constructions only, lower bounds listed as not done).

## 3. Strips: n unit squares in width w, least height, and "how many fit in w × h"

* **1 ≤ w < 2:**
  * H_2(w) = 2 (§1.1).
  * H_3(w) = 3 for w ≤ 1.5, and for w ∈ [1.5, 2) open (§1.2).
  * H_4(1.931) ≤ 3.861 < 4 (Friedman's dominoes, n = 4).
  * No general theorem found.  The natural guess "width < 2 ⇒ at most ⌊h⌋ squares" is false at n = 4, h ≈ 3.86 [I,
    from the listing].
* **2 ≤ w < 3:** the integer-box obstructions apply, e.g. Karakuş Cor. 6.1 with m = 2: 2n − 1 squares do not fit when
  *both* sides are shrunk below (2, n).  Tilted packings beat two axis columns at widths ≈ 2.47, 2.78, 2.90, 2.98
  (domino entries n = 9, 11, 12, 13).  No exact H_n(w) for any w ∈ (2, 3) and n ≥ 4.
* **Asymptotic / waste literature** (already in `waste-bounds-2026-10-12.md`, `waste-constructions-2026-10-17.md`):
  * Erdős–Graham's tilted stacks in a strip of non-integer width;
  * Roth–Vaughan (square containers only: W(α) ≥ 10⁻¹⁰⁰ √(α‖α‖) when α(α − [α]) > 1/6);
  * Chung–Graham;
  * Arslanov–Mustafin–Shangitbayev (EJC 28(4) P4.22, squeezable rectangle packings: upper side, [P] in
    `notes/wishlist-literature-2026-10-03.md`).

  None gives an exact small case in a rectangle.  The "strip packing" OR literature (orthogonal placement, e.g. PLOS ONE
  10.1371/journal.pone.0245267, arXiv:1010.4502) is a different problem.
* Grokipedia's "Square packing" page claims exact strip values ("optimal L is n/k, k = ⌊W⌋"; "L(1) = 1").  It cites a
  Friedman *triangles* page.  This is unreliable, and the formula is false in general (the Friedman domino entries are
  counterexamples) [read page; I].

## 4. Formalisations

* **chelokot/square-packing-archive** (local snapshot e1e9ef5, docs read) [read]:
  * Lean: s(5) (Friedman's 4-point set), s(8) (Friedman's 7 points), s(10) (Stromquist), s(13) (Bentz with corrected
    sets), s(22), s(33) (Bentz lattice), s(n² − 2) = n and s(n² − 1) = n for all n ≥ 2 (compensation proof replacing
    Nagamochi's false Lemma 1, plus separate proofs for 2 and 7 squares).
  * Bend: s(6) = 3 (Stromquist's nine-point argument).
  * A Lean-checked counterexample to Nagamochi's Lemma 1.
  * **All square containers.**  Its `Rectangle.lean` is DS7 Lemma 4 (a unit square whose centre is in [0, 1] × [0, 0.4]
    contains a corner of that small rectangle), not a container theorem.  Its README says the paper's "full
    rectangular-container theorem is not verified".
* **s(11) Lean projects** (Queuingtheorydotcom / Guzhou0806 11SquaresFormalized; wand125) [S: search results, local
  copies not re-read]: square container, n = 11.
* **Our repo** (`lean/`): square containers, k² − 3 etc.  WISHLIST N12 proposes fixed-height rectangle families but
  nothing is formalised.
* **wand125 / tokoharu "rectangle-density" certificates** use uniform densities on rectangles as the *measure basis*
  for square-container lower bounds.  They are not rectangle containers (`site/notes/lower-bounds-notes.md`).
* Isabelle / Coq / HOL: nothing found for square packing (Flyspeck is spheres).
* Tangential: Yu Jiang, arXiv:2609.28791 (Meir–Moser reciprocal-rectangle tails), whose "final packing statements have
  been checked in Lean 4" [read: abstract].  This is an upper-bound construction, not optimality.

## 5. The small s(n) proofs: where they are, and are they rectangle-general?

| n | value | proof(s) | label | rectangle generality |
|---|---|---|---|---|
| 2, 3 | 2 | DS7 Thm 1 (point (1, 1) unavoidable, via Lemma 1); Göbel 1979 per Nagamochi | [read] DS7; Göbel [S] (no online copy) | square only; for n = 2 the Erdős/Yang separating-line proof gives all rectangles [I] (§1.1); n = 3 partly via Yang G₃ (§1.2) |
| 4 | 2 | area | trivial | trivial for squares; in rectangles not trivial (4 fit in 1.93 × 3.86) |
| 5 | 2 + 1/√2 | Göbel 1979; DS7 Thm 2 (4-point set, Lemmas 1–3); Stromquist memo I §2 credits Göbel | [read] DS7; memo [S, via `waste-bounds-2026-10-12.md`]; Lean (chelokot) | square only |
| 6 | 3 | Kearney–Shiu 2002 (duality); Stromquist memo I (1984, unpublished); Green (unpublished, per DS7) | [read] K–S abstract and intro (square-only throughout); Bend (chelokot) | square only |
| 7 | 3 | Kearney–Shiu 2002; DS7 Thm 7 (almost-unavoidable set); El Moumni (per DS7); Bajmóczy (claimed, per Göbel) | [read] DS7, K–S abstract | square only |
| 8 | 3 | DS7 Thm 3 (7 points); Stromquist memo I; El Moumni | [read] DS7; Lean (chelokot) | square only; also = 3² − 1, so Karakuş Cor. 6.1 / Nagamochi (box form) |
| 10 | 3 + 1/√2 | Stromquist EJC 10 (2003) #R8; memo II (1984) | [S] (pdf grep: "rectangle" appears only in lemma regions); Lean (chelokot) | square only |

* Bajmóczy, El Moumni, Green: secondhand via DS7 [read DS7's text].
* Stromquist 2003 Lemma 1 [read: grep hit] is about a box whose *centre* lies in a small [0, a] × [0, b] rectangle,
  not about rectangle containers.
* **Only rectangle-container statements found:**
  * Nagamochi 2005 Thm 1 [read]: real a, b ≥ 2, ν(a, b) < ab − Δ(a) − Δ(b), with Δ(t) = t + 1 − ⌈t⌉.  "for two
    integers a ≥ b ≥ 2 … an a × b rectangle is the smallest rectangle with aspect ratio a/b into which ab − 2 unit
    squares can be packed."  The proof has a gap (Lemma 1 false: chelokot, Karakuş).
  * Karakuş 2609.37410 [read]: Thm 1.1, ν(a, b) < ab − Δ(a) for a ≥ 2, b ≥ 3, and ab − max{Δ(a), Δ(b)} for
    a, b ≥ 3; Cor. 6.1 (integer boxes, mn − 1); Cor. 6.2, s(N) ≥ ½ + √(N − ⌊√N⌋ + ¼).  He uses s(3) = 2 for the 2 × 2
    case.
  * Yang 2608.13595 [read]: three squares (any sizes) in 1 × x.

## 6. Overlap with existing notes

* `notes/wishlist-literature-2026-10-03.md` §4 already has Nagamochi, the Karakuş caveat, Arslanov et al., the
  Erdős–Graham strips, "Three squares in a rectangle (2608.13595) is tangential", and "no squares-in-rectangles page".
  * New here: Yang is *not* tangential for n = 2, 3 (§1.1, §1.2).
  * New here: Karakuş's Cor. 6.1 settles the integer domino cases.
  * New here: Friedman's Squares-in-Dominoes listing shows tilted frontier points from n = 4.
* `site/notes/lower-bounds-notes.md` (2026-10-01) records the Nagamochi gap and the Karakuş / chelokot replacements.
  This note adds nothing to that, beyond reading Karakuş Section 6 for rectangle consequences.
* `literature/waste-bounds-2026-10-12.md`: Roth–Vaughan / Erdős–Graham / Stromquist memos read in full; reused, not
  re-read.
* WISHLIST N12 / A12 (C8) (fixed-height rectangles, rectangle monotonicity): still "literature: nothing".  This scan
  confirms it.

## 7. Open, as far as this scan can tell

1. R_3 on 1.5 ≤ w < 2, max(w, 3 − w/2) ≤ h < 3: NOT infeasible (the 45° piece of Friedman's Math Magic, June 2010,
   §1.2 correction); boundary w + h/2 = 2 + √2 for 2√2 ≤ h < 3.  **Closed 10-21**: proved in Lean (`rect3_iff`).
2. R_4 and beyond: no lower bound below integer boxes.  Even H_4(w) for w ∈ [1.93, 2) is unknown.  Is Stenlund's
   1.930 optimal for the 1:2 aspect ratio?
3. Domino n = 5 (s = 2?), n = 10 (s = 5/2?).
4. Minimum perimeter for n unit squares: does tilting ever beat the integer grid?
5. Any rectangle-container theorem in a proof assistant.
