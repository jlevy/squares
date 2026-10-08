# Exact Side Values: Collection, Publication and Remaining Identification

**Date:** 2026-10-06 (last updated 2026-10-09)

**Author:** Joshua Levy, with Claude, GPT-5.6 Sol, GPT-6.1 Sol and GPT-6 Astra

**Status:** Collection and publication implemented; identification lanes remain open.

## Scope and Current Result

The formal stack is `main` → PR 403 (`claude/friendly-sagan-jk7qzy`) → PR 435
(`codex/exact-polynomial-coverage`). Workflow entry is W1 `research-survey` for
source collection and W7 `pipeline-improvement` for record and publication maintenance.
Future identification experiments enter W6 with their own preregistered acceptance rule.

Every exact fact the repository holds about the side $s$ of a best known packing
(radical closed forms, minimal polynomials, algebraic degrees) is collected in one
generated register. The register checks each fact mathematically and is published as a
web report with typeset mathematics and tables.
The frontier records are backfilled until no derivable fact is missing from them, and
the import process regenerates the register and the paper whenever a result changes one.

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

The parent refresh integrates `origin/main` at
`0f16c033a87464cfab127ba54748ca5e2536babd`. Its regenerated register covers 324 cases:
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

The parent retains 28 additional identities: that superseded Daniel root and 27
nonselected finite certificates.
Eight RyXu, three Gupta and three Daniel T-129 certificates are superseded.
Eight Couzo T-128 and five Couzo T-130 offers improve current finite sides and remain
pending adoption, with native replay retained and V0/C0 geometry-adoption status.
Both distinct offers at $n = 105$ are preserved.
`think-lhtz` owns independent replay review and the V3/C3 adoption/atlas slice for T-128
and T-130; `think-0mlq` owns T-128 historical source-house custody.
T-130 import `think-88r0` is closed after PR 469 merged; adoption remains open.
The 58 finite rational source identities partition into 31 selected current, 14
superseded and 13 pending certificates; the separate current $n = 51$ radical brings the
adopted-current backfill to 32. The certificate envelope keeps its source pin, facts,
original certificate, receipt, assurance, replay and adoption status.
Source retention is not frontier promotion.

The merged Rehwaldt $n = 68$ v1.2 packet contains a multivariate rational polynomial
system and root box, not a univariate side minimal polynomial; its binding review
remains in `think-nv5o`. Contributor `wand125`’s seven-case fine-net packet covers
$n = 19,20,26,27,28,29,31$; it and the later $n = 27$ follow-up concern lower bounds,
not packing-side identities.
Whole-net native replay, review and adoption remain separate (`think-ndvg` at 27).
Couzo’s retained extended-range decimal poses are outside this register’s $1..324$ range
and do not create inferred exact linear identities.
The later reports at $n = 375,378$ from revision `2d32a6e` are not retained in the
pinned `ffd900d` packet; `think-1545` owns their intake and supersession design.

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

**Expected child partition, pending regeneration:**

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

At the earlier upstream-integration checkpoint, the delivered child retained 170
historical identities: 160 superseded, three source-invalid and seven outside the
current frontier.
Five printed identities and three source closed forms became historical
when upstream supplied better certified rational witness sides.
The closed forms at $n = 237,258,263$ have derived polynomials and explicit
source-expression provenance; the bounded printed corpus has no equation rows at
$n = 237$ or $263$.

An algebraic certificate concerns a side value.
It does not change geometric feasibility, verified bounds, optimality, or a result’s
verification rung.

## Delivered Components

- **Frontier vocabulary and backfill.** The parent implementation records
  `algebraic_source` as `catalogue`, `derived-from-exact-form`, or `contact-system`.
  Radical minimal polynomials are derived exactly; the composite figure reads the
  frontier facts rather than owning a separate derivation.
  The linear identities at $n = 7,8,15$ are marked as derived from their exact forms,
  rather than as source-printed equations.

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

- **Independent audit.** `devtools.audit_historical_side_polynomials` checks the 182
  historical pairs independently with SymPy rational/finite-field factorization and a
  Möbius-transform/Descartes uniqueness argument.
  It also expands every printed source equation at its retained locator.
  Its 29.19 s replay fits the PR surface; it runs in the routine gates and at
  records/full checkpoints.

