---
title: Frontier Assurance and Verification Plan
description: Plan to make every square-packing frontier claim explicit, replayable, and terminologically sound
author: Codex, for the project maintainers
---
# Feature: Frontier Assurance and Verification

**Date:** 2026-08-24 (last updated 2026-08-25)

**Author:** Codex, for the project maintainers

**Status:** Core implementation validated by the ordinary full gate; general
interval-existence promotion remains open

## Overview

Make the square-packing frontier effortless to read without weakening its mathematical
standards. A reader should be able to open one generated view and see, for every `n` in
the declared case-corpus range:

- the best upper and lower bounds reported by the public sources we track;
- the best upper and lower bounds supported by exact formal evidence;
- whether the optimum is proved;
- whether each formal result comes from a published proof or certificate, an independent
  external check, or a check replayed or audited here;
- what was numerically checked, by whom, with which arithmetic, precision, and
  tolerance; and
- any source conflict, missing evidence, unsupported importer, or stale review.

This distinction determines what the frontier can claim.
A published numerical record and a formally verified upper bound are both useful, but
they are not the same claim.
The frontier will retain both instead of promoting one into the other through optimistic
wording.

This plan also makes the verification toolkit reusable.
A full-geometry witness in a supported interchange format should be viewable and
numerically checkable without custom code.
Exact algebraic or rigorous interval evidence should be independently replayable.
When an approximate witness cannot be promoted, the result must name whether the missing
piece is public source data, an importer, a checker, or new mathematics.

This specification is temporary planning scaffolding.
By completion, every durable rule below must live in the appropriate definitive
document, schema, validator, or tool.
No normal workflow may need to cite this file.

## Goals

- Reserve bare **verified** for mathematically conclusive, exact or rigorously certified
  evidence whose assumptions have been discharged.
- Call every finite-precision calculation **numerically checked**. A tolerance of
  `1e-100` is still numerical evidence, not verification.
- Separate a public record claim from a verified upper bound, and separate feasible
  placement from global optimality.
- Record the assurance, method, origin, independence, precision, tolerance, certificate,
  and replay status as separate facts rather than compressing them into a tier name.
- Distinguish an external verification claim, an independently replayable external
  certificate, and a certificate replayed by this repository.
- Give new results one generic import, visualization, numerical-check, and
  certificate-replay path; source-specific adapters stop at the interchange boundary.
- Audit the whole packing exploration—not only the current frontier pages—against the
  new vocabulary and claim rules.
- Make document authority and lifecycle visible so an agent knows whether it is reading
  a definitive rule, current synthesis, historical record, review, or transient plan.
- Define a dated, reproducible public-source coverage process without pretending that an
  internet search proves universal completeness.
- Retain process checks only when they protect a named mathematical, reproducibility,
  navigation, or operational benefit.
- Keep the six workflow entry points and the campaign/session/experiment vocabulary
  consistent across the README, synopsis, campaign runbook, conventions, schemas, and
  artifacts.
- Keep this redesign under the explicit `general-improvement` fallback: it changes the
  assurance, data, documentation, and tooling framework and is not a W4 process review.

## Non-Goals

- Proving every open optimum or converting every numerical record into an exact witness.
- Promising that arbitrary floating-point coordinates can always be lifted to the
  reported value. Singular systems, missing contact data, ill-conditioning, and
  underdetermined models may prevent it.
- Treating proof-assistant checking as a prerequisite for every formal result.
  It is a separately reported, stronger trust-kernel property.
- Treating rigidity, local optimality, successful search, source reputation, decimal
  depth, or agreement between two floating implementations as a proof of feasibility or
  optimality.
- Inventing a new research-work vocabulary.
  The existing campaign, series, agent session, workflow phase, slice, hypothesis,
  experiment, round, run, result, and ledger definitions remain the basis.
- Editing archived source transcriptions or raw evidence to conform to current prose
  conventions. Their indexes and interpretations are in scope; source-faithful contents
  are not.
- Keeping checksums for Git-tracked sources merely because they already exist.
- Designing around one `n = 29` repository.
  That case is a regression fixture for a general contract.

## Background

The project already has the right broad architecture:

- [`README.md`](../../../../README.md) is the compact operating charter and entry point;
- [`SYNOPSIS.md`](../../../../SYNOPSIS.md) owns detailed current state, workflow
  contracts, terminology, and capability boundaries;
- [`frontier/`](../../../../packing/frontier/README.md) holds one structured case per
  `n`;
- [`campaign/`](../../../../packing/campaign/README.md) records hypotheses, experiments,
  sessions, and generated views; and
- [`resources/`](../../../../packing/resources/README.md) retains the primary-source
  archive.

