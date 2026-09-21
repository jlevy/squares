---
type: is
id: is-01m32v0a6jh2jjnbgy48s0fvp1
title: A check that adopts the tracked tree must carry its precedent's fallback, or give the caller an index
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m32dvmtc77znp14556p7c5w2
created_at: 2026-09-21T20:37:31.461Z
updated_at: 2026-09-21T21:01:04.416Z
---
Main went red at c2cc1cf6 on the `validate` job (hosted run 35645657481). One of 167
negative controls did not fire: `README - retired workflow identifier survives a
migration` got `README.md: cannot ask git which files this repository tracks, so the
directory is unknown` where it rehearses drift.

What happened, and it is worth recording as a shape rather than as one red step.
6bc9a99d moved `check_readme`'s three private walks to `repo_scope.tracked_files`, which
was right: the walk wandered into `.claude/worktrees/` and read the banned identifier
out of another agent's sources. It cited `check_class_record_claims` as precedent and
then dropped the one part of that precedent that was load-bearing -- the bounded walk
the sweep keeps for where there is no index -- and wrote the reason into the code:

  "Unlike the class-record sweep, this check cannot fall back to a walk with a stated
  bound: ... there is no caller for whom 'no git here' is an ordinary case."

There was such a caller, and the precedent's own docstring named it: "a `tmp_path`
fixture, a negative-control worker's source snapshot, which carries no `.git`". The
negative-control harness runs every check in a throwaway source snapshot, and the
snapshot carried no index. So the claim in the comment was checkable against the file
it cited, and it was false.

The repair (PR to follow) is the third option rather than either of the two the comment
argued between: `run_negative_controls.clone_tree` now makes each worker tree a git
checkout of itself, so the caller that made the premise false has an index like every
other one. That keeps 6bc9a99d's gain and closes a second, quieter hole -- with no index,
the class-record control was rehearsing that sweep's fallback walk and not the
tracked-tree code the gate runs.

Two things to carry forward from it:

- Adopting `tracked_files` in a further check is adopting a contract with two answers.
  `None` means "no index here", and a check that turns it into a failure is choosing to
  be unrunnable wherever the repository is not a checkout. That is a decision to state,
  not a default.
- A premise about "no caller does X" belongs in a test, not only in a comment. Nothing
  failed when this one stopped being true; the control did, a day later, in CI.

Recorded from the repair session. The premise itself is corrected in place at
`packing/devtools/check_readme.py`'s `NO_INDEX`.

## Notes

Scope for the follow-up audit, measured on this tree: `repo_scope.tracked_files` has
three consumers -- `devtools/check_readme.py`, `devtools/check_class_record_claims.py`
and `devtools/check_archive_annotations.py`. Only `check_readme` has a registered
negative control, which is why the refusal is what CI saw and the fallback half was
latent. The audit is whether each of the three still makes the right choice on `None`,
and whether a fourth adopter can be made to state that choice without reading
`run_negative_controls`.

Repaired on `claude/fix-readme-no-index` (PR 217): the worker snapshot is now a git
checkout of itself, so all three answer from an index inside a control. The bead stays
open for the audit and for the durable form of the rule.
