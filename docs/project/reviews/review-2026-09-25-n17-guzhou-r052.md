# Proof Review: Guzhou0806’s R052, `s(17) > 231001/50000`

Reviewed 2026-09-25 in worktree `w3-review` on branch `claude/n17-guzhou-r052-intake`,
off `main` at `db3f5f31c`, in
[Session 159](../../../packing/campaign/agent-sessions/session-159-n17-guzhou-r052-intake.md).
This is an adversarial correctness review of one published computer-assisted lower bound
on `s(17)`, the least side of a square containing seventeen unit squares with disjoint
interiors. The mathematics was reviewed by a Fable max sub-agent working from a clone of
the source, the replays were run by an Opus 5.5 extra-high sub-agent from the retained
packet, and the Session 159 coordinator reconciled the two.

**In one line:** the argument is Kleddamag’s reviewed reduction with a larger resource
dictionary, no error was found in it, and all four of the source’s replay modes pass
here with both full sweeps reproducing the source’s ledgers exactly; both sweeps are one
event-cell method and this repository’s native route refuses the certificate at its
engine ceilings, so the rung is `V4`/`C3`, the same as the bound it supersedes.

## 1. What Was Reviewed

The source is retained at
[`packing/resources/web/n17-guzhou-r052-2026-09-25/`](../../../packing/resources/web/n17-guzhou-r052-2026-09-25/README.md),
whose README carries the provenance, the retention decisions and the replay commands.
Its 31 retained files match their Git blobs at the pin.

| Field | Value |
| --- | --- |
| Source | `github.com/Guzhou0806/n17-square-packing` |
| Commit | `3bf1095c68a28fb9b2750fb0bc99edd5c22b7a61`, `main` on 2026-09-25 |
| Claim | `s(17) > 231001/50000 = 4.62002` |
| Certificate, decompressed | `d77743eadf7f4bf9c424549a37a4296ea3b23fceee4af8e3d774a5a07e62e825` |
| Package manifest | `2a74ea2efef6be4435b227746d3e48f93075160b77ee5a0563a2dc81996952aa` |

Files read line by line, under `certificates/R052/`:

| File | SHA-256 |
| --- | --- |
| `PROOF.md` | `b6adec4abfbd9adcc48ffd996f473b51c8fc9cb6e095481adca7b4fe5f06fb53` |
| `REPRODUCIBILITY.md` | `c5db358e6ed0343d836f939f619ce361040d42e80a393ad00f47bf6c5271388a` |
| `SOURCE_NOTICES.md` | `a70bef48342afab3848c024c30474edc2378b3f520c7c71d7371c3c28b905595` |
| `SOURCE_PIN.json` | `1945c02f6bc8c0032f5e94057610307e24293ee77f400d7ba3a51d722395d39a` |
| `verify.py` | `1ed3da8237a67857425a36857a6d4dde64e260eb5832f58b6f6b0fe4bbba4017` |
| `src/structure.py` | `28417d6bb6e6a5eb3dd98dfaebd28923390a19a1ec3d0eb5c7ad52053f3e69aa` |
| `src/geometry.py` | `f98b8690aaef397d6f088dda77e136826fb2882a85244ee5bc208d7a625fae5c` |

The Node/BigInt checker is not redistributed by the source.
It was rebuilt from the retained R038 `exact_parent_side_scan.js` (`63e858e2…`) by the
source’s deterministic recipe, and its hash `82fad041…` matched the pin.

## 2. Verdict

**Accepted.** No mathematical defect was found.
The one addition over Kleddamag’s v1.0.0 architecture, three-of-five threshold groups at
capacity $\lfloor 5/3\rfloor = 1$, is the generic $k$-of-$m$ rule already reviewed at n
= 11 in
[the Kleddamag n11 mathematics review](review-2026-09-22-kleddamag-n11-mathematics.md).
The source’s “strict kernel” is Kleddamag’s strict core, not a new device.

The review’s acceptance was conditional on both full replays passing here.
They did, so the condition is met.

## 3. The Reduction

The chain is Kleddamag’s, which
[the 2026-09-21 review](review-2026-09-21-n17-kleddamag-461300-99853.md) traced step by
step. Each step was re-read against R052’s own files:

1. Scaling: container side `L = 4613/1000`, parent side `A = 230650/231001`, so a
   packing at side `L/A = 231001/50000` rescales to parents of side `A` in the
   container.
2. D4-invariant charges fold each parent’s orientation into $\theta\in[0,\pi/4]$ without
   a common rotation.
3. A closed core strictly inside an open parent gives pairwise disjoint cores.
4. A point charges one core at most; a $k$-of-$m$ group charges at most
   $\lfloor m/k\rfloor$ cores, with inclusion–exclusion coefficients
   $(-1)^{j-k}\binom{j-1}{k-1}$, correct in both implementations (`src/geometry.py`
   lines 214–217, the rebuilt Node checker line 27).
5. Upper semicontinuity of nonnegative closed-set charges carries the open-cell minima
   to event lines and to the boundary of the legal parent-centre domain.
6. Seventeen cores each charged at least `Γ` would need `17Γ > M`; compactness makes the
   bound strict.

