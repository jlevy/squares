# Feature: Exact Side Values Register, Paper and Backfill

**Date:** 2026-10-06 (last updated 2026-10-08)

**Author:** Joshua Levy, with Claude, GPT-6.1 Sol and GPT-6 Astra

**Status:** Register and backfill implemented; publication continues in PR 435.
Identification lanes remain open.

## Overview

Every exact fact the repository holds about the side $s$ of a best known packing
(radical closed forms, minimal polynomials, algebraic degrees) is collected in one
generated register. The register checks each fact mathematically and is published as a
standalone paper with typeset mathematics and tables.
The frontier records are backfilled until no derivable fact is missing from them, and
the import process regenerates the register and the paper whenever a result changes one.

Workflow entry: **W7 `pipeline-improvement`** for the register, the checks, the paper
and the import revision; **W1 `research-survey`** for the backfill of facts that
retained sources state.
The identification lanes in Phase 2 enter **W6** under their own hypotheses.

## Current Register and Continuation

The regenerated parent register covers 324 cases: 176 integer, 64 rational, 65
closed-form, 15 minimal-polynomial, one degree-only and three numeric-only values.
It certifies 320 exact polynomial roots and retains 19 superseded catalogue identities
and four separately checked source-only roots as notes.
The degree-only row is $n = 83$; the numeric-only cases are $n = 29,55,71$. All 77
proved cases keep their existing status.
The current identities at $n = 68,105,266,270,272,292$ reflect the latest retained
finite refinements and arrangements.

