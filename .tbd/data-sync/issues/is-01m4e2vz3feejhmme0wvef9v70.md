---
type: is
id: is-01m4e2vz3feejhmme0wvef9v70
title: Move oversized archived PDFs to hosted data and enforce a tracked-PDF budget
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex-polynomial-01a118e4
labels: []
dependencies: []
parent_id: is-01m4e2gm6ya1mxg40qmv53ysbn
created_at: 2026-10-08T15:42:18.222Z
updated_at: 2026-10-08T15:42:18.222Z
---
Audit found148 tracked PDFs totaling334168611 bytes, identical in old catalogue and incomingmain.13 originals exceed5MiB, seven exceed10MiB; generated catalogue PDF is ignored. Preserve exact original bytes and archival citation paths using existing GitHub-release hosted-data manifest, verify served assets before removing tracked working originals with trash and stage deletions. Add a5MiB tracked-PDF gate including staged additions and case-insensitive suffixes, wire into CI. No history rewriting; preserve primary source evidence. Moderate Sol xhigh owns guard/manifest/archive docs; root publication/Git/CI wiring.
