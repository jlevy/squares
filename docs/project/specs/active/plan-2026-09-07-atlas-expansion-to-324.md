# Plan: Extend the Known-Best Atlas to `n = 324`, and Draw the Poster

**Date:** 2026-09-07

**Author:** Joshua Levy, with Claude Fable 5.1 assistance

**Status:** Draft, owner-directed.
Epic `think-0juv` is created by this plan; the handoff in
[`SYNOPSIS.md`](../../../../SYNOPSIS.md#current-handoff) still selects `think-qv73`, and
this work does not preempt agendas 024–028. It runs beside them as a W7 line with a W1
opening phase, recorded in
[session-093](../../../../packing/campaign/agent-sessions/session-093-atlas-expansion-to-324.md).

**Owns:** The sequence, decisions, and acceptance criteria for widening the frontier
register and the known-best atlas from `n = 1..100` to `n = 1..324`, and for drawing a
second, poster-sized composite that does not replace the first.

**Does not own:** The retention policy text, which
[`packing/resources/web/known-best-packings/README.md`](../../../../packing/resources/web/known-best-packings/README.md)
owns; the claim vocabulary, which [`conventions.md`](../../../../conventions.md) and the
case schema own; any scientific verdict, which stays with the hypothesis registry.

## Overview

The known-best atlas retains one normalized construction and one house rendering for
every `n = 1..100`, and the frontier register holds one typed case record per `n` in the
same range.
The prospective collection already maps sources for every `n = 101..324`, but
carries no claims and no geometry for 123 of those 224 cases.

This plan promotes the whole audited range into the frontier register and the known-best
atlas, in two chunks, and then draws an 18-by-18 composite of `n = 1..324` alongside the
existing 10-by-10 figure.
The horizon is 324 because that is where the catalogue’s own completeness statement
ends; the range beyond it is surveyed here but not built.

The playbook line that governs the order of work is unchanged: **the drawing is not the
constraint, the corpus is.** Every card on the poster needs a frontier record whose
facts are sourced to the same standard as the first hundred.

## Goals

- A frontier record `frontier/n-NNN.md` for every `n = 101..324`, under the same
  `SquarePackingCase/v2` contract, with each lane’s provenance typed rather than null.
- A `Witness/v2` geometry record, feasibility receipt, and house rendering for every
  `n = 101..324`, under the retention policy already applied at `n ≤ 100`.
- One known-best manifest and one builder covering `n = 1..324`, with the existing
  `known-best-1-100` figure family byte-identical after the change.
- A second composite family, `known-best-1-324.{svg,png,pdf}`, laid out 18 by 18, with
  the same per-card facts, legend, and provenance discipline as the first.
- The Kingbird exact-form transcription checked by machine before any of the new range
  is transcribed, closing `think-k5z2`.
- A sourced survey of what is authoritative beyond `n = 324`, so a later extension
  starts from an audit rather than an assumption.
- Validation that still runs on the pull-request surface, with any deferral earned by
  measurement.

## Non-Goals

- No optimality, rigidity-beyond-screen, or `H-044` verdict for any new `n`. A card
  reports what the sources say and what this repository verified.
- No calibration-only annotation (chunk census, partitions, evidence profile, contact
  overlays, grammar coverage) runs over `n > 100`. Those layers stay pinned to
  `n = 1..100` so the new range remains an unseen corpus for a future confirmatory run.
- No raw Kingbird SVG is retained, and no permission is sought from a source author by
  an agent. Seeking express permission is an owner action outside this plan.
- The `n = 1..100` composite is not replaced, resized, or re-laid.
- Nothing above `n = 324` is built.
  Phase 6 audits `325..400` and stops.
- No new top-level tree.
  Code and records stay under `packing/`; reader prose stays at the root.

## Background

### What exists

| Layer | `n = 1..100` | `n = 101..324` |
| --- | --- | --- |
| Frontier record | 100 typed cases, 35 proved | none; `source-coverage.yaml` pins the corpus at 100 |
| Geometry | 64 exact grids, 34 Kingbird-derived numerical facts, 2 UnitSquare renderings | 97 exact grids and 4 UnitSquare cases retained; 123 Kingbird cases located, not retained |
| House rendering | 100 | 101 |
| Composite | `known-best-1-100`, 10 by 10, four exports | none |
| Calibration annotations | census, partitions, profile, overlays, escape screen | prohibited by the seed schema |

The prospective audit of 2026-08-26 found selected geometry for all 224 cases and no
gaps. Its three remaining-work items are this plan’s skeleton: resolve retention for the
123 Kingbird cases, normalize and render what becomes eligible, and audit beyond 324
separately.

### Why 324

The retained catalogue states that for every `n ≤ 324` it does not picture, the trivial
no-tilt grid is the best known packing.
That one sentence is what makes a gapless map derivable.
Above 324 the catalogue pictures a handful of isolated cases and makes no completeness
claim, so `325..400` has no authority to lean on until a survey finds one.
Phase 0 was that survey.
[Its report](../../research/research-2026-09-07-square-packing-sources-beyond-100.md)
found five family members in `325..400` (331, 335, 369, 373, 376), no dense coverage,
and no completeness claim from any source, so Phase 6 does not open under this plan’s
rule.

### Why now, against the standing decision

`think-ezcx` recorded on 2026-08-24 that per-`n` files past 100 should be created only
when a concrete research or reader need justifies them, not because a catalogue reaches
324\. Three things now supply that need:

1. The owner has directed the expansion and the poster.
2. `H-044`’s confirmatory path is “a successor on an unseen corpus frozen after the
   instrument and grammar”, and the PR44 review forbids reusing the inspected 1–100
   corpus as a holdout.
   `n = 101..324` is the only candidate, and it must be frozen as typed geometry before
   it can serve.
3. `H-035` registers its whole regime at `100 ≤ n ≤ 324` and is blocked at zero rounds
   on “a finite target list from the extended corpus”.

This plan supersedes the note on `think-ezcx`; that bead is re-parented under the new
epic rather than closed.

### The retention precedent

At `n ≤ 100` the repository retains no Kingbird SVG. It retains attributed source
metadata, normalized numerical centre-and-angle facts in `Witness/v2`, and house
renderings derived from those facts, under
`retention_policy: metadata-and-derived-numerical-facts-only`. Thirty-four rows of the
current atlas are built that way, and the builder refuses to run if a raw Kingbird
directory exists. The same machinery, `kingbird_derived_witness`, needs no retained SVG
at rebuild time. What the prospective map withholds is the one-time fetch-and-derive
pass.

### Three things called “atlas”

This plan concerns the **known-best** and **prospective** atlases only.
The global typed `n = 11` contact-graph atlas (BC-245) is rejected for the current
portfolio, and the **basin** atlas (`think-eq6l`) is closed.
Neither is touched here.

## Design

### Decisions

Each decision states the default this plan builds and the alternative it rejects.
`D2` is the one the owner should confirm before merge.

**D1: horizon 324.** Build `101..324` in two chunks, `101..200` then `201..324`. Audit
`325..400`; build it only under Phase 6, and only if the survey finds an authority
comparable to the catalogue’s completeness statement.
The survey found none, so Phase 6 stays closed unless the owner chooses the caveated
form listed under Open Questions.
*Rejected:* building to 400 on grids alone, which would assert “best known” with no
source saying so.

**D2: apply the `n ≤ 100` retention precedent to the 123 Kingbird cases.** Fetch each
SVG once, ephemerally; parse it to numerical centre-and-angle facts; retain those facts
in `Witness/v2` with the same attribution, `license_status`, and `raw_asset_retained:
false` fields as the 34 existing rows; verify feasibility at the same tolerance; render
with the house renderer.
Update the prospective map’s `acquisition_status` from `deferred-pending-license-review`
to the policy actually applied.
*Rejected:* retaining raw SVGs (no express terms found), and leaving 123 of 224 cards
empty. *Owner alternative:* express permission from the catalogue’s author, which would
allow raw retention; not required by this plan.

**D3: one collection, one register.** The known-best manifest, witnesses, renderings,
and frontier register widen to `1..324`. The prospective collection’s source map is kept
as the provenance record for the range and its seed is superseded by the known-best
rows; its README says so.
*Rejected:* a second known-best-style collection for `101..324`, which would split the
register and duplicate the pipeline.

**D4: the calibration boundary holds.** The chunk census, partitions, evidence profile,
contact overlays, and grammar coverage keep `range: n=1..100` as an explicit constant
and are not run over new cases.
The translation-escape screen and rigidity assessment do extend, because a certified
slide is a sound certificate and not a calibration instrument.
The corpus is frozen at the commit that closes Phase 3, named in the epic, for any later
confirmatory run.

**D5: the poster is a second family, built by the same code.** The builder takes a
composite specification (first `n`, last `n`, columns, file stem) and emits
`known-best-1-324.svg`, a 1x PNG, and a PDF. Card scale is unchanged from the 1–100
figure, so the canvas is 18 cards wide; legend and footer baselines are computed from
the row count rather than written as constants.
The 2x raster is emitted only if the measured 1x export stays under budget.
Encoding is decided by measurement, not assumption: the 1–100 SVG spends about 460 bytes
per square on data attributes, and 52,650 squares at that rate is about 24 MB. The
poster drops per-square `data-*` attributes and keeps them in the per-`n` renderings; if
that alone does not bring the SVG under 8 MB, coordinate precision is the next lever,
recorded against `D-359`. *Rejected:* replacing or re-laying the 1–100 figure; a
16-by-16 poster to 256, which would stop short of the audited range for no reason the
record gives.

**D6: every fast check stays on the pull-request surface.** The sweeps tier is at about
107 s against a 210 s ceiling with a 1.5x drift rule, and the corpus grows by about
3.2x. The known-best step is split by range so each part is measured on its own, the
census steps stay at their current cost because `D4` keeps them at 100 cases, and any
step that leaves the surface earns its exit by its own measured cost under OR-13.
Ceilings are re-argued from measurement, never bumped.

**D7: workflows.** Phase 0 is W1 research-survey.
Phases 1–5 are W7 pipeline-improvement, with a W2 factual review of each chunk’s
transcription before its cards ship.
Phase 5 closes with the W8 documentation pass and a W10-style handoff entry.
The session record is `session-093`.

### Components

| Surface | Change |
| --- | --- |
| `devtools/check_source_coverage.py` | Reparse every catalogue exact form and degree lock, fail on divergence from the frontier (`think-k5z2`). Handles the multi-line `aligned` form that hid `n = 54`. |
| `devtools/generate_frontier_case.py` (new) | Draft `frontier/n-NNN.md` for `n > 100` from the catalogue transcription and the bound rules below; refuses to overwrite a hand-edited record. |
| `frontier/evidence.yaml` | Widen `E-kingbird-upper-register` scope, or add a sibling for `101..324`; add the grid completeness statement as its own evidence item. |
| `sqpack/known_best.py` | `catalogue_source_map` already takes a range; add the Kingbird fetch-and-derive path for `n > 100` behind the retention fields. |
| `devtools/build_known_best_atlas.py` | Replace the 34 range and layout constants with a corpus range and a list of composite specifications; keep `--fetch` the only network path. |
| `devtools/build_composite_figure_data.py` | Per-composite record; perfect-square rigidity derivation extended to `k = 11..18`. |
| `sqpack/render/color.py`, `style.py` | Check hue separation past 20 classes; add the test. |
| Schemas under `atlas/known-best/` | Range and count constants become per-collection values; new composite entry. |
| `sqpack/cli/validate.py` | Split the known-best step by range; update the pinned counts. |
| `atlas/prospective/` | Map’s `acquisition_status` updated; seed retired with a pointer. |
| `packing/site/`, `check_published_site.py` | Publish the poster family beside the first. |
| README, SYNOPSIS, atlas READMEs, playbook, `frontier/README.md` | Counts, ranges, the second figure, the extension section rewritten for 324. |

### The promotion path for one `n`

1. **Select.** Read the source-availability entry: grid rule, UnitSquare, or Kingbird.
2. **Acquire.** Grid: generate exactly.
   UnitSquare: use the retained, hash-checked SVG. Kingbird: fetch once under `--fetch`,
   parse, keep only the numerical facts.
3. **Normalize.** Emit `Witness/v2` with the source block, retention fields, and a
   feasibility receipt at the tolerance the source supports.
4. **Record.** Generate the frontier case from the transcription and the bound rules.
5. **Render.** House SVG under `atlas/known-best/rendering/`.
6. **Screen.** Translation-escape screen, then the rigidity block.
7. **Review.** W2 pass over the chunk’s transcription against the reparser’s output.
8. **Publish.** Manifest, generated tables, composite record, and the figures.

### Bound rules for generated records

- `reported_upper_bound`: the catalogue’s printed decimal; `exact_form`,
  `algebraic_degree` and `minimal_polynomial` only when the catalogue prints them and
  the reparser agrees; `found_by` and `found_year` from the catalogue credit line where
  parseable, else `null` with provenance `absent`; `construction_method` from the enum,
  `trivial-grid` for rule-generated cases; `catalogue_rigid` from the rigid page, else
  `not-stated`.
- `verified_upper_bound`: `⌈√n⌉` under `E-basic-grid-upper`.
- `reported_lower_bound` and `verified_lower_bound`: Nagamochi’s closed form under
  `E-nagamochi-lower`, exactly as at `n ≤ 100`.
- `status: proved` only where the verified lower bound equals the reported upper bound.
  At `n ≤ 100` that is the rule for every grid-proved case; in `101..324` it yields the
  24 cases `k²`, `k² − 1`, `k² − 2` for `k = 11..18`, and nothing else.
- Arslanov’s Table 4 values at `n = 132, 156, 182, 210, 241, 273, 307` are cross-checked
  against the catalogue; disagreement becomes a typed `conflict`.
- De Winter’s unreplayed claims at `n = 126` and `206` are recorded as
  `source_asserted_unreplayed` notes, not adopted.
- `rigidity` is `null` until the screen writes it; the perfect-square tiling argument
  covers `k = 11..18`.

## Implementation Plan

Beads are linked to this spec; the epic orders them.
Each phase closes on its own validation and a commit.

### Phase 0: Source survey beyond 100 (W1)

- [x] Survey every public catalogue with geometry above `n = 100`: range, formats, reuse
  terms, primary or secondary, last update.
- [x] Write
  `docs/project/research/research-2026-09-07-square-packing-sources-beyond-100.md` with
  the comparison table and the answer for `325..400`.
- [x] Extend the source map’s audit to `325..400` if a source with a completeness claim
  exists; otherwise record the absence as scoped evidence.
  Recorded as scoped evidence in the research document: no such claim exists.
- [x] Archive the catalogue’s Göbel-squares and Göbel-strips pages under
  `packing/resources/web/` so the family statements have a retained source.
  Retained 2026-09-07 with the pandoc procedure the newer catalogue pages use; the
  strips page’s largest rendered entry is 2135, not the 3047 the survey first read from
  an HTML comment.

### Phase 1: Gates

- [x] `think-k5z2`: machine reparse of catalogue exact forms and degrees, run against
  `n = 1..100` first; it must report zero divergences before Phase 2. Landed as
  `sqpack.kingbird_catalogue`; 206 facts checked, zero divergences.
  The catalogue’s `n = 179` entry prints a superseded closed form beside a newer
  decimal, so a generated record must check every form against its decimal.
- [x] Retention record for `101..324`: the prospective map and the retention README
  carry the dated decision; `sources.json` extends when the acquisition pass runs.
- [x] Evidence items for the new range: three scopes widened to 324 and
  `E-kingbird-grid-completeness` added.
- [x] `generate_frontier_case.py` with a golden test against a regenerated `n ≤ 100`
  grid case (the generator must reproduce `n = 100`’s lanes from the same inputs).
  Every bound lane of `n = 100, 99, 98, 64, 50` reproduces byte for byte.
- [x] Parameterize the builder and the figure-data tool by range and composite list; the
  `known-best-1-100` family must be byte-identical before and after.
  `CorpusRange` and `CompositeSpec`; the family, renderings, witnesses and records were
  byte-identical after a rebuild.

### Phase 2: Corpus `101..200`

- [x] Fetch-and-derive the Kingbird cases in range under `D2`. 46 witnesses derived from
  45 pictures (n = 147 is the 148 picture less one square, by the catalogue’s own stated
  rule); 50 exact grids generated; the four UnitSquare cases taken from the retained
  release renderings.
- [x] Witnesses, receipts, renderings, frontier records, manifest for `101..200`. Twelve
  cases come out proved (`k²`, `k² − 1`, `k² − 2` for `k = 11..14`); the `n = 179`
  record carries a typed `stale-source` conflict instead of the catalogue’s superseded
  closed form.
- [x] Escape screen and rigidity blocks over the new cases.
  194 records screened, 176 not rigid, six excluded by shape residual; eight new records
  (132, 154, 155, 156, 179, 180, 181, 182) have hit counts that move between tolerances
  because their sources carry fewer digits, listed in the evidence rather than hidden.
- [ ] W2 review of the chunk’s transcription; conflicts typed.
  The machine reparse reports zero divergences over 114 pictured cases and 409 facts; a
  reviewer pass over credit lines and construction methods (64 cases stay `unknown`) is
  still owed.
- [ ] Gate step for the range measured and recorded in `gate-budgets.yaml`.

### Phase 3: Corpus `201..324`

- [x] The same steps for `201..324`. 124 records (twelve proved), 61 witnesses derived
  from the catalogue (four of them shared-picture subpackings), 63 exact grids; the
  reparse reports zero divergences over 183 pictured cases and 648 facts at the full
  range. At 324 the screen covers 318 records, 296 not rigid, 114 with a separating
  square, 23 tolerance-disagreement cases listed in the evidence; the rigidity
  assessment reads 18 tilings, 296 not rigid, seven undetermined and three left to a
  stronger argument. The full rebuild takes about eleven minutes and the screen about
  three, which Phase 5 must price.
- [x] Freeze: name the commit in the epic as the unseen-corpus baseline.
  Commit `6e21c4ca` on `claude/atlas-expansion-300-400-9f79fc` is the baseline: 324
  typed records and witnesses, with no calibration instrument run above 100.
- [x] Retire the prospective seed; keep and re-point the source map.
  The seed manifest is a dated retirement record pointing at the known-best manifest;
  the source map stays as the provenance record.

### Phase 4: The poster

- [ ] Composite specification for `1..324`, 18 columns; computed baselines; legend
  totals recomputed.
- [ ] Byte-budget measurement built into the builder’s report; encoding chosen from it.
- [ ] Exports with receipts; `render_composite_pdf` handles both families.
- [ ] Hue-separation test past 20 classes.
- [ ] Playbook section rewritten from “Extending to 200” to “The two composites”.

### Phase 5: Gate, documents, closeout

- [ ] Sweeps-tier ceilings re-argued from the recorded measurements.
  Inputs measured on 2026-09-07 on the ten-CPU local host, not calibrated: the
  known-best atlas rebuild takes about eleven minutes at 324 against a 210 s sweeps
  ceiling; the escape screen about three minutes wall; the change-reachable test
  selection passed its 900 s step ceiling in the push tier.
  The candidates are a rebuild that reuses unchanged renderings, `--jobs` for the
  per-case work, and a measured deferral of whatever stays unavoidably slow under OR-13.
- [ ] README, SYNOPSIS, atlas READMEs, `frontier/README.md`, and the site updated; W8
  pass; document map current.
- [ ] Handoff entry naming the frozen corpus commit and the selected next entry.
- [ ] `think-ezcx` re-parented and its note superseded.

### Phase 6 (conditional): `325..400`

- [ ] Opens only if Phase 0 found an authority with a completeness claim for the range.
- [ ] Same promotion path; the poster is not re-laid for it.

## Testing Strategy

- The `known-best-1-100` byte-identity check is the regression for the builder refactor
  and runs in Phase 1 before any new case lands.
- The generator’s golden test reproduces an existing grid case from the same inputs.
- The reparser reports zero divergences at `n ≤ 100` before it is trusted at `n > 100`.
- Every new witness carries a feasibility receipt; the escape screen replays.
- Existing pins (counts, ranges, `maxItems`) are updated by the change that widens the
  range, never loosened ahead of it, so a silently missing case still fails.
- Each chunk’s transcription gets a W2 review recorded under `docs/project/reviews/`.
- The pull-request surface runs everything fast; the deep-gate label runs the rest
  before merge.

## Rollout Plan

One integrated pull request from `claude/atlas-expansion-300-400-9f79fc`, opened at the
first completed phase and refreshed at each phase boundary, with the generated cost
block first (OR-9). Label `deep-gate` last.
The site publishes the poster family beside the first figure once Phase 4 closes.

## Open Questions

- `D2`: does the owner confirm the derived-facts retention route for the 123 Kingbird
  cases, or prefer to seek express permission first?
- Poster exports: is the 1x PNG plus PDF enough, or is a 2x raster wanted regardless of
  size?
- Should the poster ship to the published site, or stay repository-only?
- `325..400`: stop at 324 as the survey indicates, or build the caveated form (grids
  plus the Göbel families from their closed forms, five catalogue-derived values, every
  card marked as having no source that vouches for it as best known)?

## References

- [`packing/atlas/known-best/FIGURE-PLAYBOOK.md`](../../../../packing/atlas/known-best/FIGURE-PLAYBOOK.md),
  section “Extending to n = 1..200”
- [`packing/atlas/prospective/README.md`](../../../../packing/atlas/prospective/README.md),
  “Remaining Work”
- [`packing/resources/web/known-best-packings/README.md`](../../../../packing/resources/web/known-best-packings/README.md),
  the retention policy
- [PR44 review](../../reviews/review-2026-08-26-pr44-constructive-enumeration-and-known-best-atlas.md),
  finding F3 on the unseen corpus
- [`plan-2026-08-28-symbolic-promotion-and-the-atlas.md`](plan-2026-08-28-symbolic-promotion-and-the-atlas.md)
- [Source survey beyond 100](../../research/research-2026-09-07-square-packing-sources-beyond-100.md),
  Phase 0’s report
- Beads: `think-ezcx`, `think-k5z2`, `think-givb` (closed), `think-aaxz` (closed),
  `think-u53m`, epic `think-wfz1`
- Hypotheses `H-035`, `H-044`; defects `D-354`, `D-359`, `D-385`

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
