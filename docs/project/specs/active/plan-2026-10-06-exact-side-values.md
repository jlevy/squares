# Feature: Exact Side Values Register, Paper and Backfill

**Date:** 2026-10-06 (last updated 2026-10-09)

**Author:** Joshua Levy, with Claude, GPT-6.1 Sol and GPT-6 Astra

**Status:** Register and backfill implemented; publication continues in PR 435.
Identification lanes remain open.

## Overview

Every exact fact the repository holds about the side $s$ of a best known packing
(radical closed forms, minimal polynomials, algebraic degrees) is collected in one
generated register. The register checks each fact mathematically and is published as a
web report with typeset mathematics and tables.
The frontier records are backfilled until no derivable fact is missing from them, and
the import process regenerates the register and the paper whenever a result changes one.

Workflow entry: **W7 `pipeline-improvement`** for the register, the checks, the paper
and the import revision; **W1 `research-survey`** for the backfill of facts that
retained sources state.
The identification lanes in Phase 2 enter **W6** under their own hypotheses.

## Current Register and Continuation

The parent refresh integrates `origin/main` at
`657cc486130e9020608ff244d8a86d1d04153634`. Its regenerated register covers 324 cases:
176 integer, 72 rational, 60 closed-form, 12 minimal-polynomial, one degree-only and
three numeric-only values.
It certifies 320 exact polynomial roots.
The degree-only row is $n = 83$; the numeric-only cases are $n = 29,55,71$. All 77
proved cases retain their existing status.

The maintained backfill derives the side identities for 32 current bounds adopted
upstream: 18 RyXu bounds, including the radical side at $n = 51$, and 14 Gupta bounds.
The other 31 sides are native finite rational certificate values.
Current source, count, complete facts, certificate path, replay custody, house geometry
and each upward decimal display are checked before admission.
The polynomial belongs to the native side; the independently checked 16-place upward
display is not a second exact side.
At $n = 51$, the side polynomial is $9s^2-96s+206$; the coordinate field’s polynomial is
separate.

There are 63 current finite witness-side projections: 26 original T-098 sides, two
Rehwaldt refinements, three Daniel arrangements, 18 RyXu and 14 Gupta bounds.
These retain their upper-bound meaning and their scoped assurance.
They establish neither ideal contact geometry nor global optimality.
Ideal contact and stationarity work remains open, including $n = 68$ (`think-056g`),
$n = 105$ (`think-gl59`) and $n = 292$ (`think-w622`). Each current pose needs its own
active contact system and stable KKT seed; an older pose’s KKT data supplies no linkage.

