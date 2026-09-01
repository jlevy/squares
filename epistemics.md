# Epistemics

This document defines the four classifications attached to whole results in this
repository. [`conventions.md`](conventions.md) owns field formats and identifiers;
[`packing/frontier/evidence.yaml`](packing/frontier/evidence.yaml) holds the evidence
entries; and the results register holds each classified claim in
[`results.yaml`](packing/frontier/results.yaml), with a generated reader view in
[`RESULTS.md`](packing/frontier/RESULTS.md).

The results checker validates structural support for a declared classification.
Human review remains responsible for deciding whether the cited evidence is relevant and
complete for the stated claim.

## The Four Classifications

| Axis | Question | Treatment |
| --- | --- | --- |
| Verification (`V`) | What is the highest verification rung supported by the cited evidence, regardless of who performed it? | Structurally derived, except `V0` and `V2` |
| Confirmation (`C`) | What has this repository recorded, replayed, or established itself? | Structurally derived |
| Significance (`S`) | How important is the result? | Dated judgment; never gating |
| Novelty (`N`) | What does the retained source search support saying about novelty? | Declared and reviewed; not derived at result level |

Use `V4/C3` when describing a whole result.
The unqualified term `verified` remains the formal assurance label for an individual
evidence entry.

## Verification

Verification uses a project-prioritized ordering of evidence types.
The rungs are not cumulative: `V4` does not imply publication, and `V5` means that a
proof assistant has checked a formalization, not that the formal statement matches every
intended prose claim.

| Rung | Meaning | Structural support |
| --- | --- | --- |
| `V0` | Claimed or recorded only | No higher predicate; the result explains the classification in `notes` |
| `V1` | Numerically checked | A numerical method with recorded precision |
| `V2` | Proof asserted but not publicly recoverable | Declared with `notes` explaining the unavailable proof |
| `V3` | Published or audited proof | `method: published-proof` or `proof-audited`, with a `proof` block |
| `V4` | Machine-verified | Exact-algebraic or interval-certified evidence with a certificate, replay command, and passing replay status |
| `V5` | Proof-assistant checked | `method: proof-assistant-checked` |

The checker derives `V1` and `V3`–`V5` from the evidence cited by the result.
`V0` and `V2` are declared because the current evidence fields do not distinguish an
ordinary unsupported claim from an asserted but unavailable proof; both require an
explanatory `notes` field.
The evidence schema separately enforces its own provenance, limitations, and
method-specific fields.

## Confirmation

Confirmation counts only work recorded as `audited-here` or `replayed-here`, except
`C1`, which describes a qualifying read of external evidence.

| Rung | Meaning | Structural support |
| --- | --- | --- |
| `C0` | Recorded | No qualifying read or repository replay |
| `C1` | Read | An `external_review` with a qualifying state, date, reviewer, and note |
| `C2` | Replayed | Repository-origin evidence with a replay command and `replay_status: passed` |
| `C3` | Machine-confirmed | Repository-origin exact-algebraic or interval-certified evidence with a certificate and passing replay |
| `C4` | Confirmed by distinct methods | At least two `C3` evidence entries with different `method` values |
| `C5` | Review-ready | `C3` or `C4`, plus an existing `review_artifact` mapped as a non-superseded review |

For `C1`, a qualifying review state is `informally-verified` or `defect-found`; the
review note records what was examined and what remains unchecked.
A `C3` or higher result must also name at least one existing control path.
The evidence schema requires a limitations statement on every evidence entry.

These predicates are deliberately literal.
Two independently written implementations using the same method still derive `C3`, not
`C4`. A control path proves that a control is retained; the checker does not infer from
its filename that the control is adversarial.
The test suite, validation configuration, and review establish those stronger facts.

## Scope and Composition

A classification attaches to the exact statement in a result’s `claim` field and its
declared scope.

- A compound claim takes the minimum rung of its load-bearing parts.
- A derived claim takes the minimum rung of its inputs and the derivation itself.
- A construction’s feasibility, the sharpness of its parameter, and global optimality
  are separate claims.

The checker derives the strongest rung present among the cited evidence entries.
When a compound or derived result declares a lower rung, its `composition` note
identifies the part that sets the minimum.
That note, the relevance of each evidence reference, and coverage of every load-bearing
premise are review obligations rather than machine inferences.

## Significance and Novelty

Significance is recorded as a score, rationale, date, and scorer.
The score guides reading order and never changes validation behavior.

| Score | Anchor |
| --- | --- |
| `S1` | Bookkeeping or a routine consequence |
| `S2` | A citable detail that changes no theorem |
| `S3` | A substantive case result or machine audit |
| `S4` | A reusable technique, bound family, or resolved disputed value |
| `S5` | Movement on a central open case or broad external adoption |

The `scored` field dates the current assessment; Git retains earlier values.

Novelty uses four labels:

| Label | Meaning |
| --- | --- |
| `common-knowledge` | Standard fact not attributed to a particular source |
| `previously-published` | Present in an identified source |
| `apparently-novel` | Not found in the recorded search, subject to its stated gaps |
| `confirmed-novel` | Priority confirmed outside this repository |

Novelty is a scoped statement about a performed search, not a claim of priority.
An `apparently-novel` evidence entry records the corpus, search, narrow novel object,
and known gaps in `novelty_basis`. The result-level label is declared and reviewed; the
results checker validates its enum value but does not derive it from the cited entries.

## Enforcement and Register

Run the executable contract from `packing/` with:

```shell
uv run --frozen --all-extras --group dev python -m devtools.check_results
```

The checker:

- resolves evidence references and artifact, control, and review-document paths;
- derives the structural `V` and `C` rungs described above;
- refuses unsupported promotion and unexplained understatement;
- requires `C5` review documents to be non-superseded reviews in
  [`document-map.yaml`](docs/project/document-map.yaml); and
- rejects unknown `T-NNN` references in the README and synopsis.

[`packing/frontier/results.yaml`](packing/frontier/results.yaml) states each result’s
claim, scope, classifications, evidence, artifacts, and `next_rung`. That final field
records the next evidence-improving action or explains why no independent rung change
applies. [`packing/frontier/RESULTS.md`](packing/frontier/RESULTS.md) is generated from
the register and sorted for readers.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
