---
title: "agenda-012 — weighted proof, precision bridge, and cross-scale controls"
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-012
  title: Weighted proof, precision bridge, and cross-scale controls
  updated: '2026-09-01'
  status: active
  objective: >-
    Execute X-011's three disjoint first-wave decisions before buying another broad
    search: check the fixed 4.5058 weighted certificate at n = 17 with an independently
    written accumulation implementation and explicit shared assumptions; reconstruct
    both rounded n = 68/69 children and their hash-verified public parents under bounded
    serialization models; and exactify n = 50 as the rational large-n candidate control
    transferred from BC-089. Each block lasts two to two-and-a-half hours and is divided
    into 15--30 minute cells. A 45-minute checkpoint may then promote at most one
    successor in each lane whose prerequisite passed, from zero to three successors in
    total. No mathematical claim moves in the first wave, no agent infers exact contacts
    from rendered coordinates, and no n = 5 work expands beyond BC-010's terminal rule.
  items:
  - id: BC-108
    purpose: measurement_validation
    owner_focus: correctness
    instances: [17]
    state: ready
    priority: 0
    question: >-
      Does an independently written exact accumulation implementation agree with the
      fixed Massaccesi weighted-point certificate at L = 4.5058, and which proof
      assumptions remain shared with the source?
    hypotheses: []
    budget: >-
      150 minutes, factual-review then pipeline-improvement and research-loop. Cells:
      0--20 freeze certificate data, hashes, constants, and source defects; 20--45
      harden a source-faithful replay with explicit failures; 45--70 implement a second
      exact accumulation path without the published two-dimensional difference-array
      sweep; 70--95 compare total mass, angle coverage, event cells, and global minimum;
      95--120 run boundary, atom, weight, and angle-net mutations; 120--135 run the
      optimized-Python and source-defect controls; 135--150 record shared assumptions,
      validate, and hand off.
    entry: >-
      packing/resources/web/n17-lower-bounds-2026 contains the retained sources and
      hashes. The extracted source verifier replays with 168 atoms, total mass
      9744/576, 181 rational directions and minimum 576/576. That is source-backed and
      audit-positive, not independent. The repository's verified lower bound is
      4.426213 at n = 17 and 18; n = 19 remains at Nagamochi's 4.464102. The source
      generator's inclusive-range defect must not be copied into a candidate path.
    exit: >-
      A retained independent-implementation checker and mutation suite that agrees on
      every exact certificate invariant, or a typed discrepancy requiring adjudication
      with the smallest failing cell and witness. The record must name the fixed atoms,
      rational angle net, event-cell reduction, and shrink/scaling argument as shared
      assumptions. Agreement is not a structurally independent proof method and does not
      by itself authorize adoption. This block does not update the frontier, transfer the
      bound, or generalize the LP search; the tool, not a one-off script, is the artifact.
    bead: think-swtr
    depends_on: []
    workflows: [factual-review, pipeline-improvement, research-loop]
    next_evidence: >-
      Not started. Use the BC-108 launch card below. The write scope is
      packing/cases/n17_weighted_certificate/, packing/tests/test_n17_weighted_certificate.py,
      and one new AgentSession. Shared frontier and strategy records wait for BC-112.
    parallel_group: agenda012-first-wave
  - id: BC-109
    purpose: measurement_validation
    owner_focus: correctness
    instances: [68, 69]
    state: ready
    priority: 0
    question: >-
      Can the six-decimal UnitSquare children and their cited public parents be reduced
      to hash-verified rigid-pose candidates under conservative serialization models, or
      does source precision force a typed refusal?
    hypotheses: []
    budget: >-
      150 minutes, pipeline-improvement then factual-review. Cells: 0--20 freeze child
      hashes, parent URLs and hashes, the retention rule, and candidate serialization
      models; 20--45 retrieve each parent ephemerally, verify its declared digest, and
      normalize it without retaining raw Kingbird bytes; 45--70 build a reusable
      corners-to-rigid-pose regularizer; 70--95 fit both parent-child pairs and report
      residual, multiplicity, and conditioning; 95--120 bound wall and pair predicates
      under nearest-rounding, truncation, and any source-declared export model; 120--135
      assign only ruled-out, possible, or tolerance-qualified contact labels and run
      perturbation controls; 135--150 retain permitted artifacts, validate, and hand off.
    entry: >-
      The public release reports 45-digit sides and strong first-party interval checks,
      but publishes six-decimal child polygons rather than interval boxes, receipts or
      high-precision coordinates. The child SVGs are retained at
      packing/resources/web/known-best-packings/unitsquare/n068.svg and n069.svg. Parent
      URLs and declared SHA-256 values live in
      packing/resources/web/unitsquare-release1-2026/results.json; raw Kingbird SVGs may
      be inspected only ephemerally under the repository's retention policy. The current
      child witnesses are excluded from contact-motion screens. House hue diagnoses
      recovered orientation only; neither shade nor the raw SVG palette supplies contact
      or angle evidence for these two cases. BC-050 and H-030 remain blocked.
    exit: >-
      Permitted normalized center-angle candidates for both parents and children, with
      verified provenance, a declared serialization envelope, conservative side and
      separation receipts, and only ruled-out, possible, or tolerance-qualified contact
      labels; or a typed refusal naming the unbounded source transform, hash mismatch, or
      geometric ambiguity. Preserve nearest-rounding, truncation, and each declared
      export model as separate results; never merge them into an apparent contact graph.
      For n = 68, a model is `surgery-grade` only if its maximum induced corner
      displacement, container-side interval width, and worst wall/pair-separation
      interval width are each at most one quarter of the released
      `7.68618004216131e-5` gain, and every validity sign is decided except explicitly
      tolerance-qualified contacts. Six decimal places alone do not imply nearest
      rounding. A later surgery pilot requires both parent and child outputs under at
      least one surgery-grade model. This block does not adopt the release's interval
      claim, infer exact contacts, or run surgery.
    bead: think-26b1
    depends_on: []
    workflows: [pipeline-improvement, factual-review]
    next_evidence: >-
      Not started. Use the BC-109 launch card below. The write scope is
      packing/src/sqpack/research/unitsquare_precision.py,
      packing/tests/test_unitsquare_precision.py, packing/cases/unitsquare_precision/,
      and one new AgentSession. It does not edit H-030 or shared frontier records.
    parallel_group: agenda012-first-wave
  - id: BC-110
    purpose: measurement_validation
    owner_focus: correctness
    instances: [50]
    state: ready
    priority: 1
    question: >-
      Can the reported n = 50 packing at exact rational side 53/7 be reconstructed and
      verified exactly, turning it from a candidate into the large positive control for
      the promotion pipeline?
    hypotheses: []
    budget: >-
      120 minutes, research-pass then research-loop. Cells: 0--20 verify the BC-089
      ownership transfer and freeze retained source facts; 20--45 reconstruct the
      rational construction or derive a typed source gap; 45--70 encode and verify every
      wall and pair predicate over Q; 70--90 freeze and fire an exact mutation that makes
      one named wall or pair predicate negative; 90--105 compare the observed seam with
      the n = 18 and n = 19 exact controls; 105--120 retain the result, choose n = 54
      versus n = 39 as the next instrument rung, validate, and hand off.
    entry: >-
      Agenda-009 now transfers n = 50 out of BC-089/think-d0j1 and into this block; the
      two blocks no longer share ownership. Read packing/frontier/n-050.md and
      packing/witnesses/known-best/n-050.yaml. The frontier reports 53/7 but retains only
      the grid as verified. Knowing the exact side is not knowing the pose. n = 18 is the
      Q(sqrt(7)) positive control, n = 19 is an exact Q(sqrt(2)) mechanism contrast, and
      n = 53 is the representation refusal.
    exit: >-
      A case package and exact verifier establishing the retained n = 50 construction
      at 53/7, with a pre-frozen exact coordinate or container mutation that makes a
      named predicate fail; or a typed refusal locating the missing rule or unstable
      coordinates. The first wave retains a certificate-ready artifact but does not
      change the frontier. The handoff selects n = 54 only if nested-radical
      representation is the next seam, or n = 39 if interval certification is cheaper.
    bead: think-uz6f
    depends_on: []
    workflows: [research-pass, research-loop]
    next_evidence: >-
      Not started. Use the BC-110 launch card below. The write scope is
      packing/cases/n050_exact/, packing/tests/test_n050_exact.py, and one new
      AgentSession. Agenda-009 already records the ownership transfer; do not reopen its
      broad sweep or edit shared frontier records in this block.
    parallel_group: agenda012-first-wave
  - id: BC-111
    purpose: research
    owner_focus: insight
    instances: [17, 18, 19, 39, 50, 54, 68, 69]
    state: blocked
    priority: 1
    question: >-
      Which first-wave lane earned its successor block, and which assumption should be
      stopped or repaired before more research time is spent?
    hypotheses: []
    budget: >-
      45 minutes, insight-iteration and process-review. Cells: 0--15 audit each exit
      against its predeclared evidence; 15--30 mark BC-112 through BC-114 ready,
      blocked, or stopped without widening them and name a credible second weighted-
      certificate consumer or record that none exists; 30--45 apply every row and bead
      hold transition, update the handoff, and run the documentation pass.
    entry: >-
      BC-108, BC-109 and BC-110 are terminal (`complete` or `stopped`) with retained
      artifacts or premeasurement guard receipts, typed outcomes, and their task beads
      closed for task-completion reasons. A measured positive or negative outcome makes
      its row `complete`; only a gate that stops before measurement makes it `stopped`.
      Closing a task bead never relabels a scientific refusal as success. The checkpoint
      reads the retained artifacts; it does not rerun experiments or resolve
      evidentiary disagreement by prose.
    exit: >-
      A dated agenda update that assigns each successor a state and reason, preserves
      negative results, records a candidate second weighted-certificate consumer or an
      explicit absence, and names the exact next AgentSession entry point. It may promote
      zero to three successors, but no more than one per first-wave lane. Before closing
      think-1dm8, set each promoted successor row `ready` and its bead hold to `none`;
      keep each reparable but unpromoted row `blocked` with hold `blocked`; and set each
      stopped lane row `stopped` with hold `paused`. No new target, mathematical
      promotion, or unplanned experiment is allowed inside the checkpoint.
    bead: think-1dm8
    depends_on: [BC-108, BC-109, BC-110]
    workflows: [insight-iteration, process-review, documentation-pass]
    next_evidence: >-
      Blocked on the three first-wave exits. Each first-wave owner may terminalize only
      its own row and next_evidence at handoff. The coordinator owns every other shared
      agenda edit, verifies that all three task beads closed without conflating task and
      scientific outcomes, regenerates the map after all three rows are terminal, and
      then claims this checkpoint. Successor beads begin on blocked hold; the coordinator
      applies their explicit hold transitions before closing think-1dm8.
  - id: BC-112
    purpose: research
    owner_focus: correctness
    instances: [17, 18, 19]
    state: blocked
    priority: 1
    question: >-
      Does the fixed 4.5058 certificate support repository adoption at n = 17--19 under
      the current evidence contract, separately from whether its tooling is reusable?
    hypotheses: []
    budget: >-
      120 minutes in six 20-minute cells: collect BC-108's agreement or discrepancy and
      shared-assumption list; reconcile the result/evidence contract; determine the
      fixed certificate's mathematical checker status; determine assurance and adoption
      status separately; calculate the exact monotone consequences for n = 18 and 19 and
      update records only if warranted; validate and hand off.
    entry: >-
      BC-108's independently written accumulation implementation agrees on every fixed
      invariant, names its shared proof assumptions, and BC-111 promotes this block. The
      then-current evidence/result contract controls adoption. Agreement between two
      implementations is not silently relabelled as two independent proof methods. A
      BC-108 discrepancy routes to a repair block, not to adoption.
    exit: >-
      Three separate determinations: checker agreement or discrepancy; adopted,
      not-adopted, or unresolved assurance status; and the exact monotone consequences
      for n = 17, 18 and 19. Non-adoption is not mathematical refutation. Generic-tool
      work and the LP generator repair remain in BC-115. No n = 20 improvement is
      claimed from this value. This block owns BC-115's final gate: only an `adopted`
      outcome plus the BC-111-named second consumer may mark BC-115 `ready` and remove
      think-w8hh's blocked hold. Every other outcome leaves the row and hold blocked with
      the reason recorded.
    bead: think-5q0v
    depends_on: [BC-108, BC-111]
    workflows: [factual-review, research-loop, documentation-pass]
    next_evidence: >-
      Blocked on BC-108 agreement and the checkpoint. If promoted, it owns
      packing/frontier/n-017.md, packing/frontier/n-018.md,
      packing/frontier/n-019.md, packing/frontier/results.yaml,
      packing/frontier/evidence.yaml, and packing/frontier/proof-strategies.yaml plus
      generated packing/frontier/RESULTS.md; BC-108 does not. At handoff, explicitly
      apply or retain think-w8hh's hold according to the `adopted`-and-second-consumer
      conjunction; the dependency edge alone is not authorization.
  - id: BC-113
    purpose: research
    owner_focus: insight
    instances: [68]
    state: blocked
    priority: 1
    question: >-
      In an exploratory n = 68 pilot with a real information barrier, can a frozen
      public-parent surgery grammar recover the hidden released child's improvement?
    hypotheses: [H-051]
    budget: >-
      180 minutes. Cells: 0--20 freeze the hash-verified parent snapshot, sanitized input
      allowlist, operator roles, and child embargo; 20--45 freeze grammar, counted work,
      and hit criterion; 45--70 run parent replay and a predeclared non-hit control;
      70--100 execute the bounded proposer; 100--125 validate outputs without exposing
      the child; 125--150 lift the blind and compare; 150--180 record all misses, the
      information barrier, the pilot disposition, validation, and handoff.
    entry: >-
      BC-109 emits hash-verified, surgery-grade parent and child candidates and BC-111
      promotes the block. The proposer must have no prior child exposure and must work
      only inside an isolated, audited snapshot whose input allowlist contains the parent
      model and frozen proposer contract, excludes the child side, child pose, BC-109
      child outputs and every equivalent frontier/witness field, and disables network
      access. Operator separation is optional extra assurance, not a substitute for the
      barrier. Freeze the next free H-051 experiment record, grammar, exact proposal
      schedule and tier-S pair-test cap before target execution. The validator may see
      child data only after proposer output is immutable. Otherwise stop before
      measurement. The n = 68 released gain is about twelve times n = 69's and is the
      first discriminator. This single-case pilot cannot adjudicate H-030's two-of-six
      registered criterion.
    exit: >-
      An exploratory n = 68 pilot result with proposer version, counted work, audited
      information barrier, hidden-child comparison, independent validity, and all misses
      retained in the next free `exp-NNN-h-051-n68-surgery-calibration` experiment and
      result artifacts. Dispose H-051 under its frozen criterion. H-030 remains
      undisposed. A success is at most one calibration datum; a failure may stop
      unseen-record work as a portfolio decision but does not reject H-030 or buy a
      larger search.
    bead: think-gbkd
    depends_on: [BC-109, BC-111]
    workflows: [research-loop, insight-iteration]
    next_evidence: >-
      Blocked on surgery-grade parent and child candidates, a credible information
      barrier, and the checkpoint. If promoted, write only
      packing/cases/unitsquare_surgery/n068/,
      packing/src/sqpack/research/unitsquare_surgery.py,
      packing/tests/test_unitsquare_surgery.py, the next free H-051 experiment and result
      files under packing/campaign/series/series-000-smoke-and-calibration/, and one new
      AgentSession. The experiment record must exist before target execution. n = 69
      remains held out until n = 68 establishes a measurable response.
  - id: BC-114
    purpose: research
    owner_focus: correctness
    instances: [39, 54]
    state: blocked
    priority: 2
    question: >-
      After n = 50, is the next cheapest capability test nested-radical exact promotion
      at n = 54 or a degree-five interval certificate at n = 39?
    hypotheses: []
    budget: >-
      Up to 180 minutes in six 30-minute cells on exactly one selected case: freeze the
      criterion and control; build the missing representation or interval step; verify;
      fire the case-matched negative control; compare to n = 50; record and finalize.
    entry: >-
      BC-110 completes and BC-111 selects one branch from the measured seam. n = 19 is
      an exact Q(sqrt(2)) mechanism contrast and may refuse only an n = 18-specific
      Q(sqrt(7)) recognizer; n = 53 is the representation refusal. n = 55 stays a later
      adversarial case, and n = 51 stays in the separate rare-basin lane. The block may
      not silently become a sweep.
    exit: >-
      One verified construction certificate or typed refusal at the selected case, plus
      a concrete next instrument seam. The unselected case remains queued rather than
      being reported as attempted. This is a one-case representation calibration under
      either outcome and leaves the corpus-level H-038 claim undisposed.
    bead: think-dao9
    depends_on: [BC-110, BC-111]
    workflows: [research-loop, factual-review]
    next_evidence: >-
      Blocked on the n = 50 result and checkpoint. The coordinator records the branch
      choice before an agent claims this bead. The selected write scope is either
      packing/cases/n054_exact/ with packing/tests/test_n054_exact.py or
      packing/cases/n039_interval/ with packing/tests/test_n039_interval.py, plus one
      AgentSession; never both in one block.
  - id: BC-115
    purpose: tool_validation
    owner_focus: correctness
    instances: [17]
    state: blocked
    priority: 2
    question: >-
      After an adoption decision and a named second consumer, can the fixed-certificate
      code become a generic weighted-point certifier and sound LP candidate pipeline?
    hypotheses: []
    budget: >-
      Up to 180 minutes in six 30-minute cells: freeze two consumer contracts; define a
      generic exact certificate schema; port the n = 17 fixture without changing its
      result; repair the LP generator's inclusive endpoint; add exact replay and
      mutation controls for both consumers; validate, document, and hand off.
    entry: >-
      BC-112's assurance outcome is `adopted`, BC-111 has named a credible second fixed-
      certificate consumer, and the BC-112 coordinator has explicitly removed
      think-w8hh's blocked hold. A merely terminal `not-adopted` or `unresolved` outcome
      does not pass this gate. Float LP output remains a candidate only; exact replay is
      the proof. Tool reuse is not evidence for H-006 or H-034 and cannot change either
      hypothesis verdict.
    exit: >-
      A generic certificate reader/checker with two retained consumers, the repaired
      candidate generator, and mutations that distinguish generator failure from exact
      certificate failure; or a typed E1 refusal when a second consumer does not justify
      productization. No mathematical frontier claim moves in this block.
    bead: think-w8hh
    depends_on: [BC-112]
    blocked_on: >-
      BC-112 must adopt the certificate and a second fixed-certificate consumer must be
      named before the coordinator removes the manual hold.
    workflows: [pipeline-improvement]
    next_evidence: >-
      Held `blocked` on BC-112 adoption and a second consumer. BC-112 owns the clearing
      action; an arriving BC-115 agent must not claim the bead merely because `tbd ready`
      exposes it. If promoted, own
      packing/src/sqpack/research/weighted_certificate.py,
      packing/tests/test_weighted_certificate.py, the n = 17 fixture migration, and one
      new AgentSession; do not edit H-006 or H-034.
