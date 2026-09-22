---
type: is
id: is-01m355azf42xt0rg9qxsepw8kh
title: Generalize native n11 parent-core verification and add C4 confirmation
kind: task
status: in_progress
priority: 1
version: 6
delegate: codex@spud10
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-09-22T18:16:35.552Z
updated_at: 2026-09-22T22:47:59.666Z
started_at: 2026-09-22T22:47:59.655Z
---
Session 152 reviewed Kleddamag n11 v1.0.2 at 6a733f339395c3514f2ab63d8c4aa64cf63c0b5a. Preserve arbitrary k-of-m charges, exact orbit multiplicities and floor(m/k) budgets. Preserve the 12028 adaptive parent-angle intervals and parent-admissible centre domains; core width and centre radius must be independent inputs. First pilot rows 0, 11962 and 12027 with an interval method distinct from the exact event sweep. Measure termination and batching before the complete campaign: 5284 active sites exceed the current 4096-site guard, and 13580 feature slots exceed 8192. Do not silently raise guards. Complete independent coverage plus the mapped proof audit is the acceptance condition. Evidence: docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md and the integration review.

## Notes

The complete external Python and JavaScript replay and proof audit support the verified 31/8 bound now. This follow-up adds native generalization and method-distinct C4 confirmation; it is not an admission prerequisite. Astra array calculation: 2048 boxes yields 10821632 site-mask bytes, 27811840 gathered-member bytes and 11124736 int16-count bytes, within 16/32/32 MiB envelopes. These are analytical array bounds, not measured peak memory or runtime. Pilot seams and parent-centre semantics before a full independent run.
