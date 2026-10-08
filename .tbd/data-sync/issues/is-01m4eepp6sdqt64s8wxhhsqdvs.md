---
type: is
id: is-01m4eepp6sdqt64s8wxhhsqdvs
title: Declare exact-register ceiling consumers and align marker registry
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
labels: []
dependencies: []
parent_id: is-01m4e2gm6ya1mxg40qmv53ysbn
created_at: 2026-10-08T19:09:08.184Z
updated_at: 2026-10-08T19:09:08.184Z
---
CI exposed undeclared verified_upper_bound readers in the exact-register builder/tests, a T007 audit crash, and obsolete slow-marker expectations after upstream changed census fixtures. State ceiling semantics, repair the audit if needed, align registry to actual measured markers, and validate both stack layers.
