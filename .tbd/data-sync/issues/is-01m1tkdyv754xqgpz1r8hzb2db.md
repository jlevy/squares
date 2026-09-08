---
type: is
id: is-01m1tkdyv754xqgpz1r8hzb2db
title: "Commit the review as a dated record: map it, fix the filename, settle its formatting"
kind: task
status: closed
priority: 1
version: 3
labels:
  - review-gpt6
dependencies: []
parent_id: is-01m1tkdspk8c3n71xsc2e2t4g7
created_at: 2026-09-06T05:35:32.711Z
updated_at: 2026-09-06T06:21:09.337Z
closed_at: 2026-09-06T06:21:09.337Z
close_reason: "Implemented in 41fb401a on claude/pdf-paper-small-fixes (PR #92); reviewed by the coordinator; CI green"
resolution: null
duplicate_of: null
---
The review sits untracked at docs/project/reviews/review-2026-09-05-gpt6-pro-aversarial-review.md, so packing-validate's 'synopsis agrees with the artifacts' step fails (check_documentation: unmapped durable document). To do: (1) rename to fix 'aversarial' -> 'adversarial'; (2) add it to docs/project/document-map.yaml as role review, authority record, lifecycle retained, like the 2026-09-03 reviews; (3) decide formatting: it uses \( \) math delimiters and carries ChatGPT export artifacts ('([Jlevy][1])' citations, a '**Verdict**' lead); the two dated reviews with quoted sources are excluded in .flowmarkignore because the hook retypes quotations, so measure what flowmark would change on a copy and either exclude it or accept the reflow; (4) link it from the epic and from T-018's record. Acceptance: packing-validate --records passes with the file tracked.
