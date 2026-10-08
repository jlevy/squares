---
type: is
id: is-01m4ceevz3k7x10sgcbhfegd1v
title: Publish the complete exact side register as a generated paper
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex-polynomial-01a118e4
labels: []
dependencies:
  - type: blocks
    target: is-01m4cf1w4xst7bfypgq1at86z1
parent_id: is-01m4cee7q2jdj5scgd5wa72y24
hold: null
hold_until: null
created_at: 2026-10-08T00:26:23.074Z
updated_at: 2026-10-08T03:34:05.907Z
started_at: 2026-10-08T00:26:33.823Z
closed_at: 2026-10-08T03:34:05.905Z
close_reason: "Delivered in PR435 (https://github.com/jlevy/squares/pull/435): independent exact-side-values HTML/Markdown/PDF renderer, complete current and historical coefficients, source locators and certificate/route disclosures. Final local PDF has366 pages and2345506 bytes; visual checks cover summary, landscape tables, high-degree continuations and final pages. Renderer/structure tests and corrected publication integration pass; clean hosted Pages generation/check/assembly at e17685ef36cad388d937a32d5082d5fddc2cb18d succeeded (run37720184321), paper job95s within150s ceiling. No geometry or optimality status advanced; deployment follows a future authorized merge."
resolution: null
duplicate_of: null
---
W7 continuation of think-vtc1: create devtools.render_exact_side_values, template and focused tests, render all recorded current and superseded polynomials in full, distinguish algebraic side identification from packing feasibility or optimality. Own only new renderer/template/tests. Coordinator owns site/workflow registration and shared records. Use existing publication layer; no dependency upgrades.
