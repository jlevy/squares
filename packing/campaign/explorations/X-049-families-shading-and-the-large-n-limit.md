---
title: X-049 — families of known-best packings, contact shading, and the large-n limit
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-049
  title: Families of Known-Best Packings, Contact Shading, and the Large-n Limit
  date: '2026-10-02'
  author: Claude session-168 coordinator, with five delegated lanes (literature, family census, contact-shade census, asymptotics, exact regularization)
  campaign: packing.squares
  brief: >-
    The owner's questions after the atlas triangle view: have the families visible by
    position relative to k^2 been studied; are lighter-than-dark-green axis-aligned
    squares inexact arithmetic; can exact regularization fix the ones that are not; how
    do the families behave as n grows, is the limiting set of patterns finite, and does
    the research frontier carry these questions.
  sources:
  - packing/atlas/known-best/manifest.json
  - packing/witnesses/known-best/
  - packages/workbench/src/core/geometry.ts
  - packages/workbench/src/view/colour.ts
  - packing/campaign/explorations/X049-families-data/family-census.json
  - packing/campaign/explorations/X049-families-data/contact-shade-census.json
  - packing/frontier/README.md
  - packing/frontier/RESULTS.md
  - packing/frontier/asymptotic-waste-bounds.yaml
  - packing/campaign/hypotheses/H-035-asymptotic-primitive-finite-transfer.md
  - packing/campaign/hypotheses/H-037-asymptotic-waste-exponent.md
  - packing/campaign/hypotheses/H-044-chunk-expressibility-of-records.md
  - packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.md
  - packing/resources/papers/gobel-1979-geometrical-packing-and-covering-problems.pdf
  - packing/resources/papers/kearney-shiu-2002-efficient-packing-unit-squares.md
  - packing/resources/papers/nagamochi-2005-packing-unit-squares-in-a-rectangle.raw.md
  - packing/resources/papers/arslanov-improved-packings-n-n-1.md
  - packing/resources/papers/bentz-2010-optimal-packings-13-and-46.md
  - packing/resources/papers/erdos-graham-1975-on-packing-squares-with-equal-squares.pdf
  - packing/resources/papers/roth-vaughan-1978-inefficiency-packing-squares.md
  - packing/resources/papers/wang-dong-li-2016-new-result-packing-unit-squares.raw.md
  - packing/resources/papers/square-packing-good-squares-2504.09489.md
  - packing/resources/papers/square-packing-x06-wasted-area-2508.04603.md
  - packing/resources/papers/mcclenagan-2026-optimally-packing-large-square.md
  - packing/resources/papers/graham-lubachevsky-1996-repeated-patterns-dense-packings-disks-square.raw.md
  - packing/resources/web/kingbird-squares-in-squares.md
  - packing/resources/web/kingbird-squares-in-squares-gobel-squares.md
  - packing/resources/web/kingbird-squares-in-squares-gobel-strips.md
  - docs/project/research/research-2026-09-07-square-packing-sources-beyond-100.md
  - https://arxiv.org/abs/2609.37410
  proposes:
  - H-269
  - H-270
  - H-272
---
# X-049: Families of Known-Best Packings, Contact Shading, and the Large-n Limit

