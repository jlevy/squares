---
type: is
id: is-01m26caba1tac8rm38k4fcb4qr
title: Decide whether PDF export must reject a mathematics fallback
kind: bug
status: in_progress
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-09-10T19:22:07.553Z
updated_at: 2026-09-13T06:19:42.581Z
---
The earlier report named a host path that no longer exists: the current explainer does not call squaresMath.ready, does not request allEmbeddedFonts, and does not discard a ready status. Each formula calls kpressMathText.render or hydrate; a non-ready font result rejects, the host catches it, exposes native semantic MathML for kpress-math or source text for tex wrappers, marks that formula ready, and lets squaresMath.settled complete. The PDF exporter waits for math-ready, settled work, and document fonts, but it does not separately reject source-text fallbacks. First decide the publication contract: readable native MathML may be an intended fallback, while raw TeX in a PDF may be unacceptable. Then build a current-path browser control that forces a rendered-face timeout or error for both wrapper classes, records the resulting DOM and PDF behavior, and only add an exporter refusal if the evidence shows an unguarded unacceptable artifact.

## Notes

Reconciled against PR149 combined head 237c4023 after Astra review flagged the old API description. This remains open as a current-path policy and control question; the obsolete proposed remedy should not be implemented. It is separate from D-491, whose geometry-probe observation and timer controls are fixed.
