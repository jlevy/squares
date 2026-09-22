---
type: is
id: is-01m351egs7mgrzkrmnesq26jwp
title: "Certification block 2: extend the Goebel centred and off-centre families to nine sizes above 100"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-22-upper-bound-certification-blocks.md
labels: []
dependencies: []
parent_id: is-01m350mb40w609b2j8aksv4gq6
created_at: 2026-09-22T17:08:37.286Z
updated_at: 2026-09-22T17:08:37.286Z
---
Validation block per the spec, group A, rule-independent. W6 slice with a W7 build phase; one 30-minute slice. Instruments: packing/cases/gobel_family (build(a, b) general; verifier SUBJECTS = ((4, 5), (4, 7)) at verify_exact.py:43) and packing/cases/gobel_offcentre (build general; SUBJECTS covers (2, 3), (4, 6)). Batch, measured with each module's count rule on 2026-09-22 and matched to the records' reported exact_form: gobel_family (5,7) n = 109 at 6 + (7/2)sqrt(2); (5,8) n = 124 at 6 + 4 sqrt(2); (6,8) n = 148 at 7 + 4 sqrt(2); (7,11) n = 233 at 8 + (11/2)sqrt(2); (8,11) n = 265 at 9 + (11/2)sqrt(2); gobel_offcentre (7,10) n = 227 at (17/2) + 5 sqrt(2); and by deletion of one named square n = 147 from 148, 232 from 233, 264 from 265, each decided by the verifier and declared in CERTIFIES. Criterion: exact sign over Q(sqrt 2) on every pair and containment at the exact side; the off-centre column control refuses one more square at (7,10). Measure replay wall first (n = 265 is 34,980 pairs). Record as in block 1 (think-w47c): evidence entries, nine case records with only the upper-bound mathematics blocker removed, CERTIFIES, validate.py, TRAILING_BY_CORPUS (-9), regenerated STATUS.md, INVENTORY.md, composite-figure.json and citation data; packing-validate --records then --push; W2 non-author review before commit. Stop: certified and green, refusals recorded, or a checker blocker. Independent of block 1 in cases/ files; shares evidence.yaml, validate.py and the tripwire with it, so the coordinator integrates both.
