// Put the stage on one pair under one style and colour rule. Takes {index, style, rule}.
//
// `setColorRule` is declared with no parameter: the colouring is one map now and the call is a
// no-op kept for callers. This tool still hands it the rule, as it always has, so the call is
// typed as the one-argument call it makes rather than changed.
/** @param {{index: number, style: string, rule: string}} o */
(o) => {
  window.atlasTransitions.select(o.index);
  window.atlasTransitions.setStyle(o.style);
  /** @type {(rule: string) => import("../../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasScheme} */ (
    window.atlasTransitions.setColorRule
  )(o.rule);
};
