"""Require a reviewed release-impact disposition for changed publication inputs.

Producer declarations select candidates; they do not prove that public output changed.
A candidate needs an owning successor decision or a fresh, path-scoped no-change
review naming the examined outputs. Prior source is parsed as data, never executed.
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import override

from devtools import pages_scope, render_overview
from sqpack import release
from sqpack.known_best import KNOWN_BEST_COMPOSITES
from sqpack.yamlio import load_yaml

REPO = pages_scope.REPO
RELEASE_PATH = "packing/src/sqpack/release.py"
CHANGELOG_PATH = "packing/site-changelog.yaml"


def _git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=repo, capture_output=True, check=False)
    if result.returncode:
        raise ValueError(
            f"git {args[0]} failed: {result.stderr.decode(errors='replace').strip()}"
        )
    return result.stdout


def resolve_base(repo: Path, *, baseline_ref: str, base: str | None = None) -> str:
    """Use the PR merge base, or an explicitly chosen preceding delivery."""
    revision = (
        _git(
            repo,
            "rev-parse",
            "--verify",
            "--end-of-options",
            (base or baseline_ref) + "^{commit}",
        )
        .decode()
        .strip()
    )
    return revision if base else _git(repo, "merge-base", "HEAD", revision).decode().strip()


def changed_paths(repo: Path, base: str) -> tuple[str, ...]:
    """Committed, index, worktree and untracked changes, with both rename paths."""
    tracked = _git(repo, "diff", "--name-only", "--no-renames", "-z", base, "--")
    untracked = _git(repo, "ls-files", "--others", "--exclude-standard", "-z")
    return tuple(sorted(set((tracked + untracked).decode().split("\0")) - {""}))


def _previous(repo: Path, base: str, path: str) -> bytes | None:
    row = _git(repo, "ls-tree", "-z", base, "--", path)
    if not row:
        return None
    if row.split(b" ", 2)[1] == b"commit":
        return b"gitlink"
    return _git(repo, "show", f"{base}:{path}")


def _current(repo: Path, path: str) -> bytes | None:
    source = repo / path
    return source.read_bytes() if source.is_file() else None


class _WithoutDocstrings(ast.NodeTransformer):
    @override
    def generic_visit(self, node: ast.AST) -> ast.AST:
        node = super().generic_visit(node)
        if (
            isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
            and node.body
            and isinstance(node.body[0], ast.Expr)
        ):
            value = node.body[0].value
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                node.body = node.body[1:]
        return node


def _semantic_bytes(path: str, content: bytes | None) -> object:
    if content is None:
        return None
    if path.endswith(".py"):
        tree = _WithoutDocstrings().visit(ast.parse(content, filename=path))
        return ast.dump(tree, include_attributes=False)
    if path == CHANGELOG_PATH:
        document = load_yaml(content.decode())
        return document["entries"]
    return content


def _assignments(content: bytes | None) -> dict[str, ast.expr]:
    if content is None:
        return {}
    fields = {}
    for node in ast.parse(content, filename=RELEASE_PATH).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    fields[target.id] = node.value
        elif (
            isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value
        ):
            fields[node.target.id] = node.value
    return fields


# Published metadata has explicit owners; unknown declarations remain conservative
# candidates through the executable-AST comparison below, rather than disappearing.
_PUBLISHED_RELEASE_FIELDS: dict[str, tuple[str, ...]] = {
    "site": (
        "PUBLICATION_HISTORY",
        "PUBLICATION_VERSION",
        "PUBLICATION_STATUS",
        "PUBLICATION_EDITION",
        "PUBLICATION_STAMP",
        "PUBLICATION_DATE",
        "FIRST_PUBLISHED",
    ),
    "infographics": ("INFOGRAPHIC_HISTORY", "INFOGRAPHIC_VERSION", "INFOGRAPHIC_EDITION"),
    "paper:n11-lower-bounds-explainer": (
        "EXPLAINER_HISTORY",
        "EXPLAINER_VERSION",
        "EXPLAINER_REVISED",
        "EXPLAINER_FIRST_PUBLISHED",
    ),
    "paper:n11-optimality-review": (
        "OPTIMALITY_REVIEW_HISTORY",
        "OPTIMALITY_REVIEW_VERSION",
        "OPTIMALITY_REVIEW_STATUS",
        "OPTIMALITY_REVIEW_EDITION",
        "OPTIMALITY_REVIEW_REVISED",
        "OPTIMALITY_PROOF_PUBLISHED",
    ),
    "paper:n11-threshold-bound-review": (
        "THRESHOLD_REVIEW_HISTORY",
        "THRESHOLD_REVIEW_VERSION",
        "THRESHOLD_REVIEW_STATUS",
        "THRESHOLD_REVIEW_EDITION",
        "THRESHOLD_REVIEW_REVISED",
        "THRESHOLD_PROOF_PUBLISHED",
    ),
    "paper:square-packing-methods-survey": (
        "PACKING_METHODS_HISTORY",
        "PACKING_METHODS_VERSION",
        "PACKING_METHODS_EDITION",
        "PACKING_METHODS_FIRST_PUBLISHED",
        "PACKING_METHODS_REVISED",
    ),
}
_PIN_FIELDS = {"DATA_REVISION", "PUBLICATION_REVISION"}
_BOOKKEEPING_RECORDS = {
    "RELEASE_IMPACTS": "ReleaseImpactDecision",
    "RELEASE_NO_PUBLIC_CHANGES": "ReleaseNoPublicChange",
}


def _visible_release_fields(fields: Mapping[str, ast.expr], component: str) -> dict[str, str]:
    return {
        name: ast.dump(fields[name], include_attributes=False)
        for name in _PUBLISHED_RELEASE_FIELDS.get(component, ())
        if name in fields
    }


def _assignment_names(node: ast.stmt) -> set[str]:
    targets = (
        node.targets
        if isinstance(node, ast.Assign)
        else ([node.target] if isinstance(node, ast.AnnAssign) else [])
    )
    if targets and all(isinstance(target, ast.Name) for target in targets):
        return {target.id for target in targets if isinstance(target, ast.Name)}
    return set()


def _literal_record_sequence(value: ast.expr, constructor: str) -> bool:
    if not isinstance(value, (ast.Tuple, ast.List)):
        return False
    for record in value.elts:
        if (
            not isinstance(record, ast.Call)
            or not isinstance(record.func, ast.Name)
            or record.func.id != constructor
            or any(keyword.arg is None for keyword in record.keywords)
        ):
            return False
        try:
            for item in [*record.args, *(keyword.value for keyword in record.keywords)]:
                ast.literal_eval(item)
        except ValueError, TypeError:
            return False
    return True


def _bookkeeping_assignment(node: ast.stmt, names: set[str]) -> bool:
    if len(names) != 1 or not isinstance(node, (ast.Assign, ast.AnnAssign)):
        return False
    name = next(iter(names))
    value = node.value
    if value is None:
        return False
    if name in _PIN_FIELDS:
        return (
            isinstance(value, ast.Constant)
            and isinstance(value.value, str)
            and (
                not isinstance(node, ast.AnnAssign)
                or ast.dump(node.annotation) == "Name(id='str', ctx=Load())"
            )
        )
    constructor = _BOOKKEEPING_RECORDS.get(name)
    if constructor is None or not _literal_record_sequence(value, constructor):
        return False
    if isinstance(node, ast.AnnAssign):
        annotation = ast.dump(node.annotation, include_attributes=False)
        expected = ast.dump(ast.parse(f"tuple[{constructor}, ...]", mode="eval").body)
        if annotation not in {"Name(id='tuple', ctx=Load())", expected}:
            return False
    return True


def _release_executable_ast(content: bytes | None) -> object:
    """Retain every other executable node; never execute previous release source.

    Named published assignments are compared by owner. Only literal pins and the
    recognized literal disposition records are bookkeeping. Imports, helpers, class
    implementations, unknown fields and executable bookkeeping values stay visible.
    """
    if content is None:
        return None
    tree = ast.parse(content, filename=RELEASE_PATH)
    published = {name for names in _PUBLISHED_RELEASE_FIELDS.values() for name in names}
    tree.body = [
        node
        for node in tree.body
        if not (
            ((names := _assignment_names(node)) and names <= published)
            or _bookkeeping_assignment(node, names)
        )
    ]
    tree = _WithoutDocstrings().visit(tree)
    return ast.dump(tree, include_attributes=False)


def producer_inputs() -> dict[str, tuple[str, ...]]:
    """Declared producer inputs and helpers, without workflow-only check/test seeds."""
    result: dict[str, set[str]] = {
        component: set() for component in release.COMPONENT_HISTORY_NAMES
    }
    papers = {
        pages_scope.half_name(paper.slug): f"paper:{paper.slug}"
        for paper in render_overview.PAPERS
    }
    for half, builder in pages_scope.BUILDER_INPUTS.items():
        component = "site" if half in {"overview", "workbench"} else papers[half]
        declared = tuple(builder())
        helpers = pages_scope.import_closure(
            {path for path in declared if path.suffix == ".py" and path.is_file()}
        )
        result[component].update(
            path.relative_to(REPO).as_posix() for path in {*declared, *helpers}
        )
    result["infographics"].update(component_outputs()["infographics"])
    return {component: tuple(sorted(paths)) for component, paths in result.items()}


def component_outputs() -> dict[str, tuple[str, ...]]:
    """Recognized examined outputs; declarations name the outputs actually reviewed."""
    result = {
        "site": tuple(sorted({*render_overview.PAGES, "workbench/index.html"})),
        **{
            f"paper:{paper.slug}": tuple(
                f"papers/{paper.slug}{suffix}" for suffix in (".html", ".md", ".pdf")
            )
            for paper in render_overview.PAPERS
        },
    }
    exports = set()
    for spec in KNOWN_BEST_COMPOSITES:
        names = {
            spec.svg_name,
            spec.pdf_name,
            *(spec.raster_name(scale) for scale in spec.raster_scales),
        }
        if spec.card_units is not None:
            names.add(spec.card_png_name)
        exports.update("packing/atlas/known-best/" + name for name in names)
    result["infographics"] = tuple(sorted(exports))
    return result


def candidate_paths(repo: Path, base: str) -> dict[str, tuple[str, ...]]:
    """Exact changed inputs potentially affecting each owner, before editorial judgment."""
    inputs = producer_inputs()
    selected: dict[str, set[str]] = {component: set() for component in inputs}
    infographic_outputs = set(component_outputs()["infographics"])
    for path in changed_paths(repo, base):
        matched = {
            component
            for component, declarations in inputs.items()
            if any(
                path == declaration or path.startswith(declaration + "/")
                for declaration in declarations
            )
        }
        if path not in infographic_outputs and path != RELEASE_PATH and not matched:
            continue
        old, current = _previous(repo, base, path), _current(repo, path)
        if path == RELEASE_PATH:
            before, after = _assignments(old), _assignments(current)
            owners = {
                component
                for component in inputs
                if _visible_release_fields(before, component)
                != _visible_release_fields(after, component)
            }
            if _release_executable_ast(old) != _release_executable_ast(current):
                # The infographic producer need not be in the live site import graph.
                # Any unclassified release implementation change needs every owner's review.
                owners.update(inputs)
        elif path in infographic_outputs:
            owners = {"infographics"} if old != current else set()
        elif _semantic_bytes(path, old) == _semantic_bytes(path, current):
            owners = set()
        else:
            owners = matched
        for owner in owners:
            selected[owner].add(path)
    return {component: tuple(sorted(paths)) for component, paths in selected.items() if paths}


def _history_head(fields: Mapping[str, ast.expr], name: str) -> str:
    if name == "INFOGRAPHIC_HISTORY" and name not in fields:
        name = "PUBLICATION_HISTORY"
    node = fields.get(name)
    if isinstance(node, ast.Name):
        return _history_head(fields, node.id)
    if (
        not isinstance(node, (ast.Tuple, ast.List))
        or not node.elts
        or not isinstance(node.elts[0], ast.Call)
    ):
        raise ValueError(f"baseline {name} has no retained literal history head")
    for keyword in node.elts[0].keywords:
        if keyword.arg == "version":
            version = ast.literal_eval(keyword.value)
            if isinstance(version, str):
                release.parsed_version(version)
                return version
    raise ValueError(f"baseline {name} has no literal version")


def baseline_versions(repo: Path, base: str) -> dict[str, str]:
    """Actual retained baseline heads, parsed without importing previous source."""
    fields = _assignments(_previous(repo, base, RELEASE_PATH))
    return {
        component: _history_head(fields, name)
        for component, name in release.COMPONENT_HISTORY_NAMES.items()
    }


def _records(fields: Mapping[str, ast.expr], name: str) -> tuple[tuple, ...]:
    node = fields.get(name)
    if node is None:
        return ()
    if not isinstance(node, (ast.Tuple, ast.List)):
        raise TypeError(f"{name} must retain a literal tuple of decisions")
    records = []
    for call in node.elts:
        constructor = (
            "ReleaseNoPublicChange"
            if name == "RELEASE_NO_PUBLIC_CHANGES"
            else "ReleaseImpactDecision"
        )
        if (
            not isinstance(call, ast.Call)
            or not isinstance(call.func, ast.Name)
            or call.func.id != constructor
        ):
            raise TypeError(f"{name} requires named literal records")
        fields_type = (
            release.ReleaseNoPublicChange
            if name == "RELEASE_NO_PUBLIC_CHANGES"
            else release.ReleaseImpactDecision
        )
        if any(keyword.arg is None for keyword in call.keywords):
            raise TypeError(f"{name} requires explicit literal fields")
        keywords = {
            keyword.arg: ast.literal_eval(keyword.value)
            for keyword in call.keywords
            if keyword.arg is not None
        }
        record = fields_type(
            *(ast.literal_eval(argument) for argument in call.args), **keywords
        )
        if name == "RELEASE_NO_PUBLIC_CHANGES" and (
            not all(
                isinstance(field, tuple) and all(isinstance(item, str) for item in field)
                for field in record[:3]
            )
            or not isinstance(record[3], str)
        ):
            raise TypeError(f"{name} requires tuple-of-string scopes and a string reason")
        records.append(tuple(record))
    return tuple(records)


def _exemptions(
    candidates: Mapping[str, tuple[str, ...]],
    current: Mapping[str, ast.expr],
    previous: Mapping[str, ast.expr],
) -> tuple[set[str], list[str]]:
    old = set(_records(previous, "RELEASE_NO_PUBLIC_CHANGES"))
    outputs = component_outputs()
    covered: dict[str, set[str]] = {component: set() for component in candidates}
    errors = []
    for record in _records(current, "RELEASE_NO_PUBLIC_CHANGES"):
        if record in old:
            continue
        decision = release.ReleaseNoPublicChange(*record)
        if (
            not decision.components
            or not decision.paths
            or not decision.outputs
            or not decision.reason.strip()
        ):
            errors.append(
                "fresh no-public-change decision needs components, exact paths, "
                "examined outputs and reason"
            )
            continue
        if any(component not in candidates for component in decision.components):
            errors.append(
                "fresh no-public-change decision names a component without candidate changes"
            )
            continue
        scoped = {path for component in decision.components for path in candidates[component]}
        if any(
            path not in scoped
            or PurePosixPath(path).as_posix() != path
            or any(character in path for character in "*?[]")
            for path in decision.paths
        ):
            errors.append("fresh no-public-change paths must exactly name candidate inputs")
            continue
        declared_outputs = {
            output for component in decision.components for output in outputs[component]
        }
        if any(output not in declared_outputs for output in decision.outputs) or any(
            not set(decision.outputs) & set(outputs[component])
            for component in decision.components
        ):
            errors.append(
                "fresh no-public-change decision must name recognized examined outputs "
                "for every component"
            )
            continue
        for component in decision.components:
            covered[component].update(set(decision.paths) & set(candidates[component]))
    exempt = {
        component for component, paths in candidates.items() if set(paths) <= covered[component]
    }
    return exempt, errors


@dataclass(frozen=True)
class ImpactReport:
    """Review obligations and their observed retained baseline versions."""

    baseline: str
    candidate_paths: dict[str, tuple[str, ...]]
    baseline_versions: dict[str, str]
    exempt_components: tuple[str, ...]
    errors: tuple[str, ...]


def inspect(
    *, repo: Path = REPO, baseline_ref: str = "origin/main", base: str | None = None
) -> ImpactReport:
    """Require owning successor decisions or fresh reviewed no-change dispositions."""
    baseline = resolve_base(repo, baseline_ref=baseline_ref, base=base)
    candidates = candidate_paths(repo, baseline)
    versions = baseline_versions(repo, baseline)
    previous = _assignments(_previous(repo, baseline, RELEASE_PATH))
    current = _assignments(_current(repo, RELEASE_PATH))
    exempt, errors = _exemptions(candidates, current, previous)
    old_decisions = set(_records(previous, "RELEASE_IMPACTS"))
    fresh_decisions = {
        record[:3]
        for record in _records(current, "RELEASE_IMPACTS")
        if record not in old_decisions
    }
    for component in sorted(set(candidates) - exempt):
        key = (component, versions[component], release.component_version(component))
        if key not in fresh_decisions:
            errors.append(
                f"{component}: candidate public inputs need a fresh owning successor "
                "or reviewed no-public-change decision"
            )
            continue
        try:
            release.validate_release_impacts(
                externally_changed=(component,), previous_versions=versions
            )
        except ValueError as error:
            errors.append(str(error))
    return ImpactReport(baseline, candidates, versions, tuple(sorted(exempt)), tuple(errors))


def main(argv: Sequence[str] | None = None) -> int:
    """A local, bounded gate; no publication builds, snapshots or network requests."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-ref", default="origin/main")
    parser.add_argument("--base", help="Explicit prior main delivery rather than PR merge base")
    parser.add_argument("--json", action="store_true")
    options = parser.parse_args(argv)
    try:
        report = inspect(baseline_ref=options.baseline_ref, base=options.base)
    except (OSError, TypeError, ValueError, SyntaxError) as error:
        print(f"release impact: {error}", file=sys.stderr)
        return 1
    if options.json:
        print(json.dumps(asdict(report), indent=2, sort_keys=True))
    else:
        for component, paths in sorted(report.candidate_paths.items()):
            print(f"{component} ({report.baseline_versions[component]}): " + ", ".join(paths))
        for error in report.errors:
            print(f"release impact: {error}", file=sys.stderr)
        if not report.errors:
            print("release impact: every publication candidate has a reviewed disposition")
    return int(bool(report.errors))


if __name__ == "__main__":
    raise SystemExit(main())
