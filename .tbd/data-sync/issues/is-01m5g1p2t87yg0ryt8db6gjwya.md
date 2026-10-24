---
type: is
id: is-01m5g1p2t87yg0ryt8db6gjwya
title: Give issue 678's packet an import declaration instead of a bespoke house source (#706 A7)
kind: chore
status: open
priority: 3
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-21T20:15:47.528Z
updated_at: 2026-10-24T20:22:39.771Z
---
Review A7 of #706 (suggestion, deferred from that PR): give issue 678's packet (`packing/resources/web/couzo-issue678-2026-10-18/`) an import declaration, so T-223's house reads through `upper_bound_houses.packet_source` and `upper_bound_reports._import` like every other house.

Today T-223 has a bespoke path: `upper_bound_houses.couzo_678_source`, a `HOUSES` lambda in `upper_bound_reports`, `stored` and `receipt` fields on `Source`, and an import cycle between `upper_bound_reports` and `devtools/couzo_678_replay.py`. #706's merge with main broke the cycle by having the replay read `HORIZON`, `DISPLAY_PLACES` and `BEYOND_FORMAT` at call time (`reports.X`). That works only while neither module reads the other at import time: the next constant someone imports by name brings the `ImportError` back.

Done when: a declaration names the two in-corpus certificates (`certificates/best/n204.cert`, `n260.cert`) and `receipts/house-jobs.json.xz`; `couzo_678_source` and the lambda go; the cycle is gone (each of `upper_bound_reports`, `couzo_678_replay`, `upper_bound_houses` and `adopt_houses` imports first in a fresh interpreter); `upper_bound_houses check`, custody and `adopt_houses --check` pass unchanged. If the declaration format cannot express a certificate held to a digest in the packet's own manifest, say so in `couzo_678_source`'s docstring instead and close this.