Three improving reported polynomials remain at $n = 106,152,177$, with degrees 32, 40
and 32. Their primitive coefficients, irreducibility and unique roots in the source
intervals are independently checked against acquired source bytes.
They have no admitted geometry or Lean replay and remain V0/C0, under `think-8sm2` and
[issue 419](https://github.com/jlevy/squares/issues/419). Daniel’s T-120 polynomial at
$n = 102$ is now superseded by the current RyXu finite bound; its original coefficients,
root cell, source flags and V0/C0 envelope remain historical evidence.

The parent retains 30 additional source occurrences: that superseded Daniel root and 29
nonselected finite certificates representing 28 distinct rational sides.
Eight RyXu, three Gupta and three Daniel T-129 certificates are superseded.
Eight Couzo T-128 and five Couzo T-130 offers improve current finite sides and remain
pending adoption, with native replay retained and V0/C0 geometry-adoption status.
Both distinct offers at $n = 105$ are preserved.
`think-lhtz` owns independent replay review and the V3/C3 adoption/atlas slice for T-128
and T-130; `think-0mlq` owns T-128 historical source-house custody.
T-130 import `think-88r0` is closed after PR 469 merged; adoption remains open.
The 60 finite rational certificate occurrences partition into 31 selected current, 14
superseded and 15 pending certificates representing 14 distinct pending bounds.
PR 478 adds Daniel’s source-only $n = 132$ certificate as T-131 and a separate $n = 155$
certificate as evidence for T-128. The latter has the same exact side as Couzo’s
retained offer, with distinct source and replay custody; equal sides establish no
local-minimum or motion equivalence.
Both remain V0/C0 pending adoption.
The separate current $n = 51$ radical brings the adopted-current backfill to 32. The
certificate envelope keeps its source pin, facts, original certificate, receipt,
assurance, replay and adoption status.
Source retention is not frontier promotion.

The merged Rehwaldt $n = 68$ v1.2 packet contains a multivariate rational polynomial
system and root box, not a univariate side minimal polynomial; its binding review
remains in `think-nv5o`. Contributor `wand125`’s seven-case fine-net packet covers
$n = 19,20,26,27,28,29,31$; it and the later $n = 27$ follow-up concern lower bounds,
not packing-side identities.
Whole-net native replay, review and adoption remain separate (`think-ndvg` at 27).
Couzo’s retained extended-range decimal poses are outside this register’s $1..324$ range
and do not create inferred exact linear identities.
PR 479 retains the later reports at $n = 375,378$ from revision `2d32a6e` as derived
decimal facts. The superseded `ffd900d` reports remain historical; `think-1545` owns the
outside-corpus reader.
These reports change none of the 324 selected cases.

The child [PR 435](https://github.com/jlevy/squares/pull/435) contains the complete
degree-672 polynomial at $n = 83$, the web report and retained source history.
Its final current and historical census must be regenerated after this parent refresh.
Publication is a web report on Papers with full mathematics and lazy source details; no
report PDF is generated.
Superseded rows remain in the canonical register and are omitted from the public table.

The selected next entry is W7 driver delivery in `think-s6np`, then an independent
contact-derived $n = 11$ octic control, then one preregistered bounded current RyXu
$n = 102$ W6 slice in `think-ohhz`. The current source is
`8dc415296f697f5140caea27c7a0193d52deb4e6`; its complete native certificate is already
retained. The older Daniel input at `13ee36e5807727d12a5da36b9b90a96bdba272bf` remains a
historical driver fixture and cannot satisfy current contact or KKT prerequisites.
This refresh executes no solver, contact-derived control, geometry/Lean replay or
bounded identification search.

The shared maintenance repairs remain under `think-okcb`; snapshot selection remains
under `think-t1lk`. The source snapshot retains all eight historical replay inputs under
the unchanged 192 MiB cap.
The child hosts 13 original source PDFs outside Git and enforces a 5 MiB limit on
tracked PDFs.

**Dated recovery evidence, 2026-10-08:** the original parent certified 319 exact
identities, including 32 native T-098 sides and the certified outward decimal ceiling at
$n = 292$. It correctly refused unequal reported and verified $n = 105$ bounds.
Subsequent refinements superseded those inputs; the original receipts and negative
controls remain retained.
Earlier child counts and qualification receipts cover their stated heads, not this
refreshed stack.

## Resumed Upstream Checkpoint, 2026-10-10

The resumed integration uses fixed main `657cc486130e9020608ff244d8a86d1d04153634`,
including PR 478’s record-hunt evidence and PR 482’s n=17 completion plan.
The previous fixed checkpoint was `1871b14dc`; its source and validation receipts remain
dated. The source-only n=132 and second n=155 certificate occurrences do not replace
current sides or alter any case status, lower bound or global proof claim.

The external volume disconnected twice during qualification.
Parent hosted checks and its full checkpoint passed at f378; its local reachable-test
timeout remains a negative receipt.
The amended child at 4819 completed web reconstruction, while its one local push attempt
ended with exit 138 during the second disconnect before an edit-tier verdict.
Source heads survived both interruptions; no internal scratch fallback was used.
Qualification of this resumed stack requires fresh final-head local checks, automatic PR
checks and the full hosted checkpoint.

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
  (closes think-kj6n, think-26at). The latest 32 adopted bounds now carry side
  identities derived from their exact forms by the maintained backfill producer; earlier
  finite refinements retain their checked native fraction identities.
  The register also checks source-omitted linear identities through the retained-custody
  adapter.

- **A web report:** the Papers page renders the register as HTML, with a Markdown source
  and full closed forms and polynomials.
  It generates no report PDF.

- **Regenerable by process:** the import runbook records exact facts at Stage 3 and
  regenerates the register and the paper at Stage 5. The fast gate fails if the register
  drifts from the records.

- **Gaps mapped:** every numeric-only $n$, and $n = 83$, has a named route to an exact
  value and an open bead that owns it.

## Upstream Refresh Checkpoint, 2026-10-09

The W7 record-refresh slice began at 2026-10-09 20:16:15.292030 UTC and integrates
`origin/main` at `0f16c033a87464cfab127ba54748ca5e2536babd` through the formal stack.
Independent review verified all 58 finite source certificates, all 32 backfilled case
envelopes and all 324 unchanged case statuses and lower bounds.
The maintained records checkpoint passed all 50 selected steps in 529.81 s. PR 475 adds
regional $n = 17$ kernel exclusions and validation repairs, with no change to these side
identities or any global-optimality claim.
Its retained custody disclosure still identifies 204 older objects that are not hosted.

The earlier local push at `81db1641` passed 66 of 67 selected steps.
Its 507-file reachable-test subprocess reported 4,318 passes, one skip and ten failures
in `test_generate_frontier_case.py`, then hit the unchanged 900 s ceiling.
Passing those historical frontiers through the retained in-memory backfill preserves the
original sides, source pins and custody; the 51-test preservation subset passed in
132.17 s. The later parent push at `eac3c2ea` also passed 66 of 67 steps and hit the 900
s reachable ceiling, with 6,524 passes, one skip and four stale math-startup fixtures in
its partial progress receipt.
Those fixtures omitted the runtime-readiness observation and the warm undelayed control
required by the maintained helper.
The corrected module passed all 32 tests without changing the production helper,
readiness guard or timeout.
Both broad-run failures remain dated negative receipts.

The source copier now selects each lexical destination once across overlapping named and
bulk routes. The live inventory and Git projection agree on the same roster; equal-byte
paths and symlink aliases remain distinct and worker writes remain private.
The focused source-copy controls passed all 11 tests, with an additional ambient-Git
isolation control passing independently.
Ruff and BasedPyright are clean for these repairs.
All eight historical replay inputs remain selected; the 192 MiB cap is unchanged and the
final clean-head inventory must satisfy it.

The child also regenerates historical `relationship_to_current` labels after the adopted
bounds changed. This updates comparisons without changing original source identities,
coefficients or exact checks.
PR descriptions and beads retain the actual branch heads, remaining owners and dated
local and hosted receipts.
Qualification requires checks on the final pushed heads; earlier successes do not
qualify the refreshed stack.

## Non-Goals

- No bound, status or rung moves.
  An identified polynomial is a fact about the best known packing, not about $s(n)$.

- No new radical forms where the Galois group makes them impossible (n = 28: $S_6$; n =
  39: $S_5$) or impractical at higher degrees; the register records which.

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
The recovered Daniel inputs at `13ee36e5807727d12a5da36b9b90a96bdba272bf` remain
historical driver fixtures.
Current $n = 102$ prerequisites must bind the retained RyXu certificate at
`8dc415296f697f5140caea27c7a0193d52deb4e6`; input retention supplies no solver or
control verdict.
Broader batches wait for that control and retain each original count and
branch distinction.
Legacy numerical probe labels are quarantined as candidate/diagnostic
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
