---
type: is
id: is-01m5h7zahankya4n90qy81y3f1
title: Preserve organization-authored project result totals and filters
kind: bug
status: in_progress
priority: 1
version: 3
delegate: project_attribution_fix
labels: []
dependencies: []
parent_id: is-01m5h7me41y7pa91sts7g214vg
hold: null
hold_until: null
created_at: 2026-10-22T07:24:56.233Z
updated_at: 2026-10-22T07:55:05.378Z
started_at: 2026-10-22T07:27:07.142Z
---
Senior final review K1: project_primary_results requires resolved human profile IDs, dropping source-attributed organization results. BuddenPing/squares loses T-174/T-195 and square-packing-certificates loses nine source results. Restore exact project-source primary attribution without inventing person identities or promoting acknowledgments; preserve mixed-packet human role exclusions. Cover card counts, significance ranking and result filter membership with independent canonical regressions.

## Notes

Fixed and pushed9939b62a7282820b8e7c33d3d437df5e13a66818: explicit non-person/unresolved source-author spans retain11PingYou project Results with empty bylineIDs, personal Results/Credits unchanged. New regressions red4fail then focused52pass; Astra correctness confirms fix with115pass. Required pushgate27/27passed1041.16s:11803pass61skip1xfail plus14poolpass. Preview7333checks/696pages0badlinks confirms2+9corporatecounts andfiltermembership. Await finalhostedCI andformalKdisposition beforeclose.
