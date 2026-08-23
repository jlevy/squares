---
type: is
id: is-01m0n6rttj5zdmkgjxb3690bsb
title: "Missing resources: acquire the 11 cited sources not in the archive"
kind: task
status: open
priority: 0
version: 5
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0nrh9mwfjndkzejq34js78c
created_at: 2026-08-22T17:02:23.570Z
updated_at: 2026-08-22T22:12:58.165Z
---
THE CANONICAL LIST IS explorations/packing/frontier/source-availability.yaml
Rendered in the report as a table under 'Source Availability' in
explorations/packing/docs/project/research/research-2026-08-22-packing-11-unit-squares.md

That file is the fact-checking boundary of this research: every claim either traces to a
file in explorations/packing/resources/, or to a row in that list and is marked
[secondary]. Each row carries the obstacle (tested, not assumed), what depends on it, a
priority 1-5, and a realistic route to obtaining it.

STATE 2026-08-22: 11 unretrieved, 5 recovered.

Recovered so far (kept in the file so the correction stays visible):
- Roth-Vaughan 1978 - supplied by the requester; reading it corrected two errors carried
  by BOTH Friedman DS7 and McClenagan (a phantom 10^-100 constant, and the Montgomery
  exponent attribution).
- Markot 2021 - open access at PMC the whole time, never tested.
- Gensane-Ryckelynck 2005 - Springer serves the PDF openly at its /content/pdf/ URL.
- Nagamochi 2005 - open access at E-JC, cited by exact title in DS7's own reference list.
- Wang-Dong-Li 2016 - on arXiv.

Highest-value remaining, by what rests on them:
1. Stromquist 1984 Wagner Associates memoranda I-III (unpublished). Memo III covers
   n <= 65 and Gardner's conjecture; sits behind a large share of the claim column in the
   priority ledger. Route: author or institutional contact.
2. El Moumni 1999, Studia Sci. Math. Hungar. 35 281-290 (print only). Holds published
   priority for s(7)=s(8)=3 and s(15)=4; no summary of the field describes its method.
   Route: library access.
3. Chung-Graham 2009 and 2020 (paywall). 2020 is the O(x^{3/5}) claim McClenagan says
   'has an error in it'; reading it would let us describe the error rather than relay it.

WHY THIS IS P0: the archive's 'not retrievable' verdict has now been wrong five times.
Every recovery so far changed something in the research, and two of them corrected
published secondary sources. A 'not retrievable' entry is a negative search result, not a
fact - RE-TEST THE LIST, do not inherit it. When revisiting, re-run the URL checks first;
the source-availability.yaml header records how.
