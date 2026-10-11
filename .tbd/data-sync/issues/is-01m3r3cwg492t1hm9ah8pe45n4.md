---
type: is
id: is-01m3r3cwg492t1hm9ah8pe45n4
title: "Films on the site: PUBLISHED_FILMS pin and a publish step that fetches, verifies and caches both v0.4.2 films under films/"
kind: task
status: open
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies:
  - type: blocks
    target: is-01m3r3cz3tnqy50y2971gr776f
  - type: blocks
    target: is-01m3r3d2at84w57v6kmhd8tvg2
  - type: blocks
    target: is-01m3qr6wqssd2sm32twemg0tpy
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T02:48:15.108Z
updated_at: 2026-09-30T19:53:07.269Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
Spec: Published Media. Pin release tag, asset name, bytes and SHA-256 (the receipts' video_sha256) in sqpack/release.py; publish downloads both films into site/films/, fails on any mismatch (OR-16 trust boundary), caches by hash; pull requests never fetch. The explainer's <video> source moves to the same-origin copy.

## Notes

Reviewed design: publish runs for pull requests (only its upload is gated), so the fetch, verify and cache steps carry the upload's main-only condition. Pull requests never download the films.

Reopened: Done only on origin/claude/optimistic-gauss-uzmcl2 (764a5ac90, f760444fe), which is not in the claude/overview-page-impl PR; that branch has no PUBLISHED_FILMS or published_media and links the films at releases/download.
