# Independent Finite-Feasibility Review of the 259-Square Certificate

The
[Stage 4 review](../../../../docs/project/reviews/review-2026-11-21-geiserx-1040-n259.md)
accepts the two exact rational encodings attached to
[issue #1040](https://github.com/jlevy/squares/issues/1040): each describes 259 unit
squares inside the same rational box, and each of all 33,411 pairs separates exactly.
The encodings have identical vertex sets and imply $s(259) \le 16.590016439230$.

The review does not establish optimality, priority, identity with an earlier
floating-point packing, novelty, significance, or full Witness/v2 envelope conformance.
[scope.json](scope.json) records this boundary and the authorship and independence facts
for the integration records.

The authoring lane was Codex (OpenAI), strongest tier (`tbd-strong-max`), maximum
reasoning, separately prompted.
It wrote the checker without reading a producer or project checker implementation.
Its two methods share a rational scalar parser, CPython integer arithmetic, the
authoring session, and the elementary separating-line implication.
Those shared assumptions are disclosed in the review.

## Programs and Evidence

| File | Purpose |
| --- | --- |
| [verify_n259.py](verify_n259.py) | Exact deciding program used in the final run. Reads the original JSON and YAML independently, runs the controls, checks every square and pair, then compares the encodings. |
| [frozen/verify_n259.py](frozen/verify_n259.py.txt) | Exact deciding program used before the findings freeze. The reviewer’s final replay copy sorted the `pathlib.Path` import. |
| [predeclared-controls.json](predeclared-controls.json) | Acceptance rule and 16 control cases declared before either deciding run; 28 method-specific outcomes are required. |
| [frozen/findings-freeze.json](frozen/findings-freeze.json) | Findings fixed at 16:59:25.864539 UTC on 2026-11-21, before any prior review or implementation for this result was read. |
| [frozen/results.json](frozen/results.json), [frozen/run.stdout](frozen/run.stdout), [frozen/run.stderr](frozen/run.stderr), [frozen/exit-status.json](frozen/exit-status.json) | Original blind-run outputs, preserved byte for byte. |
| [results.json](results.json), [run.stdout](run.stdout), [run.stderr](run.stderr), [exit-status.json](exit-status.json) | Final full-run outputs, preserved byte for byte. Both deciding methods and all controls passed; worker and guard exited zero. |
| [receipt-audit.json](receipt-audit.json) | Original administrative audit receipt, including frozen identities, agreement of geometric result fields, exact displayed decimal, and resource-observation coverage. It makes no new geometric decision. |
| [lint.stdout](lint.stdout) | Recorded isolated Ruff lint result for the final checker and the original administrative audit. |
| [retention.json](retention.json) | Digests and byte counts of unchanged public artifacts; explicit inventory of host-specific material retained externally. |
| [source-sha256.txt](source-sha256.txt) | Exact input identities used by the replay recipe below. |
| [source-link-check.json](source-link-check.json) | Both public source URLs returned HTTP 200 to a header-only request during overlay preparation. |
| [check_public_packet.py](check_public_packet.py) | Administrative integrity and local-link check for this public packet. It never runs the mathematical verifier. |
| [public-integrity-check.json](public-integrity-check.json) | Administrative check of the public overlay: all preserved identities and local links pass; no geometric rerun. |

The only mathematical source inputs read before the findings freeze were the original
certificate data, issue body, and the first three lines of the original author’s README
identifying the half-angle convention and asserting the bound.
The review describes the reporting-only reading after the freeze.

The public files are a selection from the original external review archive.
Raw machine paths, launchers, environment settings, process identities and guard logs
remain in that archive.
Its filename and SHA-256 are recorded in `retention.json`. The unchanged freeze includes
the digest of a private launcher, `run.sh`; the public integrity check reports that one
member as retained externally.
The other four members bound by the freeze are present beside it.

## Source Identity

The source is the author’s
[packing-259.zip attachment](https://github.com/user-attachments/files/35066502/packing-259.zip).
This packet cites that URL and the exact member identities.
It does not depend on an in-repository link to a separate custody packet.

| Archive member | Bytes | SHA-256 |
| --- | ---: | --- |
| `retained-data/upper/n259/packing.json.gz` | 30,015 | `bfd1b2890ad846efe030113f5e4535a79f786ed6c2f0371257dd342ddd48970c` |
| `retained-data/upper/n259/witness.yaml` | 765,842 | `3d4bd6326ed60439aa3fc933bfbfc4b5716e4de8d181ce837161b97fdc88a031` |

These digests identify bytes across the external source boundary.
They neither prove the geometry nor reconstruct the attachment’s custody chain.

## Integration replay

The original final replay program is retained byte for byte as
[`verify_n259.py.txt`](verify_n259.py.txt), alongside the pre-freeze code.
The runnable `verify_n259.py` copy follows the repository’s Python style floor.
It was replayed after integration and produced identical geometry, controls, source
identities and verdicts.
[Integration receipt](integration-replay.json)

## Reproduce the Geometric Check

Start at the repository root with its Python 3.14.7 environment prepared.
Set `TMPDIR`, `CARGO_TARGET_DIR` and `UV_CACHE_DIR` to task directories on the mounted,
writable external scratch volume, following `AGENTS.md`. The source download and new
receipt stay in that scratch directory.
The checker imports only the standard library and installs no dependencies.

```bash
set -e
: "${TMPDIR:?Set TMPDIR to a task directory on the external scratch volume}"
review_repository_root="$(pwd)"
review_packet=packing/resources/web/geiserx-1040-n259-review-2026-11-21
mkdir -p "$TMPDIR/n259-review-inputs"
curl --fail --location \
  --output "$TMPDIR/packing-259.zip" \
  https://github.com/user-attachments/files/35066502/packing-259.zip
unzip -jo "$TMPDIR/packing-259.zip" \
  retained-data/upper/n259/packing.json.gz \
  retained-data/upper/n259/witness.yaml \
  -d "$TMPDIR/n259-review-inputs"
(
  cd "$TMPDIR/n259-review-inputs"
  shasum -a 256 -c "$review_repository_root/$review_packet/source-sha256.txt"
)
packing/.venv/bin/python3 -B "$review_packet/verify_n259.py" \
  --source "$TMPDIR/n259-review-inputs" \
  --out "$TMPDIR/n259-review-results.json"
```

Read the checker exit status before using the new receipt.
A successful run atomically replaces it; a failed run exits nonzero and leaves any
previous receipt in place.
The checker has a 120-second alarm.
For the original implementation, substitute `$review_packet/frozen/verify_n259.py.txt`
in the same command.
On this Mac, the recorded runs used one worker with an observe-only memory guard; future
local runs should follow the host’s resource policy.

The final recorded output was:

```
Controls passed: 28 outcomes
Center check: 33411 pairs accepted in 0.684s
Corner check: 33411 pairs accepted in 9.075s
PASS: finite feasibility; exact encodings agree; elapsed 9.950s
```

These times are execution evidence from the recorded host, not replay requirements.
The exact results and control outcomes are the acceptance evidence.

## Check Public-Packet Integrity

From the repository root, this checks preserved file identities, both receipts, the
freeze’s explicit public/private split, the review’s displayed side, and local Markdown
links. It does not download input or execute geometry:

```bash
packing/.venv/bin/python3 -B \
  packing/resources/web/geiserx-1040-n259-review-2026-11-21/check_public_packet.py
```

The original host administrative audit remains in the external archive because it
requires that archive’s raw logs.
Its retained receipt is historical evidence; this public check is the portable integrity
check for the files above.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
