---
title: Credit-Line Review of the Generated Atlas Records 101–324
description: A correctness-only audit of the six credit-line fields (found_by, found_year, improved_by, construction_method, analytically_optimized, source_date) in the 107 catalogue-sourced records the generator wrote for n = 101..324, each compared by hand against the Kingbird catalogue's own credit line and against the convention the hand-written records at n ≤ 100 set; the machine reparse checked the printed sides and forms, this pass checked what it did not.
author: Claude Code
---
# Review: Credit-Line Review of the Generated Atlas Records 101–324

**Date:** 2026-09-07

**Author:** Claude Code

**Status:** Complete

## Overview

Commits `32b796cc` and `6e21c4ca` generated the 224 case records
`packing/frontier/n-101.md` … `n-324.md` from the retained Kingbird catalogue through
`packing/devtools/generate_frontier_case.py` and the parser
`packing/src/sqpack/kingbird_catalogue.py`. `devtools.check_source_coverage` reparses
the catalogue and reports zero divergences for `exact_form`, `algebraic_degree`,
`minimal_polynomial` and `catalogue_rigid` over every pictured case, and I reran it to
the same result.
What that check does not read is the credit line under each picture, and
the six fields the generator fills from it: `found_by`, `found_year`, `improved_by`,
`construction_method`, `analytically_optimized` and `source_date`. This review reads all
of them, for every catalogue-sourced record in the range.

The population is the 107 records in `101..324` whose `reported_upper_bound.source_key`
is `[Kingbird]` and whose `catalogue_pictured` is `true`. The four `[UnitSquare 2026]`
cases (`103, 105, 110, 131`) and the 113 grid records are out of scope; one grid
observation that is really a credit-line observation is kept to its own section at the
end.

**Verdict.** No record carries a wrong finder or a wrong year: every non-empty
`found_by` is the page’s first “Found by” sentence and every `found_year` is that
sentence’s year, never the year of a later improvement.
Every `reported_upper_bound.value` equals the printed decimal, and every number the body
prose restates matches the front matter.
The defects are of omission and of one rendered sentence.
`improved_by` is empty on all 33 in-range cases whose page carries a dated “Improved by”
sentence, though the hand-written records at `n ≤ 100` transcribed that sentence five
times out of five.
Eight finders the page names are missing because the parser reads only
three sentence openers.
Two `construction_method` values are wrong (`n = 171, 198`), because the
`simulated annealing` substring matched inside a parenthesised description of a parent
packing. And the body sentence “Found by ⟨finder⟩ in ⟨year⟩, via simulated annealing”
joins the first finder to the last method, which at the seven Arslanov cases credits a
2019 analytic construction to a 2026 annealing run.
That sentence is a template inherited from the hand-written `n = 53` and `n = 87`, so
the fix is one generator change, not ten edits.

## Counts per class

| Class | Meaning | Cases |
| --- | --- | --- |
| (a) | the record agrees with the page and the `n ≤ 100` convention | 39 |
| (b) | the record is null or `unknown` where the page states something a reader would transcribe | 39 |
| (c) | the record states something the page does not support | 2 |
| (d) | the page is ambiguous, or the corpus has no single convention | 27 |
|  |  | 107 |

Each case is counted once, at the most serious class it reaches (`c > b > d > a`). Two
findings cut across the classes and are counted separately: the body-prose sentence
above, which affects ten cases whose front matter is otherwise conventional
(`126, 132, 156, 182, 207, 210, 241, 273, 297, 307`), and the seven Arslanov cases’
missing `resources` entry, which is folded into their (b) rows.

The 39 cases in class (a): `104, 109, 124, 125, 127, 147, 148, 149, 150, 155, 174, 176,
178, 180, 181, 201, 202, 204, 208, 209, 231, 232, 233, 238, 239, 262, 264, 265, 267,
270, 271, 294, 295, 296, 299, 303, 304, 305, 306`. These are the Göbel-strips and
Göbel-squares family members, the “Extends the s(m)” entries that name only the family’s
originator, and the thirteen January-to-May 2026 annealing runs Ellsworth started from a
larger packing. Where those pages name nobody for the packing itself (“Extends the s(52)
found by Frits Göbel in early 1979”), a null `found_by` is the right transcription; the
`n ≤ 100` precedents `67, 84, 89` named the extender because the page named him.

## What the hand-written records did

