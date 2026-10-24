---
type: is
id: is-01m5nvephbmqvk0ace4vzerhg9
title: "Take over PR #736 (home page News box) on the owner's word: merge main, resolve without redesign, verify a strict improvement compatible with later design choices, review, merge"
kind: task
status: in_progress
priority: 2
version: 5
delegate: c-take-736-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5p11e8qrfgfcsfpsj05t55a
hold: null
hold_until: null
created_at: 2026-10-24T02:22:20.715Z
updated_at: 2026-10-24T03:59:57.719Z
started_at: 2026-10-24T02:22:34.759Z
---

## Notes

2026-10-24 coord-intake-1023: OWNER (in conversation, 24 October). Asked whether to take over #736 (the site agent's home page News box: reviewed twice, last pushed 06:42Z on 23 October, now 225 commits behind main and conflicting; earlier "No, leave #736 to the site agent"), the owner selected "Take it over (Recommended)", then added: "Review carefully and make sure it's a strict improvement that we can land. And that it's compatible with the other design choices we've made".

2026-10-24 c-take-736-1024: #736 brought to main 14b14f2d1 at head 17a264be0 (merges 3f4cc4f7f of da117ad0b, six conflicts resolved keeping main's change and the PR's intent; 95ac0de5e of 14b14f2d1, clean). Landing record: n=204 T-231 (2026-10-24) and mishapolk-issue732-2026-10-22 (2026-10-23) backfilled from history, audit 0 differ. Re-pinned DATA_REVISION to 3f4cc4f7; papers' no-change record re-measured twice, 69 files byte-identical. One design adaptation, 08510a595: #746's small-chooser rule (one size, 24px, centered capitals) failed hosted frontend on the compact filter's 0.85 scale; the scale is dropped and the lighter weight kept. Hosted CI at 17a264be0: 31 pass, 28 skipped, 0 fail (Packing validation 40059305228); MERGEABLE CLEAN. PR body updated with the compatibility table and the main-versus-branch comparison. Draft; not merged; ready for the independent review.
