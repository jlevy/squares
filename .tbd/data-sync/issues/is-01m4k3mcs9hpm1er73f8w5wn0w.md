---
type: is
id: is-01m4k3mcs9hpm1er73f8w5wn0w
title: "acquire_source: let identical_to bind an original-gzip retained file across packets"
kind: task
status: open
priority: 3
version: 1
labels:
  - packing
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T14:31:50.824Z
updated_at: 2026-10-10T14:31:50.824Z
---
Found retaining Ryu's v1.1 packet (think-7lpw): acquire_source reads .gz twins decompressed, so identical_to cannot bind an original-gzip copy in a later packet to the earlier packet's; the five unchanged Theorem 1.6 certificates in squarepacker-k2-minus-c-upper-v11-2026-10-10 are bound only by equal digests. Teach identical_to to compare stored bytes for original-gzip rows, with a test.