The current data model nevertheless collapses facts that need to remain separate.
`SquarePackingCase/v1` has one `upper_bound`, a free-text `verified_here` list, and a
resource role named `exact_solution`. `Experiment/v1` uses `f64_screen`, `polished`, and
`exact` as a single `precision` tier.
Those fields cannot say whether a value is only reported, numerically checked, formally
certified by an external party, or replayed by this repository.
They also cannot distinguish arithmetic from assurance.

The audit that produced this plan found four concrete boundary cases.

1. The public Schadt `n = 29` repository checks decimal coordinates at tolerance
   `1e-100`. Its worst pair margins are slightly negative within that tolerance, and its
   checker accepts incomplete input.
   It is a useful numerical witness for a superseded record, not a formal certificate.
2. The retained Kingbird `n = 29` SVG is reconstructed at 160 decimal digits with a
   `1e-80` serialization tolerance.
   That supports a numerical structural observation, not exact feasibility or
   optimality. Its current `exact_solution` resource role and the “verified orientation
   classes” heading overstate the evidence.
3. The pre-change generic `NumberField` path did not itself establish irreducibility or
   unique root isolation.
   The implementation now requires an exact irreducible finite-field reduction or a
   complete supported-quartic factor-exclusion certificate, plus exact Sturm isolation.
   Unsupported declarations fail closed rather than inheriting verification from the
   built-in Trump `n = 11` path.
4. A July 2026 public source reports interval-verified improvements at several `n`,
   including `68` and `69`. The current `n = 68` and `n = 69` cases already retain those
   values and state that they have not been verified here; what is missing is typed
   evidence, a conflict or replay disposition, and access to the claimed certificate and
   checker. The result remains an external report pending source and replay adjudication.

Together, these cases identify the dimensions the general contract must represent.

## Design

### Approach

Use one claim register with reported and verified lanes on both sides of the bound.

**Reported upper bound** and **reported lower bound** preserve the strongest literal
claims found in the declared source coverage: value, wording, witness or theorem,
claimed method, and source.
They do not endorse the claim.

**Verified upper bound** and **verified lower bound** require exact formal evidence
under this plan’s definition.
A verified upper bound may equal the reported record, trail it, or be only the exact
grid construction. The grid fallback is one parametric theorem evidence
record—`s(n) ≤ ⌈√n⌉` for all finite `n`—referenced by each case rather than 100 copied
witness files.

A case is `proved` only when verified lower and upper bounds meet exactly.
A published proof may supply external verified evidence when the complete argument,
statement, scope, and assumptions are inspectable.
Its basis is shown as `published-proof`; it is not presented as audited here.
A local proof audit or certificate replay adds a separate repository evidence record
instead of overwriting the external one.
A citation that merely reports a theorem stays reported.

A feasible packing proves an upper bound only.
It does not prove that the packing is globally optimal.

Each displayed value points to typed evidence.
Tables are generated from the typed cases; prose explains context but cannot upgrade an
assurance state.

### Controlled Vocabulary

The project uses these assurance states.
`verified` has one mathematical meaning and several explicitly displayed origins; it
never means merely checked with small numerical error.

| Assurance | Meaning | Formal verification? |
| --- | --- | --- |
| `reported` | A named source states the claim; this record has not established it independently | No |
| `numerically-checked` | A finite calculation checked the stated inequalities under explicit arithmetic, precision, and tolerance | No |
| `verified` | An exact check, rigorous certificate, or complete mathematical proof decides the claim and every precondition is discharged | Yes |

The structured assurance value is `verified`; reader-facing displays also name its
origin, for example “published proof—not audited here,” “external certificate,”
“replayed here,” or “audited here.”
This qualification distinguishes trust and reproducibility without weakening the
mathematical meaning of verified.

The arithmetic or certification method is a separate field:

| Method | Required detail | Assurance it can support |
| --- | --- | --- |
| `numerical-f64` | implementation and tolerance | `numerically-checked` |
| `numerical-multiprecision` | implementation, actual decimal or bit precision, rounding policy, and tolerance | `numerically-checked` |
| `interval-certified` | outward-rounding implementation, input boxes, certificate, and replay command | `verified` |
| `exact-algebraic` | exact input representation, field or rational preconditions, certificate, and replay command | `verified` |
| `published-proof` | complete proof source, theorem statement, scope, pinpoints, and assumptions | external `verified` |
| `proof-audited` | theorem statement, scope, source pinpoints, assumptions, and independent proof audit | `verified` |
| `proof-assistant-checked` | proof object, theorem statement, kernel/toolchain, and replay command | `verified`, with the stronger mechanism named |

