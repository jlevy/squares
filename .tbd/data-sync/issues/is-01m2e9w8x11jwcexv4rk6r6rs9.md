---
type: is
id: is-01m2e9w8x11jwcexv4rk6r6rs9
title: Diagnose and repair PR156 exact-head required-suite failure
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - ci
dependencies:
  - type: blocks
    target: is-01m2e0e4ct972w6eapcr8c3xjz
parent_id: is-01m2e0e4ct972w6eapcr8c3xjz
created_at: 2026-09-13T21:13:24.640Z
updated_at: 2026-09-13T21:13:29.442Z
---
On pushed PR156 draft 9c56e901, GitHub Actions run 34782594805 job 103792203850 failed step 5 (required pull-request behavioral lane) after 7m51s, causing packing-required failure. Retrieve and retain the exact failed log; distinguish source regression, test flake, and environment from evidence. Local full --push also failed its reachable step with unretained output, while a separate exact-head standalone rerun passed 5511/9/57 in 2002.14s. Repair the actual cause, rerun appropriate local push gate and current-head CI, update PR/body and think-4ovs. Do not mark PR ready on a partial pass.
