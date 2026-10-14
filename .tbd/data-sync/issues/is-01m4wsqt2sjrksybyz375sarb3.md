---
type: is
id: is-01m4wsqt2sjrksybyz375sarb3
title: "Intake 2026-10-14: evaluate every open upper-bound report per count, in report order, and record only the strongest"
kind: epic
status: in_progress
priority: 1
version: 24
delegate: serene-hopper
labels:
  - result-import
dependencies: []
child_order_hints:
  - is-01m4wsratj3p9crt698720cq6f
  - is-01m4wsrbkd61qxbpgxphckpd6v
  - is-01m4wsrcd61weyq0xjpyk4xbqv
  - is-01m4wsrd9g7qg370shbzjs41wr
  - is-01m4wsreb5h5x2ppve9gsy2d32
  - is-01m4wt3k2f29pznyxes56xh69e
  - is-01m4wt4ehr9401mzvgm1n3br4v
  - is-01m4wv278cdppm9155311gb6y5
  - is-01m4wv27yed1e2wfnq55h1avr0
  - is-01m4wv28mebp8r7ss9p8r6dgxy
  - is-01m4wv298hea3eq4fmf0qpvqw1
  - is-01m4x2z8wp9dzqk43j4gxdwr79
  - is-01m4xmr0fhhynbfzj5vj0sh358
  - is-01m4xmr1psrjaabyjsp60ccn67
  - is-01m4xe5txp3t3t4xczs1swedc9
  - is-01m4xpwdwtx923hcd9y50kymez
  - is-01m4xpz6nts8er99w82mh09dnk
  - is-01m4xq50rrk4can2qfvaejajnv
  - is-01m4xq51qnsrbpdpjr6450hs5f
  - is-01m4y1hjs107rt9h7hbztpmbh6
hold: null
hold_until: null
created_at: 2026-10-14T08:51:21.304Z
updated_at: 2026-10-14T20:27:00.250Z
started_at: 2026-10-14T08:51:46.973Z
---
Owner's request in session 0132qkwt8gAB9vM3aQcCJLsQ (branch claude/serene-hopper-xxh80m, off origin/main f73e9de13): review every outstanding GitHub issue for intake; build one per-n ledger across all open reports; at each count, walk the reports in the order they reached the record, and record a report only where it is stronger than the record and every earlier report; a report an earlier, stronger (or equal) report already beats is not recorded unless there is a key reason, which the ledger names; track every item as beads; comment progress on the issues; finish with a summary table of every intake item, recorded or not, and why.

Coordination: the stages 1-3 imports of #521-#596 are held by the 2026-10-14 lanes of think-mq0k (session 01UXZs37jGv5vqVGADH7Gkn8, branches claude/wizardly-meitner-wqn4x3-intake-1014-*). This epic does not retain, register or renumber anything those lanes own: it supplies the ledger's verdicts to them, owns what no bead owns, and posts the progress comments. Message sent to that session 2026-10-14T08:5xZ.

## Notes

Owner decisions, 2026-10-14 ~17:05-17:15Z (verbatim):
- Compute: "Let's, for now, hold off on anything more than 40 CPU-hours but let's be sure we have a clear backlog of validation work that's tracked appropriately, and details are in beads." This replaces the earlier < 4 h delegation threshold. Items above 40 CPU-h are HELD.
- Publication reading (#582), decision 1: "yes though for significant items S4+ we should create an issue ourselves for tracking purposes." Watched-repository publications count from their first commit, the ledger's default. For S4+ results with no issue we open one: #603, Fang's excess theorem (T-163 in #602 after its review renumbering; it was T-178). T-180 has #600.
- Credits: "also be sure we use Ryan Xu real name or surname Xu not the handle for regular credits." This applies to the bibliography credited_names and authors, register prose, and the ledger displays. Identifiers stay as they are (keys, paths, URLs).
