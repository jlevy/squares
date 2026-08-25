---
type: is
id: is-01m0v0z1kj1v09bzcd9qqk45ap
title: Add explicit-source SVG rendering CLI and atomic output
kind: task
status: closed
priority: 1
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - visualization
  - cli
dependencies:
  - type: blocks
    target: is-01m0v0zahjq54tvtm1sxr0c9yx
  - type: blocks
    target: is-01m0v102z22dxytc6atqpnszdz
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-24T23:16:22.257Z
updated_at: 2026-08-25T03:00:04.880Z
closed_at: 2026-08-25T03:00:04.880Z
close_reason: Implemented and validated the deterministic SVG toolkit, exact and numerical adapters, safe serializer, static and animated views, typed overlays, CLI, retained gallery, n=3 migration, documentation, and full gate.
resolution: null
duplicate_of: null
---
File: tools/render_packing_svg.py plus CLI boundary controls. Implement parse_args, build_source_parser, load_event, load_builtin, build_spec, and main with explicit event, builtin, and n5-face sources. Parse JSON decimal tokens without an intermediate binary64 round-trip; mirror ViewLevel and AnnotationLevel without exposing raw style internals; select one BasinEvent by stable event ID; write only through write_svg_atomic after validation/reparse. Test high-precision decimal retention, malformed JSONL, missing or duplicate event IDs, incompatible source/view combinations, refusal to overwrite on failure, deterministic stdout/stderr summaries, and successful overview/comparison generation.