---
# Agenda-012 — Weighted Proof, Precision Bridge, and Cross-Scale Controls

> **Merge renumbering (2026-09-01):** this agenda was drafted in parallel with the
> epistemics codification and originally minted `BC-107`–`BC-113`; `BC-107` had landed
> on `main` first as agenda-011’s codification cell, so at merge the seven cells here
> renumbered to `BC-108`–`BC-114` per the id convention (newer branch renumbers,
> recorded as an annotation).
> The owning beads and every cross-reference in X-011 and the synopsis were swept in the
> same change. BC-115 was added afterward as a separately gated productization block and
> was not part of that renumbering.

## Workflow entry point

At the start of a block, run `tbd prime`, claim the block’s named bead, and allocate the
next free AgentSession id.
Do not reserve empty session files.
Run project Python only through `uv run --frozen ...` from `packing/` or with
`uv run --directory packing`.

Each first-wave agent owns the paths named in its launch card and sends shared-record
changes to the BC-111 coordinator.
The three blocks are intentionally disjoint and may run in parallel.
At handoff, each owner may change only its own agenda row from `ready` to `complete` or
`stopped` and replace that row’s `next_evidence`. A block that executes and returns a
typed positive or negative outcome becomes `complete`; only a premeasurement gate stop
becomes `stopped`. In both cases, close the task bead with a reason naming the
scientific outcome—task closure is not scientific success.
After all three rows are terminal and their beads are closed, the coordinator
regenerates the agenda map and owns every other shared agenda edit.

