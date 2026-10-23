---
type: is
id: is-01m5kh3wnyj43qg2pz30qgmpjw
title: Register cropped tutorial SVG assets in the published site inventory
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: ci-followups
labels: []
dependencies: []
parent_id: is-01m5kcfhfdmgfb03gn3drg43rc
hold: null
hold_until: null
created_at: 2026-10-23T04:43:11.933Z
updated_at: 2026-10-23T04:48:42.776Z
started_at: 2026-10-23T04:43:25.509Z
closed_at: 2026-10-23T04:48:42.774Z
close_reason: Fixed in pushed commit 739e283b6921d576a96c595ecd4d139c33e96c39. Added a separate overview-owned namespace limited to the two tutorial SVG stems and 16 lowercase hexadecimal digest characters; preserved generic PNG handling and regenerated only the URL YAML/Markdown inventory rows. Four focused registration tests passed in 0.97s, including unrelated name/hash/extension rejection; native registry check 1159 rows/0 failures; Ruff/BasedPyright/diff checks clean. Coordinator owns final-head CI and merge.
resolution: null
duplicate_of: null
---
