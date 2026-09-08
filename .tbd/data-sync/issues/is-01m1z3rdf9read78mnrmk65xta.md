---
type: is
id: is-01m1z3rdf9read78mnrmk65xta
title: Resolve the final PR validation timing failure
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m1z0patm2bp8vk8h8ntk3gwe
created_at: 2026-09-07T23:37:50.302Z
updated_at: 2026-09-07T23:41:58.744Z
closed_at: 2026-09-07T23:41:58.744Z
close_reason: "Completed in PR #117 at 83a2e6f3. All required hosted checks and the paper build passed; the timing-only CI failure passed one unchanged-commit retry. Three agent reviews and root review accepted the work. HTML, Markdown and the 17-page PDF were rebuilt; the web preview and Preview PDF were opened. The latest upstream deployment also passed all 26 live-site checks. Separate selector issue think-oe1g remains open."
resolution: null
duplicate_of: null
---
PR117 head83a2e6f3 passed the paper build and every correctness check, but the validate job failed its relative timing guard:151.22s vs99.39s recorded baseline, ratio1.52 with a1.5 failure threshold (absolute ceiling195s). Exact verification95.4s, soundness perimeter73.0s and basedpyright61.1s dominate. Retry failed jobs once to distinguish runner variability, inspect independently, and retain the first failure as evidence without weakening any guard.

## Notes

The first attempt passed every correctness check but failed only the relative checks-tier timing guard: 151.22 seconds vs 99.39 seconds recorded, above the 149.085-second threshold and below the 195-second absolute ceiling. Independent review confirmed the two dominant mathematical checks, inputs, worker settings, budget register, and validation workflow are unchanged by this branch. Runner variability is plausible but unproved. A single unchanged-commit retry passed the same guard in 142.51 seconds; all required checks are green on 83a2e6f3. Both attempts are retained in run https://github.com/jlevy/squares/actions/runs/34170421246 and described in PR #117. No guard, code, or baseline was weakened.
