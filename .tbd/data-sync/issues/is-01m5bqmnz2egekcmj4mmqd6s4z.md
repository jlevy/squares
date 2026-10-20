---
type: is
id: is-01m5bqmnz2egekcmj4mmqd6s4z
title: "Owner decision on the #673 credit consequences: Kevin Fang's structured and poster credit at 308, Chaoweeraprasit's finder change at 236"
kind: task
status: open
priority: 2
version: 2
labels:
  - result-import
  - owner-decision
dependencies: []
created_at: 2026-10-20T04:03:18.113Z
updated_at: 2026-10-20T17:09:56.360Z
---
Owner decisions the #673 credit correction raises in PR #692 (review A3, senior; review B1, correctness). PR #692 follows epistemics.md's rule that the source says who did what: at 146 and 308 Evan Daniel becomes the finder, as the author's #673 asks, and at 236 the issue's credit of #481 for the construction is read as "based on", so Daniel is also the finder there.

1. **308, Kevin Fang.** #673 asks for "found_by: Evan Daniel, based on Kevin Fang (#484)", which is an acknowledgement. The case frontmatter has no based-on or construction field. After the PR, Fang survives only in the credit sentence (`adopt_houses.CREDITS[308]`), in prose and in a historical claim line (packing/frontier/n-308.md:88). The poster's "Best packings due to ..." line drops him (26 names become 25; packing/tests/test_known_best_atlas.py:2158-2160) the next time the posters are redrawn. Fang was not consulted. The 19 October reply on #673 says the credit decision is queued.
2. **236, Nate Chaoweeraprasit (itsnaka).** T-218 is measured as another arrangement of #481's design, with 226 of 236 squares within a tenth. The PR moves the finder from Chaoweeraprasit to Daniel. Its #673 row names only 146 and 308.

Owner default, as of 20 October 2026: keep the PR's change. Daniel is the finder, and Fang (and Chaoweeraprasit at 236) appear in the credit sentence. No code change.

Options: (a) keep the default and say in the #673 reply that the poster's omission is intended; (b) add a structured based-on or construction credit that the poster reads, so no name a source asks to have acknowledged leaves the poster's list.

Done when the owner chooses. Under (b), the change lands in its own PR. Under (a), the #673 reply (think-gzvu's Stage 7 answer) states the omission.

## Notes

2026-10-20 (coordinator): #692 (012dcf9e5) shipped the default: Fang is in no structured credit field and leaves the posters' credited-names list at 308; Chaoweeraprasit's finder change at 236 kept as #692 landed it. #673 closed with final reply 6294849401 stating that outcome (recorded by #698). Left open for the owner to confirm or reverse; reversing needs a records PR and a follow-up on #673.
