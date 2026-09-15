---
type: is
id: is-01m2hct1sp4w0dgycetzdkj1tr
title: "PR #125 review D75: engine arm flags and one sweep path unvalidated"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb401yy3ph99cfn5mhpcv4
created_at: 2026-09-15T02:02:20.853Z
updated_at: 2026-09-15T02:13:47.306Z
closed_at: 2026-09-15T02:13:47.305Z
close_reason: "Fixed in d484ab55 (engine: Params::check_arms refuses mislabelled arm flags at parse, exit 2) and 39bb08bb (run_arm_sweep prints the summary path with shown(), no relative_to raise)."
resolution: null
duplicate_of: null
---
Review source: PR #125 review F38 (Low); triage row D75.

Engine flags and one sweep path are unvalidated: packing/sqsearch/src/search.rs :151 requires both mu0 > 0 and mu1 > 0, so --mu0 X alone silently runs the control under a pressure label; --mu0 inf --mu1 inf freezes the chain and a NaN --p-perturb disables the arm (main.rs :105-111). packing/devtools/run_arm_sweep.py :438 relative_to(REPO) raises after writing summary.json when --out is outside the checkout, so a good sweep exits 1.
Related: think-gdt9.
