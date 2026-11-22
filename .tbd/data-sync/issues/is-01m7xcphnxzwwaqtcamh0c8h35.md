---
type: is
id: is-01m7xcphnxzwwaqtcamh0c8h35
title: "Import JoostdeWinter: exact certificates of GeiserX's published packings at 202, 204, 210, 263, 264, 295 and 297, pointer (#1037)"
kind: task
status: in_progress
priority: 2
version: 4
delegate: codex-intake-1119-01a1fb
labels:
  - result-import
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T21:09:48.349Z
updated_at: 2026-11-22T20:00:58.225Z
started_at: 2026-11-20T22:45:07.840Z
---
Issue jlevy/squares#1037 (Joost de Winter, 2026-11-18T20:06:25Z), a pointer: Sergio Fernández Rubio (GeiserX) published packings below the register at seven counts, in GeiserX/squares-in-squares (data/submission-best.csv.gz at c00281c2fb4b42a1c7071dc4fd493347cfd5a87b, CC BY 4.0 by the issue). De Winter says he is not the finder and asks that the packings be credited to Fernández Rubio.

The attachment GeiserX_exact.zip (github.com/user-attachments/files/35051652) is said to hold exact rational Witness/v2 files for all seven, tightened with Evan Daniel's contact solver: 202 at 14.724372709109, 204 at 14.802436041462, 210 at 14.971210662216, 263 at 16.724372709109, 264 at 16.772843152678, 295 at 17.698042929358, 297 at 17.739455512004, gains over the frontier at 1015fc1 from 4.63e-8 to 8.79e-3. It also gives exact sides for #811: Q(sqrt 3) forms at 202 and 263, a degree-70 root at 297.

Not read beyond the issue body: the attachment and the GeiserX repository were not opened by lane rec1120. The sweep of 20 November listed the issue as not in the record with no bead; it had no `intake` label until that lane added it. The entry in result-requests.yaml is triage: pending.

Owed: stage 1 triage against the houses as they now stand (210 and 295 moved with #1009; #1040's 259 pointer, think-squj, is the same source repository), retention of the attachment and the pinned source, replay, review, registration, credit to Fernández Rubio with de Winter as the certificates' author, and the answer on the issue.

## Notes

20 November 2026 triage against main c3f4a59dc1. All seven reported ceilings remain below the displayed main houses, including 210 and 295 after #1009. Main ceilings at 202, 204, 210, 263, 264, 295 and 297 are respectively 14.72792206135785, 14.8026468431066121, 14.9712146015881915, 16.73316600789937898, 16.7738075980019989, 17.6981150186993945 and 17.7394555582889518. Those comparisons use displayed values. The report-order and Option D checks still need exact sides and the competing certificates.

The 35051652 attachment is readable. Its streamed SHA-256 is 19c069b42d6a6fbe87dd419d358e7b046eadbba20dbaadd7f519faab1152c5e9. Pin the underlying coordinates at GeiserX/squares-in-squares c00281c2fb4b42a1c7071dc4fd493347cfd5a87b when retaining the packet. Replay the seven rational witnesses by the maintained exact routes and cost the separate algebraic claims. Preserve the 297 origin split and the 202/263 relationship in the review. The author identifies Sergio Fernández Rubio as the finder and himself as the certificate author. No feasibility or identity replay ran on this host.

22 November 2026. Recovered original GeiserX_exact.zip (1,989,212 bytes, SHA-256 19c069b42d6a6fbe87dd419d358e7b046eadbba20dbaadd7f519faab1152c5e9) and retained it at /Volumes/spud-ext2/agent-evidence/squares-intake-20261121-01a1fb/1037-geiserx-20261122. The seven rational center/direction and corner encodings have identical exact side and square corner sets after the external provenance claim is treated as reported for schema reading. The original files are untouched. Both maintained exact routes accepted 20,301 pairs at 202 and 34,453 at 263, and refused both full-witness mutations for each. The remaining five native case jobs are in progress. Independent mathematical review, algebraic replays, exact report order and drawing decisions are still separate.
