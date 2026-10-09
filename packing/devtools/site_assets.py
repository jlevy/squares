"""The site's shared assets: what every page carries, published once and linked.

Every page of the site carries the same design system: kpress's stylesheets with their
faces, KaTeX's pruned stylesheets and faces, the relation glyphs, the math pipeline and
kpress's client behaviors. Inlined, they came to about 1.8 MB a page, 0.95 MB of it after
gzip, fetched again on every page a reader opened, since a page's own bytes are the only
thing a browser caches for it. Published here as files named by their content under the
site's `assets/` directory, they are fetched once and reused by every page after the
first; a file's name changes when its bytes do, so a cached copy is never stale.

`SiteAssets` collects the files: a face, a stylesheet or a script, each given a
content-hashed path (`fonts/pt-serif-latin-400-normal.<hash>.woff2`) through kpress's own
asset model (`kpress.format.assets.AssetRef`, `content_hash`), so the hashing and the
manifest are kpress's and only the bytes are the site's. A stylesheet names its faces
relative to itself (`../fonts/...`), so it reads the same from every page; a page names
the stylesheet relative to where the page is served (`asset_href`), so it does too.

`shared()` is the site's bundle, built from the same functions the papers and the site
pages inlined their assets from, and each build that writes pages writes the bundle
beside them (`SiteAssets.write`). Two builds that write the same file write the same
bytes under the same name, so the Pages workflow's separately built artifacts merge into
one `assets/` without a conflict.
"""

from __future__ import annotations

import base64
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from functools import cache
from html import escape
from pathlib import Path, PurePosixPath
from typing import Literal, NamedTuple

from kpress.format.assets import AssetLoading, AssetRef, content_hash
from kpress.output import write_bytes_atomic

from sqpack.probes import applied, probe

FONT_PRELOAD_PROGRAM = Path(__file__).resolve().parent / "probes/site_assets/preload_fonts.js"

#: The directory under the site's root the shared assets are published in.
ASSETS_DIR = "assets"

#: The faces a page draws its first screen of text in, preloaded so the browser asks for
#: them with the stylesheet rather than after laying the text out. Every face is declared
#: `font-display: block`, so a face that arrives late holds the text it draws invisible,
#: laid out in the fallback's advances, and the text around it moves when it arrives.
#: Emphasis is first-screen text: italic and bold PT Serif in the frontier's opening
#: paragraphs, left to the first layout to discover, arrived after it and moved them by
#: CLS 0.134 and 0.209 on the hosted runner (paper-design.md, Shared Assets).
PRELOADED_FACES = (
    "pt-serif-latin-400-normal.woff2",
    "pt-serif-latin-400-italic.woff2",
    "source-sans-3-latin-wght-normal.woff2",
    "pt-serif-latin-700-normal.woff2",
)

_MEDIA_TYPES = {".woff2": "font/woff2", ".css": "text/css", ".js": "text/javascript"}


@dataclass(frozen=True)
class SiteAsset:
    """One file to publish under `assets/`: kpress's reference to it, and its bytes."""

    ref: AssetRef
    data: bytes


