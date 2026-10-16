# Review: Evan Daniel’s Exact Algebraic Sides at Sixteen Counts (#639, T-193)

**Date:** 16 October 2026. **Verdict: accepted at all sixteen counts, for finite
feasibility only.** Each exact form that T-193 cites is a packing of $n$ unit squares in
the square of side $S^\ast$. Each $S^\ast$ is the one root of its integer polynomial in
the interval the file gives, and each polynomial is irreducible.
The source’s checker, `verify_exact.py`, was read line by line here.
When it prints `VALID` it proves that statement, under five hypotheses this review
states, and the replay ran it under all five.
Three of its runs were reproduced here, one of them at degree 41, and each printed the
receipt’s line. A check written for this review shares no code with that checker.
It decided all sixteen forms again with other arithmetic, the two forms pinned only by
digest among them. It proved, as identities in the field, the same number of contacts as
the checker at every count, and it refused all of its own controls, contact moves of
$10^{-30}$ among them.
Every bound the claim prints is a correct cut of its side.
Each side lies below every standing side the ledger froze at its count, and below the
certificate its regularization names.
Nine findings are recorded, and none is blocking.
One is major (RE-1). At nine counts the configuration, measured pose by pose, is the
case’s own packing to within $4.5 \times 10^{-4}$ at every centre.
It is not the T-174 or T-186 certificate that its `regularizations` item names: against
that certificate, one to eight squares move beyond a tenth at seven of the nine, and no
pairing is one to one at the other two.
The credit sentence and those items have to be rewritten.
The bound does not change.
T-193 can take `V3`/`C3` at all sixteen counts on the replay and this review; it cannot
take `V4`/`C4` from them.

