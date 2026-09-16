// Diagnostic control and treatment use the snapshot's visible-text traversal.
// Both arms select and observe the same nodes after settlement; only the treatment
// replaces each selected Text node with a new Text node containing its exact data.
// Refuse a truncated selection before changing the DOM, since a partial intervention
// could look stable while leaving the omitted prepared text untouched.
//
// `snapshot` is `math_snapshot.js`'s function, handed in as a handle.
/** @param {{ rebuild: boolean, snapshot: SquaresMathSnapshotter }} o */
({ rebuild, snapshot }) => {
  /** @type {SquaresSelectedText[]} */
  const selected = [];
  const before = snapshot("before-intervention", selected);
  const beforeHtml = document.documentElement.outerHTML;
  /** @param {SquaresSelectedText[]} nodes */
  const identities = (nodes) =>
    nodes.map(({ node, formula, token, path }) => ({ formula, token, path, text: node.data }));
  /** @type {{ requested: boolean, applied: boolean, status: string, selected_count: number, selected: object[], mutated_count: number, mutated: object[], after_selected_count?: number, after_selected?: object[], html_unchanged?: boolean }} */
  const intervention = {
    requested: rebuild,
    applied: false,
    status: "control",
    selected_count: selected.length,
    selected: identities(selected),
    mutated_count: 0,
    mutated: [],
  };
  if (before.truncated) {
    intervention.status = "refused";
    return {
      snapshots: [before],
      intervention,
      error: "prepared-text selection truncated before replacement",
    };
  }
  if (!selected.length) {
    intervention.status = "no-targets";
    return {
      snapshots: [before],
      intervention,
      error: "no visible prepared-text nodes selected",
    };
  }
  if (rebuild) {
    for (const { node, formula, token, path } of selected) {
      const text = node.data;
      /** @type {ParentNode & Node} */ (node.parentNode).replaceChild(
        document.createTextNode(text),
        node,
      );
      intervention.mutated.push({ formula, token, path, text });
    }
    intervention.mutated_count = intervention.mutated.length;
    intervention.applied = true;
    intervention.status = "applied";
  }
  /** @type {SquaresSelectedText[]} */
  const afterSelected = [];
  const after = snapshot("after-intervention", afterSelected);
  const afterIdentities = identities(afterSelected);
  intervention.after_selected_count = afterSelected.length;
  intervention.after_selected = afterIdentities;
  intervention.html_unchanged = beforeHtml === document.documentElement.outerHTML;
  const same = JSON.stringify(intervention.selected) === JSON.stringify(afterIdentities);
  if (after.truncated || !same || !intervention.html_unchanged) {
    intervention.status = "verification-failed";
    return {
      snapshots: [before, after],
      intervention,
      error: "prepared-text identities changed during diagnostic intervention",
    };
  }
  return { snapshots: [before, after], intervention };
};
