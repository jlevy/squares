---
type: is
id: is-01m1yx70zbwfc3t6tfmjvp0rdh
title: Verify latest merged explainer changes deployed
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m1ywjmdsmsjnxqbhd56er89j
created_at: 2026-09-07T21:43:29.002Z
updated_at: 2026-09-07T23:39:52.742Z
closed_at: 2026-09-07T21:44:22.246Z
close_reason: Pages runs34160383016(PR112) and34163156383(PR115) completed successfully. check_published_site against a5e9dbfd01b0b799780a93a6b7bc5542c1fd4616 passed26of26 checks; HTML/Markdown stamp and repository links match, PDF14pages and all assets returnHTTP200.
resolution: null
duplicate_of: null
---
Check Pages workflow for recent main merges and run check_published_site at latest merged revision; distinguish published main from current unmerged Figure5 fixes.

## Notes

Prior PRs #112 and #115 deployed successfully and the live site passed 26 checks against a5e9dbfd. After PR #114 merged, the Certificate page build and deploy jobs also passed for main373beb36 in run34168046492. The repository check_published_site tool passed all26 checks against full commit373beb366b98b435207694d6bd425295410dbc83, including the edition stamp, every pinned repository link, Markdown, PDF (16pages), and composite assets. PR #117 remains a preview and is not yet deployed. Latest verification log is /tmp/figure-order-latest-deployment.txt.
