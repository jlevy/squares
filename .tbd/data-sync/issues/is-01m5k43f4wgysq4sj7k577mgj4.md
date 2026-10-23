---
type: is
id: is-01m5k43f4wgysq4sj7k577mgj4
title: "Release-impact gate: a dirty tree at origin/main is judged as main's delivery (HEAD^1), so uncommitted edits ride the merged PR's records"
kind: bug
status: open
priority: 2
version: 1
labels:
  - validation
  - tooling
dependencies: []
created_at: 2026-10-23T00:55:46.588Z
updated_at: 2026-10-23T00:55:46.588Z
---
Found on #739 (c-lane-sweep-1023a, 23 October 2026). `validate._synopsis` (packing/src/sqpack/cli/validate.py, near line 3683) decides it is "on main" from `git rev-parse HEAD == git rev-parse origin/main` alone, and then runs `check_release_impact --base HEAD^1` (delivery mode) instead of `--baseline-ref origin/main`. A branch freshly cut from origin/main whose edits are not yet committed has HEAD == origin/main, so a local `packing-validate --records` (or --edit, --push) before the branch's first commit judges the working tree as main's merge delivery: the base becomes the merge's first parent, and the uncommitted edits ride the just-merged PR's fresh ReleaseNoPublicChange records.

Observed: #739's edits to packing/campaign/result-requests.yaml were validated on a branch at e929137a8 (#725's merge) before committing. The local records tier passed "release impact: every publication candidate has a reviewed disposition", listing #725's paths (adopt_houses.py, n-105.md, results.yaml, ...), i.e. base bfc04b659 = HEAD^1, covered by #725's record. Hosted validate on the PR (base e929137a8) failed: "paper:square-packing-methods-survey: candidate public inputs need a fresh owning successor or reviewed no-public-change decision" (fixed in 58c1db9af). After the first commit, HEAD != origin/main and the local run reproduces CI's verdict.

Fix: treat a tree with uncommitted or untracked changes (git status --porcelain non-empty, ignoring what changed_paths ignores) as not on main, so it compares with --baseline-ref origin/main; or decide on_main from the checked-out branch (refs/heads/main) or GITHUB_REF in CI. Add a test: a dirty tree at origin/main must use the PR baseline. The same `on_main` also chooses `announcement_base` for render_changelog --check, which has the same exposure.
