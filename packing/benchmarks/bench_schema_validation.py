#!/usr/bin/env python3
"""Compare the two JSON Schema validators over this repository's real corpus.

`devtools.validate_schemas` runs on `jsonschema_rs`. This is the measurement that
chose it, kept runnable so the choice can be re-argued rather than remembered (`OR-1`).
It reports three things, because the speed number alone is not a reason to switch:

- **Compile and validate time** for each library over the whole enforced corpus.
- **The differential verdict**: whether the two libraries accept and reject the same
  documents, and flag the same locations. A validator that is faster and more permissive
  is a soundness regression, not an optimization.
- **The per-artifact cost distribution**, because the corpus is not uniform -- a handful
  of witness files carry megabytes of exact rationals and dominate every total here.

`tests/test_schema_validator_equivalence.py` is the standing guarantee; this script is
the number that motivated it.

**One run is not a measurement.** On a shared container the Python side is stable near
seven and a half seconds while the Rust side is small enough that scheduling noise
dominates it: five runs on 2026-08-30 gave 56, 56, 62, 88 and 55 ms, so the ratio moved
between 83x and 137x without anything changing. Run it several times and quote the range.
The conclusion does not depend on which end you take, which is the useful thing about a
gap this size.

    uv run --frozen python benchmarks/bench_schema_validation.py
    uv run --frozen python benchmarks/bench_schema_validation.py --top 15
"""

from __future__ import annotations

import argparse
import functools
import pathlib
import sys
import time
from typing import Any

import jsonschema_rs
from jsonschema import Draft202012Validator as PyValidator

from devtools.validate_schemas import corpus_paths, payload_and_meta
from sqpack.yamlio import load_yaml

RsValidator = jsonschema_rs.Draft202012Validator


@functools.cache
def _schema(schema_path: pathlib.Path) -> dict[str, Any]:
    return load_yaml(schema_path.read_text(encoding="utf-8"))


def _loaded() -> list[tuple[pathlib.Path, pathlib.Path, Any]]:
    """(artifact, schema path, payload) for every enforced artifact.

    Loading happens once, outside every timed region: YAML parsing is not what is being
    compared here, and leaving it inside would have both libraries paying it equally
    while burying the difference that matters.
    """
    md, datasets = corpus_paths()
    out = []
    for path in md + datasets:
        payload, meta = payload_and_meta(path)
        if not meta or meta.get("status") != "enforced":
            continue
        schema_path = (path.parent / meta["schema"]).resolve()
        if schema_path.exists():
            out.append((path, schema_path, payload))
    return out


def _time_compile(build: Any, schema_paths: list[pathlib.Path]) -> float:
    start = time.perf_counter()
    for schema_path in schema_paths:
        build(_schema(schema_path))
    return time.perf_counter() - start


def _run(
    build: Any, errors_of: Any, corpus: list[tuple[pathlib.Path, pathlib.Path, Any]]
) -> tuple[float, dict[pathlib.Path, float], dict[pathlib.Path, tuple[bool, list[Any]]]]:
    validators = {sp: build(_schema(sp)) for _p, sp, _pl in corpus}
    per_file: dict[pathlib.Path, float] = {}
    verdicts: dict[pathlib.Path, tuple[bool, list[Any]]] = {}
    start = time.perf_counter()
    for path, schema_path, payload in corpus:
        one = time.perf_counter()
        errors = list(validators[schema_path].iter_errors(payload))
        per_file[path] = time.perf_counter() - one
        verdicts[path] = (not errors, sorted(errors_of(e) for e in errors))
    return time.perf_counter() - start, per_file, verdicts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--top", type=int, default=10, help="how many of the costliest artifacts to list"
    )
    args = parser.parse_args(argv)

    corpus = _loaded()
    if not corpus:
        print("no enforced artifacts found", file=sys.stderr)
        return 2
    schema_paths = sorted({sp for _p, sp, _pl in corpus})

    py_compile = _time_compile(PyValidator, schema_paths)
    rs_compile = _time_compile(RsValidator, schema_paths)
    py_total, py_per_file, py_verdicts = _run(
        PyValidator, lambda e: tuple(str(x) for x in e.path), corpus
    )
    rs_total, _rs_per_file, rs_verdicts = _run(
        RsValidator, lambda e: tuple(str(x) for x in e.instance_path), corpus
    )

    print(f"corpus: {len(corpus)} artifacts against {len(schema_paths)} schemas\n")
    print(f"{'validator':<28}{'compile':>12}{'validate':>12}")
    for label, compiled, validated in (
        ("jsonschema (pure Python)", py_compile, py_total),
        ("jsonschema-rs (Rust)", rs_compile, rs_total),
    ):
        print(f"{label:<28}{compiled * 1e3:>10.1f} ms{validated * 1e3:>10.1f} ms")
    if rs_total > 0:
        print(f"\nspeedup on validation: {py_total / rs_total:.0f}x")

    disagreements = [p for p in py_verdicts if py_verdicts[p] != rs_verdicts[p]]
    print(
        f"\ndifferential verdict: {len(corpus) - len(disagreements)} of {len(corpus)} agree"
        + ("" if not disagreements else f" -- DISAGREEMENTS: {[p.name for p in disagreements]}")
    )

    print(f"\nthe {args.top} costliest artifacts under the Python validator:")
    for path, cost in sorted(py_per_file.items(), key=lambda kv: -kv[1])[: args.top]:
        size_kb = path.stat().st_size / 1024
        print(f"  {cost * 1e3:>9.1f} ms  {size_kb:>8.0f} KB  {path.name}")
    return 1 if disagreements else 0


if __name__ == "__main__":
    raise SystemExit(main())
