# Incremental Intake Evidence, 19 October 2026

W1 intake closeout is owned by think-9nse under think-xmxb.
This packet records the five actions in `sweep-initial.txt`: 5 unowned actions, 0
resolved blockers, 312 owned items and 45 watched repositories.
It extends the [18 October packet](../intake-20261018/README.md); its receipts remain a
dated snapshot. The sweep also compared Kingbird’s 19 October capture with the retained
catalogue: 0 counts differed and 0 were below the record.

## Dispositions

| Action | Evidence and owner | Remaining work |
| --- | --- | --- |
| [#678](https://github.com/jlevy/squares/issues/678) | `issue-678.json`: Couzo reports 85 improved upper bounds, counts 204–998, at `7b6c87e129cf80b5ff9847b90b47fd30b4563c54`; think-xu4d. The three retained comments include the author’s seed clarification and our custody acknowledgement. | Retain the 83 new witnesses, compare in report order against the classical envelope, price exact replay and independent review, and review the promised source correction. Seed custody is established as described below; scientific assertions remain unverified. |
| [#603 comment](https://github.com/jlevy/squares/issues/603#issuecomment-6255103888) | `603-comment.json`: Fang announces draft v0.8 and public Lean project at `947bdae`; think-494l under think-0esw. | Review the note and separate Lean source, bind statements and axioms, and price replay. [Acknowledgment](https://github.com/jlevy/squares/issues/603#issuecomment-6257671390) is posted. |
| [evand head](https://github.com/evand/square-packing/commit/ddf09e382ab3c63675476503d51d1a405bb2f7e6) | `evand-source-inventory.json`: five commits after `5ca0dc3`. `4b456fe` reports the stronger filled L-shape bound, owned by think-f8py; `13da782` reports the staircase/Ryu bound, owned by think-pf37. | Source review and retained theorem evidence. The other three commits package the proof route and change pages, viewer and credit presentation. Mathematical authorship and formalization credits stay distinct. |
| [Couzo head](https://github.com/franciscouzo/square-packing/commit/7b6c87e129cf80b5ff9847b90b47fd30b4563c54) | `couzo-source-inventory.json`: 543 paths from all commit-file pages; same report as #678, think-xu4d. | Whole-source custody and classification remain with the import owner. #672/think-2vjc is an earlier report and keeps its separate ownership. Manifest credit is source evidence; it does not decide project discovery credit. |
| [Fang head](https://github.com/TheSnakeFang/squarepack-certs/commit/0e9be7961773aa78b879c4ee6ba584a67e2e5513) | `fang-source-inventory.json`: only README and `note/fang-2026-n2-n-1.md` change; think-494l. | Review with #603. This commit adds no certificate. The mixed-step form of Theorem 2 in the note and the announced single-step Lean form require separate statement checks. |

These are intake dispositions and assignments.
No certificate ran here, no Lean build ran here, and no bound, verification rating or
confirmation rating changes in this packet.
Source claims of exact replay or standard axioms remain author reports until the owning
review records its evidence.
Path inventories establish changed-file scope; they do not establish certificate
validity or a complete source-content audit.

The [retained #678 comments](issue-678-comments.json) extend the read-through to 19
October at 15:31:25 UTC. The body is unchanged; its source issue capture was updated at
14:22:50 UTC, before the separately retained acknowledgement.
[The author](https://github.com/jlevy/squares/issues/678#issuecomment-6269517369)
corrected the stale Evan source pin and identified `e90993…` as the gzip hash.
The [custody receipt](issue-678-n260-seed-custody.json) binds the
[original 4,112-byte gzip](issue-678-n260-seed-14a9af8.cert.gz) at Evan Daniel’s
immutable `14a9af8be4a8b8a8328c3eb6b486a2e553380193` revision to its decompressed hash
and exact header.
[Our correction](https://github.com/jlevy/squares/issues/678#issuecomment-6270970266)
acknowledges those byte bindings.
Joost de Winter’s construction credit (#668) and Evan Daniel’s exact-form certificate
credit remain distinct source reports.
Float conversion, the intermediate search chain, packing identity, analytic optimality
and feasibility of the 85 new bounds remain unreviewed.
The promised pin/hash-kind/credit patch is not linked in this retained thread.
T-196 remains the earlier submission already merged through #676; #675 stays separately
owned by think-pvav.
No new witness replay or result registration occurred.

## Manual Sources and Limits

`manual-source-receipt.json` retains the hand-read receipt at 00:54 UTC on 19 October.
UnitSquare’s page and results data match the retained bytes.
SQUISH’s #401 comment 6043191866 remains unchanged at its 7 October timestamp; the issue
is closed. The initial sweep’s two “not checked” entries describe its automatic/manual
boundary; this receipt supplies the separate manual checks.

The initial sweep is retained from its heading onward; shell startup diagnostics are
omitted. It precedes these dispositions.
The online closing attempt in `sweep-closing-raw.txt` found zero items without an owner
and zero resolved blockers, but GitHub API and Git DNS failures left 49 sources
unchecked. The offline closing check in `sweep-closing-offline.txt` likewise found zero
unowned items and zero resolved blockers; it deliberately skipped remote reads.
Neither is a clean final online sweep.
Rerun that sweep when Git repository access recovers.
Source witnesses, bulk replay and assurance decisions remain with the named import
owners.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
