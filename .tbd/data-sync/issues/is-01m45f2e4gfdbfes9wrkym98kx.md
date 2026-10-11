---
type: is
id: is-01m45f2e4gfdbfes9wrkym98kx
title: "PR #355 B3 (Low): drop the stale 'copied from main revision 7e45c42a' sentence in n17-diagnostics.md"
kind: task
status: closed
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m45f2ak71t5b3h9evk65mwjt
hold: null
hold_until: null
created_at: 2026-10-05T07:22:23.248Z
updated_at: 2026-10-06T08:10:50.010Z
started_at: 2026-10-06T08:09:49.903Z
closed_at: 2026-10-06T08:10:50.010Z
close_reason: "Addressed: commit 1d02a11e2 (in origin/main eb43ffe9a) removes the 'copied from main revision 7e45c42a' sentence; packing/devtools/n17-diagnostics.md:34 now reads 'The formatter is main's own module, sqpack.retained_json.'"
resolution: null
duplicate_of: null
---
Review B finding B3 on jlevy/squares#355 (https://github.com/jlevy/squares/pull/355#pullrequestreview-5411026555), at head 018ee13c5. packing/devtools/n17-diagnostics.md:34-36 says the retained-JSON formatter and its tests are 'an exact compatibility prerequisite copied from main revision 7e45c42a...'. On this stack nothing is copied: sqpack.retained_json is main's own module, carried in #347. Fix: drop the sentence, or say it is main's module.
