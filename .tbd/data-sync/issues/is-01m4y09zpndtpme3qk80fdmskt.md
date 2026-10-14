---
type: is
id: is-01m4y09zpndtpme3qk80fdmskt
title: "PR604 F2: keep News collapsed when using rating tooltips"
kind: bug
status: closed
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4xm9zrn7p4nygg25gwy9cxw
hold: null
hold_until: null
created_at: 2026-10-14T20:05:22.772Z
updated_at: 2026-10-14T20:08:41.015Z
started_at: 2026-10-14T20:05:37.056Z
closed_at: 2026-10-14T20:08:41.015Z
close_reason: "Fixed in17ead6a3 and296c65c9; current-head correctness Review F5523939695 confirms both. Four chooser/bookmark and two tooltip desktop/mobile cases pass. Dispositions: https://github.com/jlevy/squares/pull/604#issuecomment-6177309801"
resolution: null
duplicate_of: null
---
Final correctness review F2: focusin from a shared rating tooltip expanded the card. Fixed by narrow tooltip-target guard in296c65c90fd5f25c0a674abb92e798e02bb721ee. Two retained desktop/mobile browser cases pass, preserving ordinary link-focus disclosure.
