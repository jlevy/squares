---
type: is
id: is-01m4cb6azdjvj3eyf0ezg13kda
title: "PR #427 A5 — Medium: the generated open-frontier table retains the previous reports."
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4cb68shtz5h0braprdqj1qb
hold: null
hold_until: null
created_at: 2026-10-07T23:29:17.804Z
updated_at: 2026-10-08T00:20:40.437Z
started_at: 2026-10-08T00:20:33.521Z
closed_at: 2026-10-08T00:20:40.437Z
close_reason: Source fixes9ff422a/6c615115 at f1d7 are independently reviewed E/F/G/H with0newfindings and hosted final-head CI30SUCCESS26documentedSKIP. Focused379+190+3+11owner checks passed; selected broad assertions completed with original capability failure retained and unchanged supported profiler/heavy completions. Actual broad allowance1800 is unchanged. These source findings are fixed; parent422 intake/confirmation/deployment remain open until atomic stack merge and publication.
resolution: null
duplicate_of: null
---
Review https://github.com/jlevy/squares/pull/427#pullrequestreview-5449633758 head83748.

**A5 — Medium: the generated open-frontier table retains the previous reports.** The
full gate records `render_research_tables --check` refusing `frontier-open`. Its
retained block begins at
`docs/project/research/research-2026-08-22-packing-11-unit-squares.md:914`, while
`packing/devtools/render_research_tables.py:511` derives it from current cases.
The public research table is therefore outside the import’s otherwise refreshed record
set.

**Fix:** regenerate the owning research-table block after the case and assessment
repairs, retain the resulting table, and run its check mode.
Include this change in final scope and resource accounting.
