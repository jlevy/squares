---
type: is
id: is-01m0spchq2d2nh2n6m5y713t3r
title: Correct Stromquist Figure 13 coordinate transcription
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/resources/papers/stromquist-2003-packing-10-or-11-unit-squares.md
labels:
  - packing
  - focus-soundness
dependencies: []
parent_id: is-01m0p4bxnqxb8dsv2rnqgyp0w8
created_at: 2026-08-24T10:52:15.969Z
updated_at: 2026-08-24T11:14:58.256Z
closed_at: 2026-08-24T11:14:58.255Z
close_reason: Corrected both Figure 13 coordinate lists from rendered primary PDF page 9, corrected the downstream research report, annotated the reconstructed source and archive index, and logged D-146. Focused schema, generated-view, synopsis, count-mutation, Flowmark, and diff checks pass; executable tuple binding remains explicitly assigned to parent think-bvy9 rather than falsely claimed as present.
resolution: null
duplicate_of: null
---
The cleaned Stromquist transcription misread the four defining Figure 13 points. The PDF states (1,1), (s/2,1), (3/2-s/4,s/2), and (1/2+s/4,s/2), with the rest placed symmetrically; the clean Markdown instead gives (s/2,s/2), (1,s/2), and (3/2,1). Correct the clean transcription from the rendered primary page, flag the repaired passage under the archive convention, log the defect, and bind H-010's executable point set to the corrected source.
