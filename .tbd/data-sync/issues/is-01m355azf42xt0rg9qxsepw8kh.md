---
type: is
id: is-01m355azf42xt0rg9qxsepw8kh
title: Generalize native n11 parent-core verification and add C4 confirmation
kind: task
status: closed
priority: 1
version: 9
delegate: codex@spud10
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-09-22T18:16:35.552Z
updated_at: 2026-09-23T03:04:59.517Z
started_at: 2026-09-22T22:47:59.655Z
closed_at: 2026-09-23T03:04:59.516Z
close_reason: All 12028 native parent-core rows certify on clean c183cc9ab; exact premises, full transfer theorem and independent review support C4 for Kleddamag’s unchanged strict 31/8 bound. Complete proof, reconciliation, adverse controls and scoped integration evidence are retained in Session 153 and PR 223.
resolution: null
duplicate_of: null
---
Session 152 reviewed Kleddamag n11 v1.0.2 at 6a733f339395c3514f2ab63d8c4aa64cf63c0b5a. Preserve arbitrary k-of-m charges, exact orbit multiplicities and floor(m/k) budgets. Preserve the 12028 adaptive parent-angle intervals and parent-admissible centre domains; core width and centre radius must be independent inputs. First pilot rows 0, 11962 and 12027 with an interval method distinct from the exact event sweep. Measure termination and batching before the complete campaign: 5284 active sites exceed the current 4096-site guard, and 13580 feature slots exceed 8192. Do not silently raise guards. Complete independent coverage plus the mapped proof audit is the acceptance condition. Evidence: docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md and the integration review.

## Notes

Session 153 completes the native adaptive parent-core verifier without changing the
mathematical claim or Kleddamag attribution. The exact importer preserves arbitrary
k-of-m charges, D4 token multiplicities, floor(m/k) budgets, the adaptive angle partition,
strict core containment and the admissible parent-centre domain. Directed-rounding box
coverage uses exact Gamma-aware pruning and bounded site/member tables, batches and
workers.

The complete run on clean c183cc9abe93eedcb268a5390cdd1cdc6e7bbb39 certifies all 12,028
rows in 6,197.381 seconds with two workers and batch 2048: 136,081,500 boxes, no stalls,
no exhausted budgets and no refutations. The minimum charge is exactly 999,962,528
units; the exact 11 Gamma minus budget margin is 13483/125000000. The coordinator
independently reviewed all row identities, exact premises and the complete transfer
theorem. Together with the original exact source event-cell replay, the method-distinct
native coverage supports C4 for Kleddamag's strict s(11)>31/8; source replay alone
remains C3, and no C5, stronger bound or new T-ID is claimed.

The immutable receipt, row journal, fast reconciliation and full hosted-checkpoint
metadata are retained beside Session 153. The reconciliation recomputes exact premises
and checks the receipt/journal and 19 frozen Git inputs; it does not replay interval
coverage or authenticate coordinated invented data. Its positive/adverse tests pass.
The five-job full hosted checkpoint passed on c183cc9ab:
https://github.com/jlevy/squares/actions/runs/35799179943

Final green PR 222 head be736b0ef05ac2f256691bc3ded21873ad1f2ab1 is integrated without a
numerical proof-input change. The complete proof is reused at that unchanged scope;
final-head record, export and integration checks are recorded separately. The narrow
mutation snapshot repair keeps both proof artifacts and the 160 MiB cap, omitting only
a frozen historical transition-statistics file from temporary workers. Clean worker
baselines, copy-back and all 25 focused negative-control tests pass.

Durable evidence: docs/project/reviews/review-2026-09-22-native-n11-parent-core.md;
packing/campaign/agent-sessions/session-153-native-n11-parent-core.md;
packing/frontier/evidence.yaml entry E-n011-kleddamag-3875-native-parent-core.
Stacked PR: https://github.com/jlevy/squares/pull/223 . The separately requested W3
review owns the next research ordering; this completed slice creates no speculative
successor or result identifier.
