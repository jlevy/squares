# The Filled-End Lemma: Deciding Karimi’s Two-Band L Packings From Their Parameters

**Status:** ready for its stage 4 mathematical review (think-fuwd).
The lemma below is what `packing/devtools/filled_end_checker.py` holds every row of
Mohsen Karimi’s filled-end deposits to.
It has not been reviewed.
No row is recorded from it: the rows wait on the walk above 1024 (think-llit) and the
owner’s answers (D4; Q-847a for V1.0).

## What Is Claimed, and by Whom

[#847](https://github.com/jlevy/squares/issues/847) reports V2.0 of Karimi’s filled-end
set (Zenodo 10.5281/zenodo.23819397): 5,134 upper bounds $s(n) \le S$ at $n = 1182$ to
9946\. V1.0 (10.5281/zenodo.23681705), reported on #836 on 27 October, states 4,571 at
1184 to 9946. The packet `packing/resources/web/karimi-records-2026-10-31` keeps both,
from the author’s GitHub copy at `ad8b094`.

No row has a certificate.
Each states an exact side $S$, $K = \lceil\sqrt n\rceil$ and six parameters
$b_V, t_V, y_V, b_H, t_H, y_H$. The construction is Sungjoon Ryu’s L-shaped packing
(10.5281/zenodo.23278927, Theorem 1.3) with two tilted bands of independent width, tilt
and lift, and each band’s two ends filled with axis-parallel layers.
The end fill is Evan Daniel’s idea (evand/square-packing, `certificates/k2-minus-c/`),
written as in Kevin Fang’s note (10.5281/zenodo.23624565, Sections 2–3); the independent
bands and the per-$n$ search are Karimi’s. The author’s `source/filled_ends.py` states
the construction; the checker was written from it, read as data, and shares no code with
it.

By the owner’s D2 answer (think-f2io), a row stated without a certificate is a row once
a checker this project maintains decides it exactly from its recipe.
That makes the lemma the whole of the argument from a row to its bound, which is why it
needs a review of its own.

## The Construction

Throughout, a *tilt* is $t = \tan(\theta/2)$ with $0 < t < 1$, and
$c = (1 - t^2)/(1 + t^2)$, $s = 2t/(1 + t^2)$. Both are positive rationals with
$c^2 + s^2 = 1$, so $\theta \in (0, \pi/2)$.

**A band** of width $b$ (a positive integer), tilt $t$, length $L$ and lift $y$ has its
own frame, $X$ across in $[0, W]$ and $Y$ along in $[0, L]$, where
$$W = bc + s,\qquad h = bs + c,\qquad p = 1/c.$$

- **Rows.** $R = \lfloor (L - h)/p \rfloor + 1$ rows, leaving the free length
  $F = L - (R - 1)p - h \in [0, p)$, with $0 \le y \le F$. Row $j$, $0 \le j < R$, is
  $b$ unit squares turned by $\theta$: square $i$ is
  $\{P_j + u\,(c, s) + v\,(-s, c) : i \le u \le i + 1,\ 0 \le v \le 1\}$ with
  $P_j = (s,\ y + jp)$.
- **Near-end layers.** At level $i = 0, 1, \ldots$, let
  $$a_i = \max\bigl(0,\ s + (i + 1 - y)\,c/s\bigr),\qquad m_i = \lfloor W - a_i \rfloor .$$
  When $m_i > 0$ the level holds $m_i$ axis-parallel unit squares
  $[W - m_i + q,\ W - m_i + q + 1] \times [i, i + 1]$, $q = 0, \ldots, m_i - 1$.
- **Far-end layers.** The near-end layers of lift $y' = F - y$, turned by $180°$ about
  $(W/2, L/2)$: $(X, Y) \mapsto (W - X, L - Y)$.

**The box** is $[0, S]^2$:

- the grid: $(K - b_V)(K - b_H)$ axis-parallel unit squares filling
  $[0, K - b_V] \times [0, K - b_H]$;
- the V band: width $b_V$, tilt $t_V$, length $S$, lift $y_V$, placed by
  $(X, Y) \mapsto (K - b_V + X,\ Y)$;
- the H band: width $b_H$, tilt $t_H$, length $K - b_V$, lift $y_H$, placed by the
  reflection $(X, Y) \mapsto (Y,\ K - b_H + X)$, which turns each square by $-\theta$,
  so its certificate tilt is $-t_H$.

In every row of both deposits $S = K - b_V + W_V$ exactly.

## The Lemma

**Lemma.** Let $K \ge 2$, $1 \le b_V, b_H \le K - 1$, $0 < t_V, t_H < 1$, and let $S$
satisfy the fit inequalities $$K - b_V + W_V \le S,\qquad K - b_H + W_H \le S .$$ Let
each band have $h \le L$ and $0 \le y \le F$, and let each end of each band hold, at
each level $i$, any number $m_i$ of layer squares with $0 \le m_i \le W - a_i$, placed
as above. (The construction takes $m_i = \lfloor W - a_i\rfloor$, the most.)
Then the grid, both bands’ rows and all their layer squares are unit squares with
pairwise disjoint interiors inside $[0, S]^2$. Hence $s(n) \le S$ for every $n$ up to
their number, the capacity $$(K - b_V)(K - b_H) + b_V R_V + b_H R_H + \sum m_i ,$$ the
sum over the levels of all four band ends.

**Proof.** In a band, let $u$ and $v$ be the components of $(X, Y) - P_0$ along $(c, s)$
and $(-s, c)$, so that $$v = c\,(Y - y) - s\,(X - s).$$

1. **Rows.** $P_j - P_0 = (0, jp)$ has $(u, v) = (js/c,\ j)$, so square $i$ of row $j$
   is $\{js/c + i \le u \le js/c + i + 1,\ j \le v \le j + 1\}$. Two squares of one row
   are separated by their $u$-intervals, two of different rows by their $v$-intervals.
   Row $j$’s corners have $X = s,\ s + bc,\ 0,\ bc$, so its $X$-extent is $[0, W]$; its
   $Y$-extent is $[y + jp,\ y + jp + h]$. Since $y \ge 0$ and
   $y + (R - 1)p + h = L - F + y \le L$, every row lies in $[0, W] \times [0, L]$, and
   in the half-plane $v \ge 0$.
2. **Near-end layers.** A level-$i$ square is $[X_0, X_0 + 1] \times [i, i + 1]$ with
   $W - m_i \le X_0 \le W - 1$. On it $v$ increases with $Y$ and decreases with $X$, so
   its largest $v$ is at the corner $(X_0, i + 1)$:
   $$v \le c\,(i + 1 - y) - s\,(W - m_i - s) \le 0,$$ the last because
   $W - m_i \ge a_i \ge s + (i + 1 - y)c/s$ and $s > 0$. So every layer square lies in
   $v \le 0$ and meets no row’s interior.
   Two layer squares of different levels are separated by their $Y$-intervals, two of
   one level by their $X$-intervals.
   Each lies in $[0, W] \times [0, L]$: $X_0 \ge W - m_i \ge a_i \ge 0$,
   $X_0 + 1 \le W$, $i \ge 0$, and from $v \le 0$ and $X \le W$,
   $Y \le y + (W - s)s/c = y + bs < y + h \le L$.
3. **Far-end layers.** The point reflection $r(X, Y) = (W - X, L - Y)$ maps the band of
   lift $y' = F - y$ (also in $[0, F]$, with the same $R$ and $F$) onto the band of lift
   $y$. It sends row $j$’s corner $P'_j + b(c, s) + (-s, c) = (bc,\ y' + jp + h)$ to
   $(s,\ L - h - y' - jp) = (s,\ y + (R - 1 - j)p) = P_{R-1-j}$, and a point reflection
   keeps edge directions, so it maps row $j$ onto row $R - 1 - j$, and the edge $v' = 0$
   of the former’s row 0 onto the edge $v = R$ of row $R - 1$. The lift-$y'$ band’s
   near-end layers lie in $v' \le 0$ by step 2, so the far-end layers lie in $v \ge R$,
   away from every row, and in $[0, W] \times [0, L]$, which $r$ maps onto itself.
   As $R \ge 1$, they meet no near-end layer’s interior, which lies in $v < 0$.
4. **The box.** A translation and the reflection in $y = x$ are isometries, so each
   placed band keeps its squares interior-disjoint.
   The V band lies in $[K - b_V,\ K - b_V + W_V] \times [0, S]$, the H band in
   $[0, K - b_V] \times [K - b_H,\ K - b_H + W_H]$, and the grid in
   $[0, K - b_V] \times [0, K - b_H]$. The V band is right of $x = K - b_V$ and the
   other two left of it; the H band is above $y = K - b_H$ and the grid below it.
   The fit inequalities put all three inside $[0, S]^2$, and give $K - b_V < S$ and
   $K - b_H < S$.
5. **Count.** Deleting squares from a packing leaves a packing.
   $\square$

## What the Checker Does With It

`decide` holds a row to the lemma in exact `Fraction`s and returns its capacity, each
part’s count, each band’s rows and layer counts, both fit slacks, each band’s free
length and the least layer slack $\min(W - m_i - a_i)$; or it raises
`FilledEndRefusedError` with the reason.

- **What it requires beyond the lemma.** $K \le 1000$ and $S \le K$, which bound the
  work a hostile row can ask for (a band end is examined only at levels
  $i < \lfloor y + bs\rfloor + 1 \le L$, since a level at or past $y + bs$ has
  $a_i \ge W$). A side above $K$ bounds nothing the $K \times K$ grid does not.
  A checker of a lemma is sound, not complete, and may refuse what the lemma does not
  state.
- **What it reports and does not require.** $S < K$ and $K = \lceil\sqrt n\rceil$ say
  whether the bound beats the grid, not whether the packing is one.
  The ingest does require $K = \lceil\sqrt n\rceil$, as every row states it.
- **The layer counts.** With no stated layers, `floor_layers` takes
  $m_i = \lfloor W - a_i\rfloor$ for $i = 0, 1, \ldots$ while positive.
  $a_i$ increases with $i$, so the positive counts form a prefix, which is the set of
  $(i, m_i)$ the author’s `fill_levels` lists.
  A row may state counts instead, which `decide` holds to $0 \le m_i \le W - a_i$; the
  layer controls use that.
- **The write-out.** `write_out` places the grid column by column, then the V band
  (rows, near-end layers, far-end layers), then the H band reflected, and drops the
  surplus over $n$ from the start of the grid.
  That is the order of the author’s `build`, so at the five counts of the author-built
  sample (`receipts/filled-end-replay-sample.json`) its certificates are his byte for
  byte; `check` holds them to that receipt’s SHA-256s without running his code.

**The controls** each row carries, every one of which `decide` must refuse:

| Control | The change | Why the lemma refuses it |
| --- | --- | --- |
| count above the capacity | $n$ one above the capacity | the capacity bound |
| side below the binding fit | $S$ $10^{-15}$ below the larger fit | that fit inequality (the V fit at every row) |
| V or H lift past its free length | $y = F + 10^{-15}$ | $y \le F$: the last row passes the band’s far end |
| a layer one over, at each of the four band ends | each level’s $m_i$ one larger in turn, and the level after the last given one square | $m_i \le W - a_i$; the floor plus one always exceeds it |
| no tilt | $t_H = 0$ | $0 < t$ |
| a right angle | $t_V = 1$ | $t < 1$ |
| unknown kind | another kind | the kind |

## What Was Run

| Run | Result | CPU |
| --- | --- | --- |
| `decide-all --version 2` | 5,134 of 5,134 V2.0 rows decided by the lemma, none refused; all eleven controls refused at every row, the layer controls by 85,174 changes | 269.8 CPU-s |
| `decide-all --version 1` | 4,571 of 4,571 V1.0 rows decided, none refused, every control refused (76,268 layer changes); labelled apart, since Q-847a is the owner’s | 237.6 CPU-s |
| `replay-sample` | 1188, 5265, 7439, 8524 and 9517, written out by `write_out`, pass both maintained exact routes of `devtools.couzo_678_replay`; both refuse all six controls of each | 430.9 CPU-s on two workers |

In V2.0 the least slacks are: the V fit 0 at every row ($S = K - b_V + W_V$), the H fit
$1.5 \times 10^{-8}$ (at 9517), a layer $1.4 \times 10^{-6}$ (5265), and the lift room
smallest at 7439 (H) and 8524 (V); 1188 has $y_V = 0$. The replay sample is those rows.
No row of either deposit was refused by the lemma, so none needed the routes in its
place. The receipts are in the packet,
`packing/resources/web/karimi-records-2026-10-31/receipts/`, and its README gives the
rest under “W9: The Filled-End Checker”.

## For the Reviewer

This is the record’s first decision of the filled-end construction, and the lemma is the
only argument between a row and its bound.
The questions, in order of weight:

1. **The proof.** Is each step sound and complete?
   Especially the half-plane separation of rows and layers (step 2), the claim that $r$
   maps the lift-$y'$ band onto the lift-$y$ band row for row (step 3), and the
   placement of the H band by the reflection, including the tilt sign the certificate
   writes (step 4).
2. **Hypotheses.** Does `decide` require exactly the lemma’s hypotheses, and nothing
   that could pass a non-packing?
   Its order of checks decides which reason a refusal names, never whether it refuses.
3. **The construction’s layers.** Is `floor_layers` the construction the author states
   (`fill_levels` in `filled_ends.py`), including where it stops looking?
4. **The controls.** Is each meaningful?
   Is any always refused for a reason that shows nothing about the check it names?
5. **The ingest.** `row_from_record` accepts the decimal side within one unit of its
   last place of the exact side (four V2.0 rows state it exactly; none is a unit off),
   and requires $K = \lceil\sqrt n\rceil$. Does any rule let a malformed row through?
6. **Trust boundary.** The checker’s arithmetic is CPython’s `fractions.Fraction`. The
   write-out uses `devtools.evand_exact_certificates`’ `Pose` and `serialize`, which the
   routes also read. What do the lemma’s decision and the routes’ share?

Read as data: `packing/devtools/filled_end_checker.py`, the packet’s `source/` files,
and the receipts. Run only code you write.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
