---
type: is
id: is-01m4cqbwn7b3hq5rjrctxwdxww
title: Retain and verify the eight original FN-1 gzip inputs at b73473f
kind: task
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4c489df06vnyyd5fczynnkk
hold: null
hold_until: null
created_at: 2026-10-08T03:02:02.662Z
updated_at: 2026-10-08T03:02:11.516Z
started_at: 2026-10-08T03:02:11.514Z
---
Issue366 comment6029130241 supplies eight original check2/recorded-input.json.gz files at b73473fcf60421222b739294d3f7d9c4a8b8da07. Retain exact raw gzip blobs and primary binding manifest; maintained strict full-roster checker compares compressed old receipt hashes, bounded decompression byte equality with retained candidates, decompressed hashes and semantic digests. Close input binding only; no geometry replay, bounds or assurance changes. Separate branch codex/import-fn1-binding-supplement; full private source cap remains201326592.