The finite rational refinements admitted by upstream
[PR 434](https://github.com/jlevy/squares/pull/434) have checked linear identities.
Their reported and verified fractions and complete terminating displays agree exactly;
current source, count, formal evidence, pinned complete facts, replay custody and house
geometry are checked before admission.
Daniel’s new arrangements at $n = 266,270,272$, imported by
[PR 441](https://github.com/jlevy/squares/pull/441), preserve a different display
contract: the reported full decimal is the native fraction, while the verified 16-place
decimal is its least upward ceiling.
The primitive linear polynomial $q s-p$ describes the native fraction, and the display
ceiling remains explicit.
The six frontier records now carry that derived polynomial and its
`derived-from-exact-form` origin through the maintained backfill producer.
The register also admits a source-omitted polynomial only after these scoped custody
checks; nearby substitutions and unsupported polynomial origins are refused.

There are 35 current finite witness-side projections: 29 original native T-098 sides,
three Rehwaldt refinements and three Daniel arrangements.
They retain their upper-bound meaning and proof status.
Ideal contact and stationarity work remains open, including $n = 68$ (`think-056g`),
$n = 105$ (`think-gl59`) and $n = 292$ (`think-w622`). The finite representation gap at
$n = 105$ is resolved.
Each new Daniel pose needs its own active contact system and stable KKT seed; an older
pose’s KKT data supplies no linkage.

Four additional reported polynomials at $n = 102,106,152,177$ have degrees 8, 32, 40 and
32\. Their primitive coefficients, irreducibility and unique roots in the source
intervals are independently checked against the acquired source bytes.
The complete source rows, flags, intervals and acquisition identity remain in notes.
These roots lie below the current finite bounds, but have no admitted geometry or Lean
replay: assurance remains V0/C0. The missing native geometry and field-to-side binding
are tracked in `think-8sm2` and
[issue 419](https://github.com/jlevy/squares/issues/419).

**Earlier recovery checkpoint, 2026-10-08:** the parent certified 319 exact identities,
including the original 33 A1 projections: 32 native T-098 certificate sides and the
certified outward decimal ceiling at $n = 292$. The unequal reported and verified
$n = 105$ bounds were refused.
Those controls remain tied to the retained pre-refinement records and their original
certificate receipts.
The two superseded projections at $n = 68,292$ remain part of that delivered history.
The intermediate PR 434 checkpoint retained 31 original native projections; after the
new Daniel arrangements, 29 remain current.
The earlier source-refresh adapters preserved the primitive linear identities of 23
upstream certified rational witnesses.

The child [PR 435](https://github.com/jlevy/squares/pull/435) contains the full
degree-672 polynomial at $n = 83$, the web reader and complete archives, and the
continuation map. Its earlier recovery build verified 321 exact identities and 170
historical entries. The latest parent additions still require a child rebuild and
projection of the four source-only roots into the separate source history.
The final child census and publication measurements remain pending at this checkpoint.
The selected next entry is W7 driver delivery in `think-s6np`, then the known $n = 11$
contact-derived octic control, then one preregistered bounded $n = 102$ W6 slice in
`think-ohhz`. This recovery has executed no solver, contact-derived control or bounded
identification search.

The shared upstream maintenance repairs are tracked under `think-okcb`. Exact register
replay, rational source regeneration, snapshot custody, ceiling consumers and the
browser startup controls are checked on both stack layers.
Historical mutation-worker outputs leave the snapshot while declared evidence and replay
inputs remain, under the unchanged 192 MiB cap.
`think-t1lk` owns dependency-based snapshot selection.
The child additionally hosts 13 original source PDFs outside Git and enforces a 5 MiB
limit on tracked PDFs.

## Goals

- **One register, generated:** `packing/frontier/exact-values.json.gz` holds one row per
  $n = 1 \dots 324$, built from the frontier records, the retained Kingbird catalogue
  and Evan Daniel’s KKT batch, plus retained verified-bound certificates and replay
  custody for rational projections, by `devtools.build_exact_values`, with `--update`
  and `--check`.

- **Every polynomial checked, not just transcribed:** for each recorded minimal
  polynomial, the register records an irreducibility certificate over $\mathbb{Q}$, a
  rational isolating interval with exactly one real root and agreement of that root with
  the recorded side. Agreement in digits with Daniel’s independent 39-digit KKT value is
  a separate numerical diagnostic when available.

- **Exact facts complete:** the original backfill populates derivable frontier facts,
  with `algebraic_source` distinguishing source transcription from local derivation
  (closes think-kj6n, think-26at). The six latest finite records now carry primitive
  linear identities derived from their native fractions by the maintained backfill
  producer. The register also checks source-omitted linear identities through the
  retained-custody adapter.

- **A paper:** `papers/exact-side-values.html`, `.md` and `.pdf`, rendered from the
  register alone, with every closed form and polynomial in full.

- **Regenerable by process:** the import runbook records exact facts at Stage 3 and
  regenerates the register and the paper at Stage 5. The fast gate fails if the register
  drifts from the records.

- **Gaps mapped:** every numeric-only $n$, and $n = 83$, has a named route to an exact
  value and an open bead that owns it.

## Non-Goals

- No bound, status or rung moves.
  An identified polynomial is a fact about the best known packing, not about $s(n)$.

- No new radical forms where the Galois group makes them impossible (n = 28: $S_6$; n =
  39: $S_5$) or impractical (n = 70); the register records which.

- Solving the n = 29 system is out of scope: it stays with think-je8y, think-obgk,
  think-xy0e, think-utlo and think-gucc, and the register links them.

## Background

At 2026-10-06 the atlas (`atlas/known-best/composite-figure.json`) is the only place the
full picture is assembled, and it does not hold the facts itself:

| State | Count | Where the fact lives |
| --- | ---: | --- |
| Integer side (degree 1) | 182 | Frontier `exact_form` |
| Radical, degree 2 or 4, polynomial derived by the figure builder only | 66 | Frontier `exact_form`; polynomial null in the record |
| Catalogue minimal polynomial | 21 | Frontier `minimal_polynomial`, transcribed |
| Catalogue degree with no polynomial text (n = 83, degree 672) | 1 | Frontier `algebraic_degree` |
| Numeric only | 54 | Nothing exact |

Of the 21 transcribed polynomials, only n = 17 has been recomputed from a contact system
in this repository (H-265, exp-245). n = 11 enters through its published polynomial
(`cases/trump11/derive_field.py`); n = 69 and n = 87 were checked once in scratch code
(`review-2026-10-05-kingbird-intake-n69-n83-n87.md`). The gate checks transcription
fidelity (`devtools.check_source_coverage.polynomial_errors`), not roots or
irreducibility.

The catalogue prints polynomials at 13 more counts (102, 106, 123, 130, 172, 177, 199,
206, 228, 259, 269, 292, 302). Each belongs to a packing that has since been beaten, so
none of them is the side of the record packing.

The three current numeric-only cases have separate routes:

- **n = 29:** the retained six-equation system can support exact elimination and
  selected real-branch certification.
  The bounded PSLQ non-return above is not a degree or coefficient lower bound.

- **n = 55 and n = 71:** PR 435 retains source definitions, seven contact/stationarity
  equations at 55 and six contact equations at 71, plus approximate branch values.
  Elimination must exclude extraneous and rank-deficient branches and recover an exact
  geometry map. The historical quartic and octic at 71 describe different sides.

The finite rational identity at $n = 105$ is now represented, while `think-gl59` still
needs a confirmed ideal KKT seed and current contact system.
Its retained Kingbird SVG concerns an older side and supplies no equations.
The refined finite sides at $n = 68$ and $n = 292$ likewise leave their ideal contact
routes open in `think-056g` and `think-w622`.

The child’s retained degree-672 polynomial is expected to complete the parent’s $n = 83$
degree-only row once the child rebuild passes.
Ideal KKT/contact research at other counts remains separate from the exact identity of a
finite rational certificate side.
The selected delivery slice is W7 `think-s6np`, before W6 experiments: deliver the
reusable full-active-system driver and exact half-angle export, then prove the known
$n = 11$ octic from contacts as its control, then preregister one bounded $n = 102$ run.
The two native inputs have already been recovered and checked against the retained
manifest at evand/square-packing commit `13ee36e5807727d12a5da36b9b90a96bdba272bf`;
input recovery supplies no solver or control verdict.
Broader batches wait for that control and retain each original count and branch
distinction. Legacy numerical probe labels are quarantined as candidate/diagnostic
outputs under `think-yuqy`; Bézout upper bounds and bounded PSLQ non-return cannot prove
a degree or coefficient lower bound, and a numerical eliminant residual cannot prove
exact linkage.

## Design

### Approach

The frontier records stay the system of record, and the register is a view checked
against them, as `composite-figure.json` is.
The paper is a view of the register, and no fact on it is typed into a template.

### Components

1. **Record vocabulary** (`frontier/square-packing-case.schema.yaml`).
   `reported_upper_bound.algebraic_source` is one of:

   - `catalogue`: the source prints the degree or polynomial;

   - `derived-from-exact-form`: computed here from the source’s radical;

   - `contact-system`: computed here from an exact contact system, citing evidence.

   The original backfill records it with derived or transcribed polynomial facts.
   Current finite-refinement source rows carry the primitive linear polynomial and its
   derived origin after backfill.
   The register accepts either that supported form or an omitted polynomial only after
   the scoped custody checks.
   `devtools.generate_frontier_case` writes it for new catalogue intakes.

2. **Backfill** (`devtools.backfill_algebraic_facts`, one-shot with `--check`).

   - Writes `algebraic_degree`, `minimal_polynomial` and
     `algebraic_source: derived-from-exact-form` for every record whose `exact_form` is
     a radical, and `algebraic_source: catalogue` for the 22 transcribed records.

   - The composite figure then reads the source from the record (think-26at), and
     `build_composite_figure_data --review` reports zero facts derived only in the
     figure.

3. **Register builder** (`devtools.build_exact_values`, data in
   `frontier/exact-values.json.gz` under contract `packing.squares:ExactValues/v1`). Per
   $n$ it holds:

   - the side, lower bound and status;

   - the exact form, the polynomial as primitive integer coefficients, the degree and
     `algebraic_source`;

   - checks: the irreducibility certificate (factorization for low degree, otherwise the
     primes whose factorization patterns exclude every proper factor degree), the
     isolating interval, root agreement with the record, digits of agreement with
     Daniel’s `S_exact`, and the Galois group and solvability for degree ≤ 6;

   - notes: a superseded catalogue polynomial, missing polynomial text, the route and
     owning bead for numeric-only cases, and any recorded integer-relation negative with
     its scope.

   `--check` recomputes the register and compares it with the stored copy, so it runs in
   the fast tier only if it fits the wall ceiling (OR-17). If not, the expensive
   certificates move to `--records` and the fast tier checks only structure and record
   agreement.

4. **Paper** (`devtools.render_exact_side_values`, template
   `devtools/templates/exact-side-values-article.md`).

   - Sections: what “exact” means here and what each source proves; the closed-form
     families; the polynomial table (degree, height, Galois data, checks); every
     polynomial in full in an appendix; the numeric-only cases with 39-digit values and
     routes; superseded catalogue polynomials; open problems.

   - It is registered in `render_overview.PAPERS` with its Pages job, budget and
     version, per `development.md`.

5. **Import revision.** These documents change:

   - `campaign/result-import.md`: Stage 3 records exact facts with `algebraic_source`;
     Stage 5 runs `build_exact_values --update` and the paper renderer.

   - `campaign/documentation-pass.md`, New Result Publication: lists the register and
     the paper.

   - `development.md`: the register and the paper.

## Implementation Plan

### Phase 1: Register and Backfill in PR 403; Publication in PR 435

- [x] Schema: `algebraic_source`; generator support; contract test.

- [x] Backfill tool and records: 66 derived and 22 catalogue sources; composite-figure
  reads the record; think-kj6n and think-26at closed.

- [x] Register builder with irreducibility, root isolation, Daniel agreement and Galois
  data; tests with controls (a reducible polynomial, a wrong root, a perturbed
  coefficient, a superseded catalogue polynomial).

- [x] Gate step wired at the tier its measured cost allows.

- [ ] Paper renderer, template and site registration (PAPERS, `pages.yml`, budgets,
  release version, artifact dates, published-site check).

- [ ] Import runbook, documentation pass and development guide revised.

### Phase 2: Identification lanes (one W6 slice each, separate pull requests)

These lanes are parallel and disjoint:

- [ ] **High-precision sweep.** Wrap `exactsolve.py` from its retained copy in an
  instrument that re-solves Daniel’s KKT points for the numeric-only counts at rising
  precision and runs a bounded integer-relation search.
  Accepted identifications go to the register as `contact-system` with root and
  irreducibility checks.
  Negatives are recorded with their degree, height and digit scope.

- [ ] **Retention.** Retain `square-55.svg`, `square-71.svg` and `square-83.svg` from
  Kingbird in a packet, and transcribe any defining system or polynomial they hold
  (think-xy91, think-krbs).

- [ ] **Recomputation.** Recompute the transcribed catalogue polynomials from contact
  systems by a generic driver: witness → active set (`exactsolve` or
  `sqpack.promote.contacts`) → half-angle system → resultant elimination, in the exp-245
  pattern. Start with small degrees (28, 39, 70, 153, 37, 11).

- [ ] **Closed forms.** Certify exact algebraic witnesses for the radical families over
  $\mathbb{Q}(\sqrt 2)$ and $\mathbb{Q}(\sqrt 7)$, so a verified upper bound can equal
  the exact form instead of trailing it (the T-101 gap).

## Beads

Epic `think-fh50`, under `think-wfz1`.

| Bead | Work | Blocked by |
| --- | --- | --- |
| `think-k9fg` | Schema `algebraic_source`, generator and intakes | — |
| `think-kj6n` | Backfill of derived degrees and polynomials | `think-k9fg` |
| `think-26at` | Composite figure reads the record | `think-kj6n` |
| `think-pxnx` | Register builder and its checks | `think-k9fg`, `think-kj6n` |
| `think-py2q` | Register gate step at its measured tier | `think-pxnx` |
| `think-vtc1` | Paper renderer and template | `think-pxnx` |
| `think-mepe` | Paper site registration | `think-vtc1` |
| `think-t7a9` | Import runbook, documentation pass, frontier README | `think-pxnx`, `think-vtc1` |
| `think-9ok9` | Phase 1 close: validation and pull request | all of Phase 1 |
| `think-eu89` | High-precision identification sweep | `think-pxnx` |
| `think-nymu` | Kingbird SVG retention (55, 71, 83); feeds `think-xy91`, `think-krbs` | — |
| `think-qgt4` | Generic contact-system driver; feeds `think-3lro` | `think-pxnx` |
| `think-ifc9` | Recompute small-degree catalogue polynomials | `think-qgt4` |
| `think-blbm` | Exact algebraic witnesses for the radical families | `think-pxnx` |

## Testing Strategy

- Unit tests for the polynomial checks, each with a positive case and a refused negative
  control.

- The register `--check` and the paper `--check` as gate steps.

- `check_source_coverage` continues to hold catalogue fidelity, and the backfill must
  not trip it.

- Before the push, the push tier and the fast tier of `packing-validate`.

## Rollout Plan

PR 403 contains the register and backfill.
Dependent PR 435 contains the expanded source collection and publication.
Pages publishes the paper when the stack merges.
Phase 2 lanes each update the register through the revised import process.

## Open Questions

- Whether the recomputation of degree-144 and degree-158 polynomial certificates fits
  the fast-tier ceiling.
  This is measured in Phase 1 and decides where the step runs.

## References

- [`packing/campaign/result-import.md`](../../../../packing/campaign/result-import.md)

- [`packing/atlas/known-best/composite-figure.json`](../../../../packing/atlas/known-best/composite-figure.json)

- `packing/resources/web/evand-square-packing-2026-10-05/`

- Beads: think-kj6n, think-26at, think-18mu, think-xy91, think-krbs, think-je8y,
  think-obgk, think-3lro

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
