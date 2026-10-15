# Francisco Couzo’s Exact Certificates at b85dee2

[Issue #583](https://github.com/jlevy/squares/issues/583) and its update
[#586](https://github.com/jlevy/squares/issues/586) report exact rational packings at n
= 154, 211, 241 and 302, inside the case corpus, and at n = 339, 379, 380, 381 and 382,
beyond it, from
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/b85dee2b964e7f7fb9f765227e60c44cdcd3aa4d/certificates)
at `b85dee2b964e7f7fb9f765227e60c44cdcd3aa4d` (tree
`661aa077abc38b80cb4e89db487f0c6a271b393b`, committed 2026-10-13T17:30:53Z, parent
`06d8db2`), the head of `master` when retrieved.
#583 was filed at 2026-10-13T14:11Z and pins `4596670` (13:53:57Z); #586, filed at
17:37Z, pins `b85dee2` and replaces #583’s certificates at 154, 339, 379, 380 and 382
and, with tighter certificates of the same arrangements, at 211 and 241. #583’s 302 and
381 are unchanged at `b85dee2`, byte for byte.
Neither issue has comments or edits.

[Issue #570](https://github.com/jlevy/squares/issues/570), filed 2026-10-12T23:19Z, pins
`1b31bc907d2d881c6962739b6b40cd10b1cd5a9c`, which GitHub does not serve: the API answers
that no such commit exists, and the raw files are not found.
Its 154 certificate has the SHA-256 the issue states for it, `5335cb3b…`, which is the
digest of `certificates/n154.cert` at `4596670`, #583’s 154. Its 379, printed as
19.953542593650 with SHA-256 `ac463682…`, is in no commit this packet could read, and
#583 and #586 replace it.

| n | Exact side of the certificate | Rounded up at 16 places | Printed by | Requested |
| --- | --- | --- | --- | --- |
| 154 | `12921206577132631050071241337979/1000000000000000000000000000000` | 12.9212065771326311 | #586: 12.921206577133 | yes |
| 211 | `7496779456987003085666602828823/500000000000000000000000000000` | 14.9935589139740062 | #586: 14.993558913975 | yes |
| 241 | `15987117095150238758321758129189/1000000000000000000000000000000` | 15.9871170951502388 | #586: 15.987117095151 | yes |
| 302 | `3574002770080892868927770707857/200000000000000000000000000000` | 17.8700138504044644 | #583: 17.870013850405 | yes |
| 339 | `7843211074020413644369172117/414429522933500000000000000` | 18.9253193607033334 | #586: 18.925319360704 | yes |
| 379 | `3465647601101642309045474807/173685927478500000000000000` | 19.9535313621228366 | #586: 19.953531362123 | yes |
| 380 | `10836602188256857315809318661/542872123174250000000000000` | 19.9616110786711857 | #586: 19.961611078672 | yes |
| 381 | `19974977397656713743580918961689/1000000000000000000000000000000` | 19.9749773976567138 | #583: 19.974977397657 | yes |
| 382 | `16910059023533815728370360359/846022698554500000000000000` | 19.9877131576091932 | #586: 19.987713157610 | yes |
| 176 | `552305489072091180922030085613/40000000000000000000000000000` | 13.8076372268022796 | the certificates README: 13.807637226803 | no |
| 344 | `4679490218760187481582497297/246370329898500000000000000` | 18.9937246935864824 | the certificates README: 18.993724693587 | no |
| 375 | `621684579194845249501508200799/31250000000000000000000000000` | 19.8939065342350480 | the certificates README: 19.893906534236 | no |
| 376 | `995203401287300299369534803489/50000000000000000000000000000` | 19.9040680257460060 | the certificates README: 19.904068025747 | no |
| 378 | `9971259846922534078917474447089/500000000000000000000000000000` | 19.9425196938450682 | the certificates README: 19.942519693846 | no |

Each certificate gives `n` unit squares, each a rational centre in $[0, S]^2$ and a
rational $t = \tan(\theta/2)$, in a square of the stated side, in Evan Daniel’s format.
Each exact side rounds up, at the 12 places its printer uses, to the side printed.
Neither issue prints a digest; the per-certificate metadata file `certificates/nN.json`
states each certificate’s full SHA-256 and exact side, and all 18 such files at the pin
agree with their certificates.
The issues call 154, 211, 241, 302 and 381 exact optima from Evan Daniel’s exact contact
solver, and 339, 379, 380 and 382 rational witnesses of their decimal packings with
centres dilated by $1 + 10^{-11}$ at 339 and $1 + 10^{-12}$ at the others.
The certificates README at the pin calls 176, 375, 376 and 378 exact optima and 344 a
rational witness, and describes the dilation as adaptive, starting at $1 + 10^{-12}$.

The prints that #586 replaces, all of them #583’s, are each above the certificate here:
154 at 12.922499814643 (also #570’s), 211 at 14.993558914123, 241 at 15.987117095169,
339 at 18.927383638495, 379 at 19.953531531603, 380 at 19.973553606628 and 382 at
19.988600568289. Those certificates are in Git history at `4596670`; the
[issue-583 packet](../couzo-issue583-2026-10-13/README.md) retains them.

The per-count ledger of 14 October records the five certificates no issue names as
reports of their own, publications in a watched repository dated by their first commits
(176 at `93570ef`, 375 and 376 at `4596670`, 344 and 378 at `b85dee2`). The records lane
of 14 October therefore added them to the declaration’s `requested` counts, refroze the
claim record against `main` at `e1f14898d`, where the case at 154 had moved to Evan
Daniel’s #552 (T-160), and wrote their beyond-horizon claims into the claims record.

## What the Commit Changes

The [issue-561 packet](../couzo-certificates-2026-10-12/README.md) pinned `0fa0e0d`.
Four commits follow it:

- `93570ef` (2026-10-12T21:31:43Z) changes 176, 344, 375 and 378, and deletes the
  `found/` archive;
- `4596670` (2026-10-13T13:53:57Z), #583’s pin, adds 154, 211, 302 and 382 and changes
  241, 339, 375, 376, 378, 379, 380 and 381;
- `06d8db2` (15:47:39Z) changes no certificate and deletes `publications/20261012/`;
- `b85dee2` (17:30:53Z), the pin, changes 154, 211, 241, 339, 344, 378, 379, 380 and
  382\.

Against `0fa0e0d` that is 14 certificates, four added and ten changed, and this packet
retains all 14:

- **Requested, nine:** 154, 211, 241, 339, 379, 380 and 382, first committed in the pin,
  and 302 and 381, first committed in `4596670`.
- **Named by no issue, five:** 176 (first committed in `93570ef`), 375 and 376 (in
  `4596670`), and 344 and 378 (in the pin).
  Each is a newer certificate than the one #561 names at its count.

The other 59 certificates of the pin are unchanged since `0fa0e0d`. This packet pins
each one by digest and names the retained copy as `identical_to`: the issue-561 packet’s
at 156, 237, 271 and 338; the
[issue-506 packet’s](../couzo-certificates-2026-10-11/README.md) at 175, 304, 305, 308,
340 and 343; the [issue-488 packet’s](../couzo-certificates-2026-10-10/README.md) at
132, 209, 270 and 303; and the
[issue-476 packet’s](../couzo-exact-certificates-2026-10-09/README.md) at the other 45.
In all the commit holds 73 certificates.
For every one of them the `certificates/README.md` table prints the 16 hex digits its
SHA-256 starts with, its exact side and that side rounded up at 12 places, and all three
agree with the file.

The sources were retrieved at 2026-10-14T04:44Z, from a full clone.

## Retained Here

`devtools.acquire_source` wrote the packet from a checkout at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
107 files, 3,201,177 bytes.

The repository states no licence: its tree has no licence file, and neither `README.md`
nor `certificates/README.md` states reuse terms.
The 14 certificates under `source/certificates/` (639,272 bytes) are retained as factual
data under the owner decision of 2026-10-09
([Retained Factual Data](../known-best-packings/README.md)). The two READMEs, the 18
per-certificate metadata files `certificates/nN.json` and the 14 changed decimal pose
files `nN.txt` are pinned by digest only.
No prose or program is copied.

## Exact Replay

Only the retained certificates enter geometry decisions.
They go through the maintained two-route kernel of `devtools.evand_arrangement_reports`,
which the issue-476, issue-488, issue-506 and issue-561 imports also used: `sqpack`’s
exact witness verifier and the independent rational corner checker, each deciding every
wall and every pair over $\mathbb{Q}$ after an exact half-angle conversion.
The replay covers all 14 certificates, the five no issue names among them.
Each count runs a positive job, a duplicate-square control and an outside-container
control, each in its own child process.

All 14 positives pass both routes.
Both routes refuse all 28 controls, each on the overlap or the wall it was built to
break. In every positive the two routes find the same least wall clearance and the same
least pair gap: exactly `1/200000000000000000000` ($5 \times 10^{-21}$) and just under
$10^{-20}$ for the nine exact optima at 154, 176, 211, 241, 302, 375, 376, 378 and 381,
and exactly `1/1000000000000000` ($10^{-15}$) for the five rational witnesses, whose
least pair gaps are $5.79 \times 10^{-12}$ at 339, $9.01 \times 10^{-12}$ at 344,
$1.20 \times 10^{-12}$ at 379, $8.29 \times 10^{-13}$ at 380 and $7.34 \times 10^{-13}$
at 382. The 42 jobs made 4,444,044 pair decisions in 1,473.51 route CPU seconds and
2,536.72 job wall seconds, summed; the longest job, the positive at 376, took 157.79
seconds. The run used one worker on a machine shared with other import lanes, at a load
average between 9 and 20 on four cores, so the wall times are well above the CPU times.
`certify --workers 1` decided 28 jobs, through the positive at 378, from 05:28Z to
05:58Z on 14 October, and was then stopped by the session’s limit on a background
command; the other 14 were decided one at a time by the same `decide-job` command it
runs, from 06:07Z to 06:21Z, and `certify --finished` assembled and admitted the receipt
from all 42 job outputs, as it admits any.
A fresh serial `check --replay` decided all 42 jobs again, equal to the retained rows
apart from timing, in 34 minutes 3 seconds from 06:41Z (24 minutes 59 seconds of CPU).
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. The third exact route, `devtools.check_half_angle_area`, is a separate review
lane and did not run here.
No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes every certificate against the
record as it stood when the issues were read (`main` at `aeef99ef0`, 14 October 2026).
`check-claims` rebuilds it, each case ceiling from its holder’s own retained packet and
the issue-561 sides from their own packet.
Every other register entry at 154, 176, 211, 241 and 302 is above the case ceiling
there, and open pull requests #585, #587 and #591 change no ceiling at these counts;
open pull request #574 is a report of its own, compared below.

| n | Case ceiling, holder | Below it by | Other open reports at the count | Smallest |
| --- | --- | --- | --- | --- |
| 154 | 12.9230702023011408, Nate Chaoweeraprasit (T-136) | $1.86 \times 10^{-3}$ | #552 (Evan Daniel), above by $1.36 \times 10^{-3}$; #593 (Mishapolk), above by $1.29 \times 10^{-3}$ | this certificate |
| 211 | 14.9963367213363157, Daniil Ostashev (T-149) | $2.78 \times 10^{-3}$ | #575 (Ostashev), above by $1.35 \times 10^{-4}$; #593: the same exact side; #574 (PingYou Ltd), above by $2.78 \times 10^{-3}$ | this certificate and #593, one side |
| 241 | 15.988132439524990848590591447359, Couzo improved by Evan Daniel (T-098) | $1.02 \times 10^{-3}$ | #575, above by $1.72 \times 10^{-5}$; #593: the same exact side; #574, above by $1.02 \times 10^{-3}$ | this certificate and #593, one side |
| 302 | 17.8720298490811800, SQUISH improved by Evan Daniel (T-146) | $2.02 \times 10^{-3}$ | #564 (BuddenPing), above by $2.62 \times 10^{-4}$; #593, above by $2.62 \times 10^{-4}$; #574 (PingYou Ltd), above by $2.62 \times 10^{-4}$ | this certificate |
| 176 (not requested) | 13.8128562532770564, Nate Chaoweeraprasit (T-151) | $5.22 \times 10^{-3}$ | #561, above by $2.54 \times 10^{-10}$; #575 and #593, one exact side, below by $1.18 \times 10^{-2}$; #574, $1.38 \times 10^{-19}$ below #575 | #574 and #593, undecided |

Issue #593, filed 2026-10-14T01:40Z, after both issues, prints each side as the `%.16f`
rendering of the IEEE double nearest it, and the comparison reads those prints with the
importer’s `binary64` rounding, under which the frozen record leaves 211 and 241
undecided between this certificate and #593. Its certificates at
[`46f638c`](https://github.com/Mishapolk/square-packing-records/tree/46f638ce0537beeb1bad24242c6a3d357eecd9ee/certificates),
fetched for this comparison with the digests the issue states and not retained, have
exactly this packet’s sides at 211 and 241, with other poses, and at 154 exactly the
side of the certificate #583 and #570 report there.
The #552 side is the exact $S'$ the issue states, and the #564 side the exact side of
BuddenPing’s refined certificate, as the issue states it; #575’s sides are read at the
40 places it prints.
PingYou Ltd’s open pull request [#574](https://github.com/jlevy/squares/pull/574),
opened 2026-10-13T00:13Z, states the case ceilings’ certificates at 211 and 241, and
#575’s at 176, each tightened so that its side is smaller by about one part in
$10^{20}$, and at 302 an exact algebraic side, $17.87027538255505966957\ldots$; its
40-place prints, rounded up, and that decimal are read as printed, and its certificates
were not read here. At 176 the frozen record leaves #574 and #593 undecided.

Beyond the corpus there is no case record.
Each side is compared with the grid, with the row the source register tracks as current
at its count (Couzo’s issue-506 certificate, verified, read within one unit of its last
printed place), and with every other open report:

| n | Tracked row (issue 506) | Below it by | Other reports | Smallest |
| --- | --- | --- | --- | --- |
| 339 | 18.929433883808 | $4.11 \times 10^{-3}$ | #584 (Evan Daniel), above by $1.58 \times 10^{-3}$; #583, above by $2.06 \times 10^{-3}$ | this certificate |
| 379 | 19.953572709539 | $4.13 \times 10^{-5}$ | #583, above by $1.69 \times 10^{-7}$; #570, above by $1.12 \times 10^{-5}$ | this certificate |
| 380 | 19.987440766556 | $2.58 \times 10^{-2}$ | Kevin Fang’s `078789a` certificate, above by $1.52 \times 10^{-2}$; #583, above by $1.19 \times 10^{-2}$ | this certificate |
| 381 | 19.992663288464 | $1.77 \times 10^{-2}$ | Fang’s `078789a`, above by $1.99 \times 10^{-3}$; #582 (Miles Gray), above by $1.06 \times 10^{-2}$ | this certificate |
| 382 | none |  | the grid’s 20, $1.23 \times 10^{-2}$; Fang’s `078789a`, above by $1.77 \times 10^{-3}$; #583, above by $8.87 \times 10^{-4}$ | this certificate |
| 344 (not requested) | 18.994353244944 | $6.29 \times 10^{-4}$ | #561, above by $1.72 \times 10^{-5}$ | this certificate |
| 375 (not requested) | 19.906335145009 | $1.24 \times 10^{-2}$ | #561, above by $7.71 \times 10^{-3}$; #584, below by $1.15 \times 10^{-2}$ | #584 |
| 376 (not requested) | 19.910276586885 | $6.21 \times 10^{-3}$ | #561, above by $8.82 \times 10^{-4}$ | this certificate |
| 378 (not requested) | 19.942541777355 | $2.21 \times 10^{-5}$ | #561, above by $1.65 \times 10^{-5}$ | this certificate |

Kevin Fang’s 380, 381 and 382 are in
[TheSnakeFang/squarepack-certs](https://github.com/TheSnakeFang/squarepack-certs/tree/078789a4cfd36f915f1bfbe76d742413d79b2965)
at `078789a`, which #583 cites; no issue reports them and the register holds none of
them. Their sides are compared at the 12-place prints #583 gives, which the exact sides
of the files at `078789a` round up to.
Miles Gray’s #582 side is the exact 19.985624661051481 of the certificate attached to
that issue.
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the five requested counts for `check_source_coverage`.

The five certificates no issue names are each an import of their own
(`result-import.md`, stage 1). This import compares them here and registers none of
them. Each is smaller than the certificate #561 names at its count, and each but 176 and
375 is the smallest known there.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
The issues say every certificate passes this repository’s `sqpack.verify` at `562fdbd`
and Evan Daniel’s `verify_cert.py` at `31523f8`; those runs are the author’s, and
neither program of the source ran here.
Novelty, local or global optimality and rigidity are not established.

## Credit and Licence

Francisco Couzo wrote the source, which states no licence; the certificates are kept as
factual data and nothing of the source is relicensed.
The issues ask that the constructions each started from be credited.
At 154 it is Evan Daniel’s arrangement of #552, which descends from the author’s earlier
155 with one square removed, continued through the author’s browser refinement, native
basin hopping and exact finishing.
At 211 and 241 they are Daniil Ostashev’s arrangements, continued with native search and
refinement, and at 302 BuddenPing’s, continued with native basin hopping and refinement.
339 and 379 continue the author’s L-border constructions of #506; the latest step at 339
used the browser’s `fq` search, and at 379 native SLP refinement.
380, 381 and 382 continue Kevin Fang’s published arrangements through browser and native
searches, and #586 asks that his construction credit be kept.
Evan Daniel’s optimizer, contact solver and verifier, David Ellsworth’s search and
refinement ideas, and this repository’s `sqpack.verify` checker were used.
The issues state that the search implementation, the verification orchestration and the
issues used OpenAI Codex, that earlier search work used Claude Code, and that the author
directed the work.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source couzo-certificates-2026-10-13 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-13 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-13 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-13 check --replay
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 1` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
