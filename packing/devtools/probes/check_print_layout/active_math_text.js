// The text of the matched nodes that belong to the active saved-font profile. Semantic
// MathML is clipped even for active math, so its profile is selected from metadata rather
// than visual visibility, and dormant variants cannot duplicate fraction terms.
//
// Takes the matched nodes, then `math`, the math library (`math/library.js`), through a
// handle.
/**
 * @param {Element[]} nodes
 * @param {{ math: SquaresMathProbes }} o
 */
(nodes, o) => {
  const { activeVariant } = o.math;
  return nodes.filter(activeVariant).map((node) => node.textContent);
};
