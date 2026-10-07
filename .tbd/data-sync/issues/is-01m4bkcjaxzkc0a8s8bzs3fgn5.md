---
type: is
id: is-01m4bkcjaxzkc0a8s8bzs3fgn5
title: Investigate historical interval-certificate byte drift in two three-owner controls
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-06-n17-ten-hour-session.md
delegate: sol-overnight-engineering
labels: []
dependencies: []
parent_id: is-01m4bj7tj2ydjh2v673ga1mw8j
created_at: 2026-10-07T16:33:16.124Z
updated_at: 2026-10-07T16:33:16.124Z
---
Two historical chunk-byte pins fail on the Mac at source800bba6388a1611ad8466aa6d93ebd3f0978b66a, while both fresh candidates independently pass FULL exact certificate verification. Keep the literal pins unchanged until historical byte equivalence and the cause of changed proposal bytes are established; semantic validity is a separate obligation.

Exact failing pytest nodes in packing/tests/test_pilot_n17_subpattern_bb.py:
- test_interval_certificates_are_unchanged_by_the_taylor_option[2.80-3]: expected3c55b054898682ab4b10deb12c645b29f7e664e45edac61ccfe08aa6cb913370, actualaf4b38d34e892e7736e1b63d493a6693be01ffa5ce215b809df30b216ae4a8dc.
- test_interval_certificates_are_unchanged_by_the_taylor_option[2.94-3]: expectedf85e95fb536920f128c001d1ca1c2b7e2ec0a47d6ba0577ad81ad676c975f497, actualba3ab3d19072f33cf1a2e9f031560ac6e4b2423b3be2e87000d31c620f0b71f9.

Bounded reproduction using external frozen Python3.14.7 reran only these existing toy controls; original settings unchanged, outer180s, sampled currentRSS4096MiB per owned live process, cleanup complete. Both reproduced the original failures in2.08s pytest/3.17965s supervised wall. No n17 research target ran. Source remained clean and literal pins unchanged.

Existing independent devtools.verify_n17_bb_certificate FULL verified source-defined exact rectangles, not certificate-derived input cells: cap1169/250; left x[1,1.05], middle x[1.4,2.4], right x[2.8,2.85] or[2.94,2.99], all y[2,2.05]. The2.80 artifact manifest ed0d47d6d2d17281a17e247bf7b5955865bf5c90adea76603e0155c699c2371c passed27/27nodes,14closed leaves,116trig checks,.094s. The2.94 artifact manifest bb384ce4335f1d9e7c5ee665af2108eeb8e18513421804a29cb4ffb72794e5a9 passed95/95nodes,48closed leaves,167trig checks,.225s. Both receipts have zero failures and sample:null. Astra reviewed this evidential distinction; no invalid geometric certificate observed, no new n17 admission or global result follows.

Durable primary ignored evidence: attic/evidence/session-184-taylor-toy-certificate-replay-800bba638/ contains22 byte-identically copied files (54,250rawbytes,104KiB allocated): both canonical gzip sets/READMEs, source-defined cells and digest custody, JUnit/two failure logs, full exact verify-280.json/verify-294.json receipts and supervision. Original full969 output directories pytest108 were already removed by pytest retention; new unique basetemp outputs are retained. A repository search found the historical expected chunk SHAs only in the literal test dictionary, no retained historical fixture objects. Cause remains unproved; do not assume platform floating proposal variation or blindly update hashes.

Resolve by locating or reconstructing the historical witnessed inputs/runtime and comparing exact candidate artifacts; preserve recipe/mode/input assertions and independent full replay. If a test expectation change is justified later, retain historical provenance and distinguish fresh candidate correctness from historical byte stability. This session intentionally leaves the two golden assertions unresolved.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
