# A Pages Preview, Served Locally

The tree GitHub Pages would serve, assembled so the URLs behave as they would deployed.
`upload-pages-artifact` takes `packing/site` whole, so a subdirectory is a URL, and this
mirrors that shape:

| path | what | built by |
| --- | --- | --- |
| `/` | the explainer | `devtools/render_explainer.py`, in CI |
| `/workbench/` | the workbench, its own address | the v2 spike generator |
| `/atlas/` | the slideshow | the v1 spike generator |
| `/embed/*.svg` | one animation per case | `devtools/export_animation_svg.py` |

## Why the explainer is a mockup here

`packing/site/` is gitignored and rendered in CI, where
`render_explainer.py --prepare-math` stamps font geometry into the page before it draws.
A local copy of that build renders wrong, so serving one would be testing a stale
artifact rather than the layout.
[`explainer-mockup.html`](explainer-mockup.html) stands in for it, and tests the only
thing this preview needs from that page: whether an embedded animation sits correctly in
a column of prose.

## Rebuild

From `packing`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_ascent \
  --from 2 --to 6 --render --out /tmp/ascent.json --svg /tmp/ascent.svg
```

Then assemble a directory with `index.html`, `workbench/`, `atlas/` and `embed/`, and
serve it with any static server.
The point of serving rather than opening files is that Pages resolves `/workbench/` to
that directory’s `index.html`, and a `file://` open does not.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
