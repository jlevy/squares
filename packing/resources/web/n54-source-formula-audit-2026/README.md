# `n = 54` Source and Formula Receipt, 2026-09-01

This is the bounded `BC-126` source audit from Agenda 014. It starts from launch revision
`909efafa` and asks whether the current `n = 54` construction has more than a catalogue
value and a rounded drawing. It does. The public SVG source contains exact construction
equations and a symbolic generative layout. It still does not provide 54 labeled exact
pose rows or an independent verifier.

No packing geometry was run, no coordinates were inferred from decimals, and H-055
remains unmeasured and instrument-unready.

## Frozen inputs

| Input | Frozen fact |
| --- | --- |
| Agenda launch | revision `909efafa` |
| Retained `n = 54` witness | SHA-256 `e4bcdefa3472e23ca7f4e403b26361efca17702c20570f6144b70c3a01a96ad7` |
| Friedman DS7 PDF | SHA-256 `00f0a030654ee83270b3cbab5730e7ea678f11709ddaf3f4d40f934cf4bbe0a4` |
| Retained Kingbird current-page HTML | SHA-256 `d06590beefba61573f5ef2471d4e08afcfe4640bb8135824e0f715d0bb842ac8` |
| Retained Kingbird history-page HTML | SHA-256 `a5f0ac0c0632b652bf19c7e5e01a3425da4395c447383d3acade868812f7415a` |
| Live `square-54.svg` response | SHA-256 `96afd34f230d10c5dc750b8209fecb90bbebc01f4519cf58193051b9b7ddcaec`, 3,719 bytes, ETag `e87-626b3f84c10c0`, last modified 2024-11-12 |

The live SVG was inspected without retaining it. The repository's standing policy records
metadata and derived numerical facts only because no express redistribution terms were
found. That policy is not a legal conclusion.

## What the sources establish

