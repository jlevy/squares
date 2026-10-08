---
type: is
id: is-01m4e37ersbgmvw7ana72wd5an
title: "PR #395 rollout: validate lazy result popover record links on the deployed site"
kind: bug
status: closed
priority: 1
version: 7
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4e2d5gyj7m218hm9f5g01xd
child_order_hints:
  - is-01m4eb8kz1h7j4ehrj1kzdkky0
  - is-01m4eb8p5zxp3ydac3s0a2gk9p
  - is-01m4eb8rf6wx3as03vsmqnn0dm
hold: null
hold_until: null
created_at: 2026-10-08T15:48:34.711Z
updated_at: 2026-10-08T21:56:26.555Z
started_at: 2026-10-08T15:48:56.853Z
closed_at: 2026-10-08T21:56:26.555Z
close_reason: Corrected deployed checker independently reviewedA-D at3d266f8 and preserved under follow-upE/e047331, merged91ca9b8. D1 all opening targetIDs/single globalpopover guard, D2 exactLF offsets, D3 renderer-derived membership and meaningfulnegativecontrols allfixed/closed. Actual mainPages37848801634 verify-deployment113558173888 executes --commit91ca9b824873bde5aa085d7e2532bff366e0878b and passes3750/3750checks/zeroFAIL. Registry894rows; actual495 registerednonasset/nonpatternURLresponsesall200 (not894servedresponses). Homepage51rows/184recordlinks and full116rows/392recordlinks pass lazyfragment/canonicalfallbackbinding. Realworkbench startup323pairs and servedrevisionbindingpass. Independentproductionbrowser zero failures28noJScontexts/14metadata/22nav-math/9delivery with bothmarkers91ca9b8. Raw log/JSON postmerge-91ca9b824-deployment-113558173888 retained outside scratch. Final fullPacking105completion remains only under rolloutthink-7wlz.
resolution: null
duplicate_of: null
---
Actual merged deployment913781538 failed2/3750 checks: the homepage and all-results record-link checker assumes inline site-records markup, while production rows use data-row-pop-src fragments with static fallback links. Correct the checker to verify each expected row binds its own served fragment and canonical fallback, and every rendered record link remains present; retain fail-closed negative coverage for missing/mismatched rows, fragment destinations and record links. Deploy and validate through a separately reviewed follow-up PR.
