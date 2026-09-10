---
type: is
id: is-01m26caas988anpy27k5tba184
title: Explainer sets math-ready before it finishes booting the page
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-10T19:22:07.017Z
updated_at: 2026-09-10T19:22:07.017Z
---
`devtools/templates/explainer-shell.html` adds the readiness class before it finishes
booting the page:

```js
kpressMathText.complete();
document.documentElement.classList.add('math-ready');
/* Footnote hover previews ... */
if (window.kpressInitTooltips) window.kpressInitTooltips(document, { only: "footnote" });
if (window.kpressInitCodeCopy) window.kpressInitCodeCopy(document);
```

`html.math-ready` is the signal four tools wait on before they measure or capture
(`render_explainer_pdf`, `check_math_faces`, `check_math_loading`,
`inspect_explainer_typography`, all importing `READY`). `kpressInitCodeCopy` prepends DOM
into every `<pre>` after the class is set, so the signal promises more than it delivers:
the page is not finished when it says it is.

Nothing is broken today, and the reason is timing rather than design -- Playwright cannot
observe the class between two statements of the same task, so every wait in practice
returns after both init calls have run. Moving the `classList.add` below them costs nothing
and makes the guarantee real rather than incidental.

Found by a read-only audit of the page's scripts on 2026-09-10, while looking for the cause
of D-490.
