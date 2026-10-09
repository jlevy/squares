---
type: is
id: is-01m4fzyhtapn4ssshxw54j0ndn
title: "#408 adds a 29 s module setup to the fast lane (recorded cost 2.6 s)"
kind: task
status: open
priority: 3
version: 1
labels:
  - n-17
dependencies: []
parent_id: is-01m4fjgn6atbd63aj7rjjznaq4
created_at: 2026-10-09T09:29:46.058Z
updated_at: 2026-10-09T09:29:46.058Z
---
test_n17_core_stress.py on #408 takes 38.7 s vs 5.1 s on main because of a 29.2 s module-scoped setup; suite-file-costs.json records 2.598 s and the shard is near capacity. The cost guard passes because the 12 s ceiling counts only test calls. Per OR-14, measure on hosted CI after landing and move the setup or mark slow if it inflates the fast lane.
