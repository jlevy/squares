---
type: is
id: is-01m5re8ps95t49ek0prw8rjacm
title: "Fix the staged and held house sentences in case records: grammar and which confirmation (review A, A7, of #803)"
kind: task
status: open
priority: 2
version: 2
labels:
  - result-import
  - packing
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-25T02:29:36.169Z
updated_at: 2026-10-25T05:20:48.842Z
---
Review A, A7, of #803 (H1 of think-hx0e): the staged-house and held-house sentences that `adopt_houses` writes into case records are ungrammatical and say "confirmed" without saying which confirmation.

Where: packing/devtools/adopt_houses.py `staged_sentences` (about line 2940) and `held_sentences` (about line 2786). Example at packing/frontier/n-268.md: "T-242's exact side at this count `4.48e-12` below this house, is confirmed here and accepted by the [review of 24 October 2026](...)". The margin has no verb, and stage 4 (packing/campaign/result-import.md, "The exit") asks that a case record's "confirmed" name the confirmation: reproduced with the producer's code, re-implemented sharing named components, or independently re-implemented.

The wording predates #803 and appears 56 times in 46 case records (n-088, n-102, n-123 and others), so #803 does not rewrite it.

Fix: write "... exact side at this count, `4.48e-12` below this house, is confirmed, independently re-implemented, and accepted by ...", taking the kind from the register's confirmation (`verifier_registry.LABELS`, as `Prose.confirmation` does). Then run `python -m devtools.adopt_houses --refresh-openings` or `--refresh` as the docstring says, re-render, and check `adopt_houses --check`, `check_prose_ceremony` and the case-prose checks. Done when every staged and held sentence reads grammatically and names its confirmation.

## Notes

2026-10-25 coord-intake-1024: #803 merged; this template fix is ready to take.
blocked_on: none
