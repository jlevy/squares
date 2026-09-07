# Stromquist’s Twenty-Six-Square Packing

Stromquist’s Memo III construction is valid, but its side `5.650629191439388…` is larger
than the current best known `(7 + 3sqrt(2))/2 = 5.621320343559642…`, found by Friedman
in 1997. The chart’s upper bound needs no correction.
The source audit did find a separate omission: Friedman’s survey reports a stronger
lower bound from Green than the one independently verified here.
Those two evidential statuses are now explicit in the
[n26](../../../packing/frontier/n-026.md) and [n27](../../../packing/frontier/n-027.md)
records.

**Owner:** `think-zi3g`. The
[session record](../../../packing/campaign/agent-sessions/session-097-stromquist-n26-verification.md)
retains delegation, validation, and the integration checkpoint.

## What the Author Meant

We thank Walter Stromquist for drawing attention to his twenty-six-square construction
in Memo III (private communication, September 2026). His suggestion prompted this review
and the independent exact verification.

In the note supplied by the project owner on September 7, Stromquist identified his
intended small improvement as Memo III’s twenty-six-square packing.
He explicitly allowed that the comparison might be mistaken and said he had not compared
the eighteen- and twenty-six-square packings with Friedman’s page.

This corrects the
[earlier review’s inference](research-2026-09-07-stromquist-memos-and-helper-arguments.md)
that his hint concerned the date of the eleven-square lower bound.
The chronology corrections found in that review remain supported independently.
The independent replay checks both the construction and the comparison.

## Source Comparison

The archived
[Memo III](../../../packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture.pdf)
is dated November 15, 1984. Table 1 on printed page 2 gives approximately `5.651`; page
3 describes improvements over Göbel; Figure 4(b) on page 5 prints `5.650629` and an
angle of approximately `27.583°`. Two reviewers inspected the scanned pages.
The number is not an OCR ambiguity.

[Ellsworth’s historical catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares__compared.html)
already lists the construction and its cubic, credits Stromquist in 1984, and shows the
later Friedman packing alongside it:

| Construction | Side of the enclosing square | Relation to Stromquist’s side |
| --- | --- | --- |
| Göbel, 1979 | `5 + sqrt(2)/2 ≈ 5.707106781187` | Larger by approximately `0.056477590` |
| Stenlund, 1980 | `5/2 + 9sqrt(2)/4 ≈ 5.681980515339` | Larger by approximately `0.031351324` |
| Stromquist, 1984 | Unique real root of `p(s)=s³−14s²+67s−112`, approximately `5.650629191439` | Historical improvement |
| Friedman, 1997 | `(7 + 3sqrt(2))/2 ≈ 5.621320343560` | Smaller by approximately `0.029308848` |

