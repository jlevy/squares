---
title: Frontier Assurance and Verification Plan
description: Plan to make every square-packing frontier claim explicit, replayable, and terminologically sound
author: Codex, for the project maintainers
---
# Feature: Frontier Assurance and Verification

**Date:** 2026-08-24 (last updated 2026-08-24)

**Author:** Codex, for the project maintainers

**Status:** Draft

## Overview

Make the square-packing frontier effortless to read without weakening its mathematical
standards. A reader should be able to open one generated view and see, for every `n` in
the declared coverage range:

- the best result reported by the public sources we track;
- the best upper bound that has actually been certified;
- the best proved lower bound;
- whether the optimum is proved;
- what was checked, by whom, with which method, precision, tolerance, certificate, and
  replay command; and
- any source conflict, missing evidence, unsupported importer, or stale review.

This distinction determines what the frontier can claim.
A published numerical record and a certified upper bound are both useful, but they are
not the same claim.
The frontier will retain both instead of promoting one into the other
through optimistic wording.

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
- Separate a public record claim from a certified upper bound, and separate feasible
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
- [`frontier/`](../../../../frontier/README.md) holds one structured case per `n`;
- [`campaign/`](../../../../campaign/README.md) records hypotheses, experiments,
  sessions, and generated views; and
- [`resources/`](../../../../resources/README.md) retains the primary-source archive.

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
3. The generic `NumberField` path does not itself establish irreducibility or unique
   root isolation. The built-in Trump `n = 11` path discharges those assumptions, but an
   arbitrary caller cannot yet treat the generic algebraic path as an unconditional
   verifier.
4. A July 2026 public source reports interval-verified improvements at several `n`,
   including `68` and `69`, while the current Kingbird page retains older values.
   The public result page found during this review does not expose the claimed interval
   certificate and checker in a replayable form.
   The conflict belongs in the frontier as an external report pending source and replay
   adjudication, not as either silence or a local verification.

Together, these cases identify the dimensions the general contract must represent.

## Design

### Approach

Use one claim register with two reader-facing frontier columns.

**Reported best** is the strongest current upper-bound claim found in the declared
source coverage. It preserves the source’s literal value, wording, witness, and claimed
method without endorsing them.

**Certified upper bound** is the best placement whose feasibility has been verified
under this plan’s definition.
It may equal the reported best, trail it slightly, or be only the exact grid
construction.
A certified upper bound is never absent: the trivial grid supplies a formal
fallback for every finite `n`.

The proved lower bound remains separate.
A case is `proved` only when a verified lower bound and a certified upper bound meet
exactly. A feasible packing proves an upper bound only.
It does not prove that the packing is globally optimal.

Each displayed value points to typed evidence.
Tables are generated from the typed cases; prose explains context but cannot upgrade an
assurance state.

### Controlled Vocabulary

The project uses these assurance states:

| Assurance | Meaning | May bare “verified” be used? |
| --- | --- | --- |
| `reported` | A named source states the claim; this record has not established it independently | No |
| `numerically-checked` | A finite calculation checked the stated inequalities under explicit arithmetic, precision, and tolerance | No |
| `verified` | An exact check, rigorous certificate, or complete audited proof decides the claim and every precondition is discharged | Yes |

The arithmetic or certification method is a separate field:

