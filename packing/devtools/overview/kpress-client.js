/* kpress client behaviors, flattened from {{KPRESS_CLIENT_MODULES}} */
// A report page's contents rail and hash navigation are kpress's own: the scroll-spy
// that marks the section in view, the narrow-screen drawer, and Back and Forward
// restoring the reading position. The modules register their behaviors as they load
// and kpress's runtime binds them once the document is ready, so this frame adds
// nothing around them. `render_overview.kpress_client_script` fills the sentinel.
(() => {
  __SQUARES_KPRESS_CLIENT_JS__();
  // Badge explanations use the same placement, without enabling link previews.
  behaviors.override("tooltip", () => undefined);
  behaviors.override("footnote-preview", () => undefined);
  globalThis.siteKpressTooltipPosition = positionTooltip;
})();
