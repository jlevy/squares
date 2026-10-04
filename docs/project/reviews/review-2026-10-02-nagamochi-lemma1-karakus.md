# Nagamochi’s Lemma 1 Is False: What T-007 Rests On Now

**Date:** October 2, 2026. **Lane:** A of bead `think-589i`, the W2 factual review of
`T-007`. Adversarial review by an AI reviewer at extra-high (`xhigh`) reasoning effort
(Claude Fable 5.1). This review reads the sources, recomputes the counterexample exactly
with a retained tool, audits the published replacement bound, and recommends register
statuses. It edits no register file.

Karakuş’s counterexample is correct.
Lemma 1 of [Nagamochi 2005], the per-square scoring assertion from which the paper’s
Theorem 1 (the rectangle bound) is deduced by summation, is false for every container
with $a > 3$ and $b > 2$: a family of squares of side $\sqrt{1+t^2}$, $0 < t \le 1/50$,
at the lower-left corner scores $19/20 + t + t^2/2 + t^3/2 < 1$ after a concentric
shrink. Recomputed here in exact rational arithmetic, the member $t = 1/50$ scores
$387566200425101/400000000000000 = 0.968916$ and the member $t = 10^{-6}$ scores
$0.950001$; chelokot’s independent square of side $10001/10000$ in $[0,4]^2$ scores
exactly the printed $25009470849041/25584000000000 = 0.9775434$.

The paper has no proof of Theorem 1 other than Lemma 1, and Theorem 2 is algebra on
Theorem 1 at a square container $a = b$. So the gap reaches Theorem 2 as `T-007` states
it for every $N \ge 10$: every open-case floor, the $k^2-1$ family and the $k^2-2$
family alike, not only $s(k^2-2) = k$. Nothing is disproved: no packing beating any
Nagamochi value is known, and the bound may be true.
Of the three consumers, two have replacement proofs and one has only a reported one.
$s(k^2-1) = k$ is proved again by Karakuş’s strip measure, which I audited and found
sound. The general floor is proved only in the weaker form
$s(N) \ge \tfrac12 + \sqrt{N - \lfloor\sqrt N\rfloor + \tfrac14}$ for nonsquare
$N \ge 8$, strictly below Nagamochi’s value at every $N$ that is not $k^2-1$ (at
$N = 14$: $3.854$ against $4$; at $N = 82$: $9.0586$ against $9.0623$). $s(k^2-2) = k$
rests on chelokot’s Lean compensation proof alone, which is reported here: its final
statement and the definitions it is written in were read and say what the claim says,
and its continuous-integration build audits axioms mechanically, but nothing was built
or replayed here and no receipt exists to read.
I did not repair the scoring argument: the two mass-preserving local repairs each rescue
Karakuş’s square and are each defeated by an axis-parallel square at the same corner,
with both witnesses retained in the tool.

## Sources and Review Scope