| Method | Required detail | Assurance it can support |
| --- | --- | --- |
| `numerical-f64` | implementation and tolerance | `numerically-checked` |
| `numerical-multiprecision` | implementation, actual decimal or bit precision, rounding policy, and tolerance | `numerically-checked` |
| `interval-certified` | outward-rounding implementation, input boxes, certificate, and replay command | `verified` |
| `exact-algebraic` | exact input representation, field or rational preconditions, certificate, and replay command | `verified` |
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
`proof-audited` is for a complete mathematical argument, not for a citation that merely
reports a theorem.

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
| `exact-value` | Verified upper and lower bounds coincide exactly | Uniqueness or rigidity unless separately proved |
| `optimality` | No smaller container is possible | Uniqueness or a particular mechanism |
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
tolerance: "1e-80"
certificate: null
replay: uv run --frozen python tools/check_kingbird_svg.py
replay_status: passed
limitations: Does not certify exact feasibility or optimality.
```

The final schema may normalize paths or identifiers, but it may not merge these
dimensions. In particular:

- `performed_by` distinguishes the source author, an independent external party, and
  this repository;
- `relationship_to_generator` says whether the checker shares the generator,
  implementation, or input derivation;
- `precision` and `tolerance` are required for every numerical method and forbidden as
  substitutes for assurance;
- a formal artifact is required for `verified` evidence: machine methods require a
  certificate and replay command, while `proof-audited` requires the proof source,
  theorem scope, pinpoints, assumptions, and audit record;
- `replay_status` distinguishes `passed`, `failed`, `unsupported`,
  `public-certificate-missing`, and `not-attempted`; and
- a blocker names `source-evidence`, `importer`, `checker`, `field-precondition`, or
  `mathematics` rather than saying only “not verified.”

An external page that says “interval verified” without a public certificate or
replayable checker is recorded as `reported` with `reported_method: interval-certified`.
It becomes external `verified` evidence only when the formal object and its assumptions
are inspectable. A successful local replay adds a separate repository `verified` record;
it does not overwrite the external provenance.

### Frontier Case Contract

`SquarePackingCase/v2` replaces the ambiguous v1 fields with four explicit sections:

1. `reported_best`: literal value, source, source date, retrieval date, method of
   discovery, witness references, and evidence summary;
2. `certified_upper_bound`: exact value or outward-rounded bound, certificate evidence
   reference, and derivation from a witness;
3. `proved_lower_bound`: exact value or rigorous bound, theorem scope, source, and
   evidence reference; and
4. `evidence`: typed checks and verification records, plus conflicts and unresolved
   replay blockers.

Decimal values that carry identity or precision remain strings.
Machine numeric fields are derived conveniences, never the authoritative representation.
The schema rejects:

- `status: proved` without matching verified bounds;
- a numerical method paired with `assurance: verified`;
- a verified record without the formal artifact required by its method;
- numerical evidence without its actual precision and tolerance;
- `exact_solution` on a serialized numerical witness;
- an upper-bound implication from a derived-structure check; and
- a claim that local tooling reproduced external evidence when only the same source
  program was rerun.

The generated frontier view shows the reported and certified values side by side.
It also shows a compact assurance badge, last source review, and unresolved conflict or
tool gap. Detail stays on the per-`n` page.

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
| Verify arbitrary `NumberField` input | built with an unenforced precondition | reject unless irreducibility and unique root isolation are certified |
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
- the largest `n` in the declared frontier horizon;
- missing local source material, conflicting values, and unresolved newer claims; and
- a bead for every uncovered or disputed item.

Completion requires a case for every `n` in the declared horizon and every result found
in the named primary-source set.
The audit determines and records the horizon rather than assuming the current `n ≤ 100`
directory is complete.
The known Kingbird catalogue already reaches at least `n = 324`, so a horizon that stops
at 100 needs an explicit scope label until the extension lands.

Search-engine discovery can suggest sources, but promotion uses first-party pages,
papers, repositories, or author-supplied data.
A source conflict remains visible until adjudicated; the latest date alone does not
decide mathematical validity.

### Source Identity Without Ceremony

Git history, a stable local path, the source URL, and a retrieval date identify a
first-party document retained in this repository.
An additional SHA beside that file does not strengthen the mathematical claim and will
be removed.

A digest remains only when it performs a named function, such as:

- comparing two independently retrieved byte streams across a real trust boundary;
- providing a stable content identity for deduplication or an append-only event; or
- protecting completeness or cache correctness for a generated artifact.

The field or nearby documentation names that function.
“Provenance” alone is not a sufficient reason.
Checks that merely bind one Git-tracked source file to a hard-coded copy of its current
hash are removed, along with process tables that exist only to record those hashes.

### Process Discipline

The six workflow entry points remain W1 research pass, W2 factual review, W3 insight
iteration, W4 process review, W5 efficiency loop, and W6 research loop.
An orchestrator may switch workflows inside one agent session, but each switch starts a
declared phase with its own focus, output, clock, and stopping condition.
The generated session and ledger views summarize the phase history.

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

### Durable Documentation Map

The implementation adds one validated documentation map under `docs/project/`. It maps
each durable prose document to its role, authority, lifecycle, and supersession target
when applicable. It lists the small set of standalone project documents individually and
covers homogeneous artifact directories through their governing schema.

The map prevents two practical failures: agents entering through a historical review as
if it were current policy, and a current claim living only in a transient spec or
handoff.
It does not duplicate titles, summaries, dates, or evidence already owned by the
documents.

| Surface | Durable authority after implementation | Required migration |
| --- | --- | --- |
| `README.md` | core assurance rules, compact workflow selector, reader entry points | state “verified” and “numerically checked” rules; link the current frontier and synopsis |
| `SYNOPSIS.md` | full terminology, capability/gap ladder, verification process, workflow transitions, current technical state | replace tier language; explain reported versus certified frontiers and formal-promotion limits |
| `TUTORIAL.md` | first-use path through the tools and record | update examples to use inspect, check, and verify with their exact meanings |
| `conventions.md` | ids, schemas, field rules, and objective checks | remove “every convention becomes a check”; retain only checks with a named benefit |
| `frontier/README.md` | frontier semantics, coverage scope, reader and contributor workflows | document v2 case/evidence contracts, source conflicts, replay outcomes, and generated views |
| `frontier/n-*.md` | one typed claim register per `n` | migrate every case, reclassify every witness, and remove free-text assurance ambiguity |
| `campaign/README.md` | W6 mechanics | adopt the assurance/method split without duplicating synopsis definitions |
| campaign schemas and artifacts | typed historical and current research record | migrate precision fields and annotate unsupported historical verdicts without rewriting raw results |
| `resources/README.md` and source indexes | source retention and reconstruction policy | remove redundant checksum requirements; state the real trust-boundary exceptions |
| research reports | current evidence syntheses or explicitly superseded analyses | audit every mathematical and tooling claim; link corrections and capability status |
| reviews, handoffs, postmortems, and active plans | dated historical or transient records | map lifecycle; correct dangerous current-sounding claims in place or add explicit supersession notes |
| probe and component READMEs, including `frankensim-probe/README.md` | local component scope and reproducible use | map lifecycle and audit every assurance or capability claim |
| `AGENTS.md` and contributor-facing instructions | agent entry discipline | require common-doc review and the authoritative assurance vocabulary for durable edits |

All durable Markdown edits follow the common documentation guidelines.
Objective parts are automated: footer presence, local-link validity, complete
document-map coverage, schema conformance, generated-view freshness, and forbidden
current vocabulary.
Editorial review covers meaning, reader order, tone, and duplication.

Historical quotations or raw source text may contain old terms.
A validator exception must be scoped to an explicitly marked quotation or archival path,
never to a whole current document.

### Schema and API Changes

The implementation introduces or revises these contracts:

- `packing.squares:SquarePackingCase/v2` for reported and certified bounds;
- `packing.squares:FrontierEvidence/v1` for typed evidence and replay status;
- `packing.squares:Witness/v1` for center/rotation or corner geometry with explicit
  units, coordinate convention, literal values, and source references;
- `packing.squares:Experiment/v2` for assurance, method, actual precision, and
  tolerance;
- `packing.squares:DocumentMap/v1` for document authority and lifecycle; and
- generated frontier and documentation-map views checked against their source data.

The exact file split is an implementation choice.
The logical contracts and validation rules are not.

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

### Phase 1: Establish the Contract and Migrate the Current Record

- [ ] Land the controlled vocabulary and logical implications in README, synopsis,
  tutorial, conventions, frontier README, campaign runbook, component READMEs, and
  resource policy.
- [ ] Add the v2 case, evidence, experiment, witness, and document-map contracts with
  cross-record semantic validation.
- [ ] Generate a reader-first frontier table with reported best, certified upper bound,
  proved lower bound, status, assurance, conflict, and freshness.
- [ ] Migrate all current `n = 1..100` cases and every current campaign artifact to the
  new fields; preserve raw measurements and use named defects or revision notes for
  invalid historical conclusions.
- [ ] Correct the `n = 29` source roles and wording.
  Exp-012 remains a 160-digit numerical check; H-024 becomes unresolved under its
  original exact prerequisite or is superseded by a precisely numerical successor claim.
- [ ] Audit every bare “verified,” “exact,” “proof,” “polished,” `f64_screen`, and
  tolerance claim in the packing tree.
- [ ] Remove redundant Git-source hashes and retain only digests with a documented
  functional purpose.
- [ ] Add the durable documentation map and complete a common-doc editorial pass over
  every definitive doc, research report, review, handoff, postmortem, and active plan.

**Done when:** all existing structured artifacts validate under the new schemas; no
current prose blurs numerical and formal evidence; every project doc has an authority
and lifecycle; and the `n = 29` regression fixture displays only claims its public data
and local checks support.

### Phase 2: Complete Source Coverage and the Reusable Replay Path

- [ ] Audit the named primary-source set, record conflicts and review dates, determine
  the current horizon, and create a case for every `n` through that horizon.
- [ ] Adjudicate the July 2026 `n = 68` and `n = 69` claims and any other newer results;
  do not promote an inaccessible certificate.
- [ ] Build the witness interchange format, source adapters, viewer, and independent
  numerical checks for `numerical-f64` and `numerical-multiprecision`.
- [ ] Attempt local replay for every external full-geometry witness in scope and record
  one of the defined dispositions.
- [ ] Make rational and algebraic verification emit replayable certificates, and close
  the generic number-field precondition gap before calling that path verified.
- [ ] Add exact rational robustification for suitable numerical poses, with any side
  relaxation explicit in the resulting bound.
- [ ] Keep the source archive and frontier linked without duplicating file hashes or
  silently editing source-faithful material.

**Done when:** every result in the declared source set and horizon is represented, every
available geometry has a replay disposition, and a new supported witness can be
inspected and numerically checked without case-specific verifier code.

### Phase 3: Add Formal Promotion and Make the Contract Continuous

- [ ] Implement and independently test an outward-rounded interval-certificate path for
  suitable contact systems.
- [ ] Attempt formal promotion of the highest-value uncertified records, retaining exact
  certificates, slightly relaxed certified bounds, or typed blockers.
- [ ] Add small independent certificate checkers and negative controls for containment,
  overlap, field metadata, interval rounding, incomplete input, and false optimality
  promotion.
- [ ] Make schema, semantic, generated-view, document-map, terminology, and link checks
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
- Every `n` in the declared horizon occurs exactly once.
- `proved` requires exact equality between verified lower and certified upper bounds.
- Every numerical record declares method, actual precision, and tolerance.
- Every verified record declares a supported formal method and its required formal
  artifact: either a machine certificate and replay command or a fully scoped proof and
  independent audit record.
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
- An exact trivial-grid witness gives every case a certified fallback upper bound.

### Documentation Review

The objective gate checks footer, mapping, links, forbidden live terminology, and
generated content.
The editorial pass then applies the common documentation guidelines to
every durable Markdown file changed or reclassified, with special attention to:

- reader-first conclusions before mechanism;
- one authoritative home per rule;
- explicit scope, uncertainty, and supersession;
- no ceremonial tables, hashes, or fields without a named use; and
- preservation of source-faithful and historical evidence.

The existing baseline remains green:

```bash
uv run --frozen python tools/validate_schemas.py
uv run --frozen python tools/render_tables.py --check
./test.sh
```

New focused checks join these commands rather than creating an undocumented parallel
gate.

## Rollout Plan

Implementation lands as a stack above the current workflow-entry-points PR:

1. this plan and its bead map;
2. vocabulary, schema, definitive-doc, and current-corpus migration;
3. source-horizon expansion, full document/research audit, and generic witness replay;
4. exact/interval promotion tooling and continuous semantic gates.

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
- [Frontier map](../../../../frontier/README.md)
- [Campaign runbook](../../../../campaign/README.md)
- [Minimal packing toolkit plan](plan-2026-08-22-minimal-packing-toolkit.md)
- [Unattended research readiness plan](plan-2026-08-23-overnight-cartography-run.md)
- [Schadt `n = 29` repository](https://github.com/BalthasarStrauss/Squares-packing_S-29-_New-Record)
- [Kingbird square-packing catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
- [July 2026 UnitSquare results](https://www.hmbelvedere.com/)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
