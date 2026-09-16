"""The page's declared render inputs cover everything the builder itself names.

`build_site.RENDER_INPUTS` is what the Pages path filter and the change-scoped gate are
checked against, so an input missing from it is a page that goes stale with every check
green. It was a hand list, and it missed `tools/render-katex.ts`, which the builder runs
for every formula on the page (#125 F30, #160 R26). This derives the builder's inputs from
its source -- the files it imports, the modules it runs, the paths it holds and the file
names it writes into those paths -- and requires the declaration to cover them.
"""

from __future__ import annotations

import ast
import re
import subprocess
from collections.abc import Iterable
from pathlib import Path
from types import ModuleType

from workbench_tools import build_candidate, build_site
from workbench_tools.build_site import PACKAGE_ROOT, RENDER_INPUTS, REPO

#: Python packages whose modules the builder runs or imports, by import root.
MODULE_ROOTS = {
    "workbench_tools": PACKAGE_ROOT / "tools/workbench_tools",
    "devtools": REPO / "packing/devtools",
}
MODULE_NAME = re.compile(r"(?:workbench_tools|devtools)(?:\.\w+)+")
#: A relative import in a Node tool: `from "./bundle-browser.ts"`.
NODE_IMPORT = re.compile(r"""from\s+["'](\.{1,2}/[^"']+)["']""")


def _tracked(path: Path) -> bool:
    """Whether git holds anything at `path`: an input is source, never build output."""
    listed = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "--", str(path.relative_to(REPO))],
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(listed.stdout.strip())


def _module_file(name: str) -> Path | None:
    root, _, rest = name.partition(".")
    base = MODULE_ROOTS.get(root)
    if base is None:
        return None
    candidate = base.joinpath(*rest.split(".")).with_suffix(".py")
    return candidate if candidate.is_file() else None


def _node_closure(tools: Iterable[Path]) -> set[Path]:
    """Node tools and the files they import relatively, transitively."""
    seen: set[Path] = set()
    pending = list(tools)
    while pending:
        tool = pending.pop()
        if tool in seen or not tool.is_file():
            continue
        seen.add(tool)
        imports = NODE_IMPORT.findall(tool.read_text(encoding="utf-8"))
        pending.extend((tool.parent / relative).resolve() for relative in imports)
    return seen


def _joined(node: ast.expr, names: dict[str, object]) -> Path | None:
    """The path a `BASE / "name" / ...` expression evaluates to, where that is static."""
    match node:
        case ast.Name(id=name):
            value = names.get(name)
            return value if isinstance(value, Path) else None
        case ast.Attribute(value=inner, attr="parent"):
            base = _joined(inner, names)
            return base.parent if base is not None else None
        case ast.BinOp(left=left, op=ast.Div(), right=ast.Constant(value=str() as part)):
            base = _joined(left, names)
            return base / part if base is not None else None
        case _:
            return None


def builder_inputs(modules: Iterable[ModuleType]) -> set[Path]:
    """Every tracked file or directory the builder modules name, with their Node closure."""
    modules = list(modules)
    sources = [Path(str(module.__file__)).resolve() for module in modules]
    found: set[Path] = set(sources)
    bare: set[str] = set()
    for module, source in zip(modules, sources, strict=True):
        names = vars(module)
        found |= {v for v in names.values() if isinstance(v, Path) and v.is_relative_to(REPO)}
        for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ImportFrom) and node.module:
                found.add(_module_file(node.module) or source)
            elif isinstance(node, ast.BinOp):
                joined = _joined(node, names)
                if joined is not None:
                    found.add(joined)
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                text = node.value
                if MODULE_NAME.fullmatch(text):
                    found.add(_module_file(text) or source)
                elif "\n" not in text and re.search(r"\.\w+$", text):
                    bare.add(text)
    # A file name passed through a helper (`asset("workbench.css")`) is resolved against the
    # directories the builder holds, and counted only where exactly one of them has it.
    bases = {path for path in found if path.is_dir()}
    for text in bare:
        hits = {base / text for base in bases if (base / text).is_file()}
        if len(hits) == 1:
            found |= hits
    found = {path.resolve() for path in found if path.exists() and _tracked(path)}
    found |= _node_closure(path for path in set(found) if path.suffix == ".ts")
    # A directory with another named path beneath it is a root the builder computes paths
    # from (the repository, `packing/`, the package), not an input in its own right.
    return {
        path
        for path in found
        if not (path.is_dir() and any(o != path and o.is_relative_to(path) for o in found))
    }


def uncovered(inputs: Iterable[Path], declared: Iterable[Path]) -> list[str]:
    declared = [path.resolve() for path in declared]
    return sorted(
        path.relative_to(REPO).as_posix()
        for path in inputs
        if not any(path.resolve().is_relative_to(entry) for entry in declared)
    )


def test_the_declared_render_inputs_cover_what_the_builder_names() -> None:
    inputs = builder_inputs((build_site, build_candidate))
    named = {path.relative_to(REPO).as_posix() for path in inputs}
    # The derivation has to reach the inputs the hand list once missed, or it proves nothing.
    assert {
        "packages/workbench/tools/render-katex.ts",
        "packages/workbench/tools/bundle-browser.ts",
        "packages/workbench/src/data/corpus.ts",
        "packing/devtools/render_explainer.py",
        "packages/workbench/assets/template.html",
        "packing/witnesses/known-best",
    } <= named
    assert uncovered(inputs, RENDER_INPUTS) == []


def test_an_omitted_render_input_is_detected() -> None:
    """The negative control: the declaration without its Node tools."""
    inputs = builder_inputs((build_site, build_candidate))
    without_tools = [
        entry for entry in RENDER_INPUTS if not entry.is_relative_to(PACKAGE_ROOT / "tools")
    ]
    assert "packages/workbench/tools/render-katex.ts" in uncovered(inputs, without_tools)
