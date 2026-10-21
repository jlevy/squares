---
type: is
id: is-01m5fwv4cnnm68c35kmfne4wce
title: Correct Frits Göbel display name and Lewis public X account
kind: task
status: closed
priority: 2
version: 7
delegate: profiles-data-integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T18:51:10.100Z
updated_at: 2026-10-21T21:45:33.748Z
started_at: 2026-10-21T18:52:21.376Z
closed_at: 2026-10-21T21:45:33.748Z
close_reason: Completed bounded implementation, reviewed evidence and local/hosted feature acceptance. Final-head CI and separate runtime/evidence followups remain open.
resolution: null
duplicate_of: null
---
Owner explicitly requests Frits Göbel as canonical display name, already corroborated by retained catalogue/bibliography. Preserve f-gobel slug and F. Göbel alias; correct display provenance and literal source locator. Owner also requests the public X account ctjlewis, directly cross-linked by github.com/ctjlewis and corroborated by the retained n11 announcement receipt. Add only that account and supporting crosslink evidence to the existing Lewis profile; do not expand the person's name or infer a surname. Validate both records and live identity joins; preserve all archive bytes.

## Notes

Both explicit profile corrections complete: Frits Göbel full canonical display/stable slug/F. Göbel alias; Lewis public X account corroborated by GitHub crosslink and retained receipt. Both schema valid, zero repairs. Live semantic loader75profiles/1523occurrences; no archived source edits.

Completed both narrow identity/account corrections. The f-gobel profile has canonical display_name and real_name Frits Göbel, preserves its slug and F. Göbel source alias, and uses retained catalogue/bibliography provenance for the full name while keeping the literal archived byline. Lewis retains the evidenced public name and stable ctjlewis slug; the X account https://x.com/ctjlewis has the explicit GitHub social crosslink and retained announcement evidence. No fuller name or surname is invented. Both records were schema valid without repairs; later live 75-profile loader/schema/census and hosted rendered-profile checks pass. Archive bytes remain unchanged.

Final integration evidence: the scoped work is committed and published in https://github.com/jlevy/squares/pull/578, currently at db3cb6d4fe5f00a44d04a8ef91018aa2b365bad8. Hosted validation at e162a870a899a61cc77cd47fa2f56c0ff388c8ea passed Pages, Packing Validate and suites B/C; suite A passed all 4,364 assertion tests, then failed only the separate project-tally CALL wall guard. That independent runtime defect is fixed in e3e33171bf1d687190cc957a40e25fbbc9dbb23c and remains tracked by think-rolz while final-head CI runs. The exact final db3 CI verdict is not claimed here. This closure is for completed bounded acceptance; the overall think-zpfo handoff, think-uwd6 coverage parent, historical registrations, pending PDF census and real evidence gaps remain open.
