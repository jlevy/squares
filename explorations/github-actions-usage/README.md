# GitHub Actions Usage Analysis

An investigation into GitHub Actions overages across all 153 repos on the `jlevy`
account, reconstructed from the Actions API (window: Jul 1 – Aug 22, 2026).

## Verdict

One repo caused the overage: **fdu** (private).
Its CI came online Aug 8 and consumed **32,690 billable quota-minutes in 15 days** — 96%
of all billable usage, roughly $262 at standard pay-as-you-go rates.
The account crossed the Free tier’s 2,000 included minutes on Aug 10 and Pro’s 3,000 on
Aug 11.

Billable usage by repo (per-job minutes rounded up, OS multipliers applied):

| Repo | Visibility | Quota-min | Est. cost | When |
| --- | --- | ---: | ---: | --- |
| fdu | private | 32,690 | $261.52 | Aug 8–22 |
| fsqlite | private | 1,292 | $10.34 | Aug 1–2 |
| ojoshe | private | 132 | $1.06 | July |
| k-guide | private | 82 | $0.66 | August |
| 99 public repos with workflows | public | 0 | $0.00 | — |

Public repos are free on standard runners, so the busiest repos by wall-clock (`tbd` at
2,327 run-min, `metabrowser` at 498) cost nothing.
Job labels confirm no repo uses paid larger runners.
Storage (artifacts, caches) is ~0 GB — this is purely a compute-minutes problem.

## Why fdu is expensive

Its `CI` workflow runs on every pull-request push (89% of its minutes) with no
`concurrency` cancellation, and each run includes a 3-OS test matrix plus a
9-combination Python wheel build (3 Python versions × ubuntu/windows/macos).
macOS bills at 10× and Windows at 2×, so 12,115 raw runner-minutes became 32,690 billed
ones:

| Runner | Job group | Raw min | Quota min | Est. cost |
| --- | --- | ---: | ---: | ---: |
| macOS | wheel builds | 1,055 | 10,550 | $84.40 |
| macOS | test matrix | 718 | 7,180 | $57.44 |
| Windows | wheel builds | 2,731 | 5,462 | $43.70 |
| Windows | test matrix | 1,887 | 3,774 | $30.19 |
| Linux | everything | 5,724 | 5,724 | $45.79 |

## Recommended fixes, ranked by savings

1. **Build wheels on release/nightly, not per PR push** (~$139/mo): move the `python`
   job to `on: release` plus a nightly cron; keep one `ubuntu-latest` wheel smoke-build
   in PR CI.
2. **Gate macOS/Windows tests to merges to main** (~$78/mo): the cross-OS watch tests
   (inotify/FSEvents/ReadDirectoryChangesW) are intentional per the workflow’s comments,
   but they don’t need to run on every push — main-merge plus an opt-in `full-ci` label
   keeps the coverage.
3. **Cancel superseded runs** (20–40% of PR minutes): only 4 of 287 runs were cancelled.
   Add `concurrency: { group: ci-${{ github.ref }}, cancel-in-progress: true }`.
4. **Or make fdu public** — standard runners become free entirely.
5. **Same trim for fsqlite** (~$9/mo): its `Verify (macos-latest)` job is 73% of that
   repo’s bill.
6. **Set a spending limit** (Settings → Billing → Spending limits) as a guardrail
   against the next surprise.

Also worth knowing: 75 of fdu’s 287 runs failed, and failed runs bill the same as green
ones.

## Method

The billing API (`/users/{user}/settings/billing/usage`) needs a `user`-scoped token,
which the analysis session didn’t have.
Instead, `actions_usage.py` reconstructs billing from the data the meter is computed
from:

1. List every repo, then every workflow run in the window (1,949 runs across 26 active
   repos), splitting date windows to stay under the API’s 1000-results-per-query cap.
2. Fetch per-job timings for every private-repo run (445 runs); round each job up to the
   whole minute and apply the OS multiplier — the same arithmetic GitHub uses for
   standard runners. Public repos get a label-check sample to detect paid larger runners.

Caveats: pre-latest re-run attempts aren’t counted (1 existed); dollar figures assume
standard PAYG rates (Linux $0.008, Windows $0.016, macOS $0.08 per minute).
For GitHub’s own ledger, use a `user`-scoped PAT with
`gh api "/users/jlevy/settings/billing/usage?year=2026&month=8"`, or download the usage
CSV from Settings → Billing & licensing → Usage.

## Rerunning

```bash
# Any token with repo scope; uses gh for auth. Caches into .cache/ (rerun-safe).
./actions_usage.py --owner jlevy --since 2026-08-01
./actions_usage.py --owner jlevy --since 2026-08-01 --report-only   # summarize again
```