This is the stage 4 review lane (W2) for the entry PR #651 registers for issue #639
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)). It
was written by an AI agent (Claude, strong sub-agent tier, max reasoning), prompted
separately from the import, records and addressing lanes, and it shared no context with
them beyond their committed packet, register entry and ledger.
T-193 is that branch’s id, and it is not yet on `main`. Its relation to the result is
`project`. It moves no rung, writes no register row and changes no case record; it says
what the records lane should write.
Before its findings were written, this review saw no part of PR #651’s review A beyond
what its brief and bead said of it.
That was that A2 holds the rung for this review and that A5 asks about irreducibility at
the four pinned-only counts.
The brief also said the addressing lane was changing the rung hold, the claim’s margins,
the credit sentence and the replay driver’s irreducibility test, which would accept a
perfect power. RE-2 and RE-3 overlap those topics, and both were measured here.
[Review A of PR #651](#review-a-of-pr-651) compares the two reviews.

## For the Author

Evan Daniel: the sixteen exact forms were decided here a second time, by a program
written for this review in other arithmetic.
The first decision was your own `verify_exact.py`, run unchanged.
Both found every form a packing at its algebraic side, with the same contacts proved
exactly, and each polynomial irreducible and squarefree, as your issue says.
Each is accepted as a finite upper bound; nothing here bears on optimality.

- **Which packing each form solves.** Your README says the inputs were the store’s best
  at each count on 15 October.
  Measured centre by centre, nine of the forms are the packing the case held on `main`,
  each to within $4.5 \times 10^{-4}$:
  - at 88 and 199, Siddharth Gupta’s refinement of Nate Chaoweeraprasit’s packing, to
    $10^{-15}$;
  - at 126, your certificate of Ryan Xu’s arrangement, to $10^{-15}$;
  - at 175 and 232, Daniil Ostashev’s #528 packings;
  - at 204, his #562 packing;
  - at 266, your own packing, to $8 \times 10^{-12}$;
  - at 292, your regularized view of Chaoweeraprasit’s packing;
  - at 301, your exact optimum of Francisco Couzo’s packing.

  None of the nine is PR #574’s certificate or Mykhailo Polkovskyi’s (`70a033f`).
  Against those, one to eight squares move beyond a tenth at seven of the nine, and at
  199 and 292 no pairing of the two is one to one.
  Were these the inputs you meant?

- **Turned squares.** The forms put each square in an angle class.
  Against the packing each one solves, 0 to 193 squares turn by more than $10^{-6}$ in
  sine with their centres held, by 34° to 38° at 175, 204 and 232. Are these squares
  free to turn (rattlers, or squares with slack)?

- **Near contacts.** At 259 and 292 two squares stand $1.25 \times 10^{-16}$ and
  $1.9 \times 10^{-15}$ apart, and both checkers prove these gaps strictly, not as
  contacts. Are these the free parameters your `pins` fix at the input’s values?
  If so, the README could say that each form is one point of a family whose side does
  not depend on them.

- **The checker.** Two changes would make `verify_exact.py` self-contained.
  Its checks that $f$ changes sign, that $p(S) = 0$ and that $S$ lies in its interval
  are `assert` statements, which `python -O` removes; explicit raises would keep them.
  It could also check that a file lists exactly `n` squares.
  Neither change bears on these results, which were all run without `-O`.

## Claims Covered

| Entry | Source and pin | Counts | Certificate kept |
| --- | --- | --- | --- |
| T-193 (PR #651’s branch) | Evan Daniel, #639, `evand/square-packing` at `7d1407a`, `search/exact/cur/` | 88, 102, 123, 126, 175, 199, 204, 232, 258, 259, 266, 267, 292, 295, 301, 302 | 14 exact forms retained as their upstream gzip (MIT); 204 and 267 pinned by size and SHA-256 |

The claim (`packing/frontier/results.yaml` lines 26251 to 26291) gives each side cut at
40 places and ended with an ellipsis.
Under the runbook’s convention, those digits stand for every number that starts so.
At 126 and 295 it gives the closed forms $15/2 + 3\sqrt2$ and $22(1 + \sqrt2)/3$. Its
other statements are covered under [The Claim Map](#the-claim-map) and
[Credit and Lineage](#credit-and-lineage).
The packet’s other seven forms, at 51, 70, 153, 172, 207, 263 and 297, are not in
T-193’s scope. The check here decided the first five in full anyway, and only the
polynomials of 263 and 297; nothing here is recorded for them.

## What `verify_exact.py` Proves

The checker is
[`verify_exact.py`](../../../packing/resources/web/evand-exact-and-local-reports-2026-10-12/source/search/exact/verify_exact.py)
(SHA-256 `a0f38ca8…bab4`), 323 lines that use only the standard library.
It was read line by line, and its copy at the pin was fetched here and is that file
([Custody](#custody)). Line numbers below are its own.

**The field and its root (lines 203 to 223).** `f` is read as rationals, low degree
first, as are all coefficient lists (`fv`, line 206, and `ev_iv`, line 148, agree on
that order). There are two branches.
If `ta == tb`, the checker requires $f(ta) = 0$ exactly (line 208). Otherwise it
requires $ta < tb$ and $f(ta)\,f(tb) < 0$ exactly (line 210). It then bisects 200 times,
rounding the ends outward to multiples of $2^{-400}$ and requiring a strict sign change
after every step (lines 211 to 222). So the final interval $T$ holds at least one real
root $t^\ast$ of $f$. It is not shown to hold only one, nor that $f$ is irreducible or
squarefree, and neither is needed.
Every inequality is proved on the whole of $T$ and every identity at every root of $f$,
so the statement holds at each real root in $T$. The side, below, is the same at each.

**The numbers (lines 24 to 197).** `I` is a closed rational interval with outward
rounding. `rdn` is the floor at $2^{-400}$ and `rup` the ceiling (lines 27 to 32). Sums
and products are rounded outward, `inv` refuses an interval containing 0 (line 63), and
`ev_iv` is interval Horner, an enclosure over $T$. `E` is a fraction `num/den` over
$\mathbb{Q}[t]$, with the numerator reduced modulo $f$ (line 117). Every denominator is
1 or a product of factors $1 + u^2$, built only at lines 236 and 237 and by products, so
at any real root it is positive.
`V` carries an `E` and an interval built by the same operations from the same
coefficients, so both describe one quantity’s value at $t^\ast$. The `E` is computed
only when the interval cannot decide (lines 155 to 189). `nonneg` (lines 191 to 197)
accepts $g \ge 0$ in two ways.
One is `'gt'`, where the interval’s lower end is positive, so $g > 0$ on all of $T$. The
other is `'eq'`, where the numerator is 0 modulo $f$, so $g = 0$ at every root of $f$.
Anything else is refused.

**The squares (lines 232 to 240, 263 to 272).** Each square has a centre $(x, y)$ and
parameter $u$ in the field.
From $u$ the checker forms $c = (1 - u^2)/(1 + u^2)$ and $s = 2u/(1 + u^2)$, then turns
them by `m` quarter turns.
Then $c^2 + s^2 = 1$ identically, so for any real $u$ each square is a unit square, and
the bound on $|u|$ in the docstring (line 8) is neither checked nor needed.
The corners are $(x + (ca - sb)/2,\ y + (sa + cb)/2)$ for $(a, b) = (\pm1, \pm1)$, and
the four outward normals are $(c, s)$ turned by quarter turns.

**The side (lines 241 to 261).** The checker requires three things.
$p(S)$ must be 0 modulo $f$ (line 247), so $p(S(t^\ast)) = 0$ at every root.
The enclosure of $S$ over $T$ must lie in the file’s $[S_a, S_b]$ (line 249). And $p$
must change sign on that interval while $p'$ keeps one sign there (lines 254 to 261).
Failing that last test, it retries on intervals tightened about the enclosure, each
still containing it.
So $p$ is strictly monotone with exactly one root on the final interval, and
$S^\ast = S(t^\ast)$ is that root for every root $t^\ast$ in $T$. A root of $p$ where
$p'$ keeps one sign is simple, so a `VALID` $p$ has $S^\ast$ as a simple root (RE-2).
The packing proof never uses $p$; the box is $[0, S]^2$ with $S$ the field element.
What $p$ does is identify $S^\ast$ as an algebraic number.

**Containment (lines 274 to 281).** All four corners of each square are proved in
$[0, S]^2$ by four inequalities each.
By convexity, the square is then in the box.

**Pairs (lines 283 to 306).** For each pair, the checker first tries the disc rule.
If the lower end of the enclosure of the squared centre distance is at least 2 (line
288), the circumscribed discs, of radius $\sqrt2/2$, meet in at most one point.
Otherwise it looks for a side line of one square that has all four corners of the other
on its closed outer side (lines 292 to 304). Then the other square, being convex, lies
in the closed outer half-plane, and the two interiors lie in the two open half-planes.
The midpoint prefilter (lines 283 and 286) and the candidate order (line 298) only
choose what to try first, and change no decision.

**What `VALID` states.** Take any real root $t^\ast$ of $f$ in the narrowed $T$, at
least one of which exists.
The first `n` squares the file lists, `n` being the file’s own `n`, then lie in
$[0, S^\ast]^2$ with pairwise disjoint interiors.
And $S^\ast = S(t^\ast)$ is the unique root of $p$ in the printed interval.
Hence $s(n) \le S^\ast$.

**The hypotheses.**

- **H1.** CPython and `fractions.Fraction` compute exactly.
  `json` reads integers exactly, and strings are read by `Fraction`; every number in
  these files is an integer or a string.
- **H2.** Assertions are enabled.
  Lines 63, 208, 210, 247 and 249 are `assert` statements, which `-O` and
  `PYTHONOPTIMIZE` remove.
  The box and pair decisions (lines 280 and 306), the narrowing check (line 222) and the
  uniqueness test (line 261) raise explicitly and survive (RE-5).
- **H3.** The count is the file’s `n`. The checker reads `range(n)` squares (lines 272
  to 285) and so says nothing about any listed after them.
  A file listing fewer squares raises `IndexError`, which is not caught, so it exits 1.
  Nothing compares `n` with the file name (RE-6).
- **H4.** Only `AssertionError` and `RuntimeError` are caught (line 320). Any other
  exception ends the run with exit status 1 and no `VALID` line, and the replay ran one
  file per process and required both `VALID` and exit 0.
- **H5.** The file is the file meant ([Custody](#custody)).

**What could make it accept a non-packing.** Only three things could.
One is a fault in the interpreter or in `Fraction`. Another is a run under `-O`, which
would drop the side checks and the point-root check.
The last is a file that is not the one meant, or whose `n` is not its count.
Nothing about how the data were produced matters: a strict margin of $10^{-16}$ is
proved like any other, and every identity is decided exactly.
The replay and this review ran it as `python -I` with no `-O`; `-I` also ignores
`PYTHONOPTIMIZE`.

## The Replay Reproduced Here

The checker ran unchanged from its retained copy under the project interpreter (CPython
3.14.7), as `python -I verify_exact.py FILE`. Each run was one process under
`nice -n 10`, one at a time, from `packing/` in a worktree at `ef43dd02f`, and was
logged by the kept `replay_sample.sh` ([Programs Run Here](#programs-run-here)). The 267
run read a copy fetched at the pin and held to the manifest’s digest.

| n | Degree | Run (UTC, 16 October) | Wall, user CPU | Exit | Line |
| --- | --- | --- | --- | --- | --- |
| 126 | 2 | 11:00:13 to 11:00:22 | 8.8 s, 3.4 s | 0 | `VALID`, 473 identities, 3,159 strict, 7,471 by discs |
| 266 | 32 | 11:00:22 to 11:01:02 | 40.4 s, 15.9 s | 0 | `VALID`, 1,425 identities, 6,471 strict, 34,335 by discs |
| 267 | 41 | 11:01:02 to 11:05:00 | 237.7 s, 141.4 s | 0 | `VALID`, 428 identities, 7,548 strict, 34,585 by discs |

Each statement equals, character for character, the receipt’s `last_line`
(`receipts/replay-verify-exact.json`) and the source’s `data/verify.txt` line.
Of the receipt’s timings, 267’s 123 CPU seconds compare with 141 here, on a host another
lane’s jobs were sharing.
The receipt’s other 20 positives and 76 controls were not re-run.

## The Independent Check

`independent_check.py` was written for this review.
Its author read `verify_exact.py` first, so it is not clean-room, but it imports and
copies none of that code.
It decides each file again as follows:

- **The count.** `n` must equal the count in the file name and the number of squares
  listed.
- **The field.** SymPy decides that $f$ is squarefree and irreducible over $\mathbb{Q}$,
  with exactly one real root in `t_interval` by a Sturm count.
  Exact rational bisection then narrows that interval below width $10^{-260}$.
- **The configuration.** Every coefficient, the root interval and every derived quantity
  are enclosed with mpmath’s interval arithmetic at 1,400 bits, with gmpy underneath.
  Corners and normals are built from the same half-angle parametrisation, which is the
  format’s meaning.
- **The decisions.** A box margin, or the margin of a corner against a side line of the
  other square, is accepted as strict when its enclosure lies above 0. It is accepted as
  zero only when the enclosure lies within $10^{-150}$ of 0 and the quantity is exactly
  0 in $K = \mathbb{Q}[t]/f$. That is decided by SymPy over $\mathbb{Q}$, with $1 + u^2$
  inverted modulo $f$ and every element reduced, a different representation from the
  checker’s fractions.
  A pair is separated by the disc rule, decided rigorously, or by a side line whose four
  margins are each strict or exactly zero.
  Anything else is refused.
- **The side.** $p(S) = 0$ in $K$ exactly.
  $p$ is irreducible over $\mathbb{Q}$, which needs `factor_list` to give one factor of
  multiplicity one and full degree, and it is squarefree.
  It has exactly one real root in the file’s side interval by a Sturm count, and the
  enclosure of $S(t^\ast)$ lies inside that interval.

Each form also faces three controls, each a change of $10^{-30}$ to the exact data that
must be refused. A square touching a wall is moved through it.
A square in a contact the check proved exactly is moved into its neighbour along the
contact normal. And the side is lowered in $K$.

It ran from 10:50Z to 10:57Z on 16 October, one process under `nice -n 10`: 412 seconds
of wall for all 21 forms and their controls, 156 CPU seconds of it for the positives.
Every form was decided a packing and every control refused.

| n | Degree | Box: strict, exact | Pairs: discs, strict, touching (exact) | Least strict wall margin | Least strict pair gap | Controls |
| --- | --- | --- | --- | --- | --- | --- |
| 88 | 7 | 1,352, 56 | 3,569, 109, 150 (286) | $5.0 \times 10^{-5}$ | $1.0 \times 10^{-9}$ | 3 of 3 refused |
| 102 | 4 | 1,560, 72 | 4,852, 54, 245 (470) | $1.0 \times 10^{-6}$ | $8.7 \times 10^{-5}$ | 3 of 3 |
| 123 | 6 | 1,897, 71 | 7,129, 54, 320 (620) | $5.0 \times 10^{-5}$ | $1.0 \times 10^{-6}$ | 3 of 3 |
| 126 | 2 | 1,950, 66 | 7,496, 167, 212 (407) | $9.1 \times 10^{-5}$ | $1.5 \times 10^{-4}$ | 3 of 3 |
| 175 | 7 | 2,704, 96 | 14,688, 110, 427 (840) | $1.2 \times 10^{-5}$ | $6.3 \times 10^{-7}$ | 3 of 3 |
| 199 | 16 | 3,090, 94 | 19,068, 209, 424 (818) | $4.9 \times 10^{-7}$ | $2.4 \times 10^{-7}$ | 3 of 3 |
| 204 | 35 | 3,168, 96 | 20,073, 116, 517 (1,002) | $1.0 \times 10^{-6}$ | $5.9 \times 10^{-7}$ | 3 of 3 |
| 232 | 7 | 3,630, 82 | 26,054, 305, 437 (867) | $1.0 \times 10^{-6}$ | $1.0 \times 10^{-6}$ | 3 of 3 |
| 258 | 8 | 4,006, 122 | 32,307, 69, 777 (1,519) | $5.0 \times 10^{-5}$ | $1.0 \times 10^{-6}$ | 3 of 3 |
| 259 | 6 | 4,074, 70 | 32,562, 483, 366 (715) | $3.2 \times 10^{-9}$ | $1.25 \times 10^{-16}$ | 3 of 3 |
| 266 | 32 | 4,154, 102 | 34,358, 213, 674 (1,323) | $6.3 \times 10^{-7}$ | $1.6 \times 10^{-9}$ | 3 of 3 |
| 267 | 41 | 4,233, 39 | 34,624, 683, 204 (389) | $1.2 \times 10^{-7}$ | $1.2 \times 10^{-7}$ | 3 of 3 |
| 292 | 6 | 4,569, 103 | 41,519, 228, 739 (1,456) | $1.0 \times 10^{-6}$ | $1.9 \times 10^{-15}$ | 3 of 3 |
| 295 | 2 | 4,592, 128 | 42,381, 45, 939 (1,857) | $7.4 \times 10^{-2}$ | $1.7 \times 10^{-2}$ | 3 of 3 |
| 301 | 4 | 4,739, 77 | 44,132, 771, 247 (489) | $1.0 \times 10^{-6}$ | $1.2 \times 10^{-7}$ | 3 of 3 |
| 302 | 7 | 4,748, 84 | 44,425, 565, 461 (900) | $5.9 \times 10^{-5}$ | $7.9 \times 10^{-5}$ | 3 of 3 |

At every count, the exact box incidences plus the exact pair incidences equal the
checker’s identity count.
At 88, for example, $56 + 286 = 342$, as the receipt states, and so at all 21 forms, 204
and 267 among them. So the two programs found the same contacts by different means, and
every other incidence strict.
The pair counts differ from the checker’s only because the disc prefilters differ.
The other five forms, at 51, 70, 153, 172 and 207, were decided packings too, with their
controls refused, and their identity counts also equal the checker’s. Each least strict
margin is a lower end of an enclosure about $10^{-250}$ wide, so even the
$1.25 \times 10^{-16}$ gap at 259 is decided with room (RE-7).

## The Polynomials

At all 23 forms, $f$ and $p$ have the same degree.
$f$ is irreducible and squarefree with one real root in its interval, and $p$ is
irreducible, with one factor of multiplicity one, and squarefree, with one real root in
its interval.
And $p(S) = 0$ in $K$. The 21 forms were checked by `independent_check.py`,
and 263 and 297, which T-193 does not cite, by `polynomials.py`, which checks the
polynomials alone.
Since $f$ is irreducible of the degree of $p$, $S^\ast$ generates $K$:
the field $\mathbb{Q}(S^\ast)$ is the whole field the configuration lives in, and
$S^\ast$ is algebraic of exactly the stated degree.
For the four pinned-only counts, 204 and 267 (T-193’s) were decided here in full, with
configuration, polynomials and three controls each.
At 263 and 297 the polynomials were decided and the configuration was not.
For all four, the files read here are at the manifest’s digests.

## The Claim Map

`claims_and_credit.py` encloses each $S^\ast$ to width below $10^{-170}$ by exact
bisection of $p$ on the file’s interval, which holds one root of $p$ by Sturm count.
It then holds each printed cut $d$ to it: a correct cut has
$d \le S^\ast < d + 10^{-40}$. All sixteen are correct cuts at 40 places.
At 126 and 295 the closed form is a root of $p$ inside the interval, so it is $S^\ast$.

Every member that the ledger’s `gather` froze at each count (`starts.yaml`, `main` at
`e2e018f`) was compared exactly with $S^\ast$, as was the side of the certificate that
the regularization item names.
Each $S^\ast$ is below all of them:

| n | Below the case (lane, gap at least) | Below the item’s `of` (gap at least) |
| --- | --- | --- |
| 88 | T-127, $9.88 \times 10^{-20}$ | T-174, $5.92 \times 10^{-95}$ |
| 102 | T-146, $1.06 \times 10^{-19}$ | T-174, $3.69 \times 10^{-88}$ |
| 123 | T-146, $1.16 \times 10^{-19}$ | T-174, $8.95 \times 10^{-95}$ |
| 126 | T-139, $1.17 \times 10^{-19}$ | T-174, $7.77 \times 10^{-35}$ |
| 175 | T-158, $1.38 \times 10^{-19}$ | T-186, $1.00 \times 10^{-76}$ |
| 199 | T-127, $1.46 \times 10^{-19}$ | T-174, $4.48 \times 10^{-88}$ |
| 204 | T-162, $1.48 \times 10^{-19}$ | T-186, $1.48 \times 10^{-99}$ |
| 232 | T-158, $1.58 \times 10^{-19}$ | T-186, $1.58 \times 10^{-99}$ |
| 258 | T-146, $1.66 \times 10^{-19}$ | T-174, $1.51 \times 10^{-94}$ |
| 259 | T-136, $1.56 \times 10^{-31}$ | T-174, $1.43 \times 10^{-94}$ |
| 266 | T-119, $1.68 \times 10^{-19}$ | T-174, $1.49 \times 10^{-94}$ |
| 267 | T-134, $1.68 \times 10^{-19}$ | T-174, $1.18 \times 10^{-64}$ |
| 292 | T-146, $1.76 \times 10^{-19}$ | T-174, $1.66 \times 10^{-79}$ |
| 295 | T-146, $1.77 \times 10^{-19}$ | T-174, $1.86 \times 10^{-94}$ |
| 301 | T-098 (both lanes), $1.79 \times 10^{-19}$ | T-174, $1.97 \times 10^{-94}$ |
| 302 | T-181, $1.79 \times 10^{-19}$ | T-186, $1.79 \times 10^{-39}$ |

Each gap is the one the ledger prints at its count, to the three figures the ledger
shows. The brief asked for three spot-checks.
All sixteen counts were compared, since the comparison is exact and cheap.
So each count is pending adoption against its case, and none is superseded.
The claim’s summary of these margins is wrong at two counts (RE-3).

## Custody

`custody.sh` made a blobless clone of `evand/square-packing` over HTTPS on 16 October at
10:37Z, and again at 11:06Z. Each clone went to scratch space outside the repository,
where its files were read as data.
The pinned commit `7d1407a0b66c46e32cdbcbd5619586fe2bdd52a1` has tree `d6b9aae3…`, the
`git_tree` of the packet’s `acquisition/sources.json`. All 35 manifest lines have their
SHA-256 at the pin, and all 30 retained files are byte for byte their upstream blobs.
The four pinned-only forms are at the digests the packet’s README tabulates, and
`search/exact/verify_exact.py` at the pin is the retained copy the replay ran.
Nothing from the clone was executed except as data, and `verify_exact.py` ran only from
the repository’s copy.

## Trust Boundaries

| Program | Decides | Shares with the other |
| --- | --- | --- |
| `verify_exact.py` (the source’s, V-evand-verify-exact) | everything above, in `Fraction` intervals at $2^{-400}$ and fractions over $\mathbb{Q}[t]/f$ | the format’s meaning; the disc rule and side-line separation; CPython |
| `independent_check.py` (this review’s, unregistered) | the same statement, in mpmath intervals at 1,400 bits and SymPy’s $\mathbb{Q}[t]/f$ with inversion; plus the count, the root’s isolation, irreducibility and squarefreeness | the same; and mpmath, which the source’s `crosscheck.py` uses for its numerical cross-check, not for any decision |

They are one method, exact-algebraic, with one separation criterion.
That criterion is complete for two squares: by the separating axis theorem, two convex
polygons with disjoint interiors have a separating line parallel to an edge of one of
them. Their arithmetic and algebra are separate implementations.
The source states that its solver, checkers and batch were written with Claude, and so
was this review and its programs.
The reviewer and the source’s assistant are one system family, so this review’s
independence from the producer has `extent:
system-family`. The replay is reproduction with the producer’s code; this review’s check
is a re-implementation that shares only the method and the format’s meaning.

## Credit and Lineage

`lineage.py` evaluates each form’s centres and rotations at the root and pairs them with
candidate packings. The candidates are the case’s house on `main`, the certificate the
`regularizations` item names, and their sources, each read by the readers of
`devtools.check_half_angle_area` (`CREDITED_READERS`, or the T-174 and T-186 facts).
It pairs them with that module’s `arrangement_gap` and `unmoved`, which decide nothing.
The record’s sense of a refinement is a one-to-one pairing in which no square moves
beyond a tenth (T-150, T-152).

| n | Item’s `of` | Against the `of`: largest move; beyond $10^{-3}$ / $10^{-1}$ | The packing it is: entry, largest move, turned |
| --- | --- | --- | --- |
| 88 | T-174 | 0.150; 35 / 5 | T-127, $1.0 \times 10^{-15}$, 11 |
| 102 | T-174 | $2.8 \times 10^{-4}$; 0 / 0 | T-174 and T-146 alike, $2.8 \times 10^{-4}$, 14 |
| 123 | T-174 | $2.8 \times 10^{-4}$; 0 / 0 | T-174 and T-146 alike, $2.8 \times 10^{-4}$, 3 |
| 126 | T-174 | 0.137; 59 / 8 | T-139, $8.4 \times 10^{-16}$, 11 |
| 175 | T-186 | 0.453; 4 / 2 | T-158, $4.0 \times 10^{-4}$, 33 |
| 199 | T-174 | no one-to-one pairing; 108 within $10^{-3}$ | T-127, $9.2 \times 10^{-16}$, 38 |
| 204 | T-186 | 0.809; 9 / 1 (one square relocated) | T-162, $4.5 \times 10^{-4}$, 36 |
| 232 | T-186 | 0.453; 5 / 4 | T-158, $1.6 \times 10^{-4}$, 93 |
| 258 | T-174 | $1.4 \times 10^{-4}$; 0 / 0 | T-174 and T-146 alike, $1.4 \times 10^{-4}$, 2 |
| 259 | T-174 | $6.2 \times 10^{-4}$; 0 / 0 | T-174 and T-136 alike, $6.2 \times 10^{-4}$, 76 |
| 266 | T-174 | 0.119; 27 / 2 | T-119, $7.8 \times 10^{-12}$, 4 |
| 267 | T-174 | $5.4 \times 10^{-10}$; 0 / 0 | T-174 and T-134 alike, $5.4 \times 10^{-10}$, 68 |
| 292 | T-174 | no one-to-one pairing; 89 within $10^{-3}$ | T-146, $2.0 \times 10^{-4}$, 57 |
| 295 | T-174 | $1.2 \times 10^{-19}$; 0 / 0 | T-174 and T-146 alike, $2.4 \times 10^{-19}$, 0 |
| 301 | T-174 | 0.440; 189 / 4 | T-098, $1.4 \times 10^{-4}$, 193 |
| 302 | T-186 | $1.0 \times 10^{-15}$; 0 / 0 | T-186 and T-181 alike, $1.5 \times 10^{-15}$, 36 |

“Turned” counts the squares whose orientation differs by a sine above $10^{-6}$ under
the same pairing. The largest such differences reach sines of 0.56 to 0.62 at 175, 204
and 232, which is 34° to 38°. The source’s packings are its finders’, as the issue says
(“The packings are their finders’”). Measured, each form is a refinement, in the
record’s sense, of the case’s house at its count:

| n | House | Finder first, as the case credits it |
| --- | --- | --- |
| 88, 199 | T-127 | Nate Chaoweeraprasit, improved by Siddharth Gupta |
| 102, 123, 295 | T-146 | Ryan Xu, improved by Evan Daniel |
| 126 | T-139 | Ryan Xu, improved by Evan Daniel |
| 175, 232 | T-158 | Daniil Ostashev |
| 204 | T-162 | Daniil Ostashev |
| 258 | T-146 | Nate Chaoweeraprasit, improved by Mykhailo Polkovskyi (Mishapolk) and Evan Daniel |
| 259 | T-136 | Nate Chaoweeraprasit |
| 266 | T-119 | Evan Daniel |
| 267 | T-134 | Ryan Xu, improved by Francisco Couzo |
| 292 | T-146 | Nate Chaoweeraprasit, improved by Evan Daniel |
| 301 | T-098 | Francisco Couzo, improved by Evan Daniel |
| 302 | T-181 | PingYou Ltd’s arrangement, continued by Francisco Couzo |

At 102, 123, 258, 259, 267 and 295 the form pairs equally well with T-174, and at 302
with T-186. These certificates hold the house packing there within $6.2 \times 10^{-4}$,
so the `of` named stands at those counts.
At the other nine it does not (RE-1).

## Findings

Each finding is graded blocking, major, minor or note, with the file and line it
concerns. None is blocking.

**RE-1, major: at nine counts the `of` of the regularization item is not the packing the
form solves.** `packing/frontier/results.yaml` lines 26335 to 26478 list T-174 as the
`of` at 88, 126, 199, 266, 292 and 301, and T-186 at 175, 204 and 232. Measured centre
by centre, each form at those counts is instead the case’s house: T-127 at 88 and 199,
T-139 at 126, T-158 at 175 and 232, T-162 at 204, T-119 at 266, T-146 at 292 and T-098
at 301. Each pairs one to one, with every centre within $4.5 \times 10^{-4}$, and at 88,
126, 199 and 266 within $8 \times 10^{-12}$. Against the item’s `of`, one to eight
squares move beyond a tenth at 88 (five), 126 (eight), 175 (two), 204 (one, by 0.81),
232 (four), 266 (two) and 301 (four, with 189 beyond $10^{-3}$), and no pairing is one
to one at 199 and 292. The claim’s credit sentence (lines 26283 to 26289) follows the
items: “at every count but 266 by way of PingYou Ltd’s or Polkovskyi’s refinement”.
That chain is not what the measurement shows at those nine counts, and at 266 the item
itself names T-174. The credit stays with the same finders, but it routes through
PingYou Ltd and Mykhailo Polkovskyi at counts where neither’s certificate is the
packing. The records lane should set `of` to the measured house at the nine counts.
It should make each item’s `identity.basis` `measured`, with this review as
`measured_in`, stating the largest centre move and the turned count from
[Credit and Lineage](#credit-and-lineage), as epistemics.md allows for a decision made
here. And it should rewrite the sentence count by count: by way of PingYou Ltd’s
certificate (T-174) at 102, 123, 258, 259, 267 and 295, which hold the house packing
there; by way of Polkovskyi’s (T-186) at 302; and solved directly from the case’s
packing at the other nine.
Whether a square turned at its centre leaves the packing the same is for the owner (Q2).

**RE-2, minor: the replay driver’s irreducibility test accepts a perfect power.**
`packing/resources/web/evand-exact-cur-2026-10-16/review/replay_verify_exact.py` lines
189 to 193 compare `degree × multiplicity` with the degree of $p$. So $p = q^k$ would
read as `irreducible: true`, and the receipt’s `polynomial` rows cannot tell it apart.
The conclusion stands anyway.
A `VALID` run proves $S^\ast$ a simple root of $p$ (above), which rules out $k > 1$, and
every $p$ here factors with multiplicity one.
The test should require one factor of multiplicity one.
Until then, the packet README’s line 85 and the claim’s lines 26272 to 26274 rest on
that test and the `VALID` runs together, or on this review.

**RE-3, minor: the claim’s margin summary is wrong at 267 and 292.** Lines 26276 to
26278 say each side is “below PR 574’s rational certificates (T-174) by 7.8e-35 at 126
to 3.7e-88 or less elsewhere”.
The margins are at least $1.18 \times 10^{-64}$ at 267 and $1.66 \times 10^{-79}$ at
292, both above $3.7 \times 10^{-88}$ ([The Claim Map](#the-claim-map)). The sentence
should give the range at the twelve counts: $7.8 \times 10^{-35}$ at 126,
$1.2 \times 10^{-64}$ at 267, $1.7 \times 10^{-79}$ at 292, and $3.7 \times 10^{-88}$ or
less at the other nine.
The significance rationale’s “1.5e-99 to 7.8e-35” (line 26298) is right.

**RE-4, minor: the credit sentence drops Mykhailo Polkovskyi at 258.** Lines 26285 to
26287 credit “Nate Chaoweeraprasit’s at … 258”, but the case credits “Nate
Chaoweeraprasit (itsnaka), improved by Mishapolk, Evan Daniel” (the ledger’s Per Count
row, from `starts.yaml`); Mishapolk is Polkovskyi’s handle.
Where the case lists the author’s own improvements, at 102, 123, 126, 292, 295 and 301,
the sentence drops them too.
That is the author’s choice to make in his own entry, but the rule is “as the case
records credit it”, which the sentence states and should follow.

**RE-5, note: the checker’s side checks are `assert` statements.** `verify_exact.py`
lines 63, 208, 210, 247 and 249 vanish under `-O` (H2). The replay command (`python -I`,
with no `-O`) is the right one.
The evidence entry’s `replay` field could say that `-O` is not to be used, and the
author is asked about it.

**RE-6, note: the root’s isolation and the count are outside the checker.** Neither is
needed for soundness (above).
Both were decided here: one real root of $f$ in each `t_interval`, and `n` equal to the
file name and to the squares listed at all 23 forms.
The ledger’s `exact_sides.py` checks the count as well.

**RE-7, note: some strict gaps are far below any contact tolerance.** The least strict
pair gap is $1.25 \times 10^{-16}$ at 259 and $1.9 \times 10^{-15}$ at 292, and the
least wall margin is $3.2 \times 10^{-9}$ at 259. Both checkers prove each of these
strictly, so the claim’s “every contact an identity in the field” (lines 26260 to 26262)
is accurate: these are not contacts.
They show that each form fixes its free parameters (`pins`, `stats.n_free` in each file)
at rational values, so it is one point of a family whose side the pins do not change.
The register’s notes could say so.

**RE-8, note: the receipt’s controls never move a contact pair.** Its four mutations are
a wall move of $10^{-6}$, a side change, an interval move and a duplicate.
None tests the checker’s `'eq'` path for a pair at a step below the interval’s reach.
This review’s 63 controls include one such move of $10^{-30}$ at each of 21 forms, all
refused by its own check.
The checker’s own refusal of that mutation was not run.

**RE-9, minor: this review’s programs are kept but cited by nothing.** They are kept,
with their outputs, in the packet’s
[`review/review-2026-10-16/`](../../../packing/resources/web/evand-exact-cur-2026-10-16/review/review-2026-10-16/README.md).
No `verifiers.yaml` entry or evidence entry names them, so the independent check sits
beside the rung only through this document.
If the record is to cite it, `independent_check.py` needs a verifier entry with its
`independence` record (it read `verify_exact.py`, is not clean-room, shares the method,
and comes from the same system family).
It also needs an evidence entry covering the sixteen counts, with
`relationship_to_generator: independent-implementation`.

**For the owner (not findings against T-193).**

- **Q1.** RE-1’s measurements also bear on T-174, which is on `main`, at 88, 126, 199,
  266, 292 and 301. Since each T-193 form matches the house to within
  $2.0 \times 10^{-4}$ there, T-174’s certificates move two to eight squares of the
  house beyond a tenth at 88, 126 and 266. At 301 they move 189 beyond $10^{-3}$ and
  four beyond a tenth, and at 199 and 292 they pair it not one to one.
  T-174 records them as refinements of those packings, but this was measured here only
  through T-193.
- **Q2.** Is a square turned at a fixed centre, as at 0 to 193 squares per count here,
  the same packing for the record’s refinement test, which reads centres only?

## Rungs

**`V3`/`C3` for T-193 at all sixteen counts.** The confirmation is reproduced with the
producer’s code: the source’s own checker, run complete on every cited form with its
controls, in the import lane’s replay (`E-evand-639-verify-exact-replay`, the receipt of
23 `VALID` and 76 refused controls).
Three of those runs were reproduced here equal to the receipt.
This review adversarially read the checker’s soundness, the hypotheses it assumes and
the claim. Beside the rung, and cited by no evidence entry yet (RE-9), this review
re-implemented the decision independently, sharing the method and the format’s meaning.
It decided all sixteen forms, with three controls each, and the polynomials’
irreducibility. For exact-algebraic evidence, one complete replay is `C3`’s predicate; a
second route is an attribute beside it.
`V4`/`C4` is not supported.
This is one AI review, of the same system family as the source’s assistant, with no
human oversight record.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

| n | Verdict | Blocking | Open findings at this count | Rung supported |
| --- | --- | --- | --- | --- |
| 88, 126, 175, 199, 204, 232, 266, 292, 301 | accepted, a packing at $S^\ast$ | no | RE-1 (credit) | `V3`/`C3` |
| 102, 123, 258, 259, 267, 295, 302 | accepted, a packing at $S^\ast$ | no | none at the count (RE-3 at 267, RE-4 at 258: wording) | `V3`/`C3` |

The verdict lines are for the records lane.
On `E-evand-639-exact-sides-report`, set `external_review` to this review, which makes
the entry `reviewed`. On T-193, add a `reviews` item with `kind: adversarial`,
`reviewer_kind: ai`, `relation: project` and `verdict: accepted`, and keep the rungs.
The claim, notes and `next_rung` should be rewritten together for RE-1, RE-3 and RE-4.
In `next_rung`, the second route over number fields can name this review’s check, once
it is registered (RE-9), as the independent re-implementation beside the rung.
Its `independence` record names the system-family overlap with the source’s Claude
assistance. The confirmation each sentence names is the one above: reproduced with the
producer’s code for the replay, and independently re-implemented, sharing the method,
for this review’s check.

## Significance

`S2` is confirmed. These are exact algebraic forms of packings the record already
credits, $1.5 \times 10^{-99}$ to $7.8 \times 10^{-35}$ below the nearest earlier
report, as T-120 to T-123 are.
The rationale’s last clause, “the rational refinements they tighten (T-174, T-186)”
(line 26300), should follow RE-1: at nine counts the forms tighten the case’s own
packing directly. `by` should name this review.

## Proposed Record Changes

The records lane writes these; this review writes none of them.

- T-193’s `regularizations` at the nine counts of RE-1: `of` set to the measured house,
  and `identity.basis: measured` with this review as `measured_in` at all sixteen
  counts, stating each largest move and turned count.
  At the seven counts where the named `of` holds, the house can be named beside it.
- T-193’s claim: the credit sentence per RE-1 and RE-4, and the margin sentence per
  RE-3. The sentence on irreducibility (lines 26272 to 26274) should name the check that
  decides multiplicity: this review’s, or the replay driver’s once RE-2 is fixed.
- The packet README’s line 85 and the evidence entry’s `limitations`, the same.
- The review fields under [Rungs](#rungs), and the significance `by`.
- Registering this review’s check, if the record is to cite it (RE-9).
- For the owner: Q1 on T-174’s items, and Q2.
- For the author, in the reply drafted at stage 7: the questions under
  [For the Author](#for-the-author).

## Programs Run Here

The programs were written in the session’s scratch space, run there on 16 October from
10:37Z to 11:07Z, and copied with their outputs to the packet’s
[`review/review-2026-10-16/`](../../../packing/resources/web/evand-exact-cur-2026-10-16/review/review-2026-10-16/README.md).
Its README says how to run each one and what it printed.
They read the sources as data, run only this repository’s interpreter and libraries
(SymPy 1.14.0, mpmath 1.3.0 with gmpy2 2.3.1), and write nothing in the repository.

- **`custody.sh`** makes the blobless clone at the pin and checks the tree, every
  manifest line and every retained file.
  It decides no certificate.
- **`replay_sample.sh`** ran the source’s checker on 126, 266 and 267.
- **`independent_check.py`** decided the 21 forms and their 63 controls.
- **`polynomials.py`** decided the polynomials of 263 and 297.
- **`claims_and_credit.py`** encloses each $S^\ast$, checks the claim’s cuts and closed
  forms and compares the standing sides exactly.
  Its pose measurement against the item’s `of` decides nothing.
- **`lineage.py`** pairs each form with the candidate packings.
  It decides nothing.

## What This Review Does Not Establish

This review establishes no optimality, lower bound, local minimum, rigidity, novelty or
priority. It reproduces the replay only at 126, 266 and 267, and does not rerun the
receipt’s other 20 positives or 76 controls.
It does not run the source’s solver, `minpoly.py` or `crosscheck.py`. It does not decide
the configurations at 263 and 297, or record anything at the seven forms outside T-193’s
scope. It does not register its own programs (RE-9), adopt a house, or change a case
record. Beyond the centre and orientation measurements above, it identifies no
derivation.

## Review A of PR #651

Review A of PR #651 (senior review with a correctness pass, round 1, at `ef43dd0`,
published 10:23Z) was read at 11:16Z, after the findings above were written and pushed
(`6f6acc6ea`). Before then this review knew only the topics its brief named (see the
opening). The two agree on three points and differ on one.

- **A2 (the rung before the review)** is what this lane answers: the review lane has now
  run, it has no blocking finding, and `V3`/`C3` is supported at all sixteen counts.
  A2 lists three things the earlier lanes did that were open here: the checker’s trust
  boundary, the pose measurement against each `regularizations` item, and every print
  held to its exact side.
  This review did all three.
  The second found RE-1, which A2 anticipated (“T-193 leaves
  `identity.basis: source-claim` everywhere”) but Review A did not measure.
- **A3 (the margins)** is RE-3, found independently and with the same numbers.
  A3 also notes that the PR description gives the least margin as 1.6e-99 at 232. Here,
  as in the ledger, it is $1.48 \times 10^{-99}$ at 204.
- **A4 (the credit sentence)** agrees with RE-4 at 258 and disagrees with this review at
  266\. A4 reads the item `of: T-174` at 266 as right and proposes dropping “but 266”
  from the sentence. Measured, the 266 form is the author’s own T-119 packing to
  $7.8 \times 10^{-12}$, while two of its squares lie beyond a tenth of T-174’s. So the
  sentence’s exception is right, and the item is wrong, as are eight others (RE-1). A4’s
  fix should not be applied as written.
  The records lane should follow RE-1.
- **A5 (the perfect-power test)** is RE-2. A5 notes that at the four pinned-only counts
  the claim’s irreducibility rested on that test alone.
  This review settles it: $p$ factors with multiplicity one at all four, and at 204 and
  267 the full check also ran.
  In any case a `VALID` run already excludes a perfect power, since it proves $S^\ast$ a
  simple root.
- **A6, A7, A8 and A9** are outside this review’s questions.
  On A6, the three runs reproduced here from scratch printed the receipt’s lines.
  On A9, the custody refetch of 16 October found all four pinned-only forms at their
  digests.
- Review A treats the missing count check as a false positive.
  That agrees with H3 and RE-6, which grade it a note, not a defect of the replay.
- RE-1’s measurements, RE-5 (`-O`), RE-7 (near contacts), RE-8 (contact controls) and
  RE-9 (the kept programs) have no counterpart in Review A.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