`polished`, `f64_screen`, `numerical-arbitrary-precision`, and “approximately verified”
are not current assurance terms.
“Polish” may describe an optimization operation in historical discussion, but never the
resulting evidence class.
“Arbitrary precision” may describe a library capability, but a result must state the
precision actually used.

Here **exact/formal** describes the logical conclusion, not necessarily a list of
symbolic point coordinates.
An outward-rounded interval certificate may verify a claim because it proves the
required inequalities or existence statement for an entire enclosure.
A decimal point evaluation remains numerical evidence regardless of its digit count.

Exact rational inputs use `exact-algebraic` as the degree-one case.
`published-proof` records the formal mathematical basis without implying a local audit;
`proof-audited` requires an independent audit record.
Neither applies to a citation that merely reports a theorem.

“Exact” must name its object: exact coordinates, exact predicate evaluation, exact
bound, or exact proof step.
An exact formulation solved by a floating LP remains a numerical result.

### Claim Types and Logical Consequences

Every evidence record names the claim it bears on:

| Claim type | What verification establishes | What it does not establish |
| --- | --- | --- |
| `witness-feasibility` | The supplied placement contains `n` non-overlapping unit squares | Best known status or optimality |
| `upper-bound` | `s(n) ≤ u`, normally derived from verified witness feasibility | A matching lower bound |
| `lower-bound` | `s(n) ≥ l` under the theorem’s stated scope | A construction at `l` |
| `exact-value` | Verified upper and lower bounds coincide exactly, establishing `s(n)` | Uniqueness or rigidity unless separately proved |
| `witness-optimality` | A separately verified feasible witness attains an already verified exact value | Uniqueness or the mechanism that forces the value |
| `derived-structure` | A named property such as orientation-class count or contact graph | Feasibility unless that is an explicit prerequisite |

Derived claims cite their prerequisites.
A numerical orientation-class check cannot silently inherit formal feasibility from the
phrase “record packing.”

### Evidence Record

`SquarePackingCase/v2` refers to evidence records with, at minimum, these independent
fields:

```yaml
id: E-n029-kingbird-numerical
claim: derived-structure
assurance: numerically-checked
method: numerical-multiprecision
performed_by: repository
relationship_to_generator: independent-implementation
source_key: "[Kingbird n=29 SVG]"
precision:
  decimal_digits: 160
  rounding: nearest
tolerance: "1e-80"
replay: uv run --frozen python -m cases.kingbird29.verify_svg resources/papers/kingbird-square-29-provenance.svg
replay_status: passed
limitations: Does not certify exact feasibility or optimality.
```

The final schema may normalize paths or identifiers, but it may not merge these
dimensions. In particular:

- `performed_by` distinguishes the source author, an independent external party, and
  this repository;
- `relationship_to_generator` says whether the checker shares the generator,
  implementation, or input derivation;
- `precision` and `tolerance` are required for every new numerical record and forbidden
  as substitutes for assurance;
- method-specific fields are omitted when they do not apply; null placeholders do not
  add information;
- a migrated historical record may use the literal `unrecorded-historical` only when a
  dated migration annotation says that the archived run did not retain the value; known
  values such as D-021’s `1e-11` solver floor are copied only where the source record
  supports them;
- a formal artifact is required for `verified` evidence: machine methods require a
  certificate and replay command, `published-proof` requires the complete proof source,
  theorem scope, pinpoints, and assumptions, and `proof-audited` additionally requires
  the audit record;
- every display of verified evidence identifies its origin as external, independently
  external, replayed here, or audited here;
- `replay_status` distinguishes `passed`, `failed`, `unsupported`,
  `public-certificate-missing`, and `not-attempted`; and
- a blocker names `source-evidence`, `importer`, `checker`, `field-precondition`, or
  `mathematics` rather than saying only “not verified.”

An external page that says “interval verified” without a public certificate or
replayable checker is recorded as `reported` with `reported_method: interval-certified`.
It becomes external `verified` evidence only when the formal object and its assumptions
are inspectable. A successful local replay adds a separate repository `verified` record;
it does not overwrite the external provenance.

The campaign invariant survives the v2 migration: `beat_record: true` requires
`assurance: verified`. A numerically checked candidate may record that it improves a
numerical comparator, but it cannot become the formal frontier record through that flag.

### Frontier Case Contract

`SquarePackingCase/v2` replaces the ambiguous v1 fields with five explicit sections:

1. `reported_upper_bound`: literal value, source date, retrieval date, claimed method,
   witness references, and evidence summary;
2. `verified_upper_bound`: exact value or outward-rounded bound, formal evidence
   reference, and derivation from a verified witness-feasibility claim;
