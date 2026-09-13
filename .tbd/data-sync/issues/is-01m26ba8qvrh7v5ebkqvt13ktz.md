---
type: is
id: is-01m26ba8qvrh7v5ebkqvt13ktz
title: Intermittent explainer PDF byte disagreement has no identified cause
kind: bug
status: open
priority: 1
version: 4
labels: []
dependencies: []
created_at: 2026-09-10T19:04:36.347Z
updated_at: 2026-09-13T06:10:14.568Z
---
On September 10, 2026, Pages run 34453706991 at `3a18a05a` reported unequal normalized PDF lengths: `786119` and `786117` bytes. The job passed on a rerun, and the earlier PR run 34449286960 at `0c4c41b4` also passed. This establishes intermittent reproduction failure; the lengths alone do not establish truncation, an exact-prefix relationship, a race, or a particular cause. They also do not prove that the rendered pages look different.

The original investigation reported a 94-byte publication receipt on all four examined runs and a usual normalized size of 786119 bytes. Those observations do not identify the contents of the differing pair. No retained byte comparison rules out a clock-related or other runtime cause.

Forty consecutive same-host container renders agreed at 863873 bytes in 1m54s using the preinstalled headless shell. That study did not reproduce the CI failure. Its host used 19 embedded faces versus CI's 18, so it is not evidence of identical behavior on the CI runner.

PR149's D-490 changes provide bounded difference diagnostics and `--renders N`. An exact-prefix report states only the byte relationship; otherwise the diagnostic identifies the first offset, its containing object or outside-object section, declared type where available, and byte windows. The image-readiness and reduced-motion guards close separate known hazards, but neither is established as the cause of these incidents.

The September 12 stack review observed another disagreement in PR148 before these diagnostics were inherited; the notes retain its run and unchanged-rerun evidence. All three final stack heads passed their first-attempt PDF checks. The root-cause issue remains open.

On the next occurrence with the diagnostics present, inspect the reported difference before proposing a causal repair. If repeated CI draws are needed, use the maintained `--renders N` option on a CI host. A passing rerun is validation of that rerun, not proof that the intermittent cause was fixed.

## Notes

September 12 stack review: PR148 at a072723bac956d4438a21c57565cc066b760f7fa failed PDF self-reproduction in run 34739859995, attempt 1: 843074 then 843073 normalized bytes. The failing pair and object offset were not retained, so no cause can be inferred. An independent Astra Max review found no evidence identifying PR149 readiness guards as this incident’s remedy. Attempt 2 passed on the unchanged revision: two renders agreed at 843074 bytes, 22 pages, and 18 embedded fonts; the full Pages build passed. PR149 and PR156 also passed their initial hosted PDF checks with the diagnostic and readiness changes. This issue remains open. A future occurrence with the PR149 diagnostics should identify the byte location/object before another causal fix is proposed.
