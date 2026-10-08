# Exact Side Values: Collection, Publication and Remaining Identification

**Date:** 2026-10-06 (updated 2026-10-08)

**Author:** Joshua Levy, with Claude, GPT-5.6 Sol, GPT-6.1 Sol and GPT-6 Astra

**Status:** Collection and publication implemented; identification lanes remain open.

## Scope and Current Result

The continuation starts from `claude/friendly-sagan-jk7qzy` at `d948311d8` (PR 403). Its
branch is `codex/exact-polynomial-coverage`. Workflow entry is **W1 `research-survey`**
for primary-source collection and **W7 `pipeline-improvement`** for exact checks, the
generated register, publication and import contracts.
Each future identification experiment enters **W6** with its own hypothesis and
acceptance rule before execution.

The [register](../../../../packing/frontier/exact-values.json.gz) covers all current
cases $n = 1\ldots324$ and retains source polynomials for larger counts separately.
The freshly verified parent checkpoint has 320 exact identities, one degree-only row and
three numeric-only cases: $n = 29,55,71$. The child is expected to reach 321 exact
identities after its $n = 83$ polynomial is replayed; its refreshed register has not yet
been generated or verified.
Each remaining numeric-only case has a specific route and bead.
The source corpus is bounded by the retained comparison catalogues, explicit thematic
locators, and the pinned SVG readings; this is a complete extraction of that corpus, not
a claim that every polynomial ever published has been found.

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

**Expected child partition, pending regeneration:**

| Current state | Count | Change from the parent branch |
| --- | ---: | --- |
| Integer | 176 | None |
| Rational | 64 | Includes the finite refinements and new arrangements at $n = 68,105,266,270,272,292$ |
| Radical closed form | 65 | Earlier displaced source forms remain historical |
| Minimal polynomial | 16 | Full degree-672 polynomial recovered at $n = 83$; replay pending |
| Degree only | 0 | Expected after the $n = 83$ replay passes |
| Numeric only | 3 | $n = 29,55,71$, each with a named continuation lane |

**Original extraction checkpoint, 2026-10-07:** the historical collector decoded 201
source occurrences into 182 distinct triples of $n$, printed side and integer
coefficient array, reaching $n = 2135$, with zero unparsed rows.
Twenty-one triples matched the original 270-current-exact register entries.
The other 161, plus one additional main-catalogue entry, gave 162 historical register
entries: 152 superseded, three marked invalid by their source, and seven outside the
current frontier. Subsequent delivered child work expanded that record to 170 historical
entries; the refreshed child projection remains pending.
Every entry retains its polynomial in full, exact arithmetic checks, source locator,
attribution and source flags.

An algebraic certificate concerns a side value.
It does not change geometric feasibility, verified bounds, optimality, or a result’s
verification rung.

## Delivered Components

- **Frontier vocabulary and backfill.** The parent implementation records
  `algebraic_source` as `catalogue`, `derived-from-exact-form`, or `contact-system`.
  Radical minimal polynomials are derived exactly; the composite figure reads the
  frontier facts rather than owning a separate derivation.

- **SVG facts.** The pinned readings for $n = 55,71,83,126$ retain exact source text and
  acquisition metadata.
  The first two contain complete contact systems, the third contains all 673
  coefficients of its degree-672 polynomial, and the last exposes neither a polynomial
  nor a current defining system.
  The remaining 34 numeric catalogue SVGs have a separate receipt and derived-facts
  audit in that packet; these are first-time readings, with no earlier digest to
  compare. The source-coverage partition also identifies 13 polynomial rows, two
  exact-form rows and the missing $n = 211$ picture among the initial collection’s 54
  numeric cases.

- **Historical collection.** `devtools.collect_kingbird_historical_polynomials` rebuilds
  the bounded source corpus from retained primary articles.
  Source cells delimit invalid/fixed flags and credit; neighboring rows cannot supply
  either.

- **Register.** `devtools.build_exact_values --check` repeats irreducibility, unique
  root isolation, printed-side agreement, exact closed-form identity and source
  coefficient identity.
  It also verifies retained modular-certificate hints rather than trusting saved
  verdicts. Historical roots are checked at their own printed sides, never at today’s
  better side.

- **Independent audit.** `devtools.audit_historical_side_polynomials` checks the 182
  historical pairs independently with SymPy rational/finite-field factorization and a
  Möbius-transform/Descartes uniqueness argument.
  It also expands every printed source equation at its retained locator.
  Its 29.19 s replay fits the PR surface; it runs in the routine gates and at
  records/full checkpoints.

- **Paper.** `devtools.render_exact_side_values` generates HTML, Markdown and PDF from
  the register. All expressions and coefficients are included, including large
  coefficient tables. The paper is independent of the three-part $n = 11$ series.

