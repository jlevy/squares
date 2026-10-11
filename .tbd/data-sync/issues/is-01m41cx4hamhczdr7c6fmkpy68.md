---
type: is
id: is-01m41cx4hamhczdr7c6fmkpy68
title: Write PR 305's four largest retained results one record per line
kind: task
status: closed
priority: 1
version: 4
labels:
  - session-169
dependencies:
  - type: blocks
    target: is-01m41cx57k479tywz7rqpgrceb
parent_id: is-01m41cx3q2pckpmsmmwq1rsngz
created_at: 2026-10-03T17:27:34.697Z
updated_at: 2026-10-03T22:33:44.308Z
closed_at: 2026-10-03T22:33:44.308Z
close_reason: "Done in PR jlevy/squares#305: sqpack.retained_json (width 1,000, filled scalar lists, allow_nan, linear cost; b4f0638b5) and PR 305's five largest retained results re-laid by their tools, 201,257 -> 27,501 lines with every value unchanged (2d3cc8114, re-pin a0058234d). The lane's five commits were combined into three so history keeps only the final layout."
resolution: null
duplicate_of: null
---
In PR jlevy/squares#305 (branch claude/ecstatic-archimedes-62hj6a): add one shared writer that lays a retained JSON document out one record per line (objects open one key per line to depth 2; every element of a list of records, and anything deeper, compact on its own line; sort_keys and ensure_ascii as each writer has them now), and use it in the four writers: devtools.census_atlas_contact_shades, devtools.classify_known_best_families, devtools.audit_t007_consumers, devtools.regularize_axis_components (the index). Regenerate the four files with each tool's --update, keep every --check passing, re-pin DATA_REVISION if the regularized index is release data, and follow the fast tier. Expected: 198,647 lines become about 2,700; no value changes; every reader parses JSON, so none should notice.
