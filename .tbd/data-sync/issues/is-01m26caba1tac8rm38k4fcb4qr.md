---
type: is
id: is-01m26caba1tac8rm38k4fcb4qr
title: The explainer discards the font-wait status, so a three-second timeout passes silently
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-10T19:22:07.553Z
updated_at: 2026-09-10T19:22:07.553Z
---
`vendor/kpress/.../katex/katex-math-runtime.js` bounds its font waits with a wall clock:

```js
const FACE_WAIT_MS = 3000;
loadEntries.set(promise, { entry, deadline: performance.now() + FACE_WAIT_MS });
```

and resolves `ready()` with a `{status}` object that says whether the faces arrived or the
deadline did. Both of the explainer's callers discard it:
`squaresMath.ready.then(boot)` and `squaresMath.ready.then(typeset)` in
`devtools/templates/explainer-shell.html` take no argument.

With `allEmbeddedFonts: true` the runtime asks every face in `document.fonts` to load, so on
a loaded runner three seconds is a wall-clock fact rather than a content fact. That makes it
the one genuine clock dependency left in the render path: the same page can take the timeout
branch on a busy machine and not on an idle one. A timeout leaves raw TeX in the element, so
the cost when it fires is hundreds of bytes and visible -- which is also why it is not the
explanation for D-490's two bytes.

Two things worth doing, in order: have the explainer read the `{status}` it is handed and
fail or warn rather than silently proceeding, and have `render_explainer_pdf` refuse a render
whose faces timed out instead of drawing it. Neither needs kpress to change.

Found by a read-only audit of the page's scripts on 2026-09-10, while looking for the cause
of D-490.
