---
type: is
id: is-01m50ey9mm24zk1872jxfyn3a7
title: Normalize News prose, Markdown typography and mathematical notation
kind: bug
status: closed
priority: 1
version: 10
delegate: codex@spud10.local
labels: []
dependencies: []
child_order_hints:
  - is-01m50f9b766c52vrtq1ew2p95j
  - is-01m50fdg13gkf8mszjd06c5asb
  - is-01m50febxgjt75fmvmbfk6r3h6
  - is-01m50fpqk70xdm3m5vsbacpkq1
hold: null
hold_until: null
created_at: 2026-10-15T18:59:37.224Z
updated_at: 2026-10-15T20:08:46.549Z
started_at: 2026-10-15T19:01:01.841Z
closed_at: 2026-10-15T20:08:46.549Z
close_reason: "Delivered in PR623, merge6e73ef1c: independent senior/security reviews clear; matching-head PR CI passed; production Pages38797565374 deployed and exact-commit4480/4480liveauditpassed. Actual livev0.7.10 desktop/mobile reader pages checked. Owner8-itemvisualchecklist is inPRbody. Broader CIperformance/main-deep monitoring remains separate under existing open work."
resolution: null
duplicate_of: null
---
Audit every News/changelog article for overly verbose prose, inconsistent n/N packing notation, literal equations or code formatting used for math, and Markdown typography. Reuse the established site math renderer and shared article styling on News and homepage cards. Preserve scientific claims, author credit, significance/rung caveats, dates, entry IDs, PR membership and delivery evidence. Add focused rendering controls, build and inspect a real preview, independently review and ship. Root owns Git/beads/release integration; renderer and prose writers have disjoint paths.

## Notes

Delivered PR623: merge6e73ef1c2b88fbbd349247b9f86d34fb46a01d4e from reviewed sourcef026be7a892d9909efc418b823ceead7a5c4f0db. Independent Astra seniorA5538976175 and securityB5538977701 clear,27paths covered. Matching-head Packing38796366140 and Pages38796365877 fullygreen. Production Pages38797565374 deployed20:00:25UTC and exact-merge liveaudit4480/4480 passed20:06:43UTC (1101HTTPrequests,0retries). Root actual livev0.7.10 browser verified Newsmath/filters/expand-contract, both tutorialcreditsdates/font410/no markers,390pxwrapping, Aboutorderedlinks/no redundantNewsH1, homepage3S5previews/caveats and60px/40pxH1margins. Eight owner visualchecklist boxes remain intentionallyunchecked inPRbody. Local147integrated,42renderer,111sitecut passed; initial807.26spre-push failed10nodes, allsubsequentlypassedtargeted11controls; failure preserved honestly. PRgate484s, productionthroughverify775s; three-minute goal OPEN underthink-kxmq. Astra recommends existing-plan bounded reader-presentation preflight with truly page-scoped glyphfixtures; no combinedprofile implemented/measured and no selectorfaultestablished. Mainnative38797565375 still watched separately. Durable receipt and localdiagnostics inprimary .codex/regularization-closeout-evidence-2026-10-13/pr623-reader-corrections-20261015.json andpr623-local-reader-checks/. Temporarypreviewserverstopped and90MiBgeneratedbuildremoved afterswitchingtolivesite.
