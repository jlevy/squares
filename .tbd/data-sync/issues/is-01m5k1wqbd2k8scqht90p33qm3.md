---
type: is
id: is-01m5k1wqbd2k8scqht90p33qm3
title: "Workbench page: carry the site's speculation rules"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5jr2cr74kbbn71j05pqsgkd
created_at: 2026-10-23T00:17:08.410Z
updated_at: 2026-10-23T00:17:08.410Z
---
think-gr4c added render_overview.speculation_rules_tag() to the site's kpress and static pages. The workbench (packages/workbench/tools/workbench_tools/build_site.py with_head) writes its head from head_tags alone, so a link clicked from the workbench is not prerendered. Add the tag after head_tags there and extend packages/workbench/tests/test_site_nav.py.
