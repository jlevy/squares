---
type: is
id: is-01m5k62y0meb5c72fjzjqd97h2
title: "Browser check: Chromium accepts the site's speculation rules"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5jr2cr74kbbn71j05pqsgkd
created_at: 2026-10-23T01:30:26.196Z
updated_at: 2026-10-23T01:30:26.196Z
---
Chromium drops an invalid rule set silently (a console warning only). Review of #740 suggested asserting Preload.ruleSetUpdated has no errorType on one built page in an existing browser check (check_site_rendering or test_site_rendering); CDP reports it even though attached DevTools blocks the prerender itself. Probe code goes in a probes/ file per the no-JS-in-Python rule.
