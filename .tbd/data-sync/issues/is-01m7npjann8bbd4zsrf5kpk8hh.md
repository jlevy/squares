---
type: is
id: is-01m7npjann8bbd4zsrf5kpk8hh
title: "Import #1012: public Kaggle packings below the register at n = 109 and n = 270 (pointer); triage, retain at a pinned revision, register as reported"
kind: task
status: in_progress
priority: 1
version: 3
delegate: w4-records-1117r
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-17T21:28:20.405Z
updated_at: 2026-11-17T22:06:06.683Z
started_at: 2026-11-17T21:29:36.291Z
---

## Notes

## Stage 1 triage (2026-11-17, w4-records-1117r, read-only)

Source: jlevy/squares#1012 (JoostdeWinter, 2026-11-17T07:08:47Z, no comments, body unedited). It points to three public Kaggle notebooks (Apache 2.0 by the issue's word): navneetprabhat/squares-in-squares-compilation-by-instinct and tomkodaj/squares-in-squares-22-1636 (n = 109, side 10.949289580943) and malyshevdanil/squares-in-squares-living-atlas-of-tight-packings and tomkodaj/squares-in-squares-22-1636 (n = 270, 16.927469593519 Malyshev, 16.927469594094 Kodaj). It asks that the notebooks' authors be credited (Prabhat and Kodaj at 109, Malyshev and Kodaj at 270), claims no credit, and says exact rational Witness/v2 versions of the float64 Kaggle coordinates are attached.

Pin: none possible. The issue body (gh api, 1,187 bytes) holds no attachment, only the four notebook links; JoostdeWinter/square-packing's head d02237a (2026-11-16T21:26:39Z, the 262/295 registration) holds no Kaggle witness. Kaggle: www.kaggle.com answered this session's plain curl for the notebook page with HTTP/2 404 and content-length 0 (through the session proxy, 21:39Z); a retry with a browser user agent was refused by the session's permission check and not attempted again; the submission.csv files need a Kaggle login the session does not have. So the source is NOT CHECKED: no packing, no certificate, nothing retained.

Claim map: n109-kaggle, s(109) <= 10.949289580943, 4.58e-4 below the house 10.94974746830584 (T-101's exact certificate of the Kingbird packing; reported lane Kingbird 10.94974746830583); n270-kaggle, s(270) <= 16.927469593519, 6.79e-4 below the house T-283 (Ozden, 16.9281486033428544), also below #1009's refinement 16.928148603340 (lane w3, think-i38n, not on main yet). Kodaj's 270 side was quoted on #1001 too, recorded there as context only (n270-kodaj-quoted). Register action once a certificate arrives: a new upper-bound entry per count, credited to the notebooks' authors (finders) with de Winter as the reporter of the exact conversion, under the report-order ledger at 270 (after #1009's walk).

Price: nothing to run until a certificate exists; then both maintained exact routes, about minutes per count, plus sharp controls and a stage 4 review.

Disposition: result-requests.yaml #1012 entry, triage done, both results queued: true on this bead, answer bead this bead. Intake label added on GitHub (21:38Z); no case label applies (neither count has a tracker or an optimality claim).
blocked_on: jlevy/squares#1012 (the author's exact Witness/v2 files, which only he can attach or commit)

Draft acknowledgement (post after the records PR merges, from main with check_requests --draft 1012, edited to the house style):
Thank you for the pointer. The issue says the exact rational Witness/v2 files are attached, but none came through: the issue holds only the links to the three notebooks, and their submission files need a Kaggle login, which this project's sessions do not have, so nothing could be retained or checked yet. Could you attach the two Witness/v2 files to this issue, or commit them to JoostdeWinter/square-packing? Once a file is here, it is retained at that revision, replayed on both of the project's exact routes, compared with the record at 109 and 270 (and at 270 with your #1009 refinement), and registered as reported with the credit you ask for: Navneet Prabhat and Tomas Kodaj at 109, Danil Malyshev and Tomas Kodaj at 270.
