---
type: is
id: is-01m7ps0ksh7rfnhw2m987cpjxk
title: "Soundness review of R-108's clean-room decider (rv1018_bnb.c, rv1018_decide.py) for #1018/T-327, carrying #1027 review A's A3 (ring cuts rounded outward) and A7 (chord allowance's zmax)"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
created_at: 2026-11-18T07:30:20.081Z
updated_at: 2026-11-18T07:30:20.081Z
---
A soundness review of R-108's clean-room branch-and-bound decider for #1018 (T-327), so that its full 401/401 decision (E-de-winter-1018-n108-review-decision, which today sets no rung and is cited by the case records only) could support confirmation as an independently re-implemented route (T-327's next_rung).

The decider: packing/resources/web/de-winter-1018-review-2026-11-18/ (programs rv1018_bnb.c and rv1018_decide.py, frozen at 87e79188b; review docs/project/reviews/review-2026-11-18-de-winter-1018.md, PR #1027).

Points Review A of #1027 (https://github.com/jlevy/squares/pull/1027#issuecomment-6968513664) left for this review:
- A3: rv1018_bnb.c:203-211 put the strips' outer ring cuts at up(a + dn(tau)) and dn(-a - dn(tau)), so the strips run about 1.5 ulp of a (about 8e-17) past the nominal thickness 2 b_u j/m the comment at :177-185 and the review reason with. Sound as used, since delta = 1e-12 (rv1018_decide.py:45) exceeds the frame error 1.1e-16 by four orders, but that is a second use of delta's slack, not the stated argument. State that delta - 2.2 eps_cs covers the over-long strips, or round the cuts inward in a later version.
- A7: rv1018_decide.py:108-109 set zmax = 12.0 and eg = 256 * EPS * (1 + zmax) / min(sf, cf); nothing checks that the rectangle offsets and nodes stay below zmax. The constant holds for offsets up to about 800 and every offset here is below L = 10.63; state the assumption beside the allowance (or check it).

Raised by Review A of #1029 (A7): https://github.com/jlevy/squares/pull/1029#issuecomment-6971992823. Not priced by the triage, so it is not an unfinished confirmation of T-327; it is a candidate for raising T-327's confirmation relation, not a defect in the record.

## Validation
- Claim: R-108's decider decides format M coverage soundly on the declared net (the axis sweep and the rotated branch and bound), including A3's ring cuts and A7's chord allowance.
- Run: a strong-tier soundness review of the frozen programs (reading, plus a re-run of a sample of directions); no new census.
- Cost: an agent review of about two to four hours; compute under one CPU-hour; an estimate.
- Budget status: not started; not priced in the pass.
- Depends on: #1029 merged.
- Done when: the review is merged and, if accepted, T-327's relation and evidence are revisited.
