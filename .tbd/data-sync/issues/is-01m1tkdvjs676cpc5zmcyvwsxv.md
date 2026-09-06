---
type: is
id: is-01m1tkdvjs676cpc5zmcyvwsxv
title: "verify_claim.py: cross-check declared claim, total_mass and least_cell_mass, or say it does not (F4)"
kind: task
status: open
priority: 2
version: 1
labels:
  - review-gpt6
dependencies: []
parent_id: is-01m1tkdspk8c3n71xsc2e2t4g7
created_at: 2026-09-06T05:35:29.368Z
updated_at: 2026-09-06T05:35:29.368Z
---
Finding 4, confirmed: certificate.json carries claim, total_mass and least_cell_mass; verify_claim.py never reads them and pins no digest (grep finds none of the three). A file with 'claim: s(11) >= 100, total_mass: -100' still exits 0, printing the computed conclusion rather than the declared one -- not a false acceptance, but a success exit that automated consumers may read as validating the file's metadata. The thirdparty verify.py and the retention gate already compare declarations with recomputed values. Fix: either compare the three declared fields with the recomputed values and refuse on mismatch (aligning the public entry points), or print a prominent line that success verifies parameters, not declarations. Regenerate the claim documents after.
