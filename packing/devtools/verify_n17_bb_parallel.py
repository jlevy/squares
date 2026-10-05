"""Run the standing branch-and-bound verifier's node checks in parallel processes.

`devtools.verify_n17_bb_certificate` is used unchanged: its header, trigonometry, and tree
checks (T1 to T3) run once here, exactly as in its own `run_checks`, and every node is
then checked by its `Verifier.check_node`. Only the scheduling differs. The standing
verifier walks the chunks in order and keeps each open node's record for its children;
here each worker process checks whole chunks and takes a node's parent record from the
tree index of pass 1.

`check_node` reads exactly one thing from the parent: its final boxes. The index copies the
parent's `final` field from the same chunk object, and the parent's own check (in whichever
worker) confirms that field against the parent's rounds. Each worker also confirms that a
node's `final` equals the indexed copy, so the value a child inherits is the value its
parent's check accepted. The standing verifier's chunk-order condition (a parent's chunk
precedes or equals its child's) is kept as a check.

The receipt has the standing verifier's fields and counts, with a `parallel` entry added.
Only full mode is supported.

    python -m devtools.verify_n17_bb_parallel CERT_DIR --processes N --output receipt.json
"""

from __future__ import annotations

import argparse
import json
import multiprocessing
import time
from pathlib import Path
from typing import Any

from devtools import verify_n17_bb_certificate as standing

_STATE: dict[str, Any] = {}


def _check_chunk(c: int) -> tuple[int, dict[str, int], list[tuple[int, str]], int, int]:
    """Check every node of chunk c; returns the counts, failures, checked and failed."""
    verifier = _STATE.get("verifier")
    if verifier is None:
        verifier = standing.Verifier(_STATE["directory"], _STATE["name"])
        _STATE["verifier"] = verifier
    verifier.counts = {}
    finals: dict[int, Any] = _STATE["finals"]
    chunk_of: dict[int, int] = _STATE["chunk_of"]
    failures: list[tuple[int, str]] = []
    checked = failed = 0
    nodes = standing.read_named(verifier.directory, verifier.manifest["chunks"][c])["nodes"]
    for node in nodes:
        ident = node["id"]
        if node.get("final") is not None and finals.get(ident) != node["final"]:
            failures.append((ident, f"node {ident}: final differs from the pass-1 index"))
        parent: standing.Node | None = None
        if node["parent"] is not None:
            p = node["parent"]
            if chunk_of.get(p, c + 1) > c or finals.get(p) is None:
                failures.append((ident, f"node {ident}: parent {p} not loaded"))
                continue
            parent = {"final_q": [standing.box_of(box) for box in finals[p]]}
        verifier.failures = []
        try:
            verifier.check_node(standing.prepared(node), parent)
        except standing.CertificateError as exc:
            failed += 1
            verifier.failures.append(str(exc))
        failures.extend((ident, text) for text in verifier.failures)
        checked += 1
    return c, verifier.counts, failures, checked, failed


def _pass_one(
    directory: Path, name: str, cells: standing.Cells, receipt: dict[str, Any]
) -> tuple[standing.Verifier, standing.Tree]:
    """The standing verifier's checks before its node pass, in its order."""
    if not standing.constants_hold():
        raise standing.CertificateError("the pi enclosure does not hold")
    verifier = standing.Verifier(directory, name)
    receipt["pattern"] = list(verifier.manifest["header"]["pattern"])
    receipt["certificate"]["chunks"] = len(verifier.manifest["chunks"])
    verifier.check_header(cells)
    trig = standing.read_named(directory, verifier.manifest["trig"])["trig"]
    verifier.check_trig(trig, None, 1)
    tree = standing.load_tree(verifier)
    if not verifier.manifest["summary"].get("complete"):
        verifier.fail("summary.complete is false")
    return verifier, tree


