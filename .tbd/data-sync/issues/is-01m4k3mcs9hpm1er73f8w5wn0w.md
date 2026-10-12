---
type: is
id: is-01m4k3mcs9hpm1er73f8w5wn0w
title: "acquire_source: let identical_to bind an original-gzip retained file across packets"
kind: task
status: open
priority: 3
version: 2
labels:
  - packing
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T14:31:50.824Z
updated_at: 2026-10-10T15:42:52.052Z
---
Found retaining Ryu's v1.1 packet (think-7lpw): acquire_source reads .gz twins decompressed, so identical_to cannot bind an original-gzip copy in a later packet to the earlier packet's; the five unchanged Theorem 1.6 certificates in squarepacker-k2-minus-c-upper-v11-2026-10-10 are bound only by equal digests. Teach identical_to to compare stored bytes for original-gzip rows, with a test.

## Notes

2026-10-10, W7 sub-agent, branch worktree-agent-a1a6d43e4d2761761, commit e9aa9c81e (on 63cac425e), for the coordinator to merge.

Change: packing/devtools/acquire_source.py adds _original_gzip_twin and _twin_bytes. A twin that its packet's "## Original Gzip Files" README table lists (the raw-byte custody of devtools.retained_data) is read as stored by read_original_gzip_bytes. Every other twin is read by read_retained_bytes, as before. The table decides, not the file name. acquire and --check (_pinned_problems) both use it. Docstrings of the module, PinnedOnly.identical_to and Rule.identical_to are updated.

Tests (packing/tests/test_acquire_original_gzip.py), written failing first: an original-gzip twin binds by stored bytes; a recompressed twin with equal decompressed content is refused by check and acquire; a .gz twin missing from the custody table is still read decompressed; the real v1.1 packet binds exactly the three certificates v1.0 keeps as original gzip, and not the two hosted ones.

Packet: the v1.1 declaration splits data/* into two hosted digest-only rules (stair_k38250000, stair_k100000000) and a data/* rule with identical_to pointing at the 2026-10-09 source/data directory. The record was rewritten by acquire_source --checkout at 5742311db220b4bd8e825167aeae689a1bd65ce9, and the 74 retained files and the manifest came back byte-identical. 26 of 28 pinned-only files now carry identical_to. The README prose is updated (23 -> 26).

Checks: acquire_source --check passes on 48 of the 49 packets that carry a declaration. The exception is wand125-valid7-independent-check-2026-10-02, which raises ValueError in retained_data.check_packet: receipts/replay/wand125_shard01_1.jsonl.gz decompresses to 94,860,304 bytes, over MAX_DECOMPRESSED (64 MiB). It fails identically at HEAD 63cac425e and does not involve identical_to. This is pre-existing and left unfixed.
