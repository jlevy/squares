/* kpress client behaviors, flattened from {{KPRESS_CLIENT_MODULES}} */
(() => {
  __SQUARES_KPRESS_CLIENT_JS__();
  /* This page wants footnote previews and nothing else. kpress's tooltips module
   registers two behaviors at import — hover previews for internal links, and
   footnote previews — and the runtime binds both once the document is ready,
   which here would hang a preview reading "1" off every footnote's back-arrow.
   The link behavior is overridden with a no-op bind before that pass runs; the
   footnote one is left alone, and the page boots it explicitly as well. The
   copy button is kpress's own too: its behavior binds itself at the runtime's
   ready pass, and the boot below runs it earlier so the control is there before
   the reader can reach the block. */
  behaviors.override("tooltip", () => undefined);
  window.kpressInitTooltips = initKpressTooltips;
  window.kpressInitCodeCopy = initKpressCodeCopy;
  globalThis.siteKpressTooltipPosition = positionTooltip;
})();
