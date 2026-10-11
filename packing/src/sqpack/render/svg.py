"""Safe deterministic SVG construction on the standard-library XML tree."""

from __future__ import annotations

import base64
import binascii
import copy
import re
from pathlib import Path
from xml.etree import ElementTree as ET

from strif import atomic_output_file

SVG_NS = "http://www.w3.org/2000/svg"
SQPACK_NS = "https://github.com/jlevy/thinking-scratchpad/ns/sqpack/v1"
# Bumped whenever rendered output bytes change for the same input (8: rotation unwrapping).
RENDERER_VERSION = "8"
XML_DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>\n'
MOTION_MARKER = "sqpack-motion-v1"
PRINT_FONT_MARKER = "sqpack-print-fonts-v1"
PRINT_FONT_FAMILY = "Squares Atlas Print"
PRINT_ITALIC_FAMILY = "SquaresAtlasPrint-BoldItalic"
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
    "tspan",
    "defs",
    "clipPath",
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


def append_metadata(
    root: ET.Element,
    records: dict[str, str],
    *,
    coordinates: str = "mathematical-y-up; svg-y-down",
) -> ET.Element:
    metadata = sub(root, "metadata")
    profile = sub(metadata, "profile", {"version": RENDERER_VERSION})
    sub(profile, "coordinates").text = coordinates
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
    # The grammar is an allow-list, not a formality: this CSS is inlined into a document
    # meant to be self-contained and embeddable, so anything outside the vocabulary the
    # renderer emits should be refused rather than shipped. Rotation and the transform box
    # were added when the motion model stopped being translation-only; extending it is a
    # deliberate act, which is the point of writing the shapes out.
    keyframes = re.compile(
        r"@keyframes sqpack-[A-Za-z0-9_.-]+\{"
        r"(?:[0-9.]+%\{transform:translate\(-?[0-9.]+px,-?[0-9.]+px\)"
        r"(?: rotate\(-?[0-9.]+deg\))?(?:;filter:saturate\([0-9.]+\))?\})+\}"
    )
    animations = re.compile(
        r"\.motion-[A-Za-z0-9_.-]+\{"
        r"(?:transform-box:fill-box;transform-origin:center;)?"
        r"animation:sqpack-[A-Za-z0-9_.-]+ "
        r"[0-9.]+s ease-in-out 1 forwards\}"
    )
    final_overlay_keyframes = re.compile(
        r"@keyframes sqpack-final-overlay\{0%\{opacity:0\}100%\{opacity:1\}\}"
    )
    final_overlay_animation = re.compile(
        r"\.motion-final-overlay\{animation:sqpack-final-overlay "
        r"[0-9.]+s step-end 1 forwards\}"
    )
    remainder = keyframes.sub("", body)
    remainder = animations.sub("", remainder)
    remainder = final_overlay_keyframes.sub("", remainder)
    remainder = final_overlay_animation.sub("", remainder)
    if remainder:
        raise ValueError("motion CSS lies outside the renderer grammar")


def _validate_print_font_css(css: str) -> None:
    """Check the CSS grammar and encoding of caller-trusted print-font declarations.

    The caller must supply CSS generated from trusted retained assets. This checks
    the declaration shape, canonical base64, and TrueType signature; it does not
    validate complete font structure or establish font identity or provenance.
    """
    # The leading license comment is inert; anything after its first terminator must
    # match both complete declarations, with no selectors, imports, or other URLs.
    if not css.startswith("/*\n") or "*/" not in css:
        raise ValueError("embedded print fonts require their license comment")
    _license, body = css.split("*/", 1)
    declarations = []
    for family, style in ((PRINT_FONT_FAMILY, "normal"), (PRINT_ITALIC_FAMILY, "italic")):
        declarations.append(
            r'@font-face \{ font-family: "'
            + re.escape(family)
            + r'"; font-style: '
            + style
            + r'; font-weight: 700; src: url\("data:font/ttf;base64,'
            + r'([A-Za-z0-9+/]+={0,2})"\) format\("truetype"\); \}'
        )
    match = re.fullmatch("\n".join(declarations), body.strip())
    if match is None:
        raise ValueError("print font CSS lies outside the retained-face grammar")
    for encoded in match.groups():
        try:
            content = base64.b64decode(encoded, validate=True)
        except binascii.Error as error:
            raise ValueError("embedded print font payload is not base64") from error
        if not content.startswith(b"\x00\x01\x00\x00"):
            raise ValueError("embedded print font payload is not TrueType")
        if base64.b64encode(content).decode("ascii") != encoded:
            raise ValueError("embedded print font payload is not canonical base64")


def validate_safe_tree(root: ET.Element, *, embedded_print_fonts: str | None = None) -> None:
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
            if (
                embedded_print_fonts is not None
                and node.attrib.get("data-sqpack-style") == PRINT_FONT_MARKER
                and css == embedded_print_fonts
            ):
                _validate_print_font_css(css)
                continue
            if node.attrib.get("data-sqpack-style") != MOTION_MARKER:
                raise ValueError("arbitrary CSS is forbidden")
            if any(token in css.lower() for token in ("url(", "@import")):
                raise ValueError("external CSS content is forbidden")
            _validate_motion_css(css)
    if styles > 1:
        raise ValueError("at most one motion style is supported")


def _strip_indent_inside_text(document: ET.Element) -> None:
    """Undo pretty-printing inside <text>.

    SVG collapses whitespace in text content, so the newline and indent that
    ``ET.indent`` inserts around a <tspan> would render as a stray space between
    the runs. Indentation is presentational everywhere else, so it stays.
    """
    for node in document.iter(svg_tag("text")):
        if node.text is not None and not node.text.strip():
            node.text = None
        for child in node:
            if child.tail is not None and not child.tail.strip():
                child.tail = None


def _strip_formatting_indent(document: ET.Element) -> None:
    """Remove cached formatting only from SVG and metadata container elements.

    Text, tspan, descriptions, style payloads and metadata values retain their whole
    subtrees: even whitespace-only runs there can be meaningful. A mixed-content
    container is also left intact. Plain spaces are never assumed to be indentation.
    """
    containers = {
        svg_tag(name) for name in ("svg", "g", "defs", "clipPath", "marker", "metadata")
    } | {sqpack_tag("profile")}

    def visit(node: ET.Element) -> None:
        if node.tag not in containers:
            return
        if (node.text and node.text.strip()) or any(
            child.tail and child.tail.strip() for child in node
        ):
            return
        if node.text and "\n" in node.text:
            node.text = None
        for child in node:
            visit(child)
            if child.tail and "\n" in child.tail:
                child.tail = None

    visit(document)


def serialize_svg(
    root: ET.Element,
    *,
    embedded_print_fonts: str | None = None,
    compact: bool = False,
) -> str:
    """Serialize safely, optionally omitting structural formatting indentation.

    Compact output preserves semantic whitespace in text and payload subtrees. The
    default keeps the established pretty-printing behavior and output bytes.
    """
    validate_safe_tree(root, embedded_print_fonts=embedded_print_fonts)
    document = copy.deepcopy(root)
    if compact:
        _strip_formatting_indent(document)
    else:
        ET.indent(document, space="  ")
        _strip_indent_inside_text(document)
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
