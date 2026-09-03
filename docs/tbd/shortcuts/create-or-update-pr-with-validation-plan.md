---
title: Create or Update PR with Validation Plan
description: Create or update a pull request with a detailed test/validation plan
category: git
author: Joshua Levy (github.com/jlevy) with LLM assistance
---
We track work as beads using tbd.
Run `tbd prime` for more on using tbd and current status.

Instructions:

Create a to-do list with the following items then perform all of them:

1. **GitHub CLI setup:**
   - Verify: `gh auth status` (if issues, run `tbd shortcut setup-github-cli`)
   - Get repo and branch:
     ```
     BRANCH=$(git rev-parse --abbrev-ref HEAD)
     REPO=$(git remote get-url origin | sed -E 's#.*/git/##; s#.*github.com[:/]##; s#\.git$##')
     ```
   - Use `--repo $REPO` on all gh commands (required for Claude Code Cloud)

2. Check branch state: if this branch has uncommitted work, commit it first via
   `tbd shortcut code-review-and-commit` (leave files that look like another agent’s
   in-progress work); if the branch is behind its base with likely conflicts, run
   `tbd shortcut merge-upstream` first.

3. Check if a PR already exists for this branch:
   - Run: `gh pr view $BRANCH --repo $REPO --json number,url 2>/dev/null`
   - If it returns JSON, a PR exists (you’ll update it).
     If it errors, you’ll create one.

4. Review all commits on this branch since it diverged from main:
   - Run `git log main..HEAD --oneline` to see commits
   - Run `git diff main...HEAD` to see all changes
   - Review any related specs in docs/project/specs/active/

5. Write a PR title and description.
   If `.github/PULL_REQUEST_TEMPLATE.md` exists, use its section order and retain every
   applicable section. For a terminal research agenda, use the repository close command
   to generate the cost-first description from the checked agenda closeout.

   Use conventional commit prefixes: `feat`, `fix`, `docs`, `style`, `refactor`, `test`,
   `chore`, `plan`, `research`, `ops`, `process`. Scope is optional—only add when it
   resolves an important ambiguity.
   (See `tbd guidelines commit-conventions` for details.)

   ## What this branch cost

   Use the exact generated measurements.
   Keep overlapping harness intervals separate.

   ## Results and Dispositions

   State what was established at the smallest honest scope.
   If nothing was established, distinguish a completed bounded-negative search from a
   time-limited partial attempt, correct guard refusal, technical failure, unopened
   route, or inconclusive evidence.
   Give every row one action: continue, fix-and-rerun, retire-success, retire-negative,
   or defer-dependency.
   Name the follow-up bead where work remains.

   ## Changes by Purpose

   Group code, data, record, and documentation changes by the result they produce and
   name the principal files or interfaces.
   A commit or agenda chronology is supporting detail, not the summary.

   ## Validation

   Detailed validation checklist:
   - [ ] Unit tests pass (run the project’s test command)
   - [ ] Build succeeds (run the project’s build command)
   - [ ] Manual testing steps (list specific scenarios to test)
   - [ ] Edge cases considered (list any)
   - [ ] Hosted checks pass on the exact pushed revision

   ## Documentation and Replanning

   State which reader-facing documents were updated or checked current.
   For a post-agenda PR, include the reprioritized candidate set, any operator revision,
   and exactly one selected next entry point.

   ## Limits

   State what the branch does not establish, what remains open, and what evidence would
   justify reopening retired-negative work.

6. Create or update the PR:
   - If creating:
     `gh pr create --repo $REPO --head $BRANCH --base main --title "..." --body "..."`
   - If updating: `gh pr edit $BRANCH --repo $REPO --title "..." --body "..."`

7. Report the PR URL to the user, summarize the validation plan, and inform them you are
   now waiting for CI.

8. **Wait for CI to pass (CRITICAL):**
   - Run: `gh pr checks $BRANCH --repo $REPO --watch 2>&1`
   - **IMPORTANT**: The `--watch` flag blocks until ALL checks complete.
     Do NOT see “passing” in early output and move on—wait for the **final summary**
     showing all checks passed.
   - If CI fails: analyze the failure, fix the issue, commit and push the fix, then
     restart from this step.
   - Only proceed when you see all checks have passed in the final summary.

9. Confirm to the user that CI has passed and the PR is ready for review.
   The next lifecycle stages have their own shortcuts (see
   `tbd shortcut pr-review-workflows`): `tbd shortcut review-github-pr` reviews and
   publishes a review of the PR, and `tbd shortcut address-pr-review` addresses a review
   the PR receives.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
