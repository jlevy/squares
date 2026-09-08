---
type: is
id: is-01m1zzsspkf31ysgtq60kwqy2p
title: Restore full main CI before font integration merge
kind: bug
status: closed
priority: 1
version: 10
labels: []
dependencies:
  - type: blocks
    target: is-01m1zzjddp742vysds0fzm3fe8
parent_id: is-01m1zzjddp742vysds0fzm3fe8
created_at: 2026-09-08T07:47:55.730Z
updated_at: 2026-09-08T10:53:01.604Z
closed_at: 2026-09-08T10:53:01.603Z
close_reason: "Completed in Squares #128 at 33cd4760, preserving the original #122/#123 heads and main #120 changes. Final fast, deferred, Pages, and full post-merge Packing validation run 34214731500 passed. All five applicable main jobs succeeded and uploaded timings. Live HTML and PDF checks passed. Detailed evidence is in the notes; further CI performance work remains on think-ph9v."
resolution: null
duplicate_of: null
---
Main run34196866309 failed three steps: translation escape timeout900s, slow behavioral timeout1800s, quick synopsis snapshot14.44s exceeds12s. Review pending D481 PR122/123 fixes, reproduce or inspect measured evidence, integrate narrow validated repairs, run complete premerge evidence and confirm postmerge CI and page deployment.

## Notes

Squares PR #128 merged at 33cd47606dae223664f117945631440aa5c8ece9. The merged tree
ea7f5f6bf997592a1c8513226004710dea9b29ce is identical to final PR head 43c006bc and
GitHub test merge 52b49d91. Both CI repair heads, de756cef from PR #122 and f41939d0
from PR #123, are ancestors of merged main; GitHub marks all three PRs merged.
Native stack branches were preserved.

Local validation passed 4,246 reachable tests after integrating main #120, all 31 record
checks, and 881 reachable tests after the final dependency pin.
Hosted fast run 34212267383, Pages run 34212267378, and all four jobs plus the aggregate
in deferred run 34212270588 passed on the final source.
Post-merge Pages run 34214731528 passed and deployed v0.2.4-33cd4760; live loading
checks passed in Chromium, Firefox, and WebKit, and actual-font checks passed for screen
and print.

Full post-merge Packing validation run 34214731500 passed on
33cd47606dae223664f117945631440aa5c8ece9:
https://github.com/jlevy/squares/actions/runs/34214731500. All five applicable jobs
passed: validate in 30m19s, slow-lane in 14m23s, exhaustive in 28m11s, screen in 16m15s,
and macos-portability in 2m16s. The PR-only jobs are intentionally skipped for a push to
main. These are single hosted wall-time readings, not a controlled performance
comparison. Every job uploaded its timing artifact.
The complete log is retained at /tmp/squares-font-main-ci-complete.log and artifacts at
/tmp/squares-font-main-ci-artifacts/.

D-484 records the CI repair; the integration retains #120’s independent slow lane
alongside exhaustive, screen, and the remaining checks.
The xdist guard no longer treats a worker collection failure as an empty successful
selection. Workflow guards prove the full and deferred partitions, and the fresh
fast/deferred/Pages results verify the final integrated source.
The CI repair and parent rendering audit are complete; further parallel-efficiency work
remains on think-ph9v.
