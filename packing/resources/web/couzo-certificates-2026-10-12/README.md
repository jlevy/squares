# Francisco Couzo’s Exact Certificates at 0fa0e0d

[Issue #561](https://github.com/jlevy/squares/issues/561) reports exact rational
packings at n = 156, 176, 237 and 271, inside the case corpus, and at n = 338, 344, 375,
376 and 378, beyond it, from
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/0fa0e0de2ef0b414655e871b1baffcfe0d33c815/certificates)
at `0fa0e0de2ef0b414655e871b1baffcfe0d33c815` (tree
`f65aa749e20934c18dcdf6c849f3c0dce6b7f285`, committed 2026-10-12T18:26:28Z, parent
`eee88d3`). The issue was filed at 2026-10-12T18:55Z; it has no comments and its body
has not been edited.

| n | Exact side of the certificate | Rounded up at 16 places | The issue prints |
| --- | --- | --- | --- |
| 156 | `12979165853834276453965882038847/1000000000000000000000000000000` | 12.9791658538342765 | 12.979165853835 |
| 176 | `42253500388043689581217825957/3060154296728500000000000000` | 13.8076372270559608 | 13.807637227056 |
| 237 | `15902947773658185869705573326239/1000000000000000000000000000000` | 15.9029477736581859 | 15.902947773659 |
| 271 | `16948992356451205603226618436627/1000000000000000000000000000000` | 16.9489923564512057 | 16.948992356452 |
| 338 | `9453166404926046689995693165509/500000000000000000000000000000` | 18.9063328098520934 | 18.906332809853 |
| 344 | `83284325592732658265440964873/4384829811311500000000000000` | 18.9937418729194340 | 18.993741872920 |
| 375 | `581837142778534347520704447657618356033117642159/29235669412085804585614997608579500000000000000` | 19.9016186213272502 | 19.901618621328 |
| 376 | `1244059358531167002713366954627/62500000000000000000000000000` | 19.9049497364986721 | 19.904949736499 |
| 378 | `28547984384116369335179568707/1431512228978500000000000000` | 19.9425361559696001 | 19.942536155970 |

Each certificate gives `n` unit squares, each a rational centre in $[0, S]^2$ and a
rational $t = \tan(\theta/2)$, in a square of the stated side, in Evan Daniel’s format.
Each exact side rounds up, at the 12 places the issue prints, to the side it prints, and
each file’s SHA-256 is the digest the issue states.
The issue calls 156, 237, 271, 338 and 376 exact optima from Evan Daniel’s exact
contact solver, and 176, 344, 375 and 378 rational witnesses of their decimal packings
with centres dilated by $1 + 10^{-11}$, $1 + 10^{-12}$, $1 + 10^{-10}$ and
$1 + 10^{-12}$. The certificates README at the pin still describes every rational
witness as dilated by $1 + 10^{-12}$; the issue says the author corrected that sentence
after the review of #506, and the README at `b85dee2` describes an adaptive dilation.

## What the Commit Changes

The [issue-506 packet](../couzo-certificates-2026-10-11/README.md) pinned `337078c`.
Three commits follow it, all on 12 October:

- `a7067d7` (17:55:52Z) adds 176 and changes 156, 237, 271, 338, 344, 375, 376 and 378;
- `eee88d3` (18:07:42Z) changes 344;
- `0fa0e0d` (18:26:28Z), the pin, changes 375.

Against `337078c` that is nine certificates, one added and eight changed, exactly the
nine the issue names, and this packet retains all nine.
The other 60 certificates of the pin are unchanged since `337078c`.
This packet pins each one by digest and names the retained copy as `identical_to`: the
issue-506 packet’s at 175, 304, 305, 308, 339, 340, 343, 379, 380 and 381; the
[issue-488 packet’s](../couzo-certificates-2026-10-10/README.md) at 132, 209, 270 and
303; and the [issue-476 packet’s](../couzo-exact-certificates-2026-10-09/README.md) at
the other 46. `acquire_source --check` compares those bytes again on every run.

The issue’s replay script, manifest, receipt and issue text were committed after the
pin, at `e9eb44b` (18:35:46Z) under `publications/20261012/`, and deleted at `06d8db2`
on 13 October. They are not retained: the script fetches over the network, and no source
program runs here.

The sources were retrieved at 2026-10-14T04:44Z, from a full clone.

## Retained Here

