---
type: is
id: is-01m4y09zpndtpme3qk80fdmskt
title: "PR604 F2: keep News collapsed when using rating tooltips"
kind: bug
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
labels: []
dependencies: []
parent_id: is-01m4xm9zrn7p4nygg25gwy9cxw
created_at: 2026-10-14T20:05:22.772Z
updated_at: 2026-10-14T20:05:22.772Z
---
Final correctness review F2: focusin from a shared rating tooltip expanded the card. Fixed by narrow tooltip-target guard in296c65c90fd5f25c0a674abb92e798e02bb721ee. Two retained desktop/mobile browser cases pass, preserving ordinary link-focus disclosure.
