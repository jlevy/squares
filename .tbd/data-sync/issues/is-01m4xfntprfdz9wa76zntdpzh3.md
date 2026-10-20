---
type: is
id: is-01m4xfntprfdz9wa76zntdpzh3
title: Require Chromium for ordinary pull-request quick suites
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-14T15:14:45.080Z
updated_at: 2026-10-14T15:14:45.080Z
---
Independent PR599 delivery audit compared same-tree/source54b complete cohorts38583060155(normalPR) and38583046153(required-browserpush). Identical17891 collectedidentities; normal skips257 versus47, including210 additionalmissing-Chromium cases(A3/B7/C39/D161), allpassstrictcheckpoint. Normaljobs omitbrowser/npm setup so green suitejobs do not attest these browsercases. Preserve selectors/gates/ceilings; installpinnedbrowsertoolchain and requireChromium in ordinaryquick jobs or explicitly give all210a mandatoryequivalent CI owner. Current599delivery is coveredbyrequired-browsercheckpoint; this standingpipelinecleanup shouldnotbe mistakenforunexecutedcurrentdeliveryproof. Exact210case/reason/sourceaudit retainedprimary.codex/regularization-closeout-evidence-2026-10-13/cohort-comparison-38583060155-38583046153.json.
