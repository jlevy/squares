# Amund Kristiansen’s Fourteen Certificates at 334 to 504

[Issue #798](https://github.com/jlevy/squares/issues/798), opened 2026-10-24T19:03:14Z
by amundsk, reports fourteen upper bounds beyond the case corpus, credited to Amund
Kristiansen, in the gist
[amundsk/e4df936fb09c68446598d4c8309d0166](https://gist.github.com/amundsk/e4df936fb09c68446598d4c8309d0166/c9be7b70e2220c2eccb2c5ea746094bc85dda405).
The packet pins the revision the issue names, `c9be7b70e2220c2eccb2c5ea746094bc85dda405`
(tree `dd45a2617b79781d50f0551ab1eacb654cae2678`, committed 2026-10-24T19:01:54Z), 80
seconds before the issue.
It is the gist’s only revision: the GitHub API lists no other version, and the head was
the pin when it was read at 20:27Z and again at 20:56Z on 24 October, with no comments.

Each count’s certificate, `s<N>_amund.cert`, gives N unit squares, each a rational centre
and a rational $t = \tan(\theta/2)$, in an open square of the stated side, in Evan
Daniel’s format, the format of #728’s and #755’s certificates.
The issue says each is a dilation certificate made with Daniel’s
`search/packer/dilate_cert.py` at evand/square-packing `7982d7a`, on macOS arm64 with
Python 3.14.6, from the binary64 packing beside it, `s<N>_amund.input.txt`: centres and
box scaled by $1 + 10^{-12}$, coordinates rounded to rationals and each angle rounded to a
rational half-angle tangent, so every square is exactly unit.

| n | The issue prints, rounded up | Exact side rounded up at 16 places | Disposition |
| ---: | --- | --- | --- |
| 334 | 18.786944251907 | 18.7869442519060770 | row |
| 338 | 18.887926955871 | 18.8879269558703380 | row |
| 343 | 18.976291436857 | 18.9762914368560103 | row |
| 372 | 19.806121548598 | 19.8061215485970012 | not recorded: above Couzo’s `43f666c` |
| 376 | 19.884256884304 | 19.8842568843030243 | row |
| 377 | 19.906977592561 | 19.9069775925607300 | row |
| 379 | 19.950579117727 | 19.9505791177264006 | row |
| 382 | 19.987567257068 | 19.9875672570670576 | row |
| 412 | 20.822875656790 | 20.8228756567896269 | not recorded: above Couzo’s `43f666c` |
| 416 | 20.889554050378 | 20.8895540503772176 | row |
| 457 | 21.887025665808 | 21.8870256658079141 | row |
| 458 | 21.888719382533 | 21.8887193825328288 | row |
| 502 | 22.891715605670 | 22.8917156056692718 | row |
| 504 | 22.921326029542 | 22.9213260295413714 | row |

Each exact side is the certificate’s header, which the issue prints as S′ for every count;
[acquisition/claims.json](acquisition/claims.json) keeps them.

## What the Issue Reports

- **Credit name.** “Amund Kristiansen (GitHub @amundsk)”. The gist’s README says the
  same: “(Amund Kristiansen, 2026-10-24)”.
- **Claims.** Fourteen upper bounds, each the certificate’s exact side rounded up at 12
  places, and each below the side Francisco Couzo’s `964ee2b` certificate states at the
  count (#763), which the issue calls the smallest public bound it found. It compared the
  register, the open issues through #757, Mishapolk/square-packing-records at `7e82c64` and
  the public Kaggle notebooks through 23 October.
- **Digests.** It prints the SHA-256 of every certificate and of every binary64 input; all
  28 are the digests of the pinned files.
- **Checks.** The author reports that Daniel’s two exact checkers at `7982d7a`,
  `verify_cert.py` (separating axes) and `verify_cert2.py` (polygon intersection), accept
  every certificate, with a table of least wall clearances ($5.986 \times 10^{-13}$ to
  $1.735 \times 10^{-12}$), least pair separations and close pairs. A third check, a local
  workbench’s rational certifier on the float packings, is unpublished. The issue says the
  two public checkers share an author and the certificate format, which also made the
  certificates. No source program ran here.
- **Not done.** No exact KKT solve, rigidity or local-optimality analysis; only the upper
  bounds are claimed.
- **Method and lineage.** Every packing was found from #763’s certified packing at the
  same count, credited as #763 credits it. Matched one to one with it by an optimal
  assignment on centres, best of the eight symmetries, 372 and 412 move no square beyond
  0.1, so the issue calls them refinements, and the other twelve move 1 to 29 squares
  beyond 0.1, new packings found from it. At n ≤ 400 each round relaxed 4,096 perturbed
  variants in a float32 GPU batch through a box slightly below the starting side and
  polished the best 96 with Daniel’s `fq` quench; above 400 Daniel’s `explore.py` ran for
  15 to 30 minutes from the starting packing.
- **AI assistance.** “Yes. As at #755: the searches, the certificates and this report
  were done by Claude (Anthropic), working in Claude Code at my direction, using Evan
  Daniel’s open-source engine and checkers and Francisco Couzo’s published packings as
  starting points.”

[acquisition/issue.json](acquisition/issue.json) keeps the issue as read at 21:03Z on 24
October: never edited and no comments.

## Source Custody

Neither the gist nor the issue states a licence. In a
[comment on #755](https://github.com/jlevy/squares/issues/755#issuecomment-6388401978)
(2026-10-24T19:13:49Z) the author dedicates to the public domain under CC0 1.0 “every
certificate, input packing and README in the gist of #798
(`amundsk/e4df936fb09c68446598d4c8309d0166`, revision
`c9be7b70e2220c2eccb2c5ea746094bc85dda405`)”, so the packet retains all 29 files.
[acquisition/licence-answer.json](acquisition/licence-answer.json) keeps the comment as
read at 21:03Z on 24 October, never edited.

`devtools.acquire_source` wrote the packet from a blobless clone of the gist checked out
at the pin, from [acquisition/declaration.json](acquisition/declaration.json);
[acquisition/sources.json](acquisition/sources.json) is the record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
Its scope is the gist’s 29 files, 1,104,636 bytes, each retained under [source/](source/)
and bound to its Git blob at the pin: the fourteen certificates (819,319 bytes), the
fourteen binary64 inputs (282,128 bytes) and the README (3,189 bytes).
No file is stored compressed.

The tools the issue names are Daniel’s, at `7982d7a`, which the
[#728 packet](../evand-n303-2026-10-22/README.md) read; that packet and the
[n229 packet](../evand-n229-dilation-2026-10-17/README.md) pin `verify_cert.py`,
`verify_cert2.py` and `dilate_cert.py` by digest. They were not run.

## Report Order

The [ledger of 24 October for issue 798](../../../campaign/issue-intake/upper-bounds-issue798-20261024/README.md)
walks the fourteen counts from starts frozen at `main` `2ed0ea740` (#795’s merge), so each
start holds the current beyond-horizon row (#763’s, the `964ee2b` push’s notebook rows,
or #670’s at 382) and Göbel’s construction beside it.
One earlier publication states a side below the start at any of the counts: Francisco
Couzo’s
[`franciscouzo/square-packing@43f666c`](https://github.com/franciscouzo/square-packing/tree/43f666c23933fbc5cc418fa4e851218268fed0ed),
committed at 00:55:44Z on 24 October and made public by the push `964ee2b..1c17153` at
06:10:44Z, more than twelve hours before the issue. Its import is think-gn29’s; the walk
reads it as a publication at the 8 counts where its `certificates/best/nN.cert` differs
from `964ee2b`’s, each at its header side.
Mishapolk/square-packing-records at `7e82c64` and evand/square-packing at `659ee62`, both
unchanged since their last reads, state nothing below the start at these counts, and
#797’s L-band packings lie far above it.

- **Twelve rows.** At 334, 338, 343, 376, 377, 379, 382, 416, 457, 458, 502 and 504 the
  certificate is below every earlier report at its count, by $1.244 \times 10^{-5}$ at 457
  to $8.750 \times 10^{-3}$ at 334, and below Göbel’s construction by
  $9.94 \times 10^{-3}$ (416) to $0.720$ (457). At 376, 377, 416, 458, 502 and 504 the
  margin is to `43f666c`’s side rather than to the row on `main`.
- **372 and 412.** `43f666c` certifies 19.806121548578 at 372, $1.91 \times 10^{-11}$
  below this certificate, and 20.822875655538 at 412, $1.25 \times 10^{-9}$ below, so by
  the owner’s rule neither is recorded. Both certificates are retained, compared in the
  claim record, and not replayed.
- **382.** The earlier report is the certificate Couzo reported in #670, which `964ee2b`
  holds byte for byte, not #763, which does not claim the count.

No claim restates an earlier report: none lies within one unit of the 12th place below
the side it beats.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each certificate against the
record at `main` `2ed0ea740` (24 October 2026): the grid, Göbel’s construction
(`devtools.goebel_construction`), the count’s current beyond-horizon row at its print,
and `43f666c`’s side where it differs from `964ee2b`’s.
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the twelve requested counts, the record `check_source_coverage` reads the rows against.
`check-claims` rebuilds both.

## Exact Replay

The twelve recorded certificates go through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, as #755’s did: `sqpack`’s exact witness verifier
and the independent rational corner checker
(`devtools.check_rational_witness_independent`), each deciding every wall and every pair
over $\mathbb{Q}$ after an exact half-angle conversion.
Each count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on two workers.

Every positive passes both routes, and both routes refuse every control: the duplicate
square as an overlap of squares 0 and 1, and the translated square as outside the
container.
Each certificate clears every wall and pair by what its issue table prints, to the
printed digits: the walls by $5.986 \times 10^{-13}$ (338) to
$1.735 \times 10^{-12}$ (376), and the pairs by $1.199 \times 10^{-12}$ (338) to
$2.340 \times 10^{-12}$ (376), on both routes, as a $10^{-12}$ dilation gives.
The 36 jobs made 6,028,026 pair decisions in 845.53 route CPU seconds and 1,289.15 job
wall seconds, summed; the longest job took 60.3 seconds.
`certify --workers 2` took 669 seconds of wall time on 24 October 2026, under `nice` on a
four-core host shared with other lanes at a load average of about 7, and
`check --replay` decided the receipt again in 906 seconds on one process.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

**Sharp controls.** The receipt’s controls are gross, so `sharp-controls`
(`devtools.upper_bound_sharp_controls`) takes each certificate to exact contact and
$10^{-30}$ past it on both routes: the side lowered by its least far-wall clearance, the
tightest pair closed along the face normal that separates it, every square moved toward
its near wall, one square of a tight pair and the square nearest a wall enlarged, and a
duplicated square. All 132 controls, 11 at each of the twelve counts, come out on both
routes as the module’s rules require: at contact a moved square or side is accepted with
the decisive margin exactly 0 and an enlarged square is refused for its shape alone, past
contact every one is refused by the margin the rules set, and the duplicate is refused.
They took 3,114 CPU seconds, 3,242 seconds of wall time on one
process, and `sharp-controls --check` decided them again.
`receipts/sharp-controls-nNNN.json` keeps the verdicts, one file a count.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code, and no source program ran here.

## Pose by Pose

Each `measure/identity-nNNN.json`, written by `devtools.measure_identity`, measures the
packing against `964ee2b`’s at the count, which the issue names as the search’s start
(#670’s certificate at 382, which `964ee2b` holds byte for byte), and against `43f666c`’s
at the 8 counts where that differs. A measurement, which decides nothing:

- **Against `964ee2b`.** The optimal assignment, best under the identity at every count,
  reproduces the issue’s lineage table exactly: the largest move, from 0.00745 at 412 to
  0.871 at 504; the squares beyond a tenth, none at 372 and 412 and 1 to 29 at the other
  twelve; the squares beyond $10^{-2}$; and the tilted squares of both packings. Nearest
  centres pair the two one to one at every count but 376, 377 and 504.
- **The word.** The record keeps the word refinement for a pairing in which no square
  moves beyond a tenth. So 372 and 412 refine `964ee2b`’s packings, and the other twelve
  are other arrangements of them, found from them, as the issue says.
- **Against `43f666c`.** At 416, 458, 502 and 504 `43f666c`’s packing pairs best under
  another symmetry of the box (7, 7, 5 and 1), where this one pairs with `964ee2b`’s under
  the identity, which supports the issue’s account that the search started from
  `964ee2b`’s. At 377 `43f666c` re-certifies `964ee2b`’s packing, so the figures are the
  same. At 376 all three share one frame, and this packing is nearer `43f666c`’s (11
  squares beyond a tenth, at most 0.239) than `964ee2b`’s (19, at most 0.785); the
  author is asked, informationally, where the 376 search started. At 372 and 412 it moves
  no square, or two, beyond a tenth of `43f666c`’s.

## What Is Not Established

Each certificate establishes a finite upper bound at its exact side, nothing more.
The issue claims no local optimality, KKT condition or rigidity, and none was examined.
Novelty, local or global optimality and rigidity are not established.

## Credit

The issue and the gist’s README credit Amund Kristiansen (GitHub @amundsk).
The issue says each search started from Francisco Couzo’s certified packing at the count
at `964ee2b` (#763), credited as #763 credits it, and used Evan Daniel’s `fq` quench or
basin explorer, `dilate_cert.py` and checkers.
`964ee2b`’s index credits those packings to Couzo’s own search at 343, 379 and 412; Couzo refining
Kirill Tymchishin’s notebook packing at 334, and refining Vladislav Lavrentev’s “CUDA
Packing Search” v11 packings at 372, 416, 457, 458 and 502; Tymchishin’s notebook at 376;
kyleluecke’s at 377; alexchilton’s at 338 and 504; and Couzo with Kevin Fang’s seed and
construction at 382.
The bibliography credit therefore reads
`Kristiansen after Couzo, Lavrentev, Tymchishin, alexchilton, kyleluecke, Fang, Daniel, Levy`,
keeping the project link of #763’s chain
([attribution.md](../../../../attribution.md#credit-text-and-lineage)).
Per-row credit beyond the horizon stays the owner’s open question from #686.
The searches, the certificates and the report were done by Claude (Anthropic) in Claude
Code at the author’s direction, as the issue discloses.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source amundsk-issue798-2026-10-24 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports amundsk-issue798-2026-10-24 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports amundsk-issue798-2026-10-24 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports amundsk-issue798-2026-10-24 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports amundsk-issue798-2026-10-24 sharp-controls --check
uv run --frozen --all-extras --group dev python -m devtools.intake_ledger check campaign/issue-intake/upper-bounds-issue798-20261024
```

`check` admits the receipt structurally; only `--replay` decides the geometry again, and
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job directory.
Each `measure/identity-nNNN.json` is written by `devtools.measure_identity` and names its
inputs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
