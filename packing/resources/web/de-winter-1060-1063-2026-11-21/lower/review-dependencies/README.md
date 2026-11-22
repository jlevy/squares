# Issue 1060: Dependency and Parallel-Chord Review

The reviewer checked Attachment D against the preceding tables and derived the coarse
parallel-chord lemma independently after reading the source argument. All 721 exact
scalar checks passed. The final n162 and n318 contradiction margins are positive
conditional on the stated capture and fine-area bounds. Complete geometric
replay remains open.

The [source packet](../../README.md) records the original attachments and tables.
The [scalar receipt](scalar-audit.json.gz) binds the exact input values to this review.

## Exact Inheritance and the T-180 Boundary

The scalar receipt contains exact values, dependency counts, source archive
digests and check labels.

- D contains 166 distinct counts, with 40 strict and 126 weak inequalities.
  Every `previous_endpoint` equals its C endpoint exactly.
  There are 22 stronger endpoints and 144 unchanged endpoints.
- Exactly two signs change: n162 and n318 strengthen `>=` to `>`. The remaining 164
  signs persist. Both changed rows have positive final contradiction margins and strictly
  smaller test squares than the outer squares, conditional on their claimed capture and
  reserve bounds.
- All 60 rows explicitly naming T-180 retain the same endpoint and weak sign.
  Their complete count list is in the receipt.
  The note says their corner modification inherits coverage away from the changed
  corners from Hosono’s T-180.
- The other 106 rows do not carry that explicit flag.
  This absence does not establish theorem independence; several inherit earlier capture
  certificates.