**Status: an exploration with three new instruments and no verdict.** It answers four
owner questions at the evidential scope each allows.
Every retained number comes from one of three tools listed under
[Instruments](#instruments); the literature claims cite the archived source or a dated
web read. No bound moved, no witness changed, and no hypothesis was registered.
The epic is `think-los0`; the session record is
[session-168](../agent-sessions/session-168-known-best-families-and-shading.md).

## The Answers in Brief

1. **Have the families been studied?** One at a time, never as a taxonomy.
   The literature has named constructions with closed-form sides (Göbel’s strips and
   squares, Friedman’s off-centre square) and a few theorems about whole families
   (Nagamochi for $k^2-1$ and $k^2-2$, Kearney–Shiu for $n^2+1$, Arslanov et al.
   for $n^2-n$, Bentz for $k^2-3$ up to $k=7$). Nobody has classified best-known square
   packings by $n-k^2$; the closest precedent is for equal circles in a square, where
   Graham–Lubachevsky and Nurmela–Östergård track pattern series against $k^2$. The
   [family census](#what-the-atlas-shows) is the first such classification here, and it
   is descriptive.
2. **Is light shading inexact arithmetic?** No.
   In the homepage atlas 7,725 of 45,468 green squares render light; 5,272 border a
   tilted square, an empty region or a staggered row, and 2,419 sit beside a real gap or
   sideways shift of $2\times10^{-5}$ to 0.5 in the retained coordinates.
   Only 34, in nine optimizer-sourced records, miss every contact by less than ten times
   the renderer’s $2\times10^{-6}$ tolerance, the one band where precision could be the
   cause. See [Why Grid Squares Render Light](#why-grid-squares-render-light).
3. **Can exact regularization fix it?** For the slack squares, yes, as a derived view
   verified twice over $\mathbb Q$ at the certificate’s side: at the six named cases the
   atlas’s light green squares fall from 545 to 242 with no change of side.
   The rest border tilted squares, offset rows or holes, and should stay light.
   The view never replaces a witness; see [Exact Regularization](#exact-regularization).
4. **What happens as $n$ grows?** Every family visible in the atlas is transient.
   For fixed $d$, $s(k^2+d)-k\to 0$ at a rate between $k^{-1}$ and $k^{-2/5}$; for
   $d=ck$ the limit is exactly $c/2$; the integer-side region at the top of each row is
   at most $O(k^{3/5})$ wide, and whether it grows without bound is open.
   Every asymptotic construction is one finite template whose tilts and strip widths
   drift with $n$; nothing proves the set of optimal patterns finite or infinite.
   The register carries the wasted-area exponent (H-037) but none of these limits.

## Instruments

| Tool | Output | Check | Cost |
| --- | --- | --- | --- |
| `devtools.classify_known_best_families` | [`family-census.json`](X049-families-data/family-census.json) | `--check`, byte for byte | 8.8 s for 324 records |
| `devtools.census_atlas_contact_shades` | [`contact-shade-census.json`](X049-families-data/contact-shade-census.json) | `--check`, byte for byte; `--witness` shades any file | 7.6 s for 324 records |
| `devtools.regularize_axis_components` | [`regularized/`](X049-families-data/regularized/) derived poses and receipt | exact feasibility twice over $\mathbb Q$ | 99 s for six cases |

Run them from `packing/` with `uv run --frozen --all-extras --group dev python -m`. Both
censuses read the retained witnesses as projected geometry and declare
`exploratory-no-verdict`. One caveat governs every structural reading below: the 176
integer-side records are canonical row-major subsets of a $k\times k$ grid, so their
arrangement and symmetry are a drawing convention and only their side is evidence.

Three indexing conventions are named in the census and used consistently here.
A **triangle row** $k$ holds $n=(k-1)^2+1,\dots,k^2$, as the atlas draws it.
The **nearest-square offset** writes $n=k^2+d$ with $k=\operatorname{round}(\sqrt n)$,
which is how the owner named the families.
The **floor remainder** writes $n=m^2+r$ with $m=\lfloor\sqrt n\rfloor$, which is the
convention under which the L step below keeps $r$ fixed.

## Have the Families Been Studied

### What exists

| Family | Side or statement | Status | Source |
| --- | --- | --- | --- |
| $k^2$, $k^2-1$, $k^2-2$ | $s=k$ | proved by Nagamochi 2005, Theorem 2; see the correction below | [Nagamochi 2005](../../resources/papers/nagamochi-2005-packing-unit-squares-in-a-rectangle.raw.md) |
| $k^2-3$ | $s=k$ | proved for $k=3,\dots,7$; reported for all $k\ge 6$ (T-064, `V0`) | [Bentz 2010](../../resources/papers/bentz-2010-optimal-packings-13-and-46.md), [Bentz 2016](../../resources/papers/bentz-2016-optimal-packings-22-and-33.md), [RESULTS](../../frontier/RESULTS.md) |
| $k^2-4$ | $s=k$ | proved at $k=5,6,7$ (T-051–T-053) | [frontier README](../../frontier/README.md) |
| $n^2-n$ | $s(n^2-n)<n$ for $n\ge 12$ | proved by construction | [Arslanov et al. 2021](../../resources/papers/arslanov-improved-packings-n-n-1.md) |
| Göbel strip | $a+1+1/\sqrt2$ at $n=a^2+a+3+\lfloor(a-1)\sqrt2\rfloor$ | best known for $a<44$ except $a=3$; proved at 5 and 10 | [DS7](../../resources/papers/friedman-ds7-packing-unit-squares-in-squares.md) §2; [Kingbird strips](../../resources/web/kingbird-squares-in-squares-gobel-strips.md) |
| Göbel square | $a+1+b/\sqrt2$ at $n=2a(a+1)+b^2$, $a-1<b/\sqrt2<a+1$ | best-known upper bounds | DS7 §2; [Kingbird squares](../../resources/web/kingbird-squares-in-squares-gobel-squares.md) |
| Off-centre square plus column | $a+3/2+b/\sqrt2$ at $n=2a^2+4a+b^2+1$ | best known at 26, 85, 227 | DS7 §3 |
| $n^2+1$, Pell subfamily | $\delta=k/\sqrt2-t\downarrow 1/2$ at $(2t+1)^2+1=2k^2$ | proved construction | [Kearney–Shiu 2002](../../resources/papers/kearney-shiu-2002-efficient-packing-unit-squares.md) §4 |
| $n^2+1$, general | $\delta_n<3/(2n)^{1/3}+3/(2n)^{2/3}$ | proved | Kearney–Shiu 2002 |
| Friedman’s Conjecture 1 | $s(n^2-k)=n\Rightarrow s((n+1)^2-k)=n+1$ | conjecture | DS7 §3 |

Here $\delta_k=s(k^2+1)-k$, Kearney–Shiu’s notation.
Kingbird’s group pages (Göbel squares, Göbel strips, the $s(n^2-n-1)$ pattern, rigid
packings) and its “Extends” and “Adds an L” credit lines are catalogue groupings with no
theorem behind them.
The literature lane’s dated negative searches (2026-10-02) found no taxonomy keyed by
$n-k^2$, no OEIS sequence for $s(n)$, and no progress on Friedman’s Conjecture 1.

### Why the triangle shows columns: the L step

DS7 §2 states the elementary construction behind most of the visible repetition: if $n'$
squares fit in side $s'$, then $n'+2\lfloor s'\rfloor+1$ squares fit in side $s'+1$, by
adding an L of squares along two walls.
For $n'=m^2+r$ with $m<s'<m+1$ the L adds $2m+1$, which lands on $(m+1)^2+r$: the same
column of a left-justified triangle, at the same excess $s-m$. So the excess is
non-increasing down a column, which is a theorem about upper bounds.

The census measures how much of the atlas the L step actually explains.
No record violates the bound, so the atlas is consistent with it.
Of the 148 non-integer records, 130 have an L candidate one row up; 32 are exactly that
candidate’s L-extension and 98 beat it, by margins from $3.2\times10^{-5}$ (127 against
the L of 106) to 0.116 (27 against the L of 18). Columns therefore repeat a packing in
about a quarter of the cases where they could; the rest of the visible similarity is a
family constructed again at the larger size, not the same packing carried down.

The non-integer L chains are 5–10, 27–38, 52–67–84, 65 through 290 (nine steps),
104–125, 124–147, 148–173–200–229–260, 149–174–201, 150–175, 151–176, 171–198, 172–199,
203–232, 227–258, 230–261, 231–262–295, 233–264 and 265–298.

## What the Atlas Shows

### The integer-side region

Every row ends in a run of integer-side records, contiguous up to $k^2$. The best-known
$d_{\max}(k)$, the largest $d$ with $s(k^2-d)=k$ in the atlas, is $d_{\max}(k)=k$ for
$k\le 10$, then 10, 11, 12, 13, 13, 14, 15, 16 for $k=11,\dots,18$. These are best-known
values, not proved ones: Nagamochi’s theorem reaches $d=2$, the register reaches $d=3$
and 4 at a few $k$, and everything beyond is the grid holding because nobody has beaten
it. So the owner’s observation that $k^2-1$ and $k^2-2$ are clean grids holds, but the
integer run is much wider than those two offsets: it is complete through $d=-13$
wherever the atlas reaches.

### The $k^2+1$ family

All 16 records with $n=k^2+1$ have non-integer sides.
Fourteen contain 45-degree squares and have non-trivial symmetry (D4 at 5, 65, 101, 145
and 197). The two exceptions are 17 (Bidwell: tilts near 40 and 53 degrees, no symmetry)
and 50 (side $53/7$, sixteen squares on 3-4-5 tilts, C2). The sides pass through three
regimes: $k+1/\sqrt2$ at $k=2,3$; no common form at $k=4,\dots,7$; and from $k=8$ to 17
a plateau at $s-k=5/\sqrt2-3\approx 0.53553$, the Göbel square at 65 carried down by L
steps. At 170, 257 and 290 the source draws a different arrangement with the same side.
Kearney–Shiu already beat the plateau at $k=42$ and $k=43$, so it is not the family’s
limit; see [the large-n limit](#the-large-n-limit).

### The $k^2+2$ offset is not one family

Its 15 non-integer records use five different closed forms or none: 27 and 38 are Göbel
strips, 66 is $3+4\sqrt2$, 171 and 198 are $95/7$ and $102/7$, 227 and 258 belong to the
off-centre series, and 291 is 290 plus one square at the same side.
Seven (11, 18, 51, 83, 102, 123, 146) match no closed form in the census library.
What the offset shares is short L-linked pairs and a borrowed $k^2+1$ packing.

### Equal-side pairs: 232–233 and 264–265

Both pairs have equal sides, $8+\tfrac{11}{2}\sqrt2$ and $9+\tfrac{11}{2}\sqrt2$. Every
square of the smaller record reappears in the larger under the identity alignment, all
121 45-degree squares included: these are Göbel squares $(a,b)=(7,11)$ and $(8,11)$, and
the smaller record is the larger with a corner square removed.
264 is the L-extension of 233, and 298 of 265. The only non-integer equal-side pairs in
the atlas are 147–148, 232–233, 264–265, 290–291 and 295–296, each with a Göbel
construction as its upper member.
That pairing is how the catalogue presents them, not a theorem.

### The diagonal records: 268–269 and 301–302

These four share a layout rather than a packing.
Between the members of each pair there is no equal side, no L relation and no shared
tilted square; the tilted squares sit at about 70 degrees in 268, near 45 in 269,
between 55 and 61 in 301, and between 41 and 51 in 302. What they share is tilted
squares strung along a container diagonal.
301 and 302 sit at the same offsets one row below 268 and 269 but beat their
L-extensions, by 0.0321 and 0.0200. Their lineage, traced by the catalogue’s credits,
runs back to Friedman’s 1997 width-2 diagonal strips at 70 and 88 and Cantrell’s 37;
nobody names it as a family.
A declared band rule (tilted centres elongated at least fivefold within 10 degrees of a
diagonal) selects 56 records, and in each row from $k=9$ to 17 a run of such offsets
moves right as $k$ grows: 86–88, 106–108, 127–130, 151–153, 176–179, 204–207, 234–237,
266–269, and 299, 300, 302.

### Closed forms and symmetry

Of the 148 non-integer sides, 56 match a closed form $a+b\sqrt2$ or a small rational (42
in the declared small library, 14 more in a declared wider tier that catches the
121-square diamond family and the $53/7$-type 3-4-5 sides); every residual is at most
$8\times10^{-15}$. The families that recur most are $m+\sqrt2/2$ (16 records), the
$k^2+1$ plateau (11), $-5+4\sqrt2$ (9) and $-7+\tfrac{11}{2}\sqrt2$ (8).

**Symmetry follows the source, not the family.** At $10^{-6}$, 68 of the 97
Kingbird-derived records are symmetric, against none of the 50 packet-derived records
(Couzo, de Winter) and none of the UnitSquare record.
Every closed-form side is symmetric; 80 of the 92 non-integer sides without one are not.
Kingbird draws constructions and the packets are optimizer output, so the “fully
symmetric” impression at $k^2+1$ is partly a property of who drew the packing.
Thirty-eight records also have squares between $10^{-6}$ radians and half a degree off
axis; at 301, 149 squares are exactly axis-aligned and 247 within half a degree.

## Why Grid Squares Render Light

### Which rule draws the atlas

Two renderers shade squares, with different rules, and the census replicates both.

- **The homepage atlas**, Grid and Triangle views, copies its fills from the committed
  house renderings `atlas/known-best/rendering/n-NNN.svg`, shaded by
  `sqpack.render.color`. A side counts when an edge of the square coincides with a wall
  or with a same-orientation square’s edge at both endpoints within $2\times10^{-6}$,
  orientations agreeing within $10^{-6}$ radians, on the full-precision witness.
  Shade is four minus the counted sides.
- **The workbench catalogue stage** recomputes contacts in `core/geometry.ts` with a
  0.01 gap and a half-degree angle class, on frames rounded to $10^{-6}$. Its animation
  studio uses a 0.004 gap.

The replicas agree with the originals on all 52,650 squares: the house replica with each
SVG’s recorded contact count, and the stage replica with the TypeScript run under Node.
For each light green square the census sweeps each face without a contact and names the
first cause that applies: an empty region (`hole-or-open`), a tilted neighbour, an
aligned neighbour offset by more than a tenth of a side, a slide of more than ten
tolerances (`slack` or `misaligned`), or a miss within ten tolerances (the band).

### What it found

| Source of the witness | Records with light | Light of green | Structural | Slack | Within band |
| --- | --- | --- | --- | --- | --- |
| Exact grids | 158 of 176 | 1,110 of 27,570 | 1,110 (all holes) | 0 | 0 |
| Kingbird-derived | 97 of 97 | 2,350 of 10,572 | 2,343 | 7 | 0 |
| Packet-derived (Couzo, de Winter) | 50 of 50 | 4,234 of 7,284 | 1,800 | 2,400 | 34 |
| UnitSquare rendering ($n=69$) | 1 of 1 | 31 of 42 | 19 | 12 | 0 |

*House rule, from the census’s `rules` summary.*

The contacts the renderer does detect carry residuals with a median of zero, a 99th
percentile of $1.1\times10^{-12}$ and a maximum of $2.0\times10^{-6}$, so where squares
touch, the arithmetic is fine.
The light squares are light for four reasons:

- **Vacancies in the grids.** In all 34 records at $k^2-1$ and $k^2-2$, exactly the
  squares beside the one or two empty cells render light, 84 squares with three contacts
  each, and nothing else does.
  Every one of the 1,110 light squares in exact grids has a single non-contact face, and
  it looks into an empty cell.
- **Tilted neighbours.** In the Kingbird-derived records nearly every light square
  (2,343 of 2,350) touches a tilted square, which by definition cannot share a full
  side.
- **Loose optimizer output.** In the packet-derived records contacts and misses form one
  continuum from $10^{-13}$ to 0.1, and 90 percent of the light faces miss by $10^{-4}$
  or more: fifty times the tolerance and eight decades above the witness’s $10^{-12}$
  check. The source optimizer left these squares loose; the side is set by the tilted
  structure, and the grid part has room.
  At 102 every one of the 69 green squares is light: its top row sits 0.0298 from the
  left wall and 0.0030 apart.
- **A digitized record.** $n=69$ was read from a rendering at six decimals, and its 12
  slack squares miss by $2\times10^{-5}$ to $3.5\times10^{-4}$. It is the one record
  where coordinate precision plausibly explains the shading.

The 34 within-band squares are in 102, 103, 130 (14 squares), 152, 199, 206, 236, 297
and 307, all packet-derived, missing by $2\times10^{-6}$ to $2\times10^{-5}$. They are
consistent with the optimizer stopping short of convergence, which is still not rounding
in the record.

On the workbench stage, whose 0.01 gap swallows small shifts, 6,043 of 45,743 green
squares render light, 5,208 of them structurally.
Its 822 within-band squares miss by 1 to 10 percent of a side, far above any arithmetic.
The 265 near-axis squares, tilted between $10^{-6}$ radians and half a degree, are not
green in the atlas at all; on the stage they are, and their tilt alone explains 6 light
squares.

The census also lists, per record, the squares a slide could darken: 2,453 squares in 54
records under the house rule, 49 of them packet-derived.
That list is face by face and does not show every face can close at once; the
regularization prototype below is what tests it.

## Exact Regularization

**Yes for slack squares, as a derived view verified exactly; no for the structural
ones.** The prototype is `devtools.regularize_axis_components`, and its outputs for the
six named cases are retained under
[`X049-families-data/regularized/`](X049-families-data/regularized/).

### The definition and its boundary

A regularized view starts from the exact frame the record already certifies, not from
the decimal witness.
All six named cases are Couzo packings (T-056) with rational certificates at 36 digits;
the view uses the certificate’s exact side $S$, which equals the printed side at 102 and
268 and lies above it by one or two units of the fifteenth decimal at the other four.
Then:

1. every square tilted more than $10^{-4}$ radians stays exactly as certified;
2. every square within $10^{-4}$ radians is replaced by the exactly axis-aligned unit
   square at the same rational centre, where that is exactly feasible;
3. each such square slides along one axis toward the nearest lattice position,
   $\tfrac12+i$ from one wall or $S-\tfrac12-j$ from the other, and stops at the first
   exact contact, computed over $\mathbb Q$; a slide is kept only if it is a snap of at
   most $10^{-9}$, ends on a wall or an axis-aligned square without lowering that
   square’s contact count, or raises it;
4. the result is verified twice over $\mathbb Q$, by `sqpack.verify.verify_packing` and
   by the independent `devtools.check_rational_witness_independent`.

The view never replaces the source witness, never changes the side, and never promotes
an evidence tier: it proves nothing the certificate had not already proved, and any
drawing of it must say “regularized”.
Where $S$ exceeds the printed side by a unit in the fifteenth decimal, the precise
statement is “feasible at the verified upper bound”.

Two facts make the definition necessary rather than fussy.
A square tilted by $\theta$ protrudes $\theta/2$ past a wall-seated lattice slot, so the
certificate’s “axis” squares, tilted by about $10^{-17}$ from 36-digit rounding, are all
off their lattice by that much: no exact lattice statement exists until they are
straightened.
And straightening can fail, because two squares tilted opposite ways can be
separated while their straightened copies overlap; the exact check refused one such
square, at 206.

### Results

| $n$ | Atlas: light of green, before | after | Stage: light before | after | Largest move | Exact check | $S$ − printed side |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 102 | 69 of 69 | 24 of 70 | 49 | 26 | 0.163 | passed | $-1.1\times10^{-15}$ |
| 103 | 56 of 61 | 29 of 61 | 48 | 31 | 0.192 | passed | $+1.5\times10^{-16}$ |
| 106 | 41 of 83 | 21 of 83 | 21 | 21 | 0.0055 | passed | $+3.5\times10^{-16}$ |
| 206 | 104 of 136 | 60 of 138 | 69 | 59 | 0.365 | passed | $+1.1\times10^{-15}$ |
| 268 | 156 of 198 | 75 of 198 | 86 | 68 | 0.362 | passed | $-1.6\times10^{-15}$ |
| 269 | 119 of 224 | 33 of 225 | 44 | 33 | 0.015 | passed | $+4.1\times10^{-16}$ |

*“Atlas” is the house rule the homepage atlas draws with; “stage” is the workbench rule
the regularizer optimizes against.
Under the atlas rule the six records go from 545 light green squares to 242; under the
stage rule from 317 to 238. Straightening adds a few squares to the green family (102,
206, 269). At 206 two already-light squares lost one contact on the stage; no dark
square turned light.
Moves and exact checks are from [`run.txt`](X049-families-data/regularized/run.txt), one
99-second run; the shading is from
[`shades.txt`](X049-families-data/regularized/shades.txt), the census’s `--witness` mode
applied to the source and regularized files.
The regularized poses are retained gzipped; decompress one before passing it to
`devtools.check_rational_witness_independent`, which on the 106 view reports 106
squares, 5,565 pairs and a minimum pair gap of zero.*

The remaining light squares are what the packing looks like: faces against tilted
squares, rows offset by part of a side, holes where the two walls’ lattices disagree
(the 0.607 gap in 102’s top row), and, at 206, a twisted near-lattice of 33 squares
tilted between 0.01 and 0.39 degrees that the atlas’s half-degree colour class calls
axis-aligned. No case needed a change of side.

### The atlas-wide layer

The prototype above became a derived layer under `think-bgkz`, retained in
[`atlas/known-best/regularized/`](../../atlas/known-best/regularized/index.json): one
gzipped view per regularized record and an index of digests and counts, never a witness
change. Two rules were added first.
A move that costs any other square a contact, under either the house rule or the stage
rule, is undone and the run repeats from the exact frame until no count falls; and a
slide may not lower its own square’s count under either rule.

| Measure | Value |
| --- | --- |
| Records regularized | 51: all 50 packet-derived records and $n=26$ |
| Unchanged | 183, including all 176 exact grids |
| Refused | 90: 89 Kingbird-derived records whose 36-digit pose overlaps at dilation 1, and $n=69$, whose corners are decimal |
| Light green squares, house rule | 7,725 → 5,475 |
| Light green squares, stage rule | 6,043 → 5,466 |
| Squares made lighter | 0; 57 squares in 9 records are held by the non-regression rule |
| Six named cases, house rule | 545 → 246 (the prototype’s 242 included moves the rule now holds) |

*From the index’s totals and `devtools.regularize_axis_components --check-atlas`.*

`--check-atlas` compares digests in about a tenth of a second and runs in the records
tier; `--verify-atlas` re-derives every view, about 800 cpu-seconds (223 s at four
workers), and runs as the deferred `regularized-views` job.
The prototype’s six-case receipt above is superseded for 206 by the layer, which holds
three squares there.
The homepage atlas draws the views behind an “Atlas drawings” toggle
(`?layer=regularized`), each tile badged and drawn by the house renderer from
`devtools.render_regularized_atlas`. The 89 refused Kingbird records stay refused.
Every one verifies at its smallest dilation ($1+10^{-31}$ to $1+10^{-27}$), but 75 of
those views would be exact packings below the register’s verified upper bound, which is
a tier promotion. The other 14 would enlarge the container past the printed side.
And the gain is two squares across all 89. The atlas README records the measurement.
Algebraic-field witnesses, where the same algorithm runs in $\mathbb Q(\alpha)$, were
not prototyped; interval-enclosure witnesses admit no exact lattice statement at all.
The workbench stage legend now says that a lighter grid square can be loose in the
source packing rather than short of neighbours.
The homepage atlas carries no such sentence: the owner removed the notes under the atlas
grid on 2026-10-02 (`think-l38m`), and this branch follows that decision.

## The Large-n Limit

### What is proved

Write $W(x)=x^2-N(x)$, where $N(x)$ is the most unit squares that fit in side $x$. The
current upper bound is $W(x)=O(x^{3/5})$ (Bui 2025; McClenagan 2026), with no hypothesis
on the fractional part of $x$, which their constructions absorb into a strip width;
Chung and Graham’s 2020 claim of the same exponent contains an error.
The only lower bound is Roth–Vaughan 1978: if $x(x-\lfloor x\rfloor)>1/6$ then
$W(x)\gg(\lVert x\rVert x)^{1/2}$, where $\lVert x\rVert$ is the distance to the nearest
integer. Translating these into the owner’s families (derivations by the asymptotics
lane, checked by the coordinator):

- **Fixed offset $d\ge 1$.** The area bound and the upper bound give
  $\frac{d}{2k}-\frac{d^2}{8k^3}\le s(k^2+d)-k\le\frac{d}{2k}+\frac{C}{2}\frac{(k+1)^{3/5}}{k}$.
  Every fixed-offset family converges to the integer $k$, at a rate between $k^{-1}$ and
  $k^{-2/5}$. Which end is right is open; it is Bui’s Question 1 and Kearney–Shiu’s
  exponent $\beta$, now known to satisfy $2/5\le\beta\le 1$.
- **Offset proportional to the row, $d=ck$.**
  $\lim_{k\to\infty}[s(k^2+\lceil ck\rceil)-k]=c/2$. Any $W(x)=o(x)$ suffices, so this
  has been a theorem since Erdős–Graham 1975. At mid-row, Roth–Vaughan forces
  $s(k^2+k)>k+\tfrac12$ strictly for all large $k$.
- **The integer-side region.** At $x=k-\varepsilon$ the upper bound packs
  $k^2-2k\varepsilon-Ck^{3/5}$ squares, so $s(k^2-d)<k$ once $d>Ck^{3/5}+1$:
  $d_{\max}(k)=O(k^{3/5})$. Below, $d_{\max}(k)\ge 2$ (Nagamochi) and
  $d_{\max}(k)\le k-1$ for $k\ge 12$ (Arslanov).
  Whether $d_{\max}(k)\to\infty$ is open, and no lower bound keyed to $\lVert x\rVert$
  can decide it: proving $s(k^2-d)=k$ needs $W(k-\varepsilon)>d-2k\varepsilon$ for every
  $\varepsilon>0$, and Roth–Vaughan’s bound tends to zero there.
  Göbel asked the question in 1979, p. 180.
- **Across all $n$.** $s(n)-\sqrt n=O(n^{-1/5})$, and on the mid-row subsequence
  $s(n)-\sqrt n\gg n^{-1/4}$. This is the face H-037’s exponent question shows at finite
  $n$.

### What the finite data show

The atlas is far from the asymptotic regime, and every visible family is provably
transient.

| $k$ | $d=+1$ | $d=+2$ | $d=+3$ |
| --- | --- | --- | --- |
| 2 | 0.7071 | 1.0000 | 1.0000 |
| 5 | 0.6213 | 0.7071 | 0.8244 |
| 8 | 0.5355 | 0.6569 | 0.7071 |
| 12 | 0.5355 | 0.6009 | 0.6569 |
| 17 | 0.5355 | 0.5355 | 0.5972 |

The table gives the excess $s(k^2+d)-k$ for selected rows, from the census’s
`excess_table`.

- The $k^2+1$ plateau at 0.53553 holds for every $k$ from 8 to 17; the first known
  improvement is Kearney–Shiu’s at $k=42$.
- The Göbel strip sits at $d_G(k)=3-k+\lfloor(k-2)\sqrt2\rfloor\approx 0.414k$ with
  excess exactly $1/\sqrt2$ in all 13 rows $k=5,\dots,17$. The proved limit at that
  offset is about 0.207, so this family must eventually be beaten.
- The largest excess over the area bound in each row stays between 0.53 and 0.59 for
  every $k$ from 2 to 18, where the theorem says it decays like $k^{-2/5}$ eventually.
- Mid-row $s(m^2+m)-m$ is 1 for $k\le 10$ and 0.9634 at 306, against a proved limit of
  $1/2$.
- Taking Wang–Dong–Li’s explicit constant $16\sqrt2+38$ at face value (their threshold
  $x_0$ is not printed), their construction beats the grid region only for
  $k>(16\sqrt2+38)^{8/3}\approx 5.7\times10^4$. Hand-tuned constructions do far better,
  which is why the crossover estimate for $k^2+1$ is “between 18 and 42”.

### Finite or infinite set of patterns

What the theory says about **structure**, as opposed to waste:

- Roth–Vaughan’s proof forces tilted squares whenever $\lVert x\rVert$ is not tiny: each
  of $\gg x$ horizontal chains needs a tilt of order $(\lVert x\rVert/x)^{1/2}$.
- Bui’s good-squares theorem shows that removing every square tilted more than
  $10^{-10}$ costs at most a constant factor in $W$. Forty-five-degree ingredients are
  asymptotically dispensable up to a constant, which is not the same as absent.
- Every upper bound from Erdős–Graham to McClenagan is one finite template: grid bulk,
  boundary strips of width about $x^{4/5}$ filled by stacks tilted about $x^{-2/5}$, and
  end trapezoids filled by a second-level primitive.
  The template is finite; its parameters never stop changing.
- On the proof side, one unavoidable-set template per offset proves $d=-1,-2$ for all
  $k$ (Nagamochi), and one periodic measure reportedly proves $d=-3$ (T-064).

The owner’s question becomes precise in three forms, strongest first.
Call a *template* a finite recipe of regions (grid blocks, stacks of $L$ squares at a
tilt, a bounded list of filler primitives) with continuous parameters.

- **F1.** A finite set of templates contains an optimal packing for every $n$. Falsified
  by a sequence of $n$ whose optima need unboundedly many orientation classes that no
  single template’s parameter drift explains.
  Open, even for $k^2+1$.
- **F2.** The same, up to a constant factor in $s(n)-\sqrt n$. The construction chain
  and Bui’s theorem are evidence for this form; unproved.
- **F3.** For each fixed $d$, one periodic certificate proves $s(k^2-d)=k$ for all
  $k\ge k_0(d)$. Proved for $d\le 2$, reported for $d=3$, and impossible for $d$ beyond
  $O(k^{3/5})$.

Nothing in the literature proves the pattern set finite or infinite.
What is proved is that the finite atlas families—the 45-degree blocks at $d=1$, the
$1/\sqrt2$ strips at $d\approx 0.414k$, and the grid down to $d\approx -k$—are all
transient.

## What the Frontier Carries

| Question | Carried by | Gap |
| --- | --- | --- |
| Wasted-area exponent | [H-037](../hypotheses/H-037-asymptotic-waste-exponent.md), [`asymptotic-waste-bounds.yaml`](../../frontier/asymptotic-waste-bounds.yaml) | the $s(n)$ translation, Kearney–Shiu as the $\delta_k$ source, the explicit Wang–Dong–Li constant |
| Asymptotic primitives at finite $n$ | [H-035](../hypotheses/H-035-asymptotic-primitive-finite-transfer.md) | predicts failure on the $k^2+1$ family below $k=42$; not stated |
| Integer-side families | T-007, T-064, T-051–T-053, the frontier’s gap table | $d_{\max}(k)$ as a question; T-007’s proof gap (below) |
| Structure of records | [H-044](../hypotheses/H-044-chunk-expressibility-of-records.md)–H-047, X-003, X-008, calibration-only at $n\le 100$ | no family taxonomy, no L-chain account, no source-symmetry confound |
| Limits of families | nothing | the rate at fixed $d$, the $c/2$ limit, $s(k^2+k)>k+\tfrac12$, F1–F3 |
| Atlas shading semantics | the page legend only | the legend does not say that a light square can be loose rather than short of neighbours |

### Candidate hypotheses, for the codifier

None is registered here; each names its falsifier.

1. **Periodic certificates reach $d=4$ and $d=5$.** Daniel’s periodic-measure
   construction extends to $s(k^2-4)=k$ and $s(k^2-5)=k$ for all $k\ge k_0(d)$.
   Falsified by infeasibility of the periodic linear program at bounded period over a
   range of $k$, or by any $s(k^2-4)<k$. Value: the first proof that $d_{\max}(k)\ge 4$
   for all large $k$, and a test of Friedman’s Conjecture 1.
2. **The $k^2+1$ crossover lies between 18 and 42.** Some $k$ in that range has
   $s(k^2+1)<k+5/\sqrt2-3$ by a Kearney–Shiu strip construction.
   Falsified by an exact parameter scan of that construction finding nothing below
   $k=42$. Value: locates the start of the asymptotic regime on the cleanest family and
   scopes H-035.
3. **$\beta=2/5$.** $\delta_k\asymp k^{-2/5}$, so Bui’s Question 1 has a negative
   answer. Falsified by any construction with $\delta_k=o(k^{-2/5})$ along a sequence.
   Paper mathematics; it sharpens H-037 at its finite face.
4. **The atlas families are source artifacts in part.** Re-optimizing the 68 symmetric
   Kingbird-derived non-grid records with the packet sources’ optimizer breaks symmetry
   and lowers the side at a measurable fraction.
   Falsified if no side moves by more than $10^{-9}$. Value: separates construction
   families from optimum families.

## Corrections and Side Findings

- **Nagamochi’s Lemma 1 is false, and T-007’s proof has a gap.** H. Karakuş, “A
  counterexample to Nagamochi’s scoring lemma and a new rectangle packing bound”,
  [arXiv:2609.37410](https://arxiv.org/abs/2609.37410), 29 September 2026, now
  [archived](../../resources/papers/karakus-2026-counterexample-nagamochi-scoring-lemma.md).
  The
  [W2 review](../../../docs/project/reviews/review-2026-10-02-nagamochi-lemma1-karakus.md)
  verifies the counterexample family in exact arithmetic
  (`devtools.check_nagamochi_lemma1_counterexample`) and finds that Theorem 1 rests on
  Lemma 1 alone, so the gap reaches T-007 for every $N\ge 10$, not only through
  $s(k^2-2)$. Karakuş’s independent strip measure, re-derived step by step with no gap
  found, recovers $s(k^2-1)=k$ and a general floor
  $s(N)\ge	frac12+\sqrt{N-\lfloor\sqrt N
floor+	frac14}$ that is strictly weaker except at $N=m^2-1$. $s(k^2-2)=k$ now rests on
  chelokot’s Lean proof, read but not replayed.
  The inventory `devtools.audit_t007_consumers`, checked in the records tier, finds the
  bound operative at 287 records, 224 of them beyond T-007’s registered 4–100 scope.
  No register value has changed; `think-xucp` owns the re-grounding and `think-ym34` the
  Lean replay.
- **Two asymptotic transcriptions were wrong.** The Erdős–Graham cleaned text wrote
  Theorem (1) as $\Theta(lpha^{7/11})$ where the paper prints $O(lpha^{7/11})$
  (D-514), and the McClenagan text swapped Montgomery’s and Chung–Graham’s exponents,
  which the n11 research report then charged to McClenagan (D-515). Both are corrected
  with dated notes, and `asymptotic-waste-bounds.yaml` now records the Göbel origin of
  the $10^{-100}$ constant, Wang–Dong–Li’s explicit constant and Kearney–Shiu’s
  $\delta_k$ bounds.
- **A quoted catalogue side disagrees with the atlas.** The literature lane quoted
  $s(301)=17.8689$; the atlas, which uses Couzo’s packet at 301, has 17.846667.

## Follow-ups and Their Dispositions

| Bead | Outcome | Disposition |
| --- | --- | --- |
| `think-589i` | Review concluded; inventory tool in the records tier | retire-success |
| `think-xucp` (P1) | Re-ground the 287 floors and the $k^2-1$, $k^2-2$ values per the review | continue; awaits the owner’s choice of order with `think-ym34` |
| `think-ym34` (P1) | Replay chelokot’s Lean proof of $s(n^2-2)=n$ with an axiom receipt | continue |
| `think-ptt7` | H-269, H-270 and H-272 registered; $\beta=2/5$ parked under H-037 | retire-success |
| `think-hzv3`, `think-1n8w` | Sources archived; D-514 and D-515 corrected | retire-success |
| `think-bgkz` | Regularized-view layer | see its lane |

**Selected next entry:** `think-ym34`, the Lean replay, because it decides whether the
$k^2-2$ exact values survive the re-grounding in `think-xucp`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
