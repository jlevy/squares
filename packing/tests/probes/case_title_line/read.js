// The case record's title line as the browser lays it out: the count, the arrow step on
// either side of it, the drawing's frame below it and, in the case popover, the corner's
// icons above it. Read from the record the open case popover shows, or else from the page's own.
// Null until a record with a title line is shown.
() => {
  const popover = document.querySelector("[data-case-popover]:popover-open");
  const article =
    popover?.querySelector("article.site-case") ?? document.querySelector("article.site-case");
  const line = article?.querySelector(".site-case-title-line");
  const title = line?.querySelector(":scope > .site-case-title");
  const count = title?.querySelector(".katex");
  const figure = article?.querySelector(".site-case-head > .site-case-figure");
  const frame = figure?.querySelector(":scope > svg > rect");
  if (!(article && line && title && count && figure && frame)) {
    return null;
  }
  /** @param {Element} node */
  const box = (node) => {
    const { left, right, top, bottom, width, height } = node.getBoundingClientRect();
    return { left, right, top, bottom, width, height };
  };
  /** @param {string} rel */
  const step = (rel) => {
    const link = line.querySelector(`.site-case-steps > a[rel~="${rel}"]`);
    if (!(link instanceof HTMLAnchorElement)) {
      return null;
    }
    const area = box(link);
    const arrow = link.querySelector(".site-icon-arrow");
    const hit = document.elementFromPoint(
      (area.left + area.right) / 2,
      (area.top + area.bottom) / 2,
    );
    return {
      ...area,
      arrow: arrow ? box(arrow) : null,
      label: link.getAttribute("aria-label"),
      tooltip: link.getAttribute("title"),
      text: (link.textContent ?? "").trim(),
      color: getComputedStyle(link).color,
      hit: hit !== null && link.contains(hit),
    };
  };
  const ink = article.querySelector(".site-case-links a");
  const controls = popover?.querySelector(".site-popover-controls");
  const titleHit = document.elementFromPoint(
    (box(count).left + box(count).right) / 2,
    (box(count).top + box(count).bottom) / 2,
  );
  return {
    article: box(article),
    line: box(line),
    title: box(title),
    count: box(count),
    tag: title.tagName.toLowerCase(),
    titleHit: titleHit !== null && title.contains(titleHit),
    figure: box(figure),
    frame: box(frame),
    prev: step("prev"),
    next: step("next"),
    ink: ink ? getComputedStyle(ink).color : null,
    controls: controls ? box(controls) : null,
    rem: Number.parseFloat(getComputedStyle(document.documentElement).fontSize),
  };
};