3. `reported_lower_bound`: literal value, theorem claim, source, and stated scope;
4. `verified_lower_bound`: exact value or rigorous bound, proof or certificate evidence
   reference, theorem scope, and verification origin; and
5. `evidence`: typed reports, numerical checks, and formal verification records, plus
   conflicts and unresolved replay blockers.

Decimal values that carry identity or precision remain strings.
Machine numeric fields are derived conveniences, never the authoritative representation.
The contract rejects—through the schema where expressible and the semantic checker for
cross-field rules, following the existing softschema split:

- `status: proved` without matching verified bounds;
- a numerical method paired with `assurance: verified`;
- a verified record without the formal artifact required by its method;
- new numerical evidence without its actual precision and tolerance, or historical
  unknowns without the required dated migration annotation;
- `exact_solution` on a serialized numerical witness;
- an upper-bound implication from a derived-structure check;
- `beat_record: true` without `assurance: verified`; and
- a claim that local tooling reproduced external evidence when only the same source
  program was rerun.

The generated frontier view shows reported and verified upper and lower bounds side by
side. It also shows verification origin, last source review, and any unresolved conflict
or tool gap. Detail stays on the per-`n` page.

### External Replay Outcomes

Every full-geometry external result in scope receives one of these dispositions:

| Disposition | Frontier treatment |
| --- | --- |
| Formal certificate passes externally and here | retain separate external and repository `verified` evidence |
| External formal certificate exists but the local importer/checker is unsupported | retain external evidence; name the local tooling gap |
| Source asserts formal verification but publishes no replayable certificate | retain as `reported`; name the source-evidence gap |
| Witness is only numerical and passes a local numerical check | retain both source report and `numerically-checked` evidence |
| Local replay rejects the witness or certificate | show a conflict and require independent adjudication before promotion |

Every witness gets a recorded disposition; source reputation alone supplies none.

### Verification Capability Ladder

The synopsis will maintain a current capability table with four states: built and sound,
built with a named precondition, buildable engineering, and mathematically contingent.

At the time of this plan:

| Capability | Current classification | Required work |
| --- | --- | --- |
| Recompute containment and pair margins from supported decimal poses | built, numerical only | expose through the generic witness path and require precision/tolerance |
| Verify rational witness data exactly | substantially built | add interchange, certificate output, and controls |
| Verify the built-in Trump algebraic witness | built and sound for that named witness | retain independent field and root checks |
| Verify supported `NumberField` input | built and sound for accepted declarations | require a modular or complete supported-quartic irreducibility certificate plus exact unique-root isolation; reject unsupported declarations |
| Import arbitrary center/angle or corner witnesses | partially built, source-specific | define one interchange format and thin adapters |
| Prove a nearby relaxed upper bound from a robust numerical pose | buildable engineering for many poses | rationalize rotations and coordinates, add explicit safety margin, verify exactly |
| Certify existence near a contact solution at the reported value | mathematically contingent | interval Newton/Krawczyk or algebraic root isolation with outward rounding |
| Derive the correct contact model from an arbitrary SVG | mathematically contingent | expose ambiguity; do not guess silently |
| Prove global optimality from a feasible witness | not an automatic conversion | requires an independent matching lower-bound argument |

The `buildable` label means that the engineering path is understood; it does not promise
success on every witness.
A promotion tool returns a certificate or a typed failure.
It never turns a convergence heuristic into a proof.

The generic witness toolkit supports two useful promotion attempts:

1. **Robust exactification:** convert decimals and rotations to exact rational or
   algebraic data, introduce an explicit side relaxation if needed, and verify the
   resulting placement exactly.
2. **Existence certification:** use rigorous intervals around a numerical contact
   solution to certify that an exact feasible solution exists in the box.

The first may certify a slightly weaker upper bound.
The second may preserve the reported value but needs a suitable, well-conditioned
system. Both report failure without changing the original numerical evidence.

### Public-Source Coverage and Freshness

Coverage is a dated claim over a named source set, not a claim to have exhausted the
web. The frontier records:

- the source registries and first-party result pages reviewed;
- the `n` range each source covers;
- the last successful review date and source revision or page date when available;
- the case-corpus horizon, initially and explicitly `1 <= n <= 100`;
- relevant claims beyond that horizon in the source-coverage inventory; and
- missing local source material, conflicting values, and unresolved newer claims.

Completion requires a case for every `n` through 100 and a disposition for every result
found in the named primary-source set.
A beyond-horizon result can live in the coverage inventory until extending the case
corpus has a reader or research use; the known Kingbird range through at least `n = 324`
does not by itself justify 224 mostly empty case files.

Coverage state belongs in validated data.
Beads track actionable work units—one source sweep, one conflict class, or one tooling
blocker—not every `n` whose state is already represented in that data.
This keeps omissions visible without turning the issue tracker into a second frontier
database.

