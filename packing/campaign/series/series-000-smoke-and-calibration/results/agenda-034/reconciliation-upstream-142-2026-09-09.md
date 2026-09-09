# Agenda 034: reconciliation against PR 142, and why PR 145 was left out, 2026-09-09

The third reconciliation of this branch against the codex ownership line, and the second
that renumbered. Its predecessor in this directory,
[`reconciliation-upstream-2026-09-09.md`](reconciliation-upstream-2026-09-09.md), covers
the round against PR 137.

The codex line is three stacked pull requests:

| PR | branch | head | base | state |
| --- | --- | --- | --- | --- |
| 137 | `codex/n11-ownership-continuation` | `e6a01449` | already in this branch | merged earlier |
| 142 | `codex/n11-independent-owner-audit` | `8a35b482` | 137 | **merged here** |
| 145 | `codex/n11-owner-core-compatibility` | `2acf4b85` | 142 | draft, **deliberately not merged** |

`e6a01449` is the merge base, so merging `origin/codex/n11-independent-owner-audit`
brought PR 137 and PR 142 together: 103 files and 222,703 insertions.

## Why PR 145 was left out

**This is a decision, not an oversight, and the numbering gaps it leaves are reserved
rather than lost.**

PR 145 is a draft, and its last session is still running.
`session-122-direct-sixth-site-feasibility.md` carries top-level `status: in_progress`,
`stop_reason: null` and `deadline_at: 2026-09-09T20:18:31Z`. The campaign record judges
a clocked in-progress session against HEAD’s committer date, and `commit_clock.py`
offers no override, so merging that snapshot made this tree fail its own clock: their
tip is dated `2026-09-09T19:27:50Z`, before that deadline, so their branch is
self-consistent, but every commit of ours lands after it.

The two ways to make it pass were to mark their session stopped, which the schema then
requires a `stop_reason` for, or to drop its `deadline_at`, which the schema permits.
Both are assertions about another agent’s live, unfinished session, and neither is
accurate on this branch.
So the session is not carried at all.

PR 142 is the non-draft, ready line, and it ends at `session-120`, which is
`status: stopped` with a real stop reason — a complete, self-consistent record.
The five commits beyond it (`49b6d6ff`, `c8cd38da`, `0a4fe687`, `da1e42ac`, `2acf4b85`)
are PR 145’s draft work and carry the live session.
They are taken later, when that session closes and 145 stops being a draft.

The renumbering that preceded this merge was done against 145’s tip, so it cleared more
than 142 needed, and the surplus is deliberate.
The record now runs H-140 to H-147 and then H-152 to H-157, sessions 112 to 120 and then
123, idea rows 135 to 143 and then 148 to 153. `H-148` to `H-151`, `session-121` and
`session-122`, and rows 144 to 147 are the slots PR 145 already occupies upstream.
Leaving them empty is what makes this branch’s numbering forward-compatible: when 145
lands, it lands in its own slots and nothing needs renaming a fourth time.

## 1. The collision audit, re-verified twice

Every row was re-measured against `2acf4b85` before the renames, and the whole set was
re-measured against `8a35b482` before this merge was resolved.

| class | ours | PR 145 tip | PR 142 head | verified |
| --- | --- | --- | --- | --- |
| hypotheses | H-143 to H-147, H-149 | H-143 to H-151 | H-143 to H-147 | six collided with 145, five with 142 |
| idea rows | 139 to 144 | 139 to 147 | 139 to 143 | six collided with 145, five with 142 |
| results directory | `results/agenda-033/`, 97 files | same name, 49 files | same name, 35 files | collides with both; filenames disjoint from both |
| agenda document | none registered | `agenda-033-overnight-owner-geometry.md` | same | theirs owns the number on both |
| session record | `session-114-...` | `session-114` to `session-122` | `session-114` to `session-120` | collides with both |
| results `T-` | T-024, T-025, T-026 | stops at T-023 | stops at T-023 | no collision; both edit the shared `T-023` |
| explorations | X-023, X-024, X-026 | none added | none added | no collision |
| defects | D-489 | stops at D-488 | stops at D-488 | no collision |
| evidence ids | 12 new | 3 new | the same 3 | no collision; 79 ids after the union |
| `exp-` ids | none used | exp-145 to exp-153 | exp-145 to exp-149 | no collision |

One figure in the original audit had moved before the renames began: our results
directory held 97 files, not the 74 recorded, because `5a8c3338` and `2d6b8aa6` added 23
more after the audit was taken.
Both are our own commits, the filename intersection with theirs is empty on both refs,
and no mapping depends on the count, so the rename went ahead as written.

Anything that collided with 145 but not with 142 simply stays renumbered.
That costs nothing and is what reserves the slots described above.

Two things neither audit recorded.
Their line edits our shared `T-023` rather than only appending: it adds an artifact, a
control, the `E-n011-five-dot-independent-union` evidence id, and revised `composition`,
`next_rung` and `notes` prose recording exp145’s independent inclusion-exclusion replay.
Our side is byte-identical to the merge base there, so the three-way merge took theirs
with no judgement required, and the claim, the rung and the grades are unchanged.
Their `T-023` stays conditional and moves no bracket, so our verified lower bound is
untouched and remains `s(11) >= 3.826447410572939`. The `kpress` submodule pointer is
`515f4a08` on our side, on theirs and at the merge base, so there was nothing to
resolve, and the merged index carries it.

## 2. The rename map

The codex line wins every collision, as it did around PR 137: it carries seven session
records to our one and it registered the agenda document that owns `agenda-033`. Sources
and targets are disjoint within each class, so one simultaneous pass per class was safe.
Every pass ran through `uvx repren` after a dry run whose output was read and whose
match count was checked against an independent count.

