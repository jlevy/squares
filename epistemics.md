# Epistemics

**The definitive vocabulary for how much to trust a claim in this repository.** Where
another document states or restates a verification, confirmation, significance, or
novelty level, this one wins.
[`conventions.md`](conventions.md) owns the *formats* of the fields involved — enum
spellings, id shapes, where fields live; this page owns what they *mean*. The instances
— the actual classified results — live in the results register,
[`packing/frontier/results.yaml`](packing/frontier/results.yaml), rendered to
[`packing/frontier/RESULTS.md`](packing/frontier/RESULTS.md).

## Why This Document Exists

On 2026-08-31 a machine audit refuted a lemma of a peer-reviewed published paper as
printed: Bentz 2010’s Lemma 10 prints a transposed coordinate, an exact escape
certificate defeats the printed statement, and the corrected reading certifies exactly
([the settlement](packing/resources/papers/bentz-2010-optimal-packings-13-and-46.md)).
The same day, this repository’s own first-party bound was carried by two machine proofs
no human outside the project has read.
Those two facts point at the same lesson: *whether a claim is verified somewhere in the
world* and *how much of it this repository has established itself* are different facts,
both must be legible per claim, and neither may be left to a reviewer’s mood.
Before this page, the atoms of both facts existed but were scattered across five
evidence fields; a level was something one argued about.
After it, a level is something one **earns**: each rung is a conjunction of recorded,
machine-checkable facts, the checker grants or refuses it, and a result can be committed
at a level the moment the work behind that level is done.

## The Four Axes

Every registered result carries four independent classifications:

- **Verification `V`** — the strongest verification of the claim that exists *anywhere
  in the world*, this repository included.
  A property of the claim.
- **Confirmation `C`** — what *this repository* has established end-to-end itself.
  A property of our relationship to the claim.
  Nagamochi’s theorem is high-V, low-C; a first-party certificate is high-C from birth;
  Green’s reported bound is the reason low rungs of V exist at all.
- **Significance `S`** — a judged, anchored, dated score of how much the result matters.
  Deliberately subjective, deliberately non-gating.
- **Novelty `N`** — whether the result was published before, stated as a claim about a
  performed search, never as an assertion of priority.

