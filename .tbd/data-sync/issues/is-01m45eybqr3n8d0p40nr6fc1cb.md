---
type: is
id: is-01m45eybqr3n8d0p40nr6fc1cb
title: "PR #347 B3 (Medium): disclose the OR-16 paragraph in operating-rules.md and reconcile its Git-ancestry clause with OR-18"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m45ex3dssa31jvkkz9bzpc6e
created_at: 2026-10-05T07:20:09.719Z
updated_at: 2026-10-05T07:20:09.719Z
---
Review B finding B3 on jlevy/squares#347 (https://github.com/jlevy/squares/pull/347#pullrequestreview-5411026138), at head 9d2f05582. operating-rules.md:703-720 adds a paragraph to OR-16 ('Internal bookkeeping never costs a re-run...') that the body does not mention. The clause at :714 ('...and Git ancestry qualify') reads against OR-18 (no program may need to resolve a cited revision). render_operating_rules --check passes only because the AGENTS.md summary line is unchanged. Fix: name it in the body as the owner's 2026-10-03 rule carried from #307, and either align the Git-ancestry clause with OR-18 or move the paragraph to its own small PR so the owner sees a rule change as a rule change.
