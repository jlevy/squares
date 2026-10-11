---
type: is
id: is-01m41e1tqg81pgz89snb0whnv4
title: "After landing: verify the Pages deploy end to end and the new results on the live site"
kind: task
status: closed
priority: 1
version: 3
labels:
  - merge
  - site
dependencies: []
parent_id: is-01m41cr1mz526vz5b2a5e4z100
created_at: 2026-10-03T17:47:37.072Z
updated_at: 2026-10-03T18:33:43.852Z
closed_at: 2026-10-03T18:33:43.851Z
close_reason: null
resolution: null
duplicate_of: null
---
Owner, 2026-10-03: double-check everything deploys end to end and is visible on the website. After each merge to main: the 'Certificate page' workflow (pages.yml) run on main passes prepare, build, deploy and verify-deployment (check_published_site). Then on https://jlevy.github.io/squares/: Recent Results and all-results.html show T-066..T-079 with the right rungs and credits (wand125, Evan Daniel, squarepacker, Levy); the frontier shows 77 proved; case records cases/59.html, 60, 61, 77, 78, 97, 12 show the new bounds and the formula-wrap fix; the README intro example reads 5.7975. Record the run id and what was checked.

## Notes

2026-10-03 18:30 Deploy of 47569ad50 (#292 with #298): Certificate page run 37143298451 prepare, deploy, verify-deployment all success. Live https://jlevy.github.io/squares/: all-results.html carries rows t-060..t-079; T-064 V3 C3 S4 confirmed; T-066, T-067, T-075, T-079 V3 C3 S3 confirmed; cases/60, 61, 77, 78, 97 read s(n) = 8, 8, 9, 9, 10; cases/59 reads s(59) = 8; cases/12 carries 15680000/3949423 = 3.9702002. Pending: the 4043d863e (#311) deploy run 37143348932.