Search-engine discovery can suggest sources, but promotion uses first-party pages,
papers, repositories, or author-supplied data.
A source conflict remains visible until adjudicated; the latest date alone does not
decide mathematical validity.

### Source Identity Without Ceremony

Git history, a stable local path, the source URL, and a retrieval date identify a
first-party document retained in this repository.
An additional SHA beside that file does not strengthen the mathematical claim and will
be removed.

A digest remains only when it performs a named mechanical function already used by a
consumer, such as:

- comparing two independently retrieved byte streams across a real trust boundary;
- providing the stable identity that an existing deduplication or append-only event
  consumer actually indexes; or
- carrying a dependency checksum supplied by a lockfile across the package-download
  trust boundary.

The field or nearby documentation names that function.
“Provenance” alone is not a sufficient reason.
Reader-facing digest restatements and checks that merely bind one Git-tracked source
file to itself are removed, along with process tables that exist only to record those
hashes. Where a replay checker duplicates source data in code, parsing the retained
source is preferred.
No implementation-owned source digest is retained by this change.
Hashes embedded in an unedited first-party source snapshot remain source content; this
repository neither repeats nor consumes them as mathematical evidence.

### Workflow and Process Discipline

This plan is a `general-improvement` framework redesign, not a W4 process review.
It changes mathematical assurance, data contracts, reader surfaces, tools, and only the
process needed to keep those parts coherent.

The six workflow entry points remain W1 research pass, W2 factual review, W3 insight
iteration, W4 process review, W5 efficiency loop, and W6 research loop.
For routine single-purpose work, choosing an entry point is a lightweight routing
decision: record the workflow, objective, intended artifact, and focused check where the
work is already tracked.
Do not create a second artifact merely to restate those facts.

Escalate to `AgentSession/v2` only for multi-phase work, long autonomous supervision,
independently tracked coordination, expensive experiment or proof supervision, or a
consequential recovery handoff.
An orchestrator may then switch workflows inside that session; each material switch
starts a declared phase with its own focus, output, clock, and stopping condition.
The generated session and ledger views summarize those escalated histories, not every
routine task.

The work-unit meanings remain:

- a **campaign** is the durable multi-session scientific effort;
- a **series** is a campaign-wide tooling and comparability boundary;
- an **agent session** is one bounded interval of orchestrated work;
- a **workflow phase** is one contiguous purpose and focus inside that session;
- an **experiment** is the durable artifact for one preregistered **round**;
- a **round** is the bounded research work recorded by that experiment; and
- a **run** is one invocation or trial inside a round.

The synopsis owns the full definitions.
Other docs link to it and use a compact table; they do not create competing definitions.

Process additions must answer two questions: what failure does this prevent, and what
artifact or check demonstrates that benefit?
If neither answer is concrete, do not add the process.
Repetition alone does not justify a schema field, digest, table, or gate.
Correctness requirements do not become optional when they are expensive, but process
controls remain proportional to consequence, recovery cost, and demonstrated failure.
When a consequential rule is broken and nothing detects it, add the smallest useful
check that would prevent the recurrence.
There is no standing goal to mechanize every written convention.

### Durable Documentation Map

The implementation adds one validated `DocumentMap/v1` source under `docs/project/`. It
maps each durable prose document to its role, authority, lifecycle, and supersession
target when applicable.
It lists the small set of standalone project documents individually and covers
homogeneous artifact directories through their governing schema.
The synopsis renders its document table from that source; there is no second
hand-maintained map.

The map prevents two practical failures: agents entering through a historical review as
if it were current policy, and a current claim living only in a transient spec or
handoff.
It does not duplicate titles, summaries, dates, or evidence already owned by the
documents.

