// The `transform` attribute of each node, in order. For a locator's `evaluate_all`, which hands
// the probe every element the locator matches.
/** @param {Element[]} nodes */
(nodes) => nodes.map((node) => node.getAttribute("transform"));
