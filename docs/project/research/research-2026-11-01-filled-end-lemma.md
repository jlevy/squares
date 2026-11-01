# The Filled-End Lemma: Deciding Karimi’s Two-Band L Packings From Their Parameters

**Status:** accepted at stage 4, with no defect
([the review of 1 November](../reviews/review-2026-11-01-filled-end-lemma.md);
think-fuwd).
The lemma below is what `packing/devtools/filled_end_checker.py` holds every
row of Mohsen Karimi’s filled-end deposits to.
This version carries the review’s three gaps and four notes (F1 to F7) into the
statement, the proof and the controls.
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
needs a review of its own: the checker’s decisions count under D2 only once that review
accepts the lemma, as the stage 4 review of 1 November did.

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
each level $i$, $m_i \ge 0$ layer squares placed as above, finitely many levels holding
any, with $m_i \le W - a_i$ whenever $m_i > 0$. (The construction takes
$m_i = \lfloor W - a_i\rfloor$ while that is positive, the most.
Read as $0 \le m_i \le W - a_i$ at every level, the hypothesis would hold for no band,
since $a_i$ grows without bound; the review’s F1.) Then the grid, both bands’ rows and
all their layer squares are unit squares with pairwise disjoint interiors inside
$[0, S]^2$. Hence $s(n) \le S$ for every $n$ up to their number, the capacity
$$(K - b_V)(K - b_H) + b_V R_V + b_H R_H + \sum m_i ,$$ the sum over the levels of all
four band ends.

**Proof.** In a band, let $u$ and $v$ be the components of $(X, Y) - P_0$ along $(c, s)$
and $(-s, c)$, so that $$v = c\,(Y - y) - s\,(X - s).$$ As $h \le L$, $R \ge 1$, so
$F = L - (R - 1)p - h \le L - h$.

1. **Rows.** $P_j - P_0 = (0, jp)$ has $(u, v) = (js/c,\ j)$, so square $i$ of row $j$
   is $\{js/c + i \le u \le js/c + i + 1,\ j \le v \le j + 1\}$. Two squares of one row
   are separated by their $u$-intervals, two of different rows by their $v$-intervals.
   Row $j$’s corners have $X = s,\ s + bc,\ 0,\ bc$, so its $X$-extent is $[0, W]$; its
   $Y$-extent is $[y + jp,\ y + jp + h]$. Since $y \ge 0$ and
   $y + (R - 1)p + h = L - F + y \le L$, every row lies in $[0, W] \times [0, L]$, and
   in the strip $0 \le v \le R$.
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
   $Y \le y + (W - s)s/c = y + bs < y + h \le L$, the last as $y \le F \le L - h$.