- **Paper.** `devtools.render_exact_side_values` generates a searchable web browser and
  complete HTML, Markdown and PDF archives from the register.
  All expressions and coefficients are included, including large coefficient tables.
  The paper is independent of the three-part $n = 11$ series.

- **Publication and imports.** Pages has a dedicated paper job with an explicit wall
  ceiling. The overview, artifact dates, release metadata, published-site contract and
  import runbook include this fourth paper.

- **Source PDF custody.** The 13 hosted originals retain their source bytes.
  The [manifest](../../../../packing/hosted/source-pdfs.yaml) records original archive
  paths, sizes and SHA-256 digests; the loader checks downloaded bytes against it.
  Faithful extractions and acquisition metadata remain in the repository, and the
  tracked-PDF guard keeps its 5 MiB ceiling.

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
| 6 | W7 **efficiency block**: practical web reading (`think-mo36`) | Searchable index, lazy metadata and coefficient vectors; complete archives retained |
| 7 | W7: final checks, PR, delivery audit and replanning | Final validation is reported in the PR; unavailable earlier outputs remain an explicit dependency |
| 8 | W7: upstream integration and PDF storage maintenance (`think-okcb`) | Earlier 2026-10-08 checkpoint: 287 current exact values, 170 historical identities and 37 numeric routes; 13 original PDFs hosted outside Git and a universal 5 MiB tracked-PDF gate |
| 9 | W7: upstream CI contract repair | Rational refresh, hosted citation identity, publication payloads, snapshot custody, measured suite admissions and startup delay controls repaired; independent Astra review passed |

The two stack layers have separate registers.
At the earlier 2026-10-08 CI-repair checkpoint, PR 403 had 286 exact current values, one
degree-only value at $n = 83$, 37 numeric-only values and 18 legacy historical notes.
PR 435 supplied the $n = 83$ polynomial and full 170-entry historical collection.
Both retained 77 proved cases.
The refreshed parent and pending child partitions are recorded above.

The integration repair beads are `think-3y4q`, `think-uy3e`, `think-9sgi`, `think-kfpc`,
`think-qr37` and `think-s5ou`, under `think-okcb`. At that earlier checkpoint, the
snapshot repair omitted 312 unused historical output files (3,670,529 bytes), retained
declared evidence, source and replay inputs, and passed all 174 registered mutation
controls with the existing 192 MiB cap.
Its headroom is narrow; `think-t1lk` owns dependency-based selection.
Local admissions retain the existing suite-cost observations and 10% unrecorded-share
limit.
The startup self-test checks the measured readiness-call wait for its injected 300
ms delay, independently of navigation overhead.
Final validation and publication identities are reported in the PRs.

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

At the earlier upstream-integration checkpoint, 17 former numeric cases became certified
rational current values and left the numeric-only map.
Their contact and stationarity work stays open where it seeks an ideal algebraic packing
rather than the finite rational certificate.
In particular, `think-1atr` at 126, `think-hg9i` at 130 and `think-is2e` at 263 retain
their contact-system obligations.
A linear polynomial for a feasible witness side does not close those research questions
or prove optimality.
The upstream integration is `think-5lcy` and the hosted-PDF migration is `think-286j`,
under `think-okcb`.

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

The canonical web page adds search, section/kind/status filters and pagination.
Individual records and exact coefficient strings load only when opened; numeric rows and
historical source-invalid or superseded rows keep their separate meanings.
`think-r4rt` owns the export, `think-uunz` the browser and `think-3t5y` the independent
Astra review under `think-mo36`. The
[bounded measurement](../../../../packing/benchmarks/exact-catalogue-web/report.md)
checks the predeclared raw-byte threshold; complete archives preserve the full record.
The selected mathematical continuation remains `think-s6np`.

The final full checkpoint exercises the shared case-record browser as well.
`think-gtyf` tracks synchronous case-popover close state, with a deterministic
regression and independent Astra review; final corrected-head validation is recorded in
the PR.

The paper checks completeness against the register, independent-series metadata, source
quotation handling, page construction, artifact dates and Pages scope.
The final PDF is rendered with the pinned browser and inspected for layout.
Local and hosted outcomes, costs and final commit identity are recorded in the PR. Pages
publishes on merge; the current request creates and reviews the continuation PR.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
