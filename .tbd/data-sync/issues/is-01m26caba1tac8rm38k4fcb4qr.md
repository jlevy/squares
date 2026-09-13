---
type: is
id: is-01m26caba1tac8rm38k4fcb4qr
title: Reject visible raw TeX in the PDF after a mathematics font fallback
kind: bug
status: closed
priority: 2
version: 6
labels: []
dependencies: []
parent_id: is-01m2cge1zdgenaswpf8nmd9fmv
created_at: 2026-09-10T19:22:07.553Z
updated_at: 2026-09-13T07:07:21.762Z
closed_at: 2026-09-13T07:07:21.762Z
close_reason: Implemented and independently reviewed in PR149 8d0a3ff2, inherited unchanged by PR156 52e4ab65. Exact stored PDF bytes and source receipt are validated; visible raw TeX, queued math and render errors are refused before export; live PDF receipts bind to fetched HTML. All six real browser controls and final artifact checks pass in both final-head Pages workflows (34743959872 and 34743978490). Full affected local gates and final hosted packing checks pass. Raw mismatch evidence is uploaded with seven-day retention; download before rerunning because GitHub can discard earlier-attempt artifacts. The intermittent PDF root cause remains separate under think-ptit.
resolution: null
duplicate_of: null
---
The earlier report named a host path that no longer exists: the current explainer does not call squaresMath.ready, does not request allEmbeddedFonts, and does not discard a ready status. Each formula calls kpressMathText.render or hydrate; a non-ready font result rejects, the host catches it, exposes native semantic MathML for kpress-math or source text for tex wrappers, marks that formula ready, and lets squaresMath.settled complete. The PDF exporter waits for math-ready, settled work, and document fonts, but it does not separately reject source-text fallbacks. First decide the publication contract: readable native MathML may be an intended fallback, while raw TeX in a PDF may be unacceptable. Then build a current-path browser control that forces a rendered-face timeout or error for both wrapper classes, records the resulting DOM and PDF behavior, and only add an exporter refusal if the evidence shows an unguarded unacceptable artifact.

## Notes

A retained production-browser control on September 13 confirmed that real rendered-FontFace error and timeout paths expose literal TeX in .tex wrappers while math-ready and settled both pass. Before the fix, render_pdf_bytes and repeated PDF comparison accepted an 863744-byte, 22-page, 24-embedded-font PDF with literal 3.8770835-backslash-ldots in its caption; pdftotext independently confirmed it. Native wrappers preserve readable visible MathML with hidden raw text. Add final DOM refusal before Page.pdf and run all five normal/error/timeout controls in Pages, preserving readable native fallback subject to the separate font policy. This is a publication defect, not an error in the theorem.
