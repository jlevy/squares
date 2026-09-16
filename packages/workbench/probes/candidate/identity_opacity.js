// How far in one identity's square is. Takes {identity}.
/** @param {{identity: number}} o */
(o) => {
  const square = document.querySelector(`#squares g[data-identity="${o.identity}"]`);
  if (square == null) {
    throw new Error(`probe requires square identity ${o.identity}`);
  }
  return square.getAttribute("opacity");
};
