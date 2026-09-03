# BC-152 — Curve Selection Lemma: Source Verification for H-060

## Provenance and installation

This document is the review deliverable of BC-152's curve-selection source verification for H-060, written on 2026-09-03 in the
agenda-016 ten-hour run. Its author wrote only to `scratchpad/bc152-curveselection/`
-- a container-local directory outside the repository, which does not survive the
session -- and modified no repository file. It is installed here so that the evidence the
records cite outlives that directory.

The source was `552` lines with SHA-256
`158d593e2fad9bc0662b95007956d1e081f684f38a26666d61c04668758cee15`, and that hash names the scratchpad
source rather than this file. The installation added this preface and the closing guidelines footer, and reformatted the body to
house Markdown conventions; it altered no classification, verdict, finding, number,
citation, recommendation or claim boundary, and none may be altered here. References of
the form `scratchpad/...` in the body below are the reviewer's own record of what was
read and where it was written at review time, and are left as written.

* * *

Verification of the semialgebraic curve-selection step used in the H-060 isolation
argument (X-007). Prepared 2026-09-03. Read-only with respect to the repository; no
repository file was modified.

## 0. Verdict

**YES — the statement as used follows from a correctly cited theorem, and X-012 §4 is
sound as written. Two source-level strengthenings and two additions to the Milnor
reduction are recommended; no mathematical defect was found.**

The statement is verified against the Nash curve selection lemma of Bochnak–Coste–Roy,
Proposition 8.1.13. The proof's set — `F \ {0}` for `F` a closed basic semialgebraic set —
satisfies its hypotheses outright, and satisfies every extra hypothesis that any weaker
citable version of the lemma might impose.

- The usable citation is **Bochnak–Coste–Roy, Proposition 8.1.13** (the Nash curve
  selection lemma). It carries *no* extra hypothesis: an arbitrary semialgebraic set and
  an arbitrary point of its closure suffice, and the arc it returns is Nash — analytic
  *and* semialgebraic — which is strictly stronger than the real-analytic arc the proof
  asks for.
- **Milnor's Lemma 3.1 does not give the statement as written**, and the brief's suspicion
  about it is correct. Milnor's "semi-algebraic" means *real algebraic set intersected with
  finitely many strict polynomial inequalities*, not an arbitrary semialgebraic set — now
  confirmed verbatim from a peer-reviewed source that cites Milnor p. 25 (§2.6). The
  finite-union reduction is genuinely required, and the proof's set is **not** in Milnor's
  class until it is decomposed: its inequalities are non-strict and it has a point removed.
  **X-012 §4.1 already gives that reduction and gives it correctly** — see §5.2–§5.4, which
  restate it, check its five requirements, and add two more.
- **The `x ∈ Cl(A)` phrasing is safe only because of how X-012 applies it, and that is
  worth keeping explicit.** Under `x ∈ Cl(A)` alone, when `x ∈ A` the *constant* arc
  `γ ≡ x` satisfies the conclusion and the lemma yields nothing. X-012 §4.2 applies the
  lemma to `A := F \ {0}` with `0 ∉ A`, and Corollary 4.3 derives nonconstancy from
  `γ(s) ≠ 0` on `(0,1)`. **That is correct as written.** No change is required; the note
  here is that this is load-bearing, not incidental, and any later re-phrasing that
  applies the lemma to `F` itself rather than to `F \ {0}` silently breaks the argument.
  Coste's Theorem 1.14/1.15 states the `x ∈ clos(A), x ∉ A` form directly and can be cited
  if a reviewer wants the guard built into the theorem.
- Analyticity is **load-bearing, not cosmetic**: it is what guarantees a well-defined
  lowest nonvanishing coefficient `a_m`. See §4.4.

**Primary text status, stated plainly:** I did **not** reach the printed page of BCR
Prop. 8.1.13, and I did **not** reach the printed page 25 of Milnor's Lemma 3.1. Both
are behind publisher paywalls (Springer; De Gruyter/Princeton), Google Books' API quota
was exhausted, and the books are not on archive.org or HathiTrust in a readable form. I
did reach:

- the **printed BCR table of contents** (Deutsche Nationalbibliothek scan) — primary,
  front matter only, and it locates 8.1.13 correctly;
