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
  they are credited, the `V`, `C` and `S` ratings, and the three end points.
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
   [the table below](#intake-sources) and prints each item the record has not taken in.
   It exits nonzero while any item lacks an open bead to own it, or waits on something
   that has already happened.
   Read **Needs Action** first, then **Not Checked**: a source the sweep could not read
   is not a clean source.
2. **Own each item** as [stage 0](#stage-0-sweep) says: a bead for each new result, a
   recorded read where there is nothing to import, a new owner for any deferral whose
   bead has closed, and a restart for any wait whose blocker has resolved.
3. **Import** each new result through stages 1 to 3 on the same branch.
   A stage 4 replay the source prices at minutes can run in the same branch; a longer
   one waits in its bead for a budget the owner sets.
4. **Validate** from `packing/` with `packing-validate --records`, then `--push`.
5. **Open one draft pull request** with `tbd shortcut create-or-update-pr-simple`. It
   lists each item with its bead and the stage it reached, and every source under Not
   Checked.
6. **Draft the replies** each issue is owed, in its answer bead.
   They are posted after the merge, from `main`, by the owner or at the owner’s request
   ([stage 7](#stage-7-answer)).
7. **Sweep again** with `make intake`, after the branch’s changes to the records.
   The pass is done when nothing needs action, or when the pull request says why each
   remaining item waits.

The pass needs network access to `github.com`, for Git and for the API through `gh`;
`kingbird.myphotos.cc`, for the catalogue capture; `evand.github.io`, for imports from
Evan Daniel’s site, which his repository builds; and `pypi.org` with
`files.pythonhosted.org`, for the pinned transcriber.
A source the environment denies is reported as not checked, and the pull request says
so. On 2026-10-05 the agent sessions reached GitHub and PyPI and nothing else.

A pass never merges, never posts, edits or closes anything on an issue without the
owner’s word, never pushes to `main`, and never starts a replay measured in CPU-hours
without a budget the owner has set.

### The Prompt

A session asked to run the intake takes this as its instruction:

```text
Run an intake pass on jlevy/squares by packing/campaign/result-import.md, section
"Running an Intake Pass". Work on a new branch from origin/main named
claude/intake-YYYY-MM-DD, with today's date.

1. Bootstrap the clone as AGENTS.md, "A fresh clone", says; run `tbd prime` and
   `tbd policy show`.
2. From the repository root run `make intake`. Read the report: "Needs Action"
   first, then "Not Checked".
3. For each item that needs an owner, look for an open bead that already covers it
   (`tbd list --label result-import`). Otherwise open one bead per new result,
   labelled result-import and titled "Import <author>: <claim> (#<issue>)", or
   "(no issue)" when nothing on GitHub asked. A watched repository whose new commits
   hold nothing to import gets a read in packing/campaign/intake-watch.yaml instead,
   with a note saying what changed. A deferral whose bead has closed gets a new owner
   or is resolved. An item whose blocker has resolved is resumed on this branch, or
   its bead says what it waits on now. Run `tbd sync`.
4. Take each new result through stages 1 to 3 of the runbook on this branch: triage,
   retain the source in a packet at a pinned revision, register it as reported. Run a
   stage 4 replay only when the source prices it at minutes; otherwise record it in
   the bead for a budget.
5. From packing/, run `uv run --frozen --all-extras --group dev packing-validate
   --records`, then `--push`, and fix what fails.
6. Commit, push the branch, and open one draft pull request with
   `tbd shortcut create-or-update-pr-simple`. List every item with its bead and the
   stage it reached, and every source the sweep could not check.
7. Draft each reply an issue is owed in its answer bead. Do not post it.
8. Run `make intake` again and report every item that still needs action.

Never merge, never push to main, never post, edit or close anything on a GitHub issue
without the owner's word, and never start a replay measured in CPU-hours without a
budget the owner has set. If github.com, kingbird.myphotos.cc or evand.github.io is
unreachable, say so in the pull request and continue with the rest.
```

## Intake Sources

Every input reaches the record through one of these sources, and the sweep reads each.

| Source | How it is read | What an item becomes |
| --- | --- | --- |
| GitHub issues and comments | `check_requests --github` lists the issues `result-requests.yaml` lacks, the replies missing from it, and the comments after an entry’s `read_through` | A new issue: an entry with `triage: pending` and an import bead. A comment: its claims mapped into its issue’s entry, and `read_through` moved |
| Owner and other manual reports | Nothing reads them: a message, a link pasted to an agent, a result named in a review | A bead labelled `result-import` first, titled with `(no issue)`; then stage 1. The sweep lists the open ones |
| The Kingbird catalogue | [`devtools.capture_kingbird_catalogue`](../devtools/capture_kingbird_catalogue.py) fetches and transcribes it into `attic/intake/`; the sweep compares the newest capture with the record’s, count by count | A count whose side drops below its record: an import, or a `pending_catalogue_intake` entry with its bead. Other changes: classified when the retained capture is refreshed. None when nothing moved |
| Other catalogues and releases | Read by hand: the register’s other `current-catalogue` and `first-party-release` sources, UnitSquare’s release today. The sweep prints when each was last reviewed | A later release: an import. Nothing new: the source’s `reviewed` date moves |
| Watched repositories | Every repository the source register, a packet’s acquisition record, or the site’s list of other projects names. `git ls-remote` reads each head, and a fetch of commits and trees finds the commits past every pin and every read, and the commits a pin contains whose changed paths no packet at or after them retains | A new result: an import bead, then a packet at the head. New evidence for a registered entry: an evidence update. Nothing to import: a read in [`intake-watch.yaml`](intake-watch.yaml) |
| The record’s own queues | Counts pending catalogue intake, deferred conflicts, results and asks queued on open issues, triage and replies owed, the validation backlog | Nothing new: each names an open bead, and one whose bead has closed gets a new owner |
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
| 0. Sweep | W1 | Every input the sweep lists has an open bead, or a read that records nothing to import |
| 1. Triage | W1 | A claim map and a priced validation plan in the import’s bead; the author acknowledged |
| 2. Retain | W1 | The source in a packet at a pinned revision, with its bibliography key |
| 3. Record | W1 | The claim registered as reported, with its coverage entry, and merged: *imported* |
| 4. Validate | W2 | Replay evidence, a mapped review and the rungs they derive: status `confirmed`, or `incomplete` |
| 5. Publish | The change that moves the record | The reader documents state the result; once stage 4 has passed, *integrated* |
| 6. Explain | W8, with a W2 review | A review paper, for the results that warrant one |
| 7. Answer | The owner | The reply on the issue: *answered* |

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
  likely to say it was left for an import of its own, as the 4 October wand125 packet
  said of `c56b9b7` and `1ebd484`.
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
  Nothing resumes a wait when its blocker resolves, so the sweep reports it: wand125’s 4
  October certificates waited for #305, which merged that evening, and stayed queued.

## Stage 1: Triage

Triage decides what the import is before anything is retained, in an hour or less.

1. **Pin the source**, the author’s own publication and not a report of it, at a full
   commit id or a DOI with file checksums: its current head, unless the claim depends on
   an older revision.
2. **List every claim the release makes**, including those the request does not mention.
   Issue 227 asked about $n = 102$ and $103$; the source held 49 packings.
   A claim in scope that the request does not mention becomes an import of its own.
3. **Map each claim to the register** by the table below, and say who else holds each
   value.
4. **Price the validation:** the checkers a complete replay needs, the cost the source
   reports, and whether anything here decides the certificate without the source’s code.
   A missing tool is a W7 slice, and the plan says so.
5. **Open the bead and draft the acknowledgement:** what was received, the revision
   pinned, and what will be checked.
   It states no `T-NNN` and no rung, and the owner, or an agent at the owner’s request,
   posts it within a day.

| Claim | Register action |
| --- | --- |
| A bound or an exact value the record does not hold | A new entry; each exact value has its own |
| Bounds of one kind at several counts in one release | One entry whose `scope` covers them |
| A later release that raises an earlier entry’s values or adds counts | A new entry; the earlier one keeps its claim, and the case records decide which is current |
| A theorem with an unbounded parameter | One entry stating the theorem, whose `scope` lists the cases this record holds |
| A second certificate for a value the record holds | A new `simplification` entry |
| A consequence of another claim, such as monotonicity, at a count where the record holds no such value | Its own entry only when it settles a case; otherwise the parent’s `scope` covers it |
| A consequence that another entry already registers | No new entry and no change of scope: both stand, and the older claim gains a sentence naming the newer route |
| New evidence or an author’s answer about a registered entry | No new entry: the source retained at the revision that holds it, and an evidence update |
| A request for a result already registered | No new entry: link the issue and continue from the entry’s stage |
| Below the standing bound and asking for no work | None; it stays in the packet |

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
- **The bibliography key** carries the date of the pinned revision as `dated`, and is
  defined in the [resources README](../resources/README.md) as well.
  Credit is read from the source’s own files, now and not after the review.

## Stage 3: Record

Record the claim as reported, by the frontier README’s rules: a reported evidence entry,
a coverage entry that cites it, the reported lane of each case it improves, and a
register entry with its ratings and `next_rung`. Four rules are the process’s own:

- **`attribution.published` is the claim’s date, not the pin’s:** the date the source
  gives for it, or the UTC date of the first commit that contains the certificate; for
  an entry over several certificates, the last of those dates.
- **The entry’s `scope` is covered** by the scopes of the evidence it cites.
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
- **The `T-NNN` is taken last.** An id is its row’s position and cannot be reserved
  across branches, so take it in the commit that registers the result, merge that day,
  and quote it to no author until it is on `main`.
- **Exact facts are recorded with their source.** A result that changes a best known
  packing, or states its side exactly, writes `reported_upper_bound.exact_form`,
  `algebraic_degree`, `minimal_polynomial` and `algebraic_source`. The source is
  `catalogue` where it prints the degree or polynomial, `derived-from-exact-form` where
  this repository computes them from a closed form, and `contact-system` where they come
  from an exact contact system, with that evidence cited.
  `sqpack.exact_values.algebraic_fields` writes the first two cases, and the frontier
  generator and the upper-bound intakes call it, so a catalogue or packet intake arrives
  complete. A new best known packing with no exact fact writes all four as null, which
  leaves the count numeric-only in the
  [exact side values register](../frontier/exact-values.json) until an identification
  lands.

The record checks pass without a packet, a coverage entry or evidence over the whole
scope. The reviewer of the pull request looks for those.

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

**The exit** follows both lanes.
It adds the replay evidence, moves the verified lane if the review has no blocking
defect open, rewrites the entry’s `claim`, `notes` and `next_rung` together and removes
its `activity`, so that no field says a replay is pending while another says it passed.
The reviewer also confirms or changes the draft significance score.
An open defect goes to the author with the review.

The reviewer of the pull request checks one thing in every sentence the stage writes:
where the claim, the case record, the review or the reply says the result is
*confirmed*, it says which confirmation, reproduced with the producer’s code,
re-implemented sharing named components, or independently re-implemented.
The checker holds the register’s `claim`, `composition` and `next_rung` to it; the case
record, the review and the reply are held to it here.

## Stage 5: Publish

The pull request that registers or raises a result runs
[New Result Publication](documentation-pass.md#new-result-publication): the views are
rendered in the commit that changes the record, and the data pin moves in the next.
No documentation phase is opened for it.
Where the result changes an exact fact, those views include the exact side values
register (`devtools.build_exact_values --update`) and its paper
(`devtools.render_exact_side_values`). The gate’s register check fails until the
register is regenerated, and the Pages workflow rebuilds the paper from it on every
change, since the register is one of the paper’s declared inputs.

### Verify the Published Result

An import’s publication includes its public results and drawings.
Passing a local build or PR CI establishes the candidate; verify the deployed main tree
before the final publication reply in stage 7.

Before merge, check the generated result/evidence registers, owning case pages, bound
citations and selected case/overview graphics together.
Each drawn packing must match its selected exact source geometry and displayed safe
ceiling. A confirmation label must refer to evidence for that displayed bound, rather
than an earlier, weaker ceiling.
Preserve the source’s decimal print as a quote and the earlier certificate as history
when a tighter reported packing supersedes it.
Inspect representative desktop and mobile views for cropped drawings, missing source
credit or unreadable labels.

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
([the series plan](../../docs/project/specs/active/plan-2026-10-05-n11-explainer-series.md)).

## Stage 7: Answer

[epistemics.md](../../epistemics.md#import-integration-and-reply) says what an answer
contains and who posts it.
The process adds when and how:

- An agent drafts the reply in the bead when the pull request merges.
- A reply is written after the merge and links only to `main`. A link into a working
  branch dies with the branch, and a `T-NNN` quoted from one can change.
- There is one reply when the result is imported and one when it is confirmed or a
  defect is found, and a follow-up whenever the record moves past what a reply said.
  The reply that reports a confirmation names the programs that ran, and says whether
  they were the author’s own code re-run or a re-implementation.
- The issue is closed with a final comment when nothing the author asked for is queued.

### The Requests Record

[`result-requests.yaml`](result-requests.yaml) has one entry for each issue that reports
a result, a defect or a correction.
It records what the issue reports, and for each reported result the register and
evidence ids it maps to, or why it is not registered and whether it is queued.
A queued result or ask names the bead that does it as `bead`, and what it waits on as
`blocked_on`. It also names the beads that track the issue, the bead that answers it,
every reply posted with the state that reply reported, and when the issue can close.
It records no current rung.
[`devtools.check_requests`](../devtools/check_requests.py) derives each result’s state
from the register:

- *confirmed*, when every register entry it maps to is at `V3` and `C3` or above;
- *refuted* or *defect recorded*, from the entries’ reviews and evidence;
- *open* while validation runs, and *queued* while it waits for import.

A **reply is due** when the issue has had no reply, when an entry has been registered,
renumbered or moved a rung since the last reply that spoke of it, or when a reply’s
statement is marked `outdated` and no later reply `corrects` it.
An issue is **closeable** when triage is done, every result is confirmed or refuted (a
reported defect: recorded against the entry it names), and no `ask` is queued.

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
| `--draft N` | The status comment for issue N, ending in the Claude Code footer; it refuses unless `HEAD` is on `origin/main` |
| `--github` | Read-only: the issues the record lacks, the replies missing from it and the comments after an entry’s `read_through` |

A reply due is reported and never fails the gate: it is the owner’s next move, not a
broken record.

### After the Merge

1. On `main`, run `--github` and take into the record any issue, reply or comment it
   lacks. A new issue enters with `triage: pending`, and stage 1 maps its results.
2. For each issue that `--report` marks reply due, render `--draft N`. The owner posts
   it, or an agent does at the owner’s request.
3. Record the reply under the issue’s `replies`: its URL, date and kind, and in
   `reported` the id, rungs and status it stated for each result.
   Name in `corrects` any earlier reply whose `outdated` statements it corrects.
4. When `--report` says an issue is closeable, close it with the final comment and set
   the entry’s `state` and `closed`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