## 4. Replay Evidence

All four modes ran from the retained tree and exited 0. Receipts are in the packet’s
`receipts/`. Unrelated processes shared the CPU, so walls are contended readings.

| Mode | Wall | Result |
| --- | ---: | --- |
| records | 0.16 s | `PASS_R052_RECORDS` |
| containment | 3.81 s | `PASS_R052_CONTAINMENT`, least margin `4613/9240040000000000000` |
| Python full, 10 jobs | 904 s | `PASS_R052_PYTHON_FULL`, 15,721 rows, ledger `f370defb…` equal to the source’s run |
| Node/BigInt full, 10 jobs | 674 s | `PASS_R052_BIGINT_FULL`, 123 chunks, ledger `ee506dfe…` equal to the shipped `BIGINT_ROWS` |

The two fresh ledgers agree on every row’s minimum.
The Python sweep ran in a separate Python 3.14.7 environment with the source’s pinned
numpy, numba and llvmlite; the quick modes and the BigInt sweep used the project
interpreter and Node v24.19.0.

Independent checks, sharing no code with the source:

- **Counts and arithmetic.** The certificate’s D4 expansion gives 18,585 sites and 4,504
  closed groups (4,080 two-of-three, 424 three-of-five).
  The budget is 14712300904811 + 2277945754768 = 16990246659579; `Γ = ⌊M/17⌋ + 1` =
  999426274093; `17Γ − M = 2`. The active support is smaller than the dictionary: 873 of
  2,354 point orbits, 250 of 514 two-of-three orbits and 6 of 54 three-of-five orbits
  carry weight. The last row ends at `u = 207107/500000`, where
  `u² + 2u − 1 = 309449/250000000000 > 0`, so the rows cover $\tan(\pi/8)$.
- **Containment by exact minimisation.** All 62,884 strict inequalities were minimised
  exactly as quadratics in `u` over each interval, for all four sign pairs.
  All are positive, and no minimiser lies inside an interval, so the source’s endpoint
  checks are complete.
  The least margin equals the source’s. The centre envelope $A(1+2u-u^2) - 2r(1+u^2)$ is
  concave and nonnegative at both endpoints of every interval.
- **The binding rows.** Rows 15555 and 15556, the only rows that reach `Γ`, and the end
  rows 0 and 15720 were swept again with exact fractions, half-plane clipping and a
  separate range tree.
  Each equals the ledger, and a direct $k$-of-$m$ count at the minimising cell, without
  inclusion–exclusion, equals the sweep minimum.
- **Native premises.** `devtools.verify_guzhou_r052_native` loads the certificate into
  this repository’s `ParentCoreCertificate`, with site numbering matched to the source’s
  across all 568 group orbits.
  `validate_parent_core` accepts D4 symmetry, the budget, the gap, the angle cover and
  all 62,884 containment checks, minimising over whole intervals.

## 5. Findings

### F1. One method family, and the native route refuses the certificate (blocks `C4`)

The Python/Numba and Node/BigInt sweeps implement one event-cell method, which is the
[2026-09-21 review’s](review-2026-09-21-n17-kleddamag-461300-99853.md) F2 again.
The method-distinct route here is the native interval branch and bound, and its coverage
engine refuses R052 at its frozen ceilings: 8,937 atoms against 8,192, 9,261 distinct
sites against 8,192, and 44,685 member slots against 16,384
(`receipts/native/pilot-refused.json`). Those ceilings live in `interval.py` and
`threshold_interval.py`, which the n11 native audit pins at `c183cc9ab`, so raising them
is a new proof commit with a re-baselined audit.

A sizing run that lifts the ceilings in its own process certified rows 0, 15555, 15556
and 15720 with no stalls, the two binding rows exactly at `Γ`, in 1.9 to 11.1 s each
(`receipts/native/sizing-pilot.json`). A sizing receipt is never a decision.
Extrapolated from four rows, a full native run is about 8 to 49 CPU-hours.

### F2. Endpoint containment rests on an unshipped monotonicity argument (non-blocking)

`src/structure.py` lines 57–63 and `PROOF.md` §2 check containment at interval endpoints
and justify that with one sentence about monotonicity.
The sentence is correct, but unlike Kleddamag’s `independent_controls.py` no control
ships with it. The exact minimisation in §4 and the native premise check both discharge
it here.

### F3. Records mode trusts the frozen ledger (note)

`verify.py` lines 55–93 check the recorded ledger and block hashes; lines 127–162, the
two full modes, recompute every row, compare each with the ledger for equality, require
positive slab counts and re-hash the checker and candidate per chunk.
`REPRODUCIBILITY.md` discloses this.
Both full modes were run here.

The same file says the source’s original primary computation combined 13,017 directly
computed rows with 2,704 conservative lower bounds inherited from R050, and that its
Node pass recomputed all 15,721 rows.
Both replays here computed every row fresh.

### F4. Exact arithmetic in the Node checker depends on two guards (note)

