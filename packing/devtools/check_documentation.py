#!/usr/bin/env python3
"""Check durable-document coverage, lifecycle, footers, links, and generated map."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

from devtools.render_document_map import MAP, REPO, SYNOPSIS, expected_synopsis, load_map
from devtools.repo_scope import is_vendored
from sqpack.yamlio import safe_load

FOOTER = "This document follows common-doc-guidelines.md."
# `site` is the explainer's render output, gitignored and rebuilt by every run. It is
# not durable, so it has nothing to be mapped to; the page and the Markdown document
# beside it are checked by the renderer's own `--check`, which compares them byte for
# byte against a fresh render.
#
# Vendored trees are not here. They are skipped by `devtools.repo_scope`, which reads
# `.gitmodules`, and they used to be a `vendor/**/*.md` exclusion in the document map
# instead. That failed on a plain clone: the map's loader requires every exclusion to
# match a file, and an unchecked-out submodule matches none, so `git clone` without
# `--recurse-submodules` failed the docs check while CI passed (think-5e7k). Upstream
# prose is not this repository's surface whether or not it is on disk, which is a
# statement about the declaration rather than about the working tree.
IGNORED_PARTS = {
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "attic",
    "site",
}
REPOSITORY_ROOT = REPO
RETIRED_PHRASES = (
    "approximately verified",
    "numerical-arbitrary-precision",
    "numerically verified",
    "verified-construction",
)

#: Where a project document goes: the directory under `docs/project/` named for its kind,
#: and for a dated record a name that starts with that kind and the record's date. Nothing
#: sits loose in `docs/project/`, since a loose file says nothing about what kind of
#: document it is (docs/project/specs/active/plan-2026-10-11-documentation-organization.md,
#: think-mv16). A new kind of document is a new entry here.
PROJECT_DOCS = "docs/project"
DATED_KINDS = {
    "handoffs": ("handoff",),
    "postmortems": ("postmortem",),
    "research": ("research",),
    "reviews": ("review",),
    "specs": ("plan", "spike"),
}
MAINTAINED_KINDS = {"guides", "policies"}
DATE = r"\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])"
SLUG = r"[a-z0-9]+(?:[.-][a-z0-9]+)*"
DATED_NAME = re.compile(rf"(?P<kind>[a-z]+)-{DATE}-{SLUG}\.md")
#: A document's name is lowercase kebab-case, except the names a tool or convention fixes
#: and a registered record id spelled as in its frontmatter (`H-001-…`, `X-001-…`,
#: `VE-001-…`; conventions.md section 2).
KEBAB_NAME = re.compile(rf"{SLUG}\.md")
FIXED_NAMES = {"README.md", "AGENTS.md", "CLAUDE.md", "CHANGELOG.md"}
#: The advanced companion keeps the explicitly requested root manuscript name.
FIXED_PATHS = {"TUTORIAL-ADVANCED.md"}
IDENTIFIER_NAME = re.compile(rf"(?:H|X|VE)-\d+-{SLUG}\.md")
#: Documents that predate the layout and wait on a move every open pull request would
#: conflict with: the root guides, the frontier's generated views and the verifier guides
#: that `evidence.yaml` cites (think-xz7z). The other deferred moves break no rule here.
#: An entry that no longer breaks a rule fails, and `test_document_layout` refuses one that
#: was not on the list when it was made, so the list only shrinks.
LAYOUT_PENDING = frozenset(
    {
        "SYNOPSIS.md",
        "TUTORIAL.md",
        "docs/project/site-urls.md",
        "packing/frontier/CERTIFICATE-REACH.md",
        "packing/frontier/INVENTORY.md",
        "packing/frontier/RESULTS.md",
        "packing/frontier/STATUS.md",
        "packing/frontier/VERIFIERS.md",
        "packing/sqverify_fast/INDEPENDENCE.md",
        "packing/sqverify_fast/SOUNDNESS.md",
    }
)


def _matches(pattern: str) -> set[str]:
    return {path.relative_to(REPO).as_posix() for path in REPO.glob(pattern) if path.is_file()}


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    return safe_load(text.split("---\n", 2)[1])


def _slugs(text: str) -> set[str]:
    """Approximate GitHub heading ids, including duplicate-heading suffixes."""
    counts: Counter[str] = Counter()
    slugs: set[str] = set(re.findall(r'id="([^"]+)"', text))
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.MULTILINE):
        plain = re.sub(r"<[^>]+>", "", heading)
        plain = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", plain)
        base = re.sub(r"[^a-z0-9 _-]", "", plain.lower()).strip().replace(" ", "-")
        suffix = counts[base]
        counts[base] += 1
        slugs.add(base if suffix == 0 else f"{base}-{suffix}")
    return slugs


def _is_ephemeral_local_target(path: Path) -> bool:
    """Reject links whose apparent validity depends on untracked tbd working state."""
    try:
        relative = path.relative_to(REPOSITORY_ROOT)
    except ValueError:
        return False
    return relative.parts[:2] == (".tbd", "docs")


#: The opening or closing line of a fenced code block (CommonMark: three or more
#: backticks or tildes, indented by at most three spaces).
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def _outside_fences(text: str) -> str:
    """The text without its fenced code blocks, where a quoted link is not a link.

    A review that quotes a line of another file, links and all, in a code block does not
    link from where it stands (the 6 October re-check quotes a SYNOPSIS.md row). A fence
    closes on the same character, at least as long, with nothing after it; an unclosed
    fence runs to the end, as CommonMark has it.
    """
    kept: list[str] = []
    fence = ""
    for line in text.splitlines():
        match = FENCE.match(line)
        if fence:
            if (
                match
                and match.group(1)[0] == fence[0]
                and len(match.group(1)) >= len(fence)
                and not match.group(2).strip()
            ):
                fence = ""
            continue
        if match:
            fence = match.group(1)
            continue
        kept.append(line)
    return "\n".join(kept)


def _link_problems(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []
    for raw_target in re.findall(r"!?\[[^]]*\]\(([^)]+)\)", _outside_fences(text)):
        target = raw_target.strip().strip("<>")
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        relative, _, fragment = target.partition("#")
        label = path.relative_to(REPO).as_posix()
        if Path(unquote(relative)).is_absolute():
            problems.append(f"{label}: absolute local link -> {target}; use a relative path")
            continue
        resolved = path if not relative else (path.parent / unquote(relative)).resolve()
        if not resolved.exists():
            problems.append(f"{label}: dead link -> {target}")
        elif _is_ephemeral_local_target(resolved):
            problems.append(f"{label}: ephemeral local-state link -> {target}")
        elif (
            fragment
            and resolved.suffix == ".md"
            and unquote(fragment) not in _slugs(resolved.read_text(encoding="utf-8"))
        ):
            problems.append(f"{label}: dead anchor -> {target}")
    return problems


#: An absolute link to a path on this repository's `main`. The relative-link check skips it
#: as external, and GitHub does not redirect a moved file, so a move leaves it dead without
#: a word; it is held to the tree instead (think-mv16). A link pinned to a commit is not.
MAIN_LINK = re.compile(
    r"https://github\.com/jlevy/squares/(?:blob|tree)/main/([^\s)<>\"'`#?]+)"
)


def _main_link_problems(path: Path) -> list[str]:
    label = path.relative_to(REPO).as_posix()
    targets = MAIN_LINK.findall(_outside_fences(path.read_text(encoding="utf-8")))
    return [
        f"{label}: dead link to main -> {target}"
        for target in dict.fromkeys(target.rstrip(".,;:!") for target in targets)
        if not (REPO / unquote(target)).exists()
    ]


def _layout_problem(relative: str) -> str | None:
    """Why a mapped document's place or name breaks the layout, or None if it does not."""
    parts = relative.split("/")
    name = parts[-1]
    if relative.startswith(f"{PROJECT_DOCS}/"):
        inside = parts[2:]
        if len(inside) == 1:
            if name != "README.md":
                return "sits loose in docs/project/; put it in the directory for its kind"
        elif inside[0] not in DATED_KINDS.keys() | MAINTAINED_KINDS:
            return f"is in docs/project/{inside[0]}/, which is not a directory for a kind"
        elif (kinds := DATED_KINDS.get(inside[0])) and name != "README.md":
            match = DATED_NAME.fullmatch(name)
            if not (match and match["kind"] in kinds):
                names = " or ".join(f"{kind}-YYYY-MM-DD-topic.md" for kind in kinds)
                return f"is not named {names}"
    if not (
        relative in FIXED_PATHS
        or name in FIXED_NAMES
        or KEBAB_NAME.fullmatch(name)
        or IDENTIFIER_NAME.fullmatch(name)
    ):
        return "is not named in lowercase kebab-case"
    return None


