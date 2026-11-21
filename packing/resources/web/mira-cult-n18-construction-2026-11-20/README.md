# Mira Cult’s Six-Tilt Construction at n = 18

This packet retains one exact coordinate certificate for eighteen unit squares at
$H = (7+\sqrt7)/2$. The retained independent checker accepts every wall and pair over
$\mathbb Q(\sqrt7)$ and refuses all 32 controls.
The packet concerns finite construction feasibility; the full optimality claim of
[issue #1050](https://github.com/jlevy/squares/issues/1050) remains a separate intake.

## Source and Custody

The source is
[Mira-Cult/math](https://github.com/Mira-Cult/math/tree/78bec6aacebf304d942a9225e16c2f18165778ff/notes/geometry/unit-square-packing-18)
at commit `78bec6aacebf304d942a9225e16c2f18165778ff`, committed 2026-11-20T16:11:46Z,
tree `78adf8421830ff820da24bbee6b159c075780c28`. The single retained input is
[source/notes/geometry/unit-square-packing-18/replay/six-tilt18.json](source/notes/geometry/unit-square-packing-18/replay/six-tilt18.json):
775 bytes, Git blob `0f4842e1fa016b989c55fa8e98b0b57b00e5915a`, SHA-256
`bda21ee2ed4382bf4b33201f546449eee37d6ce66c3d87205c80a7b37f780ba0`.

The GitHub connector returned the file as base64 at that exact commit.
Decoding preserves its bytes; both the recomputed Git blob and SHA-256 match the pinned
metadata and the source’s published
[SHA256SUMS](https://github.com/Mira-Cult/math/blob/78bec6aacebf304d942a9225e16c2f18165778ff/notes/geometry/unit-square-packing-18/replay/SHA256SUMS).
[acquisition/retrieval.json](acquisition/retrieval.json) records the retrieval method
and content identities.
[acquisition/declaration.json](acquisition/declaration.json),
[acquisition/sources.json](acquisition/sources.json) and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) follow
`devtools.acquire_source`’s one-source packet contract.
These records were assembled from the API retrieval, without a local source checkout.
The remaining repository is identified by the pinned commit.

## Attribution and Licence Status

Credit Mira Cult for the six-tilt construction.
The pinned source states that Mira Cult directed the research and that OpenAI’s GPT-6.2
Astra developed the lower bound and exact construction.
It acknowledges Hämäläinen’s earlier packing at the same side and claims the matching
lower bound as its contribution; this certificate establishes another layout at that
side.

The source folder states no licence, and the root README’s licence references cover
other results. Issue #1050 was opened by the maintainer from a public post.
This packet retains the coordinate certificate under the recorded
[Retained Factual Data policy](../known-best-packings/README.md#retained-factual-data):
complete certificates and coordinates may be retained with their upstream identities and
exact digests. Retention grants no licence and relicenses nothing.
The packet acquires no producer prose or program and runs no producer program.

## Independent Replay

The checker and its exact field module are already retained in the
[Stage 4 review packet](../mira-cult-n18-1050-review-2026-11-20/README.md).
The review froze both before opening producer programs.
Their SHA-256 values were checked against that freeze before this run:

| Program | SHA-256 |
| --- | --- |
| `r1050_construction.py` | `401a7e9fa45ec60cfe10675a97e333bb80cf67da6bde6a6cab4d5a4211611454` |
| `r1050_q7.py` | `7f0937a6cace9f3f266904354583bb84bf33197f87852ea6865875459cc84828` |

The run used project CPython 3.14.7 with `-B -I`, one checker process, and a memory
guard attached in `--observe-only` mode before the checker began.
[receipts/replay.json](receipts/replay.json) records the exact command, input and
program digests, process identity and exit codes.
The checker and guard both exited zero.
[receipts/construction.json](receipts/construction.json) records:

- 18 squares, six tilted, at exact side $H$, with orthonormal frames
- 72 wall inequalities and 153 square pairs accepted exactly
- 24 touching pairs and 12 wall contacts
- all 32 controls refused, including side $H-10^{-30}$, each touching pair closed by
  $10^{-30}$, every tilted square made axis-parallel and a duplicated square

The whole launch, including guard startup, took 1.823 seconds of wall time.
[receipts/memory-guard-summary.json](receipts/memory-guard-summary.json) records ten
samples, normal host pressure throughout, at most one workload process, maximum tree
footprint 0.01 GiB as rounded by the guard, and no interventions.
The raw private guard journal stays in the task’s dedicated external scratch.

From the repository root after integration, with the approved project interpreter in
`$PY` and a fresh output path in `$OUT`:

```bash
R=packing/resources/web/mira-cult-n18-construction-2026-11-20
C=packing/resources/web/mira-cult-n18-1050-review-2026-11-20/programs
"$PY" -B -I "$C/r1050_construction.py" \
  --construction "$R/source/notes/geometry/unit-square-packing-18/replay/six-tilt18.json" \
  --out "$OUT"
```

This is the six-tilt artifact whose digest the Stage 4 review records.
The review’s eight-tilt transcription is a different input.
The record’s existing house is `W-known-best-n018`, credited to Hämäläinen and verified
by `E-lifted-q7-upper`; its eight tilted squares distinguish it from this construction
under every box symmetry.
This packet makes no registry, house, lower-bound or proof-status change.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