## First-wave launch cards

### BC-108 — fixed `n = 17` weighted certificate

- **Claim:** `tbd update think-swtr --status in_progress`.
- **First replay, from `packing/`:**
  `uv run --frozen python resources/web/n17-lower-bounds-2026/massaccesi-verify-n17-lower-bound-4_5058.py`.
- **Read-only inputs:** `resources/web/n17-lower-bounds-2026/`, `frontier/n-017.md`, and
  `epistemics.md` at repository root.
- **Write scope:** `cases/n17_weighted_certificate/`,
  `tests/test_n17_weighted_certificate.py`, and one new AgentSession.
- **Focused close:**
  `uv run --frozen --all-extras --group dev pytest -q tests/test_n17_weighted_certificate.py`
  followed by `uv run --frozen --all-extras --group dev packing-validate --records`.

### BC-109 — UnitSquare parent/child precision bridge

- **Claim:** `tbd update think-26b1 --status in_progress`.
- **First check, from `packing/`:**
  `uv run --frozen --all-extras --group dev pytest -q tests/test_known_best_atlas.py`.
- **Read-only inputs:** `resources/web/known-best-packings/unitsquare/n068.svg`,
  `n069.svg`, `resources/web/unitsquare-release1-2026/results.json`,
  `resources/web/known-best-packings/README.md`, `src/sqpack/known_best.py`, and
  `devtools/build_known_best_atlas.py`.
