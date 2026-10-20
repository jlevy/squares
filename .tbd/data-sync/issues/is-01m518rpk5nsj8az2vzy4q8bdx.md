---
type: is
id: is-01m518rpk5nsj8az2vzy4q8bdx
title: Render homepage News from the same articles and tags as News
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m50s7ppqb37qxtm4ty6bxw0a
hold: null
hold_until: null
created_at: 2026-10-16T02:30:56.868Z
updated_at: 2026-10-16T03:34:31.236Z
started_at: 2026-10-16T02:31:07.046Z
closed_at: 2026-10-16T03:34:31.236Z
close_reason: "Completed News consistency work: stack635/PR633-634 merged3685616d with passing exact-main Packing and4517 live checks; follow-upPR638 merged4e8c8987 by merge commit, source7627f47e retained. SeniorA5542565797 and correctnessB5542654327 at exact4e983d2c found no issues. Exact-head Packing38843354043/Pages38843354058/mergeability38843347696 passed; actual1280/390 browser cases and51forwarders passed zero skips. Sitev0.7.13 exact-main Pages38844993807 deployed and passed4519/4519 checks with0retries. Root liveUI verified all3 canonical article titles/dates/topiccomputedstyles match News, title stable-link navigation, click expansion/contraction, sans Fullchangelog shared external icon/accessiblename/href; defaultbrowserNewsopened. Ownervisualcheckboxes untouched. Nativecheckpoint38844993715 stillrunning withoutfailures atcloseout; broadercost/causaldiagnosisremainopen think-yops/ht59/kxmq. Durableevidence in primary .codex/regularization-closeout-evidence-2026-10-13/pr638-home-news-parity-20261016 and pr638-main-4e8c8987-20261016."
resolution: null
duplicate_of: null
---
Owner observed live homepage News uses result-derived cards and kind tags (e.g. Formalization), differing from canonical News articles/topics and chip sizing. Reuse the News article renderer and shared topic metadata on homepage; select the newest three S5 result news articles, preserve claim qualifications/links, unify typography/tags/card behavior, add focused parity contracts, cut the next site edition, independently review, PR and deploy. Continuing the News design-system spec; keep exact deployed368 verification and mainCI observation in parallel.
