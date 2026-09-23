# Pull-Request Cycle Receipt (W5 efficiency block, agenda-042, `think-oc16`, `think-du2j`)

Lane B of
[`agenda-042`](../../../../agendas/agenda-042-efficiency-block-the-development-cycle.md),
2026-09-23, against `main` at `f5c9c8453`. Measured by a delegated lane from the Actions
runs API over every workflow run on each of the last twenty merged pull requests’ head
branches, and from job logs for fifteen sampled red runs.
Section 4’s runner-minute figures are inferred from per-job averages, not measured per
run, and `think-d3z8` is the tool that would measure them.

Base: `main` = `f5c9c8453`. Sample: last 20 merged PRs (#200–#221, excludes #203/#210,
not present in the merged set).
Measured via `gh api actions/runs?branch=<headRefName>` (all workflow runs ever
triggered on each PR branch, not just the final green head) plus job/log inspection for
a representative sample of red runs.

## 1–2. Per-PR CI cycles and red-cause classification

“Cycles” = distinct pushed commits that triggered the `Packing validation` +
`Certificate page` (Pages) pull-request workflows on that branch (`Branch mergeability`
excluded from the count; a few PRs also had mergeability-only failures, noted below).
“Red” = a cycle where at least one of those workflow runs has `conclusion: failure`.

| PR | cycles | red | open→merge | size (+/‑ lines / files) | sampled cause of first red |
| ---: | ---: | ---: | ---: | ---: | --- |
| 221 | 5 | 2 | 5.3 h | 9,416 / 27 | record drift (composite-figure.json; PR body: “4 CI failures, cause was `--records` not `--push`, 4×”) |
| 220 | 2 | 0 | 2.1 h | 142 / 2 | — |
| 219 | 4 | 1 | 1.3 h | 201,662 / 103 | record drift (`session-close-report.yaml` had drifted) |
| 218 | 19 | 12 | 21.2 h | 21,289 / 112 | mixed: lint/type (ruff, biome/eslint/tsc) + wall-ceiling (type floor) — long-lived active branch |
| 217 | 2 | 0 | 0.1 h | 159 / 4 | — |
| 216 | 1 | 0 | 0.1 h | 401 / 4 | — |
| 215 | 5 | 0 | 0.4 h | 9,110 / 24 | — |
| 214 | 1 | 0 | 0.2 h | 726 / 7 | — |
| 213 | 4 | 0 | 0.5 h | 214,812 / 96 | — |
| 212 | 6 | 2 | 1.1 h | 168 / 4 | wall-check ceiling (`suite_b` record stale in flattering direction — this PR *is* OR-17) |
| 211 | 8 | 4 | 10.5 h | 66,361 / 206 | environment/flake — shared red-main state (`test_session_gate` corpus check), ×3 of 4 |
| 209 | 9 | 1 | 26.3 h | 9,842 / 58 | environment/flake — same `test_session_gate` failure, same time window as 208/211 |
| 208 | 5 | 1 | 27.7 h | 4,384 / 18 | environment/flake — same `test_session_gate` failure |
| 207 | 7 | 2 | 19.8 h | 10,282 / 42 | lint/format/type (ruff) |
| 206 | 7 | 2 | 20.8 h | 11,883 / 44 | genuine test failure (`ParentExperimentError`: declared dependency closure ≠ imports) |
| 205 | 10 | 3 | 25.4 h | 211,445 / 73 | wall-check ceiling (quick-lane sub-check: 14.44 s vs 12 s) |
| 204 | 4 | 0 | 26.4 h | 6,795 / 33 | — |
| 202 | 4 | 0 | 7.0 h | 3,880 / 70 | — |
| 201 | 25 | 3 | 24.3 h | 50,712 / 135 | unclear from log ("bead tree" step failed, no printed cause; other/inferred record-sync) |
| 200 | 23 | 9 | 29.1 h | 24,566 / 58 | wall-check ceiling (`geometry` stale record) + environment/flake (`suite-a` concurrency assertion) |
| **Total** | **151** | **42** |  |  | **red rate 27.8%** |

Note on self-report vs.
measured: PR #221’s own body says “five CI cycles, four of them red.”
The Actions API shows 5 `Packing validation` cycles on that branch with 2 `failure`
conclusions, plus one additional `Branch mergeability` failure (`7dd593eba1`) — 3
distinct red pushes visible via the API, not 4. The gap is most likely job-level
failures folded into one push counted as separate “causes” in the narrative (`sweeps`
failed twice, `suite-b` once, per the PR’s own disposition table).
**Finding: self-reported cycle counts in PR bodies are not reliably reconcilable against
`gh api actions/runs` at the push level** — the API is the more trustworthy instrument
for counting, the PR body is the better instrument for attributing cause.

