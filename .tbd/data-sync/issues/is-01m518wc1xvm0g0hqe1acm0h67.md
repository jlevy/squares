---
type: is
id: is-01m518wc1xvm0g0hqe1acm0h67
title: Style the full changelog as a sans-serif external navigation button
kind: bug
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m50s7ppqb37qxtm4ty6bxw0a
hold: null
hold_until: null
created_at: 2026-10-16T02:32:57.148Z
updated_at: 2026-10-16T03:34:31.242Z
started_at: 2026-10-16T02:33:12.682Z
closed_at: 2026-10-16T03:34:31.242Z
close_reason: "Completed News consistency work: stack635/PR633-634 merged3685616d with passing exact-main Packing and4517 live checks; follow-upPR638 merged4e8c8987 by merge commit, source7627f47e retained. SeniorA5542565797 and correctnessB5542654327 at exact4e983d2c found no issues. Exact-head Packing38843354043/Pages38843354058/mergeability38843347696 passed; actual1280/390 browser cases and51forwarders passed zero skips. Sitev0.7.13 exact-main Pages38844993807 deployed and passed4519/4519 checks with0retries. Root liveUI verified all3 canonical article titles/dates/topiccomputedstyles match News, title stable-link navigation, click expansion/contraction, sans Fullchangelog shared external icon/accessiblename/href; defaultbrowserNewsopened. Ownervisualcheckboxes untouched. Nativecheckpoint38844993715 stillrunning withoutfailures atcloseout; broadercost/causaldiagnosisremainopen think-yops/ht59/kxmq. Durableevidence in primary .codex/regularization-closeout-evidence-2026-10-13/pr638-home-news-parity-20261016 and pr638-main-4e8c8987-20261016."
resolution: null
duplicate_of: null
---
The News footer's Full changelog link inherits serif body typography. Use the existing navigation button/action styling and external-link icon, ensure navigation typography is always sans-serif, document the systematic design rule, and add a focused rendering/style contract. Include in the homepage/shared-article follow-up PR.
