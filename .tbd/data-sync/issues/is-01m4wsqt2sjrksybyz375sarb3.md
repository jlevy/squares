---
type: is
id: is-01m4wsqt2sjrksybyz375sarb3
title: "Intake 2026-10-14: evaluate every open upper-bound report per count, in report order, and record only the strongest"
kind: epic
status: open
priority: 1
version: 30
delegate: null
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
  - is-01m4ycpqezk8hdbpr0h7x5d8f2
hold: null
hold_until: null
created_at: 2026-10-14T08:51:21.304Z
updated_at: 2026-10-23T06:16:24.320Z
started_at: 2026-10-14T08:51:46.973Z
---
Owner's request in session 0132qkwt8gAB9vM3aQcCJLsQ (branch claude/serene-hopper-xxh80m, off origin/main f73e9de13): review every outstanding GitHub issue for intake; build one per-n ledger across all open reports; at each count, walk the reports in the order they reached the record, and record a report only where it is stronger than the record and every earlier report; a report an earlier, stronger (or equal) report already beats is not recorded unless there is a key reason, which the ledger names; track every item as beads; comment progress on the issues; finish with a summary table of every intake item, recorded or not, and why.

Coordination: the stages 1-3 imports of #521-#596 are held by the 2026-10-14 lanes of think-mq0k (session 01UXZs37jGv5vqVGADH7Gkn8, branches claude/wizardly-meitner-wqn4x3-intake-1014-*). This epic does not retain, register or renumber anything those lanes own: it supplies the ledger's verdicts to them, owns what no bead owns, and posts the progress comments. Message sent to that session 2026-10-14T08:5xZ.

## Notes

Owner decisions, 2026-10-14 ~17:05-17:15Z (verbatim):
- Compute: "Let's, for now, hold off on anything more than 40 CPU-hours but let's be sure we have a clear backlog of validation work that's tracked appropriately, and details are in beads." This replaces the earlier < 4 h delegation threshold. Items above 40 CPU-h are HELD.
- Publication reading (#582), decision 1: "yes though for significant items S4+ we should create an issue ourselves for tracking purposes." Watched-repository publications count from their first commit, the ledger's default. For S4+ results with no issue we open one: #603, Fang's excess theorem (T-163 in #602 after its review renumbering; it was T-178). T-180 has #600.
- Credits: "also be sure we use Ryan Xu real name or surname Xu not the handle for regular credits." This applies to the bibliography credited_names and authors, register prose, and the ledger displays. Identifiers stay as they are (keys, paths, URLs).

2026-10-16 ~05:25Z, overnight coordinator user-eb (epic think-hg5s): ownership transferred to user-eb-intake-residue (bead think-mu5v) from serene-hopper (last update 2026-10-14T23:42:03.230Z), because the sweep of 05:08Z reports this bead's blocker resolved and the owner asked tonight for the intake to continue. The lane resumes the work, closes the bead if it is done, or rewrites blocked_on.

2026-10-16 ~06:05Z user-eb-intake-residue (lane A, think-mu5v): resumed after the sweep of 05:08Z read #596 (closed 2026-10-16T03:45:54Z with its final reply) as this bead's wait. That was a misreading: the description's sentence 'the stages 1-3 imports of #521-#596 are held by the 2026-10-14 lanes of think-mq0k' is coordination, not a wait. This epic's own deliverables are done and closed: the ledger tool (think-giaf), its input (think-dgj1), the rendered ledger and summary (think-a30g), the verdict comments (think-prkx), the survey (think-fxs7), the 21 undecided #574 comparisons (think-abjj) and the records follow-up (think-3aum). It stays open as the parent of 14 open children, each with its own owner: think-7bw3, think-u0av, think-tsox, think-o644, think-lh7d, think-dquu, think-ts16, think-0esw, think-5pn5, think-3n1x, think-4uun, think-rn2y, think-1qc5, think-5p0y. Close it when the last of them closes; the line below makes the sweep report that moment. No record names this bead as a deferral (only a YAML comment in intake-watch.yaml).
blocked_on: think-7bw3, think-u0av, think-tsox, think-o644, think-lh7d, think-dquu, think-ts16, think-0esw, think-5pn5, think-3n1x, think-4uun, think-rn2y, think-1qc5, think-5p0y

Correction (user-eb-intake-residue, 2026-10-16T05:47Z by date -u): the '~06:xxZ' times in this lane's notes of 16 October are about an hour late; they were written between 05:30Z and 05:47Z. The site pages were read at about 05:35Z. No condition changes: every last reply named is still more than a day old.
