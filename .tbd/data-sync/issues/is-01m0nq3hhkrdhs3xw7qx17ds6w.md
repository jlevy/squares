---
type: is
id: is-01m0nq3hhkrdhs3xw7qx17ds6w
title: Write cleaned .md transcriptions for the raw-only archived papers
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0nrh9mwfjndkzejq34js78c
created_at: 2026-08-22T21:47:51.730Z
updated_at: 2026-08-22T22:13:15.278Z
---
The archive's discipline is original + cleaned .md + faithful .raw.md. Four entries fall short, and explorations/packing/resources/README.md states which under 'Transcription status, stated exactly'.

RAW-ONLY (PDF + .raw.md, no cleaned .md):
- gensane-ryckelynck-2005-improved-dense-packings
- nagamochi-2005-packing-unit-squares-in-a-rectangle
- wang-dong-li-2016-new-result-packing-unit-squares
All three were read directly from the PDF and the claims resting on them were checked there.

PARTIAL:
- roth-vaughan-1978-inefficiency-packing-squares carries abstract, introduction and
  Theorem, read from the rendered page image. Sections 2-7 are deliberately not
  transcribed: the 1978 scan's OCR loses subscripts, superscripts and interval notation,
  and transcribing it would mean RECONSTRUCTING mathematics rather than reformatting it.
  Completing it needs a human or a careful page-image pass, not an OCR cleanup.

Deferred deliberately rather than done hastily. Model-assisted cleanup is what produced
the reconstruction hazards tabulated in the resources README, and Roth-Vaughan is the
argument for caution: two independent secondary sources reported a constant the paper
does not contain. Any transcription added here must flag reconstructed passages inline
and be counted in that README table.
