# Exact Side Values: Collection, Publication and Remaining Identification

**Date:** 2026-10-06 (last updated 2026-10-10)

**Author:** Joshua Levy, with Claude, GPT-5.6 Sol, GPT-6.1 Sol and GPT-6 Astra

**Status:** Collection and publication implemented; CI stabilization and identification
lanes remain open.

## Scope and Current Result

The formal stack is `main` → PR 403 (`claude/friendly-sagan-jk7qzy`) → PR 435
(`codex/exact-polynomial-coverage`). Workflow entry is W1 `research-survey` for source
collection and W7 `pipeline-improvement` for record and publication maintenance.
Future identification experiments enter W6 with their own preregistered acceptance rule.

Every exact fact the repository holds about the side $s$ of a best known packing
(radical closed forms, minimal polynomials, algebraic degrees) is collected in one
generated register. The register checks each fact mathematically and is published as a
web report with typeset mathematics and tables.
The frontier records are backfilled until no derivable fact is missing from them, and
the import process regenerates the register and web report whenever a result changes
one.

The [register](../../../../packing/frontier/exact-values.json.gz) covers all current
cases $n = 1\ldots324$ and retains source polynomials for larger counts separately.
The verified parent checkpoint has 320 exact identities and one degree-only row.
The regenerated child has 321 exact identities, including the full $n = 83$ polynomial,
and three numeric-only cases: $n = 29,55,71$; all 77 proved cases keep their status.
Each remaining numeric-only case has a specific route and bead.
Ideal contact-system research remains open separately from the identity of a finite
certified bound. The source corpus is bounded by the retained comparison catalogues,
explicit thematic locators, and the pinned SVG readings; this is a complete extraction
of that corpus, not a claim that every polynomial ever published has been found.

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
The existing `think-kkj2` owns independent review and adoption of T-131 at $n = 132$,
preserving T-098 as historical evidence; `think-iyij` retains the import/reply work.
The original Couzo adoption and historical-house owners remain `think-lhtz` and
`think-0mlq`. The separate current $n = 51$ radical brings the adopted-current backfill
to 32. The certificate envelope keeps its source pin, facts, original certificate,
receipt, assurance, replay and adoption status.
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
decimal facts and current beyond-horizon rows.
They supersede the dated `ffd900d` reports, which remain historical; `think-1545` owns
the outside-corpus reader work.
These source reports supply neither geometry replay nor exact side identities, and they
change none of the 324 selected cases.

