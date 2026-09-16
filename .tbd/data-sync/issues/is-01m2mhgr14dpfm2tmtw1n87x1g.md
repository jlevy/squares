---
type: is
id: is-01m2mhgr14dpfm2tmtw1n87x1g
title: "PR #181: replace brittle host self-test source mutation with file-backed probes"
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T07:22:22.115Z
updated_at: 2026-09-16T07:27:09.485Z
closed_at: 2026-09-16T07:27:09.484Z
close_reason: Fixed and locally validated at 990ac878; exact hosted CI will be required on the pushed head before merge.
resolution: null
duplicate_of: null
---
Exact hosted head f0a2c7b3 failed Pages geometry run 35067664887 job 104701921471: prepare_explainer_math --host-check --self-test could not construct its negative controls after the explainer JavaScript moved into formatted files. The self-test searches for the old unbraced else-delete source spelling; Biome-formatted page.js now uses a braced else. Replace source-text mutation with explicit file-backed runtime fault probes under the JS floor, retain both print-heat and native-fallback rejection controls, add focused regression coverage, re-run the hosted exact-head visual lane, and merge only after it is green.

## Notes

Fixed in local PR #181 commit 990ac878. Root cause: after certificate/page JavaScript extraction, Biome formatted the fallback branch with braces, but the hosted host-check self-test still searched generated HTML for the old unbraced spelling and refused to construct its controls. The fix replaces both source-text mutations with file-backed JavaScript fault probes: one suppresses heat draws for print-visible certificates retaining hidden, and one falsely retains the rendered-math marker. Evidence: exact generated page host-check+self-test exits 0 with no findings; host_regressions reports print_rejected=true and native_fallback_rejected=true; 18 focused pytest cases pass; check_probes sees 389 probes; no-embedded-JS sees 910 Python files and zero sites; Ruff and BasedPyright are clean; full browser floor passes with 147 Node tests.
