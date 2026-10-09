"""Check Python import provenance in a fresh process before a selected long gate.

Binding is local to this child. Private mutation workers must call the same helper
with their own checkout, never inherit a parent PACKING_PROJECT_ROOT override.
This does not install dependencies or verify compiled artifact provenance.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

SCHEMA = "checkout-import-preflight/v1"
MODULES = {
    "sqpack": "packing/src/sqpack",
    "sqpack.cli.validate": "packing/src/sqpack/cli",
    "devtools": "packing/devtools",
    "workbench_tools": "packages/workbench/tools/workbench_tools",
}


def require(condition: bool, message: str) -> None:  # noqa: FBT001
    if not condition:
        raise ValueError(message)


def environment_for(checkout: Path, inherited: dict[str, str]) -> dict[str, str]:
    """A new environment, not a mutation or a parent override in the caller."""
    root = checkout.resolve()
    environment = dict(inherited)
    environment.pop("PACKING_PROJECT_ROOT", None)
    environment["PYTHONPATH"] = os.pathsep.join(
        str(root / part) for part in ("packing/src", "packing", "packages/workbench/tools")
    )
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return environment


def inspect_imports(checkout: Path) -> dict[str, Any]:
    root = checkout.resolve()
    observations = {}
    for name, relative in MODULES.items():
        expected = root / relative
        try:
            spec = importlib.util.find_spec(name)
            locations = (
                []
                if spec is None
                else (
                    [Path(spec.origin).resolve()]
                    if spec.origin is not None
                    else [Path(p).resolve() for p in spec.submodule_search_locations or ()]
                )
            )
            matched = bool(locations) and all(p.is_relative_to(expected) for p in locations)
            observations[name] = {
                "locations": [str(p) for p in locations],
                "matched": matched,
                "expected_root": str(expected),
            }
        except (ImportError, OSError, ValueError, AttributeError) as error:
            observations[name] = {"matched": False, "error": str(error)}
    override = os.environ.get("PACKING_PROJECT_ROOT")
    passed = not override and all(row["matched"] for row in observations.values())
    return {
        "schema": SCHEMA,
        "status": "PASS" if passed else "REFUSED",
        "checkout": str(root),
        "modules": observations,
        "project_root_override": override,
        "compiled_artifacts_checked": False,
    }


def check(checkout: Path, *, bind_paths: bool = False, timeout: float = 30) -> dict[str, Any]:
    environment = (
        environment_for(checkout, dict(os.environ)) if bind_paths else dict(os.environ)
    )
    command = [sys.executable, str(Path(__file__).resolve()), "--probe", str(checkout)]
    try:
        completed = subprocess.run(
            command,
            env=environment,
            cwd=checkout,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        report = json.loads(completed.stdout)
        require(isinstance(report, dict), "invalid checkout preflight child receipt")
        require(
            report.get("schema") == SCHEMA and completed.returncode in {0, 1},
            "invalid checkout preflight child receipt",
        )
        require(
            (completed.returncode == 0) == (report.get("status") == "PASS"),
            "checkout preflight exit and status differ",
        )
    except subprocess.TimeoutExpired:
        return {"schema": SCHEMA, "status": "INCOMPLETE", "error": "preflight child ceiling"}
    except (OSError, ValueError) as error:
        return {"schema": SCHEMA, "status": "REFUSED", "error": str(error)}
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path)
    parser.add_argument("--probe", type=Path)
    parser.add_argument("--bind-paths", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if (args.checkout is None) == (args.probe is None):
        parser.error("choose exactly one of --checkout or --probe")
    report = (
        inspect_imports(args.probe)
        if args.probe is not None
        else check(args.checkout, bind_paths=args.bind_paths)
    )
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output is not None:
        args.output.write_text(encoded)
    print(encoded, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