The convention was measured, not assumed.
For the 46 catalogue-sourced pictured records at `n ≤ 100`, I placed each record’s six
fields beside the catalogue’s credit line.

- `found_by` and `found_year` are the first sentence beginning “Found by”, “Found first
  by” or “Proved by”, and its year.
  `n = 37` (“Found by David W. Cantrell in September 2002. Improves upon the s(37) found
  by Evert Stenlund”) credits Cantrell; `n = 53`, found in 2002 and last improved in
  2026, keeps `found_year: 2002`.
- A dated, sentence-initial “Improved by ⟨names⟩ in ⟨month⟩ ⟨year⟩” is recorded in
  `improved_by` in all five cases that carry one (`53, 54, 55, 83, 87`), and the
  improver is kept even when he is also the finder (`87`). “Improved independently by
  both …” at `n = 88` was not recorded.
  “Optimized by” is inconsistent: recorded at `29`, not at `39, 41, 50, 51, 71`. A rule
  for the dated “Improved by” form reproduces 45 of the 46 records; the one miss is
  `n = 29`, where the hand pass read an “Optimized by” sentence as an improvement.
- `construction_method` is the method that produced the printed side: `53` and `87`,
  both found by hand and last improved by annealing, are `simulated-annealing`. A named
  human with no program mentioned was written `hand-construction` 22 times; the
  generator declines that inference on purpose (its docstring cites `n = 68`), which is
  why 24 in-range records are `unknown` where the hand pass would have written
  `hand-construction`. Those are class (d) below, not (b).
- `analytically_optimized` is `true` on all 46; the page’s “Not yet analytically
  optimized” disclaimer appears nowhere below `n = 100`.
- `source_date` is null on all 46. It is null on all 107 in range, which agrees.

## Class (c): the record states what the page does not support

| n | Page phrase | Record | Proposed disposition |
| --- | --- | --- | --- |
| 171 | “by combining two copies of the s(50) found by Thomas Schadt … (using a simulated annealing program …)” | `construction_method: simulated-annealing`; body “via simulated annealing” | Hand edit to `composition`. The annealing belongs to the parent `s(50)`; the page says the `s(171)` was made by combining two copies of it. |
| 198 | “Adds an ‘L’ to the s(171) found by David Ellsworth … (using a simulated annealing program …)” | `construction_method: simulated-annealing`; body “via simulated annealing” | Hand edit, with the L-family decision in class (d); the annealing is two parents up. Generator: the `simulated annealing` rule must not match inside a parenthesised parent description. |

Both are the same mechanism: the substring rule reads the whole credit line, and at
these two entries the only mention of annealing is inside a parenthesis describing how
an ancestor was found.
The other 30 `simulated-annealing` records in range are right: either the finder’s own
sentence names the program (13 cases: `155, 180, 181, 208, 209, 238, 239, 270, 271,
303–306`), or a dated improvement sentence (“Improved by”, “Refined by”, “Improved
independently by”) names it as what produced the printed side (17 cases: `126, 129, 132,
154, 156, 179, 182, 206, 207, 210, 240, 241, 272, 273, 297, 301, 307`), which is the
`n = 53` and `n = 87` convention.

## Class (b): the record is null or `unknown` where the page states something

Three mechanisms produce every row.
**`improved_by`** (33 cases): the page carries a dated, sentence-initial “Improved by
⟨names⟩ in ⟨month⟩ ⟨year⟩” and the record has `[]`; the proposed disposition is one
generator rule, and the value it would write is given in the row.
**`found_by`** (8 cases): the page names the finder with an opener the parser does not
read — “Found and improved by”, “Originally found by”, “Drafted by”.
**`resources`** (7 cases): the Arslanov records cite no paper for the finder, where the
`n ≤ 100` records cite the retained paper behind a credit (`[Bentz 2010]` at `13, 46`,
`[Stromquist 2003]` at `10, 11, 12`, `[Kearney–Shiu 2002]` at `6`,
`[Gensane–Ryckelynck 2005]` at `11`); the key `[Arslanov et al.]` already exists in
`packing/resources/README.md` for `papers/arslanov-improved-packings-n-n-1`.