| Source | Pin | What was read |
| --- | --- | --- |
| H. Karakuş, *A counterexample to Nagamochi’s scoring lemma and a new rectangle packing bound*, [arXiv:2609.37410](https://arxiv.org/abs/2609.37410) v1, submitted 29 September 2026 | PDF fetched 2 October 2026 from the arXiv `pdf` endpoint, SHA-256 `39ae2ae44f063e6555240c4a246b47f687578c57196b70a9f5d66953d5cf6513`; a sibling lane archives it | The whole paper; Lemma 5.2(i)'s printed range checked on the rendered page |
| H. Nagamochi, *Packing Unit Squares in a Rectangle*, EJC 12 (2005) R37 | [retained PDF](../../../packing/resources/papers/nagamochi-2005-packing-unit-squares-in-a-rectangle.pdf) and its `.raw.md` | Sections 2 to 5 in full: Theorem 1, Theorem 2 and its proof, the set $U$, Lemmas 1 to 7, Cases 1 to 7 |
| chelokot, [square-packing-archive](https://github.com/chelokot/square-packing-archive) | `main` at `753079eb37d8d16225a5dc1f56e493a3c3b243f4` (committed 6 September 2026), fetched 2 October 2026 as a treeless clone; the counterexample note is retained by the archive lane in [`chelokot-nagamochi-counterexample-2026-10-02`](../../../packing/resources/web/chelokot-nagamochi-counterexample-2026-10-02/README.md), the rest pinned there by digest only | `docs/nagamochi-score-counterexample.md`, `docs/nagamochi-compensation-proof.md`, `docs/nagamochi-counterexample-search.md`, `docs/nagamochi-2005-formalization.md`; the theorem statements of `formal/SquarePackingArchive/NagamochiCounterexample.lean` and `NagamochiPackingTheorem.lean`; the definitions they are stated in (`Geometry.lean`); `formal/lean-toolchain`, `formal/lakefile.toml`, `formal/lake-manifest.json`, `.github/workflows/ci.yml`, `scripts/test_lean_axiom_policy.py` and the generated `ManifestEvidence.lean` |
| This repository | `T-007` and `E-nagamochi-lower` in the register, [`epistemics.md`](../../../epistemics.md), the [27 September evand review](review-2026-09-27-evand-s32-s12.md) section 5 | The claim, its read of 30 August 2026, the rubric |

The retained instrument is
[`devtools/check_nagamochi_lemma1_counterexample.py`](../../../packing/devtools/check_nagamochi_lemma1_counterexample.py)
with
[`tests/test_nagamochi_lemma1_counterexample.py`](../../../packing/tests/test_nagamochi_lemma1_counterexample.py):
35 tests in 0.48 seconds, the tool itself in 0.24 seconds, Ruff and BasedPyright at zero
findings. It scores a rational square against a measure of rectangles, axis-parallel
segments and points with `Fraction` arithmetic only, so every printed quantity below is
checked as an equality.
The Lean archive was not built here.
Its final theorem statements and the definitions they are written in were read; its 55
Nagamochi proof files, 16,603 lines, were not.
What it proves is reported, with what that report rests on set out below.

## Lemma 1 as Printed, and the Square That Refutes It

Nagamochi’s unavoidable set in $R = [0,a] \times [0,b]$, $a, b \ge 2$, is
$R^{\ast} = [1, a-1] \times [1, b-1]$ with area density $1$; four segments of line
density $1/2$, $L_1 = [(0.9, 1), (a-0.9, 1)]$, $L_2 = [(0.9, b-1), (a-0.9, b-1)]$,
$L_3 = [(1, 0.9), (1, b-0.9)]$, $L_4 = [(a-1, 0.9), (a-1, b-0.9)]$; eight points $Q$ of
weight $0.45$ at $(0.9, 1)$, $(a-0.9, 1)$, $(0.9, b-1)$, $(a-0.9, b-1)$, $(1, 0.9)$,
$(1, b-0.9)$, $(a-1, 0.9)$, $(a-1, b-0.9)$; and $2\lceil a\rceil + 2\lceil b\rceil - 12$
points $P$ of weight $0.5$ at $(i, 0.9)$, $(i, b-0.9)$ for
$i = 2, \dots, \lceil a\rceil-2$ and $(0.9, j)$, $(a-0.9, j)$ for
$j = 2, \dots, \lceil b\rceil-2$. The printed $P$ has $(i, a-0.9)$ and $(b-0.9, j)$, a
misprint that Figure 1 and the point count correct and that is immaterial when $a = b$.
The total is $ab - (a+1-\lceil a\rceil) - (b+1-\lceil b\rceil)$.

For $\lambda > 1$ the paper shrinks $R$ and $U$ toward the origin by $\lambda^{-1}$ and
scores a unit square $S$ inside $\lambda^{-1}R$ by

$$
\sigma(S) = \lambda^2 \mathrm{area}(S \cap R^{\ast}) + \tfrac{\lambda}{2}\sum_i \mathrm{length}(S \cap L_i) + 0.45 \mathrm{card}(S \cap Q) + 0.5 \mathrm{card}(S \cap P),
$$

the objects being their shrunk copies.
Lemma 1 reads, in full: “Any unit square $S$ inside $\lambda^{-1}R$ satisfies
$\sigma(S) > 1$.” Theorem 1 follows by summing over a packing.
The paper then states the equivalent form in which it argues and in which the
counterexample is given: *any `λ × λ` square `S` with `λ ∈ (1, 1.01]` has `σ(S) > 1`
over the original `R` and `U`*, with density $1$, $1/2$, $0.45$ and $0.5$ unscaled.
The scaling is exact, so the two statements are the same.
Whether a point on the boundary of $S$ counts is not specified; the counterexample is
arranged so that it does not matter.

Karakuş’s Section 4: fix $a > 3$, $b > 2$ and $0 < t \le 1/50$ with
$t < \min\lbrace10(a-3),\thinspace b-2\rbrace$. The contact square $K_t$ has vertices

$$
A = \bigl(2 - \tfrac{9}{10}t,\ 0\bigr),\quad
B = \bigl(2 + \tfrac{1}{10}t,\ 1\bigr),\quad
C = \bigl(1 + \tfrac{1}{10}t,\ 1 + t\bigr),\quad
D = \bigl(1 - \tfrac{9}{10}t,\ t\bigr),
$$

a square of side $\sqrt{1+t^2} \in (1, 1.01)$ with its corner $A$ on the $x$-axis,
tilted by $\arctan t$. Its chord at height $0.9$ is
$[1 - t^2, 2] \times \lbrace0.9\rbrace$, so $(1, 0.9)$ is interior and $(2, 0.9)$ lies
on the edge $AB$; $B$ is on $y = 1$; the chord on $L_1$ has length $1 + t^2$; the chord
on $L_3$ is $\lbrace1\rbrace \times [0.9, 0.9+t]$; the part above $y = 1$ is a triangle
of area $t(1+t^2)/2$ inside $R^{\ast}$; no other weighted object is met.
Hence $\sigma(K_t) = 29/20 + t + t^2/2 + t^3/2$ counting the boundary point, and

$$
\sigma(K_t) - \tfrac12 = \tfrac{19}{20} + t + \tfrac{t^2}{2} + \tfrac{t^3}{2}
\le \tfrac{242551}{250000} < 1 \quad (t \le 1/50).
$$

Shrinking $K_t$ about its centre by a factor below $1$ and close to it gives $S_t$ with
side still above $1$, $(1, 0.9)$ still interior, and $(2, 0.9)$ strictly outside, so
$\sigma(S_t) \le \sigma(K_t) - 1/2 < 1$ under either boundary convention.
Shrinking $K_t$ about $A$ instead leaves $(2, 0.9)$ in the relative interior of the
image of $AB$ while $y = 1$ cuts the images of $BC$ and $CD$: the edge carrying
$(2, 0.9)$ is not one of the two cut by $y = 1$.

The tool recomputes every sentence of that paragraph for
$t \in \lbrace1/50, 1/100, 1/1000,
10^{-6}\rbrace$ in the containers $[0,4]^2$, $[0, 7/2] \times [0, 5/2]$, $[0,10]^2$ and
$[0,33] \times [0,7]$, with shrink factor $\rho = 1 - t^2/8$, and finds each printed
quantity exactly: the chord endpoints, the three lengths, the area, the polynomial, and
the value $242551/250000$ at $t = 1/50$. The shrunken interior scores are $0.968916$,
$0.959416$, $0.950938$ and $0.950001$, the same in every container, as a construction
local to one corner must give.
As a control, $t = 1/10$ is refused by the family’s hypothesis and its contact square
scores above one; at $a = 3$ the hypothesis also fails, because $(2, 0.9)$ is then a $Q$
point and $L_4$ lies on $x = 2$, both of which $K_t$ meets.
Whether Lemma 1 holds at $a = 3$ or at $a, b \in [2, 3)$ is not decided here; the family
does not reach those containers, and the only proof offered for them is the refuted one.

chelokot’s square is of the same kind: side $10001/10000$, rotation with cosine
$80/1601$ and sine $1599/1601$, bottom vertex $(10419467/5330000, 0)$ in $[0,4]^2$, with
$(2, 0.9)$ outside by $10^{-4}$ at height $0.9$. The tool finds its interior score to be
exactly the archive’s printed fraction, below the archive’s Lean ceiling of $199/200$,
with no weighted point on its boundary.
The posted date is 5 September 2026 on the search note; its archive is the earlier
public record of the defect, and Karakuş’s paper does not cite it.

## Where the Published Proof Breaks

Section 5.5, Case 6: the centre of $S$ is in $[1, a-1] \times [0, 1]$ and $y = 1$ cuts
two adjacent edges $e_1, e_2$. Its last subcase has $S$ containing $(1, 0.9)$, no point
of $P$, none of $(0.9, 1)$, $(a-1, 0.9)$, $(2, 0.9)$ and, after the reduction, not
$(1,1)$. The text: *To estimate the minimum `σ(S)` in this case, we can assume that one
corner of `S` touches the `x`-axis and point `(2, 0.9)` is on an edge of `S`* \[...\]
“Then $\sigma(S) \ge d + 0.5c + 0.5 - 0.5c'$, which is greater than 1 by Lemma 6.” Lemma
6 assumes *two adjacent edges `e_1` and `e_2` of `S` intersect line `L : y = 1`* and
*point `(2, 0.9)` is on an edge `e_2` of `S`*, and its proof computes, for the
configuration of Figure 4(b) in which $e_1$ and $e_2$ meet at the apex above $y = 1$,
the cap area $d = t(1-t)/(1+t)$ and chord $c$ with $c + d = 1$ (the printed
$c = (t+t^2)/(1+t)$ contradicts the paper’s own *`c = 1 - d`*; the apex geometry gives
$c = (1+t^2)/(1+t)$, and nothing here rests on it).
In $K_t$ the point $(2, 0.9)$ is on $AB$, which does not cross $y = 1$ once the square
is shrunk about $A$; the edges cut by $y = 1$ are $BC$ and $CD$. The reduction reaches a
contact configuration that Lemma 6 does not cover, and in that configuration
$d + 0.5c + 0.5 - 0.5c' = 0.95 + t + O(t^2)$ is below one.
That is the whole of the gap: the chord and cap lemmas are not contradicted, and no
other case is implicated by the family.

What the 30 August read recorded as unverified were the trigonometric formulas inside
Lemmas 2, 3, 5 and 6 and the completeness of Case 5. The defect is in neither: it is a
hypothesis of Lemma 6 silently dropped at the point of use in Case 6. A read that
follows a proof’s structure does not catch that, which is the point of the register’s
rule that a read is `C1` and not more.

## What the Gap Reaches

The dependence is linear and complete.

| Step | Depends on | Status after this review |
| --- | --- | --- |
| Lemma 1, every $(a, b)$ | Cases 1 to 7 | False for all $a > 3$, $b > 2$; undecided for the rest |
| Theorem 1, $\nu(a,b) < ab - \Delta(a) - \Delta(b)$ | Lemma 1 and additivity; no other argument in the paper | Unproved; not disproved |
| Theorem 2(i), $s(N) = n$ for $N \in \lbrace n^2, n^2-1, n^2-2\rbrace$ | Theorem 1 at $a = b = n$ | Unproved for $n \ge 4$ by this paper; $n \le 3$ classical |
| Theorem 2(ii), $s(N) \ge \sqrt{N - 2\lfloor\sqrt N\rfloor + 1} + 1$ | Theorem 1 at $a = b = k + \alpha \in (k, k+1)$, $k = \lfloor \sqrt N\rfloor$ | Unproved for every $N \ge 10$ by this paper |
| `T-007`’s closed form $\min(\lceil\sqrt N\rceil, \sqrt{N - 2\lfloor\sqrt N\rfloor + 1} + 1)$ | Both parts of Theorem 2 | Correct algebra on an unproved theorem |

Here $\Delta(t) = t + 1 - \lceil t\rceil$. The Section 2 algebra, which the 30 August
read re-derived, is untouched: with $\alpha = \sqrt{N - 2k + 1} + 1 - k$ the identity
$(k+\alpha)^2 - 2\alpha = N$ holds, and the ceiling branch is exactly
$N \in \lbrace n^2, n^2-1,
n^2-2\rbrace$. For $N \in \lbrace4, 5, 6, 7, 8, 9\rbrace$ Theorem 2 is invoked at
$a = b \in \lbrace2,
1+\sqrt2, 1+\sqrt3, 3, 3, 3\rbrace$, where the family does not apply and where the
values are classical in any case ($s(4) = 2$, $s(5) = 2 + 1/\sqrt2$, $s(6) = s(7) = 3$,
$s(8) = s(9)
= 3$). For every $N \ge 10$ the parameter exceeds $3$ and the proof invoked is the
refuted one.

So the answer to the question posed is: the gap reaches Theorem 2 as `T-007` states it
for all $N$ in its scope at which the theorem is doing any work, through Theorem 1
itself and not only through $s(k^2-2)$. In kind, three sets of consumers are affected,
and lane B is counting them: the open-case floors that cite `E-nagamochi-lower` as their
verified lower bound (238 of 261 open cases by the frontier README); the $k^2-1$ cases
$N = 15, 24, 35, 48, 63, 80, 99$ in the hundred; and the $k^2-2$ cases
$N = 14, 23, 34, 47, 62, 79, 98$. The gate’s `check_nagamochi_bounds` re-derives the
closed form from the formula and will keep passing; it checks transcription, not truth,
and says so in its docstring.

## Repairs in the Literature

### Karakuş’s strip measure, audited here

Theorem 1.1 of the paper: for $a \ge 2$ and $b \ge 3$, $\nu(a,b) < ab - \Delta(a)$, and
for $a, b \ge 3$, $\nu(a,b) < ab - \max\lbrace\Delta(a), \Delta(b)\rbrace$. The measure
$\mu$ on $R$ is area density $1$ on the strip $H = [0,a] \times [1, b-1]$, line density
$1/2$ on $L_- = [0,a] \times \lbrace1\rbrace$ and
$L_+ = [0,a] \times \lbrace b-1\rbrace$, and mass $1/2$ at the points $(j, 4/5)$ and
$(j, b - 4/5)$ for $j = 1, \dots, \lceil a\rceil - 1$; its total is $ab - \Delta(a)$.
Proposition 5.1 says every square $S \subseteq R$ of side $\lambda \in (1, 1.01]$ has
$\mu(S^\circ) > 1$, and the theorem follows by the same scale-and-sum as Nagamochi’s,
with interiors so that nothing is counted twice.

I read the proof in full and re-derived each step.
Lemma 5.2 works with $h = \sin\theta + \cos\theta$ and
$p = \sin\theta\cos\theta = (h^2-1)/2$ for $\theta \in [0, \pi/4]$. Its chord profile
(5.3) is the standard three-piece profile of a tilted square.
Part (i), that a square with centre at height at most $1$ has an open chord of length
above one on every line $y = r$ with $\tfrac{3-\sqrt2}{2} < r <
\sqrt2 - \tfrac12$, rests on $h - p \ge \sqrt2 - \tfrac12$ and
$\tfrac{h}{2} - p \ge \tfrac{\sqrt2 - 1}{2}$, both decreasing on $[1, \sqrt2]$ and
attained at $h = \sqrt2$, and on the concavity of the profile; the only value used is
$r = 4/5$, which sits $0.0071$ inside the lower limit that the second inequality
requires. The `pdftotext` rendering of that range is garbled, and I confirmed it on the
rendered page. Part (ii), $A + \ell/2 \ge \lambda^2 - \lambda/2$ for the area above
$y = 1$ and the chord on it, reduces in the two-opposite-sides case to
$\lambda\sin\theta + \cos\theta \ge 1$ and in the cap case to
$\lambda - h + p > (h-1)^2/2 \ge 0$; both algebraic reductions check.
The open chord at height $4/5$ of length above one in $[0, a]$ contains an integer in
$\lbrace1, \dots, \lceil a\rceil - 1\rbrace$, which is where the point row earns its
$1/2$, and
$\mu(S^\circ) \ge \lambda^2 - \lambda/2 + 1/2 = 1 + (\lambda-1)(\lambda+\tfrac12)$
follows for centres at height at most $1$, with the top of such a square below $2 \le
b - 1$. For centres in the strip, the cap estimate (5.8) $D/\ell < 1/2$ and the three
cases (all cuts triangular; one chord of length at least $\lambda$ with at most half the
area lost; two such chords) each give more than one.
The case $b = 3$, where a square can cross both lines, is covered by the same three
cases. I found no gap.
This is a read, not a machine check; the tool verifies only the total (5.2) at rational
$a, b$ and that $\mu$ scores both Karakuş’s and chelokot’s squares above one, as the
proposition requires.

Consequences (Section 6), all read: Corollary 6.1, no $m' \times n'$ rectangle with
$m' < m$, $n' < n$ holds $mn - 1$ unit squares, for integers $m, n \ge 2$; Corollary
1.2, $s(k^2-1) = k$ for every $k \ge 2$ (from 6.1 at $m = n = k \ge 3$ and the grid;
$k = 2$ is $s(3) = 2$, classical); and Corollary 6.2, for every nonsquare $N \ge 8$ with
$k = \lfloor\sqrt N\rfloor$,

$$
s(N) \ \ge\ \tfrac12 + \sqrt{N - k + \tfrac14} \ >\ \sqrt N,
$$

by solving $t^2 - \Delta(t) = N$ on $(k, k+1]$ and applying Theorem 1.1 at $a = b = t
\ge 3$. Nagamochi’s Theorem 2(ii) solves $t^2 - 2\Delta(t) = N$ instead.
Exactly, with $u = N - k + \tfrac14$ and $v = N - 2k + 1$:
$\tfrac12 + \sqrt u \le 1 + \sqrt v$ holds if and only if $k - 1 \le \sqrt v$, that is
$k^2 \le N$, so Karakuş’s value is strictly below Nagamochi’s root at every nonsquare
$N$, and it is at most $\lceil\sqrt N\rceil$ with equality exactly at $N = (k+1)^2 - 1$.
The tool checks this for every nonsquare $N \le 1000$ and the test pins the review
values:

| $N$ | $\sqrt N$ | Nagamochi, `T-007` | Karakuş, Cor. 6.2 | What Karakuş recovers |
| --- | --- | --- | --- | --- |
| 7 | 2.645751 | 3 | not stated ($N \ge 8$ needed) | $s(8) \ge 3$ from $\nu(3,3) < 8$, not $s(7)$; $s(7) = 3$ is Kearney and Shiu |
| 12 | 3.464102 | 3.645751 | 3.541381 | a weaker floor |
| 14 | 3.741657 | 4 | 3.854102 | not $s(14) = 4$ |
| 23 | 4.795832 | 5 | 4.887482 | not $s(23) = 5$ |
| 26 | 5.099020 | 5.123106 | 5.109772 | a weaker floor |
| 34 | 5.830952 | 6 | 5.908327 | not $s(34) = 6$ |
| 47 | 6.855655 | 7 | 6.922616 | not $s(47) = 7$ |
| 82 | 9.055385 | 9.062258 | 9.058621 | a weaker floor |
| 97 | 9.848858 | 9.944272 | 9.894147 | a weaker floor |

At $N = k^2 - 1$ both give $k$ (not in the table; the test checks $k = 3, \dots, 19$).

### chelokot’s Lean archive, reported

The archive claims, in `docs/nagamochi-compensation-proof.md` and
`docs/nagamochi-2005-formalization.md`, a Lean proof of $s(n^2-2) = n$ for every integer
$n \ge 2$, square containers only, dated 5 September 2026: the identity Karakuş’s own
argument does not reach.
This subsection says what that claim is, what stands behind it mechanically, and what it
would take to earn a rung here.
Nothing was built or replayed.

**What the theorem says.** `NagamochiPackingTheorem.lean` (102 lines) ends in

```text
theorem Records.NearSquare.squareMinusTwo_isMinimumSide
    {size : ℕ} (size_lower : 2 ≤ size) :
    IsMinimumSide (size * size - 2) size
```

with `size = 2` discharged by `s2_eq_two`, `size = 3` by `Records.Square7.s7_eq_three`
(two unavoidable point sets after Kearney and Shiu), and `size ≥ 4` by the grid packing
and `Packing.squareMinusTwo_side_ge`, which rests on
`Packing.squareMinusTwo_impossible_of_scaled_fits`: a packing of $n^2-2$ squares at side
$L$ with $4 \le n$, a factor $1 < \lambda \le 101/100$ and $\lambda L \le n$ is
contradictory. Instances `s14_eq_four`, `s62_eq_eight`, `s79_eq_nine`, `s98_eq_ten`
follow by `simpa`. The definitions, in `Geometry.lean`: a `PlacedSquare` is a centre and
an orthonormal `Frame` (a cosine and sine with $c^2 + s^2 = 1$), so rotation is
arbitrary; `Contains` is the closed unit square ($|x'|, |y'| \le 1/2$ in local
coordinates) and `InteriorContains` the open one; `Container.Contains side` is the
closed square $[0, \mathrm{side}]^2$; `Packing n side` is $n$ placed squares, each with
its closed square inside the closed container (`Fits`) and pairwise without a common
interior point (`InteriorDisjoint`), so boundary contact is allowed; and
`IsMinimumSide n s` is `HasPacking n s` together with $s \le s'$ for every $s'$ that has
a packing. On my reading that is this register’s $s(N)$ exactly.
The reading is mine, of the definitions only; it is not the human formalization review
the ladder’s rung 5 names, and I read none of the proof files.

**What is formalized, by the archive’s own account.** Its formalization note tabulates
as kernel-checked: the resource measure and its total $n^2-2$; scaling, disjointness and
finite-measure counting; the conditional near-square theorem from the per-square premise
`ScoresDilatedSquares`, together with `not_scoresDilatedSquares_four`, that the premise
is false at $n = 4$; the per-square inequality for centres in the inner rectangle (Cases
1 to 4) and in the four corner regions (Case 5); the edge-strip inequality for squares
containing no $Q$ point; the universal inequality for the *augmented* measure, which
keeps Nagamochi’s area and extended lines and raises each $Q$ weight from $0.45$ to
$0.5$, giving `Records.NearSquare.squareMinusOne_isMinimumSide`, $s(n^2-1) = n$ for
every $n \ge 2$ (its total is $n^2 - 1.6$, enough for $n^2-1$ and not $n^2-2$, and the
tool confirms that this measure scores both witness squares of the next section above
one and sits exactly $2/5$ above Nagamochi’s total); and, for $n \ge 4$, the
compensation argument.
That argument keeps Nagamochi’s measure and shows every square of score at most one
contains exactly one $Q$ point and no $P$ point, follows a finite chain of owners of the
next marked points along that boundary row to a terminal, and pays the shortfall from
the terminal, a $P$ terminal paying at most two chains and a $Q$ terminal one, so that
after the transfers every square exceeds one while the total is unchanged.
The note states that Cases 6 and 7 of the per-square inequality “cannot hold as stated”
and that Nagamochi’s rectangular theorem “is not verified here.”
The archive also reports, as prose: that removing the short extensions to pay for higher
$Q$ weights fails even for an axis-aligned square; that exact linear inequalities from
four squares exclude any repair that changes the four symmetric weights at total
$n^2-2$; that simple pairwise compensation fails; and that a 24-start numerical search
found no packing of $62$ squares below side $8$. None of that was checked here.

**The axiom audit, and what exists of a receipt.** The archive’s CI
(`.github/workflows/ci.yml`, job `lean`) builds the library with
`leanprover/lean-action` at the pinned `leanprover/lean4:v4.33.0` with Mathlib at
`db584cd6d46c92f209a44c0f1c829460d327499d` (the lakefile’s `rev = "v4.33.0"`), rejects
any `sorry` by grep, runs `scripts/test_lean_axiom_policy.py`, and compiles the
generated `ManifestEvidence.lean`. That file carries 79 `assert_standard_axioms`
commands, one per theorem the archive’s manifest cites, among them `s14_eq_four`,
`s62_eq_eight`, `s79_eq_nine` and `s98_eq_ten`, whose transitive axioms include those of
the universal theorem, and `s63_eq_eight`, `s80_eq_nine`, `s99_eq_ten` and
`s7_eq_three`. The command, twelve lines in `EvidenceAudit.lean`, collects transitive
axioms with `Lean.collectAxioms` and fails the build on any outside `propext`,
`Classical.choice` and `Quot.sound`; the policy test shows it rejects `sorryAx` and
`native_decide`. So the audit the prose reports is mechanical at every upstream build,
and the manifest cites the theorem for its records `exact-14-friedman`,
`exact-62-nagamochi`, `exact-79-nagamochi` and `exact-98-nagamochi`. What does not exist
is a receipt: no audit output is retained in the repository, the CI log was not fetched,
and the archive lane here pinned the proof files by digest without retaining them.

**What a replay would take.** `elan` with the pinned toolchain; the Mathlib build cache
for the pinned revision (`lake exe cache get`, several gigabytes; building Mathlib from
source instead is many CPU-hours); `lake build` in `formal/` at `753079eb` (277 Lean
files, of which the 55 `Nagamochi*.lean` files are 16,603 lines; the lakefile sets
`-j2`; tens of minutes after the cache is a guess, not a measurement); then `lake env
lean --stdin` importing `SquarePackingArchive.EvidenceAudit` and
`SquarePackingArchive.NagamochiPackingTheorem` and running `assert_standard_axioms` and
`#print axioms` on
`SquarePackingArchive.Records.NearSquare.squareMinusTwo_isMinimumSide`, with stdout
retained as the axiom receipt; and a retained statement-fidelity note on `IsMinimumSide`
and `Packing`. That is the ladder’s proof-assistant route to `V3`/`C3` for the result;
`V5` needs a named human expert’s formalization review and `C5` two, with an open-review
pointer, which the public repository already supports.

Two of the three consumers therefore have proofs by two different methods each ($k^2-1$:
a strip measure in a refereed-venue preprint and an augmented measure in Lean), one has
a single reported proof ($k^2-2$), and the general floor has only the weaker published
bound. Karakuş states the square-container measure of total $k^2-2$ as an open question
and does not cite the archive.

## Can the Scoring Argument Be Repaired Here?

No, not by a local redistribution of mass at the corners, and the reason is exact.
Let $\beta$ be Karakuş’s shrunken square at $t = 1/50$ and let $\alpha$ be the
axis-parallel square $[0.9, 1.91] \times [0, 1.01]$, whose left side lies on the column
of $(0.9, 1)$ so that point is on its boundary and uncounted.
In $[0,4]^2$, Nagamochi’s measure gives $\alpha$ exactly $10191/10000$ and $\beta$
$0.968916$. The square $\alpha$ collects $(1, 0.9)$, the whole of both extensions at the
corner $(1,1)$ (the pieces $[0.9, 1] \times \lbrace1\rbrace$ and
$\lbrace1\rbrace \times [0.9, 1]$, worth $0.05$ each) and little else; $\beta$ collects
$(1, 0.9)$, a chord of length about one on $y = 1$, and only $t$ of the vertical
extension because its tilted left edge slides off the line $x = 1$. The design pairs
each $Q$ point ($0.45$) with its extension ($0.05$) to make $0.5$; $\alpha$ needs the
extensions, $\beta$ needs the point to carry the whole $0.5$.

The tool builds three variants and scores both squares:

| Measure in $[0,4]^2$ | Total | $\alpha$ | $\beta$ |
| --- | --- | --- | --- |
| Nagamochi | $14$ | $1.0191$ | $0.9689$ |
| `weight`: $Q \to 0.5$, extensions dropped | $14$ | $0.9691$ | $1.0095$ |
| `slide`: extensions dropped, a $0.1$ segment attached to each $Q$ point along its own row or column | $14$ | $0.9691$ | $1.0095$ |
| `augment`: $Q \to 0.5$, extensions kept (chelokot) | $14.4$ | $1.0691$ | $1.0189$ |

Both mass-preserving variants rescue $\beta$ and are defeated by $\alpha$ at exactly
$9691/10000$. Moving the vertical extension below the $Q$ point, or keeping one
extension and moving the other, fails in the same way on $\alpha$ or on the reflected
copy of $\beta$ at the left wall; those hand computations are not in the tool.
In the limit $\lambda \to 1$ the two squares share no line segment of positive length
near the corner, so no redistribution onto rows and columns serves both; the archive’s
reported four-square inequality says the same for symmetric reweightings.
A repair must therefore change the measure globally (Karakuş’s open question: a measure
on $[0,k]^2$ of total at most $k^2 - 2$ with every $\lambda$-square above one) or argue
globally (chelokot’s chains).

I attempted neither.
The obligation for any candidate measure $\mu'$ on $[0,k]^2$ is exact and worth writing
down, since it is also what would make `T-007`’s $k^2-2$ family first-party: (O1)
$\mu'([0,k]^2) \le k^2 - 2$; (O2) $\mu'(S^\circ) > 1$ for every square
$S \subseteq [0,k]^2$ of side $\lambda \in (1, 1.01]$, a universal statement over a
three-parameter family that needs either a complete case analysis of the kind Nagamochi
attempted or an exact pose-space subdivision of the kind this repository already runs
for its closed covers; and (O3) a localization argument carrying a check at one $k$ to
all $k$, as the evand $k^2-3$ family has.
None of (O1) to (O3) is done here, and nothing above should be read as progress on them.

## Claims by Evidential Status

Computationally verified here, in exact arithmetic, by the retained tool: every printed
quantity of Karakuş’s Section 4 and Appendix A at the four declared $t$ in four
containers; the scores of $S_t$ and of the vertex-shrunk square below one; chelokot’s
score as the printed fraction; the totals of Nagamochi’s set, the strip measure and the
three variants; the $\alpha$ and $\beta$ scores above; the exact ordering $\sqrt N < $
Karakuş $\le$ Nagamochi with equality only at $N = m^2 - 1$, for nonsquare $N \le 1000$.

Read and re-derived here, not machine-checked: Karakuş’s Lemma 5.2, Proposition 5.1,
Theorem 1.1 and Corollaries 1.2, 6.1 and 6.2; Nagamochi’s Section 2 algebra; the
location of the gap in Case 6 and the inapplicability of Lemma 6 to $K_t$; the hand
computations in the repair section that are not in the tool.

Reported, unverified here: everything the chelokot archive proves in Lean, which is the
two near-square theorems, the per-square cases its note lists as kernel-checked and the
counterexample theorem; the axiom audit those rest on, which its continuous integration
performs at each build and which produced no receipt I could read; its negative results
on repairs; and its numerical search.
Read here and not replayed: the final theorem statements and the definitions
`PlacedSquare`, `Frame`, `Contains`, `InteriorContains`, `Container.Contains`,
`Packing`, `Fits`, `InteriorDisjoint`, `HasPacking` and `IsMinimumSide`, which on my
reading state this register’s $s(N)$.

Open, asserted by no one: Nagamochi’s Theorem 1 in full; Theorem 2(ii) at its full
strength; $s(k^2-2) = k$ by any route other than the reported Lean proof.
No Nagamochi value is contradicted by any known packing.

## Recommended Statuses

The rubric is [`epistemics.md`](../../../epistemics.md).
The ladder has no rung for a published proof whose lemma is refuted; the nearest honest
reading is that the claim is recorded with a defect found, and the status rule makes
that `incomplete` on its own once the evidence entry says `defect-found` and nothing has
replayed past it.

| Claim | Rests on now | Recommended | Why |
| --- | --- | --- | --- |
| `T-007` as stated, Theorem 2’s closed form at every $4 \le N \le 100$ | A published proof with a refuted lemma; no replacement at full strength | `V0`/`C1`, status `incomplete`; `E-nagamochi-lower.external_review` to `defect-found` dated 2 October 2026 with this review as the record | `V3` means a checkable published proof; there is none. The read stands at `C1` and found the defect |
| General floor at $N \notin \lbrace k^2-1, k^2-2\rbrace$, as a verified bound | Karakuş Cor. 6.2, read here | New evidence from arXiv:2609.37410, `published-proof`, `V3`/`C1`, at the weaker value; Nagamochi’s value stays as a reported bound | The replacement is published and audited; it is not machine-checked |
| $s(k^2-1) = k$, $k \ge 3$ | Karakuş Cor. 1.2 (read here); chelokot’s augmented measure in Lean (reported) | `V3`/`C1` on the strip-measure proof; the Lean route stays reported until replayed | Two independent methods exist; one is audited |
| $s(k^2-2) = k$, $k \ge 4$ | chelokot’s compensation proof in Lean only: statement read here, definitions read here, build and axioms not replayed, no retained receipt | Recorded, `V0`/`C0`, until the replay set out above (pinned `v4.33.0` and Mathlib `db584cd6`, `lake build` at `753079eb`, an `assert_standard_axioms` and `#print axioms` receipt on `squareMinusTwo_isMinimumSide`, a statement-fidelity note) is retained, which gives `V3`/`C3`; `V5` needs a human formalization review. Meanwhile the verified floor at $N = 14, 23, 34, 47, 62, 79, 98$ falls to Karakuş’s value and their optimality reads as reported | No published proof survives; a third-party formal claim earns a rung here only by replay, and an unreplayed Lean claim is not verified |
| Lemma 1 of [Nagamochi 2005] is false | This tool, on Karakuş’s family and chelokot’s square | A `correction` result, `S3`, with the tool as exact-algebraic evidence (`replayed-here`) and the test as its control | The counterexample is a finite exact computation and is retained |

`S3` for `T-007` is unchanged: the result is no less important for being unproved.
The consumer inventory, the evidence edits and any new result entries are the
coordinator’s and lane B’s; this review recommends and edits nothing in the register.
One more thing belongs in the record: the 30 August read judged the paper’s spine sound
with four named unverified items, and the defect was elsewhere.
The register’s rule that a read is `C1` and never more is what kept that judgment from
being overstated.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
