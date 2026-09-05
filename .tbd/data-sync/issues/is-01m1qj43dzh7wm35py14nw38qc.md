---
type: is
id: is-01m1qj43dzh7wm35py14nw38qc
title: Two dated reviews drift under flowmark, one with a corrupted comparison; exclude or repair, never reformat
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T01:14:57.854Z
updated_at: 2026-09-05T01:14:57.854Z
---
make format-check reports two dated reviews as drifting on main and on this branch: docs/project/reviews/review-2026-09-03-bc152-h060-prior-art-survey.md and review-2026-09-03-bc158-h060-record-factual-review.md. Every sub-agent worktree saw the pre-commit hook rewrite them (32 lines of straight-to-curly quotes inside block quotes of external sources, and one genuine corruption: '>= 0' becomes '> = 0'), and reverted before committing. Dated reviews are immutable records and the repository never retypes quoted sources, so the fix is an evidence-based exclusion in .flowmarkignore (the corruption is the evidence, as the archive's math-span breakage was) or a repair of the source quoting that makes flowmark's output a no-op; not a reformat. Decide and land it so the hook stops fighting every commit.
