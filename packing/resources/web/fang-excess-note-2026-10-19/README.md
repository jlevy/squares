# Kevin Fang’s Note on n² − n + 1 Squares Below Side n, Draft v0.9

Kevin Fang’s note *Packing n² − n + 1 unit squares in a square of side less than n, for
every n ≥ 15*, draft v0.9 of 18 October 2026, holds the proof of the two theorems the
record registers as `T-163`. Until 18 October the record had only the theorems’
statements and the certificates behind them, retained at `078789a` in the
[13 October packet](../fang-excess-theorem-2026-10-13/README.md); the note itself was not
public. Fang published it on Zenodo, under DOI
[10.5281/zenodo.23463481](https://doi.org/10.5281/zenodo.23463481), and in Markdown in his
certificate repository, and announced both on
[jlevy/squares#603](https://github.com/jlevy/squares/issues/603) (comments
[6255103888](https://github.com/jlevy/squares/issues/603#issuecomment-6255103888) of 18
October and
[6259031488](https://github.com/jlevy/squares/issues/603#issuecomment-6259031488) of 19
October). Bead `think-494l` owns this retention and the statement audit below.

Its Frontier key is **[Fang excess note 2026-10-19]**. Fang’s Lean formalization, which
the note cites as [FanL26], is the
[18 October Lean packet](../fang-excess-lean-2026-10-18/README.md).

## Source and Pin

| Field | Value |
| --- | --- |
| Zenodo record | [23463481](https://zenodo.org/records/23463481), version 0.9, publication date 2026-10-18, created 2026-10-19T03:28:26Z; concept DOI `10.5281/zenodo.23463480`; resource type preprint; one creator, Kevin Fang |
| Zenodo files | `fang-2026-n2-n-1.pdf`, 125,257 bytes, MD5 `beadf4508e65444d956a475e31f0e99e` (the record’s), SHA-256 `a44402f8da2523c2fdda79f6a639ecb3b03dfbe92fb7400ba2c75e8d46ef95d5`; `fang-2026-n2-n-1-tex.zip`, 12,388 bytes, MD5 `653bd4d351120ef4c11862f30af1d7f4`, SHA-256 `3ba5e8696f3ca49ec482719cc5012a6bd6774cd451f483fe16d7ca934ea7818f`, one member `main.tex`, 31,726 bytes, SHA-256 `532b233f74464fed4ce072b732189944c609f9eee74bf105345ff29899415e86` |
| Repository | [TheSnakeFang/squarepack-certs](https://github.com/TheSnakeFang/squarepack-certs/tree/9ffba0f3a84b38f0c92790c1d3089f979ef53f0b) at `9ffba0f3a84b38f0c92790c1d3089f979ef53f0b`, tree `33f93a883895ed672329b2d9d4568da34d4a9092`, committed 2026-10-19T03:29:59Z, the head when read: “README: scope the Lean formalisation statement” |
| History since `078789a` | `0e9be79` (2026-10-18T20:43:07Z) adds `note/fang-2026-n2-n-1.md`, draft v0.8; `6e26525` (2026-10-19T03:29:42Z) makes it v0.9 with the DOI; the pin changes one line of the README. No other path changed since `078789a` |
| Licence | The Zenodo record: CC BY 4.0, for the PDF and the LaTeX source. The repository’s README names no licence for `note/`; its code is MIT and its certificates CC0 1.0, as at `078789a` |
| Retrieved | The repository at 2026-10-24T04:57Z, a blobless clone with a sparse checkout of the pin; the Zenodo record at 2026-10-24T05:08:03Z |

## Credit and AI Assistance, as the Source States Them

The note has one author, Kevin Fang. Its Acknowledgements and credit section (printed
p. 6) reads, verbatim:

> The decomposition and the $n^2 - n + 1$ packings for $n = 16, 17, 18$ are due to
> Arslanov, Mustafin and Shangitbayev; the $n = 15$ packing to Joost de Winter.
> The seed packings are David Ellsworth’s and Tej Stead’s ($241, 273, 307$) and Francisco
> Couzo’s ($342$). The certificate format, one of the checkers and the exact certificates
> of the known packings used as pieces are Evan Daniel’s, who also improved three of our
> packings. The Squares Project (Joshua Levy) independently replayed all three initial
> certificates, registered the 308 result, and recorded 343 and 344 as verified
> beyond-horizon bounds. The search software, the verifiers, the gluing program and the
> certificate bundle were written and run with Claude (Anthropic) as a coding and research
> agent, directed and reviewed by the author; two language-model reviews of earlier
> drafts (GPT-6 Astra; OpenAI Codex) found errors that were corrected, which is not an
> external mathematical review. The Lean formalisation reuses Evan Daniel’s specification
> and certificate lemmas (MIT).

The repository’s README at the pin says the same of the bundle: “Search, verifier and
this bundle were written and run with Claude (Anthropic) as a coding and research agent,
directed and reviewed by Kevin Fang.” The three commits since `078789a` carry a Claude
(Anthropic) co-author trailer. The credit the record gives, **Fang after Arslanov,
Mustafin, Shangitbayev, Ellsworth, Stead, de Winter, Daniel, Couzo**, is the 13 October
packet’s, and the note names the same people in the same roles.

## What Is Retained

`devtools.acquire_source` wrote [`source/`](source/) from the declaration in
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. [acquisition/sources.json](acquisition/sources.json) is the record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
seven files, 80,609 bytes.

- **Retained, two files:** [`source/note/fang-2026-n2-n-1.md`](source/note/fang-2026-n2-n-1.md),
  the note in Markdown, 138 lines, and [`source/README.md`](source/README.md).
- **Pinned by digest, five files** that `078789a` already held, each compared byte for
  byte with the 13 October packet’s copy: `ATTRIBUTION.md`, `CHANGELOG.md`, `LICENSE`,
  `VERIFICATION.md` and `MANIFEST.sha256`. The changelog and the manifest do not mention
  the note.
- **The Zenodo record**, under [`zenodo/`](zenodo/), written by
  `devtools.capture_web_source zenodo 23463481 --extract main.tex`: the record and its
  file listing as Zenodo served them, the archive’s member manifest, the
  [receipt](zenodo/zenodo-23463481-receipt.json) with each file’s stated and computed
  digests, and the extracted [`main.tex`](zenodo/zenodo-23463481/main.tex). The tool
  refuses a file whose size or MD5 is not the record’s. The archive itself is not kept.
  The PDF, which the tool does not write, is kept as
  [`zenodo/fang-2026-n2-n-1.pdf`](zenodo/fang-2026-n2-n-1.pdf), downloaded at
  2026-10-24T04:56:41Z with the MD5 and SHA-256 the receipt records.

The author says the Markdown is “the same text” as the Zenodo version.
The three forms were compared here by reading, not by a program, since they are three
formats: the title, the abstract, both theorems, Lemma 3 and its proof, Propositions 4
and 5, the proof of the theorems, the Formal verification paragraph and the
acknowledgements read the same in the Markdown, in `main.tex` and on pages 1 to 6 of the
PDF. The LaTeX source’s first line says it was “converted from docs/note-draft.md
(v0.9)”.

## The Claims of the Note

**Theorem 1** (p. 2). $s(n^2 - n + 1) < n$ for every integer $n \ge 15$.

**Theorem 2** (p. 2). Let $n \ge 15$ and let $p, q \ge 0$ be integers with
$16p + 21q \le n - 15$. Then $n^2 - n + 1 + p + 2q$ unit squares pack in a square of side
less than $n$. In particular $s(n^2 - n + F(n)) < n$ with
$F(n) = 1 + \max\{p + 2q : p, q \in \mathbb{Z}_{\ge 0},\ 16p + 21q \le n - 15\}$.

$s(N)$ is the smallest side of a square containing $N$ unit squares with disjoint
interiors, rotations allowed (Section 1); a packing is a family of closed unit squares in
the box with pairwise disjoint interiors (Section 2). That is the record’s $s(n)$.

**The proof** (Section 2, pp. 2–3) has four parts:

- **Lemma 3**, the four-piece gluing of Arslanov, Mustafin and Shangitbayev: a
  $d$-squeezable packing $A$ of $ab - w_A$ squares in $a \times b$ and a $d$-squeezable
  packing $B$ of $a'b' - w_B$ in $a' \times b'$, with $n = b + b'$, $c = n - a'$,
  $n \ge a$, $0 \le c \le a - d$ and $0 < d \le 1/2$, give $n^2 - w_A - w_B$ squares in
  side $n - d$, with two integer blocks.
- **Proposition 4**, the rectangles: $R$, 257 squares in
  $(17 - \delta_R) \times (16 - \delta_R)$, $\delta_R \ge 0.0007436$, waste 15; and $R'$,
  443 squares in $(22 - \delta_{R'}) \times (21 - \delta_{R'})$,
  $\delta_{R'} \ge 0.0094396$, waste 19.
- **Proposition 5**, the bases: $n^2 - n + 1$ squares below side $n$ for
  $15 \le n \le 26$ (de Winter’s 211; the packings of 241 and 273 of Arslanov, Mustafin
  and Shangitbayev as refined by Ellsworth and Stead; 307 from the author’s 308 less one
  square; the author’s direct packings for 19 to 26), and $m^2 - m$ below side $m$ for
  $11 \le m \le 14$; every piece of Propositions 4 and 5 is $1/10000$-squeezable.
- **The induction**: every gluing at $d_0 = 1/10000$, $R$ adding 16 to the side and 1 to
  the excess, $R'$ adding 21 and 2, from the bases at $15 \le n \le 30$; every composite
  has side exactly $n - 1/10000$, and a uniform scaling by $1 + d_0/(2(n - d_0))$ makes it
  a strict certificate of side $n - 1/20000$.

Propositions 4 and 5 are the computer-checked part. The note states them by their exact
rational certificates in the bundle at `078789a`, which its three exact checkers accept
(Section 6); its text does not reproduce them. Section 5 states the 50 inventory
certificates of $n^2 - n + F(n)$ squares at side exactly $n - 1/20000$ for
$15 \le n \le 64$, the files the 13 October packet holds.

**Formal verification** (Section 6, p. 5): Lean 4 formalises Theorem 1 and “the maximum
of the two unmixed bounds in Theorem 2 … the mixed-step form of Theorem 2 is not
formalised”, with `#print axioms` listing `propext`, `Classical.choice` and `Quot.sound`
for all three theorems.

## The Statements Against T-163

The audit of 24 October compared the statements, their hypotheses and their conclusions,
and read no proof against another.

| Statement | Hypotheses | Conclusion | Against `T-163`’s claim |
| --- | --- | --- | --- |
| Note, Theorem 1 | integer $n \ge 15$ | $s(n^2 - n + 1) < n$ | Equal to `T-163`’s Theorem 1 |
| Note, Theorem 2 | $n \ge 15$; integers $p, q \ge 0$, $16p + 21q \le n - 15$ | $n^2 - n + 1 + p + 2q$ squares below side $n$; $s(n^2 - n + F(n)) < n$ | Equal to `T-163`’s Theorem 2, whose $F(n)$ leaves $p, q \in \mathbb{Z}_{\ge 0}$ implicit |
| Note, the construction (Section 2, Section 5) | as Theorem 2 | composites at side $n - 1/10000$, closed; strict certificates at $n - 1/20000$ | Equal to `T-163`’s “side $n - 1/20000$ at every $n \ge 15$”; its finite bounds $s(211) \le 14.99995$ to $s(307) \le 17.99995$ are the Section 5 certificates at $n = 15$ to 18 |
| Fang’s Lean, `theorem1` | `(n : ℕ) (h : 15 ≤ n)` | `minSide (n ^ 2 - n + 1) < n` | Equal to Theorem 1 under Daniel’s `Spec.lean`, whose `minSide` is `sInf {s | Packs n s}`, closed unit squares at any rotation in $[0, s]^2$ with pairwise disjoint interiors |
| Fang’s Lean, `main` | `(n : ℕ) (h : 15 ≤ n)` | `Packs (n ^ 2 - n + 1) ((n : ℝ) - 1 / 10000)` | Stronger than Theorem 1: side $n - 1/10000$ for the count of Theorem 1 |
| Fang’s Lean, `theorem2` | `(n : ℕ) (h : 15 ≤ n)` | `minSide (n ^ 2 - n + jExc n) < n`, `jExc n = max ((n + 1) / 16) (1 + 2 * ((n - 15) / 21))` | Weaker than Theorem 2 where mixing $p$ and $q$ gains (below) |
| Daniel’s Lean, `theorem1` (`T-236`) | `(n : ℕ) (hn : 15 ≤ n)` | `∃ s < (n : ℝ), Packs (n * n - n + 1) s` | Equal to Theorem 1, under the same `Spec.lean` |
| Daniel’s Lean, `theorem2` (`T-236`) | `(n p q : ℕ) (hn : 15 ≤ n) (hpq : 16 * p + 21 * q ≤ n - 15)` | `∃ s < (n : ℝ), Packs (n * n - n + (1 + p + 2 * q)) s` | Equal to Theorem 2 in its $(p, q)$ form, mixed steps included |

Fang’s vendored `Sqlean/Vendor/Spec.lean` has the same Git blob, `fa4a6248`, as the copy
of Daniel’s `Spec.lean` the
[7 October Daniel packet](../evand-exact-and-local-reports-2026-10-07/README.md) retains,
and the [18 October Daniel Lean packet](../evand-fang-ryu-lean-2026-10-18/README.md) pins
the same bytes, so both formalizations state their theorems over one definition of
`Packs`. For $N \ge 1$, `minSide N < n` holds exactly when some `Packs N s` holds with
$s < n$, since the set of feasible sides is nonempty and bounded below by 0: Fang’s and
Daniel’s forms of Theorem 1 say the same thing.

**Where Fang’s `theorem2` falls short of Theorem 2.** Write $k = n - 15$. The note’s
$F(n) - 1$ is $G(k) = \max\{p + 2q : 16p + 21q \le k\}$, and `jExc n` $- 1$ is
$H(k) = \max(\lfloor k/16 \rfloor, 2\lfloor k/21 \rfloor)$, the best of the pure steps,
since $\lfloor (n + 1)/16 \rfloor = 1 + \lfloor k/16 \rfloor$. A mixed pair needs
$p, q \ge 1$ and so $k \ge 37$; below that $G = H$, and `theorem2` is Theorem 2 for
$15 \le n \le 51$. At $k = 37$, $n = 52$, $p = q = 1$ gives $G = 3$ against
$H = \max(2, 2) = 2$, so `jExc 52` $= 3$ and $F(52) = 4$; the note’s Section 5 lists
$F(n) = 4$ for $52 \le n \le 56$, where `jExc` is 3. The gap is never more than one:
$p + 2q \le 2(16p + 21q)/21$ gives $G(k) \le 2k/21$, and $H(k) \ge 2\lfloor k/21 \rfloor
\ge 2(k - 20)/21$, so $G - H \le 40/21 < 2$. Fang’s Lean proves Theorem 1 in full and
Theorem 2 with an excess of $F(n)$ or $F(n) - 1$; the note and the repository’s README at
the pin say so. At the four counts `T-163`’s scope lists, $n = 15$ to 18, $F(n) = 1$ and
every statement above gives $s(n^2 - n + 1) < n$.

Two notes for the author, neither changing the mathematics:

- **The Lean repository’s README overstates its scope.** Its first line at `947bdae`
  says “Kernel-checked Lean 4 proof of Theorems 1 and 2”, and `Theorem2.lean` calls
  `jExc` “The excess of Theorem 2”; the note and the certificate repository’s README at
  the pin say Theorem 1 and the unmixed bounds.
- **One citation is easy to misread.** Section 6 says “the mixed-step bound is proved
  here [FanL26]”; *here* is the note, and [FanL26] does not prove it.

## What This Packet Supports, and What It Does Not

The note is a published proof of both theorems for every $n \ge 15$, with its finite
inputs given as certificates. The record’s
[`E-fang-excess-note-proof`](../../../frontier/evidence.yaml) cites it as a
`published-proof` with its `proof` block; that is the predicate `epistemics.md` gives
`V3` for a proof that has been published. It is not a review: no stage 4 review has read
the note’s proofs against the
[14 October review](../../../../docs/project/reviews/review-2026-10-14-fang-excess-theorem-and-direct-certificates.md),
which re-derived both theorems from the README and `tools/glue.py` before the note was
public. The 18 pieces of Propositions 4 and 5 were decided strict-valid by that review’s
own exact checker, and the six inventory certificates the record holds by both
maintained exact routes (`E-fang-excess-theorem-exact-feasibility`).
No program of the source was run here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
