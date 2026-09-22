---
type: is
id: is-01m355azf42xt0rg9qxsepw8kh
title: Admit Kleddamag n11 parent-core certificate through an independent complete coverage method
kind: task
status: open
priority: 1
version: 4
labels: []
dependencies: []
created_at: 2026-09-22T18:16:35.552Z
updated_at: 2026-09-22T18:54:23.115Z
---
Session 152 reviewed Kleddamag n11 v1.0.2 at 6a733f339395c3514f2ab63d8c4aa64cf63c0b5a. Preserve arbitrary k-of-m charges, exact orbit multiplicities and floor(m/k) budgets. Preserve the 12028 adaptive parent-angle intervals and parent-admissible centre domains; core width and centre radius must be independent inputs. First pilot rows 0, 11962 and 12027 with an interval method distinct from the exact event sweep. Measure termination and batching before the complete campaign: 5284 active sites exceed the current 4096-site guard, and 13580 feature slots exceed 8192. Do not silently raise guards. Complete independent coverage plus the mapped proof audit is the acceptance condition. Evidence: docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md and the integration review.

## Notes

Astra follow-on calculation: using 2048 boxes per batch yields a 10821632-byte site mask, 27811840 gathered member bytes, and 11124736 bytes of int16 counts for this fixed certificate, within the existing 16/32/32 MiB envelopes. Parameterized batch sizing with product checks is preferable to raising site/slot limits globally. These are analytical array-size bounds, not measured peak memory or runtime. Pilot exact seams and parent-centre semantics before full admission.
