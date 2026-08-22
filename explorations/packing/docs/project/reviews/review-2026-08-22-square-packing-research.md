# Review: The Square-Packing Research Corpus

**Date:** 2026-08-22 (reviewing the corpus as of commit `867b155`)

**Author:** Claude (agent), for samanthadrakova@gmail.com

**Status:** Complete

**Reviewed:** the three research documents under `../research/` — principally
`research-2026-08-22-packing-11-unit-squares.md` (**the main doc** below), with its
companions `research-2026-08-22-square-packing-algorithms-and-tooling.md` (**tooling
doc**) and `research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md`
(**FrankenSim doc**) — plus the literature archive under
[`resources/`](../../../resources/README.md) and the verifier under
[`explorations/packing/`](../../../README.md).

## Overview

This is a technical review in the manner of a code review: every substantive claim class
in the main doc was checked against a primary source or re-derived, defects are reported
with severity and evidence, and the second half turns from defects to strategy — what
this corpus still needs to become the first step of a complete, end-to-end survey
supporting serious computational research on `s(11)` and its neighbours.

The one-paragraph verdict: **the mathematical core is solid and survives independent
re-verification to 50 digits; the defects cluster at the periphery**, where the main doc
leans on secondary renderings of the asymptotic literature and on retrievability
conclusions that turn out to be wrong.
The most consequential single finding is not an error in the text at all: **two of the
six sources recorded as unretrievable are in fact freely downloadable today**, including
Gensane–Ryckelynck 2005 — the most important unread primary source on the `n = 11` case.
The most instructive error is the Roth–Vaughan lower bound, where the main doc prints a
wrong formula, attributes it to a source whose archived transcription is flagged garbled
at exactly that point, and does so while the correct statement sat elsewhere in its own
archive.

Findings are numbered `E-*` (errors), `G-*` (gaps and omissions), `C-*` (currency), and
`S-*` (strategic). File/line references are to the corpus at the reviewed commit.

## What was re-verified and held

The review re-derived or re-checked the main doc’s central mathematics independently of
the repository’s own scripts, then also ran the repository’s suite.
All of the following are confirmed:

- **The degree-8 polynomial**
  `s⁸ − 20s⁷ + 178s⁶ − 842s⁵ + 1923s⁴ − 496s³ − 6754s² + 12420s − 6865` is irreducible
  over ℚ (SymPy), has exactly the two claimed real roots `−1.85303247897250786…` and
  `3.87708359002281417…`, and matches the polynomial in the Kingbird catalogue’s
  `n = 11` entry character for character.
- **The three degree-8 polynomials are mutually consistent.** Eliminating `sin a`,
  `cos a` between the first contact equation, the circle relation, and the `sec a`
  polynomial `x⁸ − 2x⁷ − x⁴ + 2x³ + 8x² − 12x + 5` yields an eliminant containing the
  `s`-polynomial as an irreducible factor (resultant computation, this review).
  `derive_field.py` independently reproduces the `tan(a/2)` minimal polynomial.
- **Both contact equations, the closed form `s = 2 + (2 + sin a)/(cos a + sin a)`, the
  tilt angle to 47 digits, and all five derived constants** (`x₀, r₁, u₁, v₁, v₂`) hold
  at 50-digit precision with residuals below `10⁻⁴⁷` (mpmath, this review).
- **The Stromquist constants**: `3 + √(1/2)`, `2 + 4/√5`, `2 + (4/3)√2`, and the
  equality `2√(8/9) = 4√2/3`, all as stated.
- **The exact verifier’s results**: `./test.sh` passes in this container — 55 pairs, 14
  with exactly zero gap, 20 corner coordinates exactly on the boundary, `P(s) = 0`
  exactly, 33 published digits matched.
