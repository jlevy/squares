---
type: is
id: is-01m21dyyygnr8mpt1vt77b26a4
title: Match inline and display math to the surrounding text size
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: caption_rendering
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T21:14:39.439Z
updated_at: 2026-09-08T21:20:34.647Z
---
User reports sans math in figure captions looks too small and explicitly requires both inline and display math to follow the size of surrounding text. Audit the nested prepared-variant and KaTeX font-size cascade in prose, captions and displays, then correct it while rebuilding matching reserved geometry. Delegate caption_rendering.
