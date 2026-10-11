---
type: is
id: is-01m3w4hp3crpxzth3ny5dy9ch1
title: "Homepage: 'Other Square Packing Projects' sorted by significance of the results we cite from each"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:25:18.698Z
updated_at: 2026-10-01T19:39:34.040Z
closed_at: 2026-10-01T19:39:34.038Z
close_reason: "62e0a54b7, merged into jlevy/squares#276: projects ordered by (S5, S4, S3, S2, S1) counts of the results we cite, ties by newest result then name; each card ends with a tally whose total and level counts link all-results.html?project=<slug>[&s=<level>]; nine projects have tallies, five have none."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: on the Other Square Packing Projects section, let's sort them by 'significance' which is first by number of S5 results we cite, then by number of S4 (if no S5), then by S3, etc. That is: order the projects by the tuple (count of S5 results, count of S4, count of S3, …) descending, counting the register results attributed to or citing each project; the order is computed from the register at render time, with a stable tie-break (most recent result, then name); the card can show the counts.

## Notes

Done on claude/site-polish-4-home, commit 62e0a54b7: cards ordered by (S5, S4, S3, S2, S1) counts of results attributed to each project, then newest result, then repository name; computed from results.yaml via source-coverage keys (ranked_projects). Tally at each card's foot, 'N results (a at S5, b at S4)', total linked to all-results.html?project=<slug>, counts to &s=<level>; preset-only Project and At significance controls in the filter bar.
