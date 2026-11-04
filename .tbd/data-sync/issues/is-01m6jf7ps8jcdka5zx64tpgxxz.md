---
type: is
id: is-01m6jf7ps8jcdka5zx64tpgxxz
title: "Import Yim: s(260) <= 16.6339825019226, 1.99e-10 below T-257, attachment-only certificate (#895)"
kind: task
status: in_progress
priority: 1
version: 2
delegate: bold-ritchie-l36
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-04T05:06:47.208Z
updated_at: 2026-11-04T05:07:17.344Z
started_at: 2026-11-04T05:07:17.344Z
---
Import of jlevy/squares#895 (opened 2026-11-04T02:15:02Z by vitamoon, Kaelan Yim): s(260) <= 1045817814143413714427921537528704162855767253933/62872364692131569638734867237718772414897487626 (about 16.6339825019226141), about 1.99e-10 below the case's house, Evan Daniel's #845 certificate (T-257) at 16.6339825021218840.

## Claim map
- Source: the certificate exists only as a GitHub issue attachment, https://github.com/user-attachments/files/34348312/n260.cert.txt, which this environment cannot fetch (user-attachments is not reachable from the session). Nothing is retained, and no digest is stated.
- Claims: (1) s(260) <= the exact side above [register: a new upper-bound entry once retained]; (2) the author converted the rational certificate to Witness/v2 corner form and ran devtools.check_rational_witness_independent at e6e8d577: VERIFIED, 260 squares, 33,670 pairs (source statement only); (3) lineage: the search started from a public packing attributed to Evan Daniel and Kirill Tymchishin (the house, T-257), with the refinement the author's own. AI assistance: used to study and set up an environment like Daniel's and Tymchishin's.
- Who else holds a value at 260: the house T-257 (Daniel after Tymchishin at this count); no register bound pending adoption below it. The ledger of this pass walks the claim by its stated exact side; stage 3 cannot register it until a certificate is retained.

## Plan
- Acknowledge, asking the author to put the certificate at a public GitHub commit and name it with its SHA-256, as #847's acknowledgement did.
- Waits on the author's answer; then retain the packet at that commit, check the digest, decide it on both exact routes with controls, register, and give it a stage 4 review and adoption like #893's and #894's.

blocked_on: the author's answer on jlevy/squares#895 (a public commit holding the certificate)

Answer bead: this bead.