| from | to | scope | matches |
| --- | --- | --- | --- |
| `H-143` | `H-152` | repository, `\b`-anchored, file renames included | 102 over 19 files, 6 renamed |
| `H-144` | `H-153` | " | " |
| `H-145` | `H-154` | " | " |
| `H-146` | `H-155` | " | " |
| `H-147` | `H-156` | " | " |
| `H-149` | `H-157` | " | " |
| idea rows `139` to `144` | `148` to `153` | `ideas.md` only, anchored to the table cell | 6 |
| `results/agenda-033/` | `results/agenda-034/` | `git mv`, then repository-wide reference pass | 97 files, 137 references over 35 files |
| `session-114-past-the-point-atom-ceiling` | `session-123-past-the-point-atom-ceiling` | repository, file rename included | 8 over 4 files |

The idea rows were matched on the table cell, `^\| 139 \|`, rather than on the digits.
That was not caution: `research-2026-08-22-packing-11-unit-squares.md` and
`CERTIFICATE-REACH.md` both carry unrelated rows numbered 139 to 144, where the number
is a square count, and a bare pattern would have renumbered eleven of them.

Two files were deliberately left holding a stale identifier.
`ceiling-family-191-50.json` carries no agenda reference, so its SHA-256
`95cf06473f185764076d21021b75cc65962ef6b68dc717c045c2c7d76ae12427` — pinned as
`RETAINED_SHA256` in `devtools/independent_ceiling_reader.py` and quoted in X-023 and
three lane reports — survived the directory move unchanged, checked before and after.
The resource-usage rollup `cd8c0aac-f931-5096-97c8-3cccdcaa8ba9.yaml` keeps its
historical `agenda-033` token: it is a YAML mapping key recording a tool invocation as
it was made, three neighbouring tokens in the same key are already stale against the
current document, and nothing resolves it as a path, so rewriting one token would have
made a measurement record false rather than current.

`reconciliation-upstream-2026-09-09.md` was renamed with everything else, because after
the merge a reader following its `H-143` would land on the codex line’s independent
five-dot union rather than on the threshold certificate it meant.
Its second amendment paragraph was rewritten to stop quoting the second round’s numbers,
and a third amendment records this round.

## 3. What the merge resolved

`git merge --no-ff` produced six conflicts.
`ideas.md`, `n-011.md`, `evidence.yaml` and `RESULTS.md` merged without one, which is
the renaming working.

| file | shape | resolution |
| --- | --- | --- |
| `packing/frontier/results.yaml` | their `T-023` notes tail against our appended T-024, T-025, T-026 | union: their `T-023`, then our three results. 26 entries, checked structurally against both sides |
| `packing/campaign/session-close-report.yaml` | their seven session entries against our one, plus a derived count block | union in id order; counts re-derived by `close_session --render`, since neither side’s was right for the union |
| `docs/project/document-map.yaml` | our three document rows against their seven, sharing a three-line tail | union with the tail restored to our last entry — a plain concatenation would have orphaned `role`, `authority` and `lifecycle`. 320 entries, none missing a required field, no duplicate paths |
| `SYNOPSIS.md` | four hunks: derived ledger counts, the document table, the hypothesis-status table, the coverage block | tables unioned in id order; both count blocks re-derived. The aggregate sentence came from `check_synopsis`, which names the expected wording |
| `packing/campaign/ledger.md` | generated view: session rows, workflow totals, hypothesis rows | unioned, then rebuilt by `packing-ledger render` |
| `packing/frontier/INVENTORY.md` | generated view: two derived count blocks | rebuilt by `render_evidence_inventory --update` |

Every generated view was re-rendered afterwards: `render_results --update`,
`render_results_headline`, `render_evidence_inventory --update`,
`render_research_tables`, `render_certificate_reach`, `render_document_map`,
`build_composite_figure_data --update`, `render_composite_pdf --update`,
`packing-ledger render` and `close_session --render`.

The `n-011.md` front-matter evidence list is a union of twenty ids, seventeen ours and
nine theirs over a shared six, with nothing dropped and nothing invented.
The verified lower bound reads `3.826447410572939` in all three places it appears.

## 4. The exp-137 receipt: their prune, our citation

Their line prunes `agenda-032/exp-137-corner-dual-salvage.json.gz`, 11,552,761 bytes,
from every mutation-control worker on the ground that nothing needs it there, and holds
that with `test_dual_salvage_receipt_is_not_a_mutation_worker_input`. Two of that test’s
three assertions were unaffected by the merge: the receipt is named neither in
`devtools/controls.yaml` nor in any control’s `run`. The third failed, because
`lane-x2-owner-instrument-survey.md` in this directory cited the receipt by inline
Markdown link, and `linked_pruned_targets` restores any pruned file a tracked document
links, so that the in-worker link scan refuses dead links rather than every control
failing on one. That restoration rule is load-bearing and carries three recorded
incidents behind it.

Neither branch failed alone — the test is theirs, the citation is ours — and the rename
is not implicated, since the link sat at `../agenda-032/…` at the same depth before and
after.

**Resolved on our side, by dropping the link and keeping the path.** The citation now
reads as a plain backticked path, so it stays legible and keeps its meaning while no
longer pulling 11.5 MB into every worker.
Their prune was not touched and the snapshot cap was not raised: this was never a size
problem, and the snapshot now measures 130,852,246 bytes against the 167,772,160 cap,
78.0% with 36.9 MB of headroom.
The four other individually pruned files a tracked document still links are the
known-best atlas images cited from `README.md` and `SYNOPSIS.md`; they predate this
work, nothing asserts they stay out, and they were left alone.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