## 2. Cause taxonomy (from 15 sampled red runs across 11 PRs, ~36% of the 42 red cycles, via job logs)

| Category | Samples seen | PRs |
| --- | ---: | --- |
| Wall-check ceiling (stale `gate-budgets.yaml` record, usually “flattering direction”) | 4 | 200 (geometry), 205 (suite-b quick-lane), 212 (suite-b), 218 (typecheck) |
| Environment/flake — shared red-main state (`test_session_gate` corpus check) | 4 | 208, 209, 211 (identical assertion, same ~2 h window), 200 (suite-a concurrency) |
| Lint/format/type | 3 | 218 (ruff, biome/eslint/tsc), 207 (ruff) |
| Generated artifact/record drift | 2 | 221 (composite figure etc., confirmed by PR body), 219 (`session-close-report.yaml`) |
| Genuine test failure (real bug) | 1 | 206 (`ParentExperimentError`, undeclared dependency) |
| Other/unclear | 1 | 201 ("bead tree" step, no cause printed in log) |

Two clusters worth naming directly: **208/209/211 all failed the identical assertion**
(`test_session_gate.py::…assert 1 == 0`) in an ~2-hour window on 2026‑09‑21 — PR #217,
merged the same day, is titled *“…main is red”* and documents `main` red at `c2cc1cf6`.
Three independent branches inherited genuinely broken shared state via merge/rebase; no
local tier run against a stale checkout could have caught it.
And **wall-ceiling staleness is the single most common visible cause** (4 of 15 sampled,
likely more of the un-sampled 27): `gate-budgets.yaml` records a timing, CI runs faster
than recorded ("stale in the flattering direction"), and the drift rule fails the step
on purpose — that is what OR-17 (merged as PR #212) exists to enforce.
Legitimate signal, but a local run cannot reproduce it: my `--edit` timing below shows
local wall time isn’t even compared against the ceiling once the CPU/job shape differs
from the reference shape.

## 3. Local tier vs. cost, by category

| Category | Tier that catches it | Local cost |
| --- | --- | --- |
| Generated artifact/record drift | `--push` (tests reachable from the diff) | “about a minute for a narrow code change” (development.md); PR #221’s own text: cause was running `--records` instead |
| Lint/format/type | `--edit` (48/80 steps) | measured today: **181.1 s wall** (3 m 1.7 s real) at 4 cpu/4-job shape against a 240 s ceiling — includes `type floor (basedpyright)` 181.1 s and `browser floor (biome/eslint/tsc)` 137.8 s as the two biggest line items. development.md’s reference figure is 59.4 s at the (unspecified, presumably 2‑cpu) reference shape |
| Genuine test failure (structural, e.g. PR 206) | `--edit` or `--push` | same order as above; cheap |
| Wall-check ceiling / snapshot-budget staleness | **No local tier reliably catches this.** `check_gate_budgets.py`’s drift/stale rule compares against a recorded shape (cpu/job count); my `--edit` run at 4cpu/4job printed *“note: within the declared band, but this run’s shape … is not the edit tier’s reference … so the band was reported and not enforced.”* This is fundamentally a hosted-CI-timing problem, addressed by `read_tier_walls.py` re-baselining the record, not by a contributor’s local run |  |
| Environment/flake (shared red-main state) | None — inherent to merge timing, not local validation | N/A; fixed by not building on/merging a red `main`, or by re-syncing before push |
| Other (bead tree, PR 201) | Likely `--records` (cheapest tier, 33/80 steps, ~11 s per development.md) but not confirmed from the log, which printed no error text for the failing step | ~11 s if confirmed |

## 4. Wall/runner-minute estimate (inferred, not directly measured per-run)

Using development.md’s per-job hosted averages (`checks` 75.67 s, `frontend` 85.25 s,
`typecheck` 55.67 s, `geometry` 102.73 s, `suite-a` 109.92 s, `suite-b` 102.91 s,
`sweeps` 101.51 s — 7 jobs run concurrently per cycle, ≈ 634 s of runner time and ≈
110–180 s of wall time per cycle including checkout overhead):

- 151 cycles × ~634 s runner time ≈ **1,595 runner-minutes (~26.6 runner-hours)** total.
- 151 cycles × ~180 s wall (OR-14’s 3-minute outer edge, consistent with what the
  sampled logs show) ≈ **453 minutes (~7.6 hours)** of cumulative wall time.
- Red share is 42/151 = 27.8% of cycles.
  A failing job does not finish faster than a passing one (it runs the same steps up to
  the failure point), so cost is proportionate: **≈ 443 runner-minutes (~7.4 h) and ≈
  126 minutes (~2.1 h) wall spent on red cycles**, vs.
  ≈ 1,152 runner-minutes / 327 minutes on green ones.
- **Gap: no existing tool in `devtools/` produces this number directly** —
  `check_gate_budgets.py` and `read_tier_walls.py` price *tiers*, not cumulative
  red-vs-green spend across a PR sample.
  That is a measurement gap worth naming rather than a tool I could reuse.

## 5. Review time / session-cost record

- Only **2 of the 20 PR bodies** (#221, #219) mention drafting/review “lanes” at all,
  and only **#221 gives quantified minutes**: “an Opus drafting lane at 23 minutes and a
  Fable review lane at 13” against “about three hours of machine time, almost all of it
  replay” (dilation-record derivation).
  The other 18 PR bodies carry no comparable breakdown.
- `packing/campaign/resource-usage/README.md` is explicit that its records are **inputs,
  not totals**: `wall_seconds` per session is “elapsed session time, including every
  interval in which nothing was running… an upper bound on work and never a measure of
  it,” and totals must be read from `session-close-report.yaml` → SYNOPSIS.md’s
  “Sessions Conducted,” not summed from the 308 per-log files directly (double-counting
  risk when one log is claimed by several sessions).
- SYNOPSIS.md’s Rollups table (line ~4453) gives wall time per session (e.g.
  session-083: 15.16 h wall over 34 rollups) but **no field splits that wall time into
  work vs. review vs. gate-run vs.
  CI-wait** — those splits exist only as prose in a small minority of PR bodies
  (drafting/review lane minutes), not as a structured, queryable field.
- **Conclusion: the record is not consistent enough to act on.** Drafting/review-lane
  timing is reported ad hoc (1 of 20 PRs with numbers), CI-cycle cost is sometimes
  narrated (PR #221) but not reliably reconcilable against the Actions API (§1), and
  gate vs. CI-wait time is not separated anywhere in the schema-validated records.
  Anyone wanting to act on “how much of a session goes to review vs.
  CI” today would be reading PR-body prose, not a table.

## 6. Top 3 process levers (confirm/refute against the data above)

1. **Make `--push` cheap enough that skipping it is irrational, and enforce it (a
   pre-push hook), not just document it.** Confirmed as the highest-leverage fix: PR
   #221’s 4 record-drift failures across 5 CI cycles ("almost all of it replay," ~3 h
   machine time) had a stated cause of running `--records` (11 s) instead of `--push`
   ("about a minute for a narrow change" per development.md).
   AGENTS.md already says to run `--push` before pushing; the gap is enforcement, not
   cost. `make
   hooks-install` already wires a pre-commit hook for formatting — a pre-push hook is
   the same shape of fix.
2. **Re-baseline `gate-budgets.yaml` on a schedule, not live on whoever’s PR trips it.**
   The largest *visible-cause* category sampled (4 of 15): CI genuinely got faster and
   the drift rule — working as OR-17 intends — fails the step.
   Legitimate signal, but it lands as red CI unrelated to the change that trips it.
   `read_tier_walls.py` already exists for re-measuring; the lever is running it
   periodically (or after any CI-runner-class change) instead of only reactively.
3. **Keep `main`’s red-time short, or make PRs re-sync just before push.** PRs #208,
   #209, #211 independently hit the identical `test_session_gate` assertion in the same
   ~2-hour window while `main` was red at `c2cc1cf6` (PR #217’s diagnosis) — a
   hosted-only check had let a red merge through green PR-tier CI. No local tier catches
   this; it is purely a function of when a branch last synced.
   All three PRs also had 20+ hour open→merge times, consistent with a stale base.

Weaker support: “generated-artifact drift checks in the edit tier” is partly true
already — `--push`, not `--edit`, is what catches PR #221’s drift; moving that coverage
earlier would need those specific checks reclassified, a narrower fix than levers 1–3.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
