---
type: is
id: is-01m5mq8gnh3nf40y8nr1hpfyrh
title: Keep local-minimality evidence cited past a 30-day deferral (check_certificate_citations)
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T15:49:49.361Z
updated_at: 2026-10-23T15:49:49.361Z
---
Review A, finding A4, of PR #751 (https://github.com/jlevy/squares/pull/751#issuecomment-6368595518). devtools.check_certificate_citations' orphaned_evidence counts a verified certificate as cited only by a case record's packing block, method-limit evidence or beyond-horizon evidence; a result's evidence list does not count. The grade-C run's evidence entries (drafted in think-7scz: E-evand-gradec-local-minima-233-review-check and E-evand-gradec-n10-recompute) bear on no bound and no case record has a block for local minimality, so on registration they can enter only under a deferral in packing/devtools/certificate-citation-deferrals.yaml naming the register entry, which expires 30 days after the evidence register's last_reviewed. Choose and build one durable citing record: a rule beside method_limit_evidence for evidence that a registered result of a structural kind (restricted-optimality, derived-structure) cites and that claims no bound, or a case-record block for local minimality. Waits on: the grade-C claim's registration (a T-NNN) and a records design decision.
