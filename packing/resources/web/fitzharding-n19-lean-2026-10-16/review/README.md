# Independent Checks for the Review of Fitzharding’s s(19) Lean Proof

These seven programs were written for the stage 4 mathematical review of issue #640
(bead `think-o40t`),
[`review-2026-10-16-fitzharding-n19-lean.md`](../../../../../docs/project/reviews/review-2026-10-16-fitzharding-n19-lean.md).
Each reads the retained sources under [`../sq19/`](../sq19/) as data, uses the standard
library only, and shares no code with the source: none runs Lean, the source’s scripts
or its generators. They decide, for each `native_decide` fact whose module is in the Git
tree, the property it certifies (for the combinatorial facts, the predicate itself), and
the assertions behind some of the rest; they do not build the proof.
For the endgame and region facts a pass shows the certified property holds, not that the
native evaluator’s `true` is the kernel’s value (the review’s Independent Checks, “What a
pass shows”).

**Registered.** Each program is a first-party entry in
[`verifiers.yaml`](../../../../frontier/verifiers.yaml), with its independence record,
and each run is an evidence entry in
[`evidence.yaml`](../../../../frontier/evidence.yaml) with its coverage, cited by the
case record [`n-019.md`](../../../../frontier/n-019.md) and not by `T-194`, since each
decides a part and none builds the proof:

| Program | Verifier | Evidence entry | Coverage |
| --- | --- | --- | --- |
| `check_endpoint.py` | `V-sq19-review-endpoint` | `E-n019-fitzharding-endpoint-review` | full: the existence half |
| `check_cover_census.py` | `V-sq19-review-cover-census` | `E-n019-fitzharding-cover-census-review` | full: the cover and the census |
| `check_region.py` | `V-sq19-review-region` | `E-n019-fitzharding-region-review` | full: the nine region facts’ property |
| `check_capture_link.py` | `V-sq19-review-capture-link` | `E-n019-fitzharding-capture-link-review` | full: the twelve link facts |
| `check_endgame.py` | `V-sq19-review-endgame` | `E-n019-fitzharding-endgame-review` | full: the endgame facts’ property, 4,096 cases |
| `scan_archives.py` | `V-sq19-review-archive-scan` | `E-n019-fitzharding-archives-review` | full: the five archives’ custody |
| `count_native.py` | `V-sq19-review-native-count` | `E-n019-fitzharding-archives-review` | full: where the 4,320 facts are proved |

The review itself is recorded as the `external_review` of `T-194`’s report entry,
`E-n019-fitzharding-lean-report`, which takes `T-194` to `C1`.
On 16 October the records lane re-ran the four programs that need only the packet and
got the same output.

## What Each Decides

| Program | Decides | Native facts it covers |
| --- | --- | --- |
| [`check_endpoint.py`](check_endpoint.py) | the nineteen squares of `EndpointPacking.lean` in exact $\mathbb{Q}(\sqrt2)$: unit directions, containment in $[0, 3 + 4\sqrt2/3]^2$, a weakly separating edge normal for each of the 171 pairs; their order and values against this project’s witness `W-known-best-n019` | none (that file has none) |
| [`check_cover_census.py`](check_cover_census.py) | the 25 cells tile the centre box; the symmetry tables are induced by the frame symmetries; the capacity data; every 19-cell set reaches a census mask, one per D4 orbit; the routing; the 38 survivor images; every non-survivor mask contains an image of one of the 269 certified patterns, reading each roster from its name | `Sq19.Cover.orbit_check`, `Sq19.Assembly.CensusRoute.route_checked`, `captureIndex_checked` |
| [`check_region.py`](check_region.py) | each capture target, moved by the frame shift, lies in its box of `Hull.prob`, with the source’s `sqCheck` and `wallCheck` transcribed and `impliedOK` replaced by vertex enumeration of the target polygon, every one of the 76 checked bounded and nonempty; Wainwright’s configuration lies in H | the nine `Sq19.Capture.Region.*` facts |
| [`check_capture_link.py`](check_capture_link.py) | a capture state’s cells are the census cells of its roster shifted by $-\sigma$, the reflected roster is its census mask, the base windows are at least $\pi/2$ wide, and the pieces tile owner 12’s window; reads the state’s files from its release archive | `cells_ok`, `mask_ok`, `width_checked`, `tile_checked` of S3435, S3438 and S3442 (twelve) |
| [`check_endgame.py`](check_endgame.py) | for each of the 4,096 endgame cases, on the whole box H: the three Farkas multipliers are nonnegative, $S_1 > 0$, and the endpoint margin’s derivative along each direction prefix is nonnegative, with its own first-order Taylor models and outward rounding | the 2,304 `Sq19.Endgame.Reduction.Shard*.case*` facts, and the 1,792 cases they reduce |
| [`scan_archives.py`](scan_archives.py) | a release archive’s SHA-256 against `SHA256SUMS`, every member against `expected/generated-sources.sha256`, no trust-widening construct (`axiom`, `sorry`, `implemented_by`, `extern`, `unsafe`, `opaque`, `skipKernelTC`, `elab`, `macro`, `syntax`, `#eval` and the like), and the theorems proved `by native_decide` | counts only |
| [`count_native.py`](count_native.py) | where each of the 4,320 logged native facts is proved: in the Git tree, in an archive (from `scan_archives.py`’s outputs), or nowhere | accounting only |

