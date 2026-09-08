---
type: is
id: is-01m1zzsspkf31ysgtq60kwqy2p
title: Restore full main CI before font integration merge
kind: bug
status: in_progress
priority: 1
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01m1zzjddp742vysds0fzm3fe8
parent_id: is-01m1zzjddp742vysds0fzm3fe8
created_at: 2026-09-08T07:47:55.730Z
updated_at: 2026-09-08T08:08:24.917Z
---
Main run34196866309 failed three steps: translation escape timeout900s, slow behavioral timeout1800s, quick synopsis snapshot14.44s exceeds12s. Review pending D481 PR122/123 fixes, reproduce or inspect measured evidence, integrate narrow validated repairs, run complete premerge evidence and confirm postmerge CI and page deployment.
