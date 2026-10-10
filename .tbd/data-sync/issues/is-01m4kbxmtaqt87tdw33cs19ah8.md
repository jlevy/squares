---
type: is
id: is-01m4kbxmtaqt87tdw33cs19ah8
title: "Import wand125: s(28) >= 2297/400 and s(30) >= 2357/400 by fine-net check2 certificates (no issue)"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T16:56:42.570Z
updated_at: 2026-10-10T16:56:42.570Z
---
Found by the 2026-10-10 evening reads (think-0nkn): wand125/square-packing 36b85b9 and ff9f269 add problems/square-lower-bounds/certificates/mixed_n28_L57425/ and mixed_n30_L58925/, check2 bundles on the 2,073-direction net (core 4999/5000, step 1/5002), reporting s(28) >= 2297/400 = 5.7425 (mass 2799999/100000; +3/400 over T-107's 1147/200; +1/400 over #446's unadopted 287/50) and s(30) >= 2357/400 = 5.8925 (mass 2999999/100000; +9/1000 over T-109's 11767/2000). Data: square-lower-bounds-v1 assets certificates__mixed_n28_L57425.tar.gz (627,191 B, SHA-256 7d0f910768d47fcdba6233334798487471db7ef2fe556400269c34c3116d3bf3) and certificates__mixed_n30_L58925.tar.gz (638,622 B, 0d11fe0554909e1457d70efa425c82344e622006590ac6ee58a481b69d1b61ba). Author: 772 s and 1790.3 s, 0.985 control at 32 directions. No issue reports them. Stages 1-3 as T-132 (#446 s(29)) did with devtools.fine_net_followup; full capture likely CPU-hours (owner budget).