`devtools.acquire_source` wrote the packet from a checkout at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
83 files, 2,990,980 bytes.

The repository states no licence: its tree has no licence file, and neither `README.md`
nor `certificates/README.md` states reuse terms.
The nine certificates under `source/certificates/` (380,164 bytes) are retained as
factual data under the owner decision of 2026-10-09
([Retained Factual Data](../known-best-packings/README.md)). The two READMEs, the nine
changed decimal pose files `nN.txt` and the web-app submission record
`found/web/a87a2fa7fd11f1295eff8016b0a8c1a1.{cert,json,txt}` the issue cites for 375 are
pinned by digest only.
No prose or program is copied.

## Exact Replay

Only the retained certificates enter geometry decisions.
They go through the maintained two-route kernel of `devtools.evand_arrangement_reports`,
which the issue-476, issue-488 and issue-506 imports also used: `sqpack`’s exact witness
verifier and the independent rational corner checker, each deciding every wall and every
pair over $\mathbb{Q}$ after an exact half-angle conversion.
The replay covers all nine certificates.
Each count runs a positive job, a duplicate-square control and an outside-container
control, each in its own child process.

All nine positives pass both routes.
Both routes refuse all 18 controls, each on the overlap or the wall it was built to
break. In every positive the two routes find the same least wall clearance and the same
least pair gap: exactly `1/200000000000000000000` ($5 \times 10^{-21}$) and just under
$10^{-20}$ for the five exact optima at 156, 237, 271, 338 and 376, and exactly
`1/1000000000000000` ($10^{-15}$) for the four rational witnesses, whose least pair gaps
are $4.16 \times 10^{-12}$ at 176, $1.20 \times 10^{-12}$ at 344 and 378, and
$7.61 \times 10^{-11}$ at 375.
The 27 jobs made 2,519,208 pair decisions in 601.97 route CPU seconds and 939.01 job
wall seconds, summed; the longest job, the outside-container control at 378, took 97.82
seconds. `certify --workers 1` decided 26 jobs between 05:01Z and 05:15Z on 14 October,
on a machine shared with other import lanes, and was then stopped by a restart of the
container; the 27th, the outside-container control at 378, was decided by the same
`decide-job` command it runs, and `certify --finished` assembled and admitted the
receipt from all 27 job outputs, as it admits any.
A fresh serial `check --replay` decided all 27 jobs again, equal to the retained rows
apart from timing, in 18 minutes 17 seconds from 06:22Z (14 minutes 5 seconds of CPU).
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. The third exact route, `devtools.check_half_angle_area`, is a separate review
lane and did not run here. No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes every certificate against the
record as it stood when the issue was read (`main` at `aeef99ef0`, 14 October 2026).
`check-claims` rebuilds it, each case ceiling from its holder’s own retained packet.
Every other register entry at 156, 176, 237 and 271 is above the case ceiling there.
Open pull requests #585, #587 and #591 change no ceiling at these counts; open pull
request #574 is a report of its own, compared below.

| n | Case ceiling, holder | Below it by | Other open reports at the count | Smallest |
| --- | --- | --- | --- | --- |
| 156 | 12.9791726136444261, Daniil Ostashev (T-149) | $6.76 \times 10^{-6}$ | #593 (Mishapolk): the same exact side; #574 (PingYou Ltd), below by $1.30 \times 10^{-19}$ | #574 and #593, undecided |
| 176 | 13.8128562532770564, Nate Chaoweeraprasit (T-151) | $5.22 \times 10^{-3}$ | #575 (Daniil Ostashev) and #593, one exact side, below by $1.18 \times 10^{-2}$; #574, $1.38 \times 10^{-19}$ below #575 | #574 and #593, undecided |
| 237 | 15.9029496076778317, SQUISH improved by Couzo (T-140) | $1.83 \times 10^{-6}$ | #593, below by $2.43 \times 10^{-4}$; #574, below by $1.59 \times 10^{-19}$ | #593 |
| 271 | 16.9491166878150100, Nate Chaoweeraprasit (T-151) | $1.24 \times 10^{-4}$ | #593: the same exact side; #574, below by $1.69 \times 10^{-19}$ | #574 and #593, undecided |

