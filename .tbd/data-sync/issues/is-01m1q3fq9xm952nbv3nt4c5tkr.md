---
type: is
id: is-01m1q3fq9xm952nbv3nt4c5tkr
title: "kpress: expose the static asset root as a public API"
kind: task
status: open
priority: 2
version: 3
labels:
  - kpress-upstream
dependencies: []
parent_id: is-01m1q3fmvn9py28rcm0q3jadvk
created_at: 2026-09-04T20:59:10.013Z
updated_at: 2026-09-04T21:00:06.790Z
---
A consumer building one self-contained HTML file (fonts and KaTeX inlined, nothing fetched at view time, for a CSP admitting no external stylesheet) needs the static assets from disk. kpress exposes `package_asset_url()`, which returns a served URL path, and `package_asset_manifest()`; neither yields a filesystem path. `packing/devtools/render_certificate_page.py` therefore reaches into `Path(kpress.format.__file__).parent / "static"`, which is private layout.

`DEFAULT_CSS_ASSETS` and `KATEX_CSS_ASSETS` are importable, so the load order is not duplicated. The remaining gap is only the root.

Proposal: a public accessor, `kpress.format.assets.static_root() -> Path`; or better, `standalone_css(inline_fonts=True) -> str` returning the chain with `page-reset.css` first and the six webfont URLs already rewritten to data URIs, which removes the whole inlining step from every offline consumer.
