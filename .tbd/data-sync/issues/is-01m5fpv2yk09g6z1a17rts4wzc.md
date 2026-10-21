---
type: is
id: is-01m5fpv2yk09g6z1a17rts4wzc
title: Integrate profile UX work with current PR and prepare final review handoff
kind: task
status: in_progress
priority: 2
version: 43
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
updated_at: 2026-10-21T20:57:33.757Z
started_at: 2026-10-21T17:06:34.736Z
---
Preserve current remote PR578 changes; commit local profile UX/model changes, integrate latest PR branch/main as needed, validate, push reviewable PR and handoff without merging.

## Notes

Latest continuation: origin/main970e89de8 (#704, T-196 adoption and site v0.8.15) landed during hosted checks. Merged in e9149e2a2, then repinned DATA_REVISION in3ae236a16. Both commits local, not yet pushed. Three conflicts resolved preserving proposed v0.9.0 and upstream v0.8.15 history; RESULTS regenerated; exact n227/n260 occurrence joins now point to Joost de Winter. Astra reviewed merge boundaries with no findings. Counts unchanged75profiles/213primaryResults/701Credits/114authoredRecords (116globalcurrent). URLregistry1144rows0failures; sourcecoverage324cases580facts0divergences;20classifier/T196 and54identity/tally tests pass. Records52steps68.61s and edit68steps317.1s pass. Pushgate sincee2925e726 is running5305 with1800s cap, log latest-main-push-gate.log. Fullfreshpreview build98370 writes site-merged-3ae236a16, preserving live site-integrated-reviewed untilauditspass. Latestremotehead e2925e726 is conflicted against main; no Packing/Pages started for it, supersededdeferredrun39672860595 canceled. Next: finishgate/build, updateplan/PRbody, pushlocalmerge/pin, runexactheadCI+deferredcheckpoint, markreadyonlywhenallgreen. No merge/deploy.
