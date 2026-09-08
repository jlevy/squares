---
type: is
id: is-01m21f1xf01nwz7jf9bgc3zgnr
title: Review math loading complexity before release
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: kpress_font_pipeline
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T21:33:44.799Z
updated_at: 2026-09-08T21:40:34.022Z
---
Owner is concerned that the working page relies on an overengineered or brittle font pipeline. Perform a bounded independent architecture review of build-time KaTeX rendering, geometry reservations, saved font variants, cached font readiness and platform rendering assumptions. Identify removable machinery and concrete release blockers; preserve the working page and do not start a replacement rendering framework.

## Notes

Independent Astra review recommends keeping the working design. KaTeX still owns typesetting; measured per-base boxes are justified specifically by the no-shift requirement. Removed four per-base diagnostic attributes from publication HTML and its variant signatures; no runtime or layout consumer used them. Existing variant deduplication remains. KPress client-side rendering stays independent of the optional Squares build step. Main release check: validate the same Linux-built final artifact on macOS browsers, since local 16x width linearity alone does not establish cross-platform equality. A selected-profile font manifest is an optional later optimization, not a release requirement; no new abstraction or rendering engine is proposed.