- **Kingbird-sourced factual claims**, checked against the archived capture: the
  `n = 11` entry carries “Found by Walter Trump in 1979”, “Rigid.”, and no “Proved by”
  line; there is no `n = 12` entry; `s(131) = 11.95654869347733` found January 2026 from
  Hajba’s November 2024 packing, “Not yet analytically optimized”; exactly **32**
  entries carry that flag; `s(171) = 13 + 4/7` by joining two copies of Schadt’s `s(50)`
  (December 2025); Bidwell’s `n = 17` dates to 1998; the special large cases
  `626, 1453, 1765, 1850, 2043` are all present; Bentz’s proofs are dated August 2009
  and October 2018 on the catalogue.
- **Quotes and attributions from [Friedman DS7] and [Stromquist 2003]**: the “many
  people have independently discovered this packing” and “incorrectly attributed to
  Gustafson and Thule” lines; the box-device quotation; the ε-shrinking mechanism (also
  present, with the `λ`-factor spelled out, in [Kearney–Shiu 2002] §2); the Hämäläinen
  correspondence date of 20 April 1980; “the first published proof that s(6) = 3 is by
  Kearney and Shiu”; DS7’s list of which cases it proves simply (2, 3, 5, 8, 15, 24, 35)
  and hard (7, 14); Trump’s packing “improved Gobel’s packing of 11 squares.”
- **The Lean sphere-packing precedent** as cited by the tooling doc: arXiv:2604.23468
  exists; the sorry-free dimension-8 proof was announced 23 February 2026; the Gauss
  autoformalisation agent (Math, Inc.)
  closed the remaining goals, ~20k → ~60k lines in five days.
- **The corrections table itself checks out**: each of its eight rows was re-confirmed,
  including the `n = 17` (Bidwell) three-angle attribution and the
  Gensane–Ryckelynck-did-not-improve-the-packing resolution, which the archived
  Ellsworth SVG provenance supports.

This is the context for everything below: the load-bearing claims of the main doc are
correct, and were correct in a checkable way — the archive discipline worked.

## Errors found

Ranked by how much they would mislead a reader doing serious work from this document.

### E-1 (high): the Roth–Vaughan lower bound is stated wrongly, and sourced to a passage the archive itself flags as garbled

Main doc, line 1018 and the table row at line 1009, states:

> Roth and Vaughan’s lower bound, **stated precisely in [Friedman DS7]**, is that if
> `x(x − ⌊x⌋) > 1/6` then `W(x) ≥ 10⁻¹⁰⁰√(x·|x − ⌊x⌋ + 1/2|)`

Three defects compound here:

1. **The formula is wrong.** `|x − ⌊x⌋ + 1/2|` is the fractional part plus one half — a
   quantity that never vanishes, making the bound `Ω(√x)` for *every* `x` satisfying the
   side condition, including `x` just below an integer where near-perfect grid packings
   exist. The correct kernel is the **distance from `x` to the nearest integer**: the
   archive’s own Wikipedia capture (`web/wikipedia-square-packing.md`, “as Klaus Roth
   and Bob Vaughan proved”) renders it `W(x) = Ω((x·|x − round(x)|)^{1/2})`, with the
   corollary that at half-integer `x` the waste is `Ω(√x)` — which is also the only
   reading consistent with the doc’s own inference that `W(x)` is not `O(x^α)` for
   `α < 1/2`.
2. **“Stated precisely in [Friedman DS7]” is false on the archive’s own evidence.** The
   DS7 transcription (`papers/friedman-ds7-…md`, line 81) marks the statement
   `GARBLED: floor function notation lost in extraction`, offers a *different*
   reconstruction (`|⌊s⌋ − s + 1/2|` — different again from what the main doc prints),
   and hedges it “or similar.”
   The main doc cites as precise a passage its own resources README explicitly warns
   about. McClenagan’s transcription is also damaged at its Roth–Vaughan quotation
   (`W(x) > 10⁻¹⁰⁰√(x − ⌊x⌋)` with orphaned fragments), so **no file in the archive
   currently supports any precise form** — the fix requires the Roth–Vaughan original
   (see G-1).
3. **The table row is broken Markdown.** Line 1009 contains unescaped `|` characters
   inside the inline-code formula; in GitHub-flavoured Markdown pipes split table cells
   even inside code spans unless escaped `\|`. The rendered row truncates the formula
   mid-expression and loses the “approx.
   exponent” cell entirely.

