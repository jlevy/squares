---
type: is
id: is-01m5kt2xqt4dzbmcdy5qd8cr6j
title: "Decision: register kind for chelokot's and Daniel's Lean proofs of s(2) to s(5) (think-7l2j)"
kind: task
status: open
priority: 2
version: 2
labels:
  - decision
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T07:19:57.434Z
updated_at: 2026-10-23T09:04:30.628Z
---
Owner decision for think-7l2j, raised by the intake lane c-lean-1023 on 23 October 2026. The lane retained both sources (packing/resources/web/chelokot-small-n-lean-2026-09-05/ and evand-rect-small-n-lean-2026-10-22/) and their reported evidence entries (E-small-n-chelokot-lean-report, E-small-n-daniel-rect-lean-report), and held back the register entry (id T-237, allocated to the lane) because the record's rules give it no kind the checks accept:

- **Formalization** is what epistemics.md, Result Kinds, says: a proof in a proof assistant of a result the record already holds, and the case records n-002 to n-005 hold s(2) = s(3) = s(4) = 2 and s(5) = 2 + sqrt 2 / 2 as proved (s(5) by E-n005-gobel-proof). But `devtools.check_results` requires a formalization's claim to name the registered result it formalizes, on a case they share, and no register entry holds s(2) to s(5) (T-012 and T-014 are rigidity results at n = 5, T-124 restricted optimality at 2 to 4).
- **Optimality** is what the first rule gives a proof of a value the record does not hold. Registered so, with the case records unchanged, `devtools.check_standing` derives the entry superseded, since no case bound cites its evidence, and refuses it, since it equals the case bounds.

Options:
1. Register the published proofs first (Goebel 1979 for s(5), Friedman DS7 for the lower bounds at 2 to 4, or one entry for the four classical values), then the Lean proofs as a formalization naming it. Two ids.
2. Register the Lean proofs as optimality and cite their evidence in the reported lanes of n-002 to n-005, beside the published proofs, so the entry holds the reported lane. One id; changes four case pages.
3. Keep the Lean proofs as evidence on the record with no register entry, until a build here makes them a verified route. Daniel's route has a source-coverage entry; chelokot's would need one too, and with it a card for chelokot/square-packing-archive in the home page's Other Projects list (devtools/site_resources.OTHER_PROJECTS, which tests/test_overview.py holds to every source repository the coverage register reviews), a site change the intake lane did not make.

The lane's draft entry (headline, claim, significance S2, unfinished confirmations think-7l2j and think-tq3g) is in the lane's report to the coordinator and can be registered as written under option 2, or with kind formalization under option 1. Stage 4's review and the builds (think-tq3g) do not wait on this decision.

blocked_on: none
