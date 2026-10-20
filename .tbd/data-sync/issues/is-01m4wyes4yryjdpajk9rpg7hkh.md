---
type: is
id: is-01m4wyes4yryjdpajk9rpg7hkh
title: "audit_continuous_pose.build_all: hash the copied sources rather than record the manifest's digests (PR 598 review A12)"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-14T10:13:48.318Z
updated_at: 2026-10-14T10:13:48.318Z
---
Review A12 on PR 598: build_all records the manifest's digests as the sources it built without hashing the bytes it copied from release.source; off the CI compiler build_checks skips the binary comparison, so a drifted retained source would be built and recorded under the manifest digest. Hash the copies and refuse a mismatch.