| n | Page phrase | Record | Proposed disposition |
| --- | --- | --- | --- |
| 102 | “Improved by David W. Cantrell and David Ellsworth in November 2024” | `improved_by: []` | Rule → `[David W. Cantrell, David Ellsworth]` |
| 106 | “Improved by David W. Cantrell in December 2024” | `improved_by: []` | Rule → `[David W. Cantrell]` |
| 108 | “Improved by David Ellsworth in November 2024” | `improved_by: []` | Rule → `[David Ellsworth]` |
| 123 | “Found and improved by David Ellsworth in December 2024”; “Improved by David W. Cantrell in January 2025” | `found_by: []`, `found_year: null`; `improved_by: []` | Hand edit `found_by: [David Ellsworth]`, `found_year: 2024`; rule → `[David W. Cantrell]` |
| 126 | “Improved by David W. Cantrell in December 2024”; “Improved by Thomas Schadt in December 2025” | `improved_by: []` | Rule → `[David W. Cantrell, Thomas Schadt]` |
| 128 | “Improved by David Ellsworth in December 2024”; “Improved by David W. Cantrell and David Ellsworth in January 2025” | `improved_by: []` | Rule → `[David Ellsworth, David W. Cantrell]` |
| 129 | “Found and improved by David Ellsworth in December 2024”; “Improved by David Ellsworth in December 2025” | `found_by: []`, `found_year: null`; `improved_by: []` | Hand edit `found_by: [David Ellsworth]`, `found_year: 2024`; rule → `[David Ellsworth]` |
| 130 | “Improved by David W. Cantrell in November 2024”; “Improved by David Ellsworth in November 2024” | `improved_by: []` | Rule → `[David W. Cantrell, David Ellsworth]` |
| 132 | “Improved by David W. Cantrell in March 2025”; “Improved by David Ellsworth in January 2026” | `improved_by: []`; no `[Arslanov et al.]` resource | Rule → `[David W. Cantrell, David Ellsworth]`; hand edit adds the resource |
| 151 | “Improved by David W. Cantrell in December 2024” | `improved_by: []` | Rule → `[David W. Cantrell]` |
| 154 | “Originally found by David Ellsworth in December 2024”; “Improved by David W. Cantrell in February 2025” | `found_by: []`, `found_year: null`; `improved_by: []` | Hand edit `found_by: [David Ellsworth]`, `found_year: 2024`; rule → `[David W. Cantrell]` (“Improved independently by” is not recorded, as at `n = 88`) |
| 156 | “Improved by David Ellsworth in December 2024”; “Improved by David W. Cantrell in March 2025” | `improved_by: []`; no `[Arslanov et al.]` resource | Rule → `[David Ellsworth, David W. Cantrell]`; hand edit adds the resource |
| 172 | “Improved by David Ellsworth in November 2024” | `improved_by: []` | Rule → `[David Ellsworth]` |
| 177 | “Found and improved by David Ellsworth in November 2024 and December 2024” | `found_by: []`, `found_year: null` | Hand edit `found_by: [David Ellsworth]`, `found_year: 2024` |
| 179 | “Improved by David Ellsworth in January 2026” | `improved_by: []` | Rule → `[David Ellsworth]` |
| 182 | “Improved by David Ellsworth in December 2024” | `improved_by: []`; no `[Arslanov et al.]` resource | Rule → `[David Ellsworth]`; hand edit adds the resource |
| 205 | “Improved by David Ellsworth in January 2025” | `improved_by: []` | Rule → `[David Ellsworth]` |
| 206 | “Found and improved by David Ellsworth in December 2024”; “Improved by David Ellsworth in December 2025” | `found_by: []`, `found_year: null`; `improved_by: []` | Hand edit `found_by: [David Ellsworth]`, `found_year: 2024`; rule → `[David Ellsworth]` |
| 207 | “Improved by David Ellsworth in January 2026” | `improved_by: []` | Rule → `[David Ellsworth]` |
| 210 | “Improved by David Ellsworth in December 2024” | `improved_by: []`; no `[Arslanov et al.]` resource | Rule → `[David Ellsworth]`; hand edit adds the resource |
| 228 | “Improved by David Ellsworth in December 2024” | `improved_by: []` | Rule → `[David Ellsworth]` |
| 230 | “Found and improved by David Ellsworth in January 2025” | `found_by: []`, `found_year: null` | Hand edit `found_by: [David Ellsworth]`, `found_year: 2025` |
| 234 | “Improved by David Ellsworth in January 2025” | `improved_by: []` | Rule → `[David Ellsworth]` |
| 236 | “Improved by David Ellsworth in December 2024” | `improved_by: []` | Rule → `[David Ellsworth]` |
| 240 | “Improved by David Ellsworth in January 2026”; “Originally found by Károly Hajba in September 2015” | `improved_by: []`; `found_by: []` | Rule → `[David Ellsworth]`; `found_by` is a hand decision, see class (d) |
| 241 | “Improved by David Ellsworth in November 2024” | `improved_by: []`; no `[Arslanov et al.]` resource | Rule → `[David Ellsworth]`; hand edit adds the resource |
| 259 | “Improved by David Ellsworth in December 2024” | `improved_by: []` | Rule → `[David Ellsworth]` |
| 266 | “Found and improved by David Ellsworth in November 2024 and in December 2024” | `found_by: []`, `found_year: null` | Hand edit `found_by: [David Ellsworth]`, `found_year: 2024` |
| 268 | “Improved by David W. Cantrell in February 2025” | `improved_by: []` | Rule → `[David W. Cantrell]` |
| 269 | “Improved by David Ellsworth in January 2025” | `improved_by: []` | Rule → `[David Ellsworth]` |
| 272 | “Improved by David Ellsworth in January 2026”; “Originally found by Lars Cleemann between 1991 and 1998” | `improved_by: []`; `found_by: []` | Rule → `[David Ellsworth]`; `found_by` is a hand decision, see class (d) |
| 273 | “Improved by David Ellsworth in November 2024” | `improved_by: []`; no `[Arslanov et al.]` resource | Rule → `[David Ellsworth]`; hand edit adds the resource |
| 290 | “Combines two copies of the s(65)” | `construction_method: unknown` | Hand edit to `composition`; the enum value exists and nothing in the corpus uses it |
| 291 | “Combines two copies of the s(65)” | `construction_method: unknown` | Hand edit to `composition` |
| 293 | “Improved by David W. Cantrell in January 2025” | `improved_by: []` | Rule → `[David W. Cantrell]` |
| 297 | “Improved by David Ellsworth in January 2026” | `improved_by: []` | Rule → `[David Ellsworth]` |
| 300 | “Improved by David Ellsworth in January 2025” | `improved_by: []` | Rule → `[David Ellsworth]` |
| 301 | “Drafted by David Ellsworth in January 2025” | `found_by: []`, `found_year: null` | Hand edit `found_by: [David Ellsworth]`, `found_year: 2025` |
| 307 | “Improved by David Ellsworth and Károly Hajba in December 2024” | `improved_by: []`; no `[Arslanov et al.]` resource | Rule → `[David Ellsworth, Károly Hajba]`; hand edit adds the resource |