def _layout_problems(mapped: set[str]) -> list[str]:
    problems = [
        f"{relative}: {problem}"
        for relative in sorted(mapped - LAYOUT_PENDING)
        if (problem := _layout_problem(relative))
    ]
    problems.extend(
        f"layout allowlist entry no longer needed: {relative}"
        for relative in sorted(LAYOUT_PENDING)
        if relative not in mapped or _layout_problem(relative) is None
    )
    return problems


def check() -> list[str]:
    document_map = load_map()
    problems: list[str] = []
    documents = document_map["documents"]
    document_paths = [item["path"] for item in documents]
    if len(document_paths) != len(set(document_paths)):
        problems.append("document map contains duplicate standalone paths")

    covered = set(document_paths)
    for document in documents:
        path = REPO / document["path"]
        if not path.is_file():
            problems.append(f"mapped document does not exist: {document['path']}")
        replacement = document.get("superseded_by")
        if document["lifecycle"] == "superseded" and not replacement:
            problems.append(f"{document['path']}: superseded without superseded_by")
        if replacement and not (REPO / replacement).is_file():
            problems.append(f"{document['path']}: replacement does not exist: {replacement}")

    for collection in document_map["collections"]:
        matched = _matches(collection["pattern"])
        if not matched:
            problems.append(f"document collection is empty: {collection['pattern']}")
        overlap = covered & matched
        if overlap:
            problems.append(f"document map covers paths more than once: {sorted(overlap)[:3]}")
        covered |= matched
        schema = REPO / collection["schema"]
        if not schema.is_file():
            problems.append(f"collection schema does not exist: {collection['schema']}")
        for relative in sorted(matched):
            try:
                source = REPO / relative
                record = (
                    safe_load(source.read_text(encoding="utf-8"))
                    if source.suffix in {".yaml", ".yml"}
                    else _frontmatter(source)
                )
                metadata = record["softschema"]
            except (KeyError, TypeError, ValueError) as error:
                problems.append(f"{relative}: cannot read softschema metadata: {error}")
                continue
            if metadata.get("contract") != collection["contract"]:
                problems.append(
                    f"{relative}: contract {metadata.get('contract')!r} does not match "
                    f"{collection['contract']!r}"
                )

    excluded: set[str] = set()
    for exclusion in document_map["exclusions"]:
        matched = _matches(exclusion["pattern"])
        if not matched:
            problems.append(f"document exclusion is empty: {exclusion['pattern']}")
        excluded |= matched

    actual = {
        path.relative_to(REPO).as_posix()
        for path in REPO.rglob("*.md")
        if path.is_file()
        and not is_vendored(path)
        # cargo doc emits third-party font licenses beneath this crate's default
        # build directory (think-k8hl). Exclude that generated tree, not authored
        # documents in unrelated directories that happen to be named `target`.
        and path.relative_to(REPO).parts[:3]
        not in {
            ("packing", "sqsearch", "target"),
            ("packing", "sqverify_exact", "target"),
            ("packing", "sqverify_fast", "target"),
            ("packing", "n17bb_native", "target"),
            ("packing", "n17_kernel_verify", "target"),
        }
        and not any(
            part in IGNORED_PARTS or part.startswith(".")
            for part in path.relative_to(REPO).parts
        )
    }
    unmapped = actual - covered - excluded
    problems.extend(f"unmapped durable document: {path}" for path in sorted(unmapped))
    problems.extend(
        f"mapped document is also excluded: {path}" for path in sorted(covered & excluded)
    )

    for relative in sorted(covered & actual):
        text = (REPO / relative).read_text(encoding="utf-8")
        if FOOTER not in text:
            problems.append(f"{relative}: common-doc footer is missing")
        problems.extend(_link_problems(REPO / relative))
        problems.extend(_main_link_problems(REPO / relative))
    # GitHub's templates live in a dot-directory the map does not cover, and one of them
    # sends a contributor to a runbook by its `main` address.
    for template in sorted(REPO.glob(".github/**/*.md")):
        problems.extend(_main_link_problems(template))
    problems.extend(_layout_problems(covered & actual))

    current_paths = {
        item["path"]
        for item in documents
        if item["authority"] in {"definitive", "current"} and item["role"] != "plan"
    }
    for relative in sorted(current_paths):
        lowered = (REPO / relative).read_text(encoding="utf-8").lower()
        problems.extend(
            f"{relative}: retired assurance phrase {phrase!r}"
            for phrase in RETIRED_PHRASES
            if phrase in lowered
        )
        if "role: exact_solution" in lowered:
            problems.append(f"{relative}: retired exact_solution resource role")

    current = SYNOPSIS.read_text(encoding="utf-8")
    try:
        if current != expected_synopsis(current, document_map):
            problems.append("SYNOPSIS.md document map is stale")
    except ValueError as error:
        problems.append(str(error))
    if MAP.relative_to(REPO).as_posix() != "docs/project/document-map.yaml":
        problems.append("document-map location drifted from its public contract")
    return problems


def main() -> int:
    problems = check()
    if problems:
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        return 1
    document_map = load_map()
    count = len(document_map["documents"]) + sum(
        len(_matches(collection["pattern"])) for collection in document_map["collections"]
    )
    print(f"  documentation map covers {count} durable documents; footers and links resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
