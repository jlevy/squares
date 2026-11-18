---
type: is
id: is-01m7p3zhkpy1ypz3jxtppx519c
title: "Import #1021, #1022: Joost de Winter's s(268) <= 16.870013850405 and s(270) <= 16.927314216352 at JoostdeWinter/square-packing a1ba501, below #1009's (T-314..T-326) at those counts; report order after #1009; merges after the import-1009 PR"
kind: task
status: in_progress
priority: 1
version: 3
delegate: w6-dewinter-1118
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-18T01:22:44.981Z
updated_at: 2026-11-18T02:27:09.499Z
started_at: 2026-11-18T01:23:11.221Z
---

## Notes

2026-11-18T02:35Z w6-dewinter-1118: claimed. Triage, read-only: #1021 (22:49:55Z) and #1022 (22:50:19Z) name a1ba501 (22:48:48Z, pushed 22:48:50Z with 838c5ea), n268/ and n270/ centre-direction JSON with Witness/v2 twins, MIT; checkers byte-identical to n90's. 268: exact side ceil16 16.8700138504044644, ceil12 16.870013850405 = the issue's print, 2.016e-3 below the house 16.8720298490844502 (T-289), and about 1.85e-3 below #1009's 268 (T-320 on #1023, 16.871868135...). 270: ceil16 16.9273142163517014, ceil12 16.927314216352 = print, 8.344e-4 below the house 16.9281486033428544 (T-283) and below #1009's re-solve there (T-321 on #1023) and #1012's quoted Kaggle sides (no packing). Lineage per issues: 268 from nine diagonal slices of Ostashev's 129 (via Prabhat), PingYou Ltd's 153 and 302 (via Prabhat, Malyshev, Couzo); 270 from Panoras's compilation 270. Stages 2-3 on claude/intake-2026-11-18-import-1021 after #1023 merges, ledger walking #1009 then #1012 then #1021/#1022; check the one-prior-state-per-day rule if both re-house 268/270 on 18 Nov.
