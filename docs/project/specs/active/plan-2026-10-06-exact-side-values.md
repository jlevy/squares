# Feature: Exact Side Values Register, Paper and Backfill

**Date:** 2026-10-06 (last updated 2026-10-06)

**Author:** Joshua Levy, with Claude

**Status:** Draft

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

## Goals

- **One register, generated:** `packing/frontier/exact-values.json` holds one row per
  $n = 1 \dots 324$, built from the frontier records, the retained Kingbird catalogue
  and Evan Daniel’s KKT batch, by `devtools.build_exact_values`, with `--update` and
  `--check`.
- **Every polynomial checked, not just transcribed:** for each recorded minimal
  polynomial, the register records an irreducibility certificate over $\mathbb{Q}$, a
  rational isolating interval with exactly one real root, agreement of that root with
  the recorded side, and its agreement in digits with Daniel’s independent 39-digit KKT
  value.
- **Records complete:** `algebraic_degree` and `minimal_polynomial` populated in the
  frontier record wherever they are derivable, with an `algebraic_source` saying whether
  the source printed them or this repository derived them (closes think-kj6n,
  think-26at).
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

The numeric-only cases split by tractability:

- **n = 29:** the defining six-equation system is retained, and integer relations up to
  degree 20 with coefficients below 1e22 are excluded at 1000 digits.
- **n = 55 and n = 71:** the Kingbird SVGs credit an exact analytic solution to
  Ellsworth, but only the poses were retained (think-xy91).
- **n = 83:** the polynomial text is in `square-83.svg`, which is not retained
  (think-krbs).
- **Everything else:** binary64 witnesses only, but Daniel’s packet carries a
  numerically confirmed KKT point for 315 counts, and his `exactsolve.py` re-solves it
  to 60–1000 digits with an `--algdeg` integer-relation search.

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

   It is required whenever `algebraic_degree` is non-null.
   `devtools.generate_frontier_case` writes it for new catalogue intakes.

2. **Backfill** (`devtools.backfill_algebraic_facts`, one-shot with `--check`).
   - Writes `algebraic_degree`, `minimal_polynomial` and
     `algebraic_source: derived-from-exact-form` for every record whose `exact_form` is
     a radical, and `algebraic_source: catalogue` for the 22 transcribed records.
   - The composite figure then reads the source from the record (think-26at), and
     `build_composite_figure_data --review` reports zero facts derived only in the
     figure.

3. **Register builder** (`devtools.build_exact_values`, data in
   `frontier/exact-values.json` under contract `packing.squares:ExactValues/v1`). Per
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

### Phase 1: Register, backfill, paper and process (one pull request)

- [ ] Schema: `algebraic_source`; generator support; contract test.
- [ ] Backfill tool and records: 66 derived and 22 catalogue sources; composite-figure
  reads the record; think-kj6n and think-26at closed.
- [ ] Register builder with irreducibility, root isolation, Daniel agreement and Galois
  data; tests with controls (a reducible polynomial, a wrong root, a perturbed
  coefficient, a superseded catalogue polynomial).
- [ ] Gate step wired at the tier its measured cost allows.
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

## Testing Strategy

- Unit tests for the polynomial checks, each with a positive case and a refused negative
  control.
- The register `--check` and the paper `--check` as gate steps.
- `check_source_coverage` continues to hold catalogue fidelity, and the backfill must
  not trip it.
- Before the push, the push tier and the fast tier of `packing-validate`.

## Rollout Plan

Phase 1 merges as one pull request.
Pages publishes the paper on merge.
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