Where a page carries several dated “Improved by” sentences, the row quotes the first one
or two; the rule value lists every improver in page order, each once.

## Class (d): the page is ambiguous, or the corpus has no single convention

Four groups. **The L-augmentation family** (13 cases:
`101, 122, 145, 173, 197, 199, 200, 226, 229,
258, 261, 292, 298`, and `198` from class (c)): “Adds ⟨k⟩ ‘L’s to the s(m)”. The corpus
has one precedent, `n = 82` (“Adds two ‘L’s to s(65)”), transcribed `hand-construction`;
but the catalogue itself calls the same construction an extension at `170` and `257`
(“Extends the s(65) … augmented by five/eight ‘L’s”), and those two records are
`extension`. So the register now files `s(65)` plus two, three, four, six or seven L’s
as `unknown` and `s(65)` plus five or eight L’s as `extension`. One family-wide decision
is needed, not fourteen.
**Named human, no program** (10 cases: `107, 146, 152, 153, 175, 203, 235, 237, 263,
302`): the hand pass would have written `hand-construction`; the generator’s refusal to
infer it is documented and defensible; leave `unknown` unless corpus consistency is
wanted, in which case it is a hand pass, not a rule.
**The pictured alternative** (`170, 257, 260`): “This alternative … found by ⟨name⟩ in
⟨date⟩”, and the pictured file is the alternative (`square-170b.svg`, `square-257a.svg`,
`square-260b.svg`). At `n = 18` the hand record credited the original finder rather than
the pictured alternative’s, but here the original extension names nobody.
**Two lineages** (`240, 272`): “Originally found by” one person, the pictured packing
converted from Arslanov’s `s(210)` and improved by annealing.