- the **complete printed text of Basu–Pollack–Roy** (authors' own posted copy), which
  gives the continuous semialgebraic version verbatim — primary, but not the analytic
  version;
- **Michel Coste's own lecture notes** — Coste is the "C" of BCR — which state the
  analytic/Nash version in exactly the form the proof needs.

That is short of the printed BCR page. It is not short of what is needed to certify the
hypotheses, because the analytic statement is attested verbatim by a BCR author and the
hypothesis class is attested verbatim by four mutually independent author groups.

**What X-012 should change:** nothing mathematical. Four provenance and completeness
edits, listed in §7.

## 1. The statement under verification

As currently used in the proof:

> For an arbitrary semialgebraic set `A` and a point `x` in the closure of `A`, there
> exists a real-analytic arc `γ : [0, ε) → R^n` with `γ(0) = x` and `γ((0, ε))` contained
> in `A`.

## 2. Sources reached, with verbatim statements

Extraction note: in every PDF below the overline denoting topological closure is *drawn*,
not encoded as a character, so `Ā` extracts as `A`. Every occurrence where I have
restored a closure bar is flagged `[bar restored]`, and each restoration is independently
corroborated in the same row.

### 2.1 PRIMARY — Basu, Pollack, Roy (continuous semialgebraic version)

**Source.** S. Basu, R. Pollack, M.-F. Roy, *Algorithms in Real Algebraic Geometry*,
Algorithms and Computation in Mathematics, Volume 10, Springer. Complete text posted by
the authors; the copy used carries the title-page date **June 26, 2016**. Retrieved via
the Internet Archive snapshot of `perso.univ-rennes1.fr/marie-francoise.roy/bpr-ed2-posted3.pdf`
(the live host refuses this session's egress).

> **Theorem 3.22 (Curve selection lemma).** Let `S ⊂ R^k` be a semi-algebraic set. Let
> `x ∈ S̄` [bar restored]. Then there exists a continuous semi-algebraic mapping
> `γ : [0, 1) → R^k` such that `γ(0) = x` and `γ((0, 1)) ⊂ S`.

Bar restoration is certain: the proof's first line is "For every `r > 0` in `R`,
`B(x,r) ∩ S` is non-empty", which *is* the definition of `x ∈ S̄`; and Basu–Roy state the
identical theorem with an extracted bar (§2.5 below).

**Numbering drift — flag this.** In the *printed second edition (Springer, 2006)* this
result is **Theorem 3.19**, as cited by Basu–Roy (2018/2021) and by Plaumann (2023). It is
**Theorem 3.22** in the authors' posted 2016 revision, where Proposition 3.19 is a
different (auxiliary) result. Cite it by name, and give both numbers if a number is given
at all.

**Status:** primary; printed book, authors' own complete text. **Continuous semialgebraic
arc only — not analytic.**

### 2.2 PRIMARY (front matter) — the printed BCR table of contents

**Source.** Deutsche Nationalbibliothek scan of the printed table of contents of
Bochnak–Coste–Roy, *Real Algebraic Geometry* (`d-nb.info/953926273/04`). Verbatim lines:

> `2.5 Closed and Bounded Semi-algebraic Sets. Curve-selection Lemma 35`
>
> `8. Nash Functions 161`
> `8.1 Germs of Nash Functions and Algebraic Power Series 161`
> `8.2 Local Properties of Nash Functions 167`

This establishes, from the printed book itself, that BCR contains **two** curve-selection
results — one in §2.5 (p. 35 ff., the continuous version) and one inside §8.1
(pp. 161–166), the section on germs of Nash functions and algebraic power series. That is
exactly where a *Nash* curve selection lemma numbered **8.1.13** must live, and exactly
the machinery (algebraic power series, algebraic Puiseux series) that proves it. It does
not give the proposition's text.

### 2.3 AUTHOR-WRITTEN (a BCR author) — Coste, the analytic/Nash version

**Source.** Michel Coste, *Real Algebraic Sets*, lecture notes from the mini-course at the
RAAG winter school, Aussois, January 2003; document dated **March 23, 2005**;
`perso.univ-rennes1.fr/michel.coste/polyens/RASroot.pdf` (retrieved via Internet Archive).
Coste is the "C" of Bochnak–Coste–Roy.

> **Theorem 1.14 (Curve selection lemma)** Let `S ⊂ R^n` be a semialgebraic set. Let
> `x ∈ clos(S)`, `x ∉ S`. Then there exists a continuous semialgebraic mapping
> `γ : [0, 1] → R^n` such that `γ(0) = x` and `γ((0, 1]) ⊂ S`.

and, after a two-paragraph explanation identifying germs of Nash functions with real
algebraic series `R[[t]]_alg` and germs of continuous semialgebraic functions with real
algebraic Puiseux series:

> **Theorem 1.15 (Analytic curve selection)** For `A` and `x` as in theorem 1.14, there
> exists a Nash curve `γ : (−1, 1) → R^n` such that `γ(0) = x` and `γ((0, 1)) ⊂ A`.

**This is the statement under verification**, with `x ∉ A` added and with "Nash" in place
of "real-analytic" — both differences in the *safe* direction (see §4).

**Honest caveats.** These are lecture notes, self-described as "still in a provisional
form"; Coste introduces Theorem 1.15 with "We explain the reason for this fact, without
giving a complete proof". They are therefore an authoritative statement by an author of
the cited theorem, not a substitute for the printed BCR page.

Coste's companion notes, *An Introduction to Semialgebraic Geometry* (IRMAR Rennes,
October 2002; also published in print in the Pisa Dottorato series), give the same
continuous statement as **Theorem 3.13**, word for word identical to Theorem 1.14 above.

### 2.4 SECONDARY — verbatim uses of `[BCR, Prop. 8.1.13]`

All four papers below carry the bibliography entry
`[BCR] J. Bochnak, M. Coste, M.-F. Roy: Real algebraic geometry. Ergeb. Math. 36,
Springer-Verlag, Berlin` (verified in the reference lists, not assumed). Note a web-search
summary encountered during this work misidentified `[BCR]` as Basu–Pollack–Roy; that is
wrong, and the bibliography entries settle it.

| Source | Verbatim use |
| --- | --- |
| Fernando & Ueno, arXiv:1212.1811v3 | "As `p ∈ Cl_{RP^m}(S₁) \ S₁`, there exists by the Nash curve selection lemma **[BCR, 8.1.13]** a Nash path `γ : (−1,1) → RP^m` such that `γ((0,1)) ⊂ S₁` and `γ(0) = p`." |
| Fernando, arXiv:1503.05706 (*On Nash images of Euclidean spaces*) | "By the Nash curve selection lemma **[BCR, Prop.8.1.13]** there exists a Nash arc `γ : (−1,1) → M × S^{k−1}` such that `γ(0) = (a,b)` and `γ((0,1)) ⊂ Γ_ε`." |
| Carbone & Fernando, arXiv:2601.13164 | "By the Nash curve selection lemma **[BCR, Prop.8.1.13]** there exist Nash arcs `γ₁ : [−1,0] → (R₁\R₂)∪{p}` and `γ₂ : [0,1] → (R₂\Y₁)∪{p}` such that `γ_i(0) = p`, `γ₁([−1,0)) ⊂ R₁` and `γ₂((0,1]) ⊂ R₂\Y₁`." |
| Fernando, arXiv:2504.03348 | "the classical (Nash) curve selection lemma **[BCR, Prop.8.1.13]**"; and, applied: "there exists by **[BCR, Prop.8.1.13]** a Nash arc `η : [−1,1] → R^n` such that `η(0) = p` and `η((0,1]) ⊂ Int(S)`." |

The third row is the decisive adversarial datum: `R₂ \ Y₁` is a *difference* of a closed
semialgebraic set and an algebraic set — neither closed, nor open, nor basic — and the
lemma is applied to it directly. **BCR 8.1.13 carries no closedness, boundedness,
openness, basic-ness, or dimension hypothesis.**

These four are one author group (Fernando and coauthors). Independent corroboration of
BCR's *numbering convention* for chapter 8 comes from Coste–Ruiz–Shiota, *Nash triviality
in families of Nash mappings* (Ann. Inst. Fourier), which cites `[BCR], 8.10.3` — matching
the printed §8.10 "Families of Nash Functions", p. 202.

### 2.5 SECONDARY — independent statements of BCR's §2.5 (continuous) version

- **Delage, Fichou, Patel**, *The Geometry of Locally Bounded Rational Functions*,
  arXiv:2409.04232 (reference `[2]` verified as BCR, Ergebnisse 36, Springer 1998):

  > **Theorem 2.3 (The Curve Selection Lemma [2, 2.5.5]).** Let `A ⊆ R^n` be a
  > semi-algebraic subset of `R^n` and let `x ∈ Ā` [bar restored]. There exists a
  > continuous semi-algebraic function `f : [0,1] → R^n` such that `f(0) = x` and
  > `f((0,1]) ⊆ A`.

- **Plaumann**, *Real Algebraic Geometry* (IHP tutorial lectures, 12 October 2023):

  > **6.5 Theorem (Curve selection lemma).** Let `S ⊂ R^n` be a semialgebraic set, and let
  > `x ∈ S̄` [bar restored]. Then there is a semialgebraic path `α : [0,1] → R^n` such that
  > `α(t) ∈ S` for every `t ∈ [0,1)` and `α(1) = x`.
  >
  > "Two different proofs are given in [BCR98, §2.5] and [BPR06, Thm. 3.19]."

- **Basu & Roy**, *Quantitative Curve Selection Lemma*, arXiv:1803.00505v3 (Math. Z.);
  M.-F. Roy is the "R" of BCR:

  > **Theorem 1 (Curve Selection Lemma).** Let `S ⊂ R^k` be a semi-algebraic set and
  > `x ∈ S̄`. Then there exists a positive element `t₀` of `R`, and a semi-algebraic path
  > `φ` from `[0,t₀)` to `R^k` such that `φ(0) = x` and `φ((0,t₀)) ⊂ S`.
  >
  > "This result, due to Łojasiewicz [6, 7] (see also [8]) …"

Here the closure bar *did* extract, in Basu–Roy, confirming the restorations above.

### 2.6 SECONDARY — what Milnor's Lemma 3.1 actually assumes

**Source.** A. Derdzinski and Ś. R. Gal, *Indefinite Einstein metrics on simple Lie
groups*, arXiv:1209.6084 (published), §4, titled "Milnor's curve-selection lemma".
Verbatim:

> A subset of a vector space `S` is called *algebraic* if it equals `F^{−1}(0)` for some
> polynomial mapping `F : S → V` into a vector space `V`. By a *semi-algebraic set* in `S`
> one means the intersection of an algebraic set with `⋂_{j=1}^{k} f_j^{−1}((0,∞))`, where
> `k ≥ 1` and `f_1,…,f_k` are polynomial functions `S → R`. The intersection of two
> semi-algebraic sets in `S` is semi-algebraic, while complements of algebraic subsets of
> `S` constitute finite unions of semi-algebraic sets. Thus, whenever `Z ⊂ S` and `L ⊂ S`
> are algebraic, one easily sees that
>
> `Z \ L` is a finite union of semi-algebraic sets in `S`.  (4.1)
>
> The following result of Milnor **[14, p. 25]**, known as the *curve-selection lemma*,
> generalizes the earlier versions due to Bruhat and Cartan [5, Theorem 1], and Wallace
> [18, Lemma 18.3]. Further details can be found in [15, p. 402].
>
> **Theorem 4.1.** Suppose that `0` lies in the closure of a semi-algebraic subset `A` of
> a vector space `S`. Then there exists a real-analytic curve `[0,δ) ∋ t ↦ S(t) ∈ S`, with
> `δ ∈ (0,∞)`, such that `S(0) = 0` and `S(t) ∈ A` for all `t ∈ (0,δ)`.
>
> *Proof.* See [14, p. 25]. □

Reference `[14]` is Milnor, *Singular points of complex hypersurfaces*, Ann. of Math.
Stud. 61, Princeton University Press, 1968; `p. 25` is the first page of §3, "The Curve
Selection Lemma" (De Gruyter's digitisation of the Princeton edition confirms §3 spans
pp. 25–32).

