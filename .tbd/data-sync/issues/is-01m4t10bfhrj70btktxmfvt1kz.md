---
type: is
id: is-01m4t10bfhrj70btktxmfvt1kz
title: "Research report tables: split open and solved on the verified status, or label reported-only closures (n = 17, n = 96)"
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m4s74nyjg5a9eqhf80q4xcv8
created_at: 2026-10-13T07:00:38.001Z
updated_at: 2026-10-13T07:00:38.001Z
---
Deferred from PR #560 review B3 (https://github.com/jlevy/squares/pull/560#pullrequestreview-5499752686). packing/devtools/render_research_tables.py splits the generated tables of docs/project/research/research-2026-08-22-packing-11-unit-squares.md on reported_status (render_research_tables.py:171, :198), so a case reported proved but open in the verified lane leaves the table the prose at :886 calls 'every open n <= 100' and appears under 'The solved cases, for contrast' (:1158) with the formal-lane label 'proof audit pending' (render_research_tables.py:204). n = 96 has shown this way since T-081 (2026-10-03); T-153 adds n = 17. Nothing false is claimed (the columns are reported-lane and the formal lane says pending), but 'proof audit pending' understates a source-declared candidate at V0, and devtools.gap_ranking moved to the verified status for the same reason (D-520). Fix (pick one): reword the two prose lines to name the reported lane ('every reported-open n <= 100'; 'reported solved'), or give a reported-only closure a formal-lane label such as 'reported; not replayed', or split the tables on the verified status. The generator change touches every reported-only case and the report's regenerated tables, so it is broader than #560's layer; it waits on nothing but a decision on which option.
