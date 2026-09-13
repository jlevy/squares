---
type: is
id: is-01m26ba8qvrh7v5ebkqvt13ktz
title: Intermittent explainer PDF byte disagreement has no identified cause
kind: bug
status: open
priority: 1
version: 6
labels: []
dependencies: []
created_at: 2026-09-10T19:04:36.347Z
updated_at: 2026-09-13T07:50:39.175Z
---
On September 10, 2026, Pages run 34453706991 at `3a18a05a` reported unequal normalized PDF lengths: `786119` and `786117` bytes. The job passed on a rerun, and the earlier PR run 34449286960 at `0c4c41b4` also passed. This establishes intermittent reproduction failure; the lengths alone do not establish truncation, an exact-prefix relationship, a race, or a particular cause. They also do not prove that the rendered pages look different.

The original investigation reported a 94-byte publication receipt on all four examined runs and a usual normalized size of 786119 bytes. Those observations do not identify the contents of the differing pair. No retained byte comparison rules out a clock-related or other runtime cause.

Forty consecutive same-host container renders agreed at 863873 bytes in 1m54s using the preinstalled headless shell. That study did not reproduce the CI failure. Its host used 19 embedded faces versus CI's 18, so it is not evidence of identical behavior on the CI runner.

PR149's D-490 changes provide bounded difference diagnostics and `--renders N`. An exact-prefix report states only the byte relationship; otherwise the diagnostic identifies the first offset, its containing object or outside-object section, declared type where available, and byte windows. The image-readiness and reduced-motion guards close separate known hazards, but neither is established as the cause of these incidents.

The September 12 stack review observed another disagreement in PR148 before these diagnostics were inherited; the notes retain its run and unchanged-rerun evidence. All three final stack heads passed their first-attempt PDF checks. The root-cause issue remains open.

On the next occurrence with the diagnostics present, inspect the reported difference before proposing a causal repair. If repeated CI draws are needed, use the maintained `--renders N` option on a CI host. A passing rerun is validation of that rerun, not proof that the intermittent cause was fixed.

## Notes

Operational caution from the owner's 2026-09-13T07:44Z correction on PR157 (issuecomment, their own independent DOC-05 addendum): DOWNLOAD ANY FUTURE FAILURE DIAGNOSTICS BEFORE RERUNNING A GITHUB ACTIONS ATTEMPT, because reruns can make the earlier attempt's artifacts unavailable. That is why their review could not inspect a failed pair: 'No failed PDF pair from those attempts was available in this review.'

This bites directly on this bead's own standing instruction ('On the next occurrence with the diagnostics present, inspect the reported difference before proposing a causal repair'). The diagnostics only help if the artifacts are fetched before anyone re-runs the job. Treat a re-run as destructive to evidence until the artifacts are saved.

Note the two corrections on PR157 are complementary, not duplicates. The owner's states what the comparisons do not establish and what PR149 does close. Mine (issuecomment-5652038473) additionally quotes the occurrence-B byte windows from inside a /Link /Rect -- right edge 496.48898 against 491.23911, a 5.25pt text-measurement difference rather than content going missing -- which is evidence their review says was not available to it. Object attribution in my report remains unreliable (pre-hardening locator); the byte windows stand alone.
