# Retained Known-Best Packing Sources

This directory records upstream provenance for the `n = 1..100` known-best witness
corpus. [`sources.json`](sources.json) distinguishes retained upstream assets from
metadata-only source records.

## Kingbird Retention Policy

No express license or permission covering redistribution of the Kingbird catalogue SVGs
was located during the 2026-08-26 review.
The repository therefore retains no raw Kingbird SVG in this source inventory.
It retains attributed source metadata, normalized numerical center and angle facts in
the Witness/v2 corpus, and deterministic house renderings derived from those facts.
The retained Witness/v2 coordinate fields are the deterministic regeneration input.

This is a conservative repository-retention policy, not a legal conclusion.
The source metadata is not itself a geometry or feasibility claim.
Each witness carries its own finite-precision feasibility receipt and explicitly
disclaims exactness and optimality.
Live adapter audits are ephemeral and must not write source geometry; retaining raw
Kingbird assets requires an applicable license or express permission.

The metadata attributes the SVG and high-precision updates to David Ellsworth and the
original catalogue compilation to Erich Friedman, following the
[Kingbird catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html).

## The Range `n = 101..324`

Decision of 2026-09-07, under
[the atlas expansion plan](../../../../docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md),
decision `D2`: the policy above applies unchanged to the 123 catalogue cases in
`n = 101..324` whose geometry the prospective audit located but did not retain.
Each is acquired once, ephemerally, by the atlas builder’s `--fetch` path; the SVG is
parsed to numerical centre-and-angle facts, and only those facts, the attribution, and
the source metadata are retained, with `raw_asset_retained: false`. The
source-availability map records the state as
`derived-facts-acquisition-approved-2026-09-07`; its 2026-08-26 audit remains the
provenance record for which source served which `n`. The
[survey of sources beyond 100](../../../../docs/project/research/research-2026-09-07-square-packing-sources-beyond-100.md)
found no source with express reuse terms that carries this range, so there is no
licensed alternative to prefer.
Express permission from the catalogue’s author would allow raw retention and is an owner
action, not a prerequisite here.

## Source Packets’ Derived Facts

From 2026-09-29 the best known packing at 50 counts comes from two repositories that
publish no licence: Francisco Couzo’s 49 packings for `n = 68…307` and Joost de Winter’s
packing of 211 squares.
Their packets take the derived-only form of the policy above.
Each source’s packet keeps the centres and angles as Witness/v2 facts under its own
`facts/` directory, with the upstream files pinned by digest in its
`acquisition/sources.json`, and retains no upstream byte:
[Couzo’s](../franciscouzo-square-packing-2026-09-27/README.md) and
[de Winter’s](../de-winter-square-packing-211-2026-09-16/README.md).
The atlas builder reads those facts wherever a case record’s reported upper bound names
the packet’s source key, and [`sources.json`](sources.json) lists each such case as
`packet-derived-facts` with `raw_asset_retained: false`. At those counts the retained
Kingbird facts, which described the superseded catalogue packing, are no longer the
atlas’s witness; Git keeps them.

### Retained Factual Data