Issue #593, filed 2026-10-14T01:40Z, after this one, prints each side as the
`%.16f` rendering of the IEEE double nearest it, whose last places such a double does
not fix: its prints at 156 and 271 lie $2.5 \times 10^{-16}$ and $1.2 \times 10^{-15}$
from the exact sides. The comparison reads those prints with the importer’s `binary64`
rounding, under which this certificate and #593 cannot be told apart at 156 and 271.
Its certificates at
[`46f638c`](https://github.com/Mishapolk/square-packing-records/tree/46f638ce0537beeb1bad24242c6a3d357eecd9ee/certificates),
fetched for this comparison with the digests the issue states and not retained, have
exactly this packet’s sides at 156 and 271, with other poses.
Issue #575’s 176 side, 13.79587231843640726…, is read at the 40 places it prints;
#593’s 176 certificate has the same exact side, and its 237 certificate the side
$15.9027050578663667994\ldots$
PingYou Ltd’s open pull request
[#574](https://github.com/jlevy/squares/pull/574), opened 2026-10-13T00:13Z, states
this packet’s certificates at 156, 237 and 271, and #575’s at 176, each tightened so
that its side is smaller by about one part in $10^{20}$; its 40-place prints, rounded up,
are read as printed, and its certificates were not read here.
At 156, 176 and 271 the frozen record leaves #574 and #593 undecided: #574 is about
$10^{-19}$ below the certificate it tightens, and #593’s 16-place prints cannot be told
from it.
Daniil Ostashev’s #562 names a 176 packing of side 13.808663234387 that it does not
request; Couzo’s 176 continues it.

Beyond the corpus there is no case record. Each side is compared with the grid and with
the row the source register tracks as current at its count, Couzo’s issue-506
certificate, verified, read within one unit of its last printed place:

| n | Tracked row (issue 506) | Below it by | Other open reports | Smallest |
| --- | --- | --- | --- | --- |
| 338 | 18.906436500552 | $1.04 \times 10^{-4}$ | none | this certificate |
| 344 | 18.994353244944 | $6.11 \times 10^{-4}$ | none | this certificate |
| 375 | 19.906335145009 | $4.72 \times 10^{-3}$ | #584 (Evan Daniel), 19.882451030481…, below by $1.92 \times 10^{-2}$ | #584 |
| 376 | 19.910276586885 | $5.33 \times 10^{-3}$ | none | this certificate |
| 378 | 19.942541777355 | $5.62 \times 10^{-6}$ | none | this certificate |

[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the five for `check_source_coverage`.
The same author’s later certificates at 344, 375, 376 and 378, and at 176, are smaller
still: they are retained in the
[b85dee2 packet](../couzo-certificates-2026-10-13/README.md), which no issue names at
those counts.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
The issue says all nine pass this repository’s `sqpack.verify` at `562fdbd` and Evan
Daniel’s `verify_cert.py` at `31523f8`; those runs are the author’s, and neither program
of the source ran here. Novelty, local or global optimality and rigidity are not
established.

## Credit and Licence

Francisco Couzo wrote the source, which states no licence; the certificates are kept as
factual data and nothing of the source is relicensed.
The issue asks that the constructions each started from be credited.
At 156 and 176 they are Daniil Ostashev’s arrangements, continued with the author’s basin
hopping and refinement, the 176 search also through his web app.
At 237 and 271 they are Nate Chaoweeraprasit’s SQUISH arrangements, continued with the
author’s basin hopping and Evan Daniel’s `fq` refinement; 237 improves the author’s own
T-140 certificate.
At 344 it is Kevin Fang’s 344 (#484), continued from the packing reported in #506.
338, 375, 376 and 378 continue the author’s L-border constructions of #506: 338 and 375
from his 303, itself from SQUISH’s (#401), 376 from his earlier 304 and 378 from his 306;
the new refinements used Evan Daniel’s `fq` at 338 and 376 and basin hopping at 378.
The latest step at 375 came through the author’s browser web app with David Ellsworth’s
search, after a native search improved its starting packing (record
`a87a2fa7fd11f1295eff8016b0a8c1a1`, received 2026-10-12T18:16:59Z).
Evan Daniel’s optimizer, contact solver and verifier, David Ellsworth’s refinement and
search ideas, and this repository’s `sqpack.verify` checker were used.
The issue states that the continuing search and application work, the source audit, the
exact verification orchestration and the issue were assisted by OpenAI Codex, that
earlier search code and submissions were prepared with Claude Code, and that the author
directed the work.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source couzo-certificates-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-12 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-12 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-12 check --replay
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 1` writes a new receipt from a fresh job directory,
and `register-plan` prints the record entries the import needs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
