---
type: is
id: is-01m5qby1zmjad2rrmwzhvc09rs
title: "hosted_data: apply the plain-path rule in load_manifest (PR #793 review C, outside the diff)"
kind: bug
status: open
priority: 3
version: 1
labels:
  - infrastructure
dependencies: []
created_at: 2026-10-24T16:29:35.603Z
updated_at: 2026-10-24T16:29:35.603Z
---
PR #793 review C, Outside This Diff (https://github.com/jlevy/squares/pull/793#issuecomment-6386394144). sqpack.hosted_data.load_manifest does not apply the plain-path rule that check() applies, and the schema's path pattern admits '..' segments: a committed manifest naming x/../../elsewhere/s.tar.xz loads, and require resolves it outside the repository (the read is still digest-checked; devtools.hosted_shards.unpack refuses such a members directory). Run the plain-path check in load_manifest, or tighten the path pattern in packing/hosted/hosted-data.schema.yaml, with a refusal test.
