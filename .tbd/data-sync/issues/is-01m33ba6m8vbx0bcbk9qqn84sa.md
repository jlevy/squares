---
type: is
id: is-01m33ba6m8vbx0bcbk9qqn84sa
title: Open the pull request for claude/workbench-full-ascent-video with its generated cost block
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies:
  - type: blocks
    target: is-01m33bj34g60trhsnazpyetwsj
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T01:22:32.710Z
updated_at: 2026-09-22T01:57:10.334Z
closed_at: 2026-09-22T01:57:10.333Z
close_reason: Opened https://github.com/jlevy/squares/pull/218 at 512bbf456, main merged, with the generated cost block (devtools.render_pr_rollup over the committed rollup) and a description that passes devtools.check_pr_description. Hosted CI not yet read, by the owner's choice to review the page first.
resolution: null
duplicate_of: null
---
The branch (video capture and delivery profiles, the stage layout and color work, and the transition contract) has no pull request, so no hosted CI has run on it. Merge main, run the push tier, write the session's Claude rollup into packing/campaign/resource-usage, and open the PR in the template's section order with the cost block from devtools.render_pr_rollup, checked by devtools.check_pr_description. Then read hosted CI on the pushed revision and keep the description current as later fixes land on the branch.
