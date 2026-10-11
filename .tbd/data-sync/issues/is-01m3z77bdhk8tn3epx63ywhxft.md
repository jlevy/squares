---
type: is
id: is-01m3z77bdhk8tn3epx63ywhxft
title: Register s(12) >= 15680000/3949423 = 3.9702002 (this project, lane BB) after an independent review
kind: task
status: closed
priority: 1
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T21:09:49.104Z
updated_at: 2026-10-03T22:39:32.862Z
closed_at: 2026-10-03T22:39:32.862Z
close_reason: "T-079 landed on main via #292 (47569ad50): V3/C3, S3, credit 'Levy after Daniel'."
resolution: null
duplicate_of: null
---
Lane BB (cloud session session_018harhuQFyWjFkbWsNbvPSX, branch claude/lane-bb-s12-improvement, commits 6e56cf0, faf4b37, 803d364, 32cd041) found s(12) >= 15680000/3949423 = 3.9702002 by re-weighting Evan Daniel's 1,736-point certificate (Route B), +0.00108 over squarepacker's #309 (31360/7901); least captured weight 10000045/10^7 at angle net N=96000, verified by Daniel's verifier (producer code for the format). Route A (pure rescaling past #309) gives s(12) >= 1568000/395039, also verified. Both mutation controls refused. Write-up: docs/project/research/research-2026-10-02-s12-beyond-rescaling.md (method, receipts, the least-weight question, attribution). Attribution: Levy, after Evan Daniel's certificate and squarepacker's rescaling (#309); Route B's re-weighting is this project's own step. To finish: (1) a separately prompted blind review of the certificate and the net argument at N=96000 (the lane that found it must not review it); (2) a first-party independent check if one decides the shape (the native parent-core route lane AA used for #309 did); (3) records lane registers it (kind lower-bound, scope [12], novelty apparently-novel, builds_on T-049 is refused for others' results, so cite in claim) with evidence entries carrying performed_by / relationship_to_generator / verifiers; render, re-pin; (4) S-score per epistemics (likely S2-S3: small movement on an open case).

## Notes

2026-10-03 15:45 Registered on #298 (merge 4ff685f8a, re-pin 39e7254c7; dispatched run 37134709863): T-079 s(12) >= 15680000/3949423, V3/C3, S3, apparently-novel, credit 'Levy after Daniel' (builds_on: Daniel, per epistemics: builds_on names only work the certificate rests on directly); squarepacker's rescaling (T-078), which prompted the finer net, is credited in the claim prose. n12 verified lower bound 3.970200. T-078 stays in the reported lane. Owner may prefer 'Levy after Daniel, squarepacker' in the credit line; that would need squarepacker's packet cited as a source_key of a T-079 evidence entry.