*Fix:* obtain Roth–Vaughan 1978 (G-1), quote the theorem from the paper, escape the
pipes, and drop “stated precisely.”

### E-2 (medium): Kearney–Shiu’s asymptotic bound is misquoted — `27r³/2` read as `27r^{3/2}`

Main doc, line 464: “they show `n_r ≤ 27r^{3/2} + O(r²)`”. The paper (archived,
`papers/kearney-shiu-…md`, abstract and equation (5)) proves

```
n_r ≤ p(⌈3r/2⌉) = 27r³/2 + O(r²),   p(t) = 4t³ + 4t² + 3t + 1
```

i.e. `(27/2)·r³`, cubic in `r` — not `r^{3/2}`. The internal check: `p(3r/2)` has
leading term `4·(3r/2)³ = 27r³/2`, and only with the cubic reading is the `O(r²)`
remainder lower-order.
The paper also notes `n_r ≪ r^{11/4}` follows from Erdős–Graham, and gives `n₂ ≤ 43`,
`n₃ ≤ 239`, `n₄ ≤ 625`, `n₅ ≤ 1320`, `n₆ ≤ 2493`, `n₇ ≤ 4072` — worth recording while
correcting.

### E-3 (medium): the internal structure of Stromquist’s Theorems 2 and 3 is misdescribed

Main doc, lines 350 and 373, present Theorem 2 as “ten unavoidable points … which rules
out eleven boxes” (plain pigeonhole) and reserve “a **twelve**-point unavoidable set”
for the 45° Theorem 3. The paper (archived transcription, proof of Theorem 2) does
something different, and the same thing, in both theorems:

- The ten Figure-13 points are **not an unavoidable set**: “Nonavoidance lemmas apply to
  all of the regions shown **except for the rectangles at the top and bottom**.” A box
  avoiding all ten must sit in one of those rectangles.
- The finishing device is Figure 14’s **twelve** points, arranged so the escaping box
  “must contain **all three** of the points marked A”; “Since three of the twelve points
  are in one box, there cannot be eleven nonintersecting boxes” (12 − 3 = 9 points for
  the remaining ≥ 10 boxes).
