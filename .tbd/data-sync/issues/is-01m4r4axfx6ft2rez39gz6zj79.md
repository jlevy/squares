---
type: is
id: is-01m4r4axfx6ft2rez39gz6zj79
title: "Follow-ups after #516 merged (2026-10-12)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T13:20:20.989Z
updated_at: 2026-10-12T13:36:32.110Z
started_at: 2026-10-12T13:20:28.417Z
---
Replies owed on #501, #503, #504 and #505 after PR #516 merged into main (4a4910524), which registered T-147 to T-150 at V3/C3, under the owner's 2026-10-11 rule: post after merge, link only to main, check main and the deployed site first; record each reply in packing/campaign/result-requests.yaml on claude/wizardly-meitner-wqn4x3-replies-3.

## Notes

## 2026-10-12 lane: follow-ups owed by #516 (merged 4a4910524)

**Basis.** Branch replies-3 at origin/main 4a4910524. Certificate page run 38254265250 for that commit succeeded (deploy 13:19:40Z, verify-deployment 13:26:22Z). results.html carries rows #t-147 to #t-150 at V3/C3 with credits, and result/t-147.html to t-150.html show the registered sides and margins. Every comment on #501, #503, #504 and #505 (and #528) was read before drafting and again before posting; nothing had arrived since read_through. Margins were recomputed exactly from main's results.yaml and case records, and they match the register.

**Posted** from jlevy's gh account, kind confirmation, each ending with the Claude Code footer. Each was edited a minute later to name its two evidence ids:
- #503 https://github.com/jlevy/squares/issues/503#issuecomment-6125247333 (T-147; asks which AI-assistance account stands; suggests fixing numerical_screen_side)
- #504 https://github.com/jlevy/squares/issues/504#issuecomment-6125249586 (T-148; same AI question, one answer on #503 enough)
- #501 https://github.com/jlevy/squares/issues/501#issuecomment-6125250032 (T-149; KKT not registered; README delta 1e-30 vs 1e-60; asks whether #528's AI statement covers #501)
- #505 https://github.com/jlevy/squares/issues/505#issuecomment-6125250423 (T-150; T-146 stays verified second at 146, T-125 kept as history; asks whether the 146 started from Xu's certificate or Daniel's view)

**Recorded** in result-requests.yaml at 718877cf2. check_requests passes; --report shows no reply due on the four; packing-validate --records exit 0 (49 of 107, 239.5 s). PR https://github.com/jlevy/squares/pull/551 (not merged).

**Next.** Reply on each when #518 merges and the case records move.
