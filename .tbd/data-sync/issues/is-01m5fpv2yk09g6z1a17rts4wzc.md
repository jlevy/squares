---
type: is
id: is-01m5fpv2yk09g6z1a17rts4wzc
title: Integrate profile UX work with current PR and prepare final review handoff
kind: task
status: in_progress
priority: 2
version: 44
delegate: profiles-pr-coordinator
labels: []
dependencies: []
child_order_hints:
  - is-01m5fq4r2w71afncj0bpg0gsj1
  - is-01m5fqbw4gey86dc038cvz6aef
  - is-01m5fqs42kkgbj16cwk57a5hss
  - is-01m5fqs4kpenmh2g2ya3s340em
  - is-01m5fqs520v76h7ac1rdvq8h2c
  - is-01m5fqzgp1rg8bbxx0m2e47prh
  - is-01m5fr7gvch42rgdf4q2jvw206
  - is-01m5fr7he5dhknekzzf2r623xv
  - is-01m5frh64q04x1zngbk2cmxx1q
  - is-01m5frh6qfcggwvwaa3f9af9w4
  - is-01m5frjg0sxenf7fyjrryrt2db
  - is-01m5fs0mwhp9qa7qp46kdf11c9
  - is-01m5fscvj1jgv9wx923z0a30y2
  - is-01m5fsnyqj85asc7tq4276kyk9
  - is-01m5fstx5hpcn6431qmyvrnr6a
  - is-01m5ft29c3tph6bgywc9ycwgmp
  - is-01m5ft6ard4cff2y4xah2q4p2e
  - is-01m5ftdbpjs8bcm7450ngrhxae
  - is-01m5ftsx292fked2gcgpkv6a5x
  - is-01m5ftwbnpeqfcss048aexcjf7
  - is-01m5ftx2xbjaehzd0q9pwgv1hc
  - is-01m5fw6v3p9gb2jgen89a2ncs8
  - is-01m5fw9z474w84hemxsff4a9zs
  - is-01m5fwdhgyd3ar79bqwyy46jt8
  - is-01m5fwv4cnnm68c35kmfne4wce
  - is-01m5fxpvywfbye3f5gksgzsvzt
  - is-01m5fy05g8n1q6rksv7pntnrxe
  - is-01m5g022qevmw4aefxb2w4nn62
  - is-01m5g0dept4r1ejr31gnkr77kt
  - is-01m5g28824ts9q4byp8ezh6sxf
  - is-01m5g2wfw0xf50d000t9mn6wbv
  - is-01m5g3da86sky65p89agbvcpfs
hold: null
hold_until: null
created_at: 2026-10-21T17:06:17.155Z
updated_at: 2026-10-21T21:10:00.340Z
started_at: 2026-10-21T17:06:34.736Z
---
Preserve current remote PR578 changes; commit local profile UX/model changes, integrate latest PR branch/main as needed, validate, push reviewable PR and handoff without merging.

## Notes

Pushed e162a870a to PR #578, including merge e9149e2a2 of origin/main 970e89de8, data pin 3ae236a16, and updated plan. GitHub reports MERGEABLE; still draft until final CI. Local push gate passed all 69 selected steps in 952.59s (19,907 normal tests passed, 65 skipped, one expected failure; 23 pool-heavy passed). Full rebuilt preview site-merged-3ae236a16 is live on port 8790 and open in Arc. All 7,298 publication checks, 692-page profile-link audit, 48 PDF links, 59 shared assets, and eight live routes pass. Name column has a 16rem floor and long resource URLs wrap. Model remains 75 profiles, 213 primary results, 701 credits, 114 authored records; global current records 116. Latest main adoption at 227/260 and release v0.8.15 preserved beneath proposed v0.9.0. Astra found no merge issues. Explicit deep run 39676452183 and all final-head PR checks are being watched. Next: fix any CI failures, then mark ready and finish handoff without merging or deploying. Deferred archive population and historical registrations remain separately tracked.
