---
type: is
id: is-01m1tkdwn7e13kfqcqwn9chwq2
title: "Independence wording: 'third-party check' and 'share no code' overstate what is shared (F7)"
kind: bug
status: closed
priority: 1
version: 3
labels:
  - review-gpt6
dependencies: []
parent_id: is-01m1tkdspk8c3n71xsc2e2t4g7
created_at: 2026-09-06T05:35:30.470Z
updated_at: 2026-09-06T06:21:09.292Z
closed_at: 2026-09-06T06:21:09.292Z
close_reason: "Implemented in 41fb401a on claude/pdf-paper-small-fixes (PR #92); reviewed by the coordinator; CI green"
resolution: null
duplicate_of: null
---
Finding 7, confirmed. (a) explainer-article.md:479 calls the thirdparty package 'a self-contained third-party check'; its README (thirdparty/README.md:1,11) says it is a package for third-party checking and 'not itself a third-party check'. Also note there that it checks the 19/5 certificate, not the headline 381/100. (b) verifiable_claim.md (rendered line ~162) says the two other routes 'share no code with it or with each other'; interval.py:92 imports Certificate from certificate.py, and the retention gate constructs and supplies that shared representation. Fix: 'first-party package for third-party checking'; state which components are shared (the certificate representation and loader) and which differ (event-cell sweep vs interval branch-and-bound). Different algorithms are not independent implementations, independent input handling, or validation by a separate party. Regenerate the explainer and both claim documents.
