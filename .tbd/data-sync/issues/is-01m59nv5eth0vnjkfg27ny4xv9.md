---
type: is
id: is-01m59nv5eth0vnjkfg27ny4xv9
title: "PR #665 M3: cover n132 differing-lane exact margin baseline"
kind: bug
status: closed
priority: 2
version: 4
delegate: codex-665-adoption-reconcile
labels: []
dependencies: []
parent_id: is-01m59jbf3zmjznc12k8g2b5cwk
hold: null
hold_until: null
created_at: 2026-10-19T08:53:24.569Z
updated_at: 2026-10-19T09:24:32.390Z
started_at: 2026-10-19T08:53:36.196Z
closed_at: 2026-10-19T09:24:32.389Z
close_reason: Fixed at 708a372dcead45623cbda47a3a1e96ddddd7771a; authoritative retained-prior writer and exact-margin/source-custody checks confirm repair. M1 cap tracked separately in think-2921.
resolution: null
duplicate_of: null
---
Astra local review .codex/intake-resume-20261019/665-prospective-final-review.md M3, medium: retain all n29 assertions and extend exact prior-baseline, margin rounding and provenance coverage to legitimate differing-display lanes at n132. Equal-display assertions apply only to numeric agreement; do not change source metadata.

## Notes

Fixed in34903e and708a372d: exact margin fixture independently pins29/132/308retained prior rationals/displays and keeps all positive-margin/rounding/provenance assertions. Serializer-normalized expectednotes prove metadata/bodywords unchanged, stale mutation touchescurrent ownedspans only(no raw308history), strict finalbyte equality retained. Final focused margin+2retention tests3passed15.03s; complete valid-input functional set otherwise114passed with knowncap omitted; no source/math/testweakening.
