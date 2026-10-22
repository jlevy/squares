# Project PDF Credit Coverage, 21 October 2026

The four project papers’ title credits resolve to profiles.
The explainer’s generated atlas figure also prints construction, lower-bound, optimality
and formalization credits; these names belong in the profile audit alongside the
manuscript’s prose. Seventeen profiles were added from this review.
The bibliography and case records retain their original names and roles, with reviewed
identity joins in [`occurrences.yaml`](../occurrences.yaml).

## Inspected Editions and Scope

The inspected PDFs were the retained preview editions below.
Their title blocks and corresponding renderer `PaperFront` records were checked for
named humans. Text was extracted from all four PDFs to locate credits; the explainer’s
Figure 2 credit block on page 6 and footnote 4 on page 22 were also visually inspected.
These are inspection receipts for those editions, not a claim that a later PDF build or
every cited external PDF has been inspected.

| Project PDF | Inspected edition | Title credit profiles |
| --- | --- | --- |
| [Lower-bound explainer](https://jlevy.github.io/squares/papers/n11-lower-bounds-explainer.pdf) | v0.4.12 | Joshua Levy |
| [Threshold-bound review](https://jlevy.github.io/squares/papers/n11-threshold-bound-review.pdf) | Draft v0.1.1 | Marc Leonard Overbeck; Joshua Levy |
| [Optimality review](https://jlevy.github.io/squares/papers/n11-optimality-review.pdf) | Draft v0.1.8 | Manasseh Ahmed; Joshua Levy |
| [Packing methods survey](https://jlevy.github.io/squares/papers/square-packing-methods-survey.pdf) | v0.2.3 | Joshua Levy |

The explainer’s Acknowledgments names Walter Stromquist, whose profile already existed.
The source manuscript is
`packing/devtools/templates/n11-lower-bounds-explainer-article.md`, sections
Acknowledgments and footnote `trump`. The figure credit text comes from
`packing/atlas/known-best/credit-attributions.json` through
`packing/devtools/atlas_credit_attributions.py` and the atlas builder.
Construction credits additionally come from the case records and bibliography.
A template-only inspection misses these generated credits.

## Historical Names in the Explainer’s Footnote

The retained Stromquist Memo III scan was visually inspected on PDF pages 2, 3 and 13,
which have the same printed page numbers.
Page 2, Table 1, credits Gustafsson and Thulin for the eleven-square packing; page 3
prints both full names.
The explainer’s page 22, footnote 4, preserves their independent rediscovery separately
from Trump’s 1979 construction.

| Profile | Evidence and scope |
| --- | --- |
| [Mats Gustafsson](../people/mats-gustafsson.md) | Memo III page 3 names him with Magnus Thulin as a discoverer of the packing of side approximately 3.877. No account or further biography is asserted. |
| [Magnus Thulin](../people/magnus-thulin.md) | The same page 3 sentence names him with Mats Gustafsson. |
| [Martin Gardner](../people/martin-gardner.md) | Page 3 identifies Martin Gardner’s *Scientific American* columns; page 13, reference [d], cites *Mathematical Games* by M. Gardner for the relevant dates. This is cited-author credit. |

The primary file is
`packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture.pdf`,
publicly available as [Memo III](https://www.walterstromquist.com/papers/squares3.pdf).
No structured occurrence was invented for the narrative-only footnote.
The publication template needs explicit footnote links because the general prose linker
protects footnotes. The archive index has no separate Gardner bibliography key for these
columns; adding such a publication entry requires its own cataloguing work.

## Generated Proof and Formalization Credits

The explainer’s page 6, Figure 2, prints El Moumni, Vlasenko and Karakuş in proof or
lower-bound credit clauses, and EvolvingPrograms, Gurevitch, Julian-JJ and Lewis in its
formalization clause.
The following profiles preserve the evidenced name precision.

| Printed label | Profile | Primary identity evidence |
| --- | --- | --- |
| Karakuş | [Hakan Karakuş](../people/hakan-karakus.md) | The retained `karakus-2026-counterexample-nagamochi-scoring-lemma.pdf`, page 1, prints Hakan Karakuş. |
| El Moumni | [Said El Moumni](../people/s-el-moumni.md) | The retained volume `el-moumni-1999-optimal-packings-unit-squares.pdf`, PDF page 287, printed page 281, gives S. EL MOUMNI. PDF page 296, printed page 290, repeats the initial. Friedman’s published DS7 Introduction explicitly names Said El Moumni with reference [12] to this same 1999 article, supplying the full name. |
| Vlasenko | [Andrey Vlasenko](../people/andrey-vlasenko.md) | The public GitHub profile API for `chelokot`, checked 21 October 2026, returned name Andrey Vlasenko and type User; the retained source packet identifies `chelokot/square-packing-archive`. |
| Gurevitch | [Benjamin Gurevitch](../people/benjamin-gurevitch.md) | The retained formalization’s `ACKNOWLEDGEMENTS.md`, line 7, prints Benjamin Gurevitch and links `Benjamin-Gurevitch`. |
| Lewis | [Lewis](../people/ctjlewis.md) | The same acknowledgment, line 5, links `ctjlewis`. The retained announcement receipt gives that account’s display name Lewis; the public GitHub API corroborated it on 21 October 2026. No fuller name or surname is asserted. |
| Julian-JJ | [Julian-JJ](../people/julian-jj.md) | The same acknowledgment, line 8, names and links the collaborator `Julian-JJ`. The profile retains the handle and does not infer a real name. |
| EvolvingPrograms | Organization, no person profile | The figure source explicitly records `entity_kind: organization`; the public GitHub API returned type Organization on 21 October 2026. The acknowledgment names it separately from `ctjlewis`. |

The retained acknowledgment is
`packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/11SquaresFormalized/ACKNOWLEDGEMENTS.md`
at commit `cdc746ed907d258057c283aeb6d077cb2c27e349`. It credits infrastructure and
replay support to EvolvingPrograms and `ctjlewis`, T03 help to Benjamin Gurevitch, and
HPC execution work to Julian-JJ. These distinctions remain in the source.
Resolving a bibliography’s existing author label establishes identity; it does not
assign each person authorship of T-060 or claim that the formalization has a registered
result.

Eight reviewed manual spans address the figure JSON’s exact `name` fields under
`lower_bounds.contributors` and `optimality.contributors`, using record key `$` and JSON
Pointers. Their role is `credited-contributor`. A ninth span marks EvolvingPrograms as
`non-person`. These joins record the figure credit without promoting it to primary
result authorship.

## Generated Construction Credits

The same Figure 2 credit block prints the following names.
Their full names are given by the retained Kingbird catalogue,
`packing/resources/web/kingbird-squares-in-squares.md`, and the bibliography’s
`credited_names` map.

| Printed label | Profile | Catalogue locator |
| --- | --- | --- |
| Wainwright | [Robert Wainwright](../people/robert-wainwright.md) | Entry 19: first finder in late 1979. The different Wainright spelling in older sources is not added as an identity alias by this review. |
| Hämäläinen | [Pertti Hämäläinen](../people/pertti-hamalainen.md) | Entry 18: finder in 1980. |
| Stenlund | [Evert Stenlund](../people/evert-stenlund.md) | Entries 66 and 67: finder in early 1980. |
| Cantrell | [David W. Cantrell](../people/david-w-cantrell.md) | Entry 37: finder in September 2002. |
| Morandi | [Maurizio Morandi](../people/maurizio-morandi.md) | Entry 69: finder in June 2010. |
| Hajba | [Károly Hajba](../people/karoly-hajba.md) | Entry 83: finder in September 2024. |
| Chang | [Allen Chang](../people/allen-chang.md) | Entries 68 and 83: improvements in September 2026; entry 83 also credits the polynomial root solution. |
| DeVincentis | [Joe DeVincentis](../people/joe-devincentis.md) | Entry 70: finder in April 2014. |
| hmbelvedere | Identity and entity status pending | Entry 69 credits this label for a July 2026 improvement. The retained first-party release identifies its creator as the UnitSquare Project organization. That does not establish whether the separate catalogue label is a person. A GitHub user lookup returned 404, which establishes no identity. |
| PingYou Ltd | Organization, no person profile | Retained source credit is a company label; no human identity is inferred. |

All other personal labels printed in these three figure credit paragraphs already had
profiles. The `hmbelvedere` credit remains printed and unresolved.
No account link, real name or person profile is invented for it.

## Structured Join Changes and Verification

The reviewed batch resolves 37 existing construction spans, six existing bibliography
identity spans, and 16 prerequisite spans for the separately reviewed Maaz, Arslanov,
Mustafin, Shangitbayev and Stead profiles.
It appends the nine manual figure spans and three author spans for the existing
archive-index key `[Arslanov et al.]`. The latter joins identify the three authors of
the retained 2021 paper and do not register a new mathematical result.
All existing source text, span offsets and credit roles are preserved.

The `s-el-moumni` profile keeps its stable ID, displays Said El Moumni and retains S. El
Moumni as an alias. The full-name evidence is Friedman’s published DS7 Introduction and
its explicit reference [12] to the same 1999 article.
The three case spans naming Said El Moumni are resolved from that evidence.
The original initial-only paper byline is preserved in the archive.

The final stabilization pass adds [Trevor Green](../people/trevor-green.md) from
Friedman’s direct credit before Theorem 9, and [K. F. Roth](../people/kf-roth.md) and
[R. C. Vaughan](../people/rc-vaughan.md) from the visually inspected first page of their
1978 paper (PDF page 1, printed page 170). Their names retain the published initials.
The existing `f-gobel` ID gains the evidenced Frits Göbel real name and the full-name
and Goebel aliases from the catalogue and the bibliography’s explicit ASCII-spelling
note. The original `[Roth–Vaughan 1978]` archive-index key now has a bibliography entry
and two author joins; no new mathematical result is registered.

That pass resolves 27 Trevor Green case spans, nine Frits Göbel case spans, one Goebel
credit, four Roth/Vaughan prerequisite credits, three Said El Moumni case spans, and
nine spans for the separately reviewed Bui, Bašić, Slivková, Nakajima and Summins
profiles. Seventy-two PingYou Ltd spans receive the supported corporate `non-person`
disposition.
The BuddenPing operator handle remains unresolved; corporate credit does not
establish its human identity.

The frozen registry has 75 profiles.
The audit separately reports ten manual origins: the project-author constant and the
nine figure-source spans.
The reusable all-significance audit reports 1,440 resolved structured spans, 77
non-person structured spans and seven unresolved structured spans: three collective Levy
labels, the clause “register seed data from Levy”, BuddenPing and two hmbelvedere spans.
The ambiguity follow-up is `think-0v9j`; this review resolves its earlier Said El Moumni
question without claiming the remaining questions are resolved.
The broader missing-work and PDF inspection agenda remains tracked by `think-m7il`. The
recorded 146 pending external PDFs are a separate inspection scope from these
project-paper credit checks.

From `packing/`, using the task’s external scratch environment and frozen project
interpreter:

```bash
uv run --frozen --all-extras --group dev pytest -q \
  tests/test_contributors.py tests/test_contributor_occurrences.py \
  tests/test_profile_coverage.py
uv run --frozen --all-extras --group dev pytest -q tests/test_bound_citations.py
uv run --frozen python -m devtools.contributor_census --stale
uv run --frozen python -m devtools.profile_coverage --minimum-significance 4 --json
```

The occurrence loader validates every addressed scalar against the retained source.
The census stale check returned `[]` and the three-file test command passed 115 tests in
9.34 seconds. The bibliography citation suite passed 122 tests in 22.39 seconds.
The reusable profile coverage command reports remaining candidates and unregistered
authored sources without assigning identities or turning citations into results.
The broader external-PDF inspection inventory remains pending except for the explicitly
inspected pages above.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
