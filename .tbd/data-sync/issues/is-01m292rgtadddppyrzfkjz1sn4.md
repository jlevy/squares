---
type: is
id: is-01m292rgtadddppyrzfkjz1sn4
title: Remove remaining embedded workbench JavaScript and HTML
kind: task
status: open
priority: 1
version: 10
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-2
dependencies:
  - type: blocks
    target: is-01m29bhrhcs1zrcbfbhgwbb86n
  - type: blocks
    target: is-01m2chvkkmv158bkmqg9444jn8
parent_id: is-01m28p7h39vcykq99dgjmvwv98
child_order_hints:
  - is-01m298ns08hd103tjq6et26685
created_at: 2026-09-11T20:32:49.481Z
updated_at: 2026-09-13T05:43:46.556Z
---
Phase 2: preserve the ordinary source extraction already landed; finish remaining executable JS/HTML literals including bench_annealing TRIAL_JS/GUARD_JS and the build-time KaTeX program. New checked modules/probes/templates live in packages/workbench from their first commit. Use shared runtime APIs for simulation/repair and retain a separate finite/count/wall/pair verifier only where it provides independent assurance. Acceptance: no live executable JS/HTML is hidden from the applicable type/lint program; behavior and diagnostic assertions are retained without source-string-only gates. Probe naming/duplicates are inventoried now and removed under think-cqfc.

## Notes

Both halves landed and are re-verified by the coordinator.

D1 (74dc3d95): template.html 5,704 -> 275 lines; assets/workbench.css 395, assets/workbench.js 5,079; rebuilt with the banner it is sha256 abb090b1, byte-identical to the published page; node --check parses the script; RENDER_INPUTS and both Pages filter blocks now name the assets.

D2 (e52b50a6, 612943aa): 605 page.evaluate sites across five checkers now load JavaScript from 180 files. 108 of them had Python values formatted in, and 17 more passed a positional array the two sides had to agree the order of. check_probes.py reports all 180 parsing, functions, named and answered. Evidence: check_workbench byte-identical output and exit 0; check_legend the same; check_revision7 identical but its measured-duration line; test_candidate byte-identical and exit 1, as before (think-tn0j); check_revision6 has no end-to-end comparison because it cannot finish (think-i15w), so 17 of its 19 sites were compared old-JS against new-probe on the page instead.

Left as its own chore: five byte-identical probe bodies across directories and two naming conventions (think-x406).

Open decision for the owner: what lints assets/workbench.js. Recommendation is a pinned Biome, check-only.
