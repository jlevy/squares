# Lane Claim Records Retained for the Ledger

`gather` reads each lane’s claim record by path: the packet’s
`packing/resources/web/<packet>/acquisition/<record>` where the checkout holds it, else
the copy here at `lane-claims/<lane>/<packet>/<record>`. It never reads a commit.

The thirteen records below belong to packets this tree does not hold yet; their lanes
land in the other records pull request, #602. Each was copied once, on 2026-10-14, with
`git show <commit>:<path>`, and is byte-for-byte that file.
Once a packet is on `main`, `gather` reads the tree’s copy, and the copy here can go.

The lanes’ other records are read from the checkout: the four ostashev records
(`dostashev-compositions-2026-10-12`, `dostashev-merged-bands-2026-10-13`,
`evand-compositions-2026-10-13`, `evand-fresh-compositions-2026-10-14`) and the main
lane’s `fang-direct-certificates-2026-10-13`. Each of those was byte-identical at its
lane commit when the copies were made.

| Copy | Source branch | Commit | Source path |
| --- | --- | --- | --- |
| `couzo/couzo-certificates-2026-10-12/claims.json` | `claude/wizardly-meitner-wqn4x3-intake-1014-couzo` | `f8ecf2173fa69c32729e1251cdeb96a6c3007f74` | `packing/resources/web/couzo-certificates-2026-10-12/acquisition/claims.json` |
| `couzo/couzo-certificates-2026-10-13/claims.json` | `claude/wizardly-meitner-wqn4x3-intake-1014-couzo` | `f8ecf2173fa69c32729e1251cdeb96a6c3007f74` | `packing/resources/web/couzo-certificates-2026-10-13/acquisition/claims.json` |
| `mishapolk/mishapolk-exact-certificates-2026-10-12/claims.json` | `claude/wizardly-meitner-wqn4x3-intake-1014-mishapolk` | `d4c198d0da8fe619bef0bccf18a8e6e32520c0f3` | `packing/resources/web/mishapolk-exact-certificates-2026-10-12/acquisition/claims.json` |
| `mishapolk/mishapolk-records-2026-10-14/claims.json` | `claude/wizardly-meitner-wqn4x3-intake-1014-mishapolk` | `d4c198d0da8fe619bef0bccf18a8e6e32520c0f3` | `packing/resources/web/mishapolk-records-2026-10-14/acquisition/claims.json` |
| `pingyou/pingyou-n105-refinement-2026-10-12/claims.json` | `claude/wizardly-meitner-wqn4x3-intake-1014-pingyou` | `680123806e979029a25948aa98d9aaf5473ccc33` | `packing/resources/web/pingyou-n105-refinement-2026-10-12/acquisition/claims.json` |
| `pingyou/pingyou-n146-refinement-2026-10-12/claims.json` | `claude/wizardly-meitner-wqn4x3-intake-1014-pingyou` | `680123806e979029a25948aa98d9aaf5473ccc33` | `packing/resources/web/pingyou-n146-refinement-2026-10-12/acquisition/claims.json` |
| `pingyou/pingyou-n153-refinement-2026-10-12/claims.json` | `claude/wizardly-meitner-wqn4x3-intake-1014-pingyou` | `680123806e979029a25948aa98d9aaf5473ccc33` | `packing/resources/web/pingyou-n153-refinement-2026-10-12/acquisition/claims.json` |
| `pingyou/pingyou-n207-refinement-2026-10-12/claims.json` | `claude/wizardly-meitner-wqn4x3-intake-1014-pingyou` | `680123806e979029a25948aa98d9aaf5473ccc33` | `packing/resources/web/pingyou-n207-refinement-2026-10-12/acquisition/claims.json` |
| `pingyou/pingyou-n261-refinement-2026-10-12/claims.json` | `claude/wizardly-meitner-wqn4x3-intake-1014-pingyou` | `680123806e979029a25948aa98d9aaf5473ccc33` | `packing/resources/web/pingyou-n261-refinement-2026-10-12/acquisition/claims.json` |
| `pingyou/pingyou-n272-refinement-2026-10-12/claims.json` | `claude/wizardly-meitner-wqn4x3-intake-1014-pingyou` | `680123806e979029a25948aa98d9aaf5473ccc33` | `packing/resources/web/pingyou-n272-refinement-2026-10-12/acquisition/claims.json` |
| `pingyou/pingyou-n302-certificate-2026-10-12/claims.json` | `claude/wizardly-meitner-wqn4x3-intake-1014-pingyou` | `680123806e979029a25948aa98d9aaf5473ccc33` | `packing/resources/web/pingyou-n302-certificate-2026-10-12/acquisition/claims.json` |
| `pr574/pingyou-pr574-certificates-2026-10-13/claims.json` | `claude/wizardly-meitner-wqn4x3-intake-1014-pr574` | `56cf868c617975eaada5b0c10dab953cc6fa2e37` | `packing/resources/web/pingyou-pr574-certificates-2026-10-13/acquisition/claims.json` |
| `pr574/pingyou-pr574-certificates-2026-10-13/algebraic-claims.json` | `claude/wizardly-meitner-wqn4x3-intake-1014-pr574` | `56cf868c617975eaada5b0c10dab953cc6fa2e37` | `packing/resources/web/pingyou-pr574-certificates-2026-10-13/acquisition/algebraic-claims.json` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