Coordinates near $10^{20}$ exceed $2^{53}$ and are parsed losslessly to BigInt through
the `JSON.parse` reviver’s `context.source`, failing closed where that is unavailable;
`verify.py` line 143 requires Node 24 or later.
`Float64Array` accumulators are exact only under the `absolute < 2**50` guard; the
certificate’s unmerged absolute mass is 26783030323131, below it.

### F5. Zero slack (note)

`Γ` sits on the integer boundary and the surplus is 2 units of $10^{-12}$, reached at
rows 15555 and 15556 only; no other row is within $10^6$ units.
A one-unit error in either checker at a binding row would reverse the theorem.
Both binding rows were re-derived independently (§4).

### F6. A provenance claim that cannot be checked (note)

`SOURCE_PIN.json` says `src/geometry.py` was extracted unchanged from a file with hash
`038c0575…`. No public Guzhou0806 commit and no Kleddamag release held here contains
that file, and Kleddamag’s public `exact_mixed.py` has none of its function names.
Read line by line, it is a faithful reformatting of `exact_mixed.py` lines 43–77 plus
the n11-style generic $k$-of-$m$ count.
The claim is unverifiable, not wrong, and the full replays make it immaterial.

### F7. The upstream full-scan receipt is from an earlier snapshot (note)

`verification/R052.json` records full scans on a snapshot whose `PROOF.md` and
`MANIFEST.json` differ from the published ones (`ae9a9a44…` against `2a74ea2e…`); every
scientific file is hash-identical.
The replays here ran on the published bytes.

### F8. The source repeats an unpublished bound (note)

`README.md`, `SOURCE_NOTICES.md`, `NOTICE.md`, `RESULTS.md` and `CITATION.cff` report
that Kleddamag holds an unpublished internal strict bound of `4.62001`. The wording is
hedged, attributed to Kleddamag, and claims no priority.
It is second-hand, it is below R052, and it is not a rung here.
`RESULTS.md` and `NOTICE.md` call R050 “no longer best known” partly on that report; the
record states R050’s status from R052 alone.

## 6. The Public n = 17 Record on 2026-09-25

The fact-check the owner asked for.
The source says R052 is the strongest public lower bound for n = 17, above Kleddamag’s
`4.619791…`. That is true of every public claim this repository has found:

| Claim | Value | Source | Status here |
| --- | ---: | --- | --- |
| Guzhou0806 R052, 2026-09-25 | `231001/50000 = 4.62002` | `3bf1095c` | replayed, `V4`/`C3` |
| Guzhou0806 R050, 2026-09-24 | `4613000/998509 ≈ 4.619888` | `3bf1095c` | publication record, superseded |
| Guzhou0806 R043, 2026-09-23 | `461300/99851 ≈ 4.619884` | `3bf1095c` | publication record, superseded |
| Guzhou0806 R042, 2026-09-23 | `115325/24963 ≈ 4.619837` | `3bf1095c` | publication record, superseded |
| Kleddamag v1.0.0, 2026-09-21 | `461300/99853 ≈ 4.619791` | `a499e2c7` | replayed, `V4`/`C3`, now superseded |
| Guzhou0806 R038 | `461300000000/99974999999 ≈ 4.614154` | `32edfd3d` | retained since 2026-09-22, not replayed |
| ahyangyi/17squares v1.1.1 | `4.6136817` | `1a320e7f` | reported, not retained |
| Mira, 2026-09-07 | `4613/1000` | retained 2026-09-20 | replayed |

Kleddamag’s public repository was still at tag `v1.0.0` on 2026-09-25, with no push
after 2026-09-21. The unpublished `4.62001` would not change the ordering if published.
ahyangyi’s author describes that release as “not frontier any more”.
R052 raises the verified bound by `1142853/4992650000 ≈ 0.000229` over Kleddamag’s.
Bidwell’s packing, at `4.67553…`, remains the best known, about `0.0555` above R052.

## 7. The Rung

Under [`epistemics.md`](../../../epistemics.md):

- **`V4`.** An exact-algebraic certificate with a passing repository replay.
- **`C3`.** Repository-origin exact evidence with a certificate and a passing replay.
- **Not `C4`.** Both replays use one event-cell method, and the native interval route, a
  different `method`, has not decided the certificate (F1).

External bounds carry no `T-NNN` row in this repository, so the `C5` review mapping,
which applies to result rows, is not recorded; this review is the case file’s
`audit_record`. The case file’s verified lower bound moves from `461300/99853` to
`231001/50000`, and Kleddamag’s evidence stays as the previous bound.

**Credit.** R052 is Guzhou0806’s and the N17 project’s, produced with AI assistance.
It extends Kleddamag’s v1.0.0 mixed point and threshold parent-core architecture, and
through it Mira’s certificate and this repository’s parent-centre contract and threshold
atoms, all of which the source acknowledges.
The source discloses AI review only and claims neither priority nor optimality.

**Licence.** The source repository has no licence file.
`LICENSE_SCOPE.md` keeps the MIT licence on Kleddamag-derived code and recipes and does
not relicense third-party material; the certificate, ledgers and prose carry no general
grant and no restriction.
The packet retains them for verification on the same basis as the two earlier Guzhou0806
retentions.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