| Surface | Durable authority after implementation | Required migration |
| --- | --- | --- |
| `README.md` | core assurance rules, compact workflow selector, reader entry points | state “verified” and “numerically checked” rules; link the current frontier and synopsis |
| `SYNOPSIS.md` | full terminology, capability/gap ladder, verification process, workflow transitions, current technical state | replace tier language; explain reported versus verified frontiers and merge the capability ladder into “What Is Built” |
| `TUTORIAL.md` | first-use path through the tools and record | update examples to use inspect, check, and verify with their exact meanings |
| `conventions.md` | ids, schemas, field rules, and objective checks | remove “every convention becomes a check”; retain only checks with a named benefit |
| `frontier/README.md` | frontier semantics, coverage scope, reader and contributor workflows | document v2 case/evidence contracts, source conflicts, replay outcomes, and generated views |
| `frontier/n-*.md` | one typed claim register per `n` | migrate every case, reclassify every witness, and remove free-text assurance ambiguity |
| `campaign/README.md` | W6 mechanics | adopt the assurance/method split without duplicating synopsis definitions |
| campaign schemas and artifacts | typed historical and current research record | migrate precision fields and annotate unsupported historical verdicts without rewriting raw results |
| `resources/README.md` and source indexes | source retention and reconstruction policy | remove redundant checksum requirements; state the real trust-boundary exceptions |
| research reports | current evidence syntheses or explicitly superseded analyses | map lifecycle; correct assurance claims and link corrections or capability status without blanket restyling |
| reviews, handoffs, postmortems, and active plans | dated historical or transient records | map lifecycle; correct dangerous current-sounding claims in place or add explicit supersession notes |
| probe and component READMEs, including `frankensim-probe/README.md` | local component scope and reproducible use | map lifecycle and audit every assurance or capability claim |
| packing-local contributor instructions | agent entry discipline | require common-doc review and the authoritative assurance vocabulary without editing tbd-managed root `AGENTS.md` directly |

Every durable document is mapped and receives the common-doc footer and applicable
lifecycle information.
The definitive reader and operator surfaces—README, SYNOPSIS, TUTORIAL, conventions, and
the frontier, campaign, and resources READMEs—receive the full editorial pass during
Phase 1. Historical reviews, handoffs, postmortems, reports, and plans receive targeted
assurance corrections and supersession notes; broader editing rides along when
substantive work touches them.

Objective checks cover footer presence, local-link validity, complete document-map
coverage, schema conformance, and generated-view freshness.
Terminology lint targets retired current machine tokens such as structured `polished`
and `f64_screen`, `role: exact_solution`, and “approximately verified.”
Legitimate semantic uses of “exact,” “verified,” or historical “polish” remain an
editorial question, not a global word-lint.

Historical quotations or raw source text may contain old terms.
A validator exception must be scoped to an explicitly marked quotation or archival path,
never to a whole current document.

### Schema and API Changes

The implementation introduces or revises these contracts:

- `packing.squares:SquarePackingCase/v2` for reported and verified upper and lower
  bounds;
- `packing.squares:FrontierEvidence/v1` for typed evidence and replay status;
- `packing.squares:Witness/v2` for center/rotation or corner geometry with explicit
  units, coordinate convention, literal values, and source references;
- `packing.squares:Experiment/v2` for assurance, method, actual precision, and
  tolerance;
- `packing.squares:DocumentMap/v1` for document authority and lifecycle; and
- generated frontier and documentation-map views checked against their source data.

The exact file split is an implementation choice.
The logical contracts and validation rules are not.

New structured artifacts use v2 from the change that lands the v2 validator.
Existing v1 artifacts may remain only on a dated migration allowlist while Phase 1 is in
progress; Phase 1 cannot complete until current v1 artifacts are migrated and the
validator rejects new or unlisted v1 input.
Raw historical source material is not rewritten.

One public command family accepts a witness and can:

```text
inspect       render and summarize the geometry without making an assurance claim
check         recompute constraints numerically under a named method and tolerance
verify        replay an exact algebraic or interval certificate
promote       attempt robust exactification or existence certification
```

Commands return nonzero on malformed input, unsupported input, failed checks, or failed
verification. Machine output carries the same status and limitations as the frontier;
human output never prints `VALID` for an incomplete record.

## Implementation Plan

Every implementation bead linked to this spec belongs to the frontier-transparency epic,
`think-wfz1`. Existing beads are reused when they already own the work.
The current issue graph is generated by:

```bash
tbd list --spec plan-2026-08-24-frontier-assurance-and-verification.md --pretty
```

The spec does not duplicate mutable bead statuses.

This plan owns the public witness interchange, evidence contracts, `inspect`/`check`/
`verify`/`promote` semantics, and the general exact-or-interval promotion path.
The [minimal packing toolkit plan](plan-2026-08-22-minimal-packing-toolkit.md) owns
search, quench, basin identity, atlas runtime, and the low-level verifier
implementation.
The work is shared rather than duplicated: toolkit bead `think-0md2` owns
the certificate type, `think-kmwb` owns exact corpus re-verification, and `think-2lyb`
owns the unavoidable-set `PoseBox` proof hook.
This plan consumes those outputs through `think-q7d0` (public witness path),
`think-75ll` (promotion and typed outcomes), and `think-rsxe` (generic algebraic
preconditions).

### Phase 1: Establish the Contract and Migrate the Current Record

- [x] Land the controlled vocabulary and logical implications in README, synopsis,
  tutorial, conventions, frontier README, campaign runbook, component READMEs, and
  resource policy.