The differences are display approximations of rigorous rational enclosures retained by
the checker. Smaller side is better.
The live [explainer](https://jlevy.github.io/squares/) retrieved on September 7 was
`DRAFT v0.2.3-a5e9dbfd`; its chart metadata at that source commit displays
`s(26) ≤ 5.62132`. The chart and current catalogue agree.
Stromquist’s 1984 improvement was subsequently superseded; it is already acknowledged in
the historical record.

## Exact Reconstruction and Verification

The [reusable reconstruction](../../../packing/cases/stromquist/memo3_n26.py) uses the
exact scalar formulas in
[Ellsworth’s reconstruction](https://kingbird.myphotos.cc/packing/square-26_r2.svg),
dated May 31, 2023, and matches the memo’s Figure 4(b). The source SVG is inspected for
numerical and geometric facts; it is not vendored.
All reconstructed coordinates and comparison intervals are retained in
[the exact record](../../../packing/cases/stromquist/memo3-n26.json).

The field is `Q(s)` for `p(s)=0`, with initial isolating interval
`5650/1000 < s < 5651/1000`. The field implementation certifies irreducibility and root
isolation. Monotonicity is also immediate from

$$
p'(x)=\frac{(3x-14)^2+5}{3}>0.
$$

The exact orientation is

$$
\sin\theta=\frac{-s^2+9s-18}{2},\qquad
\cos\theta=\frac{s^2-11s+32}{2}.
$$

Their squared sum is exactly one modulo the cubic.
The builder makes fourteen aligned boundary squares and twelve oblique squares from six
translated unit-by-two dominoes.
The small relative slides between dominoes matter: replacing them with a solid
three-by-four rectangle does not reproduce the figure.

The production verifier checks unit-square geometry, every wall inequality, and all
`26·25/2 = 325` pairs using exact algebraic signs.
It finds 41 touching pairs and 284 strictly separated pairs.
A duplicate square and a container shrunk by `10⁻⁶` are rejected.
The independent tests use rational polynomial arithmetic and oriented-edge half-plane
separation to check the returned geometry without reusing the production sign or
separating-axis routines.

The comparison with Friedman’s side `U` does not depend on rounded decimals:

$$
p(U)=\frac{-175+123\sqrt2}{8}<0,
$$

because `2·123² < 175²`. Since `p` is strictly increasing and `p(s)=0`, `U<s`. The
existing [Friedman verifier](../../../packing/cases/gobel_offcentre/verify_exact.py)
also passes all 325 pairs and the walls for its separate construction, and rejects
duplicate and overfull-column controls.
Neither construction proves that `s(26)` equals its enclosing side.

Run from `packing/`:

```shell
uv run --frozen python -m cases.stromquist.memo3_n26 --output cases/stromquist/memo3-n26.json
uv run --frozen --all-extras --group dev pytest -q tests/test_stromquist_memo3_n26.py
uv run --frozen python -m cases.gobel_offcentre.verify_exact
```

## The Eighteen-Square Comparison

Memo III’s Figure 3(b) has side `(7 + sqrt(7))/2 ≈ 4.822875655532`, which ties the
current record. Friedman’s survey credits Hämäläinen in 1980 and a different arrangement
to Gustafsson in 1981. Ellsworth’s
[original-arrangement metadata](https://kingbird.myphotos.cc/packing/square-18.svg)
explicitly credits Stromquist with independent rediscovery in 1984.

Gardner’s *Fractal Music, Hypercards and More…*, inspected W. H. Freeman edition with
1992 copyright, chapter 20 addendum, pp.
299–300 and Figure 127, corroborates the history: it describes Stromquist’s 1984 letter
and notes Hämäläinen’s earlier eighteen-square construction and Gustafsson’s
following-year example.
The book was visually checked for this attribution; its figure’s printed numerical slips
are not used as geometric evidence.
The repository’s
[exact eighteen-square replay](../../../packing/cases/lifted_q7/verify_exact.py) checks
the current upper bound over `Q(sqrt(7))`, including all 153 pairs and walls.

## The Lower Bound Needs Two Separate Statements

The independently verified bounds in this repository remain

$$
1+\sqrt{17}\le s(26)\le\frac{7+3\sqrt2}{2}.
$$

[Friedman’s survey](https://erich-friedman.github.io/papers/squares/squares.html),
Theorem 9, reports Green’s general statement

$$
s(k^2+1)\ge
2\sqrt2-1+
\frac{k(k-1)^2+(k-1)\sqrt{2k}}{k^2+1}.
$$

At `k=5`, this is `2sqrt(2)+(27+2sqrt(10))/13 ≈ 5.3918`. Table 2 explicitly lists the
value for `n=26–27`. In the archived PDF, the theorem, table, and reference [8] are on
pages 23, 26, and 27 respectively.
The reference is Trevor Green, private communication, 2000. No proof or n26 point
coordinates accompany the claim; the illustrated smaller cases do not fill that gap.
An independent source review checked the page images and searched the retained corpus
and public survey versions without finding the missing proof.

The case records now preserve this stronger *reported* lower bound and its source gap.
They retain Nagamochi’s theorem in the *verified* lower-bound fields.
The prior sentence that nothing specific had ever been proved was unsupported and has
been removed. This source-record omission is [D-481](../../../defects.md).

## Directions Pursued and Remaining Dependencies

The
[independent mathematical review](../reviews/review-2026-09-07-stromquist-n26-directions.md)
proves a bounded negative result: a rigid `3 × 3` oblique block cannot beat Friedman’s
side while two explicitly defined opposite corner-triplet separations remain imposed.
Its center is free to translate and its angle to vary.
An exact support inequality places the minimum at `45°`. This closes that restricted
proposal without a numerical sweep; changing the separation assignments, splitting the
block, or moving the frame remains outside the argument.

The next packing-search design must identify an actual release of those assumptions and
replay both exact source constructions as controls before seeking an improvement.
`think-z0fi` tracks that bounded design and its certificate requirements.

For the lower bound, `think-0x08` tracks recovery of Green’s proof or a fully
independent twenty-five-point cover with complete all-angle verification.
`think-4g6w` tracks the remaining survey-table audit for similar omissions.
These are distinct from the earlier BC-202 numerical fractional-cover attempt at `5.52`,
which yielded no certificate and does not become a successful or failed upper-packing
search through this review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
