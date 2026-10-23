---
type: is
id: is-01m4wc2p7mrk13jr7nkjgm3nvh
title: "Import mstrmg (Miles Gray): s(381) <= 19.985624661051481, beyond the case corpus (#582)"
kind: task
status: open
priority: 2
version: 7
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: blocked
hold_until: null
created_at: 2026-10-14T04:52:37.747Z
updated_at: 2026-10-23T06:16:13.890Z
started_at: 2026-10-14T04:52:50.738Z
---
Miles Gray (GitHub mstrmg) reports s(381) <= 19985624661051481/10^15 in an exact rational certificate attached to issue #582 (n381-19.985624661051.cert.txt, SHA-256 03650573fc283abe721947d0170d833b3725a6550d4e8a9283c41f10c4a371f4); #589 is the same request, closed as its duplicate. Stages 1, 2 and the stage 4 replay of the 2026-10-14 intake lane couzo (think-mq0k), on branch claude/wizardly-meitner-wqn4x3-intake-1014-couzo.

## Notes

GitHub issue: https://github.com/jlevy/squares/issues/582 (Miles Gray, GitHub mstrmg; filed 2026-10-13T11:38:11Z, `intake` label 2026-10-14T04:38Z). #589 (2026-10-13T20:59:50Z) is the same body with the same attachment URL, closed as completed 20 seconds later; it adds nothing. Read 2026-10-14T04:49Z: no comments and no body edits on either.

## Stage 1: triage

**Source.** No repository: mstrmg has no public repositories. The certificate is the issue attachment https://github.com/user-attachments/files/33382828/n381-19.985624661051.cert.txt (36,167 bytes, 382 lines), downloaded 2026-10-14T04:49Z; its SHA-256, 03650573fc283abe721947d0170d833b3725a6550d4e8a9283c41f10c4a371f4, is the digest the issue states. Evan Daniel's format: header `381 19985624661051481/1000000000000000`, then 381 `x y t` rows. The importer's evand-cert adapter reads it, 381 poses, and admits it at the printed side 19.985624661051481 (an exact terminating decimal). A picture is attached (not fetched). No licence is stated.

**Claims.** One: s(381) <= 19985624661051481/10^15 = 19.985624661051481, beyond the n <= 324 case corpus, for the beyond-horizon list. The source states three exact-Fraction checks (two of the author's, written with Claude's help, sharing a sqrt(2) centre-distance prefilter; and this repository's sqpack verify_packing from main on 2026-10-13 with the full quadratic sweep, 72,390 pairs); Evan Daniel's verify_cert.py was not run.

**Map to the register.** A beyond-horizon row at 381 only; no case record and no T-NNN.

**Who else holds 381** (exact sides): Couzo's #506 row (couzo-certificates-2026-10-11, T-152's packet) 19.992663288464, which #582 is below by 7.04e-3; the grid 20, below by 1.44e-2. But Couzo's #583 certificate at 4596670 (unchanged at b85dee2, packet couzo-certificates-2026-10-13) is 19.974977397657, below #582 by 1.065e-2, and Kevin Fang's TheSnakeFang/squarepack-certs n0381 at e646c47 (2026-10-12T19:06Z, before #582 was filed; no issue, not in the register) is 19.976969740406, below #582 by 8.65e-3. #582 is the third smallest known at 381; its row would be tracked and superseded on arrival.

**Credit and AI.** The source credits the starting packings: Evan Daniel's Hunt 3 343 (#489) and Kevin Fang's 343/344 (#484), grown by a row and a column and optimised, with a block layout after Arslanov et al. 2021. The search program and the report were written with Claude (Claude Code); the author ran the search and reviewed the result.

**Priced validation plan.** The replay itself is small: three jobs on the two maintained exact routes, about 3 to 5 minutes with one worker (#506's 381 jobs took 6 minutes on a loaded machine). It is blocked on custody, not compute: devtools.acquire_source writes and checks packets only from a Git checkout, and upper_bound_reports admits only such packets and refuses a declaration that requests no count at or below 324. Retaining an issue attachment and importing a beyond-horizon-only report is a W7 slice: an attachment source in acquire_source (pinned by the issue's stated SHA-256 and its posting time) and a beyond-horizon-only declaration in upper_bound_reports whose register plan writes no results.yaml entry, about 2 to 3 hours with tests. Evan Daniel's #584 (339, 364, 375, all beyond 324) needs the second half too. Not done in lane couzo on 2026-10-14; recorded for the coordinator.

## Draft acknowledgement (not posted)

Thank you, Miles. We have received #582 (and closed #589 as its duplicate) and downloaded the attached certificate; its SHA-256 is the 03650573... you state, and it reads as 381 unit squares in a square of side 19985624661051481/10^15. That side is below the row the register tracks at 381 (Francisco Couzo's #506 certificate, 19.992663288464). Two smaller certificates were published at 381 before or shortly after your report: Kevin Fang's 19.976969740406 in TheSnakeFang/squarepack-certs (12 October) and Francisco Couzo's 19.974977397657 (#583, 13 October). We will record your certificate with its credit to Evan Daniel's and Kevin Fang's 343 packings, replay it on this repository's two exact routes once our importer can retain an issue attachment, and reply with the result.

## Lane couzo, resumed after the container restart (2026-10-14T06:45Z)

Not imported here. The custody and beyond-horizon-only tooling priced above (an attachment source in acquire_source and a beyond-horizon-only declaration in upper_bound_reports, about 2 to 3 hours with tests, W7) was not built, and the certificate was not replayed: #582 is not the smallest known at 381, so it is not one of the quick new-best results this pass lands first. Its comparison is frozen in packing/resources/web/couzo-certificates-2026-10-13/acquisition/claims.json (branch claude/wizardly-meitner-wqn4x3-intake-1014-couzo): Couzo's #583 certificate, exact side 19974977397656713743580918961689/10^30 (19.974977397657 rounded up), is below #582's 19.985624661051481 by 1.06e-2, and Kevin Fang's 078789a print 19.976969740406 is below it by 8.65e-3; Couzo's #506 row (19.992663288464) and the grid are above it. On import its beyond-horizon row would be tracked and superseded on arrival. Hold: blocked on the W7 slice.

## Reply posted (2026-10-14)

Replaces the draft above: thanks mstrmg, states that Couzo's #583 certificate at 381 (19.974977397657) is 1.06e-2 below #582's 19.985624661051481 and has been retained and replayed, so the record will carry Couzo's; #582 is not imported for now; further improvements are best sent as a new issue with an exact certificate in a repository.

- #582: https://github.com/jlevy/squares/issues/582#issuecomment-6163324766

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): #582 not recorded: Kevin Fang's 381 (12 October) is earlier and smaller; close at merge.
