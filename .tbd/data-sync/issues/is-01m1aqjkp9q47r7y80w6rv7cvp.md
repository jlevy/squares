---
type: is
id: is-01m1aqjkp9q47r7y80w6rv7cvp
title: Re-run price_exact_construction calibration inside declared digits (D-402 follow-up)
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-08-31T01:40:08.521Z
updated_at: 2026-08-31T01:40:08.521Z
---
devtools/price_exact_construction.py reports reproduced:false for both calibration sizes by reading counts at the finest deciding floor (1e-120, the padding window its own docstring warns about) with an exact-zero sign, where the retained n=29 extraction used a tolerance sign (cases/kingbird29/verify_svg.sign, ZERO_TOLERANCE=1e-80). Measured inside declared digits with the tolerance sign, extraction reproduces both known structures (n=11: 14/20 stable 1e-14..1e-30; n=29: 52/37 stable 1e-14..1e-98). D-402's core finding stands (floor-vs-declared-digits guard still missing); the derived claim that decimals cannot yield structure needs this re-run. From session-049's machinery inventory (X-009).
