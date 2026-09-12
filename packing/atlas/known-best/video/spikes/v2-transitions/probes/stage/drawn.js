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
      const m = /rotate\(([-0-9.eE+]+)\)/.exec(g.getAttribute("transform"));
      return [
        Number(g.dataset.identity),
        m ? Number(m[1]) : 0,
        g.firstElementChild.getAttribute("fill"),
      ];
    });