**This is the whole adversarial point.** Milnor's "semi-algebraic" is the *restricted*
class — real algebraic set `∩` finitely many **strict** polynomial inequalities. The
Némethi–Zaharia restatement ("We need a version of Curve Selection Lemma from Milnor's
book", *On the bifurcation set of a polynomial function and Newton boundary*, EMS) has the
same shape: `U = {f_i = 0}`, `W = {g_i > 0}`, arc real analytic into `U ∩ W`. Nguyen Hong
Duc (arXiv:2301.00128) attributes the *arbitrary*-semialgebraic Nash version to Milnor;
that is an over-attribution relative to Milnor's own hypotheses, and is one of the two
secondary sources the previous agent relied on. It is not wrong about the mathematics, but
it is wrong about which theorem says it.

For the record, the semianalytic generalisation as usually quoted (Massey,
arXiv:1410.3312, Appendix Lemma 5.1, citing Milnor §3 and Lê §2.1) reads: "Let `p` be a
point in a real analytic manifold `M`. Let `Z` be a semianalytic subset of `M` such that
`p ∈ Z̄`. Then, there exists a real analytic curve `γ : [0,δ) → M` with `γ(0) = p` and
`γ(t) ∈ Z` for `t ∈ (0,δ)`."

## 3. Sources attempted and not reached

Recorded so this is not re-attempted blind.

- Repository literature archive `packing/resources/`: **no** BCR, Milnor, Nash, or
  curve-selection material. The only in-repo mentions of "curve selection" are X-007,
  `frontier/evidence.yaml`, `devtools/assess_n5_rigidity.py`, and one BC-049 results file.
  `TUTORIAL.md` cites BCR only for Tarski–Seidenberg.
- `perso.univ-rennes1.fr` (Coste's and Roy's pages): HTTP 403 to this session from both
  `curl` and WebFetch, with and without browser headers. Worked around via the Internet
  Archive; that is how the Coste notes and the BPR book were obtained.
- Springer Link BCR chapter pages: redirect to an IdP authorisation endpoint.
- De Gruyter / Princeton digitisation of Milnor §3: `405` to WebFetch, `202` with an empty
  body to `curl`; the PDF endpoint is `licenseType=restricted`.
- Google Books API: `429`, daily quota for this project is `0`. The Google Books web
  preview for BCR (`id=GJv6CAAAQBAJ`) renders no body text.
- archive.org / OpenLibrary: no scanned copy of either book (`has_fulltext: false`,
  `ebook_access: no_ebook`); HathiTrust bibliographic API returns no record for
  ISBN 3540646639. The Internet Archive CDX endpoint was intermittently offline.
- `academia.edu` copy of BCR: `403`.
- `perso.univ-rennes1.fr/goulwen.fichou/RAG2.pdf`, which a search engine offered as the
  BCR book, is a 21-page set of handwritten lecture notes with the BCR cover on page 1.
  Not the book. Flagging it so nobody else spends time on it.

## 4. Hypothesis-by-hypothesis check

### 4.1 Is `A` required to be more than semialgebraic?

**No.** BCR 8.1.13 as used in the literature applies to arbitrary semialgebraic sets,
including a difference `R₂ \ Y₁` that is neither closed, open, nor basic (§2.4, row 3),
and to `Int(S)` for `S` merely semialgebraic. The continuous versions (BCR 2.5.5, BPR
3.22/3.19, Coste 1.14/3.13) likewise say "let `S ⊂ R^n` be a semialgebraic set" with no
further condition. **No boundedness, closedness, local closedness, openness, basic-ness,
pure-dimensionality, or dimension bound appears in any of them.**

The one place bounded/closed language appears near this result is BCR's *section title*
("2.5 Closed and Bounded Semi-algebraic Sets. Curve-selection Lemma") — a section heading,
not a hypothesis. Coste's proof of Theorem 1.14 opens by *reducing* to the bounded case
("Replacing `S` with its intersection with a ball with center `x` and radius 1, we can
assume `S` bounded"), which is the reduction, not an assumption.

**Milnor is the exception**, and it is a real one: his class is `V ∩ {g_1 > 0, …, g_k > 0}`
with `V` real algebraic. See §5.

### 4.2 `x ∈ closure(A)`, or `x ∈ closure(A) \ A`?

Both occur, and the difference matters more than it looks.

- `x ∈ Ā` (no exclusion): BCR 8.1.13 (as used), BCR 2.5.5, BPR 3.22/3.19, Basu–Roy Thm 1,
  Plaumann 6.5, Massey 5.1, Milnor/Derdzinski–Gal 4.1.
- `x ∈ clos(S), x ∉ S`: Coste Thm 1.14 and Thm 3.13.

Formally, the `x ∉ A` version is a *weaker theorem* (stronger hypothesis), and the gap is
vacuous: if `x ∈ A`, the constant arc `γ ≡ x` already satisfies `γ(0) = x` and
`γ((0,ε)) ⊂ A`. So no source is stronger than another here.

**But that vacuity is precisely the trap for this proof.** An isolation argument needs a
*nonconstant* arc. Under `x ∈ Ā` alone, the lemma is entitled to hand back the constant
arc, and the coefficient induction has nothing to bite on. The fix is free and must be
stated: apply the lemma to `A = F \ {p}`, so that `p ∉ A` and every arc with
`γ((0,ε)) ⊂ A` automatically satisfies `γ(s) ≠ p` for `s > 0`. Coste's Theorem 1.15 is
already phrased this way and is the cleanest thing to cite.

Formally: *`p` is not isolated in `F`* `⟺` `p ∈ clos(F \ {p})`, which is the hypothesis of
the `x ∈ clos(A) \ A` form applied to `A = F \ {p}`.

### 4.3 Real-analytic, Nash, or merely continuous?

Three distinct strengths, and the sources are consistent about which gives which:

| Result | Arc |
| --- | --- |
| BCR **2.5.5**, BPR **3.22** (2006 print: 3.19), Basu–Roy Thm 1, Coste 1.14/3.13, Plaumann 6.5 | continuous **semialgebraic** |
| BCR **8.1.13**, Coste **1.15** | **Nash** |
| Milnor **Lemma 3.1** (per Derdzinski–Gal Thm 4.1) | **real-analytic** |

A **Nash** function is a real-analytic function that is also semialgebraic (equivalently,
satisfies a nontrivial polynomial identity `P(t, γ(t)) = 0`). So **Nash ⟹ real-analytic**,
strictly: `sin`, `exp` are analytic and not Nash. The statement under verification asks
only for real-analytic, so **BCR 8.1.13 delivers strictly more than is claimed.** No gap.

Note also that BCR/Coste give a *two-sided* Nash arc on `(−1,1)`, analytic at `0` in the
ordinary sense. That resolves, in the safe direction, the mild ambiguity of "real-analytic
on `[0, ε)`": restricting the two-sided arc to `[0,1)` yields the stated form.

### 4.4 `γ((0,ε)) ⊆ A`, or only "meets `A`"?

**Containment, in every source without exception.** BPR: `γ((0,1)) ⊂ S`. Coste 1.14:
`γ((0,1]) ⊂ S`. Coste 1.15: `γ((0,1)) ⊂ A`. Delage–Fichou–Patel: `f((0,1]) ⊆ A`.
Basu–Roy: `φ((0,t₀)) ⊂ S`. Derdzinski–Gal/Milnor: `S(t) ∈ A` for all `t ∈ (0,δ)`. Fernando:
`γ((0,1)) ⊂ Γ_ε`, `η((0,1]) ⊂ Int(S)`. The proof's phrasing is correct.

### 4.5 Why analyticity is load-bearing here

Worth stating explicitly in the proof artifact, because it is the reason the *continuous*
version is not simply interchangeable.

Given the Nash (hence real-analytic) arc `γ` with `γ(0) = p` and `γ((0,ε)) ⊂ F \ {p}`:
`γ` is not identically `p` near `0`, so by the identity theorem for real-analytic
functions its Taylor expansion at `0` has a first nonvanishing coefficient. That is
exactly the `m ≥ 1` and `a_m ≠ 0` in `γ(s) = p + Σ_{k ≥ m} a_k s^k` on which X-007's
induction runs. A merely `C^∞` arc could be flat at `0` and admit no such `m`; a merely
continuous semialgebraic arc has only a *Puiseux* expansion in `s^{1/N}` and needs the
reparametrisation `s = u^N` before the induction can start.

So: **taking the Nash version removes the Puiseux step entirely.** X-007 currently reads
"the curve selection lemma gives a semi-algebraic arc into the set, and Puiseux gives
`gamma(s) = p + sum_{k >= m} a_k s^k`". With BCR 8.1.13 the arc is already a convergent
integral power series and no Puiseux argument or reparametrisation is needed. If the
Puiseux phrasing is kept, the reparametrisation to clear fractional exponents must be
written down; it is legitimate but it is a step.

## 5. The Milnor route and the finite-union reduction

If the proof wants to cite Milnor as well as (or instead of) BCR, this is what it owes.

### 5.1 What Milnor's class is

`A` must be `V ∩ U` with `V ⊆ R^n` a real algebraic set and
`U = {x : g_1(x) > 0, …, g_k(x) > 0}` — finitely many **strict** polynomial inequalities.

The proof's set is **not** in this class as written, for two independent reasons: its
defining inequalities are **non-strict** (`g_j ≥ 0`), and it has a **point removed**.

### 5.2 The reduction, stated

X-012 §4.1 already gives this reduction, and gives it in a cleaner form than the obvious
one — the removed point is handled by the single strict inequality `{|z|² > 0}` rather
than by a coordinate-by-coordinate splitting. Restated in full, with the requirements
made explicit:

Let `F = {x ∈ R^n : g_1(x) ≥ 0, …, g_N(x) ≥ 0}` (translate so the pose is `0`), let
`B = {x : r² − ‖x‖² > 0}` be the open ball on which the local description is valid, and set
`A = (F ∩ B) \ {0}`.

For `J ⊆ {1,…,N}` define

- `V_J := {x : g_j(x) = 0 for all j ∈ J}` — the zero set of a polynomial map, hence a real
  algebraic set (`V_∅ = R^n`);
- `U_J := {x : g_j(x) > 0 for all j ∉ J}` — finitely many strict inequalities
  (`U_{{1,…,N}} = R^n`).

Then `F = ⊔_J (V_J ∩ U_J)` is a partition by sign pattern, and `R^n \ {0} = {|z|² > 0}`.
Hence

```
A  =  ⋃_J  ( V_J  ∩  U_J  ∩  {|z|² > 0}  ∩  B )
```

a union of at most `2^N` sets, **each one exactly of Milnor's form**: a real algebraic set
intersected with finitely many strict polynomial inequalities. The ball `B` and the
puncture `{|z|² > 0}` are themselves strict polynomial inequalities, so they stay inside
the class.

Since the union is **finite**, `clos(⋃ A_α) = ⋃ clos(A_α)`, so `0 ∈ clos(A)` forces
`0 ∈ clos(A_α)` for at least one `α`. Milnor's Lemma 3.1 applied to that `A_α` yields a
real-analytic `γ : [0, ε) → R^n` with `γ(0) = 0` and `γ(t) ∈ A_α ⊆ A` for `t ∈ (0, ε)`.
Because `0 ∉ A`, this `γ` is nonconstant.

(If the global description is used instead of the local one, an outer finite disjunction
over separating-axis branches — X-012's `8^10` choices — precedes the sign-pattern
splitting. Only the finiteness matters.)

### 5.3 What the reduction requires, itemised

1. **Translation invariance** — Milnor states the lemma at the origin; polynomials
   translate, so this is free.
2. **Closure of the class under intersection with further strict inequalities** — holds by
   definition, and is what lets `B` and `{|z|² > 0}` be absorbed.
3. **`clos` commutes with finite unions** — true for *finite* unions only. The
   decomposition is finite; this must be said, not assumed.
4. **Non-strict `≥` must be split** into `> 0` / `= 0`, giving the `2^N` sign patterns.
   Milnor's class admits equations only through `V`. Note that `V` is the zero set of a
   polynomial *mapping*, so several simultaneous equations are native and no
   sum-of-squares combination is needed.
5. **Removing the point is a separate step**, and it is the one most likely to be skipped.
   `F \ {0}` is *not* of Milnor's form, and applying Milnor to `F` itself is useless: if
   `0 ∈ F` the lemma may legitimately return the constant arc. The `{|z|² > 0}` factor is
   what forces `γ(t) ≠ 0` for `t > 0`.
6. **Localisation must stay inside the class** — restricting to the neighbourhood `N` on
   which the twenty-inequality description is valid must be done by a strict polynomial
   inequality (an open ball, or `N` itself if it is a finite intersection of such).
7. **The reduction is standard.** Derdzinski–Gal's displayed remark (4.1) — "whenever
   `Z ⊂ S` and `L ⊂ S` are algebraic, one easily sees that `Z \ L` is a finite union of
   semi-algebraic sets in `S`" — is precisely this move, in print, in a peer-reviewed
   paper, immediately before they invoke Milnor's lemma.

Done this way, the Milnor route reaches the same conclusion as BCR 8.1.13, one strength
weaker (real-analytic rather than Nash), which is all the proof uses. **X-012's version of
this reduction is correct as written**; items 6 and 7 are the two things worth adding.

### 5.4 X-012's Milnor statement, checked

X-012 §4.1 states Milnor's Lemma 3.1 as follows, flagged there as "statement from memory":

> *if `V ⊂ R^m` is a real algebraic set and `U = {g_1 > 0, ..., g_l > 0}` with `g_i`
> polynomials, and `U ∩ V` contains points arbitrarily close to the origin, then there is
> a real-analytic curve `p : [0, ε) -> R^m` with `p(0) = 0` and `p(t) ∈ U ∩ V` for `t > 0`.*

**This matches the peer-reviewed restatement in §2.6 on every hypothesis**: real algebraic
`V`, finitely many *strict* polynomial inequalities `U`, origin in the closure of `V ∩ U`,
real-analytic curve on `[0, ε)`, `p(0) = 0`, and containment `p(t) ∈ V ∩ U` for `t > 0`.
Derdzinski–Gal attribute exactly this to "Milnor [14, p. 25]" and p. 25 is the opening page
of Milnor's §3. The "from memory" flag can be replaced by a citation to Derdzinski–Gal §4
as the corroborating restatement, with the honest note that Milnor's own printed page was
still not read.

## 6. Does the proof's set satisfy the hypotheses? Explicitly, yes

The set in question is `F \ {p}`, where `F` is the local feasible set of the `n = 5`
packing near Göbel's pose at fixed container side, cut out by finitely many polynomial
inequalities.

- **Semialgebraic.** `F` is defined by finitely many polynomial inequalities, hence
  semialgebraic; `{p}` is algebraic hence semialgebraic; semialgebraic sets are closed
  under set difference. So `F \ {p}` is semialgebraic. **This alone discharges every
  hypothesis of BCR 8.1.13.**
- **Closed and basic.** In H-060's intrinsic half-angle chart (`u = tan(θ/2)` with
  denominators cleared and kept positive) `F` is `{g_1 ≥ 0, …, g_M ≥ 0}` with no
  equalities: a **closed basic semialgebraic set**. If instead the pose is carried in
  `(cos θ, sin θ)` coordinates, `F` is `{h_i = 0} ∩ {g_j ≥ 0}` — a real algebraic set
  intersected with a closed basic set, which is *even better* suited to the Milnor route
  (the `h_i` go straight into `V_J`). Either presentation is fine; the chart form is the
  one that makes "closed basic" literally true.
- **Locally closed.** `F` is closed, `{p}` is closed, so `F \ {p} = F ∩ (R^n \ {p})` is the
  intersection of a closed set with an open set: **locally closed**. Satisfied.
- **`p ∈ clos(F \ {p}), p ∉ F \ {p}`.** The second is trivially true. The first is exactly
  the negation of "the pose is isolated in `F`", i.e. the hypothesis of the argument by
  contradiction. Satisfied by construction.
- **Localisation.** The twenty inequalities describe the feasible set only on a
  neighbourhood `N` of `p`, so the lemma must be applied to `(F ∩ N) \ {p}` with `N` an
  open ball. Intersecting with an open ball is intersecting with a strict polynomial
  inequality, which preserves membership in *both* hypothesis classes and preserves
  semialgebraicity. Local isolation is a local property, so this loses nothing. Say it
  anyway — it is the kind of step whose omission survives review.
- **Bounded.** `F ∩ N` is bounded (contained in a ball), so even the strictest reading of
  BCR's §2.5 section title is satisfied. Not needed, but free.

**Conclusion for §6:** every hypothesis of BCR Prop. 8.1.13 is satisfied outright; every
extra hypothesis that any of the weaker citable versions might impose — closed, basic,
locally closed, bounded, `x ∉ A` — is *also* satisfied. There is no hypothesis in this
family that the proof's set fails.

## 7. What to change in the proof artifact

1. **The BCR 8.1.13 statement in X-012 §4.1 is verified verbatim-equivalent and needs no
   change.** Strengthen only the provenance note: add the section reference (§8.1 "Germs
   of Nash Functions and Algebraic Power Series", pp. 161–166, located from the printed
   table of contents), add **Coste's own Theorem 1.15** (§2.3 above) as the closest thing
   to primary text — Coste is the "C" of BCR and states exactly this — and add the three
   further verbatim `[BCR, Prop. 8.1.13]` applications (§2.4), one of which applies it to a
   *difference* of semialgebraic sets and so rules out any hidden closedness or basic-ness
   hypothesis. Keep the honest statement that the printed BCR page was not read.
2. **Keep the application to `A := F \ {0}` and keep Corollary 4.3's nonconstancy
   derivation.** These are correct as written and they are what makes the `x ∈ Cl(A)`
   phrasing safe. Optionally add one sentence saying so, or cite Coste's Theorem 1.14/1.15
   (`x ∈ clos(A), x ∉ A`), which builds the guard into the theorem statement.
3. **X-012 Corollary 4.3 already takes the convergent Taylor series route, which is
   correct.** Add one clause noting *why* it is available: a Nash arc is real-analytic, so
   the identity theorem supplies a least `m` with `a_m ≠ 0` — no Puiseux series and no
   reparametrisation are needed. The **older X-007 text is the one that needs fixing**: it
   says "the curve selection lemma gives a semi-algebraic arc into the set, and Puiseux
   gives `gamma(s) = p + sum_{k >= m} a_k s^k`", which is the continuous-version route and
   requires an `s = u^N` reparametrisation to clear fractional exponents. Either write that
   reparametrisation there or replace the sentence with the Nash statement.
4. **The Milnor alternative route is sound as written.** Its statement of Lemma 3.1 matches
   the peer-reviewed restatement on every hypothesis (§5.4), so the "statement from memory"
   flag can be downgraded to "corroborated against Derdzinski–Gal §4, which cites Milnor
   p. 25; Milnor's printed page not read". Add the two missing items from §5.3: the
   localisation to `N` must itself be a strict polynomial inequality (item 6), and the
   finite-union step deserves the Derdzinski–Gal (4.1) precedent (item 7).
5. **Do not cite arXiv:2301.00128 for Milnor.** Its introduction attributes the
   arbitrary-semialgebraic Nash statement to Milnor; Milnor's own hypotheses are narrower.
   Cite BCR for the general statement and Milnor only with the reduction.
6. **Give BPR's number in both forms** if it is cited — Theorem 3.19 in the printed 2nd
   edition (2006), Theorem 3.22 in the authors' posted 2016 revision.

## Appendix — artifacts on disk

All under `scratchpad/bc152-curveselection/`:

| File | What it is |
| --- | --- |
| `src/bpr.pdf`, `src/bpr.txt` | Basu–Pollack–Roy, complete book (posted 2016-06-26). Theorem 3.22 at `bpr.txt` line 4113. |
| `src/coste-RAS.pdf`, `.txt` | Coste, *Real Algebraic Sets* (2005-03-23). Theorems 1.14, 1.15 on pp. 9–10. |
| `src/coste-SAG.pdf`, `.txt` | Coste, *An Introduction to Semialgebraic Geometry* (2002-10). Theorem 3.13, p. 55. |
| `src/bcr-toc.pdf` | Printed BCR table of contents (DNB scan). |
| `src/a1209.6084.*` | Derdzinski–Gal; §4 is Milnor's lemma with its restrictive definition. |
| `src/a2409.04232.*` | Delage–Fichou–Patel; Theorem 2.3 = `[BCR, 2.5.5]`. |
| `src/rag-ihp.*` | Plaumann, IHP 2023; Theorem 6.5. |
| `src/quantcsl.*` | Basu–Roy, *Quantitative Curve Selection Lemma*; Theorem 1. |
| `src/f1212.1811.*`, `src/f1503.05706.*`, `src/nashapprox.*`, `src/fernando2504.*` | The four verbatim `[BCR, 8.1.13]` uses. |
| `src/bifurcation.*` | Némethi–Zaharia; Milnor-shaped CSL at infinity. |
| `src/m1410.3312.*` | Massey; semianalytic CSL (Lemma 5.1). |
| `src/arcspaces.*` | Nguyen Hong Duc, arXiv:2301.00128 — the over-attribution to Milnor. |
| `extract.py`, `.sv/` | Text-extraction script and its isolated venv. |

The project virtualenv at `packing/.venv` was briefly used to test for a PDF library and
was restored to its prior state (`pypdf` uninstalled); all extraction ran in the scratchpad
venv `.sv`. No repository file was modified, added, or committed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
