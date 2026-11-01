# The Filled-End Lemma for Karimi’s Two-Band L Packings: Stage 4 Mathematical Review

**Date:** 2026-11-01. **Subject:** the filled-end lemma, stated and proved in
[`packing/devtools/filled_end_checker.py`](../../../packing/devtools/filled_end_checker.py)
and written out in
[research-2026-11-01-filled-end-lemma.md](../research/research-2026-11-01-filled-end-lemma.md).
Pull request [#870](https://github.com/jlevy/squares/pull/870) uses it to decide each
row of Mohsen Karimi’s filled-end deposits from the row’s seven parameters: V2.0 and
V1.0 of [#847](https://github.com/jlevy/squares/issues/847), retained from
`mohsensbu-jpg/square_packing_records_karimi@ad8b094` in
[karimi-records-2026-10-31](../../../packing/resources/web/karimi-records-2026-10-31/README.md).
Bead `think-fuwd` (W9). **Reviewed at:** branch `claude/bold-ritchie-xo28us-l13`, head
`7db2baa55`. **Reviewer:** Claude (AI review), strong tier (`tbd-strong-max`) at maximum
reasoning, the stage 4 mathematical lane, separately prompted.
It shared no context with the lane that wrote the lemma, read the checker and the
author’s programs as data, and kept its programs and receipts in the packet under
[`review/filled-end-lemma-2026-11-01/`](../../../packing/resources/web/karimi-records-2026-10-31/review/filled-end-lemma-2026-11-01/README.md).
It is not a human oversight record.

**Verdict: accepted.** The lemma is true, its proof is complete for the statement it
means, and the checker holds a row to exactly its hypotheses, in exact arithmetic,
refusing only more. No finding is a defect.

- An independent program shares no code with the checker or the author.
  It parses both tables itself and builds every row’s packing from its parameters.
  It then decides the whole construction exactly in integers: every row of V2.0 (5,134)
  and of V1.0 (4,571) is a packing of at least n unit squares in $[0, S]^2$ at the
  stated exact side.
- My own lemma-level computation equals the lane’s decisions receipts in all 16 compared
  fields at all 9,705 rows.
- At 25 V2.0 rows, the five edge rows and 20 drawn, the checker’s certificate is my
  construction square for square.
  Each of 497 geometric mutants is refused.

Three gaps need the addressing pass, none of them blocking:

- the layer hypothesis is unsatisfiable as literally written (F1);
- the author’s decimal side is below the exact side at 2,514 of 5,134 V2.0 rows, so it
  must never be what a row records (F2);
- seven of the lemma’s eleven hypotheses have no per-row control that depends on them,
  “no tilt” among them, since the H fit refuses it too (F3).

## Scope

**Read.** The checker’s docstring and code, `LEMMA`, `CONTROLS`, `decide`, `band`,
`floor_layers`, `_stated`, `mutants`, `controls`, the write-out and the ingest.
The write-up and its six questions.
`packing/tests/test_filled_end_checker.py`. The author’s `source/filled_ends.py`,
`regenerate_filled.py` and `README_filled.md`, read as data.
`devtools/two_strip_checker.py`, for comparison.
The decisions and replay-sample receipts, read as data.
`devtools.couzo_678_replay`’s `geometry` and `decide`, and
`devtools.evand_exact_certificates`’ `Pose`, `literal` and `serialize`, for question 6.

**Run.** Five programs of my own (What I Ran).
Two of them, `fe_crosscheck.py` and `fe_checker_mutation.py`, run the checker as the
object under test, never edited.
I ran none of the author’s code, and not the maintained routes.
My own exact geometry stands in their place.

**Not reviewed.** Whether a row is below every earlier report at its count is the walk’s
(`think-llit`), and Q-847a is the owner’s. Neither is part of the lemma.
I did not run the pull request’s tests.

## The Lemma, Step by Step

Notation as in the write-up: $t = \tan(\theta/2) \in (0, 1)$, $c$ and $s$ its cosine and
sine, $W = bc + s$, $h = bs + c$, $p = 1/c$, $R = \lfloor (L - h)c\rfloor + 1$,
$F = L - (R - 1)p - h$, and in a band of lift $y$, $u = c(X - s) + s(Y - y)$ and
$v = c(Y - y) - s(X - s)$, an orthonormal frame at $P_0 = (s, y)$. Each step was
re-derived, every inequality’s direction checked, and the boundary cases below were each
traced to the line that covers them.

1. **Rows: true.** $P_j - P_0 = (0, jp)$ has $(u, v) = (js/c, j)$, so row $j$ is
   $js/c \le u \le js/c + b$, $j \le v \le j + 1$. Squares of one row are separated in
   $u$, of two rows in $v$. Row $j$’s corners have $X \in \lbrace s, W, 0, bc\rbrace$
   and $Y \in [y + jp, y + jp + h]$. With $h \le L$, $R \ge 1$ and $F \in [0, p)$, and
   $y + (R - 1)p + h = L - F + y \le L$ exactly when $y \le F$. Every row lies in
   $0 \le v \le R$.
2. **Near-end layers: true.** A layer square at level $i$,
   $[X_0, X_0 + 1] \times [i, i + 1]$, has $X_0 \ge W - m_i$. Since $c, s > 0$, $v$
   rises with $Y$ and falls with $X$, so its largest value is at $(X_0, i + 1)$. There
   $v \le c(i + 1 - y) - s(W - m_i - s) \le 0$, and the direction holds because
   $W - m_i \ge a_i \ge s + (i + 1 - y)c/s$ is multiplied through by $s > 0$. A closed
   square in $v \le 0$ has its interior in $v < 0$, and a row’s interior lies in
   $v > 0$. On the square, $v \le 0$ and $X \le W$ give
   $Y \le y + s(W - s)/c = y + bs < y + h \le L$. The last inequality uses
   $y \le F \le L - h$, which needs $R \ge 1$.
3. **Far-end layers: true.** Let $r(X, Y) = (W - X, L - Y)$, and let $v'$ be the frame
   of the band with lift $y' = F - y$. A line of algebra gives the identity the proof
   uses implicitly:
   $$v(r(X, Y)) + v'(X, Y) = c(L - F) - s(W - 2s) = (R - 1) + ch - bcs + s^2 = R.$$ So
   $r$ maps $v' \le 0$ onto $v \ge R$. It maps row $j$ of the band with lift $y'$ onto
   row $R - 1 - j$, square $i$ onto square $b - 1 - i$, since
   $r(P'_j + u(c, s) + v'(-s, c)) = P_{R-1-j} + (b - u)(c, s) + (1 - v')(-s, c)$.
   Far-end layers lie in $v \ge R$, rows in $v \le R$, near-end layers in $v \le 0$, and
   $R \ge 1$ separates the two ends.
4. **The box: true.** The line $x = K - b_V$ separates the V band from the grid and the
   H band, and $y = K - b_H$ separates the H band from the grid.
   The fit inequalities, with $b \le K - 1$, put all three in $[0, S]^2$.
   - The H band’s placement $(X, Y) \mapsto (Y, K - b_H + X)$ is a reflection plus a
     translation. It maps a square with edges along $(c, s)$ and $(-s, c)$ to one with
     edges along $(s, c)$ and $(c, -s)$. That is the square with the same centre turned
     by $-\theta$, because a square is unchanged by a quarter-turn.
   - So the certificate’s $-t_H$ is right, and my cross-check confirms it: the negative
     tilts are exactly $-t_H$ on exactly the H rows’ squares.
     Flipping them to $+t_H$ makes 64 to 984 pairs overlap at each of 25 rows.
5. **Count: true.** Deleting squares from a packing leaves a packing.

| Boundary case | Covered by | In the data |
| --- | --- | --- |
| Closed squares, touching allowed | closed half-planes: layers in $v \le 0$ or $v \ge R$, rows in $0 \le v \le R$; interiors fall in the open ones | 3,893 to 36,700 touching pairs a row in my geometry, over both deposits, none overlapping |
| Lift $y = 0$ | step 1, $y \ge 0$, closed | in V2.0, 1,658 V and 1,489 H lifts are 0, the first at 1188 (V1.0: 1,602 and 1,514) |
| Lift $y = F$, a far lift $y' = 0$ | step 3 applies step 2 at $y' = 0$, which is the same case as $y = 0$ | no row of either deposit; the least lift room is $4.0 \cdot 10^{-5}$ (V2.0, V band, 8524) |
| $t$ near 0 or 1 | step 2 needs $s > 0$; step 1 needs $c > 0$ for $p$; nothing else depends on the size of $t$ | over both deposits $t_V \in [0.0501, 0.2325]$ and $t_H \in [0.0628, 0.2879]$ |
| $m_i = 0$ | no square, nothing to prove; but see F1 | a zero never occurs inside a band end’s counts |
| $m_i = W - a_i$ exactly | step 2, $\le$ throughout | no row; the least layer slack is $1.43 \cdot 10^{-6}$ (V2.0, 5265) |
| $h = L$, so $R = 1$, $F = 0$ | step 1 | no row; $L - h \ge 16.5$ over both deposits |
| The clip $\max(0, \cdot)$ in $a_i$ | never binds under the hypotheses: $s + (1 - y)c/s > 0$ for $y < 1 + s^2/c$, and $y \le F < 1/c < 1 + s^2/c$ since $c < 1$ | binds at no row |
| The 180° turn’s row map | the identity in step 3 | the far-end squares in my construction are $r$’s images |
| The corner where the bands meet | $x = K - b_V$, closed | the H band’s far end touches the V band’s far-end layers: an H lift $10^{-15}$ past $F$ overlaps one at all 25 sampled rows |

## The Checker Against the Lemma

**It requires exactly the lemma’s hypotheses.** `decide` checks $2 \le K$, $0 < t < 1$
for both tilts, $1 \le b \le K - 1$ for both widths, and both fit inequalities.
`band` checks $h \le L$, $y \ge 0$ and $y \le F$ for each band.
`_stated` holds a stated count to $m_i \ge 0$ and, when positive, $m_i \le W - a_i$; F1
is about the statement, not this code.
`decide` then checks $n \le$ capacity.

**What it adds refuses only more:** $K \le 1000$, $0 < S \le K$, $n \ge 1$, the kind,
and stated layers at all four ends or none.
None of these can admit a row the lemma refuses, and the order of the checks changes
only which reason a refusal names, under one constraint (F7).

**Exact arithmetic throughout.** Every quantity on the decision path is a `Fraction`,
and `math.floor` of a `Fraction` is exact.
`float` appears only in refusal messages.

**Parameters parsed exactly.** Each literal is matched whole by an ASCII-only pattern,
with no sign, at most 30 digits a part and a nonzero denominator, before `Fraction` or
`int` reads it.

**It decides the stated side.** `decide` uses `side_exact`. The author’s decimal `side`
must lie within one unit, in its own last place, of `side_exact`, and decides nothing
(F2).

**The count is right.** Capacity is $(K - b_V)(K - b_H) + b_V R_V + b_H R_H + \sum m_i$,
which is exactly the number of squares `poses` places.
My own construction places the same number at every row of both deposits.

**`floor_layers` is the author’s `fill_levels`.** That is question 3, below.

**Compared with the two-strip checker.** The structure is the same: a lemma in the
docstring, `decide` in `Fraction`s, per-row controls, and receipts that keep digests
rather than certificates.
There are two differences.
The two-strip ingest has no decimal side to hold, while this one holds the author’s
decimal within one unit either way (F2). And every row of the two-strip v5 deposit was
also decided on both maintained routes (`replay-all`), while the filled-end deposits
rest on the lemma and five routed rows.
This review’s exhaustive pass decides every filled-end row by geometry as well, but it
is a review program, not a maintained route.

## The Controls

**Each is refused for the reason it names, at every row.**
`fe_checker_mutation.py --baseline-all` decided every change of every control at all
5,134 V2.0 rows with the unmodified checker.
It classified each refusal by the check its message names.
Every change was refused by the check its control names, including all 85,174 layer
changes (21,764, 23,228, 19,458 and 20,724 for the four ends, as the receipt states).
The receipts themselves keep only a boolean per control.

**What each control exercises.** The same program deleted each `_refuse` call of
`decide`, `band` and `_stated` in turn, in memory, and decided the 25 sampled rows’
controls with each variant:

| Check deleted | Controls no longer refused (of 25 rows) |
| --- | --- |
| `_stated`: $m_i \le W - a_i$ | all four layer controls, accepted at 25 |
| `band`: $y \le F$ | V lift accepted at 12, still refused at 13 by the capacity; H lift accepted at 6, refused at 19 by the capacity (F4) |
| `decide`: the V fit | side below the binding fit, accepted at 25 |
| `decide`: $n \le$ capacity | count above the capacity, accepted at 25 |
| `decide`: the kind | unknown kind, accepted at 25 |
| `decide`: $0 < t < 1$ | a right angle raises `ZeroDivisionError` at 25; no tilt is still refused at 25, by the H fit (F3) |
| `_stated`: $m_i \ge 0$; `band`: $h \le L$, $y \ge 0$; `decide`: the H fit, $1 \le b \le K - 1$, the $K$ range, $S \le K$, $S > 0$, $n \ge 1$, the layer arity | none |

The unit test `test_parameters_the_lemma_does_not_state_are_refused` exercises every one
of the unexercised checks, with its message, at the synthetic packing `SMALL`. So each
hypothesis is tested somewhere; F3 is about what the per-row controls and their receipts
show.

**Each geometric control is a real non-packing.** At the 25 sampled rows my geometry
refuses every control that changes the packing:

- the V lift past $F$: the last row crosses the top wall;
- the H lift past $F$: the last row overlaps a V far-end layer at $x = K - b_V$;
- the side $10^{-15}$ lower: the V band crosses the right wall;
- every layer one over, 397 in all: 396 new squares overlap a band’s row.
  Ten, each at a far end’s level 0 where $m_0 + 1 > W$, at nine rows, cross a wall, and
  one of those (2447, the V far end) crosses a wall without meeting a row.

## Independent Check

**What it is.** `fe_independent.py` imports only the standard library.
It parses `filled_records.csv` with its own strict patterns and builds the construction
as the lemma states it, with its own code.
It then decides every square the construction places, not only the last n. Every
coordinate is scaled by one common denominator $D$, of 10 to 41 digits, so every corner
is an integer pair. The program checks four things:

- **unit squares:** consecutive edges of squared length $D^2$ at a right angle, opposite
  edges equal and opposite;
- **walls:** every corner in $[0, SD]^2$;
- **disjoint interiors:** every pair whose closed bounding boxes share a unit cell is
  decided by the separating axis theorem over the pair’s four edge normals.
  Two convex polygons have disjoint interiors exactly when on some edge normal their
  projections overlap in at most one point, and a pair whose interiors meet shares a
  cell, so the broad phase misses none;
- **the count:** at least n squares.

Its self-test passes six hand-made cases, among them a $10^{-30}$ overlap, a tilted
corner touching an axis-parallel square, the same square $10^{-30}$ lower, and a polygon
of side $1 + 10^{-30}$.

**What it covered.**

| Run | Rows | Result |
| --- | --- | --- |
| `fe_independent.py --all`, V2.0 | all 5,134 | every row verified: 30,445,623 squares placed, at each row exactly the receipt’s capacity; 141,533,725 pairs decided, 109,123,897 of them touching, none overlapping; no wall crossed |
| `fe_independent.py --all`, V1.0 | all 4,571 | every row verified: 27,149,538 squares placed, at each row exactly the receipt’s capacity; 126,095,237 pairs decided, 97,277,596 touching, none overlapping; no wall crossed |
| `fe_independent.py`, with mutants | 1188, 5265, 7439, 8524 and 9517 (the edge rows); 1244, 1807, 2154, 2266, 2447, 2944, 3317, 3501, 3650, 3747, 4807, 5528, 6247, 6564, 7080, 7748, 8227, 8306, 9141 and 9929 (drawn with seed 20261101) | all 25 verified; every one of 397 layer-plus-one, 25 V-lift, 25 H-lift, 25 side and 25 tilt-flip mutants refused |
| `fe_all_rows.py` | all 9,705 | my capacity, grid, band counts, rows, layers, slacks, free lengths, layer slack, surplus, side and $K$ equal the receipts’ at every row; every hypothesis holds; $S = K - b_V + W_V$ exactly and $K = \lceil\sqrt n\rceil$ at every row |
| `fe_crosscheck.py` | the 25 above | the checker’s certificate text has the receipt’s SHA-256 and size; its header is the row’s n and exact side; its squares, parsed and turned into corners by my code, equal my construction’s as a multiset; at the five edge rows its own corners verify |

The tables my reader saw have the SHA-256s the packet declaration states:
`1cbfecf8…48f5` for V2.0 and `f047c44b…0b56` for V1.0’s member.
The write-up’s edge values reproduce exactly:

- V fit slack 0 at every row;
- least H fit slack $1.537 \cdot 10^{-8}$ at 9517;
- least layer slack $1.431 \cdot 10^{-6}$ at 5265;
- least lift room $6.40 \cdot 10^{-5}$ (H, 7439) and $4.01 \cdot 10^{-5}$ (V, 8524);
- first zero lift at 1188;
- largest surplus 7 (V2.0) and 5 (V1.0).

## Findings

| Id | Severity | Where | Finding |
| --- | --- | --- | --- |
| F1 | gap | docstring “The lemma”; write-up, The Lemma | The layer hypothesis, read literally, holds for no band |
| F2 | gap | `row_from_record`; write-up question 5 | The author’s decimal side is below the exact side at 2,514 of 5,134 V2.0 rows; it is not a bound and must not be what a row records |
| F3 | gap | `CONTROLS`, `mutants`; write-up’s control table; the receipts | Seven of the lemma’s eleven hypotheses have no per-row control that depends on them, “no tilt” among them, and the receipts keep no refusing check |
| F4 | note | the two lift controls | They move the lift to $F + 10^{-15}$ from wherever it was, which also re-splits the layers |
| F5 | note | proof, steps 2 to 4 | Three inferences are right and could each be one line more explicit |
| F6 | note | write-up, What the Checker Does With It | The work bound $\lfloor y + bs\rfloor + 1 \le L$ is not true in general |
| F7 | note | write-up question 2 | The order of checks matters for one thing: the tilt check must come before any division by $c$ or $s$ |

**F1. The layer hypothesis, read literally, holds for no band.** The docstring and the
write-up say “let each end of each band hold, at each level $i$, any number $m_i$ of
layer squares with $0 \le m_i \le W - a_i$.” Every band has levels with $W - a_i < 0$
($a_i$ grows without bound), and at those no $m_i$ satisfies $0 \le m_i \le W - a_i$.
Taken literally, the lemma is vacuous.

The intended statement is the one the construction (“when $m_i > 0$”), the proof (step 2
bounds a level that holds a square) and `_stated` all use:

> $m_i \ge 0$ at every level, finitely many positive, and $m_i \le W - a_i$ whenever
> $m_i > 0$.

The `LEMMA` string, which bounds a layer of $m_i$ squares, reads that way already.
The fix is to state it so in the docstring and the write-up.
Nothing decided changes.

**F2. The decimal side is not a bound at about half the rows.** `row_from_record`
accepts the decimal `side` within one unit of its last place of `side_exact`, on either
side. My reader compared all of them:

| Deposit | Below the exact side | Equal | Above |
| --- | --- | --- | --- |
| V2.0 | 2,514 | 4 | 2,616 |
| V1.0 | 2,204 | 9 | 2,358 |

The largest gaps are 0.503 (V2.0) and 0.506 (V1.0) units of the twelfth place, so the
author rounded a float to nearest rather than rounding up.
At 1190, for example, the decimal is `34.958620689655` and the exact side is
$5069/145 = 34.95862068965517\ldots$. The V fit is tight at every row, so wherever the
decimal is below the exact side the construction does not fit a square of the decimal
side: its V band would cross the right wall.

The checker decides and reports only the exact side, which is right, and the write-up’s
“four V2.0 rows state it exactly; none is a unit off” is true.
Nothing yet says that the author’s decimal is not a bound.
The fix:

- state in the docstring and the write-up that the tolerance is a consistency check;
- have the walk record `side_exact`, or a decimal rounded up from it (as
  `couzo_678_replay.rounds_up_to` requires of a printed side), never the `side` column.

**F3. Seven of the lemma’s eleven hypotheses have no per-row control that depends on
them.** The eleven are $K \ge 2$, $1 \le b \le K - 1$, $0 < t$, $t < 1$, the V fit, the
H fit, $h \le L$, $0 \le y$, $y \le F$, $0 \le m_i$ and $m_i \le W - a_i$. The controls
depend on four: $t < 1$, the V fit, $y \le F$ and $m_i \le W - a_i$. Deleting the check
of any of the other seven leaves all eleven controls refused at every sampled row:

- the H fit, which never binds in either deposit, so the side control always meets the V
  fit first;
- $h \le L$;
- $0 \le y$;
- $0 \le m_i$;
- $1 \le b \le K - 1$;
- $K \ge 2$, which that range already implies;
- $0 < t$, whose control is overdetermined.
  With the tilt check deleted, “no tilt” ($t_H = 0$) gives $W_H = b_H$, and the H fit
  fails because $S < K$ at every row.

The control for $t < 1$ depends on its check only through a crash.
With the check deleted, “a right angle” ($t_V = 1$) raises `ZeroDivisionError` in
`frame` ($p = 1/c$), which is not a refusal.

The unit test exercises each of these checks at `SMALL`, and
`test_every_control_is_refused_for_the_reason_it_names` checks the reasons at 1182, so
the checks are tested.
But the write-up’s control table and the receipts present the eleven as the lemma’s
refusals, and each receipt keeps only `controls_refused`, a count, which cannot show a
control refused for its named reason.

Suggested fixes:

- record per row the check that refused each change, and require it to be the named one,
  as my baseline does;
- say in the docstring and the write-up which hypotheses only the unit test exercises,
  and why: no one-parameter change of a real row reaches the H fit before the V fit;
- consider a negative-tilt control, $t_H \to -t_H$. It keeps both fits; the checker
  refuses it by the tilt check, and with that check deleted accepts it at 24 of the 25
  sampled rows (the other is refused by $y \le F$).

**F4. The lift controls move the lift by its whole room.** A lift control sets
$y = F + 10^{-15}$ whatever $y$ was.
That also sets the far lift to $-10^{-15}$ and moves layers between the two ends.
With the lift check deleted, the capacity still refuses the V control at 13 of 25
sampled rows and the H control at 19.

The control is meaningful as it stands:

- every V2.0 row refuses it by $y \le F$;
- my geometry finds the V mutant through the top wall and the H mutant into a V far-end
  layer.

But “the last row passes the band’s far end” is not the only change it makes.

**F5. Three inferences could each be one line more explicit.**

- Step 3 infers that the far-end layers lie in $v \ge R$ from $r$ mapping the edge
  $v' = 0$ to $v = R$. The identity $v \circ r = R - v'$ in The Lemma, Step by Step
  gives the inference and its direction at once.
- Step 4’s “turns each square by $-\theta$” is true because a square is invariant under
  a quarter-turn: a reflection maps the square turned by $\theta$ to the one turned by
  $\pi/2 - \theta$.
- Step 2’s $y + h \le L$ uses $R \ge 1$.

**F6. The write-up’s work bound.** “A band end is examined only at levels
$i < \lfloor y + bs\rfloor + 1 \le L$.” Only $\lfloor y + bs\rfloor + 1 < L + 1$
follows. For example, $b = 1$, $c = 0.05$, $L = 2.95$ gives $R = 1$, and $y = F$ gives
$y + bs = 2.9$. It bounds work, not soundness, and the bound holds at every row of both
deposits.

**F7. Order of checks.** Question 2 says the order “decides which reason a refusal
names, never whether it refuses.”
That is true of the present order, with one constraint: the tilt check must precede
every division by $c$ or $s$. Moved after `bands()`, a row with $t = 1$ would raise
`ZeroDivisionError` in `frame` ($p = 1/c$), and one with $t = 0$ whose fits hold would
raise it in `edge` ($c/s$). Neither `controls` nor `decision_row` catches it.
That is not unsound, since the run stops, but a crash is not a refusal; a comment at the
check would keep it in place.

## Answers to the Six Questions

1. **The proof.** Sound and complete for the intended statement (F1). The half-plane
   separation in step 2 is right in every direction.
   $r$ maps the band with lift $y'$ onto the band with lift $y$ row for row and square
   for square, by the identity in step 3. The H band’s reflection is placed right, and
   the certificate’s $-t_H$ is the correct tilt.
   Wording only: F5.

2. **Hypotheses.** `decide` requires exactly the lemma’s hypotheses, plus checks that
   only refuse more. Nothing it accepts is a non-packing: my geometry verifies every row
   it decides in both deposits.
   The order of checks decides the reason, never the verdict, given F7’s constraint.

3. **The construction’s layers.** `floor_layers` equals the author’s `fill_levels`.
   - The author stops at the first level with $m \le 0$ and $a > 0$. Under the
     hypotheses $a_i > 0$ at every level (the boundary table), so that is the first
     non-positive count.
   - $a_i$ increases with $i$, so his list is the positive prefix.
   - The checker stops at the same place.
     Its range bound $\lfloor y + bs\rfloor + 1$ cuts no positive level: a level
     $i \ge y + bs$ has $a_i \ge s + (bs + 1)c/s = W + c/s > W$.
   - My code uses a third stopping rule ($a_i \ge W$), keeps any zero that might occur
     inside, and reproduces the receipts’ counts at all 9,705 rows.
   - One difference outside the data: the author’s `rows_and_free` refuses $L = h$,
     which the lemma admits ($R = 1$, $F = 0$); the least $L - h$ in either deposit is
     16.6.

4. **The controls.** Each is meaningful and, at every V2.0 row, refused for the reason
   it names. Each geometric control is a genuine non-packing at the sampled rows.
   “No tilt” is refused by the H fit as well, and so shows nothing about $0 < t$; seven
   of the eleven hypotheses have no per-row control that depends on them; the lift
   controls change more than the lift (F3, F4).

5. **The ingest.** No rule lets a malformed row through.
   Literals are matched whole (ASCII digits, no sign, bounded length, nonzero
   denominators); the header and field counts are exact; a count twice, an unknown
   source label or a $K$ that is not $\lceil\sqrt n\rceil$ is refused as custody; the
   archive read is bounded.
   The one thing to add is F2: the decimal side is a consistency check, below the exact
   side at about half the rows, and never a bound.

6. **Trust boundary.** What the lemma’s decision and the routes share:
   - CPython and `fractions.Fraction`;
   - the ingest, `records`, `parse_table` and `row_from_record`;
   - the construction’s parameters and poses: `bands`, `frame`, `floor_layers`, `basis`,
     `poses` and `construction`;
   - through `devtools.evand_exact_certificates`, the `Pose` type and its
     $t \mapsto (c, s)$ convention, which both routes read corners through
     (`basis_witness` for `sqpack`, `Pose.corners` for the independent route);
   - `couzo_678_replay.candidate_pairs`, the one filter both routes decide on.

   The routes contribute only their geometric predicates: `sqpack.verify`’s and
   `check_rational_witness_independent`’s. So a misparsed parameter, a wrong band length
   or a wrong tilt-sign convention would be shared by the lemma and the routes.
   Two further points:
   - The routes decide the in-memory certificate, so the receipts’ SHA-256s pin text no
     route parsed. My cross-check parsed that text, with its own reader, at 25 rows.
   - The author-built sample pins `write_out` to the author’s `build` at five rows.
     This review’s check shares none of the above, and it agrees with the lemma’s
     decision at every row of both deposits.

## What I Ran

All with CPython 3.14.7 (`packing/.venv/bin/python3 -I`), under `nice`, on a shared
four-core host at load about 10, at most two processes at a time.
The outputs are in the packet’s `review/filled-end-lemma-2026-11-01/outputs/`.

| Command | Output | CPU |
| --- | --- | --- |
| `fe_independent.py --self-test` | `selftest.json`: 6 of 6 as expected | under 1 s |
| `fe_independent.py PACKET sample-v2.json` (five edge rows and 20 drawn, with mutants) | `sample-v2.json`: 25 of 25 verified, every mutant refused | 50.9 s |
| `fe_independent.py PACKET all-rows-geometry-v2.json --all --version 2 --workers 1` | `all-rows-geometry-v2.json`: 5,134 of 5,134 verified | 2,206.5 s (39 min wall) |
| `fe_independent.py PACKET all-rows-geometry-v1.json --all --version 1 --workers 1` | `all-rows-geometry-v1.json`: 4,571 of 4,571 verified | 1,985.4 s (35 min wall) |
| `fe_all_rows.py PACKET all-rows.json all-rows-geometry-v2.json all-rows-geometry-v1.json` | `all-rows.json`: 0 mismatches over 9,705 rows; every row places the receipt’s capacity | 5.6 s |
| `fe_crosscheck.py PACKING crosscheck-v2.json` (the 25 rows) | `crosscheck-v2.json`: every check holds | 28.7 s |
| `fe_checker_mutation.py PACKING checker-mutation.json --baseline-all` (the 25 rows) | `checker-mutation.json`: the two tables above and the negative-tilt probe | 14.9 s |
| `fe_layer_reasons.py PACKET layer-reasons.json` (the 25 rows) | `layer-reasons.json`: each of the 397 layer mutants’ own reasons | 11.1 s |

In all, about 73 CPU-minutes, counting first runs of the sample and the mutation
analysis whose results the final runs repeat.
Every receipt but `selftest.json` records the SHA-256 of the program that wrote it and
of the table it read, and each is the program’s committed bytes:

- `fe_independent.py` `4b1544c9…`;
- `fe_all_rows.py` `c086e64b…`;
- `fe_crosscheck.py` `55deb226…`;
- `fe_checker_mutation.py` `6db1db1d…`;
- `fe_layer_reasons.py` `57dbf9de…`.

The checker’s SHA-256 at the reviewed head is `6bf305b2a4df4bfd…`, as the cross-check
and mutation receipts record.

## Verdict

**Accepted.** The filled-end lemma is true.
The checker decides exactly that lemma, in exact arithmetic, at the stated exact side
and with the right count.
Every row of both deposits is a packing of at least n unit squares in a square of its
exact side, decided both by the lemma and, independently, by exact geometry that shares
no code with it.

F1 to F3 are gaps for the addressing pass: a statement fix, a rule for the walk, and an
accurate account of what the per-row controls exercise.
F4 to F7 are notes. None holds a row.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
