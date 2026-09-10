---
type: is
id: is-01m26b9kjzhrxhsw4dm5atkax2
title: "Explainer v0.4.0: add two-entry version history"
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - explainer
  - documentation
dependencies: []
parent_id: is-01m25zrj5np9ywft00t8j8neaz
created_at: 2026-09-10T19:04:14.683Z
updated_at: 2026-09-10T19:51:53.172Z
closed_at: 2026-09-10T19:51:53.159Z
close_reason: "PR #148 commit 35484ebd publishes the v0.4.0 explainer and exactly two source-derived history entries. v0.4.0 was first labeled September 10, 2026 at 35484ebd; v0.3.0 was first labeled September 8, 2026 at ce3b1ab5606307ed5cb6780da09c1b5f233ab2e1 and is identified as the 3.81-result edition. One release-history source drives all rendered forms, focused tests cover the labels and dates, and the 135-test local documentation block plus rendering gates pass. Stacked hosted readiness remains separately owned by think-0zc1."
resolution: null
duplicate_of: null
---
Update the standalone explainer branch and PR148 so the current T-025/T-026 edition is version v0.4.0. Preserve v0.3.0 as the prior 3.81-result edition and add a concise two-entry version history near the top. Bind every displayed version surface and generated HTML, Markdown and PDF artifact to one source of truth, add focused regression coverage, retain the existing URL, and keep scientific scopes exact: v0.4.0 states the weak lower limit 3.826447410572939744... with its endpoint unresolved. Completion requires regenerated artifacts, local documentation validation, independent review and the stacked hosted checkpoint.

## Notes

Owner clarification: every version-history entry must include the date the version label first appeared. Recover v0.3.0's first-label date from Git history rather than inferring a publication or theorem date; date v0.4.0 by the commit that first introduces that label. Preserve the Git evidence in the review and bind the rendered history to focused tests.