| n | Page phrase | Record | Proposed disposition |
| --- | --- | --- | --- |
| 101 | “Adds two ‘L’s to the s(65)” | `construction_method: unknown` | L-family decision |
| 107 | “Found by Károly Hajba in November 2024” | `construction_method: unknown` | Leave `unknown` |
| 122 | “Adds three ‘L’s to the s(65)” | `construction_method: unknown` | L-family decision |
| 145 | “Adds four ‘L’s to the s(65)” | `construction_method: unknown` | L-family decision |
| 146 | “by switching to the rotationally symmetric form of adding an ‘L’” | `construction_method: unknown` | Leave `unknown`; an L-augmentation with a twist |
| 152 | “Found by David Ellsworth and David W. Cantrell in January 2025, based on the s(53)” | `construction_method: unknown` | Leave `unknown` |
| 153 | “Found by David Ellsworth in November 2024, based on the s(70)” | `construction_method: unknown` | Leave `unknown` |
| 170 | “This alternative … found by Károly Hajba in November 2024” | `found_by: []` | Hand decision; `square-170b.svg` is the alternative |
| 173 | “Adds an ‘L’ to the s(148)” | `construction_method: unknown` | L-family decision |
| 175 | “Found by David Ellsworth in December 2024. Based on the s(233)” | `construction_method: unknown` | Leave `unknown` |
| 197 | “Adds six ‘L’s to the s(65)” | `construction_method: unknown` | L-family decision |
| 199 | “Adds an ‘L’ to the s(172)” | `construction_method: unknown` | L-family decision |
| 200 | “Adds two ‘L’s to the s(148)” | `construction_method: unknown` | L-family decision |
| 203 | “Found by David Ellsworth in December 2024. Based on the s(233)” | `construction_method: unknown` | Leave `unknown` |
| 226 | “Adds seven ‘L’s to the s(65)” | `construction_method: unknown` | L-family decision |
| 227 | “using a computer program he wrote. Continues the s(26), s(85) series” | `construction_method: unknown` | Leave `unknown`; `pattern-family` is a possible reading and is unused corpus-wide |
| 229 | “Adds three ‘L’s to the s(148)” | `construction_method: unknown` | L-family decision |
| 235 | “Found by David Ellsworth and David W. Cantrell in January 2025, based on the s(53)” | `construction_method: unknown` | Leave `unknown` |
| 237 | “Found by David Ellsworth in December 2024. Similar to the s(70)” | `construction_method: unknown` | Leave `unknown` |
| 240 | “Originally found by Károly Hajba in September 2015 … Converted in December 2024 from the s(210)” | `found_by: []`, `found_year: null` | Hand decision: credit the original finder as `n = 53` does, or leave null for the second lineage |
| 257 | “This alternative … found by David Ellsworth in January 2025, using a computer program he wrote” | `found_by: []` | Hand decision; `square-257a.svg` is the alternative |
| 258 | “Adds an ‘L’ to the s(227)” | `construction_method: unknown` | L-family decision |
| 260 | “This alternative … found by David Ellsworth in December 2024” | `found_by: []` | Hand decision; `square-260b.svg` is the alternative |
| 261 | “Adds an ‘L’ to the s(230)” | `construction_method: unknown` | L-family decision |
| 263 | “Found by David Ellsworth in January 2025, based on the s(297) he found” | `construction_method: unknown` | Leave `unknown` |
| 272 | “Originally found by Lars Cleemann between 1991 and 1998 … Converted in December 2024 from the s(210)” | `found_by: []`, `found_year: null` | Hand decision on `found_by`; the year is a range and stays null |
| 292 | “Adds an ‘L’ to the s(259)” | `construction_method: unknown` | L-family decision |
| 298 | “Adds an ‘L’ to the s(265)” | `construction_method: unknown` | L-family decision |
| 302 | “Found by David Ellsworth in December 2024 … by extending the s(88)” | `construction_method: unknown` | Leave `unknown`; “extending” inside the finder’s sentence is not the “Extends the” opener the rule reads |

One more (d) observation that produces no row: nine pages end “Further improvement
pending.” (`102, 130, 172, 199, 228, 259, 269, 292, 302`) and the records carry
`analytically_optimized: true`, because the rule writes `true` wherever the disclaimer
is absent. That is what `n = 88` (“Improvement by Thomas Schadt pending”) did at
`n ≤ 100`, so it is convention, but `true` is a positive claim read from silence; the
schema allows `null`, and the coordinator may prefer it for these nine.

## The body sentence that joins the first finder to the last method

`render_record` writes one sentence under “The packing”: “Found by ⟨found_by⟩ in
⟨found_year⟩, via ⟨construction_method⟩.” The two fields follow different conventions
(first finder; method that produced the printed side), and joined they assert something
the page does not say.

