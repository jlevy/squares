---
type: is
id: is-01m4wk420zxttpex5v289hasnc
title: Keep publication checkout aligned with the atlas provenance receipt
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wcjctchxg9qv8jp0za5g13
hold: null
hold_until: null
created_at: 2026-10-14T06:55:42.621Z
updated_at: 2026-10-14T07:21:25.616Z
started_at: 2026-10-14T06:57:10.888Z
closed_at: 2026-10-14T07:21:25.616Z
close_reason: Fixed, independently reviewed, and merged in regularization stack main9f48ccc80cee8dcf94c7cadbcaded01408f94fa2; exact-head Packing and Pages CI pass. Deployment tracked by parent think-azzv.
resolution: null
duplicate_of: null
---
PR591 current183612 Pages green but Packing existingassembled-site-head contract detects publish checkout differsfromoverview afterreceipt inclusion. Publish mustuse sameprecise receipt-bearingcheckout, preserve checkout equality and head verification beforeupload; do notrelaxcontract.
