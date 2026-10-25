// The case popover's head as the browser lays it out now: the close cross's and the
// expand link's edges, the controls' top, and the panel's right edge inside its border.
// Null until the popover shows a record. The record's own head, its title line and the
// drawing above it, is `case_title_line/read.js`.
() => {
  const popover = document.querySelector("[data-case-popover]");
  const cross = popover?.querySelector(".site-popover-close");
  const expand = popover?.querySelector(".site-popover-expand");
  const controls = popover?.querySelector(".site-popover-controls");
  const article = popover?.querySelector("[data-case-body] article.site-case");
  if (!popover || !cross || !expand || !controls || !article) {
    return null;
  }
  const panel = popover.getBoundingClientRect();
  const box = cross.getBoundingClientRect();
  const hit = document.elementFromPoint((box.left + box.right) / 2, (box.top + box.bottom) / 2);
  return {
    controls_top: controls.getBoundingClientRect().top,
    expand_left: expand.getBoundingClientRect().left,
    expand_right: expand.getBoundingClientRect().right,
    cross_left: box.left,
    cross_right: box.right,
    panel_right: panel.left + popover.clientLeft + popover.clientWidth,
    cross_width: box.width,
    cross_height: box.height,
    cross_top: box.top,
    cross_bottom: box.bottom,
    panel_top: panel.top,
    panel_bottom: panel.bottom,
    scroll_top: popover.scrollTop,
    hit: hit === cross || (hit !== null && cross.contains(hit)),
  };
};
