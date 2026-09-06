---
type: is
id: is-01m1tvff0nt87r2mxga9tm04sz
title: "PR #93 review R1: correct mandatory deep-gate rollout and event coverage"
kind: bug
status: in_progress
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1tve7ex9akeg5842fnbfesr
created_at: 2026-09-06T07:56:10.628Z
updated_at: 2026-09-06T07:56:52.396Z
---
Review R1 https://github.com/jlevy/squares/pull/93#issuecomment-5557862664; development.md:332-342 and .github/workflows/deep-gate.yml:41-74. Current personal repository cannot activate advertised settings-only queue; required contexts need both event surfaces; opened missing. Correct advisory scope and add event coverage tests.
