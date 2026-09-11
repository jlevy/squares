// Every fill the page draws over every pair, at rest, at the arrival and mid block
// motion, beside the shade table and the two colours the page reserves.
() => {
  const api = window.atlasTransitions;
  api.setCapture(true);
  api.setDesaturate(false);
  // Revision 12: the angle map is one of three schemes now, and not the default.
  if (api.setColorScheme) {
    api.setColorScheme("angle-stable");
  }
  const seen = new Set();
  const collect = () => {
    const n = api.state().n;
    /** @type {NodeListOf<SVGGElement>} */ (
      document.querySelectorAll("#squares g[data-identity]")
    ).forEach((g) => {
      if (Number(g.dataset.identity) <= n) {
        seen.add(g.firstElementChild.getAttribute("fill"));
      }
    });
  };
  const count = api.pairs().length;
  for (let i = 0; i < count; i++) {
    api.select(i);
    const sc = api.schedule();
    for (const t of [0, sc.arrived, (sc.blocksStart + sc.blocksEnd) / 2, 2.8]) {
      api.seek(t);
      collect();
    }
  }
  const colour = api.colour();
  const token = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return {
    fills: Array.from(seen),
    shades: colour.shades,
    palette: colour.palette,
    reserved: [token("--new"), token("--met")],
  };
};
