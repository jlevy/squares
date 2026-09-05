---
type: is
id: is-01m1r4qj9k28kw8mpdx50q520y
title: "Two standalone verifiers, minimal_verify.py and verify_claim.py: consolidate or name apart"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m1r4229zbmgsfhw541ya0wjd
created_at: 2026-09-05T06:40:10.035Z
updated_at: 2026-09-05T06:40:10.035Z
---
Owner's question. Today: minimal_verify.py (main; pinned by SHA-256 to the retained 381/100 bytes, cross-checks the record's declared fields, refuses at the first failing check, CPython 3.8, integer arithmetic, 47 s) and verify_claim.py (this branch; unpinned, decides any certificate of the form or one embedded in a claim document, reports every condition, CPython 3.10, Fraction arithmetic, 36 s on 19/5 and about 3 minutes on 381/100; embedded in the claim documents). Recommendation: one standalone verifier, verify_certificate.py, generic and unpinned, that reports every condition, cross-checks the declared fields, prints the SHA-256 of the bytes it read for comparison with the card and sha256sum, reads a certificate out of a claim document, and keeps the integer arithmetic for speed; the card and the claim documents both invoke it; the pin-once test becomes a prints-the-digest test; the two exhaustive test files merge. Cost: merging two reviewed proof-carrying programs needs its own review at maximum effort, and the PR 78 adversarial review's disposition to keep minimal_verify.py pinned is revised by the owner. Awaiting the owner's go-ahead.