3. **Far-end layers.** Let $y' = F - y$, also in $[0, F]$, and let $v'$ be $v$ for the
   band of lift $y'$, which has the same $R$ and $F$. The point reflection
   $r(X, Y) = (W - X, L - Y)$ satisfies $$v(r(X, Y)) = R - v'(X, Y),$$ since the sum of
   the two is $c(L - F) - s(W - 2s) = (R - 1) + ch - bcs + s^2 = R$. It sends row $j$’s
   corner $P'_j + b(c, s) + (-s, c) = (bc,\ y' + jp + h)$ to
   $(s,\ L - h - y' - jp) = (s,\ y + (R - 1 - j)p) = P_{R-1-j}$, and a point reflection
   keeps edge directions, so it maps row $j$ of the band of lift $y'$ onto row
   $R - 1 - j$ of the band of lift $y$. That band’s near-end layers lie in $v' \le 0$ by
   step 2, so by the identity the far-end layers lie in $v \ge R$, where no row’s
   interior is, and in $[0, W] \times [0, L]$, which $r$ maps onto itself.
   As $R \ge 1$, they meet no near-end layer’s interior, which lies in $v < 0$.
4. **The box.** A translation and the reflection in $y = x$ are isometries, so each
   placed band keeps its squares interior-disjoint.
   The H band’s placement maps a square with edges along $(c, s)$ and $(-s, c)$ onto one
   with edges along $(s, c)$ and $(c, -s)$: the reflection turns the square turned by
   $\theta$ into the one turned by $\pi/2 - \theta$, and a square is unchanged by a
   quarter-turn, so that is the square of the same centre turned by $-\theta$, the
   certificate’s $-t_H$. The V band lies in $[K - b_V,\ K - b_V + W_V] \times [0, S]$,
   the H band in $[0, K - b_V] \times [K - b_H,\ K - b_H + W_H]$, and the grid in
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
  work a hostile row can ask for.
  A band end is examined only at levels $i \le \lfloor y + bs\rfloor$, since a level at
  or past $y + bs$ has $a_i \ge W$; and $y + bs < L$ (step 2), so that is fewer than
  $L + 1$ levels, at most $K$. (An earlier version said
  $\lfloor y + bs\rfloor + 1 \le L$, which does not follow: $b = 1$, $c = 0.05$,
  $L = 2.95$ and $y = F$ give $y + bs = 2.9$. The review’s F6.) A side above $K$ bounds
  nothing the $K \times K$ grid does not.
  A checker of a lemma is sound, not complete, and may refuse what the lemma does not
  state.

- **The order of its checks** decides only which reason a refusal names, with one
  constraint: the tilt check comes before any division by $c$ or $s$. Moved later,
  $t = 1$ would raise `ZeroDivisionError` at $p = 1/c$ and $t = 0$ at $c/s$, and a crash
  is not a refusal (F7). A comment at the check says so.

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

- **The decimal side** is a consistency check and never a bound.
  The ingest holds the author’s decimal `side` within one unit of its last place of
  `side_exact`, either way.
  The author rounded to nearest, so the decimal is below the exact side at 2,514 of
  V2.0’s 5,134 rows and 2,204 of V1.0’s 4,571, by up to 0.502 units of its twelfth place
  (0.504 in V1.0; the largest gap either way, 0.503 and 0.506, is above).
  At 1190, for example, the decimal is `34.958620689655` and the exact side is
  $5069/145 = 34.95862068965517\ldots$. The V fit is tight at every row, so where the
  decimal is below, a square of that side does not hold the construction.
  `decide` decides and reports `side_exact` alone, each receipt counts the decimal
  against it under `author_columns.side`, and a row is recorded at `side_exact`, or at a
  decimal rounded up from it, never at `side` (F2).

**The controls** each row carries, eighteen, every one of which `decide` must refuse by
the check it names. `controls` counts one as refused only when each of its changes is
refused by that check, matched by the refusal’s own words.
The last seven were added after the review found that seven of the lemma’s eleven
hypotheses had no per-row control (F3):

| Control | The change | The check that must refuse it |
| --- | --- | --- |
| count above the capacity | $n$ one above the capacity | $n \le$ capacity |
| side below the binding fit | $S$ $10^{-15}$ below the larger fit | the V fit, which binds at every row |
| V or H lift past its free length | $y = F + 10^{-15}$, from wherever $y$ was | $y \le F$ |
| a layer one over, at each of the four band ends | each level’s $m_i$ one larger in turn, and the level after the last given one square | $m_i \le W - a_i$ at that end; the floor plus one always exceeds it |
| no tilt | $t_H = 0$ | $0 < t < 1$ |
| a right angle | $t_V = 1$ | $0 < t < 1$ |
| unknown kind | another kind | the kind |
| the H band one square narrower | $b_H - 1$, which raises the band’s top by $1 - c_H$, more than the H fit’s slack at every row | the H fit |
| a negative tilt | $t_H \to -t_H$ | $0 < t < 1$ |
| a V lift below zero | $y_V = -10^{-15}$ | $y \ge 0$ |
| a layer of $-1$ squares | the V near end’s level after its last given $-1$ | $m_i \ge 0$ |
| an H band $K$ wide | $b_H = K$ | $1 \le b \le K - 1$ |
| $K$ of one | $K = 1$ | $2 \le K$ |
| an H band shorter than its depth | $b_V = K - 1$ and $y_V = 0$, which leave the H band 1 long, less than $b_H s_H + c_H$ | $h \le L$ |

The lift controls move the lift by all its room, not by $10^{-15}$. That also sets the
far lift to $-10^{-15}$ and moves layers from one end to the other, so the change is
more than the lift (F4). Every V2.0 and V1.0 row refuses them by $y \le F$.

**What each control depends on.** At 1188, with the check each names deleted
(`test_what_each_control_depends_on`), eleven are accepted:

- the count, the side, the kind and each layer one over;
- the V lift past $F$, the narrower H band, the negative tilt and the lift below zero.

The right angle raises `ZeroDivisionError`, which is why the tilt check comes first.
The other six are refused by a second check as well: the H lift past $F$ and the H band
$K$ wide by the capacity, no tilt by the H fit, the $-1$ layer by $m_i \le W - a_i$,
$K = 1$ by $S \le K$, and the short H band by $y \le F$. Each is still refused at every
row by the check it names, which is what the receipts count.
A negative count places no square, so $m_i \ge 0$ keeps the statement exact rather than
the packing sound.

## What Was Run

| Run | Result | CPU |
| --- | --- | --- |
| `decide-all --version 2` | 5,134 of 5,134 V2.0 rows decided by the lemma, none refused; all eighteen controls refused at every row by the checks they name, the layer controls by 85,174 changes | 284.2 CPU-s (269.8 with the first eleven controls) |
| `decide-all --version 1` | 4,571 of 4,571 V1.0 rows decided, none refused, every control refused by its own check (76,268 layer changes); labelled apart, since Q-847a is the owner’s | 246.0 CPU-s (237.6 with eleven) |
| `replay-sample` | 1188, 5265, 7439, 8524 and 9517, written out by `write_out`, pass both maintained exact routes of `devtools.couzo_678_replay`; both refuse all six controls of each | 430.9 CPU-s on two workers |

In V2.0 the least slacks are: the V fit 0 at every row ($S = K - b_V + W_V$), the H fit
$1.5 \times 10^{-8}$ (at 9517), a layer $1.4 \times 10^{-6}$ (5265), and the lift room
smallest at 7439 (H) and 8524 (V); 1188 has $y_V = 0$. The replay sample is those rows.
No row of either deposit was refused by the lemma.
A row it refuses is no row: `check` names it, and no route decides it in the lemma’s
place. The receipts are in the packet,
`packing/resources/web/karimi-records-2026-10-31/receipts/`, and its README gives the
rest under “W9: The Filled-End Checker”.

## The Questions Put to the Review

This is the record’s first decision of the filled-end construction, and the lemma is the
only argument between a row and its bound.
The stage 4 review answered each of these questions in turn, and its findings are
carried into the sections above.
The questions stand as they were put, in order of weight:

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
