---
type: is
id: is-01m2b7na7psnnn1j62g1yjdtta
title: The page can tell a packing from an overlap, and resolve one into the other
kind: feature
status: open
priority: 1
version: 15
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-2
dependencies:
  - type: blocks
    target: is-01m2b7nakccj4tf1tgs4k86nar
  - type: blocks
    target: is-01m2chahf57z4w9tj5gehbs0td
  - type: blocks
    target: is-01m2ckzvnsawqg79z9ybspc3yt
  - type: blocks
    target: is-01m2chr65cx0jhfd1gsmx3r31y
  - type: blocks
    target: is-01m2gxkvbndg46r6pjy3352cb8
parent_id: is-01m28p7h39vcykq99dgjmvwv98
child_order_hints:
  - is-01m2dvhzr8f87mgtghjv28rn55
created_at: 2026-09-12T16:36:56.180Z
updated_at: 2026-09-15T03:55:23.615Z
---
Phase 2: expose one fail-closed count/finite/pair/wall validity contract and bounded Resolve operation shared by Pack and the headless harness. Preserve raw and repaired states, score the geometry actually displayed, report tolerance/work/termination, and validate the repaired output. Translation-only repair does not guarantee improvement, convergence or global feasibility. Resolve is an explicit action or phase, not work repeated on every paint. Acceptance: valid retained controls and invalid/nonfinite/count/wall/pair controls agree across clients; budget exhaustion is explicit; a repaired score never labels a raw frame. Historical speed and success observations are evidence to reconcile, not required outcomes.

## Notes

2026-09-12 review: preserve raw and repaired arrangements separately; compute finite pair AND wall checks with an explicit metric/tolerance, then validate repaired output. Repair is not a guarantee of best-side monotonicity or global validity. Do not compute resolution on every paint or imply the displayed raw frame has the repaired score. Introduce explicit Resolve action/phase, bounds on effort and refusal status, then same implementation for Pack/headless/Search.

2026-09-14, PR #160 review lane C (D07, #160 R2; D09, #160 R4): the one validity contract now exists. `PACKING_VALIDITY` in `packages/workbench/src/core/runtime-contracts.ts` (count, nonfinite, dimensions, pair and wall penetration at 1e-9, area-bound, magnitude within 2^16, unit size; first failing clause reported, tolerance recorded) is mirrored by `tools/workbench_tools/packing_contracts.py`, and `tests/fixtures/packing-validity.json` is read by both `node --test` and pytest (ec0a0604, 78c338be). `CATALOGUE_PRECISION` (4e-6) is the one declared exception, for stored catalogue frames only (`assessCataloguePrecisionFrame`; 147 of 324 frames need it, re-measured by `tests/test_catalogue_precision.py`). Pack, Resolve, Search and the benchmark probe consume it. Still open here: the page consumers (gap bar, growth readout, PackController labels), which are D11 on lane D-page.

2026-09-14, PR #160 review D68 (#160 R27), lane D-tools: #160 R27 found this bead's shared-rule premise contradicted by the code at 72629c03 (several validity definitions, #160 R2). That is reconciled on #160: the contract and parity fixture above landed at ec0a0604 and 78c338be, and the page consumers named as still open here now read it (c0d9db2b, lane D-page, D11). The annealing plan, the workbench plan and the architecture review's dated addendum cite these commits (75f99fb9). What stays open is this bead's acceptance evidence beyond #160, such as browser/headless parity at release.

2026-09-14, D07 follow-up, lane D-tools (8b7bf5e3): RECORD_REFERENCE_TOLERANCE (1e-7) in animation_render.py is not a validity rule. It decides whether an animation frame that names a retained record is that record, before the renderer draws the witness's exact geometry, so it stays outside packing_contracts. It is now declared with its precision argument (binary64 reading of the exact decimal witnesses moves a centre by at most 2.4e-15 over all 324; the page's catalogue precision is 5e-7 or more), and test_record_reference_tolerance.py pins both edges.