| n | What the page says | What the body says |
| --- | --- | --- |
| 126 | Found by Ellsworth, December 2024, from Cantrell’s `s(39)`; improved by Schadt in December 2025 by annealing | “Found by David Ellsworth in 2024, via simulated annealing.” |
| 132, 156, 182, 210, 241, 273, 307 | Found by Arslanov, Mustafin and Shangitbayev in March 2019; improved by Ellsworth in January 2026 by annealing | “Found by M.Z. Arslanov, S.A. Mustafin and Z.K. Shangitbayev in 2019, via simulated annealing.” |
| 207 | Found by Ellsworth, November 2024, by extending Friedman’s `s(88)`; improved 2026 by annealing | “Found by David Ellsworth in 2024, via simulated annealing.” |
| 297 | Found by Ellsworth, January 2025, extending Friedman’s `s(85)`; improved 2026 by annealing | “Found by David Ellsworth in 2025, via simulated annealing.” |

The Arslanov rows are the ones a reader would notice: the 2021 paper’s packings are
explicit “squeezing” constructions with tabulated coordinates (its Table 2), and nothing
in it anneals. The same sentence stands in the hand-written `n-053.md` (“Found by David
W. Cantrell in 2002, via simulated annealing.”) and `n-087.md`, which is where the
template came from, so this is not a generator regression; it is a template defect that
the generator has now multiplied by ten.
The disposition is a generator change: render the finder and the method as separate
statements (“Found by … in …”; “The printed side is from simulated annealing”, or the
`improved_by` sentence carrying the method), and regenerate the seven golden records so
the test follows.

A smaller wording point in the same section: ten records say “Found by an unrecorded
author” where the page does record one (`123, 129, 154, 177, 206, 230, 240, 266, 272,
301`). The author is unrecorded by the record, not by the source; “not carried by this
record” would be accurate until the (b) edits land.

## The Arslanov cases

The seven cases `132, 156, 182, 210, 241, 273, 307` were checked against the retained
paper, `packing/resources/papers/arslanov-improved-packings-n-n-1.md` (M. Z. Arslanov,
S. A. Mustafin, Z. K. Shangitbayev, *Improved packings of n(n−1) unit squares in a
square*, Electron. J. Combin.
28(4) P4.22; submitted 14 March 2019, published 5 November 2021).

- **`found_year: 2019`** agrees with the page (“in March 2019”) and with the paper’s
  submission date. The paper was published in 2021, and a `resources` entry for it would
  carry `year: 2021`; the record’s field means the year the packing was found, so `2019`
  is the right value and the two years are not a conflict.
- **`construction_method: simulated-annealing`** is the `n = 53` convention (the method
  that produced the printed side, here Ellsworth’s January 2026 improvement) and not the
  paper’s method. The front matter is defensible; the rendered sentence is not, as the
  previous section says.
- **`resources`** on all seven lists only `[Kingbird]`, `[Nagamochi 2005]` and
  `[Friedman DS7]`; none cites the paper, though the repository retains it and
  `packing/resources/README.md` already assigns it the key `[Arslanov et al.]`. The
  `n ≤ 100` records cite the retained paper behind a credit (`[Bentz 2010]` at `13, 46`,
  `[Stromquist 2003]` at `10, 11, 12`, `[Kearney–Shiu 2002]` at `6`,
  `[Gensane–Ryckelynck 2005]` at `11`), so this is a (b) omission and a hand edit; the
  generator’s resource block is fixed by design.
- **The plan’s Table 4 cross-check** (“Arslanov’s Table 4 values … are cross-checked
  against the catalogue; disagreement becomes a typed `conflict`”) has no
  implementation: nothing under `packing/devtools` or `packing/src/sqpack` mentions
  Arslanov or Table 4, and the coverage check’s “6 newer in-horizon reports” are the six
  UnitSquare overrides.
  I did the comparison by hand.
  Every catalogue value lies below the paper’s bound, by the margin the page’s
  improvement chain explains, so there is no conflict to type; but the rule in the plan
  is unmet as a check.