- **Publication and imports.** Pages has a dedicated paper job with an explicit wall
  ceiling. The overview, artifact dates, release metadata, published-site contract and
  import runbook include this fourth paper.

The [mathematical review](../../reviews/review-2026-10-07-exact-polynomial-coverage.md)
records independent checks, defects corrected during review, and the remaining limits.
The
[source packet](../../../../packing/resources/web/kingbird-exact-side-facts-2026-10-07/README.md)
provides extraction receipts and primary-source context.

## Continuation Slices and Ownership

The implementation was divided before execution into disjoint parallel lanes.
The coordinator owns shared frontier records, schema, integration, beads and the PR;
workers own source extraction and publication; two Astra reviewers own independent
mathematical reviews.
A delivery-recovery worker checks earlier claimed output.

| Block | Entry and deliverable | Disposition |
| --- | --- | --- |
| 1 | W1: source survey, pinned SVG facts, complete bounded historical extraction | Retained in the source packet; zero undecoded occurrences |
| 2 | W7: exact admission and historical projection | Original collection checkpoint: 270 current exact sides and 162 historical entries |
| 3 | W2 review of W1/W7: independent source, irreducibility and real-root checks | Correctness findings fixed; review retained |
| 4 | W7 **efficiency block**: exact interior-sign root comparisons | Full mathematical replay preserved; initial replay reduced to 31.67 s locally |
| 5 | W7: generated paper, site wiring and import documentation | HTML/Markdown/PDF renderer and publication contracts implemented |
| 6 | W7: final checks, PR, delivery audit and replanning | Final validation is reported in the PR; unavailable earlier outputs remain an explicit dependency |

The efficiency result precedes the expanded historical corpus; it is not the claimed
wall for the larger final register.
No cached mathematical verdict replaces a check.

## Remaining Work and Beads

The parent epic is `think-fh50`, under `think-wfz1`; this continuation is `think-wgo1`.
Parent Phase 1 code beads `think-k9fg`, `think-kj6n`, `think-26at`, `think-pxnx` and
`think-py2q` already closed.
The continuation supplies the paper and publication work formerly assigned to
`think-vtc1`, `think-mepe` and `think-t7a9`, and the retained-source work formerly
assigned to `think-nymu`. Old delegated claims are preserved until their owner
reconciles them.

| Continuation bead | Deliverable |
| --- | --- |
| `think-tj83` | Pinned source facts and the complete historical extraction |
| `think-831v` | Verified historical register entries, including larger $n$ |
| `think-64cy` | Derived-facts receipts and complete bounded coverage audit of the remaining numeric SVGs |
| `think-432w` | Comprehensive generated paper |
| `think-xe25` | Independent Astra mathematical reviews and retained audit tool |
| `think-rno9` | Correctness findings and negative regression controls |
| `think-ymo4` | Site, CI, import process, final validation and PR |
| `think-492g` | Reconcile apparently stronger $n = 259$ source claim: its own cell marks micro-overlaps, so it is retained as source-invalid |

Every numeric-only current count appears exactly once in the following map.

| Bead | Count | Next work and dependency |
| --- | --- | --- |
| `think-je8y` | 29 | Eliminate the retained six-equation X-004 system and certify its real branch; preserve `think-obgk`, `think-xy0e`, `think-utlo` and `think-gucc` |
| `think-phh8` | 55 | Eliminate the seven retained contact/stationarity equations and select the current packing branch |
| `think-1blg` | 71 | Eliminate the six retained equations; the historical degree-8 and degree-4 polynomials describe different, weaker sides |

The original ideal-research batches below retain their count and branch distinctions.
A finite rational side identity does not close their contact-system or stationarity
work. In particular, the source-exact refinements at $n = 68,105,292$ retain their
`think-056g`, `think-gl59` and `think-w622` routes.
A successful identification must preserve producer inputs and contact branch, prove
polynomial irreducibility and unique root selection, and meet the current record’s
source/side contract before admission.
Bounded integer-relation searches supply candidates and scoped negatives; a candidate
relation alone is insufficient.

