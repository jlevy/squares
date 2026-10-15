<!-- A description that is not this section order is unfinished (OR-9).
Cost is 2–4 sentences: what the slice is, the honest wall, what it does not do.
Do not list every experiment. Dispositions are decisions, not probes.
From packing/: `python -m devtools.check_pr_description --file BODY.md`

Before merge, assign exactly one S1–S5 label for the highest genuinely new delivered
contribution, with its rationale in this description. Use the conservative rubric in
packing/campaign/result-import.md, "Label the PR and Prepare News", including its
examples, result inheritance and individual stack-layer rules. The optional project
label is independent of the S score and can accompany S1/S2.
Prepare appropriate News wording or an explicit editorial omission under that policy;
retain actual event dates, source PRs, public artifacts and verification/publication
limits. Check deployment before claiming publication.
-->

## What this branch cost

<!-- Replace this placeholder with the exact generated cost block.
For a terminal agenda, run
`uv run --frozen --all-extras --group dev python -m devtools.close_session --render --session session-NNN --agenda agenda-NNN`
from `packing/`.

Keep Claude and Codex measurements separate when their intervals can overlap.
-->

## New Results and Their Significance

<!-- Omit this section entirely when the branch registered or re-scored no result.
Where it applies it is generated, not written:
`devtools.render_pr_rollup --agenda agenda-NNN` joins `frontier/results.yaml` to the
agenda's wall and emits the rungs with the significance rubric's own wording from
`epistemics.md`.

It sits here, above the dispositions, because the dispositions are keyed on commitments
and a result is a different object.
Agenda 016 is why the section exists: it registered three results, scored all three, and
published a description that gave a significance rating for one of them.
-->

## Results and Dispositions

<!-- Lead with what the work established, not its agenda chronology.
Use the smallest scope with one honest answer.
If there is no result, classify why.
Use `bounded-negative` only when the declared search scope or budget was fully
exhausted; `time-limited` when valid work started but the external wall arrived first;
`guard-refused` when a correct admission, provenance, validity, or safety guard stopped
it; `technical-failure` for unintended tooling or validation failure; `never-opened`
when an upstream dependency never authorized execution; and `inconclusive` when the full
valid protocol ran but its frozen criterion did not decide.

A partial, refused, failed, or unopened attempt is not a negative result.
Every row needs an action: retire-success, retire-negative, continue, fix-and-rerun, or
defer-dependency. -->

| Work or result | What was established | Evidence | Why it stopped | Disposition and follow-up |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Changes by Purpose

<!-- Group code, data, record, and documentation changes by the result they produce.
A branch that adds hosted data (OR-18) gives the release URL, the manifest path, and
the total size.
-->

| Area | Result | Principal files or interfaces |
| --- | --- | --- |
|  |  |  |

## Validation

<!-- Name exact commands, outcomes, counts, skips, and the revision they cover.
-->

- Local:
- Hosted:

## Documentation and Replanning

<!--
For post-agenda work, state the README/SYNOPSIS/related-doc decisions, the surviving
candidate order, any operator revision, and the one selected next entry point.
-->

- Documentation review:
- Selected next entry:
- Deferred candidates:
- [ ] PR has exactly one S1–S5 label, an editorial rationale and its News/changelog
  disposition; project label applied where appropriate.

## Limits

<!-- State what this branch does not establish and what would justify reopening work.
-->

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