def verify_parallel(
    directory: Path,
    cells: standing.Cells,
    processes: int,
    *,
    manifest: str | None = None,
    progress: bool = False,
) -> dict[str, Any]:
    """The standing verifier's full-mode receipt, with node checks spread over processes."""
    clock = time.perf_counter()
    receipt: dict[str, Any] = {
        "schema": standing.SCHEMA,
        "verifier": standing.KIND,
        "provenance": standing.PROVENANCE,
        "directory": standing.repository_path(directory),
        "cells_source": cells.source,
        "mode": "full",
        "sample": None,
        "certificate": {"manifest_sha256": manifest},
        "parallel": {"processes": processes, "driver": "devtools.verify_n17_bb_parallel"},
    }
    try:
        name = manifest or standing.manifest_from_readme(directory)
        receipt["certificate"]["manifest_sha256"] = name
        verifier, tree = _pass_one(directory, name, cells, receipt)
        _STATE.clear()
        _STATE.update(
            directory=directory,
            name=name,
            finals={i: n["final"] for i, n in tree.index.items() if n["final"] is not None},
            chunk_of=dict(tree.chunk_of),
        )
        counts = dict(verifier.counts)
        node_failures: list[tuple[int, str]] = []
        checked = failed = 0
        context = multiprocessing.get_context("fork")
        chunks = range(len(verifier.manifest["chunks"]))
        with context.Pool(processes) as pool:
            for _, part, fails, n_checked, n_failed in pool.imap_unordered(
                _check_chunk, chunks
            ):
                for key, value in part.items():
                    counts[key] = counts.get(key, 0) + value
                node_failures.extend(fails)
                checked += n_checked
                failed += n_failed
                if progress:
                    seconds = round(time.perf_counter() - clock, 1)
                    print(json.dumps({"checked": checked, "seconds": seconds}), flush=True)
        verifier.counts = counts
        verifier.failures.extend(text for _, text in sorted(node_failures))
    except standing.CertificateError as failure:
        receipt.update(status="FAIL", failures=[str(failure)], failure_count=1)
    except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError, OSError) as failure:
        receipt.update(
            status="FAIL", failures=[f"malformed certificate: {failure!r}"], failure_count=1
        )
    else:
        if checked != len(tree.index):
            verifier.fail(f"checked {checked} of {len(tree.index)} nodes")
        receipt.update(
            nodes=len(tree.index),
            closed_leaves=tree.closed_leaves,
            reasons=dict(sorted(tree.reasons.items())),
            max_depth=max(tree.depth.values(), default=None),
            checked_nodes=checked,
            node_failures=failed,
            counts=dict(sorted(verifier.counts.items())),
            status="FAIL" if verifier.failures else "PASS",
            failures=verifier.failures[: standing.MAX_FAILURES],
            failure_count=len(verifier.failures),
        )
    receipt["seconds"] = round(time.perf_counter() - clock, 3)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("directory", type=Path, help="the certificate directory")
    _ = parser.add_argument("--manifest", default=None, help="else the README's last line")
    _ = parser.add_argument("--cells", type=Path, help="a JSON cells file instead of the cover")
    _ = parser.add_argument("--cells-sha256", help="the cells file's SHA-256, required with it")
    _ = parser.add_argument("--processes", type=int, default=multiprocessing.cpu_count())
    _ = parser.add_argument("--output", type=Path, required=True, help="the receipt")
    _ = parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args(argv)
    if arguments.cells is not None:
        if not arguments.cells_sha256:
            parser.error("--cells needs --cells-sha256")
        cells = standing.file_cells(arguments.cells, arguments.cells_sha256)
    else:
        cells = standing.cover_cells()
    receipt = verify_parallel(
        arguments.directory,
        cells,
        arguments.processes,
        manifest=arguments.manifest,
        progress=arguments.progress,
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    _ = arguments.output.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(
        json.dumps({k: receipt.get(k) for k in ("status", "mode", "checked_nodes", "seconds")})
    )
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
