---
type: is
id: is-01m0p6bwq1ate0pkxyq2jp4zxv
title: "PR #5 review F-1: campaign schemas declared enforced but validated by nothing"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m0p6bwcyve6zdv41ezr08e3g
created_at: 2026-08-23T02:14:33.952Z
updated_at: 2026-08-23T02:23:18.951Z
closed_at: 2026-08-23T02:23:18.950Z
close_reason: "FIXED. ledger.py now validates every artifact against its declared schema at load time, failing loud; a declared schema that cannot be loaded is a hard error rather than a silent skip. Negative-controlled: priority 0 (violating minimum 1) now fails both ledger.py --check and the full test.sh, which previously passed it."
---
Verified by negative control: priority: 0 (violating minimum: 1) passed ledger.py --check AND the full test.sh. tools/validate_schemas.py covers frontier/ only; ledger.py checked referential invariants without loading a schema. This is the tacit-validation failure class the repo closed for frontier/ and reintroduced at the moment the campaign became the record of scientific claims. Fix: validate each artifact against its declared schema inside ledger.py load().
