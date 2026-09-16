// The centre each of these identities is drawn at, in the order asked. Takes {identities}.
/** @param {{identities: number[]}} o */
(o) =>
  o.identities.map((id) => {
    const g = document.querySelector(`#squares g[data-identity="${id}"]`);
    if (g == null) {
      throw new Error(`probe requires square identity ${id}`);
    }
    const transform = g.getAttribute("transform");
    const m = transform == null ? null : /translate\(([-\d.e]+) ([-\d.e]+)\)/.exec(transform);
    if (m?.[1] === undefined || m[2] === undefined) {
      throw new Error(`square identity ${id} has no translation`);
    }
    return [parseFloat(m[1]), parseFloat(m[2])];
  });
