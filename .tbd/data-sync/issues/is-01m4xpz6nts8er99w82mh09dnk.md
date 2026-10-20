---
type: is
id: is-01m4xpz6nts8er99w82mh09dnk
title: "Validation backlog (owner cap 2026-10-14: hold anything > 40 CPU-h)"
kind: task
status: open
priority: 1
version: 2
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
created_at: 2026-10-14T17:22:12.281Z
updated_at: 2026-10-15T19:58:09.552Z
---
The validation backlog of the 2026-10-14 intake (epic think-abi1), after the owner's instruction of 2026-10-14 ~17:05Z: "Let's, for now, hold off on anything more than 40 CPU-hours but let's be sure we have a clear backlog of validation work that's tracked appropriately, and details are in beads."

Each row's bead carries a `## Validation` block (claim, run, cost and basis, budget status, a proposed subset for held items, dependencies, done-when, machine note). The cap is applied per item: an item above 40 CPU-h is HELD, and a held item's subset is a proposal that runs only on the owner's word. Statuses: running, runnable, gated on decision (an owner decision or a code slice must land first; the item is within the cap), held. Dependencies between rows are tbd dependencies only where an ordering is real (think-567s on think-4uun; think-wu73 on think-au7j).

## This epic's items

| Bead | Item | CPU-h | Status | Depends on |
| --- | --- | --- | --- | --- |
| think-9zd2 | Fang's 11 direct certificates, 421 to 814 (under think-7bw3) | 3.02 | running (serene-hopper, squares-wt/fang-certs) | - |
| think-v511 | wand125 s(145) >= 306/25, linear replay of 201 angles and control (under think-u0av; T-179) | ~37 (24-64) | runnable, with a stop at 40 | preparation: register in audit_wand125_linear, retain candidate.json and certificate.json |
| think-j7f1 | Mishapolk 70a033f, 24 certificates, and 207 decided exactly (under think-o644) | ~0.8 (to 1.2) | runnable | think-o644's stage 1-2 packet |
| think-au7j | Closed form: replay4d build and calibration on the two smallest records (under think-tsox; T-180) | ~1 | runnable | crates.io and toolchain access |
| think-4wgw | Closed form at 1c661b7: replay4d 0.1.1's source hashes and structure.json's digest (under think-tsox) | <0.1 | runnable | - |
| think-abjj | The ledger's 21 undecided PR #574 comparisons, exact | <0.1 (unmeasured) | runnable for 17; gated for 4 | the 4 at 29, 55, 71, 83 lack an exact side of the reported lane |
| think-w76a | wand125 s(37) >= 2599/400, census of 2,073 directions with whole-net controls (under think-u0av; T-177) | 6.53 (7.49) | gated on decision | owner, jlevy/squares#543: retain the check2 candidates where the census reads them |
| think-ec27 | wand125 s(44) >= 2799/400, census with controls (under think-u0av; T-176) | 16.95 (19.94) | gated on decision | #543 retention |
| think-567s | wand125 s(39) >= 533/80, census with controls (under think-u0av; T-175) | 7.09 (7.50) | gated on decision | #543 retention; think-4uun |
| think-4uun | AXIS_ROUNDING: judge the axis refusal against the sweep's enclosure (#543, option 2) | ~1 CPU-s a certificate, plus a reviewer | gated on decision | owner's option on #543; code change and review |
| think-5klg | Fang's six rectangles in both dimensions on a maintained route (under think-0esw; #603) | <0.02 once written | gated on decision (W7 code) | a rectangle-container route (no bead yet) |
| think-wu73 | Closed form: complete replay4d replay of 136 records (under think-tsox) | 4,294 (source, uncalibrated) | held | think-au7j; owner budget |
| think-o4kf | cfcheck: intervals 1 and 34 in full, 8 records (under think-3n1x; #600) | 320-650 | held | owner budget |
| think-pvov | Fang's 70 unreplayed theorem/ certificates (under think-0esw; #603) | 99.2 certify (198 with replay); <1 on a W7 bucketed route | held | retention (OR-18); the W7 bucketed route for the 44 above 1,263 squares (no bead yet) |
| think-yeq9 | Fang's 38 shipped composites (under think-rn2y; #603) | 61.2 certify, 122.3 with replay | held | retention; W7 route for 28 of 38 |
| think-dyyu | Fang's 53 table-only composites, regenerated then replayed (under think-rn2y; #603) | 59.4 certify, 118.9 with replay, plus regeneration (unmeasured) | held | regeneration route; W7 route for 28 of 53 |

## Owned by think-mq0k (session wizardly-meitner), referenced and not edited here

| Bead | Item | CPU-h | Status | Depends on |
| --- | --- | --- | --- | --- |
| think-9v2k | PR #574 (T-174 after #602): check --replay of the remaining counts, in chunks of 75 minutes or less | not stated now (the bead's earlier price: 32 rational counts ~1.5, 57 algebraic ~2.2 on route 1) | running | - |
| think-2ep3 | #593: the other 69 declared counts | ~2.5-4.2 (75-125 min certify, as much replay) | runnable; optional (recorded only at 237) | - |
| think-2zz8 | #573: the other 15 counts | ~0.6-1.0 (18-31 min certify, as much replay) | runnable; optional (none recorded beyond T-172's 153 and 207, already replayed) | - |
| think-k8z2 | #582's s(381), 3 jobs | ~0.1 | gated on decision (custody tooling for an attachment, W7); optional (not recorded) | - |

## Totals

- Running: 3.02 CPU-h here, plus PR #574's chunks in think-mq0k.
- Runnable now, with no decision outstanding: about 39 CPU-h (think-v511 ~37, think-au7j ~1, think-j7f1 ~0.8, think-4wgw and think-abjj under 0.1 each); plus 3.2-5.3 CPU-h of optional think-mq0k items. think-v511's high estimate (64) is why it carries a stop at 40.
- Gated on a decision, each within the cap: 30.6 CPU-h (s(37) 6.53, s(39) 7.09, s(44) 16.95); think-4uun and think-5klg are seconds once their code lands.
- Held (> 40 CPU-h): about 4,830 CPU-h on certify-only figures and the low cfcheck price (4,294 + 320 + 99.2 + 61.2 + 59.4), about 5,380 CPU-h with check --replay and the high cfcheck price (4,294 + 650 + 198.4 + 122.3 + 118.9), plus the unmeasured regeneration of the 53 table-only composites. A W7 bucketed exact route would bring think-pvov under 1 CPU-h, and most of think-yeq9 and think-dyyu within reach.
- Read cumulatively rather than per item, the runnable set alone is about 39 CPU-h; adding the gated set would pass 40, which is the owner's call.

## Machine

4 CPUs shared with gates. Runs over 2 wall-hours (think-9zd2, think-v511, think-w76a, think-567s, think-ec27, and every held item) are scheduled outside a validation gate.

## Not established from the record

- think-dyyu: the regeneration cost of the 53 table-only composites (reproduce.sh or a first-party rebuild) is unmeasured.
- think-abjj: the exact comparisons are unmeasured (expected seconds); at 29, 55, 71 and 83 the record has no exact form of the reported lane's side, so those four cannot be decided from it.
- think-wu73: 4,294 CPU-h is the source's own receipt, uncalibrated here until think-au7j runs.
- think-9v2k: the remaining CPU of PR #574's check --replay chunks is not stated in the bead.
- The W7 bucketed exact route and the rectangle-container route, on which think-pvov, think-yeq9, think-dyyu and think-5klg depend, have no bead.

## Notes

2026-10-15, evening intake pass (think-wnsv), lane D (think-ykg6): the sweep read the table's "held" rows as waits on think-au7j and think-9zd2, both closed on 2026-10-14 with #605 (77fa15c7e). Their rows are done: think-9zd2 replayed Fang's 11 direct certificates on both routes (1.54 CPU-h, all controls refused); think-au7j built replay4d and calibrated it at 1.22x the source's CPU, so think-wu73's complete replay is about 5,250 CPU-h here and its interval-24 subset about 22.4 CPU-h (think-wu73's notes). think-4wgw and think-abjj closed too: abjj decided 17 of the 21 PR #574 comparisons, and 29, 55, 71 and 83 stay gated, 29 on sigma, Daniel's degree-7213 root (think-6gti; #622's N29 certificate, think-30n2, waits on the same). This bead is the backlog's ledger and waits on nothing itself; its open rows wait on the owner's budget or decisions, as the table says.

blocked_on: none
