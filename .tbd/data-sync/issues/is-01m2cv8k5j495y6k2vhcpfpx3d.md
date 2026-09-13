---
type: is
id: is-01m2cv8k5j495y6k2vhcpfpx3d
title: "PR #157 review READ-03: explicit empty counts erase the weighted declaration"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:45.298Z
updated_at: 2026-09-13T08:19:32.020Z
closed_at: 2026-09-13T08:19:32.020Z
close_reason: "Fixed at both sites. Orbit parser: _multiplicities replaced by _sites (admit_threshold_atom_orbits.py:123), reading weighted_points, refusing the withdrawn multiplicities by name and refusing null/unknown-variant/mixed/empty/incomplete through AdmissionError. Before: {variant, multiplicities: []} gave token_count 2, support_size 2, admitted True -- silently all-ones. After: refused. Decide gate: _token_counts replaced by _refuse_token_counts (decide_threshold_certificate.py:114), called at line 184 BEFORE the coordinates are read, raising FormatError. Before: the same record built an atom with multiplicities (1,1,1) and passed the strict unweighted check. After: refused. The old post-construction token_count != size check was removed as unreachable once the refusal precedes the constructor. refuse_weighted_record's ValueError is caught and relabelled since FormatError and AdmissionError are both ValueError subclasses."
resolution: null
duplicate_of: null
---
threshold.py:300-302, packing/devtools/decide_threshold_certificate.py:123-127 and the orbit parser all turn 'multiplicities: []' into the constructor's omitted-count sentinel, so a tagged T025 atom becomes all ones and passes the strict reader's unweighted check. Fix: distinguish MISSING legacy data from MALFORMED declared weighted data; refuse weighted declarations at unweighted-only admission boundaries before normalization; reject null, unknown, mixed, empty and incomplete shapes through the documented error path.