- **Ephemeral parent hash checks, from `packing/`:**
  `test "$(curl -fsSL https://kingbird.myphotos.cc/packing/square-68.svg | shasum -a 256 | awk '{print $1}')" = 558fbdddfeb0b2f8752b88e172d2776544beb4d2a7122189ef77c1e1c5ebdc6d`
  and
  `test "$(curl -fsSL https://kingbird.myphotos.cc/packing/square-69.svg | shasum -a 256 | awk '{print $1}')" = 0333814c7b43ddc7db549a54771de117f8a6b7b3db0f89c12fe035115546fd08`.
  These commands retain no source bytes; the production tool must perform and record the
  same verification before parsing.
- **Write scope:** `src/sqpack/research/unitsquare_precision.py`,
  `tests/test_unitsquare_precision.py`, `cases/unitsquare_precision/`, and one new
  AgentSession. Raw Kingbird parent bytes remain ephemeral.
- **Focused close:**
  `uv run --frozen --all-extras --group dev pytest -q tests/test_unitsquare_precision.py tests/test_known_best_atlas.py`
  followed by `uv run --frozen --all-extras --group dev packing-validate --records`.

### BC-110 — candidate rational control at `n = 50`

- **Claim:** `tbd update think-uz6f --status in_progress`.
- **First check, from `packing/`:**
  `uv run --frozen packing-witness check witnesses/known-best/n-050.yaml --method numerical-multiprecision --precision 120 --tolerance 1e-8`,
  then
  `uv run --frozen --all-extras --group dev pytest -q tests/test_promote_exact_phase1.py tests/test_exact_construction_price.py`.
