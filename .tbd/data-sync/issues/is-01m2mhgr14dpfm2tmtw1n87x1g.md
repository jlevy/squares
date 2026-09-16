---
type: is
id: is-01m2mhgr14dpfm2tmtw1n87x1g
title: "PR #181: replace brittle host self-test source mutation with file-backed probes"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T07:22:22.115Z
updated_at: 2026-09-16T07:22:22.115Z
---
Exact hosted head f0a2c7b3 failed Pages geometry run 35067664887 job 104701921471: prepare_explainer_math --host-check --self-test could not construct its negative controls after the explainer JavaScript moved into formatted files. The self-test searches for the old unbraced else-delete source spelling; Biome-formatted page.js now uses a braced else. Replace source-text mutation with explicit file-backed runtime fault probes under the JS floor, retain both print-heat and native-fallback rejection controls, add focused regression coverage, re-run the hosted exact-head visual lane, and merge only after it is green.