The [1998 DS7 paper](https://www.combinatorics.org/files/Surveys/ds7/ds7v1-1998.pdf)
gives the first explicit genealogy. Wainwright's `n = 19` construction uses a width-two
diagonal strip at side `3 + 4 sqrt(2)/3`. Friedman extends the same mechanism to the
family

```text
N(m) = 9m^2 + 8m + 2
L(m) = 3m + 4sqrt(2)/3.
```

At `m = 2`, this gives 54 squares at side `6 + 4sqrt(2)/3`. The
[2009 DS7 revision](https://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7-2009.html)
then reports Cantrell's alternative `n = 19` constructions feeding improvements to
`n = 54` in 2002 and 2005. Those later steps are attributed to private communications,
not a published pose derivation.

The [current Kingbird catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
lists the present side

```text
7 - sqrt(2)/2 + sqrt(1 + sqrt(2))
```

and attributes the packing to David W. Cantrell in 2005 with Joe DeVincentis's 2014
improvement. The
[history view](https://kingbird.myphotos.cc/packing/squares_in_squares__compared2.html)
separates five retained stages: Stenlund, Friedman, Morandi, Cantrell, and DeVincentis.

The decisive new surface is the linked
[`square-54.svg`](https://kingbird.myphotos.cc/packing/square-54.svg) source. Its comments
credit DeVincentis for the 2014 construction and David Ellsworth for a 2023 exact
closed-form solution. They give two defining equations, exact expressions for the side
and tilt, and symbolic expressions for every named placement constant. The SVG describes
one half as axis-aligned paths and rotated rectangles, then obtains the other half by a
half-turn. This is a compact construction program, not just a raster picture.

The source structure accounts for the declared count without numerical geometry. One
half contains an 18-cell axis-aligned staircase, one further axis-aligned square, four
rotated single squares, and two divided `2 by 1` rotated blocks, for 27 unit cells. The
half-turn copy supplies the other 27. The cells are not individually labeled.

## Exact field receipt

Let

```text
p = sqrt(1 + sqrt(2)).
```

Then `p` is the positive real root in `(1.5537, 1.5538)` of

```text
p^4 - 2p^2 - 1 = 0.
```

The source side, auxiliary radical, tangent, and orientation vector all lie in the same
quartic field `K = Q(p)`:

```text
sqrt(2)                 = p^2 - 1
sqrt(1 + 5sqrt(2))      = 2p^3 - 3p
s                        = 15/2 + p - p^2/2
tan(a)                   = 2/7 - 6p/7 + p^2/7 + 4p^3/7
sin(a)                   = 1/2 - p + p^3/2
cos(a)                   = 1 + p/2 - p^2/2.
```

The side's minimal polynomial is

```text
4s^4 - 112s^3 + 1164s^2 - 5304s + 8897.
```

The positive embedding gives
`s = 7.8466671928434897829433145909582979...` and
`a = 55.2650997396489041743253949403...` degrees. The exact angle is an `ArcTan`
expression; it is not itself claimed to be algebraic. Exact packing data should encode
orientation by `(cos(a), sin(a))`, which is in `K`. Because every named SVG placement
formula uses rational operations on `s`, `sin(a)`, `cos(a)`, and their reciprocals, its
named exact quantities remain in `K` whenever their denominators are nonzero.

Reproduce this field statement, without fetching the source or running geometry, from
`packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.audit_n54_source_formula --check
```

## Pose and serialization coverage

| Surface | What exists | What is still missing |
| --- | --- | --- |
| Construction genealogy | Published 1998 `19 -> 54` family and later author-attributed improvement chain | A published derivation of the 2005/2014 construction |
| Side and orientation | Exact side and `ArcTan` tilt expressions; algebraic sine and cosine in the quartic field | A retained, licensed source copy or immutable upstream revision |
| Placement constants | Symbolic formulas in SVG comments and a generative transform tree | A parser that treats those comments as data and rejects incomplete or ambiguous formulas |
| Square coverage | The source structure accounts for 27 unit cells per half and the half-turn supplies 54 | Stable labels and one materialized exact pose row per label |
| Correspondence | A retained decimal witness derived from this URL | A frozen bijection from exact source cells to witness rows under one declared D4 action and orientation convention |
| Assurance | The retained decimal witness passes numerical feasibility | Exact wall and pairwise replay, plus a geometry mutation and a correspondence mutation |

The live source therefore changes the blocker. The first missing surface is no longer
"no exact construction formulas." It is
`exact-source-parser-and-labeled-correspondence-absent`, compounded by an unretained
mutable upstream asset. A later block can defensibly build a target-blind source parser
and correspondence manifest from this digest. It cannot promote H-055 until that parser,
54-pose coverage, independent exact geometry, and both mutations pass.

## Search log and bounded absence

The 2026-09-02 UTC searches covered the exact formula, DeVincentis and Cantrell name
paths, the journal survey archive, Kingbird, arXiv, and DOI-indexed pages:

```text
"7 -" "sqrt(2)" "sqrt(1 + sqrt(2))" square packing 54
"s(54)" "Joe DeVincentis" packing squares
"s(54)" "David W. Cantrell" packing square
site:kingbird.myphotos.cc/packing "54" "DeVincentis"
site:erich-friedman.github.io/packing/squinsqu "Joe DeVincentis" "54"
site:combinatorics.org/files/Surveys/ds7 "packing of 54 squares" Cantrell
site:kingbird.myphotos.cc/packing/square-54.svg
site:arxiv.org OR site:doi.org "7.84666719284348"
"Exact closed-form solution by David Ellsworth" "square-54"
"2*s-8-4*Sec[a]" square packing
"7.84666719284348" DeVincentis Ellsworth
site:github.com "square-54.svg" "DeVincentis"
```

No separate paper, preprint, DOI record, or author note deriving the current 54 poses
appeared. This is a bounded search result, not proof that none exists. The source trail
still runs through the published 1998 family, later survey attributions to private
communications, and the current catalogue/SVG maintained by Ellsworth.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
