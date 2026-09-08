---
softschema:
  contract: squares.math-startup.exploration.v1
  schema: ../schemas/exploration.schema.yaml
  status: enforced
id: X-001
title: Font readiness, parameter scheduling, and reserved geometry
proposes: [H-001, H-002]
---
# Font Readiness, Parameter Scheduling, and Reserved Geometry

The deployed page embeds its font bytes, but browser parsing and font decoding are still
asynchronous. Its no-swap fix hides formulas until the correct faces are ready.
That visibility policy does not fix the advance width of a hidden formula: font fallback
can still determine its intrinsic dimensions before the shipped face loads.

Squares’ host initialization enables `allEmbeddedFonts`, then waits on readiness before
booting both certificates.
Each boot builds a 230 by 230 heat map before updating its readouts, including the
hidden certificate. Finally, root-level pending CSS keeps all math hidden until the
static expressions and interactive renders settle.
These are source-confirmed dependencies, not measured cost attribution.
A ResizeObserver can also request readouts before boot, which is why first render call
and first correct visible frame must be measured separately.

KPress waits for a broad set of font slots before rendering each expression, even though
it already inspects the resulting glyphs to wait for their actual faces.
Creating hidden markup synchronously under the selected metric tables removes the first
barrier. The explicit `ready()` API can retain broad warmup for callers that request it.
Its three-second timeout is a failure ceiling, not an intentional delay.

Build-time KaTeX HTML alone cannot guarantee final width; it still depends on decoded
glyph advances. Nor is KaTeX’s private HTML tree a reliable width calculator: combined
text such as `ilMW1/` and `minimum` keeps a single glyph’s stored width.
Reimplementing CSS layout around these internals would create another layout engine to
maintain.

The publication browser can instead measure the final boxes under the page’s actual CSS
after fonts load. Reserve width, height, and baseline offset for each KaTeX `.base`,
which is already unbreakable.
Preserve breaks between bases, the original MathML, and selectable HTML. Whole-formula
inline blocks were rejected because they prevent normal equation wrapping.
Hydration must reuse geometry only when source, display mode, and font profile match;
changed input or a stock-font opt-out needs a normal render.

This design moves computation into publication and adds prepared-markup metadata.
Its main risks are browser differences, display-versus-print sizing, stale interactive
values, incorrect line breaks, and a missing font stranding hidden content.
Those need independent regression checks, even if timings improve.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
