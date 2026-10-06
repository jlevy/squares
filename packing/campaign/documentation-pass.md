# The W8 Documentation Pass: Runbook

How to run a documentation pass, and how to know it is finished.
[`conventions.md`](../../conventions.md) owns the formats this checks against;
[`operating-rules.md`](../../operating-rules.md) owns when a pass is due (`OR-7`). This
page is the procedure between them.

A documentation pass is worth opening when a run has closed several commitments and the
reader-facing tier has not caught up.
It is worth *closing* when every item below has an answer, including the ones whose
answer is “nothing to do”.

This is broader than W10’s mandatory document-impact review.
Every terminal agenda checks README, tutorial, synopsis, conventions, and development
guidance and records `updated` or `current`; that mechanical check does not by itself
open W8. Use this runbook when the check finds substantive drift that requires a
reader-facing reconciliation across artifacts and documents.

**Order matters.** Read the artifacts first, the documents second, and never the
reverse: a pass that starts from the prose inherits the prose’s mistakes.

**Per document.**

- [`README.md`](../../README.md): the front door.
  Does the first screen still say what the project is and what it has?
  Do the workflow entry points, the directory tree, and every headline number match the
  record? Is the thing a new reader should do first still the first thing offered?
- [`TUTORIAL.md`](../../TUTORIAL.md): orientation.
  Does every command run, on a clean checkout, in the order given?
  Does it teach the problem before the tooling?
  Does a reader who finishes it know what this project can and cannot certify, and can
  they say why the reported and verified bounds differ?
