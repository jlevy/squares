---
type: is
id: is-01m31gq9n9btr1s9ywpjq84xqb
title: Re-emit the n21 and n22-check one-spare inventory artifacts
kind: task
status: open
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:35.815Z
updated_at: 2026-10-06T08:48:52.262Z
---
PR 205 re-review, minor. one-spare-inventory-n21.json and one-spare-inventory-n22-check.json were not re-emitted after run()'s payload gained orientation_margins. Regenerating differs only by that new block - diffing every shared key of the n=21 record gives 'differing shared keys: []', so no count is wrong - but the n=32 artifact was regenerated and these were not.

## Notes

2026-10-06 bead review: think-t9du (think-nalh, filed later the same day from the same PR 204-209 review) was closed as a duplicate of this bead. Re-checked on origin/main eb43ffe9a: still unfixed.
