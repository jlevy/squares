---
type: is
id: is-01m26ba8qvrh7v5ebkqvt13ktz
title: Intermittent explainer PDF byte disagreement has no identified cause
kind: bug
status: open
priority: 1
version: 12
labels: []
dependencies: []
created_at: 2026-09-10T19:04:36.347Z
updated_at: 2026-09-14T02:25:16.172Z
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

September 13, 2026 resumed review clarification:

The later PR157 correction preserves additional quoted /Rect windows, but those windows establish only the reported numeric annotation difference. They do not establish identical prepared HTML or rule out absent content elsewhere. The earlier note's phrase 'a text-measurement difference rather than content going missing' overstates what the retained evidence proves. Current disposition remains unknown cause. PR149's artifact/source/math guards close independently reproduced publication gaps, without establishing or fixing this historical cause. Save future failure diagnostics before rerunning an Actions attempt; leave this issue open.

September 13 new retained occurrence: Pages run34774787868 attempt1 failed on PR157 cadbf7e149b65215724daf813add78d80879d327 at the stored-artifact vs fresh-draw check. All six browser/math failure controls passed first. Actual reference.pdf/replay.pdf and neutral report were downloaded before any retry from explainer-pdf-check artifact10323137895 into /private/tmp/pr157-ci-cadbf7e1/pages-artifacts/explainer-pdf-check/pdf-check-644lkxd1. Both raw/normalized lengths843157; normalized first differing byte524772 in object156. Reference SHA256 ea8a21929c8e7fe9b4a401b22e521e4fae9351617d0fb317ee5144a70f17b70e; replay e76ca05a908f8beef6bbea6a6d6237c951b38ca1a0d480499d304b5ee78fea32. Exact prepared HTML also retained. Independent byte/stream and content/visual reviews are in progress; cause is not yet established. No retry or normalization change has been made.

September 13 PR125 occurrence after refreshing onto main: Pages run 34790001091 build failed at --check-artifact, with both normalized PDFs 843168 bytes and first byte difference 511882 in object 137. Diagnostics were downloaded before any rerun from artifact explainer-pdf-check/pdf-check-j5f4o0dc into /private/tmp/squares-pr125-pdf-diagnostics; SHA256 reference d141f788ca6622d6b39e07aff8cf568749683ba77ad247643e156b8b54a52b15, replay 3adda4a7a8db72c43e74d0183363392ce4e13961e737b0ba759f70d6ba4dfc12. The report states cause unknown. No rerun or root-cause claim made.

PR125 run 34790001091 attempt 2 completed successfully after the failure pair had been downloaded. This passing retry does not establish a cause or resolve D-490.
