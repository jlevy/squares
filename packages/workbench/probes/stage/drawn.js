// Every visible square, as [identity, the angle it is drawn at, the fill it is painted with].
// The angle is read off the transform because `state()` carries no per-square pose; the
// transform is `translate(x y) rotate(a)`, with a `scale(k)` after it while the new square
// is inflating.
() =>
  Array.from(
    /** @type {NodeListOf<SVGGElement>} */ (document.querySelectorAll("#squares g[data-identity]")),
  )
    .filter((g) => g.style.display !== "none")
    .map((g) => {
      const transform = g.getAttribute("transform");
      const m = transform == null ? null : /rotate\(([-0-9.eE+]+)\)/.exec(transform);
      const rect = g.firstElementChild;
      if (rect == null) {
        throw new Error(`square identity ${g.dataset.identity} has no drawn rect`);
      }
      return [Number(g.dataset.identity), m ? Number(m[1]) : 0, rect.getAttribute("fill")];
    });