The child [PR 435](https://github.com/jlevy/squares/pull/435) contains the complete
degree-672 polynomial at $n = 83$, the web report and retained source history.
The independently audited child census is 324 current rows and 214 historical rows: 186
superseded, 18 unreconciled source, seven outside the frontier and three source-invalid.
Its current partition is 176 integer, 72 rational, 60 closed-form, 13
minimal-polynomial, zero degree-only and three numeric-only values.
All 175 earlier historical identities survive; 29 nonselected certificate occurrences
and ten newly displaced catalogue identities add 39 historical rows.
The full register retains 538 records, 560 coefficient vectors and 6,378 integer
coefficient strings in 2,821,903 decoded bytes / 843,684 gzip bytes.
At $n = 83$, all 673 coefficients remain intact, including the 724-digit integer.
Source ordinal 27 remains explicitly uncounted independently (`think-chsu`).

Publication is a web report on Papers with full mathematics and lazy source details; no
report PDF is generated.
The public subset has 352 records: all 324 current rows and 28 relevant source rows,
with 352 coefficient vectors and 2,128 integer strings.
It omits the 186 superseded rows and 22 redundant current superseded notes while the
canonical register retains them in full.
Pending adoption remains visibly V0/C0; retained replay is not global optimality.
Final web reconstruction and responsive qualification must use the clean published child
head.

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

**Verified child partition:**

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

- **Gaps mapped:** each numeric-only $n = 29,55,71$ has a named route to an exact value
  and an open bead that owns it.
  The $n = 83$ identity is complete; independent source-index counting remains optional
  under `think-chsu`.

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

The resumed parent inventory retained all eight replay leaves: 197,970,624 bytes under
the unchanged 201,326,592-byte cap, with 3,355,968 bytes of headroom.
Its one broad push attempt passed 65 edit checks, including exact-register verification,
but the type floor timed out at its maintained 900-second command ceiling with no
emitted diagnostic; reachable tests were skipped.
This is a local negative receipt, not an edit-tier pass.
The selected type-only follow-up passed at the same parent head in 428.620 seconds, with
zero errors, warnings or notes and unchanged timeout and worker flags.
That focused result does not replace the broad negative or supply a reachable verdict.
The child source collector check and 158 focused builder, custody, catalogue, renderer
and Pages tests passed; affected-file Ruff and BasedPyright were clear.
All 324 current and 212 previous historical objects survived the actual child rebuild,
with only the two new certificate occurrences added.

The child push attempt at `71a2249082` exposed generated URL-registry drift after 65
checks passed. It was stopped with normal SIGINT (exit 130) so the actual omission could
be repaired; three active commands were cancelled and reachable tests have no verdict.
The maintained URL generator added four coefficient and metadata payload URLs for
Daniel’s n=132 and separate n=155 occurrences.
Its historical-compatibility check then passed all 1,629 rows with zero failures and no
removed URLs. The register mathematics and reconstruction had already passed.
Current-head push, responsive web and hosted qualification remain required after this
repair; the interrupted gate remains a dated negative receipt.

## Upstream Refresh Checkpoint, 2026-10-09

The W7 record-refresh slice began at 2026-10-09 20:16:15.292030 UTC and integrates
`origin/main` at `1871b14dc630f802084695b7bd6007bac53b3714` through the formal stack.
Independent review verified all 58 finite source certificates, all 32 backfilled case
envelopes and all 324 unchanged case statuses and lower bounds.
The maintained records checkpoint passed all 50 selected steps in 529.81 s. PR 475 adds
regional $n = 17$ kernel exclusions and validation repairs, with no change to these side
identities or any global-optimality claim.
Its retained custody disclosure still identifies 204 older objects that are not hosted.
The previous upstream snapshot was `0f16c033`; the final snapshot also includes PR 479’s
later Couzo reports and PR 480’s owner-authorized temporary quick-lane budgets.
The current suite ceilings are 335/360/360/335 seconds; `think-2hm6` owns reducing that
cost. The older 106-step cohort below remains dated evidence under its original
143-second limit. The parent preparation at `1675e5f8` was interrupted to incorporate
these newly merged records; its cancellation is not a source-test verdict.

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

At child `b024d100`, the local push passed 68 of 69 selected steps.
Its 518-file reachable-test subprocess recorded 7,200 passes, 33 skips and five failures
before the unchanged 900 s ceiling.
Four failures were the inherited math-startup fixtures; the fifth was the saved
historical corpus carrying comparisons against older current bounds.
This completed broad-run audit remains negative evidence.

The final child refresh rebuilt the historical corpus with the maintained collector’s
full default exact verification.
Exactly 57 `relationship_to_current` fields changed across 22 counts; all 182 original
source identities, complete coefficient arrays and exact-check objects are unchanged and
verified. The maintained full `--check` passed, and the existing saved-corpus regression
passed in 14.25 s without changing its source conservation or 182-verified assertions.
PR descriptions and beads retain the actual branch heads, remaining owners and dated
local and hosted receipts.
Qualification requires checks on the final pushed heads; earlier successes do not
qualify the refreshed stack.

The earlier child records checkpoint passed 51 of 52 steps in 284.54 s; its sole failure
was the stale URL manifest for three obsolete $n = 102$ payloads.
The maintained retirement command confirmed those addresses were never published on
`origin/main`; the refreshed 1,624-row URL manifest and compatibility check passed.
The corrected $n = 102$ prerequisite changes one text field and preserves every other
register field. The regenerated checker certified all 321 polynomials and roots.
All seven stale child expectations and the current-pose route control passed in the
54-test affected suite.
These are dated repair receipts; final-head qualification remains required.

## Non-Goals

- No bound, status or rung moves.
  An identified polynomial is a fact about the best known packing, not about $s(n)$.

- No new radical forms where the Galois group makes them impossible (n = 28: $S_6$; n =
  39: $S_5$) or impractical at higher degrees; the register records which.

- Solving the n = 29 system is out of scope: it stays with think-je8y, think-obgk,
  think-xy0e, think-utlo and think-gucc, and the register links them.

## Background

The atlas (`atlas/known-best/composite-figure.json`) consumes the frontier facts and
generated register rather than holding an independent derivation.
The verified child partition after the 2026-10-09 upstream refresh is:

| State | Count | Where the fact lives |
| --- | ---: | --- |
| Integer | 176 | None |
| Rational | 72 | Includes the adopted finite source certificates and their native side identities |
| Radical closed form | 60 | Earlier displaced source forms remain historical |
| Minimal polynomial | 13 | Full degree-672 polynomial recovered and checked at $n = 83$ |
| Degree only | 0 | Resolved by the checked $n = 83$ polynomial |
| Numeric only | 3 | $n = 29,55,71$, each with a named continuation lane |

**Original extraction checkpoint, 2026-10-07:** the historical collector decoded 201
source occurrences into 182 distinct triples of $n$, printed side and integer
coefficient array, reaching $n = 2135$, with zero unparsed rows.
Twenty-one triples matched the original 270-current-exact register entries.
The other 161, plus one additional main-catalogue entry, gave 162 historical register
entries: 152 superseded, three marked invalid by their source, and seven outside the
current frontier. Subsequent delivered child work expanded that record to 170 historical
entries; the pre-refresh checkpoint expanded it to 175 while preserving the earlier
corpus. The 2026-10-09 refresh retains those 175 and adds 37 rows, reaching 212; the
2026-10-10 source refresh adds the two Daniel certificate occurrences, reaching 214.
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

The child’s checked degree-672 polynomial completes the parent’s $n = 83$ degree-only
row. Its source ordinal remains independently uncounted.
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

- **Web report.** `devtools.render_exact_side_values` generates a searchable catalogue,
  complete HTML report and Markdown export from the register.
  All expressions and coefficients are included, including large coefficient tables.
  The paper is independent of the three-part $n = 11$ series.

- **Publication and imports.** Pages has a dedicated paper job with an explicit wall
  ceiling. The overview, artifact dates, release metadata, published-site contract and
  import runbook include this standalone paper.

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
| 2 | W7: exact admission and historical projection | Initial 2026-10-07 collection: 270 current exact sides and 162 historical entries |
| 3 | W2 review of W1/W7: independent source, irreducibility and real-root checks | Correctness findings fixed; review retained |
| 4 | W7 **efficiency block**: exact interior-sign root comparisons | Full mathematical replay preserved; initial replay reduced to 31.67 s locally |
| 5 | W7: generated paper, site wiring and import documentation | Initial HTML/Markdown/PDF contracts implemented; current scope retains the web report and Markdown |
| 6 | W7 **efficiency block**: practical web reading (`think-mo36`) | Searchable index, lazy metadata and coefficient vectors; complete archives retained |
| 7 | W7: final checks, PR, delivery audit and replanning | Final validation is reported in the PR; unavailable earlier outputs remain an explicit dependency |
| 8 | W7: upstream integration and PDF storage maintenance (`think-okcb`) | Earlier 2026-10-08 checkpoint: 287 current exact values, 170 historical identities and 37 numeric routes; 13 original PDFs hosted outside Git and a universal 5 MiB tracked-PDF gate |
| 9 | W7: upstream CI contract repair | Rational refresh, hosted citation identity, publication payloads, snapshot custody, measured suite admissions and startup delay controls repaired; independent Astra review passed |
| 10 | W7: recovered stack, verified-bound identities and work map (`think-jygq`, `think-808n`) | Original 2026-10-08 A1 checkpoint: rebased both layers through the stacked-PR shortcut; 33 replay-backed rational identities projected without changing case bounds or proof status; four representation gaps then remained |
| 11 | W7: final publication input repair (`think-x0j9`) | The fresh catalogue job exposed a missing retained KKT-results leaf in its sparse checkout; keep that exact input and exercise the real Git include/exclude contract |
| 12 | W7: assembled publication contract (`think-wiu3`) | Original 2026-10-08 checkpoint: register 1,005 catalogue outputs by their exact exporter identities; reserve the 6 MB archive budget for its specific producer/path and bind approved scripts to retained source bytes |
| 13 | W7: complete PDF layout (`think-vore`) | Dated print-fit audit retained; further PDF packaging retired by the user on 2026-10-09 |
| 14 | W7 **efficiency block**: bounded receipt controls (`think-3okf`) | Separate four custody corruptions into independently named tests; each replays the full packet scan and checks its specific refusal within the unchanged per-test wall |
| 15 | W7: private snapshot copy contract (`think-3pyf`) | Copy each lexical source path once in both the worker and its live/Git inventories; omit only four unconsumed generated images and preserve their producers and dependency rescues under the unchanged 192 MiB cap |
| 16 | W7: concurrent source and storage reconciliation (`think-a0qb`) | Retain the independently reviewed parent extraction pin guard and lossless generated storage; preserve our later receipt controls and every decoded byte of the child’s larger register while updating all publication consumers |
| 17 | W7: hosted cost record (`think-a0qb`, `think-4kd6`) | Retain all three audited 106-step parent readings, including both over-ceiling observations, with geometric mean 135.17 s and spread 1.84×; keep the historical 88-step and child 108-step selections separate; PR 480 supplies the current temporary budgets under `think-2hm6` |

The two stack layers have separate registers.
At the earlier 2026-10-08 CI-repair checkpoint, PR 403 had 286 exact current values, one
degree-only value at $n = 83$, 37 numeric-only values and 18 legacy historical notes.
PR 435 supplied the $n = 83$ polynomial and full 170-entry historical collection.
Both retained 77 proved cases.
The verified refreshed parent and child partitions are recorded above.

At the later original A1 checkpoint on 2026-10-08, the parent had 319 exact identities,
one degree-only row and four numeric-only cases; the child had 320 exact identities and
the same four gaps, with 170 historical entries.
Those are pre-PR-434 observations, not the refreshed census.

The integration repair beads are `think-3y4q`, `think-uy3e`, `think-9sgi`, `think-kfpc`,
`think-qr37` and `think-s5ou`, under `think-okcb`. At that earlier checkpoint, the
snapshot repair omitted 312 unused historical output files (3,670,529 bytes), retained
declared evidence, source and replay inputs, and passed all 174 registered mutation
controls with the existing 192 MiB cap.
The expanded publication contract later exposed repeated copies of the same source path.
The copier and both inventories now share lexical path identity: each selected file has
one private writable copy, while distinct files with equal bytes remain distinct.
Four exact generated image leaves (387,934 bytes) leave the snapshot; their source files
and producers stay in Git, and a declared dependency rescues an image.
All prior scientific input paths remain selected.
The refreshed physical snapshot and full mutation run require final hosted checks.
Its headroom is narrow; `think-t1lk` owns dependency-based selection.
Local admissions retain the existing suite-cost observations and 10% unrecorded-share
limit.

The concurrent parent source update is retained in the stack’s ancestry.
At the original 2026-10-08 storage checkpoint, compression of the parent’s generated
exact-side register and chunk census preserved every decoded byte of those records.
The child’s `4dcddb7c` register contained all 324 current entries, then 320 exact
identities, and 170 historical entries.
Its 2,629,925 JSON bytes became 808,628 gzip bytes, with byte-for-byte decoded parity;
coefficients, attribution and proof status were preserved.
These are dated migration receipts.
The next recovery checkpoint stored 2,632,347 complete JSON bytes in 808,715 gzip bytes.
The pre-refresh source checkpoint stored 2,703,616 JSON bytes in 826,648 gzip bytes.
These are dated receipts; the refreshed register census is recorded above.
Bounded readers, the generated-JSON layout floor, schemas, census tools and publication
consumers all follow the maintained storage contract.
Published source links name the actual gzip file; logical JSON identities remain
available to the readers and plain test fixtures.
The matching-SVG-pin guard refuses an unpinned or mismatched source before record
writes.

The first D-shard record used two compatible 106-step parent observations, 166.59 s and
90.60 s, with geometric mean 122.85 s. That two-run record is historical.
The retained audited 106-step reference-shape cohort includes all three readings: 163.63
s, 166.59 s and 90.60 s, with geometric mean 135.17 s and spread 1.84×. Both slower
observations exceeded the unchanged 143 s ceiling and remain explicit evidence.
The historical 104.95 s reading selected 88 steps; the child’s 96.25 s reading selected
108 steps. Neither enters the 106-step cohort’s mean.
That historical calibration removed the pending fields that expired at midnight UTC and
kept its original enforcement policy.
PR 480 now supplies the current temporary 335-second D-shard ceiling and the 2026-10-09
cost record, as noted above.
Fresh final-head CI remains pending and must establish the reconciled source and storage
together.
The startup self-test verifies the injected 300 ms delay by requiring readiness
to trail both the delayed fixture’s math-runtime arrival and the fastest undelayed
control by at least 150 ms.
Final validation and publication identities are reported in the PRs.

At the original 2026-10-08 publication checkpoint, the lazy catalogue had 1,003 JSON
files, one browser script and one complete HTML archive in addition to its canonical
reader, Markdown and PDF. The retained inventories counted 1,005 renderer-owned site
registrations and 1,007 exporter-planned outputs.
These are dated output counts.
The dated registry contained 1,021 catalogue-owned outputs.
Full hosted physical snapshot validation subsequently passed on both published recovery
heads; exact-report PDF packaging was retired by the user on 2026-10-09. Site
registrations come from the exporter plan; unexpected names or owners remain refused.
The earlier live/Git snapshot inventory likewise recorded 6,467 paths and 195,613,428
bytes under the unchanged 192 MiB cap; it is a dated receipt, not a fresh inventory.
The complete HTML has a specific 6,000,000-byte budget, while ordinary HTML keeps its
2,000,000-byte cap. Executable payloads and large inline programs retain exact source
identity, approved path and individual byte budgets.

The earlier PDF preflight typeset displays at Letter’s content width and refused math
crossing its print column.
Its print-only implementation and build obligations are now retired.
The complete web report retains the equations and coefficient tables; current responsive
checks and final-head evidence are recorded in the PR.

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
| `think-ohhz` | 102, 106, 152, 172, 177, 199, 206, 207, 268, 297, 301 | Recover or reproduce all eleven claimed ideal-side identifications through `think-s6np`; the old 102 root is superseded and its current-pose route requires RyXu inputs; establish a confirmed KKT seed at 177; treat 199 and 207 as displaced branches |
| `think-056g` | 68, 103, 110, 123, 131, 132, 154, 155, 156 | Low-count ideal-side precision/degree sweep after the reusable driver is delivered by `think-s6np` |
| `think-d2kj` | 180, 181, 182, 208, 209, 210, 228, 236, 237, 238, 239, 240, 241 | Middle-count ideal-side sweep, same dependency; preserve current and displaced-side distinctions |
| `think-gg4k` | 259, 269, 270, 271, 273, 302, 303, 304, 305, 306, 307 | High-count ideal-side sweep, same dependency; preserve historical and source-invalid distinctions |
| `think-gl59` | 105 | Establish a current contact system and confirmed KKT seed |
| `think-hg9i` | 130 | Establish a current contact system and confirmed KKT seed |
| `think-uc8i` | 211 | Replace the batch’s bound-only value with a confirmed KKT seed |
| `think-is2e` | 263 | Replace the batch’s bound-only value with a confirmed KKT seed |
| `think-olv8` | 272 | Replace the batch’s bound-only value with a confirmed KKT seed |
| `think-w622` | 292 | Establish a current contact system and confirmed KKT seed; its finite rational refinement is already represented |

At the earlier upstream-integration checkpoint, 17 former numeric cases became certified
rational current values and left the numeric-only map.
Their contact and stationarity work stays open where it seeks an ideal algebraic packing
rather than the finite rational certificate.
In particular, `think-1atr` at 126, `think-hg9i` at 130 and `think-is2e` at 263 retain
their contact-system obligations.
`think-eu89` retains the original batch routing and KKT diagnostics; it does not define
the current numeric-only count.
A linear polynomial for a feasible witness side neither closes those research questions
nor proves optimality.
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

- **Driver assurance labels (`think-yuqy`).** Quarantine `probe_system_degree`,
  `probe_minimal_polynomial` and `probe_elimination` as candidate/export diagnostics
  before driver reuse.
  Their Bézout, bounded PSLQ and numerical-residual outputs cannot establish
  degree/coefficient lower bounds, exact ideal membership or real geometry.
  Preserve scoped search negatives and distinguish operational refusals from them.

- **Delivery recovery (`think-s6np`).** The original delivery audit found five commits
  and a generic producer named by closed `think-qgt4` and `think-ifc9` absent from that
  branch, remote deliveries and local worktrees.
  PR 403 then had four delivered commits; its originating Claude session was
  inaccessible. The eleven claimed ideal results remain unadmitted; the finite rational
  projection does not depend on those missing deliveries.
  This recovery has already retained the native $n = 11$ and $n = 102$ inputs from
  `evand/square-packing@13ee36e5807727d12a5da36b9b90a96bdba272bf` and checked them
  against `acquisition/upstream-subtree.sha256`. All 320 batch inputs are digest-pinned;
  only these two were selected for recovery.
  Their 476 and 5,305 bytes are retained in durable evidence outside disposable scratch;
  the source packet remains digest-only for these inputs.
  The undelivered W7 dependency is the reusable full-active-system driver with an exact
  half-angle export. It must retain the full active/weak/forced contact system, frozen
  variables, precision and residuals, and export exact polynomials with denominator
  exclusions. Generating digits from the known polynomial is only search calibration.
  After delivery, prove the known $n = 11$ octic from contacts as its control, then
  preregister one bounded $n = 102$ W6 slice in `think-ohhz`. This recovery has executed
  no solver, contact-derived control or bounded search.
  These two acquired inputs remain fixtures for the driver recovery.
  The retained $n = 102$ input describes Daniel’s older packing, whose claimed ideal
  root is now superseded.
  The current finite bound is RyXu’s arrangement at
  `8dc415296f697f5140caea27c7a0193d52deb4e6`, already retained in the
  [RyXu packet](../../../../packing/resources/web/ry-xu-new-packings-2026-10-08/README.md).
  Before a current-pose $n = 102$ slice, convert that complete certificate into the
  driver’s input, establish its active, weak and forced contacts, frozen variables and
  confirmed seed, and then preregister the bounded run.
  The historical Daniel input cannot satisfy that current-pose prerequisite; geometry or
  Lean work on its T-120 root is optional source-history work.

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

The selected next entry is **W7 `think-s6np` driver delivery**, followed by the known
$n = 11$ contact-derived control and then one bounded $n = 102$ W6 slice in
`think-ohhz`. The independent $n = 29,55,71$ elimination lanes can proceed in parallel;
the $n = 105$ system/seed lane remains ideal research.
Each experiment enters W6 with its own hypothesis and acceptance rule; a relation for an
ideal side must not replace a different finite certificate merely because their printed
decimals are close. The continuation epic stays open while these identification and
witness obligations remain.

## Stabilization Checkpoint, 2026-10-08

The recovery uses formal stack **447**: parent
[PR 403](https://github.com/jlevy/squares/pull/403), branch
`claude/friendly-sagan-jk7qzy`, then child
[PR 435](https://github.com/jlevy/squares/pull/435), branch
`codex/exact-polynomial-coverage`. Both incorporate upstream `main` at
`3213d651b880d7768bce8506efaf75c2089aeb4f`. The PR descriptions and recovery beads
record the current pushed heads and subsequent CI disposition; every result below names
the checkpoint it measured.
Both PRs remain open.
This recovery began at 2026-10-08 22:26:36.377 UTC; the elapsed cost checkpoints in
their descriptions cover one shared interval and must not be added.
No solver cost or identification result is claimed for this recovery.

### Repairs and Preservation

The parent repair checkpoint `910a7a4f2d46277e92515723aa40b4f3a73c9998` reconciles
standalone arithmetic tests with their later source-note assembly, the superseded
$n = 266$ case, retained compressed chunk readers and the declared negative-control use
of the reported source-root field.
Complete source-note equality remains checked separately.

The child publication/context repair was first committed at
`9763e6eefe2da7c1ec0d13dc641b7378b4c26a15`, then replayed onto that parent at
`1c335bb54b4a53c8d6899f3dadb7d1b0fb8c67c0`. It uses the authoritative paper roster for
all eight front-door cards, accepts a compressed Pages input only when both
representations are explicitly declared and a recognized data sibling exists, and adds
the retained reader to Pages push triggers.
The maintained collector regenerated historical relationship context: eight scalars
across seven rows changed after the finite-bound refresh; all source coefficients, 182
exact-check certificates, occurrences, flags and attribution remain identical.

The combined test retains all 15 selected counts and $n = 83$'s slow marker.
Source occurrences and the four appended source notes are checked at complete-record
assembly. Post-cascade verification passed **43 tests**, with the one slow $n = 83$
standalone case deselected, in **8.74 s**. The four assembled source-note entries are
compared in full and all 27 source-history controls passed.
Python 3.14 AST, Ruff, scoped BasedPyright and diff checks also passed.
No source or production adaptation was needed after conflict resolution.
At documentation checkpoint `6fa5d0524`, the selected $n = 83$ slow parity and complete
fresh-register equality tests both passed (27.36 s and 33.84 s; 65.30 s total).
The maintained register checker then verified all 321 irreducibility certificates and
321 isolated roots in 58.76 s. These mathematical controls ran under Python 3.14.7 and
changed no source or data.

The register remained byte-identical to both `9763e6eef` and `1666a7490`: 826,648 gzip
bytes, retaining every $n = 83$ coefficient, current identity, source-only note and
historical source payload.
The source/storage fixes from `086f29fc` and `470c8712` remain incorporated.
The primitive fractions and distinct display contracts at $n = 68,105,266,270,272,292$
remain those of the admitted primary inputs.
The four $n = 102,106,152,177$ roots remain **V0/C0**: geometry, Lean replay, packing
upper bounds and global optimality have not been admitted by these checks.

### Hosted Validation Disposition

Before the cascade, maintained mathematical replay checked 320 parent and 321 child
exact identities. Local repair controls passed 13 historical-collector tests, 30
downstream preservation tests and 37 publication controls, together with the parent
source-assembly and compressed-reader regressions.
Those establish the repaired components; final-head PR, Pages and full gates remain
required.

| Hosted checkpoint | Observed result | Disposition |
| --- | --- | --- |
| Parent `90266f785`, [PR run 37888714814](https://github.com/jlevy/squares/actions/runs/37888714814) | Eight math/storage assertions failed across fast A/B | Repaired locally in `910a7a4f2`; replacement-head gate pending |
| Child `1666a7490`, [PR run 37888715069](https://github.com/jlevy/squares/actions/runs/37888715069) | Inherited assertions plus paper roster and Pages input contracts failed | Captured repairs; replacement-head gate pending |
| Parent `90266f785`, [full run 37888858320](https://github.com/jlevy/squares/actions/runs/37888858320) | Integration failed on the eight known assertions and native frontier `1280-dark` CLS `0.2085927463531494 > 0.1`; eleven other jobs passed | Math/storage repaired; layout-shift finding remains open |
| Child `1666a7490`, [full run 37888861956](https://github.com/jlevy/squares/actions/runs/37888861956) | Integration failed on known contracts; slow lane refused stale historical context; ten other jobs passed | Context regenerated; replacement-head full gate pending |
| Parent `90266f785`, [Pages run 37888714728](https://github.com/jlevy/squares/actions/runs/37888714728) | Sixteen startup-limit failures | Remains open; cause has not been established |
| Child `1666a7490`, [Pages run 37888714875](https://github.com/jlevy/squares/actions/runs/37888714875) | Exact-paper, publish and `pages-required` jobs passed | Dated PDF inspected; small print type and final-head qualification remain open |

Both old-head hosted physical negative-control lanes passed all **174 selected
controls** in two private worker trees: parent snapshot 185.2 MiB, controls 289.68 s;
child snapshot 187.2 MiB, controls 437.24 s. Their combined three-step subsets passed in
491.79 s and 741.74 s respectively.
This is scoped fixture evidence, not a full-gate pass.
Failed behavioral shards made the PR wall summaries unmeasurable; the aggregate 312 s
and 331 s cannot determine compliance with or regression against the PR wall budget.
No assurance, startup, CLS, snapshot, JavaScript or tier ceiling was widened.

### Published Recovery Gates, 2026-10-09

The replacement published checkpoints are parent `910a7a4f2` and child `4789e36aa`. Both
automatic Packing gates and both full dispatched workflows passed.
These results qualify those source heads; later diagnostic or print changes need their
own gates.

| Published gate | Result | Scope |
| --- | --- | --- |
| Parent [Packing 37894154628](https://github.com/jlevy/squares/actions/runs/37894154628) | Passed | Replaces the eight repaired fast assertions |
| Child [Packing 37894154039](https://github.com/jlevy/squares/actions/runs/37894154039) | Passed | Repaired math, source, roster and retained-input contracts |
| Parent [full 37896687146](https://github.com/jlevy/squares/actions/runs/37896687146) | Passed; completed 07:38:05 UTC | 94 of 107 integration steps, 2,031.98 s under 3,600 s; 13 distributed steps and all prerequisite jobs passed |
| Child [full 37896690041](https://github.com/jlevy/squares/actions/runs/37896690041) | Passed; completed 07:36:26 UTC | 96 of 109 integration steps, 1,920.56 s under 3,600 s; 13 distributed steps and all prerequisite jobs passed |
| Child [Pages 37894154058](https://github.com/jlevy/squares/actions/runs/37894154058) | Passed | Fresh paper artifact 11599503887 generated; physical print readability still needs qualification |
| Parent [Pages 37894154719](https://github.com/jlevy/squares/actions/runs/37894154719) | Failed | Native frontier 1280-light CLS 0.2085927463531494 exceeds unchanged 0.1 guard |

The full workflows each passed all twelve prerequisite jobs and their aggregate.
The child slow lane passed all 184 tests.
Both new physical lanes passed all 174 selected negative controls in two private trees.
Their three-step subsets remain scoped evidence; the distributed full workflows supply
the full verdict. Integration used four CPUs, one outer job and two inner workers, so
these wall observations are not reference-shape speed comparisons.

The old dark-theme CLS failure did not recur in the new full runs, and the sixteen old
startup-limit failures did not recur in the new parent Pages run.
Neither observation establishes a causal repair.
The current parent Pages light-theme CLS failure remains open.
Controlled macOS prose-font and KaTeX-face delays did not reproduce it: PT Serif
released CLS ranged from 0.032885 to 0.078662; KaTeX-face delay measured 0.000501 in
both themes. Eleven maintained controls passed in 30.44 s, including two controls that
verify phase evidence survives a font refusal.
Production CSS and every existing budget remain unchanged; the same diagnostics need the
Linux regime before a layout candidate can be justified.

The dated
[print investigation](../../../../packing/benchmarks/exact-paper-print/ideas.md)
registered an 8-point physical readability criterion before CSS changes.
Its first candidate was refused: all 6,012 cells and 1,428 displays were checked, but
the exact fractions at $n = 68,292,105$ spilled 94.94, 26.05 and 15.45 pixels
respectively. No candidate PDF was generated or qualified.
The user then retired PDF packaging for this large catalogue and requested the same
content as a clean report on the Papers page.
`think-yon5` is canceled by that scope change; `think-ja78` owns complete web
publication. Preserve the dated negative result and cost, then remove print-only
implementation and build requirements.
No follow-up print experiment or PDF qualification belongs to the active scope.

### Publication Formats and Availability

The machine-readable table is the compressed JSON register, with complete normalized
integer coefficients, exact intervals, source references and verification status.
The website reader is HTML with search, filters and per-entry coefficient downloads.
The report is published as a responsive HTML catalogue and a complete HTML report, with
Markdown and complete coefficient downloads.
The user explicitly removed PDF packaging from this report’s scope on 2026-10-09 UTC.
Earlier public catalogue and PDF URL checks returned HTTP 404 because these PRs had not
merged. The successful child Pages checkpoint supplied Actions artifacts; deployment
still follows integration into `main`. The new web-only head must pass its own checks.

The web-only candidate on dirty `add30089a`, checked 2026-10-09, passed all eight views:
catalogue and complete report at 390/1280 pixels in both themes.
Document overflow, lost ink and math errors were zero; each complete view exposed all
321 current and 175 historical polynomial headings.
Independent reconstruction retained all 499 records, 519 vectors and 6,273 coefficient
strings.
Initial transfer was 366,952 / 5,357,841 bytes (6.849%, passing the explicit 10%
threshold); catalogue JavaScript was 21,988 / 24,000 bytes.
The 53 focused web tests and scoped language floors passed.
Protected receipts and eight screenshots preserve this candidate evidence; these checks
do not qualify the later rebased commit or its October 9 dateline.
No PDF was generated.
Final source-head CI remains required.

At clean child `1666a7490`, the maintained HTML-only build measured **362,534 bytes** of
initial transfer against **5,257,078 bytes** of complete HTML, a fraction
**0.06896112250950052**, passing the explicit 0.10 acceptance check.
The tool’s default 0.25 remains unchanged.
Reconstruction retained **499 records**, **519 coefficient vectors** and **6,273 integer
strings**, with 1,021 catalogue-owned outputs present.
The local ownership audit deferred the PDF, recording one expected omission.
The same-head hosted exact-paper artifact is `11597149165`, 5,194,737 bytes.
The preserved same-head PDF is **2,810,786 bytes / 546 Letter pages**, comprising 455
portrait and 91 landscape pages.
Metadata and representative inspection passed for the title, $n = 17$ equations, the
$n = 83$ heading and longest coefficient, and two dense summary tables; no clipping or
overlap was observed in those inspected pages.
Text extraction found **321 current polynomial headings and 175 historical headings**;
the three numeric-only current cases have no polynomial heading.
All **673 $n = 83$ coefficients** were reconstructed from PDF pages 400–492 and matched
the retained same-head JSON exactly, including a 724-digit integer on page 485. This is
a full $n = 83$ coefficient check, not an exhaustive PDF reconstruction of every other
vector. The landscape summary body measures about **5.4-point effective type**, which
remains a physical-print readability issue.
The producer log exposes no supported print-fit count or overflow summary; older such
measurements are not credited.
This dated PDF remains historical evidence; the active web-only report requires complete
web-content and responsive-rendering checks.

### Storage and Evidence Custody

At clean `1666a7490`, the read-only source inventory had **6,516 paths / 196,279,044
bytes**, identical between live and Git-selected sources, under the unchanged
**201,326,592-byte** cap with **5,047,548 bytes** of headroom.
It executed no physical copy or local negative controls.
Thirteen oversized original source PDFs are retained in the hosted
[source release](https://github.com/jlevy/squares/releases/tag/data/source-pdfs-v1) with
declared identities, byte sizes and checksums.

The external volume earlier had only 32 MB free, causing ENOSPC during local fixture
creation. On 2026-10-09 UTC it also became unmounted; macOS still detected the APFS
volume, which was remounted and checked writable before the paused rebase resumed.
It remained 99% used, with about 5.5 GiB free at that check.
Later readings at 07:26–07:30 UTC showed only 1.1–1.6 GiB free; the volume was mounted
and writable. Small diagnostics continued while local PDF and physical-fixture builds
stayed deferred. The cause of the unmount has not been established.
Disk-heavy fixtures and PDF builds remain hosted; scratch has no internal-disk fallback.
Source and unique evidence remain outside disposable scratch:

- Child source: `/Volumes/spud-ext1/agent-source/polynomial-catalogue-01a118e4`.
- Parent source: `/Volumes/spud-ext1/agent-source/polynomial-parent-01a118e4`.
- Protected receipts:
  `/Volumes/spud-ext1/agent-evidence/polynomial-catalogue-01a118e4/recovery-2026-10-08/`.
- Task environments: the corresponding directories under
  `/Volumes/spud-ext1/agent-scratch/`, each with `env.sh`, Python 3.14, explicit
  `TMPDIR`, `CARGO_TARGET_DIR`, `UV_CACHE_DIR` and separate Cargo targets.

### Next Slices and Tracking

Recovery remains open in `think-jygq`, coordination in `think-a0qb`, and latest-source
reconciliation in `think-wuol`. The bounded acquired corpus is preserved; CI
stabilization, web publication in `think-ja78` and the identification obligations remain
open. The retired print task is not a successful readability outcome.
Capture each new result against its actual head in the PRs and beads before continuing.

1. **W7 stabilization:** preserve the published full-gate checkpoint through stack 447,
   then qualify the maintained font diagnostics and complete web-only report.
   Keep parent Pages CLS open until its own controls pass.
   Preserve every equation, coefficient and source distinction at desktop/mobile widths
   in both themes. Exact-report PDF producer, preview, URL and format-link requirements
   are retired. Refresh pins and source-head gates after the upstream stack integration,
   and capture actual-head evidence on both PRs and the beads.
2. **W7 driver:** deliver `think-s6np` using the acquired $n = 11$ control and the
   historical Daniel $n = 102$ fixture, then derive the known $n = 11$ octic from active
   contacts as the exact control.
   No reusable driver, solver, contact-derived control or target search has been
   delivered in this recovery.
3. **W6 identification:** after the driver and $n = 11$ control pass, bind and convert
   the retained current RyXu $n = 102$ certificate, establish its contact system and
   confirmed seed, then preregister one bounded slice in `think-ohhz`. Keep
   $n = 29,55,71$ and ideal contact obligations open.
   Retain `think-yuqy`’s quarantine of unsupported degree, height and numerical-linkage
   inferences.

Pending finite-bound adoption remains in `think-lhtz`; T-128 source-house custody
remains in `think-0mlq`. The Rehwaldt $n = 68$ multivariate binding review remains in
`think-nv5o`; PR 479 completed the later extended-range source import, while
`think-1545` retains the outside-corpus reader work.
The optional $n = 83$ source-index count remains in `think-chsu`.

The adjacent import stabilization is recorded separately in
[PR 467](https://github.com/jlevy/squares/pull/467). Accepted upstream results are
incorporated; pending intake branches require qualification before import and have not
been absorbed into this stack.

## Validation and Acceptance

The push and PR run the project’s edit, reachable-test and fast surfaces.
The full register rebuild remains on the fast surface; the independent historical audit
runs at PR and records/full checkpoints.
Regressions include perturbed coefficients, a reducible polynomial, an alternate
conjugate, rational approximations substituted for radical forms, a destination-side
mismatch, inward-rounded error bounds, forged modular hints, and source flags or credits
taken from neighboring rows.
Verified-bound projection controls also refuse unequal fractions below displayed
precision, wrong source/count/evidence scope, stale or missing custody/replay inputs,
proved cases and replacement of existing algebraic identities.
The retained pre-refinement $n = 292$ control keeps outward-ceiling provenance distinct
from its native certificate side.

The canonical web page adds search, section/kind/status filters and pagination.
Individual records and exact coefficient strings load only when opened; numeric,
pending, source-invalid and outside-frontier rows keep their separate meanings.
Superseded rows remain in the raw register and are omitted from the visible web subset.
`think-r4rt` owns the export, `think-uunz` the browser and `think-3t5y` the independent
Astra review under `think-mo36`. The
[bounded measurement](../../../../packing/benchmarks/exact-catalogue-web/report.md)
checks the predeclared raw-byte threshold; complete archives preserve the full record.
The selected mathematical continuation remains W7 driver delivery in `think-s6np`.

The final full checkpoint exercises the shared case-record browser as well.
`think-gtyf` tracks synchronous case-popover close state, with a deterministic
regression and independent Astra review; final corrected-head validation is recorded in
the PR.

The paper checks completeness against the register, independent-series metadata, source
quotation handling, page construction, artifact dates and Pages scope.
The complete HTML report is checked with the pinned browser at desktop and mobile widths
in both themes, including long equations and coefficients.
All source data must reconstruct exactly.
This report’s build does not generate a PDF. Local and hosted outcomes, costs and final
commit identity are recorded in the PR. Pages publishes on merge; the current request
creates and reviews the continuation PR.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
