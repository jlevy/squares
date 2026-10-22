---
type: is
id: is-01m5h50qj4p0j18gmb3hp88pw8
title: Enforce significance-first resource sorting on every surface
kind: task
status: in_progress
priority: 2
version: 3
delegate: about_profiles_implementation
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-22T06:33:16.610Z
updated_at: 2026-10-22T06:56:57.352Z
started_at: 2026-10-22T06:33:23.739Z
---
Investigate homepage resource order regression. Use one shared sort by authored result counts at S5 then S4 then S3 etc with stable tie-breaks for homepage and profile resource cards; validate rendered output after upstream merge.

## Notes

Committed with think-jmuq, think-beyg, think-j7kn and think-gddk in b3646ac72 through normal hooks. Legacy catalogue pinning and profile inventory-order rendering caused the reported sort regression. All resource kinds and profile subsets now share primary-result counts S5→S1, newest date, name and URL; unknown personal sites get a full zero vector.

Directory now orders Name/Records/Results/Credits/Years active/Resources/Accounts. Supported Records summary intersects the union of profiled primary-authored IDs with the current-record index. Table-only muted significance breakdowns start below dark totals. All columns reuse Results table.js keyboard/aria/numeric sorting with explicit missing-last behavior; no-JS links remain native. Historical Couzo/Joost resource copy now names T-225 replacement house views.

Focused validation:8passed40.60s; native-directory/browser and3Results-asset regressions5passed58.89s; shared sorter Node26passed95.7ms. Ruff/format6files, Biome5files, production overview tsc and diff check clean. Independent Astra final review has no actionable findings. Source frozen; no push by worker.

Complete normal build of b3646ac72 running5793 into external site-final-b3646ac72; log build-final-b3646ac72.log. Final count check:75people/228registered/217primaryResults/714Credits/112authoredRecords versus114globalRecords. Keep all five presentation beads open until coordinator combined validation and final output acceptance.