class SiteAssets:
    """The files a set of pages links, each named by its content."""

    def __init__(self) -> None:
        self._files: dict[str, SiteAsset] = {}
        self._faces: dict[str, AssetRef] = {}

    def _add(self, folder: str, name: str, data: bytes, loading: AssetLoading) -> AssetRef:
        source = PurePosixPath(name)
        if source.name != name or not source.suffix:
            raise SystemExit(f"a site asset is named by a plain file name, not {name!r}")
        digest = content_hash(data)
        output = f"{folder}/{source.stem}.{digest}{source.suffix}"
        ref = AssetRef(
            id=f"{folder}/{name}",
            kind="generated",
            path=f"{folder}/{name}",
            media_type=_MEDIA_TYPES.get(source.suffix, "application/octet-stream"),
            content_hash=digest,
            output_path=output,
            entry_point=loading != "resource",
            loading=loading,
            mode="hashed",
        )
        self._files[output] = SiteAsset(ref, data)
        return ref

    def face(self, name: str, data: bytes) -> str:
        """A face, as a stylesheet in `css/` names it: a `FaceSink`
        (`render_n11_lower_bounds_explainer.FaceSink`)."""
        ref = self._add("fonts", name, data, "resource")
        known = self._faces.setdefault(name, ref)
        if known.output_path != ref.output_path:
            raise SystemExit(f"two faces named {name} with different bytes")
        return f"../{ref.output_path}"

    def face_ref(self, name: str) -> AssetRef | None:
        """The face added under `name`, if one was."""
        return self._faces.get(name)

    def stylesheet(self, name: str, css: str) -> AssetRef:
        if "</style" in css.lower():
            raise SystemExit(f"{name} contains a closing style tag")
        return self._add("css", name, css.encode("utf-8"), "stylesheet")

    def script(self, name: str, js: str) -> AssetRef:
        if "</script" in js.lower():
            raise SystemExit(f"{name} contains a closing script tag")
        return self._add("js", name, js.encode("utf-8"), "classic")

    def stylesheet_file(self, path: Path) -> AssetRef:
        """A stylesheet of the repository's, by its own name."""
        return self.stylesheet(path.name, path.read_text(encoding="utf-8"))

    def script_file(self, path: Path) -> AssetRef:
        """A page program of the repository's, by its own name."""
        return self.script(path.name, path.read_text(encoding="utf-8"))

    def referenced(self, texts: Iterable[str]) -> dict[str, bytes]:
        """Every file of the bundle that `texts`, pages, name, with every face a named
        stylesheet names: what a directory holding those pages has to hold under
        `assets/`, by path under it. A page that names a file the bundle does not hold
        fails, since it would draw without it."""
        wanted: set[str] = set()
        for text in texts:
            wanted.update(_PAGE_REFERENCE.findall(text))
        for output in sorted(wanted):
            asset = self._files.get(output)
            if asset is None:
                raise SystemExit(f"a page names {ASSETS_DIR}/{output}, which no build wrote")
            if asset.ref.loading == "stylesheet":
                wanted.update(_STYLESHEET_REFERENCE.findall(asset.data.decode("utf-8")))
        return {output: self._files[output].data for output in sorted(wanted)}

    def files(self) -> dict[str, bytes]:
        """Every file, by its path under `assets/`."""
        return {output: asset.data for output, asset in sorted(self._files.items())}

    def inlined(self, page: str) -> str:
        """`page` with every file of the bundle it links put back in it (`inline_assets`)."""

        def read(output: str) -> bytes:
            found = self._files.get(output)
            if found is None:
                raise SystemExit(f"a page names {ASSETS_DIR}/{output}, which no build wrote")
            return found.data

        return inline_assets(page, read)


def inline_assets(page: str, read: Callable[[str], bytes]) -> str:
    """`page` with every shared asset it links put back in it: a stylesheet as a `<style>`
    with its faces as data URIs, a script as an inline `<script>`, and the face preloads
    dropped. The page as a reader's browser assembles it, as one file, for a tool or a
    test that reads a page whole or opens it with nothing beside it. `read` gives a
    file's bytes by its path under `assets/`: from a bundle (`SiteAssets.inlined`) or
    from a built site (`inlined_from`)."""
    from devtools.render_n11_lower_bounds_explainer import inline_face  # noqa: PLC0415

    for tag in _MARKED_STYLESHEET_TAG.finditer(page):
        if _STYLESHEET_TAG.fullmatch(tag[0]) is None:
            raise SystemExit(f"unsupported marked math stylesheet: {tag[0]}")

    def checked_read(output: str) -> bytes:
        if any(part in ("", ".", "..") for part in output.split("/")) or any(
            character in output for character in "\\?#\x00"
        ):
            raise SystemExit(f"invalid shared asset path: {output!r}")
        return read(output)

    def style(match: re.Match[str]) -> str:
        css = checked_read(match.group("output")).decode("utf-8")
        css = _STYLESHEET_REFERENCE.sub(
            lambda face: f'url("{inline_face(face.group(1), checked_read(face.group(1)))}")',
            css,
        )
        marker = " data-site-math-styles" if match.group("marker") else ""
        return f"<style{marker}>{css}</style>"

    def script(match: re.Match[str]) -> str:
        return f"<script>{checked_read(match.group(1)).decode('utf-8')}</script>"

    page = _PRELOAD_TAG.sub("", page)
    page = _FONT_PRELOAD_BOOTSTRAP_TAG.sub("", page)
    page = _STYLESHEET_TAG.sub(style, page)
    return _SCRIPT_TAG.sub(script, page)


