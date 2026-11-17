---
type: is
id: is-01m5q9h2v09zqp5k29wf7s9mk1
title: "PR #793 (merge): dedicated security review C of W7's hosted shard reader (hosted_shards.py, tar.xz from a hosted release)"
kind: task
status: closed
priority: 1
version: 4
delegate: c-rev-793c-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T15:47:33.344Z
updated_at: 2026-10-24T16:04:53.419Z
started_at: 2026-10-24T15:47:51.199Z
closed_at: 2026-10-24T16:04:53.418Z
close_reason: "Review C (security) posted https://github.com/jlevy/squares/pull/793#issuecomment-6386394144: no security objection; C1-C3 Low (pax/longname header memory, shared members directory, root-shard ValueError), C4 suggestion; custody chain verified by proof of concept."
resolution: null
duplicate_of: null
---

## Notes

c-rev-793c-1024, 2026-10-24: Review C (security, round 1) published at head 6d44159 as https://github.com/jlevy/squares/pull/793#issuecomment-6386394144. Verdict: no security objection; no Blocker/High/Medium. C1 Low (pax/longname header records bypass MAX_UNPACKED; a 78 KB pinned shard reached 2,085 MiB RSS and was accepted), C2 Low (members directory shared across manifests; stale member wedges read), C3 Low outside security (root-level shard raises ValueError), C4 suggestion (resolve members dir inside repo). A7 measured: 1,060 MiB peak for a 512 MiB member. Evidence: scratchpad/rev-793c/ (scripts/poc.py, scripts/fixproto.py, *.log).
