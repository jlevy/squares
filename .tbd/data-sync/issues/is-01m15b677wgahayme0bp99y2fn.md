---
type: is
id: is-01m15b677wgahayme0bp99y2fn
title: Move the tree with repren, renames only
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m15219m6eh8fww5pm9sc2sqd
created_at: 2026-08-28T23:27:27.482Z
updated_at: 2026-08-28T23:27:30.152Z
closed_at: 2026-08-28T23:27:30.151Z
close_reason: Landed in the reorg branch
resolution: null
duplicate_of: null
---
Hoist README, SYNOPSIS, TUTORIAL, conventions, development, defects.md and docs/ to the repository root; move everything else to packing/; delete explorations/.

Use `repren --renames` with a pattern file, not git mv, so the docs-tier rule and the packing/ rule are expressed once. Two dotfiles (.python-version, sqsearch/.gitignore) fall outside repren's default dot-path exclusion and need moving explicitly.

Commit renames only, so Git records them and git log --follow survives. The tree is knowingly broken at this commit.

Commit with --no-verify: the pre-commit hook formats the whole repository and .flowmarkignore still names the old resources path, so running it would reflow the 26 .raw.md ground-truth extractions.