- **Read-only inputs:** `frontier/n-050.md`, `witnesses/known-best/n-050.yaml`,
  `resources/web/known-best-packings/sources.json`, the `verify_packing` verifier in
  `src/sqpack/verify.py`, the `fixed_cell_lp` and `solve_from_scratch` helpers in
  `src/sqpack/exact_lp.py`, and the exact field controls
  `cases/lifted_q7/verify_exact.py` and `cases/lifted_q2/verify_exact.py`.
  `tests/test_promote_exact_phase1.py` is an n = 11 exact-LP control and
  `tests/test_exact_construction_price.py` is a source/refusal control; neither is an n
  = 50 reconstruction entry point.
- **Write scope:** `cases/n050_exact/`, `tests/test_n050_exact.py`, and one new
  AgentSession.
- **Focused close:**
  `uv run --frozen --all-extras --group dev pytest -q tests/test_n050_exact.py` followed
  by `uv run --frozen --all-extras --group dev packing-validate --records`.

## Cell check-in contract

At every 15--30 minute boundary, record four lines in the AgentSession:

- **Artifact:** what durable file or receipt now exists;
- **Result:** the measured fact, refusal, or unresolved ambiguity;
- **Guard:** which independent check or negative control fired;
- **Next:** the next cell or the predeclared stop.

If a cell produces no durable instrument or evidence, stop and rescope before spending
the next cell. Keep the last 15--20 minutes of every block for records, validation, bead
notes, and a handoff that another agent can execute without reconstructing context.

## Launch order

1. Run BC-108, BC-109 and BC-110 concurrently when three agents are available.
2. Run BC-111 only after all three have typed exits.
3. Promote zero to three successors, with at most one successor per first-wave lane.
   BC-112, BC-113 and BC-114 are dependency-linked and begin on blocked holds.
   BC-111 must remove a hold only for a promoted row, retain it for a reparable blocked
   row, and pause a stopped row before the checkpoint closes.
4. BC-111 names a candidate second weighted-certificate consumer or records that none
   exists. BC-115 stays held after BC-112 unless BC-112 both adopts the certificate and
   explicitly clears the hold for that named consumer.
   Adoption and productization are separate decisions.
5. Do not open another `n = 5` task.
   Dedicated BC-010 bead think-iivb gets one final bounded block with a preregistered
   `n = 10` transfer or is parked; legacy H-023 owner think-1s0h is not the queue gate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