- [x] Add the v2 case, evidence, experiment, witness, and document-map contracts with
  cross-record semantic validation.
- [x] Generate a reader-first frontier table with reported and verified upper and lower
  bounds, verification origin, status, conflict, and freshness.
- [x] Script the v1-to-v2 migration of all current `n = 1..100` cases, compare it with a
  fresh source reparse, and direct human or agent scrutiny to cases with local evidence,
  conflicts, or `verified_here` entries rather than hand-transcribing 100 files.
- [x] Migrate current campaign artifacts without rewriting raw measurements.
  Preserve unrecorded historical precision or tolerance explicitly and use named defects
  or revision notes for invalid historical conclusions.
- [x] Correct the `n = 29` source roles and wording.
  Exp-012 remains a 160-digit numerical check; H-024 becomes unresolved under its
  original exact prerequisite or is superseded by a precisely numerical successor claim.
- [x] Audit assurance claims in current prose.
  Automate retired structured tokens and exact deprecated phrases; review contextual
  mathematical words editorially.
- [x] Remove reader-facing Git-source digests.
  Retain, replace, or remove each embedded-transcription staleness pin according to its
  named failure and document every retained pin.
- [x] Add the durable documentation map, generate the synopsis view from it, and map
  every project document.
  Complete the full common-doc pass on definitive docs; apply lifecycle labels and
  targeted assurance corrections to historical or transient docs.

**Done when:** all existing structured artifacts validate under the new schemas; no
current prose blurs numerical and formal evidence; every project doc has an authority
and lifecycle; and the `n = 29` regression fixture displays only claims its public data
and local checks support.

### Phase 2: Complete Source Coverage and the Reusable Replay Path

- [x] Audit the named primary-source set and record conflicts and review dates.
  Keep the case corpus complete through the declared `n = 100` horizon and record
  relevant beyond-horizon claims in the source inventory.
- [x] Adjudicate the July 2026 `n = 68` and `n = 69` claims and any other newer results;
  do not promote an inaccessible certificate or expose held-out child geometry before
  preregistered H-030 is settled or versioned.
- [x] Build the witness interchange format, source adapters, viewer, and independent
  numerical checks for `numerical-f64` and `numerical-multiprecision`.
- [x] Attempt local replay for every external full-geometry witness in scope and record
  one of the defined dispositions.
- [x] Make rational and algebraic verification emit replayable certificates, and close
  the generic number-field precondition gap before calling that path verified.
- [x] Add exact rational robustification for suitable numerical poses, with any side
  relaxation explicit in the resulting bound.
- [x] Keep the source archive and frontier linked without duplicating file hashes or
  silently editing source-faithful material.

**Done when:** every result in the declared source set and horizon is represented, every
available geometry has a replay disposition, and a new supported witness can be
inspected and numerically checked without case-specific verifier code.

### Phase 3: Add Formal Promotion and Make the Contract Continuous

- [ ] Implement and independently test an outward-rounded interval-certificate path for
  suitable contact systems.
- [x] Attempt formal promotion of the highest-value unverified records, retaining exact
  certificates, slightly relaxed verified bounds, or typed blockers.
- [ ] Add small independent certificate checkers and negative controls for containment,
  overlap, field metadata, interval rounding, incomplete input, and false optimality
  promotion.
- [x] Make schema, semantic, generated-view, document-map, terminology, and link checks
  part of the normal packing validation path at the cheapest useful cadence.
- [ ] Re-run the complete claim and common-doc audit after migrations, then move this
  plan out of `active/` once every durable rule has an authoritative home.

**Done when:** formal evidence can be replayed without the search or source generator;
failed promotions leave explicit source, tooling, or mathematical blockers; current
status is regenerated from validated records; and no definitive behavior depends on this
transient spec.

## Testing Strategy

### Schema and Whole-Set Invariants

- Every frontier case, evidence record, witness, experiment, and documentation-map entry
  validates against its declared contract.
- Every `n` through the declared case-corpus horizon occurs exactly once; beyond-horizon
  source claims have an inventory disposition without requiring empty case files.
- `proved` requires exact equality between verified lower and verified upper bounds.
- Every new numerical record declares method, actual precision, and tolerance; a
  historical unknown carries the sentinel and dated migration annotation.
- Every verified record declares a supported formal method and its required formal
  artifact: a machine certificate and replay command, a complete published proof, or a
  fully scoped proof plus independent audit record.
  Its origin is visible.
- `beat_record: true` requires `assurance: verified`.
- Every result and certificate reference resolves; every generated table is current.
- Every durable project document is mapped; raw archival paths are explicitly excluded.

### Verification Controls

