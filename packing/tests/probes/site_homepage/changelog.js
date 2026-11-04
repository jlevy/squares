// The home page's News and Changelog sections as a reader meets them: the section order,
// each section's own buttons, the Changelog's day blocks and the lines that show, where
// it sits in the page and the inks it is drawn in.
async () => {
  await document.fonts.ready;
  const heading = document.getElementById("changelog");
  const log = heading?.nextElementSibling;
  const actions = log?.nextElementSibling;
  const news = document.getElementById("news");
  /** @param {Element | null | undefined} row */
  const links = (row) =>
    [...(row?.querySelectorAll("a") ?? [])].map((link) => ({
      label: link.textContent?.trim(),
      href: link.getAttribute("href"),
    }));
  // The News box's buttons: the action row closing the News section, before the
  // Changelog's heading.
  let newsRow = heading?.previousElementSibling;
  while (newsRow && !newsRow.matches(".site-action-row") && newsRow !== news) {
    newsRow = newsRow.previousElementSibling;
  }
  /** @param {Element} element */
  const box = (element) => {
    const rect = element.getBoundingClientRect();
    return { width: rect.width, height: rect.height };
  };
  const blocks = [...(log?.querySelectorAll(":scope > details") ?? [])];
  const frame = log?.getBoundingClientRect();
  const style = log ? getComputedStyle(log) : null;
  // The ground the section is drawn on: the nearest ancestor that paints one.
  let ground = log ?? null;
  while (ground && getComputedStyle(ground).backgroundColor === "rgba(0, 0, 0, 0)") {
    ground = ground.parentElement;
  }
  const top = newsRow?.getBoundingClientRect().top ?? 0;
  const bottom = actions?.getBoundingClientRect().bottom ?? 0;
  return {
    heading: heading?.tagName,
    title: heading?.textContent?.trim(),
    order: [...document.querySelectorAll("h2.site-title")].map((title) => title.id),
    log_class: log?.className,
    news_actions: newsRow?.matches(".site-action-row") ? links(newsRow) : [],
    actions: actions?.matches(".site-action-row") ? links(actions) : [],
    days: blocks.map((block) => {
      const items = [...block.querySelectorAll("li")];
      return {
        day: block.getAttribute("data-day"),
        id: block.id,
        open: block instanceof HTMLDetailsElement && block.open,
        lines: items.length,
        // A closed disclosure keeps its lines laid out but unrendered, which only
        // `checkVisibility` reads.
        visible: items.filter((item) => item.checkVisibility({ visibilityProperty: true })).length,
        summary: block.querySelector("summary")?.textContent?.replace(/\s+/g, " ").trim(),
        box: box(block),
      };
    }),
    box: log ? box(log) : null,
    // Every shown element, each line box of a wrapped link included, inside the
    // section's own box: text that runs out of its day is clipped there, which the
    // page's own overflow never shows.
    outside: [...(log?.querySelectorAll("*") ?? [])]
      .filter(
        (element) =>
          frame &&
          element.checkVisibility({ visibilityProperty: true }) &&
          [...element.getClientRects()].some(
            (rect) =>
              rect.width > 0 && (rect.left < frame.left - 0.5 || rect.right > frame.right + 0.5),
          ),
      )
      .map((element) => element.textContent?.trim().slice(0, 60)),
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    text: style?.color,
    background: ground ? getComputedStyle(ground).backgroundColor : null,
    // The stretch from News's buttons to the Changelog's, in the document's coordinates,
    // for a review screenshot.
    clip: { y: top + window.scrollY, height: bottom - top },
  };
};