The endgame program transcribes the source’s row definitions (`Endgame/RowsH.lean`,
`RowsAH.lean`, `PhiExpr.lean`, `Combine.lean`, `ReductionCases.lean`) by hand, and
`check_region.py` transcribes `sqCheck` and `wallCheck` (`Capture/ToHull.lean:52-59`)
and their mirror forms line for line, replacing only `impliedOK`; both are independent
in evaluation, not in formulation. The census coverage check assumes that
pattern `P<hex>`’s roster is the cell set of mask `0x<hex>`; the rosters are in the
census archive.

## Running Them

From `packing/`, with the project interpreter, `P` the packet directory and `W` a
scratch directory outside the checkout. The first four need only the packet:

```sh
P=resources/web/fitzharding-n19-lean-2026-10-16
.venv/bin/python3 -I $P/review/check_endpoint.py $P/sq19 witnesses/known-best/n-019.yaml
.venv/bin/python3 -I $P/review/check_cover_census.py $P/sq19
.venv/bin/python3 -I $P/review/check_region.py $P/sq19 witnesses/known-best/n-019.yaml
.venv/bin/python3 -I $P/review/check_endgame.py $P/sq19 --cases all
```

The rest read the release. Download `SHA256SUMS` (its SHA-256 is in the packet’s
[README](../README.md#the-release-archives)), then take the five archives one at a time:
download, scan, and for a capture state extract its directory and check its link facts.
`count_native.py` needs all five scans.

```sh
R=https://github.com/ofitzharding/sq19/releases/download/v1.0.0
curl -sSfL -o $W/SHA256SUMS $R/SHA256SUMS
for A in S3438 S3442 S3435 census survivors; do
  curl -sSfL -o $W/a.tar.xz $R/sq19-generated-$A.tar.xz
  .venv/bin/python3 -I $P/review/scan_archives.py $P/sq19 sq19-generated-$A.tar.xz $W/a.tar.xz \
    --sums $W/SHA256SUMS --json $W/scan-$A.json
  case $A in S34*)
    mkdir -p $W/x-$A && tar -xJf $W/a.tar.xz -C $W/x-$A --wildcards "*Sq19Lean/Capture/$A/*"
    .venv/bin/python3 -I $P/review/check_capture_link.py $P/sq19 $W/x-$A ${A#S} ;;
  esac
  rm $W/a.tar.xz
done
.venv/bin/python3 -I $P/review/count_native.py $P/sq19 $W/scan-*.json
```

Each prints one line per check and `PASS` or `FAIL`, exits 0 only on a pass, and writes
its full result with `--json OUT`. `check_endgame.py --cases all` takes about two and a
half minutes on one core; the archive scan about 90 seconds per 500 MB extracted. Download
first rather than piping `curl` into the scan: a stream held open that long was reset by
the proxy once.

## Results on 16 October 2026

- `check_endpoint.py`: pass; minimum containment clearance 0; 31 pairs in contact on
  their best axis; the witness has the same squares in the same order (largest
  difference $4.4 \times 10^{-16}$, the decimals’ rounding).
- `check_cover_census.py`: all 21 checks pass; 177,100 sets, no miss; 22,475 orbits;
  tree masks at census indices 1, 2, 5423, 5453 and capture masks at 3435, 3438, 3442;
  177,062 non-survivor masks covered and no survivor image covered.
- `check_region.py`: the nine facts pass; all 76 target polygons are bounded and
  nonempty (a check added after the PR’s review A); Wainwright’s configuration lies in H
  with margin $7.0 \times 10^{-5}$.
- `check_capture_link.py`: the twelve facts pass for the three states, every file read
  matching its listed digest.
- `check_endgame.py --cases all`: 4,096 of 4,096 pass. Lower bounds over H: multipliers
  0.701147, 0.7009, 0.999596; $S_1$ 1.49126; slope 0.0383454. The margin at $\theta = 0$ is zero
  to $10^{-46}$. 25,564 random cone points (floating point) gave a smallest margin of
  $1.2 \times 10^{-4}$.
- `scan_archives.py`, all five archives, each downloaded to scratch, scanned and
  deleted: S3438 151 members, S3442 235, S3435 756, census 540, survivors 430 (2,112,
  10,155,114,248 bytes of source); every archive digest equals `SHA256SUMS`, every member
  its listed digest, none unlisted, no forbidden construct; 87, 145, 441, 1,077 and 417
  native theorems.
- `count_native.py` over the five scans: of the 4,320 logged native facts, 2,328 are
  proved in the Git tree and 1,992 only in the archives, none is missing, and 6 are in
  both (the three `State.lean` files the archives also carry, byte-identical); 170 native
  theorems are built but unused by the final theorem.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
