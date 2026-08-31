---
type: is
id: is-01m18bjzka1yh1wrp2t58x81vf
title: Retain per-sample keys for exp-015 so the n=4 labelled control can score a relation
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-08-30T03:32:08.938Z
updated_at: 2026-08-30T03:32:08.938Z
---
X-005 scored four candidate endpoint-identity relations against the four proved component counts in exp-014 and exp-015. Three of the four scored 'undecidable' on the n=4 controls, because exp-015's retained JSON records the spaces and their component counts but no per-sample geometric keys or contact certificates -- exp-014 records four samples, exp-015 records none.

That matters because n=4 labelled is the control that most directly tests the relation the atlas uses today: 24 isolated labelled grids, so a correct labelled relation must report 24. It is currently the one control 'geometric + contact' cannot be scored against.

The fix is to emit per-sample keys for exp-015's 24 labelled states in the same shape exp-014 uses (geometric_key, contact_certificate, and the contact/wall detail), then extend devtools/check_identity_relation.py, whose Control dataclass already carries a samples field that is empty for n=4.

Do not change any proved count while doing this; exp-015's determination and acceptance rule are terminal. This adds retained detail to an existing result rather than re-running it.