Owner decision of 2026-10-09, taken for Francisco Couzo’s eight refinements of
[issue #451](https://github.com/jlevy/squares/issues/451): a packet that carries a
source’s packings may also retain that source’s factual data in full, even when the
source publishes no licence.
Factual data means the source’s numbers: complete certificates, coordinates and poses,
and the records that list, compare or check them, such as digest manifests, comparators
and verification output.
Each retained file is bound in the packet’s acquisition record to its upstream identity,
a Git blob and SHA-256 or a release asset’s digest, and its retained copy, however it is
stored, reproduces those bytes exactly.
Original prose and programs, other than a licence notice, are never copied into such a
packet: the source’s READMEs, papers, credits and code are at most pinned by digest, and
no author program is executed.
[Ryan Xu’s packet](../ry-xu-new-packings-2026-10-08/README.md) retains the text of the
source’s 25 certificates this way.

Retaining a file grants no licence and relicenses nothing, and, like the policy above,
it is not a legal conclusion.
Every packet records the source’s identity, its pinned revision, its licence status and
its attribution, whichever form it takes.
Retention is permitted, never required: derived-only custody remains allowed, and a
packet may prefer it, as Couzo’s and de Winter’s packets above do.
The catalogue’s SVG pictures stay under the Kingbird rule.

## Facts Read From a Pinned Parse

At $n = 69, 83$ and $87$ the catalogue’s packings of September 2026 (T-088, T-089) were
taken in on 2026-10-05 from a session that could not fetch the SVGs.
Their centre-and-angle facts are read instead from Evan Daniel’s parse of the same
pictures, `site/www/data/p/square-<n>.json` in `evand/square-packing` at
`7ff3b2113532889708a3baa4d56bc44294022e63`: his own SVG reader’s output, exported in
binary64. Each witness names that file in `source.revision`, its limitations say the
numbers are a third party’s parse and not the SVG, and [`sources.json`](sources.json)
carries the same `revision`. No byte of the parse is retained either; the policy above
applies to it unchanged.
`devtools.derive_kingbird_facts --compare-parse` holds the parse to this repository’s
own reading: at the 90 counts whose witnesses were read from their own pictures, every
side agrees and every pose agrees to one binary64 ulp.
Re-deriving the three from the SVGs, once they can be fetched, replaces the parse.

### The Pictures Read Again, 5 October

The egress policy was widened on 2026-10-05, and at 23:13Z
`devtools.derive_kingbird_facts --range 1 324 --compare-pictures` fetched the picture
behind each of the 98 retained Kingbird witnesses into memory, read it with this
repository’s own SVG adapter, and compared it with the witness, square for square.
No SVG was written; the receipt keeps each picture’s size, SHA-256 and `Last-Modified`,
and the attribution paragraph of its comment
([`kingbird-2026-10-05-pictures.json`](receipts/kingbird-2026-10-05-pictures.json)).

- **95 witnesses are their pictures exactly:** the side and every centre and angle are
  the same decimal text. They include $n = 71$, whose picture the server dates
  2026-09-10, after its witness was read on 2026-08-26; the change left the geometry as
  it was.
- **The three read from the parse agree with their pictures at binary64.** At $n = 69$
  and $87$ every coordinate of the parse is the picture’s rounded to binary64. At
  $n = 83$ one angle differs, by $1.5 \times 10^{-33}$ of a unit in the last place:
  the picture gives square 82’s angle as 0 and the parse as $3.4 \times 10^{-49}$
  degrees. So the witnesses of T-088 and T-089, and the certificates promoted from them,
  are of the packings the catalogue pictures.
- **None of the 98 pictures is newer than the page.** The newest, `square-83.svg`, is dated
  2026-09-24T16:37:57Z; the page was captured again at 22:39Z with the same bytes as on
  2026-09-30.

The parse stays the witnesses’ source for now. The pictures give each pose to at least
50 digits, so re-deriving the three from them and certifying that pose with a finer
dilation is the route T-088’s and T-089’s `next_rung` names to a verified bound within
one unit of the printed side. It changes the certificates, the receipts and both
entries, and is left to its own bead, `think-krbs`.

### Certified Here

On 2026-10-05 the three witnesses were certified exactly by
[`devtools.catalogue_upper_bounds`](../../../devtools/catalogue_upper_bounds.py), with
the robust rational promotion `devtools.upper_bound_packets` runs for T-056 and T-057,
unchanged.
Each pose is rounded to rationals of 36 digits and dilated about the centre by
the first factor that makes every pair and wall pass the promotion’s exact
separating-axis test.
Each certificate is then decided again by `devtools.check_rational_witness_independent`,
which shares no geometry or verification code with the promotion, only Python’s
integers and `Fraction` and the YAML layer.
The certificates are in [`witnesses/kingbird-2026/`](../../../witnesses/kingbird-2026/)
and the receipts in [`receipts/`](receipts/):
[`kingbird-2026-09-certification.json`](receipts/kingbird-2026-09-certification.json),
and two mutations of the $n = 69$ certificate, its side cut by $10^{-15}$ and square 1
moved by $10^{-6}$, which both checkers refuse
([`kingbird-2026-09-negative-controls.json`](receipts/kingbird-2026-09-negative-controls.json)).

| n | Side printed | Dilation | Certified side | Above the printed side | Verified value |
| --- | --- | --- | --- | --- | --- |
| 69 | `8.82719465572973` | $1 + 10^{-15}$ | `8.82719465572974782719…` | $1.78 \times 10^{-14}$ | `8.82719465572975` |
| 83 | `9.63475764863108` | $1 + 10^{-13}$ | `9.63475764863194547576…` | $8.65 \times 10^{-13}$ | `9.63475764863195` |
| 87 | `9.83881526994826` | $1 + 10^{-13}$ | `9.83881526994914488152…` | $8.85 \times 10^{-13}$ | `9.83881526994915` |

Each certificate proves $s(n)$ at most its own side, which lies above the printed side
at all three counts, for two reasons.
The catalogue prints each side cut short, so the side the picture gives is already above
it, by $8.9 \times 10^{-15}$, about $2.0 \times 10^{-15}$ and $2.3 \times 10^{-15}$:
at $n = 69$ and $87$ the root of the printed polynomial, and at $n = 83$ the parse’s
side, since the degree-672 polynomial is not retained.
And a binary64 pose of a packing whose squares touch overlaps by rounding, so the promotion
has to dilate it: at $n = 69$ by $1 + 10^{-15}$, which adds $8.9 \times 10^{-15}$ to the
side, and at $n = 83$ and $87$, where $1 + 10^{-15}$ left one and thirteen pairs
overlapping, by $1 + 10^{-13}$, which adds about $8.7 \times 10^{-13}$. The verified
value is the certified side rounded up at the printed precision, the rule T-056 uses,
and at none of the three counts is it the printed side.
The SVG’s own 30-digit pose, or a pose refined on its active contacts, would close most
of the gap. So would a finer dilation ladder at $n = 83$ and $87$: the promotion’s steps
are a factor of 100 apart, and at $1 + 2 \times 10^{-15}$ both pass, 2 units above the
printed sides
([review of 2026-10-05](../../../../docs/project/reviews/review-2026-10-05-kingbird-intake-n69-n83-n87.md),
KB-3).

These verified values held the three counts’ ceilings until 2026-10-06, when Evan Daniel’s
exact certificates of the same packings, refined on their active contacts, took them to
`8.82719465572974`, `9.63475764863109` and `9.83881526994827`, one unit of the printed last
place above each printed side (T-101; the
[exact-optima packet](../evand-square-packing-2026-10-05/README.md#the-77-ceiling-counts)).

## Retained UnitSquare Renderings

The `unitsquare/` files are retained public evidence renderings for the `n = 68` and
`n = 69` records, which drew on them until Couzo’s packing took `n = 68` on 2026-09-29
and the catalogue’s took `n = 69` on 2026-10-05; no case draws on them now, and the
screen’s exclusion control is built from the `n = 69` rendering.
Those renderings identify governed source receipts in metadata but expose only rounded
polygon coordinates, so the normalized witnesses preserve that limitation.
Their retained bytes are checked against the SVG digests independently declared in the
UnitSquare Release 1 `results.json`; the source inventory names those values
`upstream_declared_sha256`. Git and deterministic full-content replay remain the
integrity boundary for co-committed outputs.
Do not reformat these archival source bytes or replace them with the repository’s house
renderings.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
