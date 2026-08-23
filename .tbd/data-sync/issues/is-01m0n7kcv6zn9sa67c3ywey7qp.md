---
type: is
id: is-01m0n7kcv6zn9sa67c3ywey7qp
title: "Archive: extraction pipeline and provenance index"
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n7kcep0mgx5jnr6qz39e2h
created_at: 2026-08-22T17:16:53.989Z
updated_at: 2026-08-22T17:30:04.093Z
closed_at: 2026-08-22T17:30:04.093Z
close_reason: "resources/ built: papers/ with 14 PDFs plus faithful pdfminer raw extractions, web/ with 8 HTML captures plus Markdown, the Kingbird SVG, and README.md indexing everything with citation keys matching the research doc, grep recipes, and a table of non-retrievable sources with the obstacle for each."
---
Set up resources/papers/ with a README index recording for each paper: source URL, retrieval date, licence/open-access status, extraction method, and cleanup status. Pipeline is pdfminer.six then subagent cleanup.
