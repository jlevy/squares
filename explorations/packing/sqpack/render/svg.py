"""Safe deterministic SVG construction on the standard-library XML tree."""

from __future__ import annotations

import copy
import re
from pathlib import Path
from xml.etree import ElementTree as ET

from strif import atomic_output_file

SVG_NS = "http://www.w3.org/2000/svg"
SQPACK_NS = "https://github.com/jlevy/thinking-scratchpad/ns/sqpack/v1"
RENDERER_VERSION = "1"
XML_DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>\n'
MOTION_MARKER = "sqpack-motion-v1"
MOTION_MEDIA_PREFIX = "@media (prefers-reduced-motion: no-preference){"
ALLOWED_ELEMENTS = {
    "svg",
    "title",
    "desc",
    "metadata",
    "g",
    "rect",
    "polygon",
    "polyline",
    "line",
    "circle",
    "path",
    "text",
    "defs",
    "marker",
    "use",
    "style",
    "source",
    "value",
    "evidence",
    "profile",
    "coordinates",
    "feature",
}
URL_ATTRIBUTES = {"href", "src"}

ET.register_namespace("", SVG_NS)
ET.register_namespace("sqpack", SQPACK_NS)


def svg_tag(name: str) -> str:
    return f"{{{SVG_NS}}}{name}"


def sqpack_tag(name: str) -> str:
    return f"{{{SQPACK_NS}}}{name}"


def element(name: str, attributes: dict[str, str] | None = None, **extra: str) -> ET.Element:
    tag = (
        sqpack_tag(name)
        if name in {"source", "value", "evidence", "profile", "coordinates", "feature"}
        else svg_tag(name)
    )
    return ET.Element(tag, {**(attributes or {}), **extra})


def sub(
    parent: ET.Element, name: str, attributes: dict[str, str] | None = None, **extra: str
) -> ET.Element:
    child = element(name, attributes, **extra)
    parent.append(child)
    return child


def append_title_desc(root: ET.Element, title: str, description: str) -> None:
    if not title.strip() or not description.strip():
        raise ValueError("SVG title and description must be non-empty")
    sub(root, "title", {"id": "figure-title"}).text = title
    sub(root, "desc", {"id": "figure-description"}).text = description


def append_metadata(root: ET.Element, records: dict[str, str]) -> ET.Element:
    metadata = sub(root, "metadata")
    profile = sub(metadata, "profile", {"version": RENDERER_VERSION})
    sub(profile, "coordinates").text = "mathematical-y-up; svg-y-down"
    for key, value in sorted(records.items()):
        node = sub(profile, "value", {"name": key})
        node.text = value
    return metadata


def append_exact_comment(parent: ET.Element, text: str) -> None:
    if not text or "--" in text or text.endswith("-"):
        raise ValueError("invalid XML comment text")
    if any(ord(character) < 32 and character not in "\t\n\r" for character in text):
        raise ValueError("invalid XML character in comment")
    parent.append(ET.Comment(text))


def append_local_use(parent: ET.Element, fragment: str, **attributes: str) -> ET.Element:
    if not fragment.startswith("#") or any(token in fragment for token in (":", "/")):
        raise ValueError("SVG use reference must be a local fragment")
    return sub(parent, "use", {"href": fragment, **attributes})


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _namespace(tag: str) -> str:
    return tag[1:].split("}", 1)[0] if tag.startswith("{") else ""


def _validate_motion_css(css: str) -> None:
    if not css.startswith(MOTION_MEDIA_PREFIX) or not css.endswith("}"):
        raise ValueError("motion CSS is not reduced-motion scoped")
    body = css[len(MOTION_MEDIA_PREFIX) : -1]
    keyframes = re.compile(
        r"@keyframes sqpack-[A-Za-z0-9_.-]+\{"
        r"(?:[0-9.]+%\{transform:translate\(-?[0-9.]+px,-?[0-9.]+px\)\})+\}"
    )
    animations = re.compile(
        r"\.motion-[A-Za-z0-9_.-]+\{animation:sqpack-[A-Za-z0-9_.-]+ "
        r"[0-9.]+s ease-in-out 1 forwards\}"
    )
    remainder = keyframes.sub("", body)
    remainder = animations.sub("", remainder)
    if remainder:
        raise ValueError("motion CSS lies outside the renderer grammar")


def validate_safe_tree(root: ET.Element) -> None:
    if root.tag != svg_tag("svg"):
        raise ValueError("SVG document root must be svg")
    ids: set[str] = set()
    styles = 0
    for node in root.iter():
        if not isinstance(node.tag, str):
            continue
        if _namespace(node.tag) not in (SVG_NS, SQPACK_NS):
            raise ValueError("unsupported XML namespace")
        name = _local_name(node.tag)
        if name not in ALLOWED_ELEMENTS:
            raise ValueError(f"unsupported SVG element: {name}")
        identifier = node.attrib.get("id")
        if identifier:
            if identifier in ids:
                raise ValueError(f"duplicate SVG id: {identifier}")
            ids.add(identifier)
        for attribute, value in node.attrib.items():
            if _namespace(attribute):
                raise ValueError("namespaced SVG attributes are forbidden")
            local = _local_name(attribute)
            if local.lower().startswith("on") or local == "xlink":
                raise ValueError(f"unsafe SVG attribute: {local}")
            if local in URL_ATTRIBUTES and not value.startswith("#"):
                raise ValueError("external SVG reference is forbidden")
            if (
                "url(" in value.lower()
                and re.fullmatch(r"url\(#[A-Za-z][A-Za-z0-9_.-]*\)", value) is None
            ):
                raise ValueError("URL-bearing presentation attribute is forbidden")
        if name == "style":
            styles += 1
            css = node.text or ""
            if node.attrib.get("data-sqpack-style") != MOTION_MARKER:
                raise ValueError("arbitrary CSS is forbidden")
            if any(token in css.lower() for token in ("url(", "@import")):
                raise ValueError("external CSS content is forbidden")
            _validate_motion_css(css)
    if styles > 1:
        raise ValueError("at most one motion style is supported")


def serialize_svg(root: ET.Element) -> str:
    validate_safe_tree(root)
    document = copy.deepcopy(root)
    ET.indent(document, space="  ")
    text = (
        XML_DECLARATION
        + ET.tostring(document, encoding="unicode", short_empty_elements=True)
        + "\n"
    )
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    ET.fromstring(text, parser=parser)
    return text


def canonicalize_svg(text: str) -> str:
    return ET.canonicalize(text, with_comments=True)


def write_svg_atomic(path: str | Path, text: str) -> None:
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    root = ET.fromstring(text, parser=parser)
    if serialize_svg(root) != text:
        raise ValueError("SVG text is not canonical renderer output")
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(text, encoding="utf-8")


def safe_id(text: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", text).strip("-")
    if not value or not value[0].isalpha():
        value = f"id-{value}"
    return value
