// The case popover's head as the browser lays it out now: the close cross's left and
// right edges, the right edge of the last of the record's steps (the next case's link),
// and the panel's right edge inside its border. Null until the popover shows a record.
() => {
  const popover = document.querySelector("[data-case-popover]");
  const cross = popover?.querySelector(".site-popover-close");
  const expand = popover?.querySelector(".site-popover-expand");
  const controls = popover?.querySelector(".site-popover-controls");
  const steps = [...(popover?.querySelectorAll("[data-case-body] .site-case-steps a") ?? [])];
  const next = steps[steps.length - 1];
  if (!popover || !cross || !expand || !controls || !next) {
    return null;
  }
  const panel = popover.getBoundingClientRect();
  const box = cross.getBoundingClientRect();
  const hit = document.elementFromPoint((box.left + box.right) / 2, (box.top + box.bottom) / 2);
  return {
    controls_top: controls.getBoundingClientRect().top,
    expand_left: expand.getBoundingClientRect().left,
    expand_right: expand.getBoundingClientRect().right,
    next_top: next.getBoundingClientRect().top,
    next_bottom: next.getBoundingClientRect().bottom,
    pager_math: steps.map((step) => ({
      text: step.querySelector(".kpress-math-semantic math")?.textContent,
      family: step.querySelector(".katex")
        ? getComputedStyle(step.querySelector(".katex")).fontFamily
        : null,
      prepared: step.querySelectorAll('[data-kpress-math-prepared="true"]').length,
    })),
    cross_left: box.left,
    cross_right: box.right,
    next_right: next.getBoundingClientRect().right,
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
