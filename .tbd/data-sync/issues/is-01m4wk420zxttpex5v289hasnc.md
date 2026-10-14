---
type: is
id: is-01m4wk420zxttpex5v289hasnc
title: Keep publication checkout aligned with the atlas provenance receipt
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m4wcjctchxg9qv8jp0za5g13
created_at: 2026-10-14T06:55:42.621Z
updated_at: 2026-10-14T06:55:42.621Z
---
PR591 current183612 Pages green but Packing existingassembled-site-head contract detects publish checkout differsfromoverview afterreceipt inclusion. Publish mustuse sameprecise receipt-bearingcheckout, preserve checkout equality and head verification beforeupload; do notrelaxcontract.