| n | Paper, Table 4 | Catalogue and record | Catalogue lower by |
| --- | --- | --- | --- |
| 132 | `< 11.99790201731` | `11.99143643966336` | `0.00646557764664` |
| 156 | `< 12.9940424` | `12.98219172354800` | `0.01185067645200` |
| 182 | `< 13.98318264114` | `13.97442960739443` | `0.00875303374557` |
| 210 | `< 14.98318264114` | `14.97421396826961` | `0.00896867287039` |
| 241 | `< 15.99595004` | `15.99091684780193` | `0.00503319219807` |
| 273 | `< 16.9950917682252` | `16.98832058897683` | `0.00677117924837` |
| 307 | `< 17.9950917682252` | `17.98281564631754` | `0.01227612190766` |

## “Not yet analytically optimized”

The brief said 23 entries; the catalogue in range carries the disclaimer on 32, and the
generator’s docstring says 32. Four of them are the UnitSquare cases
(`103, 105, 110, 131`), whose `analytically_optimized: false` comes from the release,
not the catalogue; the other 28 are catalogue-sourced
(`132, 154, 155, 156, 179, 180, 181, 182, 206, 207, 208, 209, 210,
238, 239, 240, 241, 270, 271, 272, 273, 297, 301, 303, 304, 305, 306, 307`), and every
one of the 28 records carries `false`. The other 79 catalogue-sourced records carry
`true`. No disagreement.

## Spot-checks of value and body

The brief asked for ten; the check is cheap, so it ran over all 107.
`reported_upper_bound.value` equals the catalogue’s printed decimal in every case.
In every open case the body’s gap (`reported_upper − verified_lower`, four places), its
“trails the reported construction by” value (`⌈√n⌉ − reported_upper`, exact), and its
algebraic degree match the front matter; no body contains “Later improved by” while
`improved_by` is empty.

The ten read in full, spread across the range, were `101, 126, 132, 150, 171, 179, 198,
240, 272, 307`. Apart from “The packing”, the body sections are template: the ceiling
paragraph, the Nagamochi paragraph, and at `179` the stale-form conflict, whose body
correctly restates the front matter’s `conflicts` entry and carries no form.
The one sentence that asserts more than the front matter carries is the joined
finder-plus-method sentence discussed above (`126, 132, 171, 198, 307` among the ten);
at `240` and `272` the body’s “unrecorded author” is the wording point noted there.

## Out of scope, but a credit-line fact: the sixteen pictured grids

The catalogue pictures `k² − 2` and `k² − 1` for `k = 11..18` (sixteen cases,
`119, 120, 142, 143, 167, 168, 194, 195, 223, 224, 254, 255, 287, 288, 322, 323`), each
with the credit “Proved by Hiroshi Nagamochi in 2005.” Their records carry
`catalogue_pictured: false`, `found_by: []`, `found_year: null` and
`construction_method: trivial-grid`. The generator does this deliberately and says so
(`build_payload`: recorded “exactly as it records `n = 47, 48, 62, 63, 79, 80, 98, 99`:
a trivial grid, credited to nobody, with `catalogue_pictured` false”). But the hand
corpus has two conventions for the same page shape: `n = 23` and `n = 34` (also “Proved
by Hiroshi Nagamochi in 2005”, also pictured) carry `catalogue_pictured:
true`, `found_by: [Hiroshi Nagamochi]`, `found_year: 2005`, `hand-construction`. The
generator followed the larger, later block.
Two things are worth a decision: `catalogue_pictured: false` is literally untrue for
these sixteen (the page pictures them, and the reparse matched them to a block), and the
prover’s credit is dropped.
The reparse does not compare `catalogue_pictured`, which is why it did not notice.

## What a generator rule can absorb, and what needs a hand

Safe to absorb, each measured against the `n ≤ 100` hand records:

- **`improved_by` from a dated, sentence-initial “Improved by ⟨names⟩ in ⟨month⟩
  ⟨year⟩”**, names split on “and” and commas, each kept once in page order.
  Reproduces 45 of 46 hand records; the miss is `n = 29`, where the hand pass counted an
  “Optimized by” sentence, which the rule deliberately does not read (the docstring’s
  own `29`-versus-`50` evidence).
  Writes 33 in-range records.
- **Three more `found_by` openers** in the parser’s `_CREDIT` regex: “Found and improved
  by”, “Originally found by”, “Drafted by”.
  Each is unambiguous on the page and reaches `123, 129, 154, 177, 206, 230, 266, 301`
  and, with a hand decision on lineage, `240, 272`. The generator’s `_CREDIT_ROLES`
  already knows “Refined by”, “Refound by”, “Improved by” and “Optimized by” for naming
  UnitSquare parents; the parser and the generator should read the same list.
