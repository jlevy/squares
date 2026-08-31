---
type: is
id: is-01m0v0yf3ffe0tg78dss3cdx77
title: Build the safe deterministic ElementTree SVG spine
kind: task
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - visualization
  - tdd
dependencies:
  - type: blocks
    target: is-01m0v0ypqc2shhf313140pqsmk
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-24T23:16:03.310Z
updated_at: 2026-08-25T03:00:04.855Z
closed_at: 2026-08-25T03:00:04.855Z
close_reason: Implemented and validated the deterministic SVG toolkit, exact and numerical adapters, safe serializer, static and animated views, typed overlays, CLI, retained gallery, n=3 migration, documentation, and full gate.
resolution: null
duplicate_of: null
---
Files: sqpack/render/svg.py and XML/safety controls in tools/check_svg_rendering.py. Implement the namespace helpers, accessible title/desc ordering, versioned metadata, exact comments, fragment-only use, safe-tree validator, readable serializer, diagnostic C14N, and atomic write boundary from the spec. Use xml.etree.ElementTree rather than a custom scene graph or third-party XML library. Test first for attribute/element order, comment grammar, escaping, duplicate IDs, forbidden DTD/script/event/foreignObject/xlink/external references, one terminal LF, comment-preserving reparse, and byte replay.
