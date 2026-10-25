# Kevin Fang’s Theorem A, $c^*(k) < 4\sqrt{2k} + 1$ for Every $k \ge 6$: Mathematical Review

**Verdict: accept with findings.
The proof is complete and correct for every $k \ge 6$.** Every inequality it uses was
re-derived here and decided symbolically, and programs written here from the note alone
decided the construction exactly at every $k$ from 6 to 250,000. Two minor findings
concern the note’s illustrative and comparative text (M-1, M-2), and twelve notes
concern presentation, credit and the record.
None is blocking or major.

The source is Kevin Fang’s note *Packing $k^2 - \lceil\sqrt{32k}\,\rceil - 1$ unit
squares in a square of side less than $k$*, draft v0.2 of 24 October 2026
([10.5281/zenodo.23624565](https://doi.org/10.5281/zenodo.23624565)), reported on issue
[#797](https://github.com/jlevy/squares/issues/797) and retained in
[fang-theorem-a-2026-10-24](../../../packing/resources/web/fang-theorem-a-2026-10-24/README.md)
as `source/theorem-a/note/main.tex` (SHA-256 `f6f26d7b…1152`) and `main.pdf`
(`fdc87cb6…257a`). Line numbers below are of `main.tex`, page numbers of the five-page
PDF. v0.1 ([10.5281/zenodo.23624412](https://doi.org/10.5281/zenodo.23624412)) has the
same mathematics: v0.2 changes only the credit and comparison text.
The result has no `T-NNN`; PR #801 records it as a reported row of
`deficiency_upper_bounds` in `packing/frontier/asymptotic-waste-bounds.yaml`, after Evan
Daniel’s earlier row.

Reviewer: Claude, strongest tier, maximum reasoning (`tbd-strong-max`; acting name
`c-review-797-math`, bead `think-qmqq`), the stage 4 mathematical lane of the #797
import for the intake pass `coord-intake-1024`, in a worktree of its own at PR #801’s
head `a3e826606`. It read the source as data, ran only code it wrote, and kept that code
in the packet under
[`review/review-2026-10-25/`](../../../packing/resources/web/fang-theorem-a-2026-10-24/review/review-2026-10-25/README.md).
The findings were written, at 02:23Z on 25 October (SHA-256 of that text
`d0c35b5e…3146`), before this review read the maintained
`packing/cases/asymptotic/fang_theorem_a.py`, the stage 1 triage’s notes or the model
review (Comparison).
It is not a human oversight record.

## Summary for the Author

- **The theorem holds.** Sections 2 to 5 prove it for every $k \ge 6$. Every identity
  and polynomial inequality the proof uses was decided symbolically here.
  These include (E1), (E3), the floor pairing of Lemma 2 and the rearrangement of Lemma
  3, and the final $b(b^2+1)^2(\kappa_b - 1/b - 1/(b^2+1)) = 6b^4 - b^3 - 2b^2 - b > 0$.
  The geometry of the filled band ends is complete (Theorem A Re-Derived).
- **Your numbers reproduce.** Programs written here from the note, without reading or
  running yours, found:
  - the bound at every $k$ from 6 to 250,000, with both odd widths where there are two;
  - every square of 46 packings up to $k = 101$ valid;
  - your least slack, $B(k) - w = 8019401/78023840599$ at $k = 19{,}705$;
  - the sharpness remark true for every odd $b$ from 5 to 2001;
  - every comparison of Section 7.
- **Two sentences need changing, neither in the proof.**
  - The fixed-squeeze example of Section 6 does not reproduce with the squeeze read as
    $k - S$, as the bullet before it defines the squeeze; it reproduces with
    $t - 1/b = 10^{-7}$ (M-1).
  - “Not a new record for any range of $k$” (Section 7) contradicts your own counts: the
    integer bound is strictly the smallest stated bound at about half of all $k$, in
    runs of hundreds of consecutive $k$ (M-2).
- **Smaller points.**
  - “Rounding loss below $3/2$” in the abstract is undefined, and as uncovered level
    length it exceeds $3/2$ at a few band ends (N-1).
  - The sharpness remark has no proof (N-3).
  - The rest are clarifications (N-4 to N-12).

## Scope and Evidence

Read, in this order:

1. `result-import.md`, stage 4, and `epistemics.md`’s rules for kept code.
2. The packet’s README. It summarises what the maintained module decided (its ranges,
   its 60,167 pairs, the least slack, 75 refused mutants), so those headline figures
   were known before any program here ran.
3. The note v0.2, TeX and PDF, in full.
4. The register rows PR #801 adds, which repeat those figures, and
   `deficiency_family.py` for its definition of $c^*(k)$ and its statement texts.
5. Ryu’s preprint v1.1, retained in
   [squarepacker-k2-minus-c-upper-v11-2026-10-10](../../../packing/resources/web/squarepacker-k2-minus-c-upper-v11-2026-10-10/README.md):
   Sections 1 to 6 and the start of 7.
6. Daniel’s packet README and the header of `RyuLayers.lean`.
7. v0.1’s TeX, as a diff.

The intake coordinator’s assignment said that the stage 1 triage had found no gap; the
triage’s notes were not opened until the findings were written.

Not read: the source’s `lband.py`, `windowed_check.py` and `regenerate.sh`, its
certificates, and the checkers the note uses.
None of them was run.

The claim reviewed is Theorem 1 of the PDF with Lemmas 2 and 3, the sharpness remark,
and the comparisons of Section 7 and the abstract.
Nothing here decides the 36 shipped certificates, which the records lane’s replay holds.

## The Claim and the Notion

Theorem 1 of the PDF (line 59, page 1), which the issue, the register and this review
call Theorem A, states: for every integer $k \ge 6$, $w(k) < 4\sqrt{2k} + 2$, where
$w(k) = k^2 - M(k)$ and $M(k) = \max\{N : s(N) < k\}$. Equivalently
$c^*(k) < 4\sqrt{2k} + 1$, so $c^*(k) \le \lceil\sqrt{32k}\,\rceil$, and $s(n) < k$ for
every integer $n \le k^2 - \lceil\sqrt{32k}\,\rceil - 1$.

**It is the register’s statement.**

- The note’s $c^*(k) = \max\{c : s(k^2 - c) = k\}$ (line 46) is `deficiency_family.py`’s
  definition word for word, and the row PR #801 adds states all three forms.
- The reduction $c^*(k) = w(k) - 1$ (line 48) holds: $s$ is nondecreasing, $s(k^2) = k$
  by area and the grid, and $M(k)$ is the largest of a nonempty set of integers below
  $k^2$.
- For the integer $w(k)$, $w < 4\sqrt{2k} + 2$ is $(w - 2)^2 < 32k$ when $w \ge 2$, and
  it is exactly $c^* \le \lceil\sqrt{32k}\,\rceil$: an integer $m$ is below $x$ exactly
  when $m \le \lceil x \rceil - 1$. So the integer form loses nothing.
- $\sqrt{32k}$ is an integer only at $k = 2m^2$, where the bound $8m + 2$ on $w$ has no
  slack from a ceiling.
  These are the $k$ where $\sqrt{2k}$ is an even integer and two odd widths are
  admissible.
- The container’s side is $S = k - b + W$, strictly below $k$ because $W < b$.

## Theorem A Re-Derived

### The band (Section 2, page 2)

With $c = (1 - t^2)/(1 + t^2)$ and $s = 2t/(1 + t^2)$, a row is the $b \times 1$
rectangle $P$ in frame coordinates $(u, v)$, with corner at $(s,\ y_0 + j\sec)$.

- (R1) holds since $X - s = uc - vs$ is linear, with extremes $-s$ at $(0, 1)$ and $bc$
  at $(b, 0)$.
- (R2) holds since the shift $(0, \sec)$ changes $v$ by $c\sec = 1$ and $u$ by
  $s\sec = T$.
- (R3) holds since $Y$ increases in $u$ and $v$.
- $F = L - (R-1)\sec - h \in [0, \sec)$ since $R - 1 = \lfloor (L - h)c \rfloor$.
- $W < b$ for every $t > 1/b$ follows also from $W - b = 2t(1 - bt)/(1 + t^2)$.

(E1) is two identities, $Y - y - (X - s)T = v/c$ and $Y - y - (s - X)/T = u/s$, each
nonnegative because every row has $u, v \ge 0$ in row 0’s frame.
A square under the graph of $\ell$ and a row above it can meet only on that graph, which
has empty interior. The end region is therefore the whole part of the band below the
first row, bounded by both lower sides of row 0. That is slightly larger than the
trapezoid $\mathrm{Reg}(y)$ of Ryu’s Section 6, and the note proves what it needs about
it.

(E2) holds level by level.
If $a_i \ge s$, then $a_i = s + (i + 1 - y)\tau$ unclipped, $\ell(a_i) = i + 1$ exactly,
and $\ell$ increases on $[a_i, W] \supseteq [W - m_i, W]$. If $a_i < s$, then
$i + 1 < y = \min \ell$.

(E3) is an identity: the rotation by $\pi$ maps the point $(u, v)$ of row $j$ to the
point $(b - u, 1 - v)$ of a row with lift $y_1 + (R - 1 - j)\sec$. The two fills are
disjoint because, on every vertical line $X \in [0, W]$:

- the near fill lies below row 0, by (E1);
- the far fill lies above row $R - 1$, by (E1) after the rotation;
- row $R - 1$ is row 0 translated up by $(R - 1)\sec$, and every row meets the line, by
  (R1).

So a graph separates the two fills, even when $R = 1$.

### The packing (Section 3, page 2)

The grid, the band of length $S$ and the reflected band of length $k - b$ lie in
$[0, k-b]^2$, $[k-b, S] \times [0, S]$ and $[0, k-b] \times [k-b, S]$, whose interiors
are disjoint. Identity (1) is the count $k^2 - (k - b)^2 = bk + b(k - b)$ rearranged.
It is an equality for the construction, and $w(k)$ is at most the construction’s waste
because $s(N(t)) \le S < k$.

### Closeness (Section 4, page 3)

At $t_0 = 1/b$:

- $W_0 - s_0 - \tau_0 = (b - 1)/2 + \delta_b$, with
  $2b(b^2 + 1)\delta_b = (b - 1)(b^2 - 2b - 1)$, positive for $b \ge 3$, and
  $\delta_b < 1/2 + 1/(2b) \le 1$;
- $\eta_0 = 1/(2b)$, $2\tau_0 - bc_0 = (b^2 - 1)/(b(b^2 + 1))$ and
  $3 - h_0 = 4/(b^2 + 1)$.

So (a) to (d) hold strictly at $t_0$, and each is continuous in $t$. A scan of 512
points at each of 54 widths finds the close set to be one interval
$(1/b, 1/b + \varepsilon_b)$, with $\varepsilon_b b^3$ tending to 1. That is the scale
at which (c) fails: its margin is about $1/b$ at $t_0$, and it shrinks at a rate of
about $b^2$.

### Lemma 2 (lines 110–123, page 3)

For $0 \le y < \sec$ no $a_i$ is clipped, since $s + (1 - \sec)\tau = c(1 - c)/s > 0$.
Level 0 has length $z + \tau$ and level 1 has length $z$. Since $b$ is odd,
$\tau = (b - 1)/2 + 1/2 - \eta$ with $(b - 1)/2$ an integer.

The floor pairing is right in both cases.
Write $z = n + f$:

- if $f < 1/2 + \eta$, the sum is $2n$, which exceeds $2z - 1 - 2\eta$ by
  $1 + 2\eta - 2f > 0$;
- otherwise it is $2n + 1$, which exceeds $2z - 1$ by $2 - 2f > 0$.

The tie $f = 1/2 + \eta$ falls in the second case, as the note has it.
The bound is sharp: a lift with $f = 1/2 + \eta - 10^{-25}$ leaves a slack of
$2 \cdot 10^{-25}$. It also holds when $z < 0$, where level 1 is empty and
$\lfloor z \rfloor < 0$ is still a lower bound.

### Lemma 3 (lines 127–137, page 3)

Put $R = 1 + c(L - h - F)$ and subtract the right side of (2) from
$bL - [bR + (b - 1)/2 + (b - 1)/2 + 2z_F - 1 - 2\eta]$. The difference is exactly
$F(bc - 2\tau)$, as a polynomial identity, so (c) and $F \ge 0$ give (2). The value at
$t_0$, $2bL/(b^2 + 1) + b + 2 - \kappa_b$, and the four values the proof quotes, are
identities.

### The theorem (Section 5, page 3)

- An odd $b$ with $|b - \sqrt{2k}| \le 1$ always exists, and $b \ge 3$ for $k \ge 6$.
- $k - \sqrt{2k} - 1 \ge 3$ is $(k - 2)(k - 8) \ge 0$; for $k = 6$ and 7, $b = 3$ and
  $k - b \ge 3$.
- $H$ is a rational function of $t$, with $H(1/b) = B(k)$ and $S(1/b) = k$.

$B(k) = 4\sqrt{2k} + (2/b)(b - \sqrt{2k})^2 + 2 + 2/(b^2 + 1) - 2\kappa_b - 4k/(b(b^2 + 1))$
identically. So $|b - \sqrt{2k}| \le 1$ and the final polynomial give
$B(k) < 4\sqrt{2k} + 2$, and continuity gives a close $t$ with $H(t)$ below the bound.
The proof does not need $t$ to be rational.

## What the Checks Decide, and Their Trust Boundaries

**The proof needs no computation.** Every step is an identity, a polynomial inequality
or a continuity argument, valid for every $k \ge 6$. The runs below are checks of it and
of the stated numbers, not premises.

**The note’s programs.** `lband.py` builds the construction in exact rationals, and
`windowed_check.py` drives two certificate checkers on overlapping windows (Section 6).
Neither was read or run here.
The proof does not rest on them, and the certificates they produced are the replay
lane’s.

**The programs written here** trust CPython’s integers and `Fraction` for every decision
except two:

- the identities use sympy 1.14.0’s simplification of rational functions to 0;
- the two comparisons with real constants (Daniel’s $k^{2/5}$ bound and Ryu’s Theorem
  1.2) use mpmath 1.3.0 at 50 digits.
  A value within $10^{-30}$ of an integer is refused, and a perfect fifth power, where
  the value is rational (for example 4910 at $k = 15^5$), is evaluated in rationals.

The geometry check finds candidate pairs by an exact integer centre distance and decides
each by exact separating axes.
Floating-point values in the receipts are reports only.

**The maintained `fang_theorem_a.py`**, written from the note by the records lane,
trusts `Fraction`. It decides the polynomial identities by evaluating them at more
points than their degree, and samples Daniel’s $k^{2/5}$ crossover every 1,000 $k$.

**What they share.** The programs here import nothing from the repository or the source,
and their authors had not read the maintained module when they decided.
Both implementations and the source are Claude’s, by their authors’ statements, and both
read the note’s construction the same way: the same $R$, $F$, levels and placement of
the far fill. A misreading common to both would not show as a disagreement.
The exact layout of every square at 46 packings tests this reading against the note’s
geometry, and the general argument above does not depend on it.

## Independent Checks

`fang_a_identities.py`, `fang_a_review.py` and `fang_a_comparisons.py`, written from the
note, ran on 25 October 2026 with the project interpreter (CPython 3.14.7) under `nice`,
at most two processes at a time.
Their README records each program’s SHA-256 and every receipt.

| Check | Range | Result |
| --- | --- | --- |
| Every identity and polynomial inequality of Sections 2–5 and the remark, symbolically | all $b$, $k$, $t$ | 46 hold; 4 mutated identities refused |
| The construction at a chosen close rational $t$: (a)–(d), $S < k$, $k - b > h$, identity (1), Lemma 2 at all four ends, Lemma 3 for both bands, $w < H(t)$, $H(t)$ and $w$ below $4\sqrt{2k} + 2$, $B(k)$ below it | $6 \le k \le 250{,}000$ with both widths at a tie: 250,347 pairs | all hold; $t = 1/b + 1/(b(b^2+1)(6k_b + 4b))$, $k_b = \lfloor (b+1)^2/2 \rfloor$, never needed reducing |
| The one-sided limit count as $t \to 1/b^+$, by exact power series in $t - 1/b$ | $6 \le k \le 20{,}000$: 20,094 pairs | least $B(k) - w = 8019401/78023840599$ at $k = 19{,}705$, $b = 199$, $w = 796$, as the note states; equal everywhere to the count at the chosen $t$ |
| Lemma 2 at sampled lifts, ties included, with (E2) square by square; Lemma 3 at sampled lengths, $F = 0$ and $F$ just below $\sec$ included | 54 odd widths from 3 to 2001, about 14 close $t$ each spread over the close interval | 291,401 and 133,989 cases hold; least slacks $2 \cdot 10^{-25}$ and $3.0 \cdot 10^{-4}$ |
| The whole chain, $w(t) < H(t)$, at close $t$ far from $1/b$ | $6 \le k \le 400$ and five larger $k$ | 5,807 cases hold, $H(t)$ below the bound at all of them |
| Every square inside $[0, S]^2$, unit, with pairwise disjoint interiors, and the count equal to $N(t)$ | $k = 6$–40, 50, 59, 72, 98, 101, both widths at ties: 46 packings | all valid; 49 mutated packings refused |
| $k = 2m^2$, both widths | $2 \le m \le 1000$ | 1,998 pairs hold; the waste is at most $8m$, 2 below the bound |
| The sharpness remark | odd $5 \le b \le 2001$ | waste $4b$ in the limit; $4b$ at every sampled close $t$ for $b \le 61$ |
| The comparisons of Section 7 and the abstract, and the register’s counts | to $10^6$, with tail lemmas | all as stated (Comparisons below) |

The whole review used about 0.2 CPU-hours.

**Comparisons, against the register’s statements.** The note’s statements of Ryu’s
Theorems 1.2, 1.3, 1.4 and 1.6 and of T-163 match the register rows and Ryu’s v1.1. In
integers, with tail lemmas the receipt prints:

- **Against Daniel.** Theorem A is smaller at 495,210 of $7 \le k < 10^6$, Daniel’s
  bound at 255,215, and they tie at 249,568. They differ by at most 2 from $k = 89$, and
  for every $k \ge 102$ by the tail lemma.
  Below 89, Daniel’s is smaller by 3 to 5 at 17 values: 7, 8, 10, 11, 14, 15, 16, 20,
  21, 27, 28, 35, 43, 44, 53, 64 and 88.
- **Against Daniel’s $k^{2/5}$ bound.** It is first smaller at $k = 735{,}988$, and
  smaller at every $k$ from 736,595, so “about $7.4 \cdot 10^5$” holds.
- **Against Ryu’s Theorem 1.4.** Theorem A is smaller at 6 and from 9, ties at 7, and is
  larger at 8.
- **Against Ryu’s Theorem 1.3 at its best $b$.** Theorem A is larger at 6 to 11, ties at
  12 and 13, and is smaller from 14.
- **Against T-163.** Theorem A is larger at 15 to 39, ties at 40 and 41, and is smaller
  from 42.
- **Against Ryu’s Theorems 1.2 and 1.6.** Theorem 1.2 is smaller at $1.6 \cdot 10^7$
  (15,738 against 22,628) and beyond.
  Theorem 1.6 gives 1583, 3972 and 10039 against 1789, 5657 and 17889.
- **The register’s own counts.** Theorem A is strictly the least statement at 346,919 of
  $42 \le k \le 702{,}000$, and below Daniel’s at 346,920.

## Findings

| Id | Grade | Where | Finding |
| --- | --- | --- | --- |
| M-1 | minor | main.tex line 162 (with 161), page 4 | The fixed-squeeze example does not reproduce with the squeeze as line 161 defines it |
| M-2 | minor | main.tex line 179, page 4 | “Not a new record for any range of $k$” contradicts the note’s own per-$k$ comparison |
| N-1 | note | main.tex line 37, page 1 | “Rounding loss below $3/2$” is undefined; as uncovered level length the far end can exceed it |
| N-2 | note | main.tex lines 20–21, 58, 110, 127; pages 1–3 | The PDF numbers Theorem 1, Lemma 2, Lemma 3; the record says Theorem A, Lemma 1, Lemma 2 |
| N-3 | note | main.tex lines 153–155, page 4 | The sharpness remark is stated without proof |
| N-4 | note | main.tex line 37; line 141 | “The odd integer nearest $\sqrt{2k}$” is two integers at $k = 2m^2$ |
| N-5 | note | main.tex lines 44, 66, 141 | $N$, $c$ and $s$ each carry two meanings |
| N-6 | note | main.tex line 48 | That $s$ is nondecreasing is used and not stated |
| N-7 | note | main.tex line 70, page 2 | The derivative argument for $W < b$ does not cover $t \ge 1$ |
| N-8 | note | main.tex line 80, page 2 | The disjointness of the two fills is complete but terse |
| N-9 | note | main.tex line 161, page 4 | A squeeze $k - S$ does not determine a rational $t$ |
| N-10 | note | main.tex line 37; line 164 | “Certificates for $k \le 600$” and “independently written” overstate |
| N-11 | note | main.tex lines 62 and 183 | The credit is right; one precursor of the axis layers could be named |
| N-12 | note | main.tex lines 2 and 34 | The TeX comment names a v0.3 that the note is not |

**M-1. The fixed-squeeze example.** The first bullet of Section 6 (line 161) defines the
squeeze as $k - S$. At $k = 43{,}218$, $\sqrt{2k} = 294$ and the bound
$4\sqrt{2k} + 2 = 1178$ is an integer.

- With $k - S = 10^{-7}$ the construction has waste 1176 at both odd widths, 293 and
  295\. There $H(t) = 1177.978$, and $t$ fails condition (c).
- Waste 1178 appears with $t - 1/b = 10^{-7}$ and $b = 293$, where
  $k - S = 2.00004 \cdot 10^{-7}$.
- A scan of $k - S$ from $10^{-9}$ to $10^{-5}$ first reaches 1178 near
  $2.0 \cdot 10^{-7}$ at $b = 293$ and $3.2 \cdot 10^{-7}$ at $b = 295$. Wherever it
  appears, $t$ fails (c) and (d).

The example shows a $t$ outside the close interval, which the theorem does not cover.
That is a sound reason why a fixed squeeze fails, since $\varepsilon_b$ is about
$b^{-3}$; but the number matches only the other reading of “squeeze”.
The text should say which quantity is $10^{-7}$ and that $t$ is not close there.
The proof does not use the example.
Receipts: `outputs/squeeze.json`, and `outputs/squeeze-conditions.json` for the
conditions that fail.

**M-2. “Not a new record for any range of $k$”** (line 179).

- By the note’s counts (line 173), $\lceil\sqrt{32k}\,\rceil$ is strictly below
  $4\lceil\sqrt{2k-7}\,\rceil - 1$ at 495,210 of $7 \le k < 10^6$.
- Writing $x = \sqrt{2k}$, this happens about when the fractional part of $x$ lies in
  $(0, 1/2]$. So these $k$ come in runs of about $\sqrt{2k}/2$ consecutive values, one
  of 703 ($996{,}876$ to $997{,}578$).
- Against every statement the register holds, the bound is strictly the least at 346,919
  of $42 \le k \le 702{,}000$, in runs of up to 589 consecutive $k$ ($700{,}932$ to
  $701{,}520$).
- Under the register’s rule that a tie stays with the earlier report, Theorem A holds
  the smallest stated bound at those $k$.

What is true is that its asymptotic strength is Daniel’s and that neither integer bound
is the smaller at every $k$. The sentence should say that.
Receipt: `outputs/comparisons.json`.

**N-1. “Rounding loss below $3/2$.”** The body does not define it.
Measured as the uncovered length of the levels, $\sum_i (W - a_i) - \mathrm{fill}$:

- the near end loses less than $1/2$ at every $k$ computed here (at most 0.4979);
- by Lemma 2’s case analysis, the far end can lose up to $3/2 + \eta$, plus a sliver of
  level 2 shorter than $2/(b(b^2 + 1))$;
- the far end loses more than $3/2$ at 1,058 of the 500,694 far band ends with
  $6 \le k \le 250{,}000$, most at $k = 14$, $b = 5$ (1.5664).

What stays below $3/2$ is Lemma 2’s deficit $1 + 2\eta$, measured from $(b - 1)/2 + 2z$,
while $\eta < 1/4$. A definition, or “about $3/2 + \eta$”, would make the abstract’s
sentence exact. Receipts: `outputs/construction.json` and
`outputs/construction-extension.json`.

**N-2. Numbering.** The lemma counter is shared with the theorem’s (lines 20–21), so the
PDF prints Theorem 1, Lemma 2 (the fill) and Lemma 3 (the band).
The issue, the packet README and the register row call them Theorem A, Lemma 1 and Lemma
2, and the row’s `constant` cites “(Lemma 2)” for the band estimate.
The record’s side of this is under For the Records Lane.

**N-3. The sharpness remark has no proof.** It holds in every case computed here:

- in the limit $t \to 1/b^+$, the waste at $k = (b^2 - b + 8)/2$ is exactly $4b$ for
  every odd $b$ from 5 to 2001, with $b$ the only admissible width;
- for $b \le 61$, the waste is $4b$ at every sampled close $t$, not only near $1/b$;
- the expansion $31/(2b) + O(b^{-2})$ is an identity of series, and
  $(4\sqrt{2k} + 2 - 4b)\,b$ lies between 15.50 and 15.99 for every such $b$, tending to
  $31/2$.

A proof, or the range checked, would let a reader rely on the remark.

**N-4. The nearest odd integer.** At $k = 2m^2$ the abstract’s “the odd integer nearest
$\sqrt{2k}$” is two integers, $2m \pm 1$. Section 5’s “an odd integer with
$|b - \sqrt{2k}| \le 1$” is the precise form, and both widths work at every such $k$
checked here.

**N-5. Notation.** $N(x)$ is the largest count in side $x$ (line 44), and $N(t)$ is the
construction’s count (line 141). $c$ and $s$ are $\cos\theta$ and $\sin\theta$ (line
66), and also the deficiency variable of $c^*(k)$ and the side function $s(N)$.

**N-6. Monotonicity of $s$.** Line 48’s “$s(k^2 - c) < k$ exactly when
$M(k) \ge k^2 - c$” uses that removing squares keeps a packing, which the note does not
state.

**N-7. $W < b$.** The derivative argument (line 70) is stated for $\tan\theta > 1/b$,
which says nothing about $t \ge 1$, although the conclusion holds there.
$W - b = 2t(1 - bt)/(1 + t^2)$ covers every $t > 1/b$ in one line.
Only $t$ near $1/b$ is used.

**N-8. The two fills.** “Since each vertical line $X = \text{const}$ meets row 0 and row
$R - 1$” (line 80) rests on the three facts listed under (E3) above; a sentence could
name them.

**N-9. A rational $t$ from a squeeze.** Given $k - S = e$, $t$ solves
$(2b - e)t^2 - 2t - e = 0$ and is irrational in general, while Section 2 fixes a
rational $t$. How `lband.py` obtains its $t$ bears on M-1, not on the proof.

**N-10. The certificate sentence** (line 37 and line 164).

- “Certificates for $k \le 600$” means 38 values: 6 to 40, 101, 300 and 600.
- The 300 and 600 certificates are not published; `LARGE.sha256` states their digests.
- Both checkers were written with Claude, by their authors’ statements: the note’s
  acknowledgement and Daniel’s `CREDITS.md`. “Independently written” is independence of
  authorship within one AI system family.

**N-11. Credit.**

- The credit to Ryu matches his v1.1. The L is his Sections 3 and 4 (Lemmas 3.4 and
  4.1). The lifted-row end framework, with the far end as the $180^\circ$ image of the
  near one, is his Lemma 6.1 and Corollary 6.2.
- The credit to Daniel matches his packet.
  `RyuLayers.lean` fills the four band ends with axis squares, and Daniel committed it
  at 05:44:46Z on 18 October and pushed it at 15:47:56Z, six days before v0.1.
- One addition would make the history complete.
  Right-justified axis-parallel layers in a band end, running to the wall, are already
  one ingredient of Ryu’s Section 7 staircase (S5), after Bui’s primitive construction,
  where they replace the lower squares of tilted columns.
  What Daniel and this note add is an end made of such layers alone, at
  $b \approx \sqrt{2k}$.

**N-12. Version label.** The TeX comment (line 2) says the note was built from
`docs/theorem-a.md` (v0.3), while the note is Draft v0.2 (line 34); the Markdown source
is not in `theorem-a/`.

## Questions for the Author

1. In Section 6’s second bullet, is the fixed squeeze $10^{-7}$ the quantity $k - S$ of
   the first bullet, or $t - 1/b$, and which width does the example use?
2. What does “rounding loss of each filled end” in the abstract measure?
3. Would you restate the last sentence of Section 7 as a per-$k$ comparison?
4. Is there a proof of the sharpness remark for every odd $b \ge 5$? If it is
   computational, over which $b$?
5. How does `lband.py` obtain a rational $t$ from a chosen squeeze?
6. Is there a v0.3 of the note, and does its mathematics differ from v0.2’s?

## Significance

The draft score is S2, and this review keeps it.
The claim is a bound family, $c^*(k) \le \lceil\sqrt{32k}\,\rceil$ for every $k \ge 6$.
Daniel’s earlier $4\lceil\sqrt{2k-7}\,\rceil - 1$ already has the constant $4\sqrt2$ and
the same idea, so this is a second proof.
Its integer bound is smaller by 1 or 2 at about half of all $k$, and its odd-width
pairing (Lemma 2) is a neat device that changes the bound by at most 2. It moves no case
$n \le 324$ and no theorem.

## For the Records Lane

- **The review raises the row.** The row’s `note` says the review is pending; it can now
  say that the proof was re-derived in this review (accepted with findings; no blocking
  or major finding) and what the review’s own programs decided.
  - The deficiency rows carry no `reviews` or evidence field, so, as with Ryu’s rows,
    the record of the review is that prose.
  - `evidence.yaml` scopes entries by count, and no case record would cite a count the
    theorem reaches, so an entry for the review’s run needs a deferral or a decision.
  - The drafts are in the review directory’s `record-changes.md`: three `verifiers.yaml`
    records, the row’s new text and a count-scoped entry with that caveat.
- **Lemma numbers.** The register row’s `constant` and the packet README call the band
  estimate “Lemma 2” and the fill estimate “Lemma 1”. The retained PDF prints them as
  Lemma 3 and Lemma 2, and the theorem as Theorem 1. Cite the PDF’s numbers, or say once
  that the record renumbers them (N-2).
- **The row’s constant.** It says each band term is “below
  $2bL/(b^2+1) + b + 2 - \kappa_b$ … as $t \to 1/b$”. Each is below the right side of
  (2) at $t$, whose limit is that value.
- **The comparison window can widen.** Daniel’s unregistered $k^{2/5}$ bound is not
  smaller than Theorem A at any $k$ below 735,988 (exhaustively, not every 1,000). The
  register’s “not smaller at 702,000 and smaller at 748,000” can read “first smaller at
  735,988, and smaller at every $k$ from 736,595”. The window $[42, 702{,}000]$ is sound
  as it stands.
- **A slip in `fang_theorem_a.py`.**
  - The tail check `tail_100` evaluates `4 * 200 - 7 + 2 * isqrt(200 * 193) >= 28 * 28`.
    At $k = 100$, $(\sqrt{2k} + \sqrt{2k - 7})^2 = 4k - 7 + 2\sqrt{2k(2k - 7)}$, which
    is $393 + 2\sqrt{38600}$, not $793 + \ldots$.
  - The check passes for the wrong reason.
    The true premise holds, $393 + 392 = 785 \ge 784$, so no conclusion changes; the
    expression should be `4 * 100 - 7`.
- **“Confirmed”.** Wherever the row, the case material or the reply says confirmed, it
  should say which: the construction is independently re-implemented clean-room, by a
  Claude agent, a system family the producer also used.
  The 36 certificates’ replay shares the maintained routes’ components.
- **The reply.** The questions above, with M-1 and M-2, are for the author, in the
  answer bead.

## Comparison

**With the maintained `fang_theorem_a.py` and its receipts**, read after the findings.

- **Agreement.** It and the programs here agree on every number both compute:
  - 60,167 pairs to 60,000 and the least slack;
  - the waste $4b$ at its 25 sharpness widths;
  - the counts 495,210, 255,215 and 249,568, with the 17 values below 89;
  - 346,919 and 346,920;
  - the thresholds against Ryu’s Theorems 1.3 and 1.4 and against T-163;
  - Ryu’s Theorem 1.2 at $1.6 \cdot 10^7$.
- **The same reading of the note.** It reads the construction as this review does, with
  the same $R$, $F$, $a_i$, $m_i$ and far-fill placement, and stops at the first empty
  level. That is equivalent, since $a_i$ is nondecreasing in $i$.
- **Differences in method.** It chooses $t - 1/b = 1/(1000k^3)$ where this review
  chooses $1/(b(b^2+1)(6k_b + 4b))$. It decides the identities by evaluation at more
  points than their degree, where this review uses symbolic simplification.
  It checks $w < H(t)$ as one inequality, where this review checks Lemmas 2 and 3 at
  each end and band.
- **What it does not cover.** It does not test the lemmas across the close interval, the
  fixed-squeeze example (M-1) or the abstract’s rounding loss (N-1). It samples Daniel’s
  $k^{2/5}$ crossover, and its `tail_100` expression has the slip above.

`fang_a_comparisons.py` was revised once after this reading, at 02:25Z, to report the
first $k$ where Daniel’s $k^{2/5}$ bound is smaller and its margin at $10^6$.
`fang_a_squeeze_conditions.py` was written afterwards to record which conditions fail in
M-1’s example, and decides nothing about the theorem.
`fang_a_identities.py` and `fang_a_review.py` are byte for byte the programs that
decided before the reading.

**With the stage 1 triage** (c-triage-797-1024, notes read after the findings).
It re-implemented the construction from the note and reproduced the same headline
figures to 60,000. It read the proof line by line and found no gap, which this review
agrees with. It passed over the fixed-squeeze remark as “a remark on method” without
testing it, so M-1 is new here, as are M-2 and the notes.
Its draft significance, S2, is kept.

No earlier review of Theorem A is in the record.
The note reports two blind language-model reviews run by its author (line 183), which
are not retained and were not read here.

## Verdict

Theorem A holds: the note’s Sections 2 to 5 prove $w(k) < 4\sqrt{2k} + 2$, and so
$c^*(k) \le \lceil\sqrt{32k}\,\rceil$, for every integer $k \ge 6$, which is exactly the
register row’s statement.
Accept with findings.
The two minor findings and the notes go to the author and the records lane, and none
holds the row.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