- Exact contacts pass exact or rigorous interval checks and are not accepted through a
  numerical tolerance loophole.
- Perturbations on both sides of zero distinguish feasible, infeasible, and unresolved
  interval cases.
- Missing squares, duplicate ids, malformed angles, non-unit rotations, and truncated
  files fail with nonzero status.
- A field with a reducible polynomial or ambiguous root interval is rejected before
  algebraic sign evaluation.
- A certificate replays without the search engine, original optimization process, or
  network access.
- A numerical witness can be retained after a failed formal-promotion attempt without
  having its assurance upgraded.

### Regression Cases

- The Schadt `n = 29` repository is shown as a superseded numerical record; tolerance
  `1e-100` never renders as verification.
- The Kingbird `n = 29` SVG is numerically checked at the recorded 160 digits and
  `1e-80`; its six-class observation is not presented as exact until a formal
  certificate exists.
- The built-in Trump `n = 11` witness remains verified because its field assumptions are
  discharged; arbitrary generic fields do not inherit that status.
- A reported external interval result without a public certificate stays reported.
- One parametric exact grid theorem gives every case a verified fallback upper bound.

### Documentation Review

The objective gate checks footer, mapping, links, retired machine tokens, and generated
content. It does not word-lint legitimate mathematical uses of “exact” or “verified.”
The editorial pass then applies the common documentation guidelines to every durable
Markdown file changed or reclassified, with special attention to:

- reader-first conclusions before mechanism;
- one authoritative home per rule;
- explicit scope, uncertainty, and supersession;
- no ceremonial tables, hashes, or fields without a named use; and
- preservation of source-faithful and historical evidence.

The current focused and complete gates are:

```bash
uv run --frozen --group dev packing-validate --fast
uv run --frozen --group dev packing-validate
uv run --frozen --group dev packing-validate --strict
```

New focused checks join these commands rather than creating an undocumented parallel
gate.

The 2026-08-25 implementation checkpoint passes the ordinary full gate, including its
behavioral tests, exact witness replays, complete frontier, structured datasets,
document map, mutation controls, and 20,000-pair differential check.
The validation command and generated views own their live inventory; this transient plan
does not copy counts that change whenever a document or focused check is added.
The generic interval-existence certificate remains planned work rather than an implicit
prerequisite or a claimed capability.

## Rollout Plan

Implementation lands as successive PRs on the current square-packing stack.
As lower PRs merge, the next PR merges the new stack tip and retargets without changing
the ownership boundaries above:

1. this plan and its bead map;
2. the integrated vocabulary, schema, corpus, source-coverage, documentation-map,
   witness, exact-promotion, and semantic-gate implementation;
3. a later interval-existence implementation only after its certificate format and
   independent trusted core are reviewed.

Each PR is internally consistent and passes the full existing test suite.
A schema migration and the artifacts it governs land together; the repository never has
a state where old artifacts appear to satisfy a new contract.

Historical numeric results are preserved.
Corrections use named defects, revised verdicts, or explicit supersession rather than
deleting inconvenient measurements.
Generated views are replaced atomically with their source changes.

When the final phase lands, the durable rules live in README, synopsis, conventions,
frontier and campaign runbooks, schemas, and tool help.
This plan moves from `active/` to the project’s completed-spec location or is otherwise
marked implemented according to the repository’s spec lifecycle.

## Open Questions

- Will the authors of the July 2026 interval claims publish their certificates and
  checker, or must those entries remain external reports?
- Which smallest interchange representation supports both center/rotation sources and
  corner/polygon sources without making source adapters mathematically interpret
  ambiguous geometry?
- Which interval library and certificate shape produce the smallest independently
  checkable trusted core for contact systems?
- For which numerical records can rational robustification certify a useful nearby upper
  bound without deriving a contact model?
- Should proof-assistant replay become a later evidence method for selected landmark
  cases, after the independent exact and interval checkers are stable?

None of these questions changes the assurance vocabulary or permits an unsupported
promotion while it is unresolved.

## References

- [Packing exploration README](../../../../README.md)
- [Packing synopsis](../../../../SYNOPSIS.md)
- [Packing conventions](../../../../conventions.md)
- [Frontier map](../../../../packing/frontier/README.md)
- [Campaign runbook](../../../../packing/campaign/README.md)
- [Minimal packing toolkit plan](plan-2026-08-22-minimal-packing-toolkit.md)
- [Unattended research readiness plan](plan-2026-08-23-overnight-cartography-run.md)
- [Schadt `n = 29` repository](https://github.com/BalthasarStrauss/Squares-packing_S-29-_New-Record)
- [Kingbird square-packing catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
- [July 2026 UnitSquare results](https://www.hmbelvedere.com/)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
