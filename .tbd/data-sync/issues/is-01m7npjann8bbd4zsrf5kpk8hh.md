---
type: is
id: is-01m7npjann8bbd4zsrf5kpk8hh
title: "Import #1012: public Kaggle packings below the register at n = 109 and n = 270 (pointer); triage, retain at a pinned revision, register as reported"
kind: task
status: in_progress
priority: 1
version: 6
delegate: w4r-records-1118
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-17T21:28:20.405Z
updated_at: 2026-11-18T08:22:09.031Z
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

2026-11-18T03:55Z w4r-records-1118: acknowledgement posted 18 November (https://github.com/jlevy/squares/issues/1012#issuecomment-6967037708) asking for the two Witness/v2 files; JoostdeWinter/square-packing head 838c5ea read the same day holds no 109 file, and its n270/ (a1ba501) is #1022's packing. #1026 (merged 46510a0dc) records it and #1012's blocked: author; the blocked:author label was added after the merge. Stays open: both results queued on the author's files.

## Stage 1 triage of de Winter's comment of 18 Nov (w10-1118, read-only, 2026-11-18T08:40Z)

Worked by lane w10-1118 under the coordinator's brief; the bead's claim (w4r-records-1118) could not be taken over with tbd start (skipped), so the coordinator is asked to reassign it.

Source: jlevy/squares#1012 issuecomment-6972165182 (JoostdeWinter, 07:33:46Z). Pin: the attachment https://github.com/user-attachments/files/35013424/Issue_1012_n109_Kodaj_Coordinates.zip, 42,790 bytes, SHA-256 b0134067b9093947fa0a86dd47458bac13b41a9ed54c77f834f93741c8d64db1, retrieved 2026-11-18T08:18:13Z over a direct connection (the session proxy answers user-attachments with 403; muglich-issue686 precedent). Members (zip times 08:09-08:12 local, i.e. before the comment): README.txt 3,298 B f9296ea85059cb3b7edbbe9f70d49f54088931f47e62d3a6ef8e160d69041ea2; n109_tomkodaj.csv 7,095 B c4f76a5a0dcf6055da754bc35a8ea23abb832109b4d0dc4c534924f47b631e8b; n109_tomkodaj.yaml 183,871 B 56b4655fada7dfd5d54c1483b021d5b700ecb5c41beba2865a6a8ef7e223b3fb; verification.txt 190 B d9647ac120a2bfeaac88dc12f48ea60c8fddb451cd855ff007b94aec20ac38d4. Treated as untrusted data in its own scratch directory; nothing in it was run.

Claims: (1) s(109) <= 547464479047171949843/50000000000000000000 = 10.94928958094343899686, rounded up 10.949289580944; the issue's 10.949289580943 was rounded to nearest (below the exact side, so it bounds nothing). A Witness/v2 corners file, rational, 109 squares, transcribed by de Winter from the 109 rows of Tomas Kodaj's Kaggle dataset 'Squares in Squares: strips and bands (coordinates)' v2 (13 Nov 2026, CC0 by Kaggle's listing, per README.txt), tan(angle/2) rounded at 28 places, centres translated. (2) verification.txt: this repository's check_rational_witness_independent at f9ddfeeef reports VERIFIED, 109 squares, 5,886 pairs, min pair gap ~2e-15. (3) The full submission.csv's SHA-256 7700b20d7c901a831741d0dbabae0941fefe460381cc18d969ec29aa728e489b (not checkable: Kaggle unreachable here). (4) At 270 the author withdraws: his #1022 (16.927314216352) is below both Kaggle sides.

Read-only check here (own script, python -I, file passed as argument): 109 squares, every edge exactly of length 1, every corner inside [0, side]^2; the CSV centres equal the witness centres translated by (5.474644790471717, 5.474644790471717) within 8.9e-16.

Comparison with main 50962004c at 109: the house is the Kingbird packing, reported 6 + (7/2)sqrt 2 = 10.94974746830583, verified 10.949747468305832670915408009418 (T-101, T-155). The new side is 4.579e-04 below it. No register entry or open report states an upper bound at 109 below the house; #1018 (PR #1029) is a lower bound at 108/109 and does not interact. Samanyu-dev/squares_in_squares 53551d7 (2026-11-07T20:20:31Z, best_fit_101_500.csv) holds a 109 pinwheel at binary64 side 10.94928958094538, recorded on #958 as context only (not a report, repository not watched); this side is 1.94e-12 below it. Guilherme Dias da Fonseca published a 109 pinwheel at 10.949392392 on Kaggle on 6 Nov 2026 (discussion 756468; notebook gfonsecabr/a-packing-of-109-squares-that-beats-gobel-s; not readable here).

Map: a bound the record does not hold -> a new upper-bound entry at 109 (stage 3), reported lane at 109; once validated (stage 4) the house rule adopts it and it is regularized in the PR that makes it the house (stage 5). n270-kaggle: not registered, withdrawn by the author (queued false), no certificate ever arrived.

Credit (proposal, to settle at stage 3 after measuring identity): the certificate's source is Kodaj's CC0 dataset (README.txt: Kodaj publishes the coordinates and refers readers to his source notebooks for the original credits; he claims no finding). Navneet Prabhat's compilation holds the same packing (~10.94928958094337 by de Winter's reading) but is not the certificate's source and is not readable here. By the Tymchishin 22-3662 precedent (a union notebook credited to its author, its construction credits left to the notebook), credit Kodaj as the publisher of the coordinates the certificate transcribes, with de Winter as the reporter of the exact transcription, and state the earlier publications by date beside it (epistemics.md, Priority is stated): Fonseca's pinwheel of 6 Nov (10.949392392) and Samanyu-dev's merged 109 of 7 Nov (10.94928958094538). No 'after' names unless a retained source states the lineage; measure_identity against Samanyu-dev's 53551d7 109 (and contraction_margin of it, option D) is a measurement for the record, deciding nothing about credit. OWNER QUESTION if the measurement shows Kodaj's 109 is Samanyu-dev's packing to ~1e-12: is the result Kodaj's (the first exact-certifiable publication) or Samanyu-dev's/an unidentified leaderboard author's, and does Prabhat share it?

Price: both maintained exact routes on one 109-square witness, minutes; sharp controls (plan hashed first); measure_identity vs the house and vs Samanyu-dev's 53551d7 109; contraction_margin; then a blind stage 4 review; adoption and both strong regularizers at 109 (house rule), each minutes to an hour. Far under the 40 CPU-h cap.

Disposition: stages 2-3 on branch claude/keen-galileo-9gbz1a after think-a88h's PR merges; read_through moves to 2026-11-18T07:33:46Z; blocked:author lifts (files arrived) after the merge of that change.
