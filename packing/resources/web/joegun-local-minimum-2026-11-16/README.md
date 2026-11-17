# JoeGun’s Local-Minimum Check at 5971b95

This packet retains part of
[JonathanGun/square-packing-upper-bounds](https://github.com/JonathanGun/square-packing-upper-bounds/tree/5971b95f7141bb9bd1bac4b501bc3a094fb84822)
at `5971b95f7141bb9bd1bac4b501bc3a094fb84822` (committed 2026-11-16T09:28:39Z), the
only child of `0aac839e`, the head that
[intake-watch.yaml](../../../campaign/intake-watch.yaml) read through for the import of
[issue #1001](https://github.com/jlevy/squares/issues/1001).
It adds `local-minimum/`, the inputs, logs, reports and certificates of a local-minimum
check the author ran after filing, and edits the README and `LICENSE.md` to match.
The author said the same on #1001 in a comment at 09:29:26Z
([6912585795](https://github.com/jlevy/squares/issues/1001#issuecomment-6912585795)) and
edited the issue’s body at 09:29:27Z to add the section.
Intake lane L188 (think-664l) fetched the repository at 10:27Z on 16 November 2026, when
`git ls-remote` read this commit as the only head.

The five certificates are unchanged: every file outside `local-minimum/`, `README.md`
and `LICENSE.md` has the Git blob it had at `0aac839e` and at `bc10ce4`, the pin of the
[joegun-upper-bounds-2026-11-16 packet](../joegun-upper-bounds-2026-11-16/README.md),
which retains them and from which the record registers T-305 to T-309.
Nothing here is registered, and no rung, house or credit changes.

## What the Source Claims

The author ran `exactsolve.py` from Evan Daniel’s
[evand/square-packing](https://github.com/evand/square-packing) at `6067db5` (MIT) on
all five packings, in 80-digit arithmetic. The README and #1001 say it gave a result for
four:

| n | KKT point | Local minimum | Rigid | Flat motions | Least contact force | Side at the exact point |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | yes | yes | no | 52 | 6.66 × 10⁻⁸ | 11.801753890364738880 |
| 204 | no result | no result | no result | | | |
| 232 | yes | yes | no | 110 | 7.28 × 10⁻⁷ | 15.759531623540125992 |
| 264 | yes | yes | no | 155 | 6.75 × 10⁻⁷ | 16.773807597982933201 |
| 305 | yes | yes | no | 132 | 2.55 × 10⁻⁶ | 17.945762359467513364 |

- **The verdict.** At the four counts the tool reports a KKT point, every contact force
  positive and the balance residual 0, and its verdict “local minimum of S, strict
  modulo N exact flat motions”. A flat motion slides some squares at the same side, so
  the author says none of the four is rigid.
- **At 204.** The load rests on 30 corner-on-corner touches; the tool found no smooth
  equilibrium and its Newton step diverged, so there is no result either way.
- **The object.** The result is about the exact touching point near each witness
  (`n-NNN-input.exact.txt`), not the witness: the witnesses are loosened copies of it,
  their sides larger by 1.9 × 10⁻¹¹ to 4.0 × 10⁻⁹. At 232 the tool moved 22 loose squares
  into the contact system, and the least gap between pairs that do not touch is 1.5 ×
  10⁻¹² there.
- **The tool’s certificates.** It wrote its own rational certificate of each exact point
  (`n-NNN-input.cert`, its exact check `VALID`), and the author does not claim those
  lower sides.
- **The assurance.** The author says the check is numerical, at 80 digits, and not a
  proof; one tool by one author made it; and this repository’s `local_rigidity` code was
  not run.
- **What it replaces.** The README read “They are upper bounds only.
  We make no optimality or rigidity claim.” and now reads “They are upper bounds.
  We make no optimality claim.” Its list of what was not done drops “No local-optimality,
  rigidity or KKT analysis.” for “No local minimum result at n = 204.” and “No proof of
  the local minimum results. They are numerical.” The issue’s body, as the import lane
  read it, said “We make no optimality, rigidity or KKT claim.”, and the edit of
  09:29:27Z drops that sentence.
- **AI assistance.** The README says AI agents also ran the local minimum check, and
  that JoeGun directed the work.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json): `README.md`, `LICENSE.md`,
the whole of `local-minimum/` and Evan Daniel’s MIT notice, 31 files, 30 retained under
[source/](source/) and the notice pinned by digest against the byte-identical `LICENSE`
the [issue 845 packet](../evand-issue845-2026-10-29/README.md) retains, as the earlier
packet pins it.
The rest of the tree is the earlier packet’s and is pinned by the commit alone.

For each of 127, 232, 264 and 305, `local-minimum/` holds six files: the solver’s input
(`n-NNN-input.txt`, the side and each square’s centre and angle in degrees, which
`make-input.py` writes from the decimal pose beside the certificate), its log
(`n-NNN-exactsolve.txt`), its report (`n-NNN-input.json`), the exact point
(`n-NNN-input.exact.txt`), its contact equations (`n-NNN-input.contacts.json`) and its
rational certificate (`n-NNN-input.cert`). At 204 it holds the input, the log and the
report. `make-input.py` is retained as data and was never run here, and no other
program of the source or of the solver ran in writing this packet.

## Against the Record

The record’s regularization of the five new houses on 16 November
([the runs](../../../cases/regularized_drawings/think-0y9m-2026-11-16/README.md)) ran
the same solver through Evan Daniel’s driver (`devtools.regularize_evand`, at
evand/square-packing `675a5ea`) from each exact certificate, and holds what it found at
row 3 as register candidates, not admitted: a KKT local minimum below the side at 127,
232, 264 and 305, and an exact solve that failed at 204, at 80 and at 100 digits.
`test_the_sources_local_minimum_check_reaches_the_points_the_driver_holds` in
[the lane’s test module](../../../tests/test_upper_bound_reports_l187_1116.py) reads the
author’s reports through the driver’s own `solve_block` and compares them with the
driver’s retained reports:

- **The same exact points.** At the four counts the author’s exact side equals the
  driver’s in every digit both print, 63, 63, 62 and 63 decimals, and the side of the
  tool’s rational certificate of each point equals the side of the driver’s solved view
  as a fraction. Each point therefore lies 1.2175 × 10⁻¹⁰, 4.0164 × 10⁻⁹, 1.9066 × 10⁻¹¹
  and 1.9146 × 10⁻¹⁰ below its certificate’s exact side, the amounts the register’s notes
  print for the held solves: about 1.006, 273, 1.007 and 1.004 times each certificate’s
  own contraction margin, beyond it at each.
- **The same verdicts.** Status, convergence, certificate validity, the free squares, the
  promoted squares (the 22 at 232, none elsewhere), the corner-on-corner branches and the
  second-order verdict, with its count of flat motions, agree at all four.
- **The same failure at 204**, with the same 25 free squares. The jam residual, the one
  figure that differs, agrees there and at 264 to nine significant digits or more.
- **From different starts.** The author’s inputs come from the binary64 decimal poses,
  the driver’s from the exact certificates, and no input file is the same; the solver ran
  at `6067db5` for the author and at `675a5ea` for the driver.

That is context, not a registration. The four points are the candidates the owner’s RV-3
question (think-ruu2) holds, and the author claims none of their sides.
The case records’ rigidity blocks say each retained witness is not rigid, by the
translation-escape screen; the author’s “not rigid” is of the exact point, by its flat
motions.

## What Is Not Established

- **A local minimum or a KKT point.** Both runs are the same solver’s numerical analysis
  at 80 digits, one author’s code at two pins; the agreement is a reproduction, not an
  independent check, and the author says it is not a proof. The record registers no
  local-minimum, KKT or rigidity statement for T-305 to T-309.
- **Anything at 204**, either way.
- **Human oversight**: no record is retained.

## Credit and Licence

The check is JoeGun’s, run with Evan Daniel’s solver; the source says AI agents ran it
under JoeGun’s direction, and the record credits people, not AI agents
([attribution.md](../../../../attribution.md)).
`LICENSE.md` at the pin, copyright 2026 JoeGun, licenses the files in `local-minimum/`
under CC BY 4.0, except `make-input.py`, which it licenses under MIT with `check.py` and
`make-pose.py`; at `bc10ce4` it named no licence for `make-pose.py`, which the earlier
packet retains under the presumption of permission for a source its author submitted
(think-cnn7). It says the licence covers the author’s own contribution and does not
change the terms of Tomáš Kodaj’s work, and that Evan Daniel’s `exactsolve.py` made the
logs and outputs, none of his code being in the repository.
The bibliography key stays **[JoeGun upper bounds 2026-11-16]**.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source joegun-local-minimum-2026-11-16 --checkout CHECKOUT
python -m devtools.acquire_source joegun-local-minimum-2026-11-16 --check
python -m pytest tests/test_upper_bound_reports_l187_1116.py -k local_minimum
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
