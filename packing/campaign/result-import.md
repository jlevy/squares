# The Result Import Process: Runbook

An import starts from an input: an issue or a comment on this repository, a message from
the owner, a count the Kingbird catalogue moves, a new release of another catalogue, or
a commit in a repository whose results the record carries.
Everything below follows from that input, and ends with the result registered, validated
and rated in this record and its author answered.
[Intake Sources](#intake-sources) says where inputs arrive and how each is read, and an
[intake pass](#running-an-intake-pass) reads all of them at once.

This page holds the sequence, and the few rules that belong to no single record.
The rest has an owner, and is not repeated here:

- [`epistemics.md`](../../epistemics.md#results-by-others) owns which results enter, how
  their evidential status, the `V`, `C` and `S` ratings, and the three end points.
- [Attribution Policy](../../attribution.md) owns person names, handle reconciliation,
  lineage credit, project and tool attribution, and case-specific exceptions.
- [The frontier README](../frontier/README.md#adding-or-reviewing-a-result) owns the
  rules and fields of the records.
- [The synopsis](../../SYNOPSIS.md#result-import-and-efficient-confirmation) owns the
  workflow contracts, and how a W2 phase chooses and prices a check.
- [New Result Publication](documentation-pass.md#new-result-publication) owns the
  commands that render and check a changed record.

## Running an Intake Pass

An intake pass brings the record up to date with every source at once.
It runs when the owner asks for one (“run the intake”), not on a schedule, and it is one
W1 phase on one branch:

1. **Sweep.** From the repository root, run `make intake`. It captures the Kingbird
   catalogue into `attic/intake/`, then runs
   [`devtools.intake_sweep`](../devtools/intake_sweep.py), which reads every source in
   [the table below](#intake-sources) and prints each item the record has not taken in,
   and under **Regularization owed** each count whose drawing still waits for the strong
   generators, with the bead that owns its runs.
   It exits nonzero while any item lacks an open bead to own it, or waits on something
   that has already happened.
   Read **Needs Action** first, then **Not Checked**: a source the sweep could not read
   is not a clean source.
2. **Own each item** as [stage 0](#stage-0-sweep) says: a bead for each new result, a
   recorded read where there is nothing to import, a new owner for any deferral whose
   bead has closed, a restart for any wait whose blocker has resolved, and an open bead
   for each count pending regularization that none owns, named in the count’s
   `default_drawings.PENDING_ALLOWED` entry.
3. **Import** each new result through stages 1 to 3 on the same branch, triaging every
   one before anything heavier runs ([stage 1](#stage-1-triage)). Where several open
   reports state upper bounds at one count, the
   [report-order ledger](#several-reports-at-one-count) decides which stage 3 records.
   A stage 4 replay runs in the branch when it fits under the pass’s
   [compute cap](#the-compute-cap-and-the-validation-backlog); a larger one waits in its
   validation bead. Start each new proof’s mathematical review as soon as its source is
   retained, in parallel with stage 3, by [stage 4’s review lane](#stage-4-validate).
   It does not wait for a replay budget, and it lands in a pull request of its own when
   it returns. Where a validated result is smaller than a case’s house best packing, the
   pass adopts it ([the house rule](#the-house-rule)). **Every new house best packing is
   regularized** in the pull request that makes it one
   ([stage 5](#adopt-a-house-then-regularize-it)), whichever import made it: the
   adoption of a register result like T-174 or T-186 to T-190, a Kingbird catalogue
   intake, or an exact re-solve that changes a house best packing.
   None defers its runs: they run in the pull request that makes the change, under the
   item cap (the owner’s 40 CPU-hours where the pass sets none), and an adoption too
   large for one is split, its other counts waiting with their runs, never apart from
   them. Only a witness corrected or re-solved with its source and exact side unchanged
   may defer its runs, in `default_drawings.PENDING_ALLOWED` with the open bead that
   owns them, naming the witness it replaced in `default_drawings.CORRECTED`. The sweep
   then lists each count still owed.
4. **Validate** from `packing/` with `packing-validate --records`, `--edit` too where
   the pass changed code, and the tests the change directly affects; leave `--fast` to
   CI, which gates the draft pull request ([stage 5](#stage-5-publish)).
5. **Open one draft pull request** with `tbd shortcut create-or-update-pr-simple`,
   labelled `intake`. It lists each item with its bead and the stage it reached, and
   every source under Not Checked.
6. **Render the announcement** of the results the pass registered, from `packing/`:
   `uv run --frozen --all-extras --group dev python -m devtools.render_announcement
   --ids T-NNN … --github`, with the pass’s own `T-NNN`. Select by id, not with
   `--since`: the date the register received a result also picks up what other passes
   registered that day.
   [The tool](../devtools/render_announcement.py) prints a dated header and one brief
   line per result, crediting its finders by an X handle the record or their GitHub
   profile declares and by full name otherwise, never the owner, and says on stderr what
   it left out and where each handle came from.
   Put its output in the pull request description under **Announcement**, for the owner
   to post; an agent never posts it.
   **A result the pass registers at S4 or S5, or raises to either, also owes a News
   item**: draft it in the description under **News**, and land it in the first change
   after the merge ([Announce a Significant Result](#announce-a-significant-result)).
   Until it does, the records tier fails the next pull request that changes the register
   or News, and warns on any other change.
7. **Draft the replies** in each issue’s answer bead: every issue the pass touches gets
   one. Once the pull request merges, render each from `main`, check that `main` and the
   deployed site say what it says, post it, and record it under the issue’s `replies` in
   the next change ([stage 7](#stage-7-answer)). Where a ledger decided the pass’s
   counts, each result issue also gets a
   [report-order verdict comment](#report-order-verdict-comments).
   Once the deploy is verified, run `check_requests --report` and close each closeable
   issue with its final comment ([Close a Settled Issue](#close-a-settled-issue)).
8. **Sweep again** with `make intake`, after the branch’s changes to the records and
   again after the merge.
   The sweep, like `check_requests --report`, is what finds the replies due: it lists
   `#N owes a reply` until a recorded reply covers the issue’s state, and lists each
   closeable issue still open under **Needs Action** until it is closed.
   Each new item it finds is triaged read-only, with a proposed disposition, before any
   of it is worked ([stage 1](#stage-1-triage)). The pass is done when nothing needs
   action, every count it re-housed is regularized or owned by an open bead under
   **Regularization owed**, and every reply it owes is posted and recorded, or when the
   pull request says why each remaining item waits.

The pass needs network access to `github.com`, for Git and for the API through `gh`;
`kingbird.myphotos.cc`, for the catalogue capture; `evand.github.io`, for imports from
Evan Daniel’s site, which his repository builds; and `pypi.org` with
`files.pythonhosted.org`, for the pinned transcriber.
A source the environment denies is reported as not checked, and the pull request says
so. On 2026-10-05 the agent sessions reached GitHub and PyPI and nothing else.

A pass never merges without the owner’s word, never pushes to `main`, never posts the
announcement, and never starts a replay above the compute cap the owner set for it, or
with no cap set, one measured in CPU-hours.
It does answer the issues, under the `github-workflows` grant (`tbd policy show`); the
owner’s standing instruction of 2026-10-11 is why the rule exists.
It comments on every issue it touches ([stage 7](#stage-7-answer) says what touching is)
and follows up each later change of its state, each comment posted once the pull request
that carries the change has merged, and it closes an issue only with its final comment.
Without the grant it drafts each reply in the issue’s answer bead and asks the owner to
post it. The owner may post instead.
Under the same grant it adds the `intake` label, and a case label where one applies; it
edits nothing else on an issue without the owner’s word.

**The day a result lands.** Every register entry carries `landed`, the UTC day it
reached `main` and the site, which the results page’s Added in the Last Seven Days and
its Added filters read; the schema requires it.
A lane writes it with each new entry, as the day it registers it
([stage 3](#stage-3-record)). When the owner gives the word to merge, the branch’s last
two commits re-date the branch’s new entries to the merge day and re-pin
([stage 5](#stage-5-publish), Before merge).
The same stamp dates a branch’s new house best packings and new sources of dated
beyond-horizon rows in `packing/frontier/landings.yaml`, which the home page’s Recently
Added places them by; a test fails until every adopted count and row source has its day.
A forgotten re-date leaves that pull request’s entries a day or two early and turns
nothing red. The sweep after a merge runs `python -m devtools.stamp_landed --audit` from
`packing/`, which compares every entry on `main` with `main`’s first-parent history and
gates nothing; `--audit --apply` writes its corrections, which ride the next records
pull request.

### The Prompt

A session asked to run the intake takes this as its instruction:

```text
Run an intake pass on jlevy/squares by packing/campaign/result-import.md, section
"Running an Intake Pass". Work on a new branch from origin/main named
claude/intake-YYYY-MM-DD, with today's date.

1. Bootstrap the clone as AGENTS.md, "A fresh clone", says; run `tbd prime` and
   `tbd policy show`.
2. From the repository root run `make intake`. Read the report: "Needs Action"
   first, then "Not Checked", then "Regularization owed".
3. For each item that needs an owner, look for an open bead that already covers it
   (`tbd list --label result-import`). Otherwise open one bead per new result,
   labelled result-import and titled "Import <author>: <claim> (#<issue>)", or
   "(no issue)" when nothing on GitHub asked. A watched repository whose new commits
   hold nothing to import gets a read in packing/campaign/intake-watch.yaml instead,
   with a note saying what changed. A deferral whose bead has closed gets a new owner
   or is resolved. An item whose blocker has resolved is resumed on this branch, or
   its bead says what it waits on now. An issue that reports a new item for intake
   (a result, a counterexample or a method) and lacks the `intake` label gets it under
   the github-workflows grant (`gh issue edit N --add-label intake`), and the case
   label too where one applies (development.md, "Issue and Pull-Request Labels");
   without the grant, list those issues for the owner. A count pending
   regularization that no open bead owns gets its runs in this pass, or an open bead
   labelled regularization (and validation, with stage 4's block and a backlog row,
   where its runs are held above the cap), named in the count's PENDING_ALLOWED
   entry in default_drawings.py by this pass's pull request: the sweep counts the
   count owned only once the entry names the bead. Run `tbd sync`.
4. Take each new result through stages 1 to 3 of the runbook on this branch: triage,
   retain the source in a packet at a pinned revision, register it as reported.
   Triage every result before any large token or CPU spend. Where several open
   reports state upper bounds at one count, run the report-order ledger before
   registering (stage 1, "Several Reports at One Count"). Run a stage 4 replay only
   when it fits under the compute cap the owner set, recorded on the pass's epic bead,
   or with no cap, when the source prices it at minutes; otherwise give it a
   validation bead and a row in the backlog bead (stage 4, "The Compute Cap and the
   Validation Backlog"). Start each new proof's mathematical review (stage 4, "Who
   reviews, and when") as soon as its source is retained, in parallel. Then follow
   stage 5, "The House Rule", and the adoption steps after it: adopt each validated
   result smaller than a case's house best packing in this pass, whoever found it, and
   regularize each count where any import changes the house best packing in the same
   pull request, within the item cap (the owner's 40 CPU-hours where the pass sets
   none), never deferring its runs to default_drawings.PENDING_ALLOWED. Only a witness
   corrected or re-solved with its source and exact side unchanged may defer its runs,
   naming the witness it replaced in default_drawings.CORRECTED.
5. From packing/, run `uv run --frozen --all-extras --group dev packing-validate
   --records`, `--edit` too where the pass changed code, and the tests the change
   directly affects, and fix what fails. Hosted CI is the draft's full test gate.
6. Commit, push the branch, and open one draft pull request, labelled intake, with
   `tbd shortcut create-or-update-pr-simple`. List every item with its bead and the
   stage it reached, and every source the sweep could not check. Before merge, assign
   exactly one S1–S5 significance label and prepare the News disposition by stage 5,
   "Label the PR and Prepare News". Add project where the PR delivers a site or
   project capability.
7. From packing/, run `uv run --frozen --all-extras --group dev python -m
   devtools.render_announcement --ids T-NNN ... --github` with the T-NNN this pass
   registered (not --since, which also picks up other passes' results), and add its
   output to the pull request description under "Announcement", for the owner to
   post. Do not post it. For each result registered at S4 or S5, or raised to
   either, draft its News entry under "News" too, and land it in the first change
   after the merge (stage 7, "Announce a Significant Result"); until it does, the
   records tier fails the next pull request that changes the register or News.
8. Draft the reply each issue the pass touches is owed in its answer bead; every one
   gets a comment. Once the pull request merges, render each from main with
   `check_requests --draft N`, check that main and the deployed site say what it says
   (runbook stage 5, "Verify the Published Result"), post it, and record it under the
   issue's replies in result-requests.yaml in the next change. Where the ledger
   decided the pass's counts, draft each result issue's verdict comment with
   devtools.intake_comments (stage 7, "Report-Order Verdict Comments"). Once the
   deploy is verified, run `check_requests --report` and close each closeable issue
   with its final comment (stage 7, "Close a Settled Issue"). A question to the
   author goes under the issue's awaiting_author and holds it open only when the
   record asserts something the answer could falsify and no measurement here can
   settle it; any other goes in the closing comment. Post nothing on, and close
   nothing of, an issue held for the owner (held in result-requests.yaml).
9. Run `make intake` again, and again after the merge: it and
   `check_requests --report` list the replies still due, and its "Regularization
   owed" lists every count still pending where this pass changed the house best
   packing. Triage each new item it lists read-only and propose its disposition on
   the epic bead (stage 1). Report every item that still needs action.

Never merge without the owner's word, never push to main, never post the announcement,
and never start a replay above the owner's compute cap for the pass, or with no cap
set, one measured in CPU-hours. Under the github-workflows grant, comment on every
issue the pass touches (runbook stage 7 says what touching is) and follow up each
later change of its state until the issue is closed with a final comment; the owner's
standing instruction of 2026-10-11 is why. Without the grant, draft each reply and ask
the owner to post it. Post only after the pull request that carries the change has
merged, link only to main, and check first that main and the deployed site say what
the comment says; the verdict comment is the one exception, on the condition stage 7,
"Report-Order Verdict Comments", states. Add the `intake` label, and a case label where
one applies, under the github-workflows grant; edit nothing else on a GitHub issue
without the owner's word. If github.com, kingbird.myphotos.cc or evand.github.io is
unreachable, say so in the pull request and continue with the rest.
```

## Intake Sources

Every input reaches the record through one of these sources, and the sweep reads each.

| Source | How it is read | What an item becomes |
| --- | --- | --- |
| GitHub issues and comments | `check_requests --github` lists the issues `result-requests.yaml` lacks, the replies missing from it, the comments created or edited after an entry’s `read_through`, and the `result-report` entries and entries marked `intake: true` whose issues lack the `intake` label | A new issue: an entry with `triage: pending`, an import bead and, when it reports a new item for intake, the `intake` label. A comment: its claims mapped into its issue’s entry, and `read_through` moved |
| Owner and other manual reports | Nothing reads them: a message, a link pasted to an agent, a result named in a review | A bead labelled `result-import` first, titled with `(no issue)`; then stage 1. The sweep lists the open ones |
| The Kingbird catalogue | [`devtools.capture_kingbird_catalogue`](../devtools/capture_kingbird_catalogue.py) fetches and transcribes it into `attic/intake/`; the sweep compares the newest capture with the record’s, count by count | A count whose side drops below its record: an import, or a `pending_catalogue_intake` entry with its bead. Other changes: classified when the retained capture is refreshed. None when nothing moved |
| Other catalogues and releases | Read by hand: the register’s other `current-catalogue` and `first-party-release` sources, UnitSquare’s release today. The sweep prints when each was last reviewed | A later release: an import. Nothing new: the source’s `reviewed` date moves |
| Watched repositories | Every repository the source register, a packet’s acquisition record, or the site’s list of other projects names. `git ls-remote` reads each head, and a fetch of commits and trees finds the commits past every pin and every read, and the commits a pin contains whose changed paths no packet at or after them retains | A new result: an import bead, then a packet at the head. New evidence for a registered entry: an evidence update. Nothing to import: a read in [`intake-watch.yaml`](intake-watch.yaml) |
| The record’s own queues | Counts pending catalogue intake, deferred conflicts, results and asks queued on open issues, triage and replies owed, the validation backlog | Nothing new: each names an open bead, and one whose bead has closed gets a new owner |
| The regularized layer | `atlas/known-best/default-drawings.json`’s `states` against `default_drawings.PENDING_ALLOWED` and `SETTLED`: each count pending regularization, each decision that still owes runs or an outcome, each exemption, and whatever the regularization-state gate fails on | Nothing new: each names an open bead. A pending count the list does not name, or whose bead has closed, gets its runs or an owner |
| Blocked imports | A queued result’s or ask’s `blocked_on`, and what an open `result-import` bead says it waits on or depends on, read through `gh` and the bead store | A blocker that merged or closed: the wait resumes, or the bead says what it waits on now |

The capture is the network half of the dated research survey that refreshes the retained
catalogue ([the frontier README](../frontier/README.md#source-coverage-and-freshness));
it writes only to `attic/`, and taking a capture into the record stays a W1 change of
its own. No validation tier runs either command.
From `packing/`, `python -m devtools.intake_sweep --offline` skips the two network
steps, and `--json` prints the whole sweep.

## The Sequence

| Stage | Workflow | Exit |
| --- | --- | --- |
| 0. Sweep | W1 | Every input the sweep lists has an open bead, or a read that records nothing to import, and so does every count it lists as owed regularization |
| 1. Triage | W1 | A claim map and a priced validation plan in the import’s bead; the author acknowledged |
| 2. Retain | W1 | The source in a packet at a pinned revision, with its bibliography key |
| 3. Record | W1 | The claim registered as reported, with its coverage entry, and merged: *imported* |
| 4. Validate | W2 | Replay evidence, a mapped review and the rungs they derive: status `confirmed`, or `incomplete` |
| 5. Publish | The change that moves the record | The reader documents state the result, and each count it re-houses is regularized in the same change; once stage 4 has passed, *integrated* |
| 6. Explain | W8, with a W2 review | A review paper, for the results that warrant one |
| 7. Answer | After each merge, by the pass | A reply on the issue for each change of its state, to the final comment, and a News item for each S4 or S5 result: *answered* |

Stage 0 finds the inputs, stages 1 to 3 are the import, stage 4 is the correctness part,
and stages 5 to 7 are the publication.
It is a sequence of ordinary workflow phases, not a workflow of its own, and each phase
is declared as any other is.

Two rules shape every import:

- **One bead.** Each import has a bead labelled `result-import`, titled
  `Import <author>: <claim> (#<issue>)`, or `(no issue)` when nothing on GitHub asked,
  that holds the claim map and stays open until the author is answered, or until the
  result is integrated where no author asked.
- **Two pull requests.** Stages 1 to 3 merge on the day the result is first seen.
  Stage 4 merges when its replay and review are done, which can be days later.
  A reported result is then visible while it waits, and no branch holds an unmerged
  `T-NNN` for long. That is the separable boundary for which
  [`OR-9`](../../operating-rules.md#or-9-a-pull-request-leads-with-what-the-branch-cost)
  allows a second pull request.

## Stage 0: Sweep

The sweep finds the inputs and decides nothing about them.
Its exit is that every item it lists has an owner and nothing waits on what has
happened:

- **A new result gets a bead** labelled `result-import` and titled by the convention
  above. Look for an open one first, since another session may have opened it.
- **An issue that reports a new item for intake gets the `intake` label** on GitHub.
  The item is a result, a counterexample or a method.
  In [`result-requests.yaml`](result-requests.yaml) such an issue is a `result-report`,
  or an entry of another kind marked `intake: true`, such as a defect report with a
  counterexample (#295, #308) or a method report (#367). The project’s own issues that
  track the intake of a reported item carry the label too, as #532 to #537 do; an issue
  that tracks other work does not.
  Under the `github-workflows` grant the pass adds the label with
  `gh issue edit N --add-label intake`, and the case label as well where one applies
  (`--add-label n-17,intake`), as
  [the label policy](../../development.md#issue-and-pull-request-labels) says; without
  the grant, it lists those issues for the owner.
  The sweep lists each `result-report` entry and each entry marked `intake: true` whose
  issue lacks the label.
  The owner asked for the label on 12 October 2026, when no issue carried it.
- **A watched repository with nothing to import gets a read** in
  [`intake-watch.yaml`](intake-watch.yaml): the head, the date, and a note saying what
  the commits changed, so the next sweep starts there.
  A read that names a bead holds a result back for later, and is removed once a packet
  pins that commit. A pin is an acquisition record’s commit, retaining the paths the
  record declares, or a revision in a register source’s address, retaining the path the
  address names after it (`/tree/<commit>/<path>`) or the whole tree when it names none.
  Where both pin one commit, the acquisition record’s scope stands: the register’s
  address says what it cites, not what was retained, and reading it as the whole tree
  hid every earlier commit no packet took in.
  A commit a README names in prose pins nothing, because prose that names a commit is as
  likely to say it was left for an import of its own, as Hiroaki Hosono’s 4 October
  packet said of `c56b9b7` and `1ebd484`.
- **A Kingbird count that drops below its record** is a result by others, imported like
  any other. Where the register cannot take it yet, it is declared under
  `pending_catalogue_intake`, with its bead and the day it was recorded.
- **A deferral names an open bead.** Whatever the record holds back for later names the
  bead that owns it: a pending catalogue intake, a deferred conflict, a read with
  something to import, an open issue’s `answer_bead`, and a queued result or ask, which
  names its own `bead` because the answer bead owns the reply and not the import.
  The schemas refuse a pending intake or a deferred conflict without one, and
  `check_bead_tree` fails any deferral whose bead is not open, `in_progress` or
  `blocked`: one that is closed, deferred or does not exist.
  The three Kingbird counts held on 2026-09-30 named none, and the record trailed the
  catalogue for five days
  ([the postmortem](../../docs/project/postmortems/postmortem-2026-10-05-orphaned-catalogue-intake.md)).
- **Closing a bead a record names takes a record edit in the same change**: a new owner
  for the deferral, or the deferral resolved.
  The bead store changes with no tracked change, and a continuous-integration checkout
  reads it, so the gate fails a dead deferral only in a change that touches a record
  declaring deferrals (`source-coverage.yaml`, `result-requests.yaml` or
  `intake-watch.yaml`), and reports it as a warning anywhere else.
  A bead closed with its deferral left in place passes every other change and fails the
  next one to touch that record; `check_bead_tree` run directly, and the sweep, list it
  whatever changed.
- **A wait names what it waits on.** A queued result or ask gives it as `blocked_on`, a
  pull request or issue as `owner/name#N` or a bead, and the wait is over once every one
  has resolved. A bead declares it on a line of its own in its description or its notes,
  `blocked_on: jlevy/squares#305, think-wpuu`, read the same way; the last such line
  stands, so a note that adds `blocked_on: none` ends the wait.
  Without one, a sentence of the description in the present tense says it, such as
  “waits for jlevy/squares#305”, and a `blocks` dependency always does.
  Prose in the notes is never read: notes accumulate, and the sweep once took “was held
  for #305, which merged” and another bead’s example of a wait as waits still open.
  Nothing resumes a wait when its blocker resolves, so the sweep reports it: Hosono’s 4
  October certificates waited for #305, which merged that evening, and stayed queued.
- **A drawing owed regularization names its bead.** Every new house is a new witness,
  and its count reads `pending` in `default-drawings.json` until both strong generators
  decide it, whichever import made the house: an adoption, a Kingbird catalogue intake
  or an exact re-solve.
  The sweep’s **Regularization owed** lists each pending count with the bead its
  `default_drawings.PENDING_ALLOWED` entry names, each decision whose `owed` names a
  bead, and each exemption.
  A pending count that the list does not name, or whose bead is no longer open, needs
  action: its runs in this pass, or an open bead that owns them, labelled
  `regularization` (and `validation`, with stage 4’s block and a backlog row, where the
  runs are held above the cap) and named in the count’s `PENDING_ALLOWED` entry
  ([stage 5](#adopt-a-house-then-regularize-it)). The entry is made by the pull request
  that corrects the witness, never by one that re-houses the count, whose runs are owed
  in that pull request ([the house rule](#the-house-rule)); for a count re-housed
  earlier whose bead has since closed, this pass’s pull request names the new bead.
  The owner, 16 October 2026: “we should make sure all of the intake process covers the
  regularization and we update that for any other new packings we have.
  That should be part of our standard process to do the regularization.”
  The adoptions of #553, #598 and #614 had left twenty counts without that decision, and
  n = 176 drew its raw house on the site until the owner saw it (think-sfas).

## Stage 1: Triage

Triage decides what the import is before anything is retained, in an hour or less.
Every result a pass finds is triaged before the pass spends heavily on any of them, in
tokens or in CPU, so the owner sees the whole intake first.
An item the closing sweep finds is triaged the same way, read-only: read the source at
its head and propose one of three dispositions on the pass’s epic bead, an import bead,
an evidence update on the bead that owns the result, or a read in
[`intake-watch.yaml`](intake-watch.yaml).

1. **Pin the source**, the author’s own publication and not a report of it, at a full
   commit id or a DOI with file checksums: its current head, unless the claim depends on
   an older revision.
2. **List every claim the release makes**, including those the request does not mention.
   Issue 227 asked about $n = 102$ and $103$; the source held 49 packings.
   A claim in scope that the request does not mention becomes an import of its own.
3. **Map each claim to the register** by the table below, and say who else holds each
   value. Where other open reports state an upper bound at the same count, the
   [report-order ledger](#several-reports-at-one-count) decides which are recorded.
4. **Price the validation:** the checkers a complete replay needs, the cost the source
   reports, and whether anything here decides the certificate without the source’s code.
   A missing tool is a W7 slice, and the plan says so.
   A replay the pass does not run gets a validation bead
   ([stage 4](#the-compute-cap-and-the-validation-backlog)).
5. **Open the bead and draft the acknowledgement:** what was received, the revision
   pinned, and what will be checked.
   It is posted by [stage 7](#stage-7-answer)’s rule, once the pull request that carries
   the triage has merged.
   It states no `T-NNN` and no rung unless that pull request registered the result, and
   then it is the import reply as well.
   A result that reached the record with no issue and whose draft significance is `S4`
   or above gets an issue the project opens for it, labelled `intake`, so its intake,
   review and validation have one public place (the owner, 2026-10-14: “for significant
   items S4+ we should create an issue ourselves for tracking purposes”);
   [jlevy/squares#603](https://github.com/jlevy/squares/issues/603) was the first.

| Claim | Register action |
| --- | --- |
| A bound or an exact value the record does not hold | A new entry; each exact value has its own |
| Bounds of one kind at several counts in one release | One entry whose `scope` covers them |
| A later release that raises an earlier entry’s values or adds counts | A new entry; the earlier one keeps its claim, and the case records decide which is current |
| A theorem with an unbounded parameter | One entry stating the theorem, whose `scope` lists the cases this record holds |
| A second certificate for a value the record holds | A new `simplification` entry, or a `formalization` entry where a proof assistant checked it |
| A consequence of another claim, such as monotonicity, at a count where the record holds no such value | Its own entry only when it settles a case; otherwise the parent’s `scope` covers it |
| A consequence that another entry already registers | No new entry and no change of scope: both stand, and the older claim gains a sentence naming the newer route |
| New evidence or an author’s answer about a registered entry | No new entry: the source retained at the revision that holds it, and an evidence update |
| A request for a result already registered | No new entry: link the issue and continue from the entry’s stage |
| Below the standing bound and asking for no work | None; it stays in the packet |

### Several Reports at One Count

When two or more open reports state an upper bound at the same count, the owner’s rule
of 2026-10-14 decides which are recorded: “If they are reported in order, then each one
should be recorded as a result, as long as each one is stronger than the last.
If a stronger result is reported first, then the other one should not be recorded since
it’s weaker after that, unless there’s some key reason it should be recorded.”
[`devtools.intake_ledger`](../devtools/intake_ledger.py) applies it to an intake
directory, `campaign/issue-intake/<subject>-<YYYYMMDD>/`, and its module docstring owns
the inputs and the comparison:

- **The start** at each count is the record on `main`, frozen in `starts.yaml` at a
  named `main` commit: both upper lanes of the case record, any smaller register bound
  pending adoption, and above the horizon the beyond-horizon row or the grid.
- **The order** is the time each claim reached this repository: the issue, comment or
  pull request that made it, or the update comment or commit that added it later.
  A certificate published in a watched repository with no issue is a report from its
  first commit (the owner, 2026-10-14).
- **The comparison** reads each printed side as the span its rounding allows (`up`,
  `nearest`, `unstated`, `cut` or `binary64`), or as its exact side where a lane or the
  certificate gives one.
  A claim is recorded when every number it may be is below every member of the standing
  side. A tie stays with the earlier report, and a comparison the printed precision
  cannot decide is undecided, never guessed.
- **A refinement** of a standing packing is recorded like a new packing and credited to
  its finder after the finder of the packing it refines, as a regularization
  ([stage 3](#stage-3-record)), unless it restates the report below the print.

**One report registered as two entries is credited in both.** A tie stays with the
earlier report, but two register entries can carry one report: T-073 and T-080 register
one certificate of wand125’s 2 October release, and T-083 and T-084 one paper of
Karakuş’s. When every tied entry carries the identical attribution, the same source keys
at the same date, each is credited as current: the owner’s answer of 24 October 2026,
“Credit both (Recommended)” (think-33u4).
[`devtools.profile_records`](../devtools/profile_records.py) applies it to the profiles’
Records, and a tie between attributions that differ in any way is still ordered by
publication date, or left unassessed.

Beyond the corpus the owner’s answers of 23 October 2026 are rules of the walk.
The ledger’s `rulings` list names each one it applies, and the module docstring of
`devtools.intake_ledger` owns them.
The answers are quoted as the decision beads record them; the rest of each item is the
record’s statement of the rule:

- **A restatement is not recorded** (think-fwa9): “sub-print re-certifications are
  RESTATEMENTS, not new rows.
  The earlier certificate stays the row”.
  The record reads a sub-print re-certification as a side below an earlier report at its
  count by less than one unit in the 12th place, with both rounding up to the same
  12-place print. The walk measures the distance to the member of the standing side the
  claim is closest below, a report and not a construction; whether the answer also
  reaches a side within the print below a construction is open (think-oqjd), and no such
  side exists to 1024. A claim in the ruling’s words that an earlier ledger recorded and
  the answer did not name waits on the owner (`awaiting_owner`). #719’s 631 is the one
  such claim to 1024: another holder’s re-certification of Couzo’s `4e4c8ce`
  certificate, which #722 recorded (think-oqjd).
- **Göbel’s classical constructions are earlier reports** (think-8krd,
  [#613](https://github.com/jlevy/squares/issues/613)): “Goebel’s classical
  constructions count as earlier reports beyond n = 324 (the baseline): a rational row
  above Goebel’s exact side is not recorded.”
  At each count the least side of the three families the Kingbird catalogue states, at
  that count or by deleting squares from a larger one, joins the start, so a rational
  side at or above it is not recorded.
  The 15 October packet’s retained program computes it exactly to 1073, where its reach
  ends, and a count beyond that is refused.
  A register row above it stays listed and is marked
  ([frontier README](../frontier/README.md#source-coverage-and-freshness)). From the day
  of the answer (`intake_ledger.GOEBEL_FROM`) every reading takes it beyond 324: a start
  `gather` freezes holds it as a member, the claims importer compares each certificate
  with it (`upper_bound_reports.goebel_construction`), and so does the replay’s standing
  side. `intake_ledger check`, `render` and `gather` hold a ledger read from that day
  with claims beyond 324 to both of that day’s answers (`answer_problems`). It lists the
  `restatement` ruling through every such count, and takes Göbel’s construction at each
  one through its `classical-constructions` ruling or a member of its frozen start.
  Otherwise it names the answer it leaves out under `rulings_not_applied` with the
  reason, which its README shows, or the check fails.
  A reading from before keeps what it froze, so the earlier ledgers and claim records
  stand as written. #732’s walk, read on the day of the answer, is the one frozen before
  the rule: its `starts.yaml` holds no Göbel member, its `classical-constructions`
  ruling seeds the construction at each count it walks instead, and `check --tree`
  reports those counts as drift.
  The Fang inventory stays on recorded rows, since it measures the excess over what the
  record holds (think-a75a).
- **A certificate its author withdrew from an issue is not a report** (think-8m4k): “a
  watched certificate its author withdrew from an issue, claiming a lower file later, is
  NOT a report.” A file in the author’s watched repository that his issue withdrew, where
  his later release claims a lower side at that count, stays among the walk’s
  publications. The walk keeps it out of the record
  (`beyond_horizon_replay.Held.answer`), and no verdict rests on it.
- **A deletion bound is an earlier report** (D6 on think-f2io). The owner selected the
  option labelled “Yes, an earlier report (Recommended)”. The rest is the question the
  coordinator asked, not the owner’s words: whether a side obtained by deleting a square
  from a neighbour’s certificate, as Couzo’s 985 from his 986, is an earlier report,
  with that option described as “A published deletion bound counts like any stated
  bound; a later equal or higher side is not recorded”.
  So a bound one square below the next count’s published certificate is a report from
  the publication that states it, and #732’s 985, which ties Couzo’s `4e4c8ce` bound
  there, is not recorded.
  The walk records the bound and the chain passes over it.
  That it has no row of its own is the decision’s recommendation, not yet the owner’s
  word; think-kzme asks that, whether an issue claiming the count (743, 798, 855, 985)
  gives it a row, and about the three bounds that delete two or three squares (751, 752
  and 927), which stay held.
  A deletion from a construction no certificate file states, as 23aff0c’s from
  Friedman’s, waits with that construction (D2, think-zkxy).

Transcribe each report’s claims into the directory’s `sources.yaml`, then, from
`packing/`, run `python -m devtools.intake_ledger gather DIR` (`--snapshot` reuses the
saved `github-issues.json`; `--refresh-starts` freezes the starts again), `render DIR`
with `--write` and then `--check`, and `check DIR`. Stage 3 registers what `ledger.json`
records, and nothing it does not unless the owner names a key reason.

The owner has named one standing key reason, the [house rule](#the-house-rule): a claim
validated exactly below the case’s verified upper bound, and undecided only against the
reported lane’s print of the packing the verified lane certifies, is recorded.
The pass lists it under the ledger’s `exceptions` with the house rule as its reason, and
asks the owner nothing more: “This should be built into our policy.
It shouldn’t even be a question.
If there’s any ambiguity on that, we should fix that in our process docs for intake.”
(the owner, 16 October 2026). PR #622 at 29 was the first (T-195): 1.57e-36 below
T-155’s exact side, and 9.19e-15 above the catalogue’s print $5.93383346267692$, within
one unit of its last place.

A comparison the prints leave undecided, and an exact decision later settles, is
transcribed into `sources.yaml` as the claim’s `record_relations`: the case lane’s value
and exact form as `starts.yaml` froze them, or a pending register entry’s id and stated
value; the relation and its margin; and a `read_from` naming the decision’s receipt and
tool. The 14 October ledger’s PR #574 rows are the example
(`upper-bounds-20261014/undecided-resolved.json`, from
`devtools.decide_undecided_comparisons`).

The ledger’s README lists what the rule leaves to the owner, without deciding it: how a
publication in a watched repository is read, key-reason candidates, an identity measured
against what the source says, refinement chains, exact ties between holders, a
certificate committed before the report that holds its count, undecided comparisons and
claims of unknown time.
The pass puts these to the owner in its pull request.
A decision that holds for later passes becomes a rule where the rules on its subject
live: this runbook, or [epistemics.md](../../epistemics.md#results-by-others) for
credit.

## Stage 2: Retain

- **The packet** holds one subject of one source at one pinned revision.
  It goes under [`../resources/web/`](../resources/README.md), named
  `<author>-<subject>-<date of the pinned revision>`. Its README records the address,
  the pin and its date, the retrieval time, the licence, what the source’s attribution
  files say about credit and AI assistance, what is retained and what is not, a manifest
  with digests, and the issue.
  It retains every repository the certificate needs, such as a checker pinned in another
  author’s repository.
  A later revision is a new packet; files added later from the same revision join the
  packet they belong to.
  [`devtools.acquire_source`](../devtools/acquire_source.py) writes a packet from a
  declaration kept in its `acquisition/` directory, and its `--check` re-derives the
  packet from its manifest.
- **A source its author submitted is presumed retainable.** Where the author submitted
  the source to this repository, in an issue, a comment or a pull request, the
  presumption is permission to retain and import the submitter’s own material, and its
  exact licence is followed up on a bead of its own that does not hold the import.
  Files of others inside the source keep their own basis, such as their stated licence
  or the retained-factual-data decision.
  The packet’s declaration and README say which files rest on that presumption and name
  the bead. The owner, on Francisco Couzo’s #763, 24 October 2026: “so Couzo’s has
  submitted so the presumtion is permission from that.
  We should track a bead to follow up on the exact license, but it should not impair our
  ability to import things” (think-cnn7; the licence follow-up is think-m8f4). The
  owner’s words are about Couzo’s submission; reading them as a rule for any submitting
  author is the coordinator’s, and is put to the owner on #789.
- **Bulk goes to hosted data, decided before the first commit.** Size what the packet
  and the pass retain as
  [OR-18](../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)
  counts it. By OR-18’s threshold, a certificate, dump or evidence file of more than a
  few megabytes, or a set of them totalling tens of megabytes, goes into no commit.
  The per-pull-request added-blob check enforces it, with its limits in
  `packing/devtools/added-blobs.yaml`: stage the packet, run `git fetch origin` so the
  base is current, and run
  `python -m devtools.check_added_blobs --base origin/main --staged` from `packing/`
  before the first commit, so the decision is made before the bytes are in history.
  Publish such data as a hosted data release by
  [Publishing Hosted Data](../../development.md#publishing-hosted-data): ignore the
  directory that will hold it, stage a manifest in `packing/hosted/` with
  `python -m devtools.hosted_data stage`, publish it under a `data/<subject>-v<N>` tag
  with `python -m devtools.hosted_data publish`, and commit the manifest and the code
  that reads through `sqpack.hosted_data.require`, never the bytes.
  A hosted upstream file is declared pinned-only in the packet’s acquisition
  declaration, with the manifest as its reason, and fetched outside the packet’s
  archived directory: the packet `squarepacker-k2-minus-c-upper-2026-10-09` pins Ryu’s
  two largest certificates that way, and their manifest fetches them to
  `packing/cases/asymptotic/hosted/`. Inside the packet,
  `devtools.acquire_source --check` would read such a file as a retained one its record
  does not list. The packet’s README lists each hosted file with its manifest, the
  receipts, verdicts and summaries the record cites stay in Git, and the pull request
  gives the release URL, the manifest path and the total size.
  This is decided at retention, not at review: once a blob is in a branch’s history,
  taking it out means rebuilding the branch.
  An import never raises the mutation workers’ snapshot cap or prunes their inputs to
  make room. That cap (`SNAPSHOT_MAX_BYTES` in
  [`devtools/run_negative_controls.py`](../devtools/run_negative_controls.py)) is a
  coarse bound against accidents, which the owner reset to 512 MiB on 22 October 2026.
- **The bibliography key** carries the date of the pinned revision as `dated`, and is
  defined in the [resources README](../resources/README.md) as well.
  Credit is read from the source’s own files, now and not after the review, and names
  each person as [epistemics.md](../../epistemics.md#parallel-projects-and-their-credit)
  says: by name, not by a handle.

## Stage 3: Record

Record the claim as reported, by the frontier README’s rules: a reported evidence entry,
a coverage entry that cites it, the reported lane of each case it improves, and a
register entry with its ratings and `next_rung`.

For a formal proof, also inspect the producer’s execution evidence under
[epistemics.md → Reported Formal Proofs and Source Builds](../../epistemics.md#reported-formal-proofs-and-source-builds).
When a complete source build qualifies, keep the literal reported entry and add a
separate external source-build entry.
It can raise V at intake; its passing status describes the producer’s run and cannot
raise C beyond a qualifying read.
An announcement, source scan, private run summary with unresolved build coverage, or
partial build does not qualify as complete execution.

The eight record rules are:

- **`attribution.published` is the claim’s date, not the pin’s:** the date the source
  gives for it, or the UTC date of the first commit that contains the certificate; for
  an entry over several certificates, the last of those dates.
- **The entry’s `scope` is covered** by the scopes of the evidence it cites.
- **`landed` is written with the entry**, after `registered` and as the same day.
  The schema requires it, and the merge step re-dates it to the day the entry reaches
  `main` ([stage 5](#stage-5-publish)).
- **A new house best packing or new beyond-horizon rows get a landing.** After changing
  `upper_bound_houses.ADOPTED` or adding a source’s beyond-horizon rows to
  `source-coverage.yaml`, run `python -m devtools.stamp_landed --apply` from `packing/`,
  which dates them in `packing/frontier/landings.yaml`, the record the home page’s
  Recently Added places them by.
  `tests/test_stamp_landed.py` fails until every adopted count and row source has its
  day, and the merge step re-dates them ([stage 5](#stage-5-publish)); run it again
  after merging `main`.
- **The claim states each bound it reports**, in a form `devtools.check_standing` reads:
  `s(n) <= v` for an upper bound, `s(n) >= v` for a lower bound and the same with `=`
  for an exact value, where $v$ is the value the source certifies, written as a fraction
  or as decimals that end.
  A value that is no such number, such as a root of a polynomial, is written by its
  decimals cut where they are certain and ended with an ellipsis,
  `s(106) <= 10.822908044132847555086207…`, which stands for every number that starts
  so. A closed form written with `√` or `sqrt` may stand before them,
  `s(11) >= 38100√(8100042893309449)/899996306539 = 3.8100257…`. Where the case lanes
  are left unchanged until the result is adopted, as `T-128`’s were, those values are
  all that relate the entry to its cases: it is *pending adoption* where one is better
  than its case’s bound, and *superseded* only where the case holds one at least as good
  ([epistemics.md](../../epistemics.md#status)).
- **A confirmation the triage priced and did not run is listed** in the entry’s
  `unfinished_confirmations`, with the rung it would reach, its bead and its
  `estimated_cost` from the bead’s price, and it is removed in the change that lands it
  ([epistemics.md](../../epistemics.md#status)).
- **A regularization is listed as one.** Where an imported certificate rearranges a
  packing the record already credits, as Evan Daniel’s regularized record lists do
  (`T-146`), the entry lists each count in `regularizations`, naming the result whose
  packing it regularizes, so the packing keeps its finder’s credit and the regularizer
  is credited with the regularization; the `identity` stays the source’s claim until a
  measurement here decides it
  ([epistemics.md](../../epistemics.md#parallel-projects-and-their-credit)).
- **The `T-NNN` is taken last.** An id is its row’s position and cannot be reserved
  across branches, so take it in the commit that registers the result, merge that day,
  and quote it to no author until it is on `main`.

The record checks pass without a packet, and the reviewer of the pull request looks for
one. `devtools.check_source_coverage` refuses a source dated from 22 August 2026 that a
register entry or its evidence cites and no coverage entry holds, by its key or by
citing its evidence (think-g6d5), and `devtools.check_results` an entry whose scope its
evidence does not cover, or a recent case bound, upper or lower, that no entry covers
(think-506q).

## Stage 4: Validate

Stage 4 is one W2 phase with two lanes that share no context: a replay of the
certificate and a review of its mathematics.

**The replay** is a complete verification of the retained certificate, in full: the
source’s own checker, or a first-party implementation of the same theorem whose
soundness has been adversarially reviewed and whose independence is recorded, as
`sqverify-fast` is for measure-capture certificates (`V-sqverify-fast`). The
[review of 5 October 2026](../../docs/project/reviews/review-2026-10-05-wand125-october-5-and-independent-replays.md#carrying-the-route-to-t-082-t-090-and-t-091)
lists what a records lane checks for each certificate on that route, and what needs
another review. For a format M certificate on a net its file declares (`proof_net`), the
[soundness review of 6 October 2026](../../docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md#for-the-records-lane)
gives the checklist, and the census row must be built from a crate source whose review
read the declared net (`REVIEWED_SOURCES` in `devtools/sqverify_fast_census.py`). Run
`--control` before counting on its receipt.
It runs the 99/100 mutant at every direction of the net, since a single direction may
have more than 1% slack (FC-1 of the
[re-check](../../docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-fix-check.md#fc-1--non-blocking-closed-failure-constrains-every-declared-net-control-receipt-the-99100-control-runs-at-an-index-chosen-by-termination-margin)),
and counts only coverage refusals at poses in the centre domain, each checked apart from
the crate, as the
[review of that change](../../docs/project/reviews/review-2026-10-06-sqverify-fast-census-control-fc1.md#for-the-records-lane)
requires; receipts of the earlier kind, which ran it at the least-bound direction alone,
stand where they are `CONTROLS_REFUSED`. Any other change of direction or scale is a
change of control logic and needs a review.
A fast tier or a sample of roots is a diagnostic.
One complete replay is what `C3` needs; a second route is recorded beside the rung and
is not a condition of it.

- A source’s checker runs from its retained copy, which is read before it is run.
  A script that fetches one over the network is run with the fetch replaced, and the
  receipt says so.
- Its evidence entry names every program the replay runs in `verifiers`, deciders and
  premise checks alike, and registers a new one in
  [`verifiers.yaml`](../frontier/verifiers.yaml) with the digest that ran and the
  retained path of its source.
  `relationship_to_generator` is read from the deciding programs: `same-implementation`
  for the source’s own checker, `shared-components` with the reused parts listed,
  `independent-implementation` with the record of what its authors read
  ([epistemics.md](../../epistemics.md#which-code-confirmed-it)).
  `devtools.backfill_verifier_relation --dry-run` shows what it would write and which
  values look wrong.
- Where the source’s script cannot pass as published, the evidence entry’s `limitations`
  say so, the author is told, and the same checks are run as this repository’s own
  sequence.
- A replay that fails is recorded with `replay_status: failed`, which makes the entry
  `incomplete`.
- Two mutated certificates are refused by every checker that accepted the original, and
  a test holds them.
- The receipts are committed and pushed when the run ends, on a branch the bead names.
  A replay that passed in scratch space and was never committed did not happen.

**The review** is a mapped document under `docs/project/reviews/`, a
[review record](../../epistemics.md#review-records) like any other.
It states the claim and each `T-NNN` it covers; re-derives the argument from the
certificate to the claim, with every hypothesis the checker assumes; gives each
checker’s trust boundary and what any two share; and marks each defect blocking or not.
It is recorded as `external_review` on the reported evidence entry, which makes the
entry `reviewed`, or `incomplete` when the read found a defect, and listed in the
register entry’s `reviews` under the kind it was run as.

**Who reviews, and when.** Every proof an import registers gets a mathematical review, a
formalization registered as its own result included, and it starts at intake: once the
source is retained, in parallel with stage 3. It runs as a sub-agent at the strongest
tier, `tbd-strong-max`, at maximum reasoning, in a worktree of its own; it reads the
source as data and runs only code it writes.
It does not read an earlier review of the same result until its own findings are
written, and then adds a section comparing them; anything of an earlier review it saw
first, it discloses.
It is written to be shared with the author: a summary the author can read first,
findings graded blocking, major, minor or note with the source file and line, and
questions; it names no `T-NNN` that is not yet on `main`, and its reviewer line names
the system family, tier and reasoning setting, not a model identifier.

Its code is kept and registered as
[epistemics.md, Every Run’s Code Is Kept](../../epistemics.md#every-runs-code-is-kept)
requires: in the result’s packet with a README that says what each program does, what it
read, how to run it and what it printed; each program in
[`verifiers.yaml`](../frontier/verifiers.yaml) with its structured `independence`
record, which says what its authors read (the mathematics, the proof text, a
specification, the producer’s code), whether it is clean-room, what it shares and who
wrote it; and an evidence entry, with its coverage, for each thing a run decides or
samples, cited by the case record where it would derive a rung it does not support.
A program that decides nothing is kept, and its README says so.

When it returns, the findings that are the record’s are fixed and the rest go to the
author. The review is mapped as above, the entry’s `unfinished_confirmations`, the
validation backlog (`devtools.check_requests --backlog`) and the pass’s
[backlog bead](#the-compute-cap-and-the-validation-backlog) are brought up to date, and
`devtools.check_results` re-derives `V` and `C`: a rung the evidence now supports is
changed, and where none moves the entry says why.
The reply that shares the review with the author is drafted in the import’s answer bead
and posted at [stage 7](#stage-7-answer), on the owner’s word.

**The exit** follows both lanes.
It adds the replay evidence, moves the verified lane if the review has no blocking
defect open, rewrites the entry’s `claim`, `notes` and `next_rung` together and removes
its `activity`, so that no field says a replay is pending while another says it passed.
The reviewer also confirms or changes the draft significance score.
An open defect goes to the author with the review.
For a result by others, `devtools.check_results` (`verified_lane_review_problems`)
refuses the verified bound until the review is recorded in one of two forms: a `reviews`
item on a register entry that cites the evidence and covers the count, of kind
`adversarial`, `confirming` or `formalization` with verdict `accepted` or
`defects-resolved`; or, on the evidence entry, an `external_review` in state
`informally-verified`, or a `proof.audit_record`, that names the review by its full
path, `docs/project/reviews/review-….md`. A bare file name is not found.

The reviewer of the pull request checks one thing in every sentence the stage writes:
where the claim, the case record, the review or the reply says the result is
*confirmed*, it says which confirmation, reproduced with the producer’s code,
re-implemented sharing named components, or independently re-implemented.
The checker holds the register’s `claim`, `composition` and `next_rung` to it; the case
record, the review and the reply are held to it here.

### The Compute Cap and the Validation Backlog

The owner sets each pass a compute cap in CPU-hours, and the pass’s epic bead records
it. It is the budget a pass needs before it starts a replay measured in CPU-hours, and
the work above it is tracked in beads (the owner, 2026-10-14, setting the first cap:
“let’s be sure we have a clear backlog of validation work that’s tracked appropriately,
and details are in beads”). A validation item priced within it runs in the pass, and one
priced above it is *held* until the owner raises the cap or approves a subset.
The cap applies to each item; whether the runnable items together may pass it is the
owner’s call. With no cap set, only a replay the source prices at minutes runs; an
adoption’s regularization runs are the one exception, held to the owner’s standing 40
CPU-hours an item
([Adopt a House, Then Regularize It](#adopt-a-house-then-regularize-it)).

Every validation item the pass leaves pending is a bead labelled `validation` under the
import bead it serves, and its description carries one block:

```markdown
## Validation
- Claim: the result, its certificate and source pin, and the checker.
- Run: the commands, and any preparation slice before them.
- Cost: CPU-hours, and their basis: the source's receipt, a sample run here, or an estimate.
- Budget status: running, runnable, gated on decision, or held, against the cap.
- Possible subset under the cap: for a held item, proposed; it runs on the owner's word.
- Depends on: beads, owner decisions and code slices that must land first.
- Done when: what the receipts show and where the evidence is registered.
- Machine note: what the run needs and whether it can share the machine with a gate.
```

*Gated on decision* means the item fits under the cap but waits for an owner decision or
a code slice. One backlog bead under the epic tabulates every item, with its bead, cost,
status and dependencies, then totals by status and what the record cannot yet price.
Each item’s bead is the one the entry’s `unfinished_confirmations` names (stage 3).

## Stage 5: Publish

The pull request that registers or raises a result runs
[New Result Publication](documentation-pass.md#new-result-publication): the views are
rendered in the commit that changes the record, and the data pin moves in the next.
No documentation phase is opened for it.

It cuts no site edition.
Site editions are retired as of 22 October 2026
([Cutting an edition](../../development.md#cutting-an-edition); `think-wdqo`): the site
deploys continuously from `main`, and `check_release_impact` asks it for no disposition
and refuses an edit to the frozen `PUBLICATION_HISTORY` or `PUBLICATION_REVISION`, so
the claim documents are not regenerated for an intake either.
A paper or the posters still take their own cut, or a no-change record, when the import
changes what they print.

The pull request’s `--fast` surface runs on CI’s runners, not on a machine that is also
running a replay, where a tier’s wall measures the contention rather than the branch
([What each tier costs](../../development.md#what-each-tier-costs-and-where-its-ceiling-lives)).
That hosted run is the draft’s full test gate: marking the pull request ready for
review, and merging it, both need `packing-required` and `pages-required` green on the
head ([development.md](../../development.md#hosted-ci-gates-a-draft-pull-request)). It
merges on the owner’s word, by
[the merge policy](../../development.md#merging-a-pull-request).

### The House Rule

A case record’s two upper lanes hold one certificate, that of the case’s **house best
packing**, which the synopsis defines under
[The measurements](../../SYNOPSIS.md#the-measurements).
At every count the house best packing is the smallest of the current one and every
packing whose certificate has passed [stage 4](#stage-4-validate), whoever found it: a
validated packing smaller than the house best packing replaces it, and a larger one
never does. A smaller validated packing is adopted in the intake pass that validates it,
and each count where the adoption changes the house best packing is regularized in the
same pull request ([stage 5’s adoption steps](#adopt-a-house-then-regularize-it)). The
owner set the rule on 16 October 2026: “We should always be adopting the smallest
packing and then regularizing it.
That should be the policy, obviously.”
and “This should be built into our policy.
It shouldn’t even be a question.”

No adoption waits for the owner’s word, and each case that once did is decided here:

- **Validated** is stage 4’s exit: the register entry at `V3` and `C3` with an accepted
  review covering it. One complete replay is what `C3` needs, so a certificate decided on
  one exact route, as a number-field witness is today, is adopted like any other.
- **Smaller** is decided by exact arithmetic, never by a print or a person.
  `devtools.exact_sides` holds each side exactly, as a fraction or as the one root of an
  irreducible polynomial in a rational interval, and the case’s ceiling the same way, a
  closed form included.
  Where the code cannot order two sides, the code is fixed, and `select_houses --check`
  fails until it is.
- **A witness’s size never holds an adoption back.** The certificate stays where its
  packet keeps it, as a gzipped derived fact or as an upstream file pinned by its
  digest. The house best packing’s witness, `witnesses/known-best/n-NNN.yaml`, goes into
  Git while
  [OR-18](../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)
  allows, its sizes counted as Git stores them, which OR-18 defines: no file of more
  than a few megabytes and no pass’s set of tens.
  Past that it is published as a hosted data release, in the same pass, and read through
  its manifest with `sqpack.hosted_data.require`
  ([Publishing Hosted Data](../../development.md#publishing-hosted-data)). No tool that
  reads a house best packing’s witness takes a hosted one yet, so the adoption that
  first needs one writes that reader in its own pull request (think-ot5c names it for
  T-193’s forms). `python -m devtools.upper_bound_houses sizes` measures the witnesses a
  staged adoption would write.
  On 17 October 2026 the witnesses of T-174’s 50 staged adoptions at rational sides add
  2.84 MB to history as Git stores them, since the witnesses they replace stay in it,
  and 14.55 MB to a checkout, the largest 0.22 MB stored: they go into Git.
- **A regularized view below the house best packing’s side is a smaller packing.** It is
  registered as a result and taken through stages 3 and 4 like any report, with the
  packing credited to its finder and the regularization to the regularizer
  ([epistemics.md](../../epistemics.md#parallel-projects-and-their-credit)), and adopted
  once validated (the regularization guide’s
  [Register Candidates](../../docs/project/guides/regularization-process.md#register-candidates)).
- **Equal sides** keep the earlier report, by the
  [report-order rule](#several-reports-at-one-count) the ledger applies, which governs
  wherever two orders could differ.
  An exact tie between different holders is decided by it: the ledger lists one for the
  owner only as a possible exception to recording a result, and an exception changes no
  house best packing. `select_houses` replaces a house best packing only with a smaller
  one, so the case keeps its own at an exact tie; between validated candidates of one
  side it keeps the earlier `attribution.published`, then the earlier entry.
  That date is the last of an entry’s certificates where it has several, so it stands in
  for report order only where the two agree.
  On 16 October 2026 no two candidates at a count that moves are exactly equal.
- **Regularizing is part of adopting.** Both strong generators run on each count where
  the adoption changes the house best packing, in the adoption’s pull request, and the
  count is admitted or settled on what they find: its runs are owed there, so such a
  count is never deferred to `default_drawings.PENDING_ALLOWED`. A drawing less regular
  than the strong view it replaces is no reason to wait.
  The owner on n = 176, 16 October 2026: “Adopt as settled.”
  - A view that rows 7 or 8 of the regularization policy’s
    [decision table](../../docs/project/policies/regularization-policy.md#the-decision-table)
    send to the owner settles the count on its current drawing and waits in the review
    queue, holding neither the adoption nor the count.
    The owner reviews it under the policy’s
    [section 5](../../docs/project/policies/regularization-policy.md#5-manual-review-and-adjustment),
    and a view the owner admits is drawn on its review record, as at n = 211 on 16
    October 2026: “Admit it.”
  - Where the house best packing has an algebraic side, the count draws its exact house
    and its regularization stays owed under think-mbdw: its `SETTLED` entry’s state is
    `regularization-owed`, not decided, and its `owed` names the bead: no rational view
    is `same` or `bound` at an irrational side, and no number-field view is decided on
    two exact routes yet (the policy’s obligation 1; think-mbdw is that second route).
    A rational view just above an algebraic U is not drawn.
    The owner answered question 13 so on 23 October 2026 (think-r8cn): the best record
    is always the record, and a regularized drawing may change the side only as a strict
    improvement.
- **A conjectured optimum** that the new house best packing is below, wherever its print
  rounds, is withdrawn, and any other stays; the adoption goes ahead either way.

`devtools.select_houses --check` is the gate, and `tests/test_house_adoption.py` runs it
on every pull request: it fails wherever a validated smaller packing is not the house
best packing. A count’s adoption may follow in a later pull request than the one that
validates it only where the count is staged in `select_houses.PENDING_ADOPTION`, with
the open bead that adopts it and one of three reasons (`STAGING_REASONS`): the pass’s
next pull request; regularization runs over the item cap, which split the adoption
([stage 5’s adoption steps](#adopt-a-house-then-regularize-it)); or no writer, where
`adopt_houses` cannot yet write the new house best packing.
A house best packing with an algebraic side was the one such gap the rule names until 23
October 2026, when the writer took an algebraic side, written in both lanes as the one
root of its minimal polynomial in an interval, or of degree two as its closed form
(`exact_sides.form`). The gap now is an algebraic house that no derived number-field
fact and receipt hold (`upper_bound_houses.FIELD_COUNTS`), and the writer’s bead,
think-ot5c, owns its counts.
`bead tree` holds each bead open, and the adopting pull request takes the count off.
`--check` fails on a staged count where the selection no longer changes the house best
packing, or would change it to a packing other than the one staged, and on a count
staged for want of a writer that the writer can write, or the reverse.
`default_drawings --check-state` fails while `PENDING_ALLOWED` defers the runs of a
witness whose packing is no longer its count’s house best packing, whichever import
replaced it. Each entry is a corrected witness’s, and `default_drawings.CORRECTED` names
the witness it replaced, by its source, path, revision and exact side.
The records tier holds that to the record of the commit the change is built on
(`--check-state --base-ref origin/main`, which reads its merge base): the base’s witness
at the count must be the one named, the record’s must have its source and exact side,
and it must be another witness only, by another path or revision, or, at a source that
pins no revision, by another witness file.
So a deferral fails wherever an adoption, a Kingbird catalogue intake (whose source key
never changes) or an exact re-solve has changed the count’s house best packing, whatever
its entry declares (review C3 of #660). Once the base defers the count, the entry stands
while the record’s witness keeps the base’s source and exact side, whatever a later
change does to the witness’s file or path (review D1).

### Adopt a House, Then Regularize It

Once stage 4 has confirmed and reviewed a certificate below a case’s house, the pass
adopts it as the case’s new house wherever the house selection takes it
([The House Rule](#the-house-rule)). `devtools.select_houses` names the counts,
`devtools.upper_bound_houses` rebuilds each witness from the retained certificate, and
`devtools.adopt_houses` moves the case records; its docstring, under “A later pass”,
lists what the pass adds first.

A new house is a new witness, and the count’s regularized view lapses with it.
So every count whose known-best witness changes is regularized in the pull request that
changes it, whichever import made the new packing a house:

- a house adoption, the usual cause, of a result from any import, such as T-174 or T-186
  to T-190 once its house is adopted;
- a Kingbird catalogue intake that moves a count’s record;
- an exact re-solve or a correction of a witness;
- any other result that `build_known_best_atlas --update` takes into the atlas.

None of them defers its runs but a witness corrected or re-solved with its house’s side
unchanged, as below.
The steps are the regularization guide’s
[When a Witness Changes](../../docs/project/guides/regularization-process.md#when-a-witness-changes):
`build_known_best_atlas --update` writes the new witness, the axis tool’s
`--update-atlas` redraws its view, `default_drawings --update` records each count’s
state, and `--check-state` names each count left `pending`. Then both strong generators
run on each pending count, and the selection admits what improves on the drawing.
Where neither draws better, the count is settled as the guide says.
`adopt_houses` prints the re-housed counts and these commands when it writes, and with
`--dry-run` before it does.
It names the run directories for the adoption’s day and its lowest and highest re-housed
count, since the layer records a run by its directory’s name and a repeated name would
replace an earlier run’s record: the index holds only the runs merged into the branch,
so two adoptions in flight on one day would otherwise print the same names.

The strong runs cost 5 to 25 CPU-minutes a count, from the layer’s run receipts:

- Evan Daniel’s driver takes 140 to 220 CPU-seconds a count
  (`evand-regularize-adopt518-v2-rerun-2026-10-13`,
  `evand-regularize-refreshed-adopt518-v2`);
- grid-slack takes 37 to 110 CPU-seconds a count at each of its three thresholds
  (`grid-slack-deg5-1013-b`, `grid-slack-all`);
- the selection takes seconds to about four minutes for each of a count’s four candidate
  views, a figure no receipt yet measures on a new witness.

Ten re-housed counts take 50 to 250 CPU-minutes.
The regularization an adoption owes is one validation item, priced at the total
`adopt_houses` prints and held to the cap the owner set for the pass
([The Compute Cap and the Validation Backlog](#the-compute-cap-and-the-validation-backlog)).
Unlike a replay, it has a default where the pass sets no cap: the owner’s standing cap
of 40 CPU-hours an item (14 October 2026, think-lh7d), since its runs are part of the
adoption ([The House Rule](#the-house-rule)) and a pass with no cap would otherwise
stage every adoption larger than minutes (review C8 of #660). They are within the cap
and run in the adoption’s pull request: at the receipts’ dearest, 25 CPU-minutes a
count, about a hundred re-housed counts fit.
An adoption whose runs would pass the cap is split into pull requests that each fit, and
the counts a pull request does not adopt are staged in `select_houses.PENDING_ADOPTION`
as over the item cap, with the open bead that adopts them, labelled `regularization` and
`validation` and carrying stage 4’s `## Validation` block, with a row in the backlog
bead. A re-housed count is never deferred to `default_drawings.PENDING_ALLOWED`, and
`default_drawings --check-state` fails while the list defers the runs of a witness whose
house has moved since.
A count the list already names, such as one of the twenty below, is run in the
adoption’s pull request and taken off it.

The adoption’s pull request lists each re-housed count’s drawing before and after, with
`default_drawings --compare` on its base branch’s record, `BASE` being `main` unless the
pull request is stacked:
`python -m devtools.default_drawings --compare <(git show origin/$BASE:packing/atlas/known-best/default-drawings.json)`.
Where a strong view gives way to a drawing worse than it on a goal of the improvement
rule, whatever drew it, the table names those goals at each such count, and marks each
one that still reads pending, “its runs are owed in this pull request”, as every
re-housed count’s are; one its runs have regularized or decided is listed and not
marked. The axis tool’s view is the usual replacement, since the refresh draws it
wherever it improves on the new house: it replaced all seven strong views the adoption
of 16 October 2026 (#657) lost, and at n = 302 a drawing with no uneven and no near-axis
square gave way to one with 26 and 11. A house drawing is the rarer one, as at n = 176
on 15 October (review D1 of #641).

A witness corrected or re-solved with its house’s source and exact side unchanged may
defer its runs where they do not fit under the cap, except at a count the table marks.
Its pull request adds each deferred count to `default_drawings.PENDING_ALLOWED`, naming
the open bead that owns its runs: labelled `regularization`, as every such bead is, and
`validation`, since its runs are held above the cap, carrying stage 4’s `## Validation`
block, with a row in the backlog bead.
It names the witness the correction replaced in `default_drawings.CORRECTED` too, by its
source, path, revision and exact side as the base branch’s record names them, since
`--check-state` reads any other entry as deferring a moved house’s runs and fails it,
and holds this one to the base record ([The House Rule](#the-house-rule)). It runs
`default_drawings --update` again, since the record copies the entry into the count’s
reason, then the guide’s render step, and lists the drawings as above.

The records tier’s
`every drawn picture is regularized, regular as published, decided, owed to an open bead or exempt`
(`default_drawings --check-state`) fails on a pending count that the list does not name,
so an adoption cannot pass until its runs have decided every count it re-houses.
It also fails on a listed count that is no longer pending and on a `SETTLED` entry
decided on the earlier witness.
So the adoption’s pull request takes each count its runs decided off the list, and
settles each such entry again or removes it.
A new house that reads regular does not take a listed count off: on the list, a count
waits for runs that decide it.
The gate cannot tell a hand-dropped entry from a decided one: dropping an entry whose
count then reads regular as published passes it, and so does adding a count whose house
reads regular, which the list then holds pending.
Either is a reviewed decision, and its pull request shows the bead’s runs or the
`--compare` table (review C2 of #641; think-k6rj). The adoptions of #553, #598 and #614
refreshed only the axis tool’s views, and left twenty counts without a strong
generator’s decision on their witness, with the raw house drawn at n = 176, until that
gate was added (think-sfas).
Fourteen of the twenty lost a strong view before the index recorded lapses, and their
entries in the list are the record of it.
The sweep’s **Regularization owed** lists every count still pending, with the bead that
owns its runs, so each pass sees what its own houses and earlier ones still owe
([stage 0](#stage-0-sweep)).

### Label the PR and Prepare News

Before merge, give each PR exactly one GitHub significance label, `S1` through `S5`,
under the `github-workflows` grant (`tbd policy show`). Replace an earlier S label when
the assessment changes.
Score the highest genuinely new result or capability delivered by the PR; a citation to
an existing result does not inherit its score.
Keep the rationale in the PR description and the eventual entry’s `significance`.

Use the following rubric conservatively.
Most supporting work belongs at S1 or S2; choose a higher score only when the delivered
contribution meets its anchor.
Being public alone does not make a change noteworthy.

| Label | Delivered contribution | Short | Examples |
| --- | --- | --- | --- |
| `S1` | Bookkeeping, internal documentation, planning or formatting only | Minor housekeeping or internal documentation | Session closeout, a roadmap, changelog synchronization, prose reflow |
| `S2` | A routine fix or refactor, custody or attribution work, modest UI refinement, ordinary maintenance or supporting prototype | Routine engineering, maintenance or internal reliability | Refreshing a source packet, correcting credit, adjusting spacing, preparing a vendor import or an internal prototype |
| `S3` | A distinct noteworthy new result, substantive public explanation, verification or policy, key tooling, or meaningful artifact delivery | Distinct noteworthy result, explanation, verification, policy or key usable tooling | A new S3 result, a substantive proof explanation, a reproducible verification tool, a useful new paper or certificate delivery |
| `S4` | A major delivered capability or site restructure, or a substantial new result | Substantial result or major public project capability | A complete regularization capability, a major site reorganization, a new S4 result |
| `S5` | A landmark mathematical contribution or major resolution | Landmark mathematical advance or major resolution | A new S5 result establishing an important previously open case |

The Short column is each label’s description on GitHub.
It is also what a News meter and the archive’s S buttons say a level means
(`render_changelog.news_significance_meanings`); a result’s meter keeps the result
ladder in `epistemics.md`.

A new registered result and its announcement inherit that result’s actual S score.
An incidental reference to a result does not raise the PR’s score.
A grouped release or announcement takes the maximum of its genuinely new contributions;
score each stack layer for what that layer actually delivers, without assigning every
layer the final release’s score.
A plan, vendor preparation or supporting prototype generally remains S1/S2 until it
delivers a capability that meets a higher anchor.

For example, a typo fix in a public paper is S1/S2, not a new substantive explanation; a
routine verifier repair is S2 unless it delivers a distinct noteworthy verification or
capability. A large diff or a merge into a major stack does not supply significance.
This judgment measures importance independently of verification and confirmation.

Add the separate `project` label for site restructuring and project capabilities such as
regularization. It is orthogonal to significance: project work can be S1/S2, and the
label gives no score increase.
It maps to the shared **Project** topic in News; it is not a scientific result kind.
Engineering and Verification remain available topics, alongside the precise result
kinds. News excludes Correction and Audit topic labels; Results keeps those registered
kinds.

For S4 and S5 results a News entry is required, by the step and the gate in
[Announce a Significant Result](#announce-a-significant-result).
For other S3–S5 work, S3 results included, News stays optional, as before: draft a
concise News entry before merge, or record an editorial omission when the PR is an
intermediate research checkpoint without a distinct reader-facing development.
Name what changed, why it matters, the source PR and relevant `result_ids`, direct
public artifact links where available, and the actual verification or publication
limits.
Use surnames throughout News titles, summaries, details and display labels unless
two distinct people share one; retain handles, organization names and literal cited
titles. Canonical attribution keeps full identities.
Use the real event date once known.
The merged delivery date and the independently verified publication date are separate
facts. A merged PR alone does not establish a live website, released artifact or
completed proof replay.

For S1/S2, record a coverage omission or retain an entry in the full changelog; these
scores stay out of News.
Existing published entries keep their dates and PR membership.
Later verification or adoption is a separate event, with its own evidence and entry when
noteworthy.

After the source PR merges and its commit reaches local main, use the existing authoring
command from `packing/` to prepare the follow-up change:

```bash
uv run --frozen --all-extras --group dev python -m devtools.import_changelog \
  --pr NNN --significance-rationale "Explain the new delivered contribution." \
  --output "$TMPDIR/changelog-candidate.yaml"
```

The importer fetches labels and takes the score from the single S label, so the editor
supplies only the rationale.
It rejects multiple S labels or a score conflicting with explicit metadata or
`--significance`. Retained historical JSON without labels can still supply
`significance: {score, rationale}`, or an explicit `--significance` with its rationale.
Citations never assign importance automatically.
Review the candidate and coverage audit, replace placeholder prose, and bring the
approved entry into [`site-changelog.yaml`](../site-changelog.yaml) through
[Maintaining the project changelog](../../development.md#maintaining-the-project-changelog).
Rendering and routine validation remain offline.

### Verify the Published Result

An import’s publication includes its public results and drawings.
Passing a local build or PR CI establishes the candidate; verify the deployed main tree
before any reply in stage 7 that reports it.

Before merge, check the generated result/evidence registers, owning case pages, bound
citations and selected case/overview graphics together.
Each drawn packing must match its selected exact source geometry and displayed safe
ceiling. A confirmation label must refer to evidence for that displayed bound, rather
than an earlier, weaker ceiling.
Preserve the source’s decimal print as a quote and the earlier certificate as history
when a tighter reported packing supersedes it.
Inspect representative desktop and mobile views for cropped drawings, missing source
credit or unreadable labels.

Last, once the owner has given the word, re-date the branch’s new register entries to
the merge day.
The branch’s last two commits are the stamp, `uv run --frozen --all-extras
--group dev python -m devtools.stamp_landed --apply` from `packing/`, which sets
`landed` on every entry `origin/main` lacks to today in UTC and dates, in
`packing/frontier/landings.yaml`, each house best packing and each source of
beyond-horizon rows the branch adds to `main`’s tree, and its re-pin, `python -m
devtools.release_pin --update`. If `main` moves, or the merge slips past midnight UTC,
run both again after the re-merge: the stamp re-dates the same entries.
`landed` is the day of the stamp, so the stamp is the last step before the merge.

Synchronize the owning beads to the native `tbd-sync` branch before clearing fallback
outbox exports.
Verify every exported issue identity/version and alias against the remote
native records, retain the raw variants, and commit outbox cleanup separately.
An empty local outbox alone does not establish successful synchronization.

After merge:

1. Identify the successful main Pages deployment and its full source commit.
   A newer deployment is suitable when it contains the merged import.
   Record its run and commit; a successful PR build is not deployment evidence.
2. From `packing/`, run the existing site checker with project Python:
   `uv run --frozen --all-extras --group dev python -m devtools.check_published_site --commit FULL_DEPLOYED_SHA`.
   Preserve its completion receipt and actual pass/fail/skip counts.
   Diagnose browser or environment failures without disabling TLS verification or
   publication checks.
3. Follow each imported result’s `all-results.html#t-NNN` link on the main site.
   Check its scope, V/C/S rungs, status and credit against the merged register;
   provisional branch-only status must not survive publication.
4. Check every changed case’s main drawing and overview/regularized rendering against
   the selected source, exact side and safe display.
   Confirm that reported versus verified labels and their citations agree, and that
   retained historical evidence remains accessible.
   Check the rendered layouts as well as their source metadata.
5. Record deployment, result-row and graphics evidence in the owning intake bead.
   The final author reply states only the scope actually imported, reviewed and
   published; a later source revision or newly split issue remains queued with its own
   owner.
6. Complete the prepared News/changelog disposition in the next change, following
   [Label the PR and Prepare News](#label-the-pr-and-prepare-news).
   For an S4 or S5 result that change is required, and stage 7’s
   [Announce a Significant Result](#announce-a-significant-result) says who opens it.
   Retain the actual merge date, source PR, `result_ids`, artifact links and limits.
   After that change deploys, check the live News entry and its public artifact links
   against the merged record, and retain the deployment receipt.
   Claim publication only after this check.

## Stage 6: Explain

Some results warrant a paper that explains the proof and this project’s review of it to
a reader outside the project.
[The review of the eleven-square optimality proof](https://jlevy.github.io/squares/papers/n11-optimality-review.html)
is the model. Write one when a result is confirmed and is scored `S5`, or is scored `S4`
with a proof that cannot be followed from its source alone, or when the owner asks.

The paper leads its credits with the original proof and its author.
It gives the argument from start to finish, what was verified here and what that
verification does and does not establish.
It states nothing the register does not hold, and its exposition gets its own W2 review.
It is neither a replay nor the human oversight record that rung 4 requires.
[conventions.md → Naming](../../conventions.md#2-naming) owns its slug, and
[the development guide](../../development.md) how it is built and served.
A paper on a case that already has papers joins them as a series, as the $n = 11$ papers
are one, read in order: the threshold-bound review of T-037 is Part II between the
lower-bounds explainer and the optimality review.
It is one entry in `render_overview.PAPERS`, defines every term before it uses it, and
follows the series rules in
[paper-design.md](../devtools/templates/paper-design.md#the-papers-front)
([the series plan](../../docs/project/specs/done/plan-2026-10-05-n11-explainer-series.md)).

## Stage 7: Answer

[epistemics.md](../../epistemics.md#import-integration-and-reply) says what an answer
contains and who posts it.
The process adds when and how.
The owner’s standing instruction of 2026-10-11 is why: “be sure the process codifies
that you need to comment on every issue and follow up on each”, and “An update on the
issues as they are approved.
We should validate everything follows and then comment after the PRs are merged.”
What lets an agent post is the `github-workflows` grant, which covers issues.

- **Every issue a pass touches gets a comment**, and every later change of its state
  gets a follow-up: imported, registered, confirmed or a defect found, a rung or status
  moved, adopted on its case, superseded, closed.
  No issue is left without a reply, and the last is the final comment that closes it.
- **A pass touches an issue** when its change makes one of those changes to a result the
  issue reports or asks for, or reads one of the issue’s comments into the record: a
  review, case record, register entry or bead that quotes the comment or rests on it.
  A change of significance alone touches no issue: a reply states ids, rungs and status,
  and a score guides reading order and changes none of them.
- **A reply follows the merge** of the pull request that carries the change, and links
  only to `main`. A link into a working branch dies with the branch, and a `T-NNN`
  quoted from one can change.
  An agent drafts it in the issue’s answer bead while that pull request is open.
  A [report-order verdict comment](#report-order-verdict-comments) is the one progress
  comment that may come before, on the condition that section states.
- **The poster validates first** that `main` and the deployed site say what the reply
  says: it is rendered with `check_requests --draft N` from `main`, and the site is
  checked as [Verify the Published Result](#verify-the-published-result) says.
- **An agent posts it as part of the pass**, under the `github-workflows` grant; without
  the grant it drafts the reply in the answer bead and asks the owner to post it.
  The owner may post instead.
  Either way the reply is recorded under the issue’s `replies` in the next change
  ([After the Merge](#after-the-merge)).
- The reply that reports a confirmation names the programs that ran, and says whether
  they were the author’s own code re-run or a re-implementation.
- **Every pending review is tracked on a GitHub issue**, and its state is posted there
  at each change (the owner, 24 October 2026: “This state of all reviews should be
  tracked in the GitHub issues.”). A review is pending while its result stands below
  `V3` or `C3`, names an unfinished confirmation or an activity, or has a comparison the
  record index leaves unassessed, which its author’s profile shows as Review pending.
  The tracking issue is the one that reported the result, or, where none did, one the
  project opens, as it does for every S4 or S5 result (#603 for T-163). Each change of
  that state gets a follow-up there: the review or replay queued with its bead, run,
  landed or held, a rung moved, a comparison settled.
  `check_requests --pending` lists every pending review with its beads, its issues and
  whether one of them states its present state; a comparison is a state no reply field
  holds, so it stays listed until it is settled.
  The pass answers every issue the view marks stale, and reports to the owner, before
  opening any, the results it lists with no tracking issue.
  The view lists apart a result whose owing issues are all held for the owner, since no
  pass posts on a held issue until the owner lifts the hold, and marks one tracked only
  on closed issues, which still count as tracking it.
  Two follow-ups it cannot see are the pass’s to post by hand: the one a comparison owes
  once settled, since it leaves the view as it settles (#603 for T-163), and those owed
  where an issue names a result only in an ask, not in its `results` (#532 for T-142 to
  T-144).
- **A settled issue is closed with its final comment**, after the verified deploy, once
  nothing the author asked for is queued and no question to the author would change the
  record: [Close a Settled Issue](#close-a-settled-issue).
- **Every S4 or S5 result gets a News item** in the first change after the merge that
  registered or raised it:
  [Announce a Significant Result](#announce-a-significant-result).

### Close a Settled Issue

The owner’s instruction of 23 October 2026: “if we have actually imported something,
it’s already on the website, and we validated that, we should close the issues.
That should be our standard process.”
What is unresolved, or needs the reporter’s answer, stays open.
That morning twelve issues were closeable and open: nothing ran the closing step, the
sweep did not list them, and lanes had kept issues open for questions to their authors
that the record did not track and whose answers would change nothing in it.

1. **After the verified deploy**
   ([Verify the Published Result](#verify-the-published-result)), run
   `check_requests --report` from `main` and take each issue it marks closeable that is
   still open on GitHub.
   An issue held for the owner (`held` in the record) is never closeable: no pass posts
   on it or closes it, `check_requests --draft` and `intake_comments --out` refuse it,
   and the sweep lists it for the owner with what would otherwise be owed.
   A hold is set on the owner’s recorded instruction (`basis: owner-instruction`), or on
   a reservation for the owner that beads record (`basis: recorded-reservation`, pending
   the owner’s confirmation), with those beads in `beads` and a note saying what each
   records; only the owner lifts it.
   An issue GitHub already shows closed is not posted on again: record its final comment
   and its close (step 4).
2. **Check that `main` and the deployed site say what the final comment will say**,
   render the comment with `check_requests --draft N`, and edit it to the house style:
   what is settled and where, linked into `main` and the site, then that nothing the
   author asked for is queued, so the comment closes the issue.
3. **Put an informational question in the closing comment**, saying that an answer is
   still welcome and holds nothing open.
   A question holds the issue open only when the record asserts something the answer
   could falsify (who is credited with a result, what the record says it was derived
   from, or which file or commit a claim names) and no measurement here can settle it.
   Almost any provenance answer would change some sentence, so that is not the test.
   A question the record already answers is informational, and one a measurement here
   could settle is measured instead, as review A3 of #747 measured #470’s counts pose by
   pose against the packings published before it.
   A question that passes is recorded under the issue’s `awaiting_author`, naming the
   reply that asked it and what the answer could falsify.
   It holds the issue open: `check_requests` counts it against closeable, and the sweep
   lists it under the answer bead, and for a decision (chase, withdraw or keep waiting)
   once it has waited more than 14 days.
   When the answer comes, read it into the record and mark the question `answered`,
   naming the comment; when the record no longer needs it, mark it `withdrawn`, with a
   note saying why.
4. **Post the comment and close the issue** under the `github-workflows` grant, then
   record the comment under the issue’s `replies` as `final` and set the entry’s `state`
   and `closed` in the next change.
   Close the answer bead once the record no longer names it on an open issue, which
   `check_bead_tree` checks.

Each six-hourly check-in of a running pass does the same.
Until an issue is closed, `make intake` lists it under **Needs Action** and exits 1;
once GitHub shows it closed and the record does not, the item says to record the close
and post nothing. An issue held for the owner is listed for the owner and fails nothing.

### Announce a Significant Result

The owner’s decision of 22 October 2026: “We need a systematic process for the
significant results”, then “Let’s have it do S4 and S5 then”.
Every registered result at S4 or S5 has a News item: an entry in
[`site-changelog.yaml`](../site-changelog.yaml) that News shows, scored at the result’s
own score, with the result in its `result_ids`. S3 News stays optional, as
[Label the PR and Prepare News](#label-the-pr-and-prepare-news) says.

1. **Before the merge**, the pull request that registers a result at S4 or S5, or raises
   one to either (a stage 4 rescoring included), drafts the entry in its description
   under **News**, beside the announcement.
   An entry names only merged pull requests, by their retained merge date and commit, so
   it cannot land in the change it announces.
2. **Right after the deploy of that merge is verified**
   ([Verify the Published Result](#verify-the-published-result)), the pass’s coordinator
   opens the News follow-up, or the next records pull request carries it.
   From `packing/`, run
   `uv run --frozen --all-extras --group dev python -m devtools.import_changelog --pr NNN
   --significance-rationale "..." --output "$TMPDIR/changelog-candidate.yaml"` with the
   merged pull request’s number.
   Bring its delivery row, its coverage number and the reviewed entry into
   `site-changelog.yaml`, dated the delivery’s merge day as the record requires, and
   render with `python -m devtools.render_changelog`.
3. **The gate is the backstop.** The records tier’s “synopsis agrees with the artifacts”
   step, which pull-request CI runs, passes `--announcement-base` to
   `devtools.render_changelog`. A result registered or raised on the branch under test
   is reported as owed after the merge.
   Once it is on `main` without its item, the gate fails any pull request that edits
   `packing/frontier/results.yaml` or `packing/site-changelog.yaml`, measured against
   its merge base. That pull request is the one that can settle the debt, since the pull
   request that owes it has merged and its item now validates: add the item in it, or
   land this step’s follow-up first and merge `main`. The failure names the result, its
   score, the merged pull request the entry must name, the command that drafts it and
   who scored the result.
   Any other pull request gets a warning naming the result and the pull request that
   owes it, and passes.
   On `main` itself, a push or the scheduled run (`--announcement-base HEAD^1`), an owed
   item is only ever a warning, records change or not: pull-request CI enforces the
   rule, and a merged change can no longer act on a failure.
   The one way `main` sees an owed item is a records pull request that went green before
   an S4 or S5 merge and merged after it, and that must not turn `main` red.
   Letting the registering pull request carry its own item, which names that pull
   request and is stamped at merge as `landed` is, is `think-n51k`.

The fifteen S4 and S5 results that landed before the News archive existed, on 13 October
2026 (6279bd0e6), are exempt, listed with the score each is exempt at in
`render_changelog.ANNOUNCEMENT_EXEMPT`, which may only shrink.
Backfilling them as dated News, as T-060’s item was on 16 October (UTC), is a separate
decision. The gate exists because T-194, the S5 report of a Lean proof that
$s(19) = 3 + 4\sqrt{2}/3$, landed on 16 October and had no News item until 22 October:
completing the item “in the next change” was a step nothing checked, and its pull
request, #651, was never imported into the changelog.

### Report-Order Verdict Comments

Where a [report-order ledger](#several-reports-at-one-count) decided a pass’s counts,
each result issue gets one comment giving the verdicts at the counts it claims.
[`devtools.intake_comments`](../devtools/intake_comments.py) drafts them from the
ledger’s `ledger.json` and a `comments.yaml` beside it in the intake directory, from
`packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.intake_comments \
    campaign/issue-intake/<directory>/comments.yaml --out DIR
```

The tool owns the comment’s form: `@author,`, a thank-you and the rule, then a table of
each count’s side at 12 places, its verdict and the best side now, then a pointer to the
records pull request and the Claude Code footer.
A comment over many counts can lead with a summary and fold the table into `<details>`.
It refuses a draft that names a `T-NNN` or holds any `tree/` or `blob/` link, into
`main` as well as into a branch, and a result issue that has neither a comment nor a
stated skip. `comments.yaml` holds what one pass says that another would not:

- the issues that get a comment and their authors, and each issue skipped because
  another comment already covers it, with the reason;
- the records pull request, and how a holder or handle the ledger prints is named, by
  [the credit rule](../../epistemics.md#parallel-projects-and-their-credit);
- each comment’s own sentences.
  An owner decision a count waits on is one plain sentence.
  Where an earlier reply said otherwise, the comment says so and that “this evaluation
  replaces it”. A publication in a watched repository is named as a backticked
  `owner/repository@commit`, never as a link.

The verdict comment is a progress comment: it may go out before the records pull request
merges, because it names no id, rung or branch link.
When the ledger later changes what a posted comment stated, the comment is edited to the
regenerated draft, as deciding 17 of PR #574’s undecided comparisons in the 14 October
ledger required of the #574 and #593 comments.
The reply with ids and rungs follows the merge, as above.
Posting stays manual, under the `github-workflows` grant.
The drafts go to a scratch directory, not into the record, and `--check DIR` confirms
them against the committed ledger before they are posted.
Each posted comment’s id goes on the bead that owns the comments, and the comment is
recorded under the issue’s `replies` like any other reply.

### The Requests Record

[`result-requests.yaml`](result-requests.yaml) has one entry for each issue that reports
a result, a defect or a correction.
It records what the issue reports, and for each reported result the register and
evidence ids it maps to, or why it is not registered and whether it is queued.
A queued result or ask names the bead that does it as `bead`, and what it waits on as
`blocked_on`. It also names the beads that track the issue, the bead that answers it,
every reply posted with the state that reply reported, and when the issue can close.
An entry’s `kind` says what the record owes the author.
An entry whose kind is not `result-report` but whose issue reports a new item for intake
is marked `intake: true`, so that `--github` checks its label as it checks a result
report’s. It records no current rung.
[`devtools.check_requests`](../devtools/check_requests.py) derives each result’s state
from the register:

- *confirmed*, when every register entry it maps to is at `V3` and `C3` or above;
- *refuted* or *defect recorded*, from the entries’ reviews and evidence;
- *open* while validation runs, and *queued* while it waits for import.

A **reply is due** when the issue has had no reply; when an entry a result maps to has
no reply naming it under that result; when the entry has been renumbered since the last
reply that named it there; when one of its rung or status fields has moved since the
last reply that stated that field there; or when a reply’s statement is marked
`outdated` and no later reply `corrects` it.
A reply that mentions the result without naming the entry, or names the entry without
stating a field, leaves the earlier statement standing.
Each reason quotes the one reply it holds a field to, by its date, and by its kind or
its address where the issue has another reply that day.
An issue is **closeable** when triage is done, every result is confirmed or refuted (a
reported defect: recorded against the entry it names), no `ask` is queued, and no
question under `awaiting_author` awaits the author’s answer, and the owner does not hold
it (`held`). `awaiting_author` holds only the questions whose answers could falsify what
the record asserts and that no measurement here can settle: `changes` says whether the
credit, the lineage, or which file or commit a claim names, and `asked` is the recorded
reply that asked it.
`held` holds an issue for the owner, on the owner’s recorded instruction or on a
reservation for the owner that beads record, with its `basis`, the day it was recorded
here, the beads and a note: while it stands no pass posts on the issue or closes it.

A confirmation is described from the confirming evidence’s `relationship_to_generator`:
*reproduced with the author’s own checker* for `same-implementation`, *re-verified by an
independent implementation* for `independent-implementation`. The programs are the
entry’s `verifiers`, named from `frontier/verifiers.yaml`; without them no program is
named, and without a usable relation the report and the draft say it is not yet
recorded. An exact value is described by its lower half alone, as its confirmation is.

Run each command from `packing/` as
`uv run --frozen --all-extras --group dev python -m devtools.check_requests`, with:

| Option | What it does |
| --- | --- |
| none | The gate step: the schema holds and every id resolves; one line per issue |
| `--report` | A table per issue: each result’s entries, rungs, state, how it was confirmed and whether its id is on `main`; the replies due; whether it is closeable |
| `--backlog` | Every register entry below `V3` or `C3`, with its `next_rung`, its `activity`, the beads it names and the issues it serves |
| `--pending` | Every pending review (stage 7): the backlog’s entries, any entry naming an unfinished confirmation or activity, and the record index’s unassessed comparisons, each with its beads, its tracking issues and whether one states its present state; then the count with no tracking issue, the stale, those held for the owner and those tracked only on closed issues. It does not see the follow-up a settled comparison owes, nor a result an issue names only in an ask |
| `--draft N` | The status comment for issue N, ending in the Claude Code footer; it refuses unless `HEAD` is on `origin/main` |
| `--github` | Read-only: the issues the record lacks, the replies missing from it, the comments created or edited after an entry’s `read_through`, and the `result-report` entries and entries marked `intake: true` whose issues lack the `intake` label |

A reply due is reported and never fails the gate: it is owed after the merge, not a
broken record.

### After the Merge

1. On `main`, run `--github` and take into the record any issue, reply or comment it
   lacks. A new issue enters with `triage: pending`, and stage 1 maps its results.
2. For each issue that `--report` marks reply due, and each other issue the merged
   change touched, render `--draft N`, check that `main` and the deployed site say what
   it says, and post it; an agent does as part of the pass, or the owner does.
   `--report` marks what the register shows: no reply yet, a new or renumbered id, a
   moved rung or status, an `outdated` statement.
   A change it does not show, such as a case adopting the result, a supersession or a
   comment read into the record, is followed up by the pass that makes it.
3. Record the reply under the issue’s `replies` in the next change: its URL, date and
   kind, and in `reported` the id, rungs and status it stated for each result.
   Name in `corrects` any earlier reply whose `outdated` statements it corrects.
4. When `--report` says an issue is closeable, close it with the final comment and set
   the entry’s `state` and `closed`, as [Close a Settled Issue](#close-a-settled-issue)
   says.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