- **Scoping the `simulated annealing` rule** to text outside parentheses, or to the
  sentence whose subject is the printed packing.
  Fixes `171` and `198`; changes nothing else in range, since the other 30 matches are
  in the finder’s or a dated improver’s own sentence.
- **Splitting the body sentence** so that the finder and the method are not one clause.
  Fixes ten in-range bodies and, on regeneration, the two hand-written precedents.

Needs a hand, because the page or the corpus does not settle it:

- The **L-augmentation family** (`hand-construction` per `n = 82`, or `extension` per
  the page’s own verb at `170, 257, 260`): one decision for fourteen records.
- **`composition`** at `171, 290, 291`: three records, and a rule for “Combines two
  copies” would reach exactly those, so it is a hand edit either way.
- **The Arslanov `resources` entry** on seven records.
- **`found_by` at `170, 257, 260` (pictured alternative) and `240, 272` (two
  lineages).**
- **`analytically_optimized` on the nine “Further improvement pending” pages**, if
  `null` is preferred to the convention’s `true`.
- **The sixteen pictured grids**, if `n = 23`’s convention is preferred to `n = 47`’s.

## Commands run

All from `packing/`, with the project interpreter.
Scratch files went to the session scratchpad and nothing under `packing/frontier` was
written.

```bash
uv run --frozen --all-extras --group dev python -m devtools.check_source_coverage
uv run --frozen --all-extras --group dev python -m devtools.generate_frontier_case \
    --range 101 324 --out "$SCRATCH/w2-gen"
uv run --frozen --all-extras --group dev python "$SCRATCH/dump.py" 101 324 "$SCRATCH/dump-101-324.json"
uv run --frozen --all-extras --group dev python "$SCRATCH/dump.py"   1 100 "$SCRATCH/dump-001-100.json"
uv run --frozen --all-extras --group dev python "$SCRATCH/show.py" 101 180   # and 181 260, 261 324
uv run --frozen --all-extras --group dev python "$SCRATCH/classify.py"
grep -h -A3 "found_by" frontier/n-0{29,50,55,71,87}.md
grep -n -B2 -A14 "square-29\.svg\|square-50\.svg\|square-55\.svg" \
    resources/web/kingbird-squares-in-squares.md
grep -h "construction_method:" frontier/n-*.md | sort | uniq -c
grep -h "^  - key:" frontier/n-0*.md frontier/n-100.md | sort | uniq -c | sort -rn
grep -n -i "arslanov\|table 4" devtools/*.py src/sqpack/*.py
```

`dump.py` reads each record’s front matter with `yaml.safe_load` and places its
`reported_upper_bound` fields, `resources` keys, `conflicts` and “The packing” section
beside `sqpack.kingbird_catalogue.parse_catalogue()[n]` (`credit_line`, `found_by`,
`found_year`, `side_decimal`, `svg_path`). `classify.py` applies the dated “Improved by”
rule, compares every value to the printed decimal, recomputes the body’s gap, trail and
degree from the front matter, and emits the class of each case.
The generator run reported `construction_method unknown: 64` and listed them; the sixty
catalogue-sourced ones are the (b) and (d) `unknown` rows above plus the 24 named-human
cases and the family entries that are (a).

## Counts and the three findings that matter

Of the 107 catalogue-sourced records in `101..324`: **39 agree (a), 39 omit what the
page states (b), 2 state what the page does not support (c), 27 are ambiguous (d).**
Separately: 10 bodies join the first finder to the last method; 7 Arslanov records cite
no paper; 16 pictured grids are recorded as unpictured and uncredited.

1. **The body sentence “Found by ⟨finder⟩ in ⟨year⟩, via simulated annealing” is false
   at the seven Arslanov cases and three others** (`126, 207, 297`), because it joins a
   first-finder field to a last-method field.
   It is inherited from the hand-written `n = 53` and `n = 87`; one template change
   fixes twelve records.
2. **`improved_by` is empty on all 33 in-range cases with a dated “Improved by”
   sentence**, though the hand pass recorded that sentence five times out of five.
   A rule for exactly that form reproduces 45 of the 46 hand records and is safe to add.
3. **Two `construction_method` values are wrong (`171, 198`) and eight finders are
   missing (`123, 129, 154, 177, 206, 230, 266, 301`)**, for two mechanical reasons: the
   annealing substring matched a parenthesised parent, and the parser reads three
   sentence openers where the page uses six.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