- Theorem 3 repeats exactly this two-stage structure with the 45°-strengthened lemmas
  and its own twelve points ("Again these 12 points form an unavoidable set in the
  context of 45° packings, and since three of them are in one box…").

This matters beyond fidelity: the three-points-in-one-box step is a *threshold*
certificate — a box is charged 3 quanta, not 1 — which is an instance of the
weighted/fractional “resource starvation” generalisation the main doc later presents as
the field’s later evolution ([Bentz 2016]). Stromquist’s 2003 proof already contains it,
which *strengthens* the doc’s own thesis and moves its origin earlier.
(Also worth noting while editing: even Theorem 1’s ten points against ten boxes cannot
finish by pigeonhole — the paper names the boxes and closes by case analysis.)

### E-4 (medium): two “not retrievable” sources are retrievable, and one is open access in the field’s own journal

The resources README’s “Not retrievable” table and the main doc’s reference list record:
Gensane–Ryckelynck 2005 “[not retrieved] — paywalled” (all portals 403), and Nagamochi
2005 “[not retrieved] — no open-access copy located”, with the dependent claims demoted
to **[secondary]**. Both conclusions are wrong as of this review:

- **Gensane & Ryckelynck, DCG 34 (2005) 97–109**: Springer serves the full PDF openly at
  `https://link.springer.com/content/pdf/10.1007/s00454-004-1129-z.pdf` (verified HTTP
  200, `application/pdf`, 269 KB, 2026-08-22; the URL is listed as the paper’s
  `openAccessPdf` by Semantic Scholar).
  The likely earlier failure mode: fetching the `/article/` landing page rather than the
  `/content/pdf/` URL. This is the **single most important unread primary source on
  `n = 11`** — the doc’s Gensane–Ryckelynck history, currently rated “medium confidence…
  rest on secondary reporting,” becomes directly checkable.
- **Nagamochi 2005** is *“Packing Unit Squares in a Rectangle”*, **Electron.
  J. Combin. 12 (2005), #R37** — open access in the same journal as half the corpus.
  The citation is in the archived DS7 reference list ([19], line 435 of the
  transcription) the whole time; the search presumably failed on a guessed title.
  The [secondary] flag on the `s(m²−1) = s(m²−2) = m` family can be retired once
  archived.

*Fix:* retrieve both, archive per house format, re-key the affected claims, and update
the two “Not retrievable” rows.
(Deliberately not done in this review — the archive’s three-format discipline is
per-paper work and belongs to its own change.)

### E-5 (medium): the priority record for the small solved cases omits El Moumni (1999)

Main doc, line 477, attributes the row `6, 7, 8, 9` entirely via Kearney–Shiu.
The archived DS7 (line 41) records a richer and partly uncomfortable history:

> “Gobel says that Schrijver claims that Bajmoczy proved s(7) = s(8) = 3 [7]. Walter
> Stromquist claimed to have proved s(6) = 3 and s(10) = 3 + 1/√2 … None of these proofs
> were published. **Said El Moumni evidently proved s(7) = s(8) = 3 and s(15) = 4 [12]
> but no one was aware of this until recently.** Finally, in 2002, Kearney and Shiu
> published a proof of s(6) = 3.”

S. El Moumni, *Studia Sci.
Math.
Hungar.* **35** (1999) 281–290, thus holds published priority for `s(7) = s(8) = 3`
and `s(15) = 4`, three years before Kearney–Shiu and never appears in the corpus.
The “first published proof of s(6) = 3” credit to Kearney–Shiu is correct; the row’s
implied coverage of 7, 8, 9 is not.
A survey should also record the Bajmóczy claim chain and Stromquist’s unpublished 1984
memoranda as *claims*, distinct from published proofs — DS7’s own motto is “the number
of claims far outweighs the number of published results in this area.”

### E-6 (low): the Cleemann counterexample description drifts from its source

Main doc, line 519: “Three of its squares are tilted at 45° and **the rest** at
`arctan(8/15)`.” DS7 (line 83): “Three squares are tilted by an angle of 45°, and **the
other tilted squares** are tilted by an angle of arctan(8/15)” — most of the 272 squares
are axis-aligned; “the rest” quietly tilts ~269 squares.
One word, but it misstates the record configuration.

### E-7 (low): the asymptotic upper-bound chain skips Wang–Dong–Li 2016

The table at lines 1005–1013 runs Erdős–Graham `7/11` → Montgomery → Chung–Graham 2009 →
Chung–Graham 2020 → McClenagan/Bui.
Both the archived Wikipedia capture and Bui’s own introduction (archived) give the chain
as `0.637 → 0.631 → 0.625 → 0.6`; the `O(x^{5/8})` step is **S. Wang, T. Dong, J. Li, “A
New Result on Packing Unit Squares into a Large Square,” arXiv:1603.02368 (2016)**,
absent from the corpus.
Two adjacent nuances worth folding into the same edit: McClenagan’s archived paper
states outright that Chung–Graham 2020’s claimed `O(x^{3/5})` proof “has an error in it”
(the main doc’s “(2020, claimed)” undersells this — the 2026 papers are not
re-derivations but repairs); and the archive’s Erdős–Graham transcription reconstructs
the central theorem as `w(α) = Θ(α^{7/11})` where the true published claim is the upper
bound `O(α^{7/11})` — the reconstruction (already flagged as such) is not merely
unverified but wrong in kind, since later work brought the exponent down to 0.6.

### E-8 (nits, for one consolidated edit)

- **Bentz year inconsistency across the corpus**: main doc says “[Bentz 2016]”
  (arXiv:1606.03746), tooling doc says “22 and 33 (Bentz **2018**)”, Kingbird says
  “Proved … in October 2018”. Pick one convention (arXiv 2016; revised/accepted 2018)
  and state it once.
- Archive metadata: `square-packing-x06-…md` header says “Year: 2026” for
  arXiv:2508.04603 (August 2025; v2 March 2026). The main doc’s key “[Waste-0.6 2025]”
  is the better reading; harmonise.
- Main doc’s Methodology quotes `2 + 4/√5 = 3.7888543819998315` (a float64 artifact;
  correctly `…8317…` at higher precision) and an interval width correct only to the
  ~12th digit because it used the 15-digit `s`. Cosmetic, but a doc this careful about
  digits should not carry them.
- DS7 is described as “last revised 2009”; the archived HTML capture carries a
  **Corrigendum dated 1 March 2023** (fixing the typeset Montgomery exponent).
  Worth a parenthetical, since the corrigendum concerns exactly the formula family in
  E-1/E-7.

## Gaps and omissions

Things a complete survey needs that no document currently provides.

### G-1: the asymptotic branch rests on secondary renderings — the two primary papers are absent

Every Roth–Vaughan and Chung–Graham statement in the corpus is quoted through DS7,
Wikipedia, McClenagan, or Bui — and E-1/E-7 show those renderings disagreeing.
Roth–Vaughan 1978 (ScienceDirect, blocked to bots but accessible in a browser; also
routinely available via interlibrary access) and Chung–Graham 2009 (Fan Chung hosts her
papers) should join the archive before the asymptotic section is edited, so the
corrected statements are keyed to primaries.
Wang–Dong–Li (arXiv:1603.02368) and the published Chung–Graham 2020 belong alongside.

### G-2: Nagamochi’s *general* lower bound is missing from the bounds inventory

Nagamochi’s paper (per its E-JC abstract) proves, for `N ≥ 4`:

```
s(N) ≥ min{ ⌈√N⌉,  √(N − 2⌊√N⌋ + 1) + 1 }
```

— the only *general-purpose closed-form* lower bound in the literature beyond area.
The main doc uses only its `m² − 1, m² − 2` corollary.
For `n = 11` it gives `min{4, √6 + 1} ≈ 3.449` — weaker than Stromquist, so nothing
changes for the headline case — but a survey’s per-`n` table (G-3) needs it: for most
open `n` it is the best bound in print that doesn’t require a bespoke unavoidable set.

### G-3: there is no “open frontier” table — the survey’s spine

The corpus states that 11 and 12 are open and lists the solved cases, but nowhere
tabulates, for each unsolved `n` (say `n ≤ 100`): best upper bound (Kingbird value, with
method and analytic status), best proved lower bound (Stromquist / Nagamochi /
monotonicity `s(n) ≥ s(n−1)` / area), the gap, and the algebraic degree of the
conjectured optimum.
That table *is* the systematic survey the project wants, it is mechanically
constructible from sources already in the archive plus Nagamochi, and it would
immediately expose where the method’s reach ends (e.g. `s(12)`'s best proved lower bound
is Stromquist’s `s(11)` bound via monotonicity — the doc never says so).
It is also the natural machine-readable artifact to pair with the record-corpus parser
the tooling doc recommends.

### G-4: the priority ledger

E-5’s cast (El Moumni, Bajmóczy-via-Schrijver-via-Göbel, Stromquist’s memoranda, Trevor
Green’s unpublished proof, Gustafsson–Thulin, Hämäläinen, the many independent
rediscoveries of Trump’s packing) shows this field’s history is unusually full of
unpublished, lost, or late-surfacing work.
A short claims-vs-published ledger — who claimed what, when, published where, first
verified where — would take an afternoon against sources already archived and would
prevent every future attribution error of the E-5 type.
DS7 §1 and the Kingbird per-entry annotations are 90% of the raw material.

### G-5: `n = 12` through `16` deserve one section of their own

The doc’s `n = 12` treatment establishes only that it is open.
A survey should record: the best packing for each of 12–16 (Kingbird), whether the
conjectured optimum is the grid (12: side 4?), what the monotonicity chain gives, and
why Bentz-style methods do or don’t reach them — since “the smallest open case after 11”
is the natural second target for any computational program, and the tooling doc’s own
recommendation (attack an integer-optimum case rigorously) needs this data to pick its
target.

### G-6: minor structural gaps worth one line each

- The Erdős–Graham 1975 paper’s own open conjecture (`f(k² + 1) = 4k` for maximal total
  circumference) is the historical seed of the field and appears nowhere.
- The transversal section’s LP-duality thread stops before naming the modern entry
  points (fractional Helly, Alon–Kleitman-style bounded τ*/ν arguments); one paragraph
  of pointers would make the “most interesting conceptual gap” actionable.
- The main doc’s confidence table rates the Smith-diagram material “high” but the BSST
  1940 primary is unretrieved; squaring.net is excellent but is a specialist secondary.
  Low priority; note it.

## Currency: the landscape as of 2026-08-22

The archive was captured today and the review re-searched the perimeter; on the central
question the corpus is current: **no change to either `s(11)` bound was found; the
Kingbird `n = 11` entry still carries no proof attribution; records elsewhere in the
table are moving monthly** (January–February 2026 finds by Ellsworth/Schadt verified in
the capture). Two currency additions matter:

### C-1: a directly relevant 2025 paper is missing

**Arslanov & Bui, “Note on 'efficient packings of unit squares in a large square',”
*Discrete & Computational Geometry* (2025), doi:10.1007/s00454-025-00767-w** — cited in
Bui’s archived reference list — is a current continuation of exactly the Kearney–Shiu
`δ_n / n_r` problem the main doc discusses (and E-2 corrects).
It should be read and archived with the E-2 fix.

### C-2: the AI-for-mathematical-discovery landscape moved fast in 2025–26, and the corpus records only its first event

The tooling doc covers AlphaEvolve (May 2025; hexagon `n = 11` to side 3.931; its “no
AlphaEvolve-class result for squares-in-squares has been reported” **survived this
review’s re-check**) and the Berthold et al.
response. Since then, in the adjacent-benchmark ecosystem:

- **Berthold, Kamp, Mexi, Pokutta, Pólik** now have two papers: “Global Optimization for
  Combinatorial Geometry Problems Revisited in the Era of LLMs” (arXiv:2601.05943, Jan
  2026 — the AlphaEvolve comparison; solvers “reproduce, and in several cases improve
  upon” the LLM discoveries) and “Out-of-the-Box Global Optimization for Packing
  Problems” (arXiv:2605.04850, May 2026 — S-lemma and Farkas formulations; new
  incumbents across polygon/solid families).
  The tooling doc’s comparison table draws on this line; both papers plus the open
  solution database (`DominikKamp/Packing`) should be pinned as references.
- **An open evolutionary-search ecosystem formed around the AlphaEvolve benchmark**:
  OpenEvolve/ShinkaEvolve/CodeEvolve (replications; already cited), then ThetaEvolve
  (arXiv:2511.23473), FM Agent (arXiv:2510.26144), ImprovEvolve (arXiv:2602.10233),
  Helix (arXiv:2603.07642), SeaEvo (arXiv:2604.24372), and flow-based generative search
  (arXiv:2601.18005 — which set a new record on the 26-circle sum-of-radii benchmark).
  None touches squares-in-squares.
- **Humans and AI systems are now trading records at the 10⁻⁵ level on these
  benchmarks**: on the `n = 26` circle sum-of-radii problem, an independent individual
  ("Alex," ~6 weeks of work) beat AlphaEvolve’s 2.63586275 with 2.63592717 via a novel
  configuration, before the flow-based system pushed further (2.63598308). The sociology
  matters for strategy: benchmark problems adjacent to ours are contested; `s(n)` itself
  is not — it is still one closed-source annealer and one catalogue maintainer.
- **Formalisation crossed its threshold** (verified above): dimension-8 sphere packing
  sorry-free in Lean, February 2026, finished by an autoformalisation agent.
  The tooling doc’s reading — the missing ingredient for square packing is an informal
  computer-assisted proof to formalise, not the assistant — stands.

The strategic reading: **the field’s AI activity is all on the search side and all on
other problems.** Nobody has aimed the 2026 evolutionary stack at `s(n)`; nobody has
aimed anything at the lower-bound side.
Both are open lanes.

## Strategic assessment

What stands between this corpus and “the groundwork for a complete, systematic,
end-to-end survey,” in priority order.
Items 1–3 are corrections and acquisitions; 4–7 are the survey; 8–10 are the modern
research program the survey should feed.

1. **S-1 — Apply the fixes.** E-1 through E-8 in the main doc (and the two archive
   metadata nits), in one edit pass keyed to this review.
2. **S-2 — Complete the archive’s unretrieved tier.** Gensane–Ryckelynck (URL above,
   verified live), Nagamochi (E-JC v12 R37), Roth–Vaughan and Chung–Graham 2009 (G-1),
   Wang–Dong–Li, Arslanov–Bui 2025, El Moumni (Studia Sci.
   Math. Hungar. 35 — likely needs library access), and a fresh attempt on Trump’s March
   2023 ResearchGate note (author’s profile hosts it; a polite author request is the
   reliable route, as it also is for Stromquist’s 1984 memoranda).
   Each per the three-format house discipline that E-1 just vindicated.
3. **S-3 — Read Gensane–Ryckelynck and close the loop.** The `n = 11` history section
   currently carries “medium” confidence resting on Ellsworth’s annotations; after S-2
   it can rest on the paper.
   Also settles the open question about their contact classes for `n = 11` — did the
   billiard ever visit a class other than Trump’s?
4. **S-4 — Build the open-frontier table (G-3) as both prose and data.** One row per
   `n ≤ 100`: status, both bounds with provenance, gap, algebraic degree, analytic
   status of the record.
   Sources: Kingbird capture + Nagamochi + Stromquist + monotonicity.
   This is the survey’s spine and the first artifact the record-corpus parser (tooling
   doc rec #1) should emit.
5. **S-5 — Write the priority ledger (G-4).** Claims vs publications, 1979–2026.
6. **S-6 — Reconcile the asymptotic branch against primaries (G-1)** and rewrite that
   section of the main doc from them, including the corrected Roth–Vaughan theorem, the
   full exponent chain, and the Chung–Graham-2020-error → 2025/26-repair story.
7. **S-7 — Fold the three documents’ inventories into one survey document** once S-1–S-6
   land: the main doc’s mathematics + strategy catalogues, the tooling doc’s stacks and
   measurements, the FrankenSim doc’s engineering imports, each currently excellent and
   none currently the single end-to-end reference the project wants.
   (The cross-referencing is already good; the merge is mostly editorial.)
8. **S-8 — Stand up the verifier-first computational program** (unchanged from the
   tooling doc’s recommendations, which this review endorses and re-prioritises): the
   machine-readable record corpus + filtered exact kernel first — it is cheap, it is
   unclaimed territory, it makes every record independently auditable, and every later
   effort consumes it.
9. **S-9 — Point the modern search stack at `s(n)` as a benchmark.** C-2 shows the
   evolutionary-search ecosystem is active, open, and has never touched
   squares-in-squares, while the actual records come from one closed annealer.
   An open `jagua-rs`-based annealer (tooling rec #2) plus an OpenEvolve-style harness,
   seeded with the Kingbird corpus and scored by the exact verifier, would (a) test
   whether the 2026 stack can rediscover Trump’s basin and the low-`n` records, (b)
   generate the basin statistics that today exist only for two cases, and (c) give the
   community a reproducible baseline the closed annealer cannot be.
   Deterministic-RNG and measurement discipline per the FrankenSim doc.
10. **S-10 — Open the lower-bound lane, where nothing automated has ever run.** Three
    graded moves: (i) machine-verify the existing unavoidable sets (a 3-parameter
    decision per set — interval branch-and-bound or `nlsat`; tooling rec #4); (ii)
    *search* for new unavoidable configurations at `n = 12…16` targets, which is a
    discrete-continuous search problem well-shaped for the same agentic stack as S-9 but
    aimed at proofs, honouring E-3’s lesson that threshold (3-points-in-a-box)
    certificates are admissible and already classical; (iii) formalise one existing
    small proof (Friedman’s Lemmas 1–3 plus `s(2) = s(3) = 2`, then Stromquist’s Theorem
    1\) in Lean as the first square-packing formalisation — small, self-contained, and
    it would surface any informal gaps in the lemma layer that everything else stands
    on.

Two calibration notes to keep the program honest, both inherited from the corpus and
confirmed here: rigorous certification of `s(11)` itself remains far out of reach (the
`n = 3`-in-a-circle ceiling stands), so S-10’s targets are the integer-optimum cases,
not 11; and search success at `n = 11` can only ever re-confirm the conjecture — the
proof problem is the lower bound, which is why S-10 exists.

## Review methodology

Conducted 2026-08-22 against commit `867b155`.

- **Re-derivation**: SymPy (irreducibility, real roots, resultant-based consistency of
  the three degree-8 polynomials, re-run of `derive_field.py`) and mpmath at 50 digits
  (contact equations, closed form, tilt angle, five derived constants, Stromquist
  constants). The repository’s `test.sh` was run and passed in this container.
- **Source-checking**: every claim quoted above was grepped in the archived
  transcriptions (`resources/papers/`, `resources/web/`), with `.raw.md` consulted where
  transcriptions carry GARBLED/NOTE flags; the E-1, E-2, E-3, E-5, E-6, E-7 findings
  each cite the specific archived line.
- **Currency and retrievability**: targeted web search on 2026-08-22 for changes to the
  `s(11)` bounds (none found), the AI-for-discovery ecosystem (C-2’s items each
  confirmed to exist via arXiv listings), the Lean milestone (confirmed), Nagamochi’s
  E-JC identity (confirmed against the journal), and the Gensane–Ryckelynck open PDF
  (fetched: HTTP 200, application/pdf, 269 KB). Negative results from search remain weak
  evidence, per the corpus’s own standard; they are labelled as such.
- **Not reviewed line-by-line**: the FrankenSim doc’s internal measurements of that
  codebase (its scale/architecture/licensing sections were read; its build and probe
  results were spot-checked only via the probe README and its cross-consistency with the
  verifier’s 41/14 split, which held).

## References new to the corpus (found by this review)

- S. El Moumni, “Optimal packings of unit squares in a square,” *Studia Sci.
  Math. Hungar.* **35** (1999), no.
  3–4, 281–290. (Priority for `s(7) = s(8) = 3`, `s(15) = 4`; via DS7 ref [12].)
- H. Nagamochi, “Packing Unit Squares in a Rectangle,” *Electron.
  J. Combin.* **12** (2005), #R37.
  https://www.combinatorics.org/ojs/index.php/eljc/article/view/v12i1r37
- T. Gensane, P. Ryckelynck, “Improved Dense Packings of Congruent Squares in a Square,”
  *Discrete Comput. Geom.* **34** (2005) 97–109 — open PDF:
  https://link.springer.com/content/pdf/10.1007/s00454-004-1129-z.pdf
- S. Wang, T. Dong, J. Li, “A New Result on Packing Unit Squares into a Large Square,”
  arXiv:1603.02368 (2016). (The `O(x^{5/8})` step.)
- M. Z. Arslanov, H. D. Bui, “Note on 'efficient packings of unit squares in a large
  square',” *Discrete Comput.
  Geom.* (2025), doi:10.1007/s00454-025-00767-w.
- T. Berthold, D. Kamp, G. Mexi, S. Pokutta, I. Pólik, “Global Optimization for
  Combinatorial Geometry Problems Revisited in the Era of LLMs,” arXiv:2601.05943
  (2026); and “Out-of-the-Box Global Optimization for Packing Problems,”
  arXiv:2605.04850 (2026).
- AlphaEvolve-ecosystem papers named in C-2: arXiv:2511.23473 (ThetaEvolve),
  arXiv:2510.26144 (FM Agent), arXiv:2602.10233 (ImprovEvolve), arXiv:2603.07642
  (Helix), arXiv:2604.24372 (SeaEvo), arXiv:2601.18005 (flow-based extremal discovery).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