`V`, `C`, and `N` are grounded in recorded atoms and checkable; `S` is a judgment and is
fenced accordingly (see [Significance](#significance-s)). In prose, write levels as
`V4/C4` rather than the bare word “verified” — the bare word is exactly the ambiguity
this page retires.

## The Verification Ladder (V)

The strongest verification of the claim known to exist anywhere, ours included.
Derived as the maximum any single evidence entry supports.

| rung | meaning | exemplar |
| --- | --- | --- |
| `V0` | claimed only — a catalogue or survey assertion with no known verification | record values as records in [Kingbird] |
| `V1` | numeric — numerical evidence at any precision, no proof | the reported upper bounds; float diagnostics |
| `V2` | proof-unpublished — a mathematical proof is asserted to exist but is not publicly recoverable | Green’s Theorem 9 at `n = 17` |
| `V3` | proof-published — a peer-visible published proof | Nagamochi 2005; Bentz 2010 |
| `V4` | machine-verified — an exact or rigorously certified machine proof exists, with public artifacts and a replay | the green17 certificates; the Theorem 8 audit |
| `V5` | formally verified — checked by a proof assistant | none yet |

**The V3/V4 caveat is part of the ladder.** Peer review and machine checks catch
different failure modes: review catches conceptual errors in what a theorem *says*; a
machine check catches errors in what a proof *does*, and Lemma 10 is the standing
exhibit of V3 failing where V4 caught it.
The converse failure — a machine-certified claim whose *statement* does not mean what
its author thinks — is what V4 alone can miss, which is why C5’s review artifact states
hypotheses in prose.
The ladder ranks V4 above V3 because this project’s method is exactness; V5 is where the
two concerns merge.

Rung predicates, each checkable from a cited evidence entry:

- `V1`: an entry with numerical method and recorded precision and tolerance.
- `V2`: a recorded claim with a `source_key` and a `source-evidence` blocker saying the
  proof is not recoverable.
- `V3`: an entry with `method: published-proof` and a `proof` block naming source,
  theorem, and pinpoints, with the source retrieved into `packing/resources/`.
- `V4`: an entry meeting the C3 predicate below — whoever performed it — with public
  certificate artifacts and a passing replay.
- `V5`: an entry with `method: proof-assistant-checked` and the proof-assistant artifact
  retained.

## The Confirmation Ladder (C)

What this repository has established end-to-end itself.
Rungs are cumulative in spirit but granted independently: each is a conjunction of
predicates over recorded atoms, so **a level is committed after an effort** — do the
work, record the atoms, declare the rung, and the gate agrees or the build fails.
Nothing here involves anyone’s judgment at commit time.

| rung | meaning |
| --- | --- |
| `C0` | recorded — transcribed or cited, nothing established here |
| `C1` | read — a careful read of the source argument, with what was *not* re-derived stated |
| `C2` | replayed — the numbers re-computed here, or the source’s own checker replayed |
| `C3` | machine-confirmed — our own exact or certified implementation decides the claim and its preconditions end-to-end |
| `C4` | independently confirmed — C3 by at least two independent methods or implementations |
| `C5` | review-ready — C3 or better, assembled as a self-contained artifact a stranger can review |

**Promotion checklists.** To commit a result at a rung, produce exactly these recorded
facts; the checker derives the rung from them.

- **C1 (read):** a dated `external_review` block on the evidence entry with `state` in
  `{informally-verified, defect-found}`, naming who read it, what was worked through,
  and — mandatory — what was *not* re-derived.
  The [Nagamochi read](packing/frontier/evidence.yaml) is the template: its value is the
  four unverified items it lists, not the reassurance.
- **C2 (replayed):** a recorded `replay` command with `replay_status: passed`, declared
  precision and tolerance for numerical work, and the replay reachable from the
  validation gate.
- **C3 (machine-confirmed):** an entry with `origin` in `{audited-here, replayed-here}`,
  `method` in `{exact-algebraic, interval-certified}`, a retained `certificate`
  artifact, a replay that runs in the gate, **adversarial controls linked** — tests in
  which the checking code refuses tampered input — and a `limitations` statement
  covering the preconditions in scope.
- **C4 (independently confirmed):** at least two entries each meeting C3, whose methods
  differ or whose implementations are declared independent (`relationship_to_generator`
  and the entries’ own limitations carry the independence facts), with deterministic
  replays. Independence here is between *mechanisms*, not authors; author-independent
  checking is a V-side event (external review, V5).
- **C5 (review-ready):** C3 or C4, plus a review artifact of the declared structural
  shape — statement, hypotheses in prose, proof narrative, code map, replay
  instructions, limitations — registered in the document map, its links resolving and
  its replay commands verified.
  “Publishable quality” is deliberately reduced to this structural checklist; what a
  journal does with it is the world’s business, not a rung.

**What deliberately does not exist:** a rung for “someone here feels good about it.”
The run-night device of holding results `unresolved` with `needs_review` remains
available to *unattended* sessions as a safety hold, but a hold is a queue position, not
a level; the review that clears it consists of finishing a checklist above, after which
the level speaks for itself.

## Granularity and Composition

A level attaches to **one stated claim**, and the statement must be written down where
the level is declared (the register’s `claim` field).

- **Compound claims take the minimum over their load-bearing parts.** `s(13) = 4` is C1
  even though Figure 2 and the corrected Lemma 10 are C3, because the Sections 3.1–3.2
  case analysis is read-only — the register says so rather than letting the strongest
  part speak for the whole.
- **Derived claims take the minimum of their inputs**, and the derivation itself must be
  recorded and meet C3’s bar if the result is to stay C3 (`s(18) ≥ s(17)` by
  monotonicity: one recorded line, trivially checkable).
- A bound and its exactness are different claims: “the set works at side `4426213/10^6`”
  and “the set’s ceiling is exactly `753/250 + √2`” carry different rungs, and the
  register keeps them separate.

## Significance (S)

A judged score, `1` to `5`, anchored so that scoring is calibration rather than mood,
and **never a gate** — a checker that grades taste teaches people to game taste.
Recorded as `{score, rationale, scored, by}`; revisable, with the date carrying the
revision history.

| score | anchor |
| --- | --- |
| `S1` | trivial or bookkeeping — the grid and area bounds |
| `S2` | minor — a real, citable detail that changes no theorem: the Lemma 10 erratum |
| `S3` | solid — a new bound at specific small `n`; the first machine-check of a proof in this literature |
| `S4` | substantial — a reusable technique or a bound family; resolving a disputed value |
| `S5` | major — movement on a famous case; a method adopted beyond this project |

The checker enforces only the *shape* of an S declaration, never its value.

## Novelty (N)

Adopted unchanged from the evidence contract: `common-knowledge`,
`previously-published`, `apparently-novel`, `confirmed-novel`, with `novelty_basis`
recording the corpus, the search, the novel object named narrowly, and the known gaps.
Novelty is a statement about a performed search and is only as good as the recorded
corpus; `confirmed-novel` is granted externally or not at all.
The one addition this page makes is emphasis: the *novel object* is usually narrower
than the claim reads — certifying someone else’s bound is real work and is not a new
bound — and naming it is what keeps a defensible claim from being read as a larger one.

## Derivation and Enforcement

The rubric’s executable form is the results checker (`devtools/check_results.py`), run
in the records tier of `packing-validate`:

- Every register entry **declares** its `V` and `C` and cites its evidence entries; the
  checker **derives** both from the cited atoms and fails the build when a declared rung
  is not supported — or when a supported rung is understated, since sandbagging distorts
  the record as surely as inflation.
- `S` and `N` are checked for shape and reference integrity only.
- Every `T-NNN` mentioned anywhere in the reader tier (`README.md`, `SYNOPSIS.md`) must
  exist in the register — a dangling result id is a failed build.
- A negative control in `devtools/controls.yaml` mutates a register entry to claim an
  unsupported rung and requires the checker to catch it, so the enforcement itself is
  enforced.

## The Results Register

[`packing/frontier/results.yaml`](packing/frontier/results.yaml) holds one `T-NNN`
record per first-party or load-bearing result: the claim stated in full, its scope, the
four axes, the evidence entries and artifacts it rests on, and `next_rung` — what
concrete work would raise `C` or `V`. That last field is what makes the register a work
queue rather than a trophy case.
[`packing/frontier/RESULTS.md`](packing/frontier/RESULTS.md) is the generated view,
sorted by `S` descending then `C` descending, and is the single prioritized surface the
reader tier points at.
Register ids follow the identity rules in [`conventions.md`](conventions.md#1-identity).

## Bridging From the Evidence Atoms

The evidence entries in
[`packing/frontier/evidence.yaml`](packing/frontier/evidence.yaml) remain the atoms;
nothing about their fields changed.
What each atom feeds:

| atom | feeds |
| --- | --- |
| `assurance` | coarse sanity only — `verified` entries are the C3/V3+ candidates; the word itself is superseded in prose by V/C |
| `method` | V rung selection; C3’s exactness requirement |
| `performed_by`, `origin` | whether an entry counts toward C at all (ours) or only toward V (the world’s) |
| `relationship_to_generator` | C4 independence |
| `external_review` | C1, and V-side review state on external proofs |
| `replay`, `replay_status` | C2 and C3’s replay requirement |
| `precision`, `tolerance` | V1/C2 numerical honesty |
| `proof` block | V3 |
| `novelty`, `novelty_basis` | N |
| `limitations` | granularity: what the claim’s load-bearing parts are |

## Resolved Ambiguities

Permanent answers to the four gaps the
[2026-08-31 verification review](docs/project/reviews/review-2026-08-31-overnight-run-verification-determinations.md)
surfaced:

- **Round tier versus hypothesis disposition.** A campaign round’s verdict (`rejected` =
  its criterion measured and missed) is a fact about the round; a hypothesis’s
  disposition is governed by its registration, and a calibration-only round cannot
  dispose the hypothesis it measured.
  Where the ledger’s mechanical derivation would say otherwise, the round stays
  `unresolved` with the reason carrying the review — the exp-046 resolution is the
  template.
- **“Near the threshold.”** A measured value is *near* a hold threshold only when the
  outcome differs across the registered text’s supportable readings.
  A miss under every supportable reading is not near anything, whatever the margin.
- **Independence vocabulary for hand-designed objects.** An object designed against a
  checker makes that checker `same-implementation` evidence; the independent leg must be
  a mechanism the design never touched.
  This is C4’s definition doing the work the old field vocabulary left to judgment.
- **Sourceless claims.** A stronger claim with no recoverable proof (Green) is V2 and
  enters `reported_*` lanes only with its blocker recorded; it never suppresses a weaker
  claim at higher V/C, and the register may carry both.

## What This Page Is Not

Field formats, enum spellings, and id shapes are [`conventions.md`](conventions.md); how
sessions conduct themselves is [`operating-rules.md`](operating-rules.md); the
campaign’s verdict machinery (accept rules, tiers, freezes) is owned by the campaign
schemas and [`SYNOPSIS.md`](SYNOPSIS.md)’s workflow contracts, and this page defers to
them for everything except the round-versus-hypothesis boundary stated above.
The reader-facing short forms in [`README.md`](README.md) and
[`SYNOPSIS.md`](SYNOPSIS.md) may abbreviate this vocabulary but must not contradict it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
