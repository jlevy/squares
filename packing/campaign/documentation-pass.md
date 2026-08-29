# The W8 Documentation Pass — Runbook

How to run a documentation pass, and how to know it is finished.
[`conventions.md`](../../conventions.md) owns the formats this checks against;
[`operating-rules.md`](../../operating-rules.md) owns when a pass is due (`OR-7`). This
page is the procedure between them.

A documentation pass is worth opening when a run has closed several commitments and the
reader-facing tier has not caught up.
It is worth *closing* when every item below has an answer, including the ones whose
answer is “nothing to do”.

**Order matters.** Read the artifacts first, the documents second, and never the
reverse: a pass that starts from the prose inherits the prose’s mistakes.

**Per document.**

- [`README.md`](../../README.md) — the front door.
  Does the first screen still say what the project is and what it has?
  Do the workflow entry points, the directory tree, and every headline number match the
  record? Is the thing a new reader should do first still the first thing offered?
- [`TUTORIAL.md`](../../TUTORIAL.md) — orientation.
  Does every command run, on a clean checkout, in the order given?
  Does it teach the problem before the tooling?
  Does a reader who finishes it know what this project can and cannot certify — and can
  they say why the reported and verified bounds differ?
- [`SYNOPSIS.md`](../../SYNOPSIS.md) — the technical account.
  Does the readiness table match [What Is Built](../../SYNOPSIS.md#what-is-built)?
  Does the handoff point at work that exists, on beads that exist?
  Are the defect aggregates the generated ones?
- [`conventions.md`](../../conventions.md) — Is every `[checked]` claim still checked by
  something, and every `[convention]` still observed?
- [`operating-rules.md`](../../operating-rules.md) — is every rule still one an agent
  should follow, and does each still cite the failure that motivated it?
  Regenerate `AGENTS.md`’s summary with `devtools.render_operating_rules` rather than
  editing it.
- [`development.md`](../../development.md) — do the commands still exist, with those
  flags?
- **A dated document is a record, so a pass adds to it rather than rewriting it.** A
  `research-YYYY-MM-DD-` report states what was known on its date.
  Where the project’s own record has since moved past it, append what now holds and say
  when; do not restate the newer finding as though it were the original one.
  Which dated reports a given pass owns is the active agenda’s to name, not this page’s.

**Across documents.**

- One fact, one home. Where two documents state the same number, one of them should be
  citing the other or the artifact — not restating it.
- No document should be the only place a load-bearing claim appears.
- Claim boundaries survive editing.
  `reported` is not `verified`, `verified` is not the optimum, and a bound on a retained
  witness is not a bound on `s(n)`. These are the sentences most likely to be smoothed
  away, and the ones that must not be.

**Generated graphics.** Figures drift the way prose does, and they drift more quietly
because nobody rereads them.

- Run each generator’s own check, which is the cheap half:
  `build_known_best_atlas --check`, `check_svg_rendering --check`,
  `render_known_best_contact_overlays --check`, `build_prospective_atlas --check`,
  `build_composite_figure_data --check`, `render_document_map --check`. A failure here
  means the stored artifact no longer matches its inputs.
- Then the half no checker does: **a figure can be byte-identical to its inputs and
  still be stale in meaning.** If the record now says something the figure was drawn
  before — a bound moved, a case was added, a claim narrowed — the drawing is wrong even
  though it regenerates clean.
  Read each figure against the sentence that introduces it.
- Never hand-edit a generated artifact.
  If it is wrong, the generator is wrong.
- Two known limits, so a pass does not rediscover them: the composite PNG needs macOS
  `sips` or ImageMagick 7 and cannot be regenerated on a stock Linux runner, and
  emission precision is pinned at 28 ([D-359](../../defects.md)) with a related check
  still open ([D-362](../../defects.md)) — a pass that finds a figure needing a
  precision change is looking at that defect, not at a figure bug.

**Before closing.**

- Every drift either fixed or filed as a defect, with no third option.
- Generated views regenerated: `packing-ledger render`, `devtools.render_defects`,
  `devtools.check_synopsis`.
- `make format` clean, gate green, and a statement of what was checked *and what was
  left*.

Everything else on this page is convention, and convention is what drifts.
When a rule here is broken and nothing catches it, the fix is a check, not a reminder.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