- [`SYNOPSIS.md`](../../SYNOPSIS.md): the technical account.
  Does the readiness table match [What Is Built](../../SYNOPSIS.md#what-is-built)?
  Does the handoff point at work that exists, on beads that exist?
  Are the defect aggregates the generated ones?
- [`conventions.md`](../../conventions.md): Is every `[checked]` claim still checked by
  something, and every `[convention]` still observed?
- [`operating-rules.md`](../../operating-rules.md): is every rule still one an agent
  should follow, and does each still cite the failure that motivated it?
  Regenerate `AGENTS.md`’s summary with `devtools.render_operating_rules` rather than
  editing it.
- [`development.md`](../../development.md): do the commands still exist, with those
  flags?
- **A dated document is a record, so a pass adds to it rather than rewriting it.** A
  `research-YYYY-MM-DD-` report states what was known on its date.
  Where the project’s own record has since moved past it, append what now holds and say
  when; do not restate the newer finding as though it were the original one.
  Which dated reports a given pass owns is the active agenda’s to name, not this page’s.

**Across documents.**

- One fact, one home. Where two documents state the same number, one of them should be
  citing the other or the artifact, not restating it.
- No document should be the only place a load-bearing claim appears.
- Claim boundaries survive editing.
  `reported` is not `verified`, `verified` is not the optimum, and a bound on a retained
  witness is not a bound on $s(n)$. These are the sentences most likely to be smoothed
  away, and the ones that must not be.

## New Result Publication

Publish a newly retained result in the same change as its registration.
Start from the accepted evidence and its scope; an unfinished search or a certificate
awaiting a required verification route stays unresolved.
Use
[Registering a First-Party Result](../frontier/README.md#registering-a-first-party-result)
for id allocation, evidence fields, and the review obligations behind the declared
rungs.
For each result, complete this sequence before declaring the change ready to land:

1. Update the owning case under `packing/frontier/`, `evidence.yaml`, and
   `results.yaml`, as applicable, with the accepted claim, verification level,
   provenance, and retained receipts.
   Preserve earlier rungs and historical decisions.
   A result by others is registered too, when the case record acts on it, by stage 3 of
   the [result import process](result-import.md); `check_results` fails while a recent
   case lower bound has no entry.
   Validate those source records before rendering, from `packing/`:

   ```shell
   uv run --frozen python -m devtools.validate_schemas
   uv run --frozen python -m devtools.check_results
   ```

2. Render the result register, evidence inventory, frontier tables, synopsis headline,
   and README’s three results tables (New Results, Results by Others and the recent
   results by case) from those records.
   The README tables are re-rendered, never hand-edited: a result’s row, headline,
   rungs, date, credit and standing all come from the register, the case records and the
   bibliography. From `packing/`:

   ```shell
   uv run --frozen python -m devtools.render_results --update
   uv run --frozen python -m devtools.render_evidence_inventory --update
   uv run --frozen python -m devtools.render_research_tables
   uv run --frozen python -m devtools.render_results_headline
   ```

3. When a result changes an atlas value, badge, label, or geometry, regenerate the atlas
   data:

   ```shell
   uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --update
   ```

   This refreshes the figure data, the witnesses, the house renderings and the manifest.
   The two survey composites, `known-best-1-100` and `known-best-1-324`, are not redrawn
   for a result: each states the data it was drawn from and is redrawn at the next
   version bump, as
   [Release assets](../../development.md#release-assets-are-drawn-at-a-version-bump-or-on-demand)
   says. `--check-composites` lists the cards that now trail.
   When the result should be on the posters before then, redraw them with
   `--update-composites` in a commit of its own, inspect the affected cards in the SVG
   and PDF, and confirm their values and evidence status against the frontier.

   After the data is committed, re-pin the data revision, which is one line and rebuilds
   nothing:

   ```shell
   uv run --frozen --all-extras --group dev python -m devtools.release_pin --update
   ```

4. When a result changes what is known exactly about a best known side (a new best known
   packing, a closed form, a minimal polynomial, a degree, or an identification from a
   contact system), regenerate the exact side values register and its paper:

   ```shell
   uv run --frozen --all-extras --group dev python -m devtools.build_exact_values --update
   uv run --frozen --all-extras --group dev python -m devtools.render_exact_side_values --pdf
   ```

   The register re-checks every polynomial (irreducibility, a unique root in a rational
   interval, agreement with the record and with the independent KKT values), so a new
   fact that fails one of those checks stops here rather than reaching the paper.
   The gate’s `build_exact_values --check` fails while the register trails the records,
   so this step cannot be skipped silently, and the Pages workflow rebuilds the paper
   whenever the register changes.

5. Reconcile the README prose around its generated tables (the introduction’s summaries,
   the $s(11)$ thread under New Results, the machine audits, Earlier in 2026 and the
   Survey section), the synopsis’s current claims, and affected tutorial or survey prose
   against the refreshed artifacts.
   Each result marked `apparently-novel` or `confirmed-novel` gets its row in the New
   Results table from the register; its scoped summary is the register entry and its
   case record, and README prose adds to it only where a reader needs the thread.
   Check older summaries that still call a superseded bound current.
   Link to the record for detail, and distinguish a new bound from a solved case.
   Append dated updates to historical reports instead of rewriting their original
   conclusions.

6. Run the renderers’ check modes, README and synopsis checks, and the applicable
   [validation tiers](../../development.md#validation-tiers).
   The atlas `--check --sample` checks every retained record, composite label, and
   export receipt while rebuilding sampled case geometry; the full `--check` belongs in
   the deferred checkpoint.
   Retain the checked source/base and name each publication surface as updated or
   checked current in the closeout.
   A stacked PR must publish the results present at its own layer.

The generated tables and README result-ID coverage catch an omitted or stale result;
they do not prove the hand-written prose around them correct.
The editorial comparison and generated-artifact checks remain separate obligations.

## Synopsis Research-Status Roll-Up

The synopsis owns the current, reader-facing synthesis of the research program.
Open a roll-up when a frontier result lands, an agenda or consequential session ends,
the selected handoff or owner strategy changes, readiness changes materially, an
explicit state audit is requested, or a release is prepared.
OR-7’s common-edit pass remains due at documentation block boundaries even when none of
those events changes a headline.

Freeze the observation before editing.
Record the ISO date and scientific cutoff Git revision, then inventory the latest agenda
update, the latest terminal session by its recorded end timestamp rather than its
number, the highest exploration, hypothesis, experiment, and frontier-result artifacts
actually present, the live tbd snapshot time, and the exact revision to which validation
will apply. Pause concurrent writers to the records being reconciled.
Counts are a snapshot at that cutoff, not a claim about a moving checkout.

Precedence is fact-specific: each source owns only the fields in its contract.
When sources disagree, use this fact-to-owner map rather than treating one file type as
globally authoritative:

| Fact | Owning source | Derived or reader view |
| --- | --- | --- |
| Agenda and commitment state | Enforced agenda YAML frontmatter | Generated agenda map |
| Session chronology, outcome, usage, and next action | Enforced session YAML frontmatter and retained native receipts | Generated session-close report |
| Exploration scope and forward `proposes` links | Enforced exploration YAML frontmatter | Idea board and synopsis synthesis |
| Hypothesis statement and prerequisites | Enforced hypothesis YAML frontmatter | Registry table in the synopsis |
| Hypothesis status | Ledger precedence applied to experiment and frontier records | Fresh generated ledger and checked synopsis row |
| Experiment invocation, evidence scope, and verdict | Enforced experiment YAML frontmatter plus its retained receipt | Fresh generated ledger and synopsis tables |
| Promoted result registration | `packing/frontier/results.yaml` and its evidence links | Generated `RESULTS.md`, status tables, and headline |
| Strategy, ranking, and selected next entry | Accepted W10 agenda and session closeout, or an explicit operator decision retained in an agenda and session | Current synopsis handoff and active plan |
| Implementation owner, dependencies, holds, and resumability | Live tbd state | Agenda bead links and current handoff; never scientific truth |
| Reader-facing implications and readiness | `SYNOPSIS.md`, after the sources above agree | README orientation and links; no volatile roll-up totals |

Apply the following interpretation rules before writing prose:

- Count files that satisfy the registered filename pattern; never infer a count from the
  highest identifier. Agenda status and commitment state are different fields and must be
  reported separately.
- Order new sessions by their recorded `ended_at` timestamp; a planned deadline is not
  an observed terminal time.
  Sessions before session-128 have no end field, so the checker uses their start
  timestamp as a legacy fallback.
  `stopped` means the declared block ended, not that its work failed.
  Use only the top-level session resource roll-up for totals, because child totals can
  overlap it.
- An exploration is codified only when its `proposes` field links it forward.
  Derive hypothesis status from the freshly checked ledger, and derive an experiment
  decision from its own record and retained receipt.
- `running` or `in-progress` is not evidence that a target ran.
  Require a target receipt or result record.
  A confirmed hypothesis is not a frontier theorem; only the frontier register and its
  evidence promote a result.
- State validation with the exact revision, validation surface, local or hosted
  environment, skipped checks, and outcome.
  “CI passed” without those qualifiers is not a reproducibility statement.

Run the roll-up in order:

1. Validate source records, repair ownership or status conflicts there, and only then
   regenerate the ledger, agenda map, session-close report, results views, defects,
   research tables, and document map.
2. Reconcile the synopsis’s dated status snapshot, readiness boundary, program arc,
   current roadmap, and one selected handoff against those fresh views.
   Reconcile active plans and tbd to an accepted W10 decision or an explicit operator
   decision retained in the agenda and session; route unresolved strategy or selection
   to W10.
3. Reconcile README and the remaining reader-facing documents.
   Link to the synopsis for current state rather than copying its volatile counts.
4. Update the synopsis date only after the complete pass and format edited Markdown.
   Follow [the named validation tiers](../../development.md#validation-tiers): check and
   render records, run the pre-push tier, push, then retain the exact-head full
   checkpoint and hosted-check outcomes.

When two sources conflict, fix the record that owns the fact or file a defect; do not
select the more convenient wording.
Rewrite maintained current-state documents.
Append a dated correction to historical reports so the original claim remains legible in
its time context.

**Generated graphics.** Figures drift the way prose does, and they drift more quietly
because nobody rereads them.

- Run the applicable generators’ checks: `build_known_best_atlas --check --sample`,
  `check_svg_rendering --check`, `render_known_best_contact_overlays --check`,
  `build_prospective_atlas --check`, `build_composite_figure_data --check`,
  `render_document_map --check`. A failure here means the stored artifact no longer
  matches its inputs. The full atlas geometry rebuild runs in the deferred checkpoint; it
  is not a cheap documentation check.
- Then the half no checker does: **a figure can be byte-identical to its inputs and
  still be stale in meaning.** If the record now says something the figure was drawn
  before: a bound moved, a case was added, a claim narrowed.
  The drawing is wrong even though it regenerates clean.
  Read each figure against the sentence that introduces it.
- Never hand-edit a generated artifact.
  If it is wrong, the generator is wrong.
- Composite PNGs and PDFs use the locked CairoSVG dependency and the system Cairo
  library described in
  [Supported Environment](../../development.md#supported-environment).
  Emission precision is pinned at 28 ([D-359](../../defects.md)) with a related check
  still open ([D-362](../../defects.md)); a pass that finds a figure needing a precision
  change is looking at that defect, not at a figure bug.

**Before closing.**

- Every drift either fixed or filed as a defect, with no third option.
- Generated views regenerated: `packing-ledger render`, `devtools.render_agenda_map`,
  `devtools.close_session --render`, `devtools.render_results --update`,
  `devtools.render_results_headline`, `devtools.render_research_tables`,
  `devtools.render_defects`, and `devtools.render_document_map`.
- `devtools.check_synopsis` and `devtools.check_readme` agree with those views,
  including the marked current-research snapshot and the single selected handoff.
- `make format` clean, gate green, and a statement of what was checked *and what was
  left*.

Everything else on this page is convention, and convention is what drifts.
When a rule here is broken and nothing catches it, the fix is a check, not a reminder.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
