---
type: is
id: is-01m713xzyykpqv9j0nh1frrsbx
title: "Run the exact L-step and monotonicity scan at each adoption, so a consequence like #938's 199 is found by the record (devtools.l_step_scan)"
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-09T21:37:51.069Z
updated_at: 2026-11-09T21:37:57.977Z
---
#938 (think-1goz) showed a gap: when #937 adopted T-282 at 172 on 9 November, the L step from the new house improved 199 by 2.88e-3, and nothing in the record noticed. X049's family census, which #937 derived again, listed 199 under `bound_violations` (margin -0.002882320307 from 172), but no gate or sweep reads that list, and its 1e-9 tolerance hides sub-print consequences. The 31 October senior review of #852 had scanned L steps into and out of its re-housed counts by hand; no step of the adoption runbook asks for it.

Lane L76 wrote `devtools.l_step_scan` (OR-1), which decides the L step and monotonicity exactly from every case's verified ceiling, with `--with N=FRACTION` to stand an adopted side in. On main 200f2ebc1 it lists 199 from 172 as the only step that crosses its count's 12-place print, and ten padding-sized steps inside the print (4.8e-33 to 1.76e-19 at 101, 125, 170, 174, 198, 201, 257, 262, 292, 298), which are think-ruu2's RV-3 / RV-4 class. It finds no monotonicity inversion. Receipts: packing/resources/web/ozden-s199-upper-bound-2026-11-09/measure/l-step-scan*.json.

Decide, with the owner where it is a policy question:
- whether an adoption (adopt_houses, or the runbook's "Adopt a House, Then Regularize It") runs the scan with each new house standing in, and lists any consequence that crosses a print for registration;
- whether a check (records tier, or the intake sweep) fails on such a consequence that no open bead owns, as the census's bound_violations should have shown for 199;
- what RV-3 and RV-4 (think-ruu2) say about the ten sub-print consequences; the scan reports them and decides nothing.

Nothing is gated today; the scan is a measurement tool with a test of its logic.