| Bead | Counts | Next work and dependency |
| --- | --- | --- |
| `think-1atr` | 126 | Recover the current witness/KKT contact system; the retained SVG has a different side and the three historical polynomials do not identify the current record |
| `think-ohhz` | 102, 106, 152, 172, 177, 199, 206, 207, 268, 297, 301 | Audit and admit the eleven earlier claimed identifications (including an unconfirmed KKT seed at 177) only after `think-s6np` recovers or reproduces their outputs |
| `think-056g` | 68, 103, 110, 123, 131, 132, 154, 155, 156 | Low-count precision/degree sweep after the reusable driver is delivered by `think-s6np` |
| `think-d2kj` | 180, 181, 182, 208, 209, 210, 228, 236, 237, 238, 239, 240, 241 | Middle-count sweep, same dependency |
| `think-gg4k` | 259, 269, 270, 271, 273, 302, 303, 304, 305, 306, 307 | High-count sweep, same dependency; preserve historical/invalid source distinctions |
| `think-gl59` | 105 | Establish a current contact system and confirmed KKT seed |
| `think-hg9i` | 130 | Establish a current contact system and confirmed KKT seed |
| `think-uc8i` | 211 | Replace the batch’s bound-only value with a confirmed KKT seed |
| `think-is2e` | 263 | Replace the batch’s bound-only value with a confirmed KKT seed |
| `think-olv8` | 272 | Replace the batch’s bound-only value with a confirmed KKT seed |
| `think-w622` | 292 | Establish a current contact system and confirmed KKT seed |

The existing $n = 29$ negative is specifically a PSLQ run at 700 search digits, using a
1200-digit re-solve, degrees 2 through 20, tolerance $10^{-675}$, `maxcoeff = 10^22` and
`maxsteps = 50000`. No relation was returned in that search.
It is not a proof of a minimum algebraic degree.

Legacy numerical probe labels remain quarantined as candidate/diagnostic outputs under
`think-yuqy`. Bézout upper bounds and bounded PSLQ non-return do not prove a degree or
coefficient lower bound; numerical eliminant residuals do not prove exact linkage.

Additional work:

- **Delivery recovery (`think-s6np`).** The original delivery audit found five commits
  and a generic producer named by closed `think-qgt4` and `think-ifc9` absent from that
  branch, remote deliveries and local worktrees.
  PR 403 then had four delivered commits; its originating Claude session was
  inaccessible. The eleven claimed ideal results remain unadmitted.
  This recovery has already retained the native $n = 11$ and $n = 102$ inputs from
  `evand/square-packing@13ee36e5807727d12a5da36b9b90a96bdba272bf` and checked them
  against `acquisition/upstream-subtree.sha256`. All 320 batch inputs are digest-pinned;
  only these two were selected for recovery.
  The undelivered W7 dependency is the reusable full-active-system driver with an exact
  half-angle export. After delivery, prove the known $n = 11$ octic from contacts as its
  control, then preregister one bounded $n = 102$ W6 slice in `think-ohhz`. This
  recovery has executed no solver, contact-derived control or bounded search.

- **Independent contact derivations (`think-o0az`).** After delivery recovery,
  independently rederive the small-degree catalogue cases (28, 39, 37, 70, 153, 11)
  before attempting the larger cases.
  Source transcription plus algebraic checking does not establish the geometric
  construction.

- **Optional source-index count (`think-chsu`).** Independently count the $n = 83$
  source’s `Root[...,27]` index.
  Index 27 is disclosed as stated and uncounted; unique selection at the reported side
  is already certified.

- **Exact geometric witnesses (`think-blbm`).** The existing radical-family lane remains
  separate: a side expression and its polynomial do not by themselves close the
  exact-witness gap tracked by T-101.

- **macOS mathematical snapshots (`think-e4qp`).** Replace solver-dependent byte or
  floating-point snapshots with assertions on the exact mathematical contract.
  Independent verification accepted the fresh OBBT certificates and all 13 checks on the
  fresh $n = 17$ widened theorem; the narrower reported ratio also satisfies the bound.
  The cause of the platform-dependent output remains unproved.

- **macOS test portability (`think-1fwk`).** Audit inherited RSS, subprocess-startup and
  copy-heavy timing assumptions under external scratch storage.
  Keep declared gate budgets and the required external-storage policy intact.

The selected next entry is **W7 `think-s6np`**, followed by the known $n = 11$
contact-derived control and then one bounded $n = 102$ W6 slice in `think-ohhz`; the
independent $n = 55$ and $71$ elimination lanes can proceed in parallel.
The continuation epic stays open while these identification and witness obligations
remain.

## Validation and Acceptance

The push and PR run the project’s edit, reachable-test and fast surfaces.
The full register rebuild remains on the fast surface; the independent historical audit
runs at PR and records/full checkpoints.
Regressions include perturbed coefficients, a reducible polynomial, an alternate
conjugate, rational approximations substituted for radical forms, a destination-side
mismatch, inward-rounded error bounds, forged modular hints, and source flags or credits
taken from neighboring rows.

The paper checks completeness against the register, independent-series metadata, source
quotation handling, page construction, artifact dates and Pages scope.
The final PDF is rendered with the pinned browser and inspected for layout.
Local and hosted outcomes, costs and final commit identity are recorded in the PR. Pages
publishes on merge; the current request creates and reviews the continuation PR.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