[T-180’s declaration](https://github.com/jlevy/squares/blob/e6a86b6edb199502edea902697ef1ae6124bcc1e/packing/frontier/results.yaml#L25254)
is V0/C1. Its closed-form evaluation and family structure checks passed, and the
[existing review](https://github.com/jlevy/squares/blob/e6a86b6edb199502edea902697ef1ae6124bcc1e/docs/project/reviews/review-2026-10-14-wand125-closed-form-lower-bound.md)
accepted the mathematical reduction.
The universal capture condition still rests on 136 source records and 187,183,108 exact
leaf tests. Only two complete records were locally replayed.
The declared next rung requires complete replay and controls; the estimated 5,250 local
CPU-hours exceed the owner’s recorded 40 CPU-hour cap per validation item.

Thus the 60 dependent follow-ups cannot become verified through corner-only replay or
exact endpoint evaluation.
They require either the inherited T-180 coverage or another complete proof of coverage
on every unchanged region.
Exact equality suffices to carry the same *reported claim* forward with its dependency
intact. It does not strengthen its evidential status.

For the other unchanged rows, equality settles which filed endpoint is inherited.
Verified status can pass through only after identifying an already verified predecessor
certificate and checking that the inherited hypotheses, measure and pose coverage are
unchanged. This audit did not establish that mapping for all 144 rows.

## What the New Rows Still Require

D’s 22 endpoint increases partition as follows.
These are source-family assignments, not verification verdicts.

| Family | Counts | Remaining geometric dependency |
| --- | --- | --- |
| Additional small counts | 26, 27, 30, 37, 39, 42 | Complete wall-angle capture certificates and occupancy capacities; n28 uses this family but its final endpoint is unchanged |
| Dual capture | 115, 138, 219, 282, 317 | Inherited capture floors and capacities, plus every new wall box |
| Parallel chord | 163, 248, 250, 283, 314 | Earlier capture and line bounds, plus the fine weighted chord enclosure |
| Combined area and line | 162, 318 | Enlarged wall capture, earlier floors and capacities, and fine area and line reserves |
| Reserve | 190, 247, 249, 280 | Source capture and line tables, and the new missed-area bound |

The separate C wall-extension family has 16 rows.
Its geometric reduction is plausible: enlarging the domain can add only poses crossing
the old walls, so a complete outward enclosure of those poses suffices if the inherited
interior certificate is valid.
Its default replay validates archived interior results and runs the new walls;
`--full-core` additionally reconstructs and replays interiors and negative controls.
A default or saved-capture invocation is not evidence of a fresh complete interior
replay.

## Independent Coarse Parallel-Chord Argument

This checks the coarse lemma in D’s `overnight/parallel-chords/PROOF.md`. It does not
reproduce the finer weighted-density table used for the final n162/n318 margins.

Let outer squares of side $a$ have disjoint interiors and contain concentric parallel
inner squares of side $b<a$. Put $d=(a-b)/2$. Their intersections with a square window
of side $c$ cover area $A$ and have total perimeter $P$. Divergence about each
inner-square center gives

$$
4A/b-P=\sum_{\text{window edges}}(2h/b-1)\,\ell.
$$

Here $h$ is the signed distance from that center and $\ell$ is the clipped edge length.
Only $h>b/2$ contributes positive charge.

Normalize $b=1$ and fold the orientation to $u=\cos\theta\ge v=\sin\theta\ge0$. Write
$H=(u+v)/2$. For $v>0$ and $1/2\le h\le H$, the tip chord has length $(H-h)/(uv)$. The
inward parallel chord at $h-3/5$ has length

$$
\min\left(1/u,\;[H-\lvert h-3/5\rvert]/(uv)\right).
$$

With $t=\tan(\theta/2)$, $w=u+v$ and $h=(1+(w-1)z)/2$, the charge divided by this inward
length is the larger of

$$
\frac{t(1-t)^2z(1-z)}{1+t^2},\qquad
\frac{(w-1)^2z(1-z)}{w-2\lvert h-3/5\rvert}.
$$

Both are less than $\rho=17/500$. An independent exact proof replaces the source’s
angle/depth grid:

1. Since $z(1-z)\le1/4$, the first inequality follows from $4\rho(1+t^2)-t(1-t)^2>0$. On
   each of the eight intervals $[j/16,(j+1)/16]$, all four cubic Bernstein coefficients
   are positive. The receipt retains every coefficient.
   These intervals cover the larger domain $0\le t\le1/2$.
2. Put $x=w-1\le X=207107/500000$, with $(1+X)^2>2$. The second denominator is either
   $4/5+x(1+z)$ or $6/5+x(1-z)$. In each branch the ratio increases with $x$ and the
   branches join continuously.
   At $x=X$, subtracting the numerator from $\rho$ times either denominator gives a
   quadratic in $z$ with positive leading coefficient and negative discriminant.
   Both exact discriminants are in the receipt.

The tangential displacement can be bounded by $b$, strengthening the source’s $1.01b$
enclosure. For $b=1$, the tip interval is

$$
[(-1/2+vh)/u,\;(1/2-uh)/v].
$$

Intersecting the two strip constraints $\lvert ux+vy\rvert\le1/2$ and
$\lvert-vx+uy\rvert\le1/2$ gives the inward interval.
Its upper endpoint minus the tip’s lower endpoint is at most $(1-(3/5)v)/u\le1$, since
$t<3/5$. The opposite displacement is at most the smaller of

$$
F(t)=\frac{1+t^2}{2(1+t)}+\frac{6t}{5(1-t^2)},\qquad
G(t)=\frac1{5t}+\frac45t.
$$

On $[0,2/5]$, $F$ increases and $F(2/5)=69/70<1$. On $[2/5,\sqrt2-1]$, $G$ decreases and
$G(2/5)=41/50<1$. These monotonicities follow from $F'\ge-1/2+6/5>0$ and
$G'=4/5-1/(5t^2)<0$ for $t<1/2$. The $t=0$ case has no positive charge.

Every inward chord therefore lies within the edge’s tangential span extended by $b$ at
either end. The chords have disjoint interiors because their inner squares do.
Their summed lengths are at most $c+2b$ on each side.
Hence

$$
P\ge4A/b-4\rho(c+2b),
$$

which also proves the source’s weaker constant $D=4\rho(c+2.02b)$.

For $m$ positive-area pieces, expand each by a disk of radius $d$. Each expansion
remains inside its outer square and inside the expanded window, and the expansions have
disjoint interiors. The polygon parallel-area formula yields

$$
A+dP+\pi d^2(m-1)\le c^2+4cd.
$$

Combining these inequalities and $A\le mb^2$ proves the source’s coarse integer-count
area bound for any separately justified rational lower bound $0\le p\le\pi$. It is enough to
maximize over $1\le m\le\lceil c^2/b^2\rceil$, also including zero: after this
threshold, the $mb^2$ bound has stopped binding and the perimeter-derived bound
cannot increase. This review does not claim to have rerun the source’s Machin-series check of
its numerical $p$.

The interior-count refinement is also justified at the level of its argument.
An inset of $\sqrt2(b+d)$ ensures that every inner square meeting the inset has its full
outer square inside the window.
Substituting that outer square for the rounded expansion adds $(4-\pi)d^2$ of area.
If $R$ squares meet the inset of side $h$, then $R\ge(A-c^2+h^2)/b^2$. A nonnegative
rational coefficient below $4-\pi$ gives the claimed strengthened inequality, even when
this latter lower bound on $R$ is negative.

## Final n162 and n318 Composition

The scalar audit matched each final side to the table, checked the
area-plus-line-plus-surplus identity, checked positive reserves and margin, bound the
surplus and prior side to the corresponding wall result, and proved strict shrink.
The exact margin fractions remain in the receipt; decimal figures below only indicate
scale.

| Count | Final side | Exact-sign result | Gap below test-square cap |
| --- | --- | --- | --- |
| 162 | $12896484854176723/10^{15}$ | Margin $>0$, approximately $2.554525476\times10^{-16}$ | $3363789673429403/100839000000000000000>0$ |
| 318 | $1797459518711171/10^{14}$ | Margin $>0$, approximately $4.327613216\times10^{-15}$ | $3805902400849/3338100000000000000>0$ |

The strict shrink keeps the closed inner squares disjoint even where outer boundaries
touch. Conditional on every capture and reserve inequality, the positive margin excludes
the closed board at the filed side, and compactness yields the stated strict lower
bound.
At a cap where $a=b$, the same reasoning generally excludes only smaller sides and
must retain a weak inequality.

D’s `overnight/fine_chords.py` uses a finer density enclosure and exterior-strip
integration than the coarse proof above.
Its reverse running maximum has the appropriate direction: a strip may receive mass from
every box whose rounded displacement reaches it.
Reading that accumulation and the final fractions does not establish all input interval
bounds or complete pose coverage.
The exact positive margins therefore remain conditional, especially at their small
scale; floating-point agreement would be inadequate.

## Compressed Files

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `scalar-audit.json.gz` | receipt | `3974676e451376551edc5bfc13b1a833f56b4ed8` | `b09af7dd29b258798842deeca1e1e367520539d38d970561af8a92d07247636b` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
