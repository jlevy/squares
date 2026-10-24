---
type: is
id: is-01m5p95y6vn6swc12d683dmeqd
title: "Profiles: T-163's Records line prints its superseded finite counts, not the current family facet (render_contributors.py:216-232, PR #770 review A7)"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T06:22:13.723Z
updated_at: 2026-10-24T06:22:13.723Z
---
Review A7 on PR #770 (https://github.com/jlevy/squares/pull/770#issuecomment-6380669495), deferred: a template change, outside that intake pass's scope (the owner, 23 October 2026: site templates and visuals are the site agent's).

Since #770, T-163 is current only by its family facet, record_scope's `deficiency_upper_bounds: ... k >= 15`, assessed by cases/asymptotic/deficiency_family.py; its four finite bounds (n = 211, 241, 273, 307) trail their cases and are superseded. Kevin Fang's profile (contributors/people/kevin-fang, rendered at https://squaremath.org/profiles/kevin-fang.html#records) lists T-163 under "Current registered contributions in their recorded family and scope", and the line prints the register scope through `_cases_text` (packing/devtools/render_contributors.py:216-232 at the #770 branch): "n = 211, 241, 273, 307", none of which is current. Before #770 the same line sat under Review pending. Hosono's line for T-073 likewise prints its register scope, n = 83 to 105.

Do: print a family facet's scope on the Records line when the facet is what makes the result current (for T-163, "c*(k) <= k - 1 - F(k) for k >= 15, smallest at k = 15 to 68 and 70 to 75"), with a test on the rendered line; check the other profiles' Records lines for the same case. Site/template work: for the site agent, not an intake lane. No CPU.
