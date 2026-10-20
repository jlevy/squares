---
type: is
id: is-01m52v9rgthxyrrjczpgtc51gk
title: Merge the 16 October PRs once reviewed (owner's word, 16 Oct afternoon)
kind: task
status: open
priority: 2
version: 29
labels: []
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
child_order_hints:
  - is-01m53c3469tq34ee6pbcn8xygw
created_at: 2026-10-16T17:14:04.698Z
updated_at: 2026-10-17T17:40:24.504Z
---
Owner: 'If everything is reviewed, you can merge it.' and 'Follow up everything you can, and once things are reviewed, be sure you merge.' Merge order and gate per review-and-merge-prs; release re-cuts after each merge.

## Notes

17:30Z merge plan. Deep gates are running on #642, #649 and #651. #647 passed its follow-up review B (0 findings); it updates from main after #642 merges (conflict in intake-watch.yaml), then gets the deep-gate label. #641 takes D1 (High, think-cmj7) before merge; addr-641 is running and also does #650's B1. #649 contains #652, so #652 merges first, after its follow-up.

user-eb-integrator: PR #647 updated from main: merge 0afbc796e (intake-watch + release.py conflicts, both sides kept), 61b8a72f8 (record names head v0.7.15), re-pin 68ce40481 pushed; deep-gate label added. Next: local validation, CI watch, description update.

user-eb-integrator: PR #647 at 68ce40481: local records tier exit 0 (205 s), release_pin --check ok, check_release_impact ok, release tests 40 passed; description updated (Update from main for merge, v0.7.15, cost, local validation). Waiting on hosted CI (Packing validation 38943263036, Certificate page 38943263014, Deferred checkpoint 38943272778).

18:45Z: #644 addressed at 6fee7bfc8 (D and E; D2 is deferred to think-fhz2 until the deep gate can run after the update from main). Follow-up F is running. #646 addressed at 7b925989f; follow-up D is running. Merge queue for the integrator: #647 (in progress) → #655 → #648 → #652 → #649 → #644 → stack (#653 → #654 → #656 → #657) → #641 → #650 → policy PR → #646 → #645 → #658.

19:20Z: #644's follow-up review F at 6fee7bfc8 has 0/0/2/2 and a suggestion. Addressing pass addr-644b is running. Merge condition (review F): hold #644 on think-fhz2. The deep gate (regularized-views, exhaustive-1..3, deep-gate-required) and Packing validation must succeed at the exact head that merges, after the integrator's update from main, and that run must be recorded in the PR's Validation before think-fhz2 closes.

user-eb-integrator: PR #647 ready to merge at 68ce40481a327568c367bf0cbd6a8f48cb6f0938: Packing validation 38943263036, Certificate page 38943263014, Deferred checkpoint (deep-gate) 38943272778, Branch mergeability 38943257188 all success; mergeable clean; still a draft. Description carries the update section and hosted result. Waiting for the coordinator's next PR.

user-eb-integrator: PR #655: merged main 7b34cd5bb in 1efce164b (no conflicts; diff vs main stays the same 11 files, identical change lines), cut site v0.7.16 in 565dea9d3 (README, release.py, 5 claim docs, explainer no-change record); #645 also holds v0.7.16. Pushed; deep-gate label added. Next: records tier, CI, description.

user-eb-integrator: PR #655 at 565dea9d3: records tier exit 0 (125 s), release_pin/check_release_impact ok, release tests 40 passed; description updated (Update from main for merge, v0.7.16 row, #645 collision). Waiting on Packing validation 38949883721, Certificate page 38949883964, Deferred checkpoint 38949927603.

user-eb-integrator: PR #655: hosted at 565dea9d3 had two flakes (frontend setup-uv manifest timeout job 117138845290; Certificate page prepare render-twice style-attr instability job 117138870826); re-triggered once with empty commit b835bea63. Waiting on CI.

user-eb-integrator: PR #655 ready to merge at b835bea632f004830e9e325d95fb6718ca758517 (site v0.7.16; #645 also holds v0.7.16 and must re-cut if it merges after). CI: Packing validation 38951274753, Certificate page 38951274861, Deferred checkpoint 38951274874, Branch mergeability 38951268935 all success; mergeable clean; still draft. Description updated.

user-eb-integrator: PR #648: merged main 8069b12e2 in 815f3c67e (map rows kept both, SYNOPSIS regenerated, cut files from main), re-cut site v0.7.17 in 75d272651; pushed; deep-gate label added. Next: records tier, description (B1), dispositions review, CI.

user-eb-integrator: PR #648 at 75d272651: records tier exit 0 (124 s), release checks ok, 40 release tests passed; description updated (B1 fixed, update section, v0.7.17); B dispositions posted as review 5552768422. Waiting on CI.

user-eb-integrator: PR #648 ready to merge at 75d27265132419a57c45cb0fc009317b8fc3b9b2 (site v0.7.17). CI: Packing validation 38955634631, Certificate page 38955634059, Deferred checkpoint 38955742135, Branch mergeability 38955629316 success. #641 (68cdbc614) merged after: disjoint release.py hunk, PR still clean, trial merge passes release checks. Still draft.

user-eb-integrator: PR #648 B1: session GitHub proxy wraps any URL into packing/resources/web/ in backticks (probed: blob, tree, reference-style all wrapped; docs/ path not), which is how B1's broken link arose; description now names the README path as code; dispositions review 5552768422 says so. #648 ready at 75d272651, clean.

user-eb-integrator: #652: merged main 96510ae7a in 1cc0dbbe3, re-cut v0.7.18 in b868ba4e5, pushed, deep-gate label. Next: #649 merge #652's head, cut v0.7.19.

user-eb-integrator: #649: merged #652 b868ba4e5 in 2d57609b3, re-pin 3d4ada4c7, cut v0.7.19 32634cfca, pushed. Records tier: 51/52, only synopsis step fails: check_release_impact vs origin/main (v0.7.17) needs one successor, finds v0.7.18+v0.7.19; passes vs #652's head. So #649's hosted packing-required will be red until #652 merges and #649 merges main.

20:10Z: merged so far today: #642 (abd65fba3), #651 (26d8bb335, v0.7.15), #647 (7b34cd5bb), #655 (8069b12e2, v0.7.16), #641 (68cdbc614), #648 (96510ae7a, v0.7.17). In progress: the integrator on #652+#649 (v0.7.18, v0.7.19), #650's update, the stack lane's phase 1. #645 was addressed through review E (7/0/0; no further round: small predicate tightenings with tests, no live rung change) and is ready for update. #646 is done through review E and ready for update. Queue after #649: #646, #645, then the stack (lane S phase 2), #660, #658.

user-eb-integrator: #652 description (collision rewritten, update section) and B dispositions (review 5553251410) posted at b868ba4e5; #649 description updated at 32634cfca with the known release-impact red. Watching CI on both.

user-eb-integrator: #652 ready at b868ba4e5e2e4360bfd2cbd1d6b25c1e2177a7c4 (v0.7.18): runs 38960055955, 38960056031, 38960049586, deep gate 38960076560 success; clean vs main 321d492c7 (#650, no overlap). #649 at 32634cfca: validate red only on check_release_impact vs main (by design, v0.7.18+v0.7.19 vs v0.7.17); needs main merge + one CI run after #652 lands.

user-eb-integrator: #649 merged main c9038049c in f62671cc2 (no conflicts), pushed; records tier exit 0 (144 s), release_pin/check_release_impact pass vs main now; 40 release tests passed. CI running. Starting #646.

user-eb-integrator: #646: merged main c9038049c locally in f79f22cd1 (cut files from main, papers NPC kept); not pushed yet to keep #649's CI runners free; release-impact asks for the site successor as expected. Cut waits for #649 to land (v0.7.20).

user-eb-integrator: #649 ready at f62671cc2b2e32be5d14d5674e634902b7278b30 (v0.7.19): runs 38964806395, 38964806387, 38964803683, deep gate 38964806391 success; clean. #646 merge f79f22cd1 pushed for early CI signal (release-impact red expected until the v0.7.20 cut after #649 lands).

user-eb-integrator: #645 merged up: 5b041b88a (merge main 80b116ede; cut files from main, two paper NPC records kept at tuple end, INVENTORY/VERIFIERS regenerated), dafff1238 (re-pin to 5b041b88), pushed. Records tier: only release-impact step red (site successor pending cut); 409 focused tests passed. Waiting for #644 -> #646 (v0.7.21) -> #645 cut.

Merge condition for #661 (T-195, #622's s(29)): it keeps T-195 at V3/C3 on the replay alone. The T-193-style hold makes T-195 derive 'superseded' against the Kingbird print at 29, with no superseding result (lane N, 58de4dedc). So #661 merges only together with its stage 4 review PR, stacked on it: both reviewed, then merged back to back, the review PR right after #661 with no other merge between. Main never shows T-195 at V3/C3 without the review mapped.

00:05Z, 17 Oct: #654 merged (5012a97d6, v0.7.22). #662 was merged into #661's branch by lane N's fast-forward push and closed as merged at 23:42Z; its commits reach main through #661. New order: #656, #657 (stack); then #660 after its follow-up review; then #661 (drop HELD['T-195'], fold the adopt branch, adopt and settle 29 under the house rule, re-cut, follow-up review); then #646, #645; then #658.

04:10Z 17 Oct: merged since the afternoon, 16 PRs: #642, #651, #647, #655, #641, #648, #650, #652, #649, #644, #653, #654, #656, #657, #663 and #660 (main 804eff369, site v0.7.25; infographics v0.6.2 live). In flight: #661 (T-195 adoption pass, v0.7.26), #658 (T-193: drop the exemption and stage the counts), the T-174 adoption (think-3mry, new lane). Then #646 and #645.

17:55Z 17 Oct: the worker was down from 07:50Z to 17:35Z, and lanes were resumed. Open lanes: #661 (review C: 2 Blocker, 2 High, being addressed), #665 (T-174 at 37 counts, resumed with uncommitted work), #658 (review B's B1), #667 (sweep: senior review running), the Evan Daniel imports #659 and #664 (new lane), the #446 census of 18 lower bounds (new lane, owner: all 18). Waiting behind them: #646, #645. Merge order once ready: #667, #661, #658, #665, the evand PR, census batches, #646, #645.
