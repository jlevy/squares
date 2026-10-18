---
type: is
id: is-01m573m6xkdxqn6j7davjkmvnp
title: "PR671 review A1/A5: retain certificates without overwrite and replace manifests atomically"
kind: bug
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m572ssbx1x412zpvsw1sb6je
hold: null
hold_until: null
created_at: 2026-10-18T08:56:33.457Z
updated_at: 2026-10-18T10:02:58.561Z
started_at: 2026-10-18T09:42:48.172Z
---
Review https://github.com/jlevy/squares/pull/671#pullrequestreview-5562187918 at32d47d3214ec28f2a82b89689cd8bb8f63f98e02 reproduced silent overwrite/deletion of an existing plain candidate with exit0. Fix collision refusal before any write; manifest replacement must be atomic. Add fail-closed regression controls. No new expensive census is required. Preserve digest-only adapted source archive custody.

## Notes

2026-10-18 continuation: A1/A5 fixed and pushed on PR #671 at 1b2cf7cfe15c4eec90d447bf3977a683d96dec1d. Source commits be93e8ea3a2e41916ce226f741dfae9d2d9ff7a0 and 13fcf887f48dce4c128499504b22ac63c002cde5, both with normal hooks and coordinator source review. Full destination preflight refuses existing plain counterparts (matching or conflicting), nonregular/symlink manifests and symlink targets; private gzip staging keeps gzip -9n bytes; os.link publishes members without clobber; strif atomic manifest replacement preserves prior complete records. Initial controls reproduced 5 failures; final focused retention tests 33 passed in 6.67 s, broader acquisition/retention group 232 passed in 32.98 s. Scoped Ruff/format and configured BasedPyright pass. Unique receipts retained outside scratch at /Volumes/spud-ext1/agent-source/squares-671-retention-evidence-20261018/. Hosted CI pending; unrelated publication/page-size findings remain open. No source verifier archive fetched or opened.
