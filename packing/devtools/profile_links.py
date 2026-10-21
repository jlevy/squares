"""Link evidenced people only inside explicitly authored site prose.

Reviewed credits keep their occurrence joins. Full names and exact public account
links are a separate presentation rule; aliases never become automatic name matches.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import cache
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, override
from urllib.parse import urlsplit

from sqpack.contributors import PROFILES_DIR, record_metadata


@dataclass(frozen=True)
class ProfileName:
    full_name: str
    label: str
    sort_key: tuple[str, str, str]


def _name_key(name: str) -> str:
    return " ".join(name.split()).casefold()


def profile_names(metadata: Mapping[str, Mapping[str, Any]]) -> dict[str, ProfileName]:
    """Choose labels across the whole registry using explicit family-name evidence."""
    surnames = Counter(
        _name_key(record["surname"]) for record in metadata.values() if record.get("surname")
    )
    handles = {
        identifier: next(
            (
                link["handle"]
                for kind in ("github", "twitter", "substack")
                for link in record.get("links", ())
                if link["kind"] == kind and link.get("handle")
            ),
            "",
        )
        for identifier, record in metadata.items()
    }
    labels = {
        identifier: (
            record["surname"]
            if surnames[_name_key(record["surname"])] == 1
            else record["display_name"]
        )
        if record.get("surname")
        else handles[identifier] or record["display_name"]
        for identifier, record in metadata.items()
    }
    counts = Counter(_name_key(label) for label in labels.values())
    labels = {
        identifier: metadata[identifier]["display_name"]
        if counts[_name_key(label)] > 1
        else label
        for identifier, label in labels.items()
    }
    counts = Counter(_name_key(label) for label in labels.values())
    labels = {
        identifier: f"{label} ({handles[identifier] or identifier})"
        if counts[_name_key(label)] > 1
        else label
        for identifier, label in labels.items()
    }
    counts = Counter(_name_key(label) for label in labels.values())
    return {
        identifier: ProfileName(
            record["display_name"],
            f"{labels[identifier]} ({identifier})"
            if counts[_name_key(labels[identifier])] > 1
            else labels[identifier],
            (
                _name_key(
                    record.get("surname") or handles[identifier] or record["display_name"]
                ),
                _name_key(record["display_name"]),
                identifier,
            ),
        )
        for identifier, record in metadata.items()
    }


@cache
def public_names() -> dict[str, ProfileName]:
    """The same registry-wide labels in sparse and complete builds."""
    return profile_names(record_metadata())


def profile_identifier(
    address: str, people: Mapping[str, ProfileName] | None = None
) -> str | None:
    """Recognize only local or canonical own-site profile destinations."""
    people = public_names() if people is None else people
    parsed = urlsplit(address)
    path = parsed.path
    if parsed.netloc:
        if (
            parsed.scheme != "https"
            or parsed.netloc != "jlevy.github.io"
            or not path.startswith("/squares/")
        ):
            return None
        path = path.removeprefix("/squares/")
    elif parsed.scheme:
        return None
    match = re.fullmatch(r"(?:\.\./)*profiles/([a-z0-9-]+)\.html", path)
    return match[1] if match and match[1] in people else None


def person_label(name: str, address: str) -> str:
    """Paper-front identities already have a reviewed profile destination."""
    identifier = profile_identifier(address)
    return public_names()[identifier].label if identifier is not None else name


@dataclass(frozen=True)
class AccountTarget:
    identifier: str
    labels: frozenset[str]


@dataclass(frozen=True)
class ProfileIndex:
    names: Mapping[str, str]
    accounts: Mapping[str, AccountTarget]
    ambiguous_names: frozenset[str]
    people: Mapping[str, ProfileName]
    personal_labels: Mapping[str, frozenset[str]]


def profile_index(metadata: Mapping[str, Mapping[str, Any]]) -> ProfileIndex:
    """Only unique full names and validated account destinations can identify people."""
    candidates: dict[str, set[str]] = {}
    spellings: dict[str, str] = {}
    accounts: dict[str, list[AccountTarget]] = {}
    people = profile_names(metadata)
    personal_labels: dict[str, frozenset[str]] = {}
    for identifier, record in metadata.items():
        names = {record["display_name"], record.get("real_name", "")}
        labels = {" ".join(name.split()).casefold() for name in names if name}
        for name in names:
            if len(name.split()) < 2:
                continue
            key = " ".join(name.split()).casefold()
            spellings.setdefault(key, name)
            candidates.setdefault(key, set()).add(identifier)
        personal_labels[identifier] = frozenset(
            _name_key(name)
            for name in (
                *names,
                *record.get("aliases", ()),
                people[identifier].label,
                *(link.get("handle", "") for link in record.get("links", ())),
                *(
                    "@" + link["handle"]
                    for link in record.get("links", ())
                    if link.get("handle")
                ),
            )
            if name
        )
        for link in record.get("links", []):
            if link["kind"] not in {"github", "twitter", "substack"}:
                continue
            link_labels = set(labels)
            if handle := link.get("handle"):
                link_labels.update({handle.casefold(), "@" + handle.casefold()})
            accounts.setdefault(link["url"].removesuffix("/"), []).append(
                AccountTarget(identifier, frozenset(link_labels))
            )
    ambiguous = frozenset(spellings[key] for key, ids in candidates.items() if len(ids) > 1)
    return ProfileIndex(
        {spellings[key]: next(iter(ids)) for key, ids in candidates.items() if len(ids) == 1},
        {
            url: targets[0]
            for url, targets in accounts.items()
            if len({target.identifier for target in targets}) == 1
        },
        ambiguous,
        people,
        personal_labels,
    )


@cache
def public_index() -> ProfileIndex:
    """Read committed identity metadata even in archive-sparse paper builds."""
    return profile_index(record_metadata())


def _name_pattern(index: ProfileIndex) -> re.Pattern[str] | None:
    names = sorted(index.names, key=lambda name: (-len(name), name))
    return (
        re.compile(
            r"(?<![\w@])(?:"
            + "|".join(r"\s+".join(re.escape(word) for word in name.split()) for name in names)
            + r")(?![\w-])"
        )
        if names
        else None
    )


def named_profile_ids(text: str, index: ProfileIndex) -> tuple[str, ...]:
    """Unique full-name identities in authored text, using the prose link boundaries."""
    pattern = _name_pattern(index)
    if pattern is None:
        return ()
    by_name = {_name_key(name): identifier for name, identifier in index.names.items()}
    return tuple(
        dict.fromkeys(by_name[_name_key(match[0])] for match in pattern.finditer(text))
    )


_EXCLUDED = frozenset(
    {
        "a",
        "code",
        "pre",
        "math",
        "svg",
        "script",
        "style",
        "blockquote",
        "q",
        "textarea",
        "head",
        "nav",
        "footer",
        "table",
    }
)
_HEADINGS = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
_VOID = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
)
_ATTRIBUTE = re.compile(r"([^\s=/>]+)(?:\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+))?")


class _Prose(HTMLParser):
    def __init__(
        self,
        index: ProfileIndex,
        *,
        prefix: str,
        current_profile: str | None,
        audit: bool = False,
    ) -> None:
        super().__init__(convert_charrefs=False)
        self.index = index
        self.prefix = prefix
        self.current_profile = current_profile
        self.audit = audit
        self.parts: list[str] = []
        self.stack: list[tuple[str, bool, frozenset[str]]] = []
        self.anchor: tuple[int, AccountTarget, bool] | None = None
        self.anchor_data: list[int] = []
        self.anchor_protected = False
        self.anchor_text: list[str] = []
        self.unlinked: Counter[str] = Counter()
        self.label_mismatches: Counter[str] = Counter()
        self.contexts: dict[str, Counter[str]] = {}
        self.pattern = _name_pattern(index)
        self.by_name = {
            " ".join(name.split()).casefold(): identifier
            for name, identifier in index.names.items()
        }

    def enabled(self) -> bool:
        return not any(blocked for _, blocked, _ in self.stack)

    @override
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        if tag == "a" and self.enabled() and sum(name == "href" for name, _ in attrs) == 1:
            address = attributes.get("href") or ""
            identifier = profile_identifier(address, self.index.people)
            if self.audit and identifier is None and self.prefix == "profiles/":
                identifier = profile_identifier(self.prefix + address, self.index.people)
            target = self.index.accounts.get(address.removesuffix("/"))
            if identifier is not None:
                target = AccountTarget(identifier, self.index.personal_labels[identifier])
            if target is not None and target.identifier != self.current_profile:
                self.anchor = len(self.parts), target, identifier is not None
                self.anchor_text = []
                self.anchor_data = []
                self.anchor_protected = False
        self.parts.append(self.get_starttag_text() or "")
        if tag not in _VOID:
            blocked = tag in (_EXCLUDED - {"table"} if self.audit else _EXCLUDED) or bool(
                {"kpress-math", "katex"}.intersection(classes)
            )
            if not self.audit:
                blocked = blocked or tag in _HEADINGS or "site-contributor-sources" in classes
            if self.anchor is not None and tag != "a" and blocked:
                self.anchor_protected = True
            self.stack.append((tag, blocked, frozenset(classes)))

    @override
    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in _VOID:
            self.stack.pop()

    @override
    def handle_endtag(self, tag: str) -> None:
        suffix = ""
        if tag == "a" and self.anchor is not None:
            start, target, is_profile = self.anchor
            text = " ".join("".join(self.anchor_text).split())
            personal = text
            for ending in ("\u2019s", "'s", "\u2019", "'"):
                if personal.endswith(ending):
                    personal = personal.removesuffix(ending)
                    suffix = ending
                    break
            if (
                self.audit
                and not self.anchor_protected
                and is_profile
                and _name_key(personal) in target.labels
                and personal != self.index.people[target.identifier].label
                and not any(
                    tag in _HEADINGS
                    or "site-contributor-sources" in classes
                    or "site-profile-table" in classes
                    for tag, _, classes in self.stack
                )
            ):
                self.label_mismatches[target.identifier] += 1
            if (
                not self.audit
                and not self.anchor_protected
                and _name_key(personal) in target.labels
            ):
                if not is_profile:
                    href = html.escape(
                        f"{self.prefix}{PROFILES_DIR}/{target.identifier}.html", quote=True
                    )
                    original = self.parts[start]
                    changes: list[tuple[int, int, str]] = []
                    for attribute in _ATTRIBUTE.finditer(original, 1):
                        if attribute[1].lower() == "href":
                            first, last = attribute.span(2)
                            changes.append((first, last, f'"{href}"'))
                        elif (
                            attribute[1].lower() == "target"
                            and (attribute[2] or "").strip("\"'").lower() == "_blank"
                        ):
                            changes.append((*attribute.span(), ""))
                    for first, last, replacement in sorted(changes, reverse=True):
                        original = original[:first] + replacement + original[last:]
                    self.parts[start] = original
                for position in self.anchor_data:
                    self.parts[position] = ""
                if self.anchor_data:
                    self.parts[self.anchor_data[0]] = html.escape(
                        self.index.people[target.identifier].label
                    )
            else:
                suffix = ""
            self.anchor = None
        self.parts.append(f"</{tag}>" + suffix)
        for position in range(len(self.stack) - 1, -1, -1):
            if self.stack[position][0] == tag:
                del self.stack[position:]
                break

    @override
    def handle_data(self, data: str) -> None:
        if self.anchor is not None:
            self.anchor_text.append(data)
            self.anchor_data.append(len(self.parts))
        if self.pattern is None or not self.enabled():
            self.parts.append(data)
            return

        def replace(match: re.Match[str]) -> str:
            name = match[0]
            identifier = self.by_name[" ".join(name.split()).casefold()]
            if identifier == self.current_profile:
                return name
            self.unlinked[name] += 1
            if self.audit:
                classes = {name for _, _, names in self.stack for name in names}
                if any(tag in {"h1", "h2", "h3", "h4", "h5", "h6"} for tag, _, _ in self.stack):
                    context = "heading"
                elif "site-contributor-sources" in classes:
                    context = "profile source evidence"
                elif "site-case-prose" in classes:
                    context = "case narrative"
                elif "site-case-result-summary" in classes:
                    context = "case result summary"
                elif "site-case-data" in classes or "site-case-figure" in classes:
                    context = "case structured facts"
                elif "site-result" in classes:
                    context = "result structured facts"
                elif any(tag == "table" for tag, _, _ in self.stack):
                    context = "structured table"
                else:
                    context = "reader prose"
                self.contexts.setdefault(context, Counter())[name] += 1
                return name
            label = html.escape(self.index.people[identifier].label)
            return f'<a href="{self.prefix}{PROFILES_DIR}/{identifier}.html">{label}</a>'

        self.parts.append(self.pattern.sub(replace, data))

    @override
    def handle_entityref(self, name: str) -> None:
        if self.anchor is not None:
            self.anchor_data.append(len(self.parts))
        self.parts.append(f"&{name};")
        if self.anchor is not None:
            self.anchor_text.append(html.unescape(f"&{name};"))

    @override
    def handle_charref(self, name: str) -> None:
        if self.anchor is not None:
            self.anchor_data.append(len(self.parts))
        self.parts.append(f"&#{name};")
        if self.anchor is not None:
            self.anchor_text.append(html.unescape(f"&#{name};"))

    @override
    def handle_comment(self, data: str) -> None:
        self.parts.append(f"<!--{data}-->")

    @override
    def handle_decl(self, decl: str) -> None:
        self.parts.append(f"<!{decl}>")


def link_prose(
    markup: str,
    *,
    current_profile: str | None = None,
    prefix: str = "",
    index: ProfileIndex | None = None,
) -> str:
    """Link unique full names and exact account labels inside one authored fragment."""
    parser = _Prose(
        index if index is not None else public_index(),
        prefix=prefix,
        current_profile=current_profile,
    )
    parser.feed(markup)
    parser.close()
    return "".join(parser.parts)


def audit_site(root: Path) -> dict[str, Any]:
    """Report remaining full-name prose by surface, including retained table credits."""
    index = public_index()
    surfaces = sorted(root.rglob("*.html"))
    remaining = {}
    label_mismatches = {}
    contexts: dict[str, dict[str, dict[str, int]]] = {}
    for path in surfaces:
        if not path.is_file():
            continue
        parser = _Prose(
            index,
            prefix="profiles/" if path.parent == root / "profiles" else "",
            current_profile=path.stem if path.parent.name == "profiles" else None,
            audit=True,
        )
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
        if parser.label_mismatches:
            label_mismatches[path.relative_to(root).as_posix()] = dict(parser.label_mismatches)
        if parser.unlinked:
            relative = path.relative_to(root).as_posix()
            remaining[relative] = dict(sorted(parser.unlinked.items()))
            for context, names in parser.contexts.items():
                contexts.setdefault(context, {})[relative] = dict(sorted(names.items()))
    by_surface: dict[str, dict[str, int]] = {}
    for path, names in remaining.items():
        surface = path.split("/", 1)[0] + "/" if "/" in path else path
        counts = by_surface.setdefault(surface, {"pages": 0, "mentions": 0})
        counts["pages"] += 1
        counts["mentions"] += sum(names.values())
    return {
        "scanned_html_pages": len(surfaces),
        "counts_by_surface": by_surface,
        "remaining_by_context": contexts,
        "remaining_full_names": remaining,
        "ambiguous_full_names": sorted(index.ambiguous_names),
        "profile_link_label_mismatches": label_mismatches,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-site", type=Path, required=True)
    options = parser.parse_args(argv)
    print(json.dumps(audit_site(options.audit_site), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