def inlined_from(site: Path, page: str) -> str:
    """The page `page`, a path from `site`'s root, with the shared assets it links put
    back in it from `site`'s own `assets/` (`inline_assets`)."""
    root = site / ASSETS_DIR
    text = (site / page).read_text(encoding="utf-8")
    return inline_assets(text, lambda output: (root / output).read_bytes())


def write_assets(site: Path, files: dict[str, bytes]) -> None:
    """Publish a producer's assets without removing another producer's files.

    Content-addressed paths are immutable. A different payload at an existing path
    indicates corruption or a collision, and publication refuses it.
    """
    root = site / ASSETS_DIR
    for output, data in files.items():
        relative = PurePosixPath(output)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"invalid asset path: {output!r}")
        path = root / output
        if path.exists():
            if not path.is_file() or path.read_bytes() != data:
                raise ValueError(f"asset collision: {path}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        write_bytes_atomic(path, data)


def stale_assets(site: Path, files: dict[str, bytes], *, exact: bool = False) -> list[str]:
    """Missing or changed producer assets; optionally include unclaimed files.

    Shared publication combines several independent producers. Only a caller owning
    the complete assembled manifest can request an exact directory comparison.
    """
    root = site / ASSETS_DIR
    present = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    compared = present | set(files) if exact else set(files)
    return [
        f"{ASSETS_DIR}/{output}"
        for output in sorted(compared)
        if output not in files
        or output not in present
        or (root / output).read_bytes() != files[output]
    ]


_INLINE_STYLE = re.compile(
    r"<style(?P<marker> data-site-math-styles)?>(?P<css>.*?)</style>", re.DOTALL
)
_MARKED_INLINE_STYLE = re.compile(
    r"<style\b[^>]*\bdata-site-math-styles(?=\s|=|>)[^>]*>.*?</style>",
    re.DOTALL,
)
_INLINE_SCRIPT = re.compile(r"<script>(.*?)</script>", re.DOTALL)
_INLINE_FONT = re.compile(r"url\([\"']?data:font/woff2;base64,([A-Za-z0-9+/=]+)[\"']?\)")


def link_inline_assets(
    page: str, page_path: str, *, assets: SiteAssets | None = None
) -> tuple[str, dict[str, bytes]]:
    """Publish an already prepared inline page as linked, cacheable assets.

    The bytes of CSS and scripts retain their order. Tiny head scripts stay inline
    because they set preferences before first paint. JSON data blocks are untouched.
    Fonts reuse the shared bundle's names wherever their bytes match.
    """
    for tag in _MARKED_INLINE_STYLE.finditer(page):
        if _INLINE_STYLE.fullmatch(tag[0]) is None:
            raise SystemExit(f"unsupported marked inline math stylesheet: {tag[0]}")
    bundle = shared()
    target = assets if assets is not None else bundle.assets
    names = {
        data: PurePosixPath(name).name.rsplit(".", 2)[0] + ".woff2"
        for name, data in bundle.assets.files().items()
        if name.endswith(".woff2")
    }
    inline_shared = {
        bundle.assets.inlined(stylesheet_tag(ref, page_path)): ref
        for ref in (bundle.kpress_css, bundle.katex_css, bundle.relation_css)
    }
    if target is bundle.assets:
        # The explainer originally combines these two stylesheets in one element.
        joined = (
            "<style>"
            + "".join(
                text.removeprefix("<style>").removesuffix("</style>")
                for text in list(inline_shared)[:2]
            )
            + "</style>"
        )
        page = page.replace(
            joined,
            stylesheet_tag(bundle.kpress_css, page_path)
            + stylesheet_tag(bundle.katex_css, page_path),
        )
        for inline, ref in inline_shared.items():
            page = page.replace(inline, stylesheet_tag(ref, page_path))

    def font(match: re.Match[str]) -> str:
        data = base64.b64decode(match.group(1), validate=True)
        name = names.get(data, f"font-{content_hash(data)}.woff2")
        return f'url("{target.face(name, data)}")'

    def style(match: re.Match[str]) -> str:
        css = _INLINE_FONT.sub(font, match.group("css"))
        marker = bool(match.group("marker"))
        name = "site-math.css" if marker else "page.css"
        linked = stylesheet_tag(target.stylesheet(name, css), page_path)
        return linked.replace("<link ", "<link data-site-math-styles ", 1) if marker else linked

    page = _INLINE_STYLE.sub(style, page)
    head_end = page.find("</head>")

    def script(match: re.Match[str]) -> str:
        text = match.group(1)
        if match.start() < head_end and len(text.encode("utf-8")) <= 4096:
            return match.group(0)
        return script_tag(target.script("page.js", text), page_path)

    page = _INLINE_SCRIPT.sub(script, page)
    files = target.referenced([page])
    preloads = {
        reference[1]: tag
        for tag in preload_tags(target, page_path).splitlines()
        if (reference := _PAGE_REFERENCE.search(tag)) and reference[1] in files
    }
    if preloads and _STYLESHEET_TAG.search(page):
        page = _PRELOAD_TAG.sub(
            lambda match: (
                ""
                if any(name in preloads for name in _PAGE_REFERENCE.findall(match[0]))
                else match[0]
            ),
            page,
        )
        page = _FONT_PRELOAD_BOOTSTRAP_TAG.sub("", page)
        first_sheet = _STYLESHEET_TAG.search(page)
        assert first_sheet is not None
        offset = first_sheet.start()
        page = (
            page[:offset]
            + "\n".join(preloads.values())
            + "\n"
            + font_preload_bootstrap_tag()
            + "\n"
            + page[offset:]
        )
    return page, files


def read_inline_page(path: Path) -> str:
    """Read a published or offline page, resolving linked assets from its own root."""
    text = path.read_text(encoding="utf-8")
    # The offline tool consumes the page without a base URL or network access.
    # Stable publication favicons can therefore be replaced by their inline SVG.
    from devtools.render_overview import favicon_html  # noqa: PLC0415

    text, icons = re.subn(
        r'<link\b[^>]*rel="(?:icon|apple-touch-icon)"[^>]*href="(?:\.\./)*(?:favicon\.svg|favicon-48\.png|apple-touch-icon\.png)"[^>]*>',
        "",
        text,
    )
    if icons and favicon_html(inline=True) not in text:
        text = text.replace("</head>", favicon_html(inline=True) + "</head>", 1)
    roots = {
        (path.parent / match.group(1)).resolve()
        for match in re.finditer(r'(?:href|src)="((?:\.\./)*assets)/[^"#?]+"', text)
    }
    if not roots:
        return text
    if len(roots) != 1:
        raise ValueError(f"page references multiple asset roots: {path}")
    root = roots.pop()
    return inline_assets(text, lambda output: (root / output).read_bytes())


#: A file of the bundle as a page names it, from any depth, and as a stylesheet in
#: `css/` names a face; each captures the path under `assets/`.
_PAGE_REFERENCE = re.compile(rf'(?:href|src)="(?:\.\./)*{ASSETS_DIR}/([^"#?]+)"')
_STYLESHEET_REFERENCE = re.compile(r'url\("\.\./(fonts/[^"]+)"\)')
#: The three tags this module writes into a page, as `stylesheet_tag`, `script_tag` and
#: `preload_tags` write them, each capturing the path under `assets/`.
_STYLESHEET_TAG = re.compile(
    rf'<link(?P<marker> data-site-math-styles)? rel="stylesheet" '
    rf'href="(?:\.\./)*{ASSETS_DIR}/(?P<output>[^"]+)">'
)
# Only the generated bare math marker is supported; malformed marked links fail
# instead of silently leaving an external stylesheet in a self-contained export.
_MARKED_STYLESHEET_TAG = re.compile(r"<link\b[^>]*\bdata-site-math-styles(?=\s|=|>)[^>]*>")
_SCRIPT_TAG = re.compile(rf'<script src="(?:\.\./)*{ASSETS_DIR}/([^"]+)"></script>')
_PRELOAD_TAG = re.compile(
    rf'<link (?:rel="preload"|data-site-font-preload) '
    rf'href="(?:\.\./)*{ASSETS_DIR}/[^"]+"[^>]*>\n?'
)
_FONT_PRELOAD_BOOTSTRAP_TAG = re.compile(
    r"<script data-site-font-preloads>.*?</script>\n?", re.DOTALL
)


def asset_href(ref: AssetRef, page: str) -> str:
    """The address `page`, a path from the site's root, names `ref` by."""
    if ref.output_path is None:
        raise SystemExit(f"{ref.id} has no output path")
    depth = PurePosixPath(page).parent.parts
    return "../" * len(depth) + f"{ASSETS_DIR}/{ref.output_path}"


def stylesheet_tag(ref: AssetRef, page: str) -> str:
    return f'<link rel="stylesheet" href="{escape(asset_href(ref, page))}">'


def script_tag(ref: AssetRef, page: str) -> str:
    """A classic script element, parsed and run where it stands, as the inline one it
    replaces was."""
    return f'<script src="{escape(asset_href(ref, page))}"></script>'


def preload_tags(assets: SiteAssets, page: str) -> str:
    """Inert font declarations, activated with the correct protocol's credentials
    before stylesheets. With no JavaScript, the existing CSS loads its faces normally."""
    tags = []
    for name in PRELOADED_FACES:
        ref = assets.face_ref(name)
        if ref is not None:
            href = escape(asset_href(ref, page))
            tags.append(
                f'<link data-site-font-preload href="{href}" as="font" type="font/woff2">'
            )
    if tags:
        tags.append(font_preload_bootstrap_tag())
    return "\n".join(tags)


def font_preload_bootstrap_tag() -> str:
    """The reviewed prepaint program; no active CORS hint precedes its decision."""
    program = applied(probe(Path(__file__).with_name("probes"), "site_assets/preload_fonts"))
    return f"<script data-site-font-preloads>{program}</script>"


class SharedAssets(NamedTuple):
    """The site's bundle, and the files of it each page links, in the order they apply."""

    assets: SiteAssets
    #: kpress's design system and KaTeX's stylesheets, as `kpress_css` and `katex_css`.
    kpress_css: AssetRef
    katex_css: AssetRef
    #: The relation glyphs (`relation_face_css`).
    relation_css: AssetRef
    #: The math pipeline (`katex_js`).
    katex_js: AssetRef

    def head(self, page: str, *, katex: Literal["joined", "apart"] = "joined") -> str:
        """The face preloads and the three stylesheets, for `page`'s head. `katex` is
        whether KaTeX's stylesheet follows kpress's directly, as the site pages and the
        lower-bounds paper have it; the order is the cascade, so a caller that put
        another stylesheet between them keeps doing so with `apart` and links
        `katex_css` itself."""
        tags = [preload_tags(self.assets, page), stylesheet_tag(self.kpress_css, page)]
        if katex == "joined":
            tags.append(stylesheet_tag(self.katex_css, page))
        tags.append(stylesheet_tag(self.relation_css, page))
        return "\n".join(tag for tag in tags if tag)


@cache
def shared() -> SharedAssets:
    """The site's bundle, from the functions every page took its assets from."""
    from devtools.render_n11_lower_bounds_explainer import (  # noqa: PLC0415
        katex_css,
        katex_js,
        kpress_css,
        kpress_static,
        relation_face_css,
    )

    static = kpress_static()
    assets = SiteAssets()
    return SharedAssets(
        assets=assets,
        kpress_css=assets.stylesheet("kpress.css", kpress_css(static, assets.face)),
        katex_css=assets.stylesheet("katex.css", katex_css(static, assets.face)),
        relation_css=assets.stylesheet("relations.css", relation_face_css(static, assets.face)),
        katex_js=assets.script("katex-math.js", katex_js(static)),
    )
